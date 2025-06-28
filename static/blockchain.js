 // MetaMask and Web3 Integration
const web3 = new Web3(window.ethereum);

// Check if MetaMask is installed
function isMetaMaskInstalled() {
    return typeof window.ethereum !== 'undefined';
}

// Connect to MetaMask wallet
async function connectWallet() {
    try {
        if (!isMetaMaskInstalled()) {
            throw new Error('Please install MetaMask to connect your wallet');
        }

        // Request account access
        const accounts = await window.ethereum.request({ 
            method: 'eth_requestAccounts' 
        });
        
        if (!accounts || accounts.length === 0) {
            throw new Error('No accounts found. Please unlock MetaMask.');
        }
        
        return accounts[0];
    } catch (error) {
        console.error('Wallet connection error:', error);
        throw error;
    }
}

// Get wallet balance
async function getWalletBalance(address) {
    try {
        const balance = await window.ethereum.request({
            method: 'eth_getBalance',
            params: [address, 'latest']
        });
        return web3.utils.fromWei(balance, 'ether');
    } catch (error) {
        console.error('Error getting balance:', error);
        throw error;
    }
}

// Get network information
async function getNetworkInfo() {
    try {
        const chainId = await window.ethereum.request({ method: 'eth_chainId' });
        const networkId = await window.ethereum.request({ method: 'net_version' });
        
        return {
            chainId: parseInt(chainId, 16),
            networkId: parseInt(networkId)
        };
    } catch (error) {
        console.error('Error getting network info:', error);
        throw error;
    }
}

// Validate data with MetaMask
async function validateWithMetaMask(dataId, isApproved) {
    try {
        if (!isMetaMaskInstalled()) {
            throw new Error('Please install MetaMask to validate data');
        }

        // Request account access
        const accounts = await window.ethereum.request({ 
            method: 'eth_requestAccounts' 
        });
        const validatorAddress = accounts[0];

        // Get transaction details from server
        const response = await fetch('/validate_with_metamask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                data_id: dataId,
                is_approved: isApproved,
                validator_address: validatorAddress
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Validation request failed');
        }

        const result = await response.json();
        
        if (result.error) {
            throw new Error(result.error);
        }

        // Send transaction through MetaMask
        const txHash = await window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [result.transaction]
        });

        // Update transaction status
        const statusResponse = await fetch('/update_transaction_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                transaction_id: result.transaction.transaction_id,
                tx_hash: txHash,
                status: 'completed'
            })
        });

        if (!statusResponse.ok) {
            throw new Error('Failed to update transaction status');
        }

        return txHash;
    } catch (error) {
        console.error('Validation error:', error);
        throw error;
    }
}

// Update wallet address
async function updateWalletAddress(address) {
    try {
        const response = await fetch('/update_wallet_address', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                wallet_address: address
            }),
            credentials: 'same-origin'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update wallet address');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error updating wallet address:', error);
        throw error;
    }
}

// Listen for account changes
if (isMetaMaskInstalled()) {
    window.ethereum.on('accountsChanged', function (accounts) {
        // Reload the page when the user changes accounts
        window.location.reload();
    });

    window.ethereum.on('chainChanged', function (chainId) {
        // Reload the page when the user changes networks
        window.location.reload();
    });
}

// Export functions for use in other scripts
window.blockchain = {
    connectWallet,
    getWalletBalance,
    getNetworkInfo,
    validateWithMetaMask,
    updateWalletAddress,
    isMetaMaskInstalled
};