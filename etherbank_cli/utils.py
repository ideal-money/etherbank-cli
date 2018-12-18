import os
import sys
import sha3
import json
import uuid
from web3.auto import w3
from eth_keys import keys
from . import ganache as network

abies = {
    'etherbank': '[{"constant": false, "inputs": [], "name": "unpause", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "paused", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "lastLoanId", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "liquidatorAddr", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "oracleAddr", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "depositRate", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "pause", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "etherPrice", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "liquidationDuration", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "etherDollarAddr", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"inputs": [{"name": "_tokenAdd", "type": "address"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"payable": true, "stateMutability": "payable", "type": "fallback"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "borrower", "type": "address"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateralAmount", "type": "uint256"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "LoanGot", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "borrower", "type": "address"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateralAmount", "type": "uint256"}], "name": "IncreaseCollatral", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "borrower", "type": "address"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateralAmount", "type": "uint256"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "LoanSettled", "type": "event"}, {"anonymous": false, "inputs": [], "name": "Pause", "type": "event"}, {"anonymous": false, "inputs": [], "name": "Unpause", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}], "name": "OwnershipRenounced", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}, {"indexed": true, "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"constant": false, "inputs": [{"name": "_liquidatorAddr", "type": "address"}], "name": "setLiquidator", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_tokenAdd", "type": "address"}], "name": "setEtherDollar", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_oracleAddr", "type": "address"}], "name": "setOracle", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_type", "type": "uint256"}, {"name": "value", "type": "uint256"}], "name": "setVariable", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "amount", "type": "uint256"}], "name": "getLoan", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}], "name": "increaseCollatral", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}, {"constant": false, "inputs": [{"name": "amount", "type": "uint256"}, {"name": "loanId", "type": "uint256"}], "name": "settleLoan", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}], "name": "liquidate", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "loanId", "type": "uint256"}, {"name": "amount", "type": "uint256"}, {"name": "buyer", "type": "address"}], "name": "liquidated", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}]',
    'etherdollar': '[{"constant": true, "inputs": [], "name": "mintingFinished", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transferFrom", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint32"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_to", "type": "address"}, {"name": "_amount", "type": "uint256"}], "name": "mint", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_value", "type": "uint256"}], "name": "burn", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_subtractedValue", "type": "uint256"}], "name": "decreaseApproval", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "finishMinting", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_addedValue", "type": "uint256"}], "name": "increaseApproval", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "burner", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Burn", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "to", "type": "address"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "Mint", "type": "event"}, {"anonymous": false, "inputs": [], "name": "MintFinished", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}], "name": "OwnershipRenounced", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}, {"indexed": true, "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "owner", "type": "address"}, {"indexed": true, "name": "spender", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "from", "type": "address"}, {"indexed": true, "name": "to", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"}]',
    'liquidator': '[{"constant": false, "inputs": [], "name": "unpause", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "paused", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "pause", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_tokenAddr", "type": "address"}, {"name": "_etherBankAddr", "type": "address"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "liquidationId", "type": "uint256"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "collateralAmount", "type": "uint256"}, {"indexed": false, "name": "loanAmount", "type": "uint256"}, {"indexed": false, "name": "startTime", "type": "uint256"}, {"indexed": false, "name": "endTime", "type": "uint256"}], "name": "StartLiquidation", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "liquidationId", "type": "uint256"}, {"indexed": true, "name": "loanId", "type": "uint256"}, {"indexed": false, "name": "bestBid", "type": "uint256"}, {"indexed": false, "name": "bestBidder", "type": "address"}], "name": "StopLiquidation", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "withdrawalAccount", "type": "address"}, {"indexed": false, "name": "amount", "type": "uint256"}], "name": "Withdraw", "type": "event"}, {"anonymous": false, "inputs": [], "name": "Pause", "type": "event"}, {"anonymous": false, "inputs": [], "name": "Unpause", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}], "name": "OwnershipRenounced", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}, {"indexed": true, "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"constant": false, "inputs": [{"name": "_etherBankAddr", "type": "address"}], "name": "setEtherBank", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_tokenAddr", "type": "address"}], "name": "setEtherDollar", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "getDepositAmount", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_loanId", "type": "uint256"}, {"name": "_collateralAmount", "type": "uint256"}, {"name": "_loanAmount", "type": "uint256"}], "name": "startLiquidation", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "liquidationId", "type": "uint256"}], "name": "stopLiquidation", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "liquidationId", "type": "uint256"}, {"name": "bidAmount", "type": "uint256"}], "name": "placeBid", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "liquidationId", "type": "uint256"}], "name": "getBestBid", "outputs": [{"name": "", "type": "address"}, {"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}]',
    'oracles': '[{"constant": false, "inputs": [], "name": "unpause", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "paused", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "pause", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "recruitingFinished", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_etherBankAddr", "type": "address"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "oracle", "type": "address"}, {"indexed": false, "name": "score", "type": "uint256"}], "name": "EditOracles", "type": "event"}, {"anonymous": false, "inputs": [], "name": "FinishRecruiting", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": false, "name": "oracle", "type": "address"}, {"indexed": false, "name": "_type", "type": "uint8"}, {"indexed": false, "name": "_value", "type": "uint256"}], "name": "SetVote", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "_type", "type": "uint8"}, {"indexed": false, "name": "_value", "type": "uint256"}], "name": "Update", "type": "event"}, {"anonymous": false, "inputs": [], "name": "Pause", "type": "event"}, {"anonymous": false, "inputs": [], "name": "Unpause", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}], "name": "OwnershipRenounced", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "previousOwner", "type": "address"}, {"indexed": true, "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"constant": false, "inputs": [{"name": "_etherBankAddr", "type": "address"}], "name": "setEtherBank", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_type", "type": "uint8"}, {"name": "_value", "type": "uint256"}], "name": "vote", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [{"name": "_account", "type": "address"}, {"name": "_score", "type": "uint64"}], "name": "setScore", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": false, "inputs": [], "name": "finishRecruiting", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}]'
}

