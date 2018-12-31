INFURA_URL = 'https://ropsten.infura.io/v3/c556c4fcd2d64c41baef3ef84e33052a'

ETHERBANK_ADDR = '0x0ff877052eb95e308b281b88fbc685dabcd28e50'

ABIES = {
    'etherbank':
    '[{"constant": true, "inputs": [], "name": "oraclesAddr", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "lastLoanId", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "liquidatorAddr", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "etherPrice", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "liquidationDuration", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "collateralRatio", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "etherDollarAddr", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"inputs": [{"name": "_tokenAdd", "type": "address"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"payable": true, "stateMutability": "payable", "type": "fallback"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "recipient", "type": "address"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateral", "type": "uint256"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "LoanGot", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "recipient", "type": "address"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateral", "type": "uint256"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "LoanSettled", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "recipient", "type": "address"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateral", "type": "uint256"}], "name": "CollateralIncreased", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "recipient", "type": "address"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateral", "type": "uint256"}], "name": "CollateralDecreased", "type": "event"}, {"constant": false, "inputs": [{"name": "_liquidatorAddr", "type": "address"}], "name": "setLiquidator", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_oraclesAddr", "type": "address"}], "name": "setOracle", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_type", "type": "uint8"}, {"name": "value", "type": "uint256"}], "name": "setVariable", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "amount", "type": "uint256"}], "name": "getLoan", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}], "name": "increaseCollateral", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}, {"name": "amount", "type": "uint256"}], "name": "decreaseCollateral", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}, {"name": "amount", "type": "uint256"}], "name": "settleLoan", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}], "name": "liquidate", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}, {"name": "collateral", "type": "uint256"}, {"name": "buyer", "type": "address"}], "name": "liquidated", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "amount", "type": "uint256"}], "name": "minCollateral", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}]',
    'etherdollar':
    '[{"constant": true, "inputs": [], "name": "mintingFinished", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transferFrom", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint32"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_to", "type": "address"}, {"name": "_amount", "type": "uint256"}], "name": "mint", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_value", "type": "uint256"}], "name": "burn", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_subtractedValue", "type": "uint256"}], "name": "decreaseApproval", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "finishMinting", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_addedValue", "type": "uint256"}], "name": "increaseApproval", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "burner", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Burn", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "to", "type": "address"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "Mint", "type": "event"}, {"anonymous": false, "inputs": [], "name": "MintFinished", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}], "name": "OwnershipRenounced", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}, {"indexed": true, "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "owner", "type": "address"}, {"indexed": true, "name": "spender", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "from", "type": "address"}, {"indexed": true, "name": "to", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"}]',
    'liquidator':
    '[{"constant": true, "inputs": [{"name": "", "type": "uint256"}], "name": "liquidations", "outputs": [{"name": "loanId", "type": "uint256"}, {"name": "collateral", "type": "uint256"}, {"name": "amount", "type": "uint256"}, {"name": "endTime", "type": "uint256"}, {"name": "bestBid", "type": "uint256"}, {"name": "bestBidder", "type": "address"}, {"name": "state", "type": "uint8"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "deposits", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"inputs": [{"name": "_tokenAddr", "type": "address"}, {"name": "_etherBankAddr", "type": "address"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "liquidationId", "type": "uint256"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateral", "type": "uint256"}, {"indexed": false, "name": "amount", "type": "uint256"}, {"indexed": false, "name": "endTime", "type": "uint256"}], "name": "LiquidationStarted", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "liquidationId", "type": "uint256"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "bestBid", "type": "uint256"}, {"indexed": false, "name": "bestBidder", "type": "address"}], "name": "LiquidationStopped", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "withdrawalAccount", "type": "address"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "Withdrew", "type": "event"}, {"constant": false, "inputs": [], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "loadId", "type": "uint256"}, {"name": "collateral", "type": "uint256"}, {"name": "amount", "type": "uint256"}, {"name": "duration", "type": "uint256"}], "name": "startLiquidation", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "liquidationId", "type": "uint256"}], "name": "stopLiquidation", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "liquidationId", "type": "uint256"}, {"name": "bidAmount", "type": "uint256"}], "name": "placeBid", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}]',
    'oracles':
    '[{"constant": false, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "recruitingFinished", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_etherBankAddr", "type": "address"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "oracle", "type": "address"}, {"indexed": false, "name": "score", "type": "uint256"}], "name": "EditOracles", "type": "event"}, {"anonymous": false, "inputs": [], "name": "FinishRecruiting", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "oracle", "type": "address"}, {"indexed": false, "name": "_type", "type": "uint8"}, {"indexed": false, "name": "_value", "type": "uint256"}], "name": "SetVote", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "_type", "type": "uint8"}, {"indexed": false, "name": "_value", "type": "uint256"}], "name": "Update", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}], "name": "OwnershipRenounced", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}, {"indexed": true, "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"constant": false, "inputs": [{"name": "_type", "type": "uint8"}, {"name": "_value", "type": "uint256"}], "name": "vote", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_account", "type": "address"}, {"name": "_score", "type": "uint256"}], "name": "setScore", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "finishRecruiting", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}]'
}

GAS = 500 * 10**3
GAS_PRICE = 30 * 10**9
