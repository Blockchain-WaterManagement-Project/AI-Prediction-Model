// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WaterQualityIncentives {
    address public owner;
    
    struct User {
        address userAddress;
        uint256 totalRewards;
        uint256 totalPenalties;
        uint256 dataSubmissions;
        bool isRegistered;
    }
    
    struct DataSubmission {
        address submitter;
        uint256 timestamp;
        bool isValidated;
        bool isValid;
        address validator;
        uint256 rewardAmount;
        uint256 penaltyAmount;
    }
    
    mapping(address => User) public users;
    mapping(uint256 => DataSubmission) public submissions;
    mapping(address => bool) public validators;
    
    uint256 public submissionCounter;
    uint256 public constant REWARD_AMOUNT = 0.001 ether; // 0.001 ETH reward for valid data
    uint256 public constant PENALTY_AMOUNT = 0.0005 ether; // 0.0005 ETH penalty for invalid data
    
    event UserRegistered(address indexed user);
    event DataSubmitted(uint256 indexed submissionId, address indexed submitter);
    event DataValidated(uint256 indexed submissionId, bool isValid, address indexed validator);
    event RewardPaid(address indexed user, uint256 amount);
    event PenaltyCharged(address indexed user, uint256 amount);
    event ValidatorAdded(address indexed validator);
    event ValidatorRemoved(address indexed validator);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyValidator() {
        require(validators[msg.sender], "Only validators can call this function");
        _;
    }
    
    modifier onlyRegistered() {
        require(users[msg.sender].isRegistered, "User must be registered");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        validators[msg.sender] = true; // Owner is also a validator
    }
    
    function registerUser() external {
        require(!users[msg.sender].isRegistered, "User already registered");
        
        users[msg.sender] = User({
            userAddress: msg.sender,
            totalRewards: 0,
            totalPenalties: 0,
            dataSubmissions: 0,
            isRegistered: true
        });
        
        emit UserRegistered(msg.sender);
    }
    
    function submitData() external onlyRegistered {
        submissionCounter++;
        
        submissions[submissionCounter] = DataSubmission({
            submitter: msg.sender,
            timestamp: block.timestamp,
            isValidated: false,
            isValid: false,
            validator: address(0),
            rewardAmount: 0,
            penaltyAmount: 0
        });
        
        users[msg.sender].dataSubmissions++;
        
        emit DataSubmitted(submissionCounter, msg.sender);
    }
    
    function validateData(uint256 submissionId, bool isValid) external onlyValidator {
        require(submissionId <= submissionCounter, "Invalid submission ID");
        require(!submissions[submissionId].isValidated, "Data already validated");
        
        DataSubmission storage submission = submissions[submissionId];
        submission.isValidated = true;
        submission.isValid = isValid;
        submission.validator = msg.sender;
        
        address submitter = submission.submitter;
        
        if (isValid) {
            // Reward for valid data
            submission.rewardAmount = REWARD_AMOUNT;
            users[submitter].totalRewards += REWARD_AMOUNT;
            
            // Transfer reward (if contract has sufficient balance)
            if (address(this).balance >= REWARD_AMOUNT) {
                payable(submitter).transfer(REWARD_AMOUNT);
                emit RewardPaid(submitter, REWARD_AMOUNT);
            }
        } else {
            // Penalty for invalid data
            submission.penaltyAmount = PENALTY_AMOUNT;
            users[submitter].totalPenalties += PENALTY_AMOUNT;
            
            emit PenaltyCharged(submitter, PENALTY_AMOUNT);
        }
        
        emit DataValidated(submissionId, isValid, msg.sender);
    }
    
    function addValidator(address validator) external onlyOwner {
        require(!validators[validator], "Address is already a validator");
        validators[validator] = true;
        emit ValidatorAdded(validator);
    }
    
    function removeValidator(address validator) external onlyOwner {
        require(validators[validator], "Address is not a validator");
        require(validator != owner, "Cannot remove owner as validator");
        validators[validator] = false;
        emit ValidatorRemoved(validator);
    }
    
    function getUserInfo(address userAddress) external view returns (
        uint256 totalRewards,
        uint256 totalPenalties,
        uint256 dataSubmissions,
        bool isRegistered
    ) {
        User memory user = users[userAddress];
        return (user.totalRewards, user.totalPenalties, user.dataSubmissions, user.isRegistered);
    }
    
    function getSubmissionInfo(uint256 submissionId) external view returns (
        address submitter,
        uint256 timestamp,
        bool isValidated,
        bool isValid,
        address validator,
        uint256 rewardAmount,
        uint256 penaltyAmount
    ) {
        require(submissionId <= submissionCounter, "Invalid submission ID");
        DataSubmission memory submission = submissions[submissionId];
        return (
            submission.submitter,
            submission.timestamp,
            submission.isValidated,
            submission.isValid,
            submission.validator,
            submission.rewardAmount,
            submission.penaltyAmount
        );
    }
    
    function depositFunds() external payable onlyOwner {
        // Function to deposit funds for rewards
    }
    
    function withdrawFunds(uint256 amount) external onlyOwner {
        require(address(this).balance >= amount, "Insufficient balance");
        payable(owner).transfer(amount);
    }
    
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
    
    receive() external payable {
        // Allow contract to receive ETH
    }
}