cfg = {
    'gas': 5*10**6,
    'gas_price': 150*10**9
}

etherbank_address = w3.toChecksumAddress('0x3130f14038a44a11986d0f1919f68684e6fa93aa')

# export ETHERBANK_PRIVATEKEY="93449babbac70bfdefc807a0f012c74cd68f92ca35eaf952e991a329f88fc850"


def approve_amount(spender, dollar, private_key):
    part1 = sha3.keccak_256(b'approve(address,uint256)').hexdigest()[:8]
    part2 = pad32(hex2int(spender))
    part3 = pad32(dollar * 100)  # CONVERT DOLLAR TO CENT
    data = '0x{0}{1}{2}'.format(part1, part2, part3).lower()
    raw_transaction = sign_transaction(cfg['addresses']['etherdollar'], 0, data, private_key)
    network.send_raw_transaction(raw_transaction)


def get_addresses(contract_addr):
    contract = w3.eth.contract(
        address=contract_addr, abi=json.loads(abies['etherbank']))
    addresses = {
        'etherbank': contract_addr,
        'oracles': contract.call().oracleAddr(),
        'liquidator': contract.call().liquidatorAddr(),
        'etherdollar': contract.call().etherDollarAddr(),
    }
    return addresses


def start():
    global cfg
    if 'ETHERBANK_PRIVATEKEY' not in os.environ:
        print('Fisrt run:\n\t export ETHERBANK_PRIVATEKEY="your ethereum private key"')
        sys.exit()
    if os.path.exists(os.path.expanduser('~/.etherbank.json')):
        with open(os.path.expanduser('~/.etherbank.json'), 'r') as f:
            cfg['addresses'] = json.load(f)
    elif 'ETHERBANK_CONTRACTADDRESS' in os.environ:
        try:
            cfg['addresses'] = get_addresses(os.environ['ETHERBANK_CONTRACTADDRESS'])
            with open(os.path.expanduser('~/.etherbank.json'), 'w') as f:
                f.write(json.dumps(cfg['addresses']))
        except:
            print('First edit the ETHERBANK_CONTRACTADDRESS and try again')
            sys.exit()
    else:
        try:
            cfg['addresses'] = get_addresses(etherbank_address)
            with open(os.path.expanduser('~/.etherbank.json'), 'w') as f:
                f.write(json.dumps(cfg['addresses']))
        except:
            print('First remove ~/.etherbank/addresses and try again')
            sys.exit()


def check_account(ctx, param, value):
    if not value and 'ETHERBANK_PRIVATEKEY' in os.environ:
        value = os.environ['ETHERBANK_PRIVATEKEY']
    if not value:
        print('Fisrt run:\n\t export ETHERBANK_PRIVATEKEY="your ethereum private key"')
        sys.exit()
    if value.startswith('0x'):
        value = value[2:]
    return value


def priv2addr(private_key):
    pk = keys.PrivateKey(bytes.fromhex(private_key))
    return pk.public_key.to_checksum_address()


def hex2int(s):
    assert s.startswith('0x')
    return int(s[2:], 16)


def pad32(n):
    return format(int(n), '064X')


def new_address():
    rand_hex = uuid.uuid4().hex
    account = w3.eth.account.create(rand_hex)
    return (account.address, account.privateKey.hex())


def sign_transaction(contract_addr, wei_amount, data, private_key):
    transaction = {
        'to': contract_addr,
        'value': hex(int(wei_amount)),
        'gas': hex(cfg['gas']),
        'gasPrice': hex(cfg['gas_price']),
        'nonce': hex(network.get_nonce(priv2addr(private_key))),
        'data': data
    }
    signed = w3.eth.account.signTransaction(transaction, private_key)
    return signed.rawTransaction.hex()


def get_abi(contract_name):
    with open("../build/contracts/{}.json".format(contract_name)) as f:
        print(json.dumps(json.load(f)['abi']))


start()