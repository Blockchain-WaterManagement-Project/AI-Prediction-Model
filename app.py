
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from web3 import Web3
import os
import torch
import joblib
import numpy as np
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///water_quality.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Connect to Ethereum Mainnet
#alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/3OqltayCdWx7230AEE3WNjtBp-xdAqoN"
#web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Connect to Sepolia Test Network
#sepolia_rpc_url = "https://sepolia-testnet-rpc.com"
#web3_sepolia = Web3(Web3.HTTPProvider(sepolia_rpc_url))
bsc_testnet_url = "https://bsc-testnet.public.blastapi.io"
web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))

# Verify connection and retry if needed
max_retries = 3
retry_count = 0
while not web3.is_connected() and retry_count < max_retries:
    print(f"Attempting to connect to BSC Testnet (attempt {retry_count + 1}/{max_retries})...")
    web3 = Web3(Web3.HTTPProvider(bsc_testnet_url))
    retry_count += 1

if not web3.is_connected():
    print("Failed to connect to BSC Testnet after multiple attempts")
else:
    print("Successfully connected to BSC Testnet")
    print(f"Current block number: {web3.eth.block_number}")

# Load the trained model and scaler
# Define the WaterQualityModel class (as it was in train_model.py)
class TransformerModel(torch.nn.Module):
    def __init__(self, input_dim):
        super(TransformerModel, self).__init__()
        self.fc = torch.nn.Linear(input_dim, 2) # Output 2 classes: potable or not potable

    def forward(self, x):
        return self.fc(x)

#model = torch.load('water_quality_model.pth', weights_only=False)
def get_model():
    if not hasattr(get_model, 'model'):
        try:
            get_model.model = torch.load('water_quality_model.pth', weights_only=False)
            get_model.model.eval()
        except Exception as e:
            print(f"Error loading model: {e}")
            get_model.model = None
    return get_model.model
#scaler = joblib.load('scaler.pkl')
#model.eval() # Set the model to evaluation mode
def get_scaler():
    if not hasattr(get_scaler, 'scaler'):
        try:
            get_scaler.scaler = joblib.load('scaler.pkl')
        except Exception as e:
            print(f"Error loading scaler: {e}")
            get_scaler.scaler = None
    return get_scaler.scaler

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    wallet_address = db.Column(db.String(42), nullable=True)  # Ethereum addresses are 42 chars (0x + 40 hex)

class WaterData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ph = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    acidity = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    validated = db.Column(db.Boolean, default=False)
    validator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    validation_timestamp = db.Column(db.DateTime, nullable=True)  # Add this line
    user = db.relationship('User', foreign_keys=[user_id], backref='water_data')
    validator = db.relationship('User', foreign_keys=[validator_id], backref='validated_data')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # 'incentive', 'penalty', 'validation'
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed'
    water_data_id = db.Column(db.Integer, db.ForeignKey('water_data.id', name='fk_transaction_water_data'), nullable=True)  # Add this line
    blockchain_tx_hash = db.Column(db.String(66), nullable=True)  # Add this line
    user = db.relationship('User', backref='transactions')
    water_data = db.relationship('WaterData', backref='transactions')  # Add this line

class DataSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prediction = db.Column(db.Integer, nullable=False)  # 0 or 1
    confidence = db.Column(db.Float, nullable=False)
    wallet_address = db.Column(db.String(42))  # Ethereum address
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_validated = db.Column(db.Boolean, default=False)
    is_valid = db.Column(db.Boolean, default=None)
    validated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    validation_timestamp = db.Column(db.DateTime)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return render_template('signup.html')
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/api/dashboard_stats')
def dashboard_stats():
    if 'role' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    stats = {}
    if session['role'] == 'user':
        # Basic water data stats
        stats.update({
            'userDataCount': WaterData.query.filter_by(user_id=session['user_id']).count(),
            'userValidatedCount': WaterData.query.filter_by(user_id=session['user_id'], validated=True).count(),
            'userPendingCount': WaterData.query.filter_by(user_id=session['user_id'], validated=False).count()
        })
        
        # Transaction statistics
        user_transactions = Transaction.query.filter_by(user_id=session['user_id']).all()
        
        # Transaction counts by type
        incentive_count = sum(1 for tx in user_transactions if tx.transaction_type == 'incentive')
        penalty_count = sum(1 for tx in user_transactions if tx.transaction_type == 'penalty')
        validation_count = sum(1 for tx in user_transactions if tx.transaction_type == 'validation')
        
        # Transaction amounts
        total_incentives = sum(tx.amount for tx in user_transactions if tx.transaction_type == 'incentive' and tx.status == 'completed')
        total_penalties = sum(tx.amount for tx in user_transactions if tx.transaction_type == 'penalty' and tx.status == 'completed')
        total_validations = sum(tx.amount for tx in user_transactions if tx.transaction_type == 'validation' and tx.status == 'completed')
        
        # Blockchain statistics
        blockchain_transactions = [tx for tx in user_transactions if tx.blockchain_tx_hash]
        pending_transactions = [tx for tx in user_transactions if tx.status == 'pending']
        completed_transactions = [tx for tx in user_transactions if tx.status == 'completed']
        failed_transactions = [tx for tx in user_transactions if tx.status == 'failed']
        
        # Wallet statistics
        user = User.query.get(session['user_id'])
        wallet_connected = 1 if user and user.wallet_address else 0
        
        stats.update({
            # Transaction counts
            'totalTransactions': len(user_transactions),
            'incentiveCount': incentive_count,
            'penaltyCount': penalty_count,
            'validationCount': validation_count,
            
            # Transaction amounts
            'totalIncentives': round(total_incentives, 8),
            'totalPenalties': round(total_penalties, 8),
            'totalValidations': round(total_validations, 8),
            'netRewards': round(total_incentives - total_penalties, 8),
            
            # Blockchain stats
            'blockchainTransactions': len(blockchain_transactions),
            'pendingTransactions': len(pending_transactions),
            'completedTransactions': len(completed_transactions),
            'failedTransactions': len(failed_transactions),
            
            # Wallet stats
            'walletConnected': wallet_connected,
            'blockchainType': 'BSC Testnet' if web3.is_connected() else 'Not Connected'
        })
        
    elif session['role'] == 'government':
        stats = {
            'pendingValidation': WaterData.query.filter_by(validated=False).count(),
            'validatedByMe': WaterData.query.filter_by(validator_id=session['user_id']).count()
        }
    elif session['role'] == 'admin':
        stats = {
            'totalUsers': User.query.count(),
            'totalWaterData': WaterData.query.count(),
            'validatedData': WaterData.query.filter_by(validated=True).count(),
            'pendingData': WaterData.query.filter_by(validated=False).count()
        }
    return jsonify(stats)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/create_water_data', methods=['GET', 'POST'])
def create_water_data():
    if 'username' in session and session['role'] == 'user':
        if request.method == 'POST':
            ph = float(request.form['ph'])
            color = request.form['color']
            acidity = float(request.form['acidity'])
            negative_values = ph < 0 or acidity < 0

            new_data = WaterData(ph=ph, color=color, acidity=acidity, user_id=session['user_id'])
            db.session.add(new_data)
            db.session.commit()

            # Get user's wallet status
            user = User.query.get(session['user_id'])
            has_wallet = user and user.wallet_address

            if negative_values:
                if has_wallet:
                    flash('Data created with negative values. You will need to pay a penalty if validated.')
                else:
                    flash('Data created with negative values. Connect your wallet to enable penalties.')
            else:
                if has_wallet:
                    flash('Data created successfully. Awaiting validation for potential rewards.')
                else:
                    flash('Data created successfully. Connect your wallet to receive validation rewards.')

            return redirect(url_for('dashboard'))
        return render_template('create_water_data.html')
    return redirect(url_for('login'))

@app.route('/view_water_data')
def view_water_data():
    if 'username' in session and session['role'] == 'user':
        water_data = WaterData.query.filter_by(user_id=session['user_id']).all()
        transactions = Transaction.query.filter_by(user_id=session['user_id']).all()

        # Get validator information
        validator_usernames = {}
        for data in water_data:
            if data.validator_id:
                validator = User.query.get(data.validator_id)
                if validator:
                    validator_usernames[data.validator_id] = validator.username

        return render_template('view_water_data.html', water_data=water_data, transactions=transactions, validator_usernames=validator_usernames)
    return redirect(url_for('login'))

@app.route('/manage_users')
def manage_users():
    if 'username' in session and session['role'] == 'admin':
        users = User.query.all()
        return render_template('manage_users.html', users=users)
    return redirect(url_for('login'))

