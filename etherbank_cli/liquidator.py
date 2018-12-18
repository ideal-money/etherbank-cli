#!/usr/local/bin/python3.7

import sha3
import click
from web3.auto import w3
from . import ganache as network
# from . import infura as network
from . import utils


@click.group()
def main():
    "Simple CLI for working with Ether dollar's liquidator"
    pass


@main.command()
@click.option('--liquidation_id', type=int, required=True, help="The liquidation's ID")
@click.option('--ether', type=float, required=True, help="The bid's amount")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def place_bid(liquidation_id, ether, private_key):
    'Place a bid on the liquidation'

    dollar = _active_liquidations(liquidation_id)[0]['loanAmount']
    utils.approve_amount(utils.cfg['addresses']['liquidator'], dollar, private_key)
    part1 = sha3.keccak_256(b'placeBid(uint256,uint256)').hexdigest()[:8]
    part2 = utils.pad32(liquidation_id)
    part3 = utils.pad32(ether * 10**18)
    data = '0x{0}{1}{2}'.format(part1, part2, part3)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['liquidator'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')


@main.command()
@click.option('--liquidation_id', type=int, required=True, help="The liquidation's ID")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def stop_liquidation(liquidation_id, private_key):
    'Stop the finalized liquidation'

    part1 = sha3.keccak_256(b'stopLiquidation(uint256)').hexdigest()[:8]
    part2 = utils.pad32(liquidation_id)
    data = '0x{0}{1}'.format(part1, part2)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['liquidator'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')


@main.command()
@click.option('--liquidation_id', type=int, required=True, help="The liquidation's ID")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def get_best_bid(liquidation_id, private_key):
    "Get the best bid amount and the bidder's address for the liquidation"

    part1 = sha3.keccak_256(b'getBestBid(uint256)').hexdigest()[:8]
    part2 = utils.pad32(liquidation_id)
    data = '0x{0}{1}'.format(part1, part2)
    result = network.send_eth_call(utils.priv2addr(private_key), data, utils.cfg['addresses']['liquidator'])
    click.secho('{0}, {1}'.format(result[:66], (utils.hex2int('0x{0}'.format(result[66:]))) / 10.0**18), fg='green')


@main.command()
@click.option('--dollar', type=int, required=True, help='The amount to withdraw')
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def withdraw(dollar, private_key):
    'Withdraw the leftover Ether dollar from liquidations'

    part1 = sha3.keccak_256(b'withdraw(uint256)').hexdigest()[:8]
    part2 = utils.pad32(dollar * 100)
    data = '0x{0}{1}'.format(part1, part2)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['liquidator'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')


@main.command()
@click.option('--loan_id', type=int, help="The loan's ID")
def active_liquidations(loan_id):
    return _active_liquidations(loan_id)


def _active_liquidations(loan_id=None):
    result = []
    liquidator_contract = w3.eth.contract(
        address=utils.cfg['addresses']['liquidator'], abi=utils.abies['liquidator'])
    filters = {'loanId': loan_id} if loan_id else None
    start_filter = liquidator_contract.events.StartLiquidation.createFilter(
        fromBlock=1, toBlock='latest', argument_filters=filters)
    for liquidation in start_filter.get_all_entries():
        liquidation_id = liquidation['args']['liquidationId']
        stop_filter = liquidator_contract.events.StopLiquidation.createFilter(
            fromBlock=1,
            toBlock='latest',
            argument_filters={'liquidationId': liquidation_id})
        if not stop_filter.get_all_entries():
            result.append(dict(liquidation['args']))
    click.secho(str(result), fg='green')
    return result


if __name__ == '__main__':
    main()
