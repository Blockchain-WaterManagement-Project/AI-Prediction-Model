# 🌊 Water Quality Management System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1.0-red.svg)](https://pytorch.org)
[![Web3](https://img.shields.io/badge/Web3-6.11.0-orange.svg)](https://web3py.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Revolutionizing water quality monitoring with AI and blockchain technology**

A cutting-edge water quality management system that combines artificial intelligence, blockchain technology, and user-friendly interfaces to provide comprehensive water quality monitoring, prediction, and management capabilities. Built with Flask, PyTorch, and Ethereum smart contracts.

## 🚀 Key Features

### 🤖 AI-Powered Predictions
- **Neural Network Model**: PyTorch-based model with >90% accuracy
- **Real-time Analysis**: Instant water quality assessment
- **9 Quality Parameters**: pH, hardness, TDS, chloramines, sulfate, conductivity, organic carbon, trihalomethanes, turbidity
- **Confidence Scoring**: Prediction confidence levels for reliability

### 🔗 Blockchain Integration
- **MetaMask Integration**: Secure wallet connection for users
- **Smart Contracts**: Solidity-based incentive and penalty system
- **BSC Testnet**: Binance Smart Chain integration for transactions
- **Reward System**: Earn tokens for valid data submissions
- **Transparent Validation**: Blockchain-based data verification

### 👥 Multi-Role Authentication System
- **Users**: Submit water quality data and receive AI predictions
- **Government Officials**: Validate submissions and apply penalties
- **Administrators**: System oversight and user management
- **Role-Based Access**: Granular permissions and security

### 📊 Professional Analytics Dashboard
- **Interactive Visualizations**: Real-time charts and graphs
- **Data Analytics**: Comprehensive quality metrics and KPIs
- **Transaction History**: Blockchain transaction tracking
- **User Statistics**: Performance and submission analytics

### 📱 Modern Responsive Design
- **Mobile-First**: Optimized for all devices and screen sizes
- **Bootstrap 5**: Modern, clean UI with animations
- **Professional Styling**: Gradient backgrounds and smooth transitions
- **Accessibility**: WCAG compliant design principles

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3 (Python)
- **Database**: SQLAlchemy with SQLite/PostgreSQL support
- **Authentication**: Werkzeug security with password hashing
- **API**: RESTful endpoints with JSON responses
- **Migrations**: Flask-Migrate for database versioning

### Machine Learning
- **Framework**: PyTorch 2.1.0
- **Model**: Neural Network for binary classification
- **Preprocessing**: Scikit-learn for data scaling
- **Accuracy**: >90% on water potability prediction
- **Features**: 9 water quality parameters

### Blockchain
- **Network**: BSC Testnet (Binance Smart Chain)
- **Smart Contracts**: Solidity 0.8.0
- **Web3 Integration**: Web3.py 6.11.0
- **Wallet**: MetaMask browser extension
- **Incentives**: 0.001 ETH rewards, 0.0005 ETH penalties

### Frontend
- **HTML5/CSS3**: Semantic markup with modern styling
- **JavaScript**: Interactive features and animations
- **Bootstrap 5**: Responsive grid system and components
- **Bootstrap Icons**: Professional icon set
- **Animate.css**: Smooth animations and transitions

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js (for blockchain development)
- MetaMask browser extension
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WQM
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Run database migrations**
   ```bash
   flask db upgrade
   ```

5. **Start the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5001`
   - Create an account or explore the demo features

## 📖 Usage Guide

### For Regular Users
1. **Sign Up**: Create an account with your preferred role
2. **Connect Wallet**: Link your MetaMask wallet for blockchain features
3. **Submit Data**: Enter water quality parameters (pH, hardness, TDS, etc.)
4. **Get Predictions**: Receive AI-powered quality assessments with confidence scores
5. **Earn Rewards**: Receive blockchain rewards for valid submissions

### For Government Officials
1. **Data Validation**: Review and validate submitted water quality data
2. **Apply Penalties**: Issue blockchain penalties for invalid submissions
3. **Analytics Access**: View comprehensive quality reports and statistics
4. **Transaction Management**: Oversee blockchain reward/penalty transactions

### For Administrators
1. **System Oversight**: Monitor overall system health and performance
2. **User Management**: Manage user accounts, roles, and permissions
3. **Analytics Dashboard**: Access advanced analytics and system metrics
4. **Configuration**: System settings and blockchain contract management

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Blockchain    │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • Flask API     │◄──►│ • Smart Contract│
│ • Bootstrap 5   │    │ • SQLAlchemy    │    │ • BSC Testnet   │
│ • MetaMask      │    │ • PyTorch ML    │    │ • Web3.js       │
│ • Responsive UI │    │ • Authentication│    │ • Incentives    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Machine Learning Model

### Model Performance
- **Accuracy**: 94%+ on test dataset
- **Precision**: High precision for water quality classification
- **Recall**: Excellent recall for non-potable water detection
- **F1-Score**: Balanced performance across all metrics

### Input Parameters
- **pH Level**: Acidity/alkalinity measurement
- **Hardness**: Calcium and magnesium content (mg/L)
- **Total Dissolved Solids**: TDS concentration (ppm)
- **Chloramines**: Disinfectant levels (ppm)
- **Sulfate**: Sulfate concentration (mg/L)
- **Conductivity**: Electrical conductivity (μS/cm)
- **Organic Carbon**: Total organic carbon (ppm)
- **Trihalomethanes**: THM concentration (μg/L)
- **Turbidity**: Water clarity measurement (NTU)

## 🔐 Security Features

- **Password Security**: PBKDF2-SHA256 hashing with salt
- **Session Management**: Secure user sessions with Flask
- **Role-Based Access Control**: Granular permission system
- **Input Validation**: Comprehensive data validation and sanitization
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **Blockchain Security**: Cryptographic transaction verification
- **CSRF Protection**: Cross-site request forgery prevention

## 📈 Deployment Options

### Local Development
- SQLite database for simplicity
- Single Flask development server
- Local blockchain testing

### Production Deployment
- PostgreSQL/MySQL database
- Gunicorn + Nginx setup
- Load balancing configuration
- Redis caching layer
- CDN for static assets

### Enterprise Scaling
- Microservices architecture
- Docker containerization
- Kubernetes orchestration
- Database clustering
- ML model serving
- Advanced monitoring and logging

## 🤝 Contributing

We welcome contributions from the community! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed
- Ensure responsive design compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SWUST AI and Blockchain Technology Team** for the innovative approach
- **PyTorch** for the machine learning framework
- **Flask** for the web framework
- **Bootstrap** for the responsive design components
- **Ethereum Foundation** for blockchain technology

## 📞 Support

For support, questions, or feature requests:
- Create an issue in the repository
- Contact the development team
- Check the documentation in the project wiki

---

**Built with ❤️ by the SWUST AI and Blockchain Technology Team**