@app.route('/validate_data')
def validate_data():
    if 'username' in session and session['role'] == 'government':
        water_data = WaterData.query.filter_by(validated=False).all()
        # Get user information for each water data entry
        user_info = {}
        for data in water_data:
            user = User.query.get(data.user_id)
            if user:
                user_info[data.id] = user.username
        return render_template('validate_data.html', water_data=water_data, user_info=user_info)
    return redirect(url_for('login'))

@app.route('/update_wallet_address', methods=['POST'])
def update_wallet_address():
    app.logger.debug("Received update_wallet_address request")
    app.logger.debug(f"Session data: {session}")
    app.logger.debug(f"Request headers: {request.headers}")
    app.logger.debug(f"Request data: {request.get_data()}")
    
    if 'username' not in session:
        app.logger.debug("User not logged in")
        return jsonify({'error': 'Not logged in'}), 401
        
    if not request.is_json:
        app.logger.debug("Request is not JSON")
        return jsonify({'error': 'Request must be JSON'}), 400
        
    try:
        data = request.get_json()
        app.logger.debug(f"Parsed JSON data: {data}")
        
        if not data:
            app.logger.debug("No data provided")
            return jsonify({'error': 'No data provided'}), 400
            
        wallet_address = data.get('wallet_address')
        if not wallet_address:
            app.logger.debug("No wallet address provided")
            return jsonify({'error': 'Wallet address is required'}), 400
            
        try:
            # Validate and convert to checksum address
            app.logger.debug(f"Converting wallet address to checksum: {wallet_address}")
            wallet_address = web3.to_checksum_address(wallet_address)
            app.logger.debug(f"Converted wallet address: {wallet_address}")
        except ValueError as e:
            app.logger.error(f"Invalid wallet address: {str(e)}")
            return jsonify({'error': f'Invalid wallet address: {str(e)}'}), 400
            
        # Update user's wallet address
        app.logger.debug(f"Looking up user with ID: {session['user_id']}")
        user = User.query.get(session['user_id'])
        if not user:
            app.logger.error(f"User not found with ID: {session['user_id']}")
            return jsonify({'error': 'User not found'}), 404
            
        app.logger.debug(f"Updating wallet address for user: {user.username}")
        user.wallet_address = wallet_address
        db.session.commit()
        app.logger.debug("Database update successful")
        
        return jsonify({
            'message': 'Wallet address updated successfully',
            'wallet_address': wallet_address
        }), 200
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating wallet address: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
    
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', 
                             username=session['username'], 
                             role=session['role'],
                             wallet_address=user.wallet_address)
    return redirect(url_for('login'))

@app.route('/validate/<int:data_id>')
def validate(data_id):
    if 'username' in session and session['role'] == 'government':
        data = WaterData.query.get_or_404(data_id)
        data.validated = True
        data.validator_id = session['user_id']
        user = User.query.get(data.user_id)
        
        # Create an incentive transaction
        # Placeholder for actual MetaMask transaction
        # incentive_amount = 0.00000034  # Incentive amount in ETH
        # tx = {
        #     'to': ACCOUNT.address,
        #     'value': web3.toWei(incentive_amount, 'ether'),
        #     'gas': 2000000,
        #     'gasPrice': web3.toWei('20', 'gwei'),
        #     'nonce': web3.eth.getTransactionCount(ACCOUNT.address),
        # }
        # signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        # tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Add incentive transaction to database
        # incentive_transaction = Transaction(user_id=user.id, transaction_type='incentive', amount=incentive_amount)
        # db.session.add(incentive_transaction)
        db.session.commit()

        flash(f'Data validated successfully. User {user.username} has been incentivized.')
        return redirect(url_for('validate_data'))
    return redirect(url_for('login'))

@app.route('/blockchain_transactions')
def blockchain_transactions():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get user's transactions
    transactions = Transaction.query.filter_by(user_id=session['user_id']).order_by(Transaction.timestamp.desc()).all()
    
    # Get blockchain details for each transaction
    transaction_details = []
    for tx in transactions:
        details = {
            'id': tx.id,
            'type': tx.transaction_type,
            'amount': tx.amount,
            'timestamp': tx.timestamp,
            'status': tx.status,
            'tx_hash': tx.blockchain_tx_hash,
            'water_data': tx.water_data
        }
        
        # If transaction is completed, get additional blockchain details
        if tx.blockchain_tx_hash:
            try:
                # Get transaction receipt
                tx_receipt = web3.eth.get_transaction_receipt(tx.blockchain_tx_hash)
                tx_details = web3.eth.get_transaction(tx.blockchain_tx_hash)
                
                details.update({
                    'block_number': tx_receipt['blockNumber'],
                    'gas_used': tx_receipt['gasUsed'],
                    'gas_price': web3.from_wei(tx_details['gasPrice'], 'gwei'),
                    'nonce': tx_details['nonce'],
                    'method': 'validateData' if tx.transaction_type == 'validation' else 'submitData'
                })
            except Exception as e:
                app.logger.error(f"Error fetching blockchain details: {str(e)}")
                details['error'] = str(e)
        
        transaction_details.append(details)
    
    return render_template('blockchain_transactions.html', 
                         transactions=transaction_details,
                         username=session['username'],
                         role=session['role'])

