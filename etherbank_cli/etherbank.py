#!/usr/local/bin/python3.7

import click
import sha3
from web3.auto import w3
from . import utils
from . import ganache as network
# from . import infura as network


@click.group()
def main():
    "Simple CLI for working with Ether dollar's bank"
    pass


@main.command()
@click.option('--ether', type=float, required=True, help='The collateral amount in ETH')
@click.option('--dollar', type=float, required=True, help='The loan amount in Ether dollar')
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def get_loan(ether, dollar, private_key):
    'Get Ether dollar loan by depositing ETH'

    part1 = sha3.keccak_256(b'getLoan(uint256)').hexdigest()[:8]
    part2 = utils.pad32(int(dollar) * 100)  # CONVERT DOLLAR TO CENT
    data = '0x{0}{1}'.format(part1, part2)
    raw_transaction = utils.sign_transaction(
        utils.cfg['addresses']['etherbank'],
        int(ether) * 10**18,  # CONVERT ETHER TO WEI
        data,
        private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')
    return result


@main.command()
@click.option('--ether', type=float, required=True, help='The collateral amount in ETH')
@click.option('--loan_id', type=int, required=True, help="The loan's ID")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def increase_collateral(ether, loan_id, private_key):
    "Increase the loan's collateral"
    part1 = sha3.keccak_256(b'increaseCollatral(uint256)').hexdigest()[:8]
    part2 = utils.pad32(loan_id)
    data = '0x{0}{1}'.format(part1, part2)
    raw_transaction = utils.sign_transaction(
        utils.cfg['addresses']['etherbank'],
        int(ether) * 10**18,  # CONVERT ETHER TO WEI
        data,
        private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')
    return result


@main.command()
@click.option('--dollar', type=float, required=True, help='The loan amount in Ether dollar')
@click.option('--loan_id', type=int, required=True, help="The loan's ID")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def settle_loan(dollar, loan_id, private_key):
    'Settle the Ether dollar loan'

    utils.approve_amount(utils.cfg['addresses']['etherbank'], dollar, private_key)
    part1 = sha3.keccak_256(b'settleLoan(uint256,uint256)').hexdigest()[:8]
    part2 = utils.pad32(dollar * 100)
    part3 = utils.pad32(loan_id)
    data = '0x{0}{1}{2}'.format(part1, part2, part3)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['etherbank'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')
    return result


@main.command()
@click.option('--loan_id', type=int, required=True, help='The loan id')
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def liquidate(loan_id, private_key):
    'Start the liquidation proccess'

    part1 = sha3.keccak_256(b'liquidate(uint256)').hexdigest()[:8]
    part2 = utils.pad32(loan_id)
    data = '0x{0}{1}'.format(part1, part2)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['etherbank'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')
    return result


@main.command()
@click.option('--account', required=True, help="The account's address")
def get_balance(account):
    "Get Ether dollar account's balance"

    part1 = sha3.keccak_256(b'balanceOf(address)').hexdigest()[:8]
    part2 = utils.pad32(utils.hex2int(account))
    data = '0x{0}{1}'.format(part1, part2)
    result = network.send_eth_call(account, data, utils.cfg['addresses']['etherdollar'])
    click.secho(str(utils.hex2int(result) / 100.0), fg='green')


@main.command()
@click.option('--account', help="The user's address")
@click.option('--loan_id', type=int, help='The loan id')
def loans(account, loan_id):
    result = {}
    if account is None and loan_id is None:
        click.secho('Enther an account or a loan ID', fg='red')
    ether_bank_contract = w3.eth.contract(
        address=utils.cfg['addresses']['etherbank'], abi=utils.abies['etherbank'])
    if loan_id:
        loan_filter = ether_bank_contract.events.LoanGot.createFilter(
            fromBlock=1, toBlock='latest', argument_filters={'loanId': loan_id})
    else:
        loan_filter = ether_bank_contract.events.LoanGot.createFilter(
            fromBlock=1, toBlock='latest', argument_filters={'borrower': account})
    for loan in loan_filter.get_all_entries():
        loan_id = loan['args']['loanId']
        result[loan_id] = dict(loan['args'])
        settle_filter = ether_bank_contract.events.LoanSettled.createFilter(
            fromBlock=1,
            toBlock='latest',
            argument_filters={'loanId': loan_id})
        for settle in settle_filter.get_all_entries():
            result[loan_id]['collateralAmount'] -= settle['args'][
                'collateralAmount']
            result[loan_id]['amount'] -= settle['args']['amount']
    for loan in sorted(result.values(), key=lambda loan: loan['loanId']):
        click.secho('loadId:\t\t{}'.format(loan['loanId']), fg='green')
        click.secho('collateral:\t{} ether'.format(loan['collateralAmount']*10**-18), fg='green')
        click.secho('amount:\t\t{} dollar'.format(loan['amount']*10**-2), fg='green')
        click.secho()
    return result.values()


@main.command()
def get_variables():
    contract = w3.eth.contract(
        address=utils.cfg['addresses']['etherbank'], abi=utils.abies['etherbank'])
    result = {
        'depositRate': contract.call().depositRate() / 1000.0,
        'etherPrice': contract.call().etherPrice() / 100.0
    }
    click.secho(str(result), fg='green')
    return(result)


if __name__ == '__main__':
    main()
