// MetaMask and Web3 Integration for Water Quality Management
class WaterQualityBlockchain {
    constructor() {
        this.web3 = null;
        this.contract = null;
        this.userAccount = null;
        this.contractAddress = '0x776A1E56d80feC35C7b16476116C4257e061C223'; // Replace with actual deployed contract address
        this.contractABI = [
            {
                "inputs": [],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "uint256",
                        "name": "submissionId",
                        "type": "uint256"
                    },
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "submitter",
                        "type": "address"
                    }
                ],
                "name": "DataSubmitted",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "uint256",
                        "name": "submissionId",
                        "type": "uint256"
                    },
                    {
                        "indexed": false,
                        "internalType": "bool",
                        "name": "isValid",
                        "type": "bool"
                    },
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "validator",
                        "type": "address"
                    }
                ],
                "name": "DataValidated",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "user",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "PenaltyCharged",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "user",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "RewardPaid",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "user",
                        "type": "address"
                    }
                ],
                "name": "UserRegistered",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "validator",
                        "type": "address"
                    }
                ],
                "name": "ValidatorAdded",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "validator",
                        "type": "address"
                    }
                ],
                "name": "ValidatorRemoved",
                "type": "event"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "validator",
                        "type": "address"
                    }
                ],
                "name": "addValidator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "depositFunds",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getContractBalance",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "submissionId",
                        "type": "uint256"
                    }
                ],
                "name": "getSubmissionInfo",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "submitter",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isValidated",
                        "type": "bool"
                    },
                    {
                        "internalType": "bool",
                        "name": "isValid",
                        "type": "bool"
                    },
                    {
                        "internalType": "address",
                        "name": "validator",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "rewardAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "penaltyAmount",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "userAddress",
                        "type": "address"
                    }
                ],
                "name": "getUserInfo",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "totalRewards",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "totalPenalties",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "dataSubmissions",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isRegistered",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "owner",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "PENALTY_AMOUNT",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "registerUser",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "validator",
                        "type": "address"
                    }
                ],
                "name": "removeValidator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "REWARD_AMOUNT",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "submissionCounter",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "name": "submissions",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "submitter",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isValidated",
                        "type": "bool"
                    },
                    {
                        "internalType": "bool",
                        "name": "isValid",
                        "type": "bool"
                    },
                    {
                        "internalType": "address",
                        "name": "validator",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "rewardAmount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "penaltyAmount",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "submitData",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "name": "users",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "userAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "totalRewards",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "totalPenalties",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "dataSubmissions",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isRegistered",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "submissionId",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bool",
                        "name": "isValid",
                        "type": "bool"
                    }
                ],
                "name": "validateData",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "name": "validators",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "withdrawFunds",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "stateMutability": "payable",
                "type": "receive"
            }
        ];
    }

    // Initialize Web3 and connect to MetaMask
    async init() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                // Request account access
                await window.ethereum.request({ method: 'eth_requestAccounts' });
                
                // Initialize Web3
                this.web3 = new Web3(window.ethereum);
                
                // Get user account
                const accounts = await this.web3.eth.getAccounts();
                this.userAccount = accounts[0];
                
                // Initialize contract
                this.contract = new this.web3.eth.Contract(this.contractABI, this.contractAddress);
                
                // Listen for account changes
                window.ethereum.on('accountsChanged', (accounts) => {
                    this.userAccount = accounts[0];
                    this.updateUI();
                });
                
                // Listen for network changes
                window.ethereum.on('chainChanged', () => {
                    window.location.reload();
                });
                
                this.updateUI();
                return true;
            } catch (error) {
                console.error('Error connecting to MetaMask:', error);
                this.showError('Failed to connect to MetaMask. Please try again.');
                return false;
            }
        } else {
            this.showError('MetaMask is not installed. Please install MetaMask to use blockchain features.');
            return false;
        }
    }

    // Check if MetaMask is connected
    isConnected() {
        return this.web3 !== null && this.userAccount !== null;
    }

    // Register user on blockchain
    async registerUser() {
        if (!this.isConnected()) {
            await this.init();
        }

        try {
            this.showLoading('Registering user on blockchain...');
            
            const tx = await this.contract.methods.registerUser().send({
                from: this.userAccount,
                gas: 200000
            });
            
            this.showSuccess('User registered successfully on blockchain!');
            this.updateUI();
            return tx;
        } catch (error) {
            console.error('Error registering user:', error);
            this.showError('Failed to register user on blockchain.');
            throw error;
        }
    }

    // Submit data to blockchain
    async submitDataToBlockchain() {
        if (!this.isConnected()) {
            await this.init();
        }

        try {
            this.showLoading('Submitting data to blockchain...');
            
            const tx = await this.contract.methods.submitData().send({
                from: this.userAccount,
                gas: 200000
            });
            
            this.showSuccess('Data submitted to blockchain successfully!');
            return tx;
        } catch (error) {
            console.error('Error submitting data:', error);
            this.showError('Failed to submit data to blockchain.');
            throw error;
        }
    }

    // Validate data (for government officials)
    async validateData(submissionId, isValid) {
        if (!this.isConnected()) {
            await this.init();
        }

        try {
            this.showLoading('Validating data on blockchain...');
            
            const tx = await this.contract.methods.validateData(submissionId, isValid).send({
                from: this.userAccount,
                gas: 300000
            });
            
            this.showSuccess(`Data ${isValid ? 'approved' : 'rejected'} successfully!`);
            return tx;
        } catch (error) {
            console.error('Error validating data:', error);
            this.showError('Failed to validate data on blockchain.');
            throw error;
        }
    }

    // Get user information from blockchain
    async getUserInfo(address = null) {
        if (!this.isConnected()) {
            return null;
        }

        try {
            const userAddress = address || this.userAccount;
            const userInfo = await this.contract.methods.getUserInfo(userAddress).call();
            
            return {
                totalRewards: this.web3.utils.fromWei(userInfo.totalRewards, 'ether'),
                totalPenalties: this.web3.utils.fromWei(userInfo.totalPenalties, 'ether'),
                dataSubmissions: userInfo.dataSubmissions,
                isRegistered: userInfo.isRegistered
            };
        } catch (error) {
            console.error('Error getting user info:', error);
            return null;
        }
    }

    // Get submission information
    async getSubmissionInfo(submissionId) {
        if (!this.isConnected()) {
            return null;
        }

        try {
            const submissionInfo = await this.contract.methods.getSubmissionInfo(submissionId).call();
            
            return {
                submitter: submissionInfo.submitter,
                timestamp: new Date(submissionInfo.timestamp * 1000),
                isValidated: submissionInfo.isValidated,
                isValid: submissionInfo.isValid,
                validator: submissionInfo.validator,
                rewardAmount: this.web3.utils.fromWei(submissionInfo.rewardAmount, 'ether'),
                penaltyAmount: this.web3.utils.fromWei(submissionInfo.penaltyAmount, 'ether')
            };
        } catch (error) {
            console.error('Error getting submission info:', error);
            return null;
        }
    }

    // Get contract balance
    async getContractBalance() {
        if (!this.isConnected()) {
            return '0';
        }

        try {
            const balance = await this.contract.methods.getContractBalance().call();
            return this.web3.utils.fromWei(balance, 'ether');
        } catch (error) {
            console.error('Error getting contract balance:', error);
            return '0';
        }
    }

    // Check if user is a validator
    async isValidator(address = null) {
        if (!this.isConnected()) {
            return false;
        }

        try {
            const userAddress = address || this.userAccount;
            return await this.contract.methods.validators(userAddress).call();
        } catch (error) {
            console.error('Error checking validator status:', error);
            return false;
        }
    }

    // Update UI elements
    updateUI() {
        if (this.userAccount) {
            // Update wallet address display
            const walletElements = document.querySelectorAll('.wallet-address');
            walletElements.forEach(element => {
                element.textContent = `${this.userAccount.substring(0, 6)}...${this.userAccount.substring(38)}`;
            });

            // Show connected state
            const connectButtons = document.querySelectorAll('.connect-wallet-btn');
            connectButtons.forEach(button => {
                button.textContent = 'Wallet Connected';
                button.classList.add('btn-success');
                button.classList.remove('btn-primary');
                button.disabled = true;
            });

            // Update user info
            this.updateUserInfo();
        }
    }

    // Update user blockchain information
    async updateUserInfo() {
        const userInfo = await this.getUserInfo();
        if (userInfo) {
            // Update rewards display
            const rewardsElements = document.querySelectorAll('.user-rewards');
            rewardsElements.forEach(element => {
                element.textContent = `${userInfo.totalRewards} ETH`;
            });

            // Update penalties display
            const penaltiesElements = document.querySelectorAll('.user-penalties');
            penaltiesElements.forEach(element => {
                element.textContent = `${userInfo.totalPenalties} ETH`;
            });

            // Update submissions count
            const submissionsElements = document.querySelectorAll('.user-submissions');
            submissionsElements.forEach(element => {
                element.textContent = userInfo.dataSubmissions;
            });

            // Update registration status
            const registrationElements = document.querySelectorAll('.registration-status');
            registrationElements.forEach(element => {
                element.textContent = userInfo.isRegistered ? 'Registered' : 'Not Registered';
                element.classList.toggle('text-success', userInfo.isRegistered);
                element.classList.toggle('text-warning', !userInfo.isRegistered);
            });
        }
    }

    // Show loading message
    showLoading(message) {
        this.showNotification(message, 'info');
    }

    // Show success message
    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    // Show error message
    showError(message) {
        this.showNotification(message, 'error');
    }

    // Show notification
    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
}

// Initialize blockchain integration
const waterQualityBlockchain = new WaterQualityBlockchain();

// Connect wallet function
async function connectWallet() {
    await waterQualityBlockchain.init();
}

// Register user function
async function registerUserOnBlockchain() {
    try {
        await waterQualityBlockchain.registerUser();
    } catch (error) {
        console.error('Registration failed:', error);
    }
}

// Submit data to blockchain function
async function submitToBlockchain() {
    try {
        await waterQualityBlockchain.submitDataToBlockchain();
    } catch (error) {
        console.error('Submission failed:', error);
    }
}

// Validate data function (for government officials)
async function validateDataOnBlockchain(submissionId, isValid) {
    try {
        await waterQualityBlockchain.validateData(submissionId, isValid);
    } catch (error) {
        console.error('Validation failed:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Auto-connect if MetaMask is available
    if (typeof window.ethereum !== 'undefined') {
        waterQualityBlockchain.init().catch(console.error);
    }
});