@app.route('/apply_penalty', methods=['POST'])
def apply_penalty():
    if 'username' in session and session['role'] == 'government':
        recipient_address = request.form.get('recipient_address')
        
        # Placeholder for actual MetaMask transaction
        # penalty_amount = 0.0000057  # Penalty amount in ETH
        # tx = {
        #     'to': recipient_address,
        #     'value': web3.toWei(penalty_amount, 'ether'),
        #     'gas': 2000000,
        #     'gasPrice': web3.toWei('20', 'gwei'),
        #     'nonce': web3.eth.getTransactionCount(ACCOUNT.address),
        # }
        # signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        # tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # Add penalty transaction to database
        # penalty_transaction = Transaction(user_id=session['user_id'], transaction_type='penalty', amount=penalty_amount)
        # db.session.add(penalty_transaction)
        db.session.commit()

        return jsonify({'message': 'Penalty applied (placeholder)'})
    return '', 403

@app.route('/update_transaction_status', methods=['POST'])
def update_transaction_status():
    if 'username' in session and session['role'] == 'government':
        try:
            data = request.get_json()
            transaction = Transaction.query.get(data['transaction_id'])
            if transaction:
                transaction.status = data['status']
                transaction.blockchain_tx_hash = data['tx_hash']
                db.session.commit()
                return jsonify({'message': 'Transaction updated'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return jsonify({'error': 'Unauthorized'}), 403
@app.route('/apply_validation', methods=['POST'])

def apply_validation():
    if 'username' in session and session['role'] == 'government':
        recipient_address = request.form.get('recipient_address')
        
        # Placeholder for actual MetaMask transaction
        # validate_amount = 0.000004  # Validation amount in ETH
        # tx = {
        #     'to': recipient_address,
        #     'value': web3.toWei(validate_amount, 'ether'),
        #     'gas': 2000000,
        #     'gasPrice': web3.toWei('20', 'gwei'),
        #     'nonce': web3.eth.getTransactionCount(ACCOUNT.address),
        # }
        # signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        # tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # Add validation transaction to database
        # validation_transaction = Transaction(user_id=session['user_id'], transaction_type='validation', amount=validate_amount)
        # db.session.add(validation_transaction)
        db.session.commit()

        return jsonify({'message': 'Validation applied (placeholder)'})
    return '', 403


@app.route('/about_us')
def about_us():
    return 'About Us Page'

@app.route('/email_us')
def email_us():
    return 'Email Us Page'

@app.route('/water_supply')
def water_supply():
    return 'Water Supply Page'

@app.route('/water_treatment')
def water_treatment():
    return 'Water Treatment Page'

@app.route('/water_discharge')
def water_discharge():
    return 'Water Discharge Page'

@app.route('/water_demand')
def water_demand():
    return 'Water Demand Page'

@app.route('/predict_quality')
def predict_quality():
    return render_template('predict_quality.html')

@app.route('/water_consumers')
def water_consumers():
    return 'Water Consumers Page'

@app.route('/prediction_history')
def prediction_history():
    return render_template('prediction_history.html')

@app.route('/quality_visualizations')
def quality_visualizations():
    return render_template('quality_visualizations.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/view_csv_data')
def view_csv_data():
    return render_template('view_csv_data.html')

@app.route('/analytics_dashboard')
def analytics_dashboard():
    return render_template('analytics_dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract features in the correct order for the water potability model
        features = [
            float(data['ph']),
            float(data['hardness']),
            float(data['solids']),
            float(data['chloramines']),
            float(data['sulfate']),
            float(data['conductivity']),
            float(data['organic_carbon']),
            float(data['trihalomethanes']),
            float(data['turbidity'])
        ]
        
        # Scale the features
        scaler = get_scaler()
        if scaler is None:
           return jsonify({'error': 'Scaler not available'}), 500
        features_scaled = scaler.transform([features])
        
        # Convert to tensor
        features_tensor = torch.FloatTensor(features_scaled)

         # Get model and make prediction
        model = get_model()  # Add this line
        if model is None:    # Add this line
            return jsonify({'error': 'Model not available'}), 500
        
        # Make prediction
        model.eval()
        with torch.no_grad():
            output = model(features_tensor)
            # For binary classification, use sigmoid to get probability
            probability = torch.sigmoid(output[0][0]).item()
            prediction = 1 if probability > 0.5 else 0
            confidence = probability if prediction == 1 else (1 - probability)
        
        return jsonify({
            'prediction': prediction,
            'confidence': confidence,
            'probability': probability,
            'features': features
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/submit_data', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        
        # Create new data submission record
        submission = DataSubmission(
            prediction=data['prediction'],
            confidence=data['confidence'],
            wallet_address=data.get('wallet_address'),
            timestamp=datetime.utcnow(),
            is_validated=False
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'submission_id': submission.id,
            'message': 'Data submitted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/validate_with_metamask', methods=['POST'])
def validate_with_metamask():
    app.logger.debug("=== Validate with MetaMask Request ===")
    app.logger.debug(f"Request Method: {request.method}")
    app.logger.debug(f"Request Headers: {dict(request.headers)}")
    app.logger.debug(f"Session Data: {dict(session)}")
    
    if 'username' not in session:
        app.logger.error("User not logged in")
        return jsonify({'error': 'Not logged in'}), 401
        
    if session.get('role') != 'government':
        app.logger.error("User is not a government validator")
        return jsonify({'error': 'Unauthorized - government access required'}), 403
        
    if not request.is_json:
        app.logger.error("Request is not JSON")
        return jsonify({'error': 'Request must be JSON'}), 400
        
    try:
        data = request.get_json()
        app.logger.debug(f"Request data: {data}")
        
        data_id = data.get('data_id')
        is_approved = data.get('is_approved')
        validator_address = data.get('validator_address')
        
        if not all([data_id, is_approved is not None, validator_address]):
            app.logger.error("Missing required fields")
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Validate addresses
        try:
            validator_address = web3.to_checksum_address(validator_address)
        except ValueError as e:
            app.logger.error(f"Invalid validator address: {str(e)}")
            return jsonify({'error': f'Invalid validator address: {str(e)}'}), 400
            
        # Get water data
        water_data = WaterData.query.get(data_id)
        if not water_data:
            app.logger.error(f"Water data not found: {data_id}")
            return jsonify({'error': 'Water data not found'}), 404
            
        if water_data.validated:
            app.logger.error("Data already validated")
            return jsonify({'error': 'Data already validated'}), 400
            
        # Get user's wallet address
        user = User.query.get(water_data.user_id)
        if not user or not user.wallet_address:
            app.logger.error("User or wallet address not found")
            return jsonify({'error': 'Recipient wallet address not set'}), 400
            
        try:
            recipient_address = web3.to_checksum_address(user.wallet_address)
        except ValueError as e:
            app.logger.error(f"Invalid recipient address: {str(e)}")
            return jsonify({'error': f'Invalid recipient address: {str(e)}'}), 400
            
        # Create transaction
        amount = web3.to_wei(0.0001 if is_approved else 0.0005, 'ether')
        gas_price = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(validator_address)
        
        transaction = {
            'from': validator_address,
            'to': recipient_address,
            'value': amount,
            'gas': 21000,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': web3.eth.chain_id
        }
        
   
        # Create transaction record
        transaction_type = 'incentive' if is_approved else 'penalty'
        db_transaction = Transaction(
           user_id=user.id,
           transaction_type=transaction_type,
           amount=web3.from_wei(amount, 'ether'),
           status='pending',
           water_data_id=water_data.id
        )

        db.session.add(db_transaction)
        db.session.commit()
        
        # Update water data
        water_data.validated = True
        water_data.validator_id = session['user_id']
        water_data.validation_timestamp = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction prepared',
            'transaction': {
                'transaction_id': db_transaction.id,
                'to': transaction['to'],
                'value': hex(transaction['value']),
                'data': '0x',
                'gas': hex(transaction['gas']),
                'gasPrice': hex(transaction['gasPrice']),
                'nonce': hex(transaction['nonce']),
                'chainId': transaction['chainId']
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in validate_with_metamask: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)


