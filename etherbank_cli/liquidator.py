import time
import sys
import click
from . import utils


@click.group()
def main():
    "Simple CLI for working with Ether dollar's liquidator"
    pass


@main.command()
@click.option(
    '--liquidation-id', type=int, required=True, help="The liquidation's ID")
@click.option('--ether', type=float, required=True, help="The bid's amount")
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def place_bid(liquidation_id, ether, private_key):
    "Place a bid on the liquidation"

    liquidation = _show(liquidation_id)
    if not ether < liquidation['bestBid'] * 10**-18:
        click.secho('Inadequate bidding', fg='red')
        click.secho()
        sys.exit()
    dollar = liquidation['amount'] / 100.0
    utils.approve_amount(utils.addresses['liquidator'], dollar, private_key)
    print('Place bid')
    func = utils.contracts['liquidator'].functions.placeBid(
        liquidation_id, int(ether * 10**18))
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
@click.option(
    '--liquidation-id', type=int, required=True, help="The liquidation's ID")
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def stop_liquidation(liquidation_id, private_key):
    "Stop the finalized liquidation"

    func = utils.contracts['liquidator'].functions.stopLiquidation(
        liquidation_id)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def withdraw(private_key):
    "Withdraw the leftover Ether dollar from liquidations"

    func = utils.contracts['liquidator'].functions.withdraw()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
def active_liquidations():
    "Get list of active liquidations"

    result = []
    start_filter = utils.contracts[
        'liquidator'].events.LiquidationStarted.createFilter(
            fromBlock=1, toBlock='latest')
    liquidations = utils.w3.eth.getLogs(start_filter.filter_params)
    for liquidation_bytes in liquidations:
        liquidation = start_filter.format_entry(liquidation_bytes)
        liquidation_id = liquidation['args']['liquidationId']
        liquidation = _show(liquidation_id)
        if liquidation['amount'] != 0 and liquidation['state'] == 'active':
            result.append(liquidation)
    for liquidation in sorted(
            result, key=lambda liquidation: liquidation['liquidationId']):
        click.secho(
            'liquidationId:\t{}'.format(liquidation['liquidationId']),
            fg='green')
        click.secho('loanId:\t\t{}'.format(liquidation['loanId']), fg='green')
        click.secho(
            'collateral:\t{} ether'.format(
                liquidation['collateral'] * 10**-18),
            fg='green')
        click.secho(
            'loan:\t\t{} dollar'.format(liquidation['amount'] * 10**-2),
            fg='green')
        click.secho(
            'endTime:\t{}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(liquidation['endTime']))),
            fg='green')
        click.secho(
            'bestBid:\t{0} ether'.format(liquidation['bestBid'] / 10.0**18),
            fg='green')
        click.secho(
            'bidder:\t\t{0}'.format(liquidation['bestBidder']), fg='green')
        click.secho()
    if not result:
        click.secho('There is no active liquidation.', fg='green')


@main.command()
@click.option('--liquidation-id', type=int, help="The liquidation's ID")
def show(liquidation_id):
    "Show the specified liquidation"

    liquidation = _show(liquidation_id)
    click.secho(
        'liquidationId:\t{}'.format(liquidation['liquidationId']), fg='green')
    click.secho('loanId:\t\t{}'.format(liquidation['loanId']), fg='green')
    click.secho(
        'collateral:\t{} ether'.format(liquidation['collateral'] * 10**-18),
        fg='green')
    click.secho(
        'loan:\t\t{} dollar'.format(liquidation['amount'] * 10**-2),
        fg='green')
    click.secho(
        'endTime:\t{}'.format(
            time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime(liquidation['endTime']))),
        fg='green')
    click.secho(
        'bestBid:\t{0} ether'.format(liquidation['bestBid'] / 10.0**18),
        fg='green')
    click.secho('bidder:\t\t{0}'.format(liquidation['bestBidder']), fg='green')
    click.secho('state:\t\t{0}'.format(liquidation['state']), fg='green')
    click.secho()


def _show(liquidation_id):
    liquidation_params = [
        'loanId', 'collateral', 'amount', 'endTime', 'bestBid', 'bestBidder',
        'state'
    ]
    liquidation_satates = ['active', 'finished']
    liquidation = dict(
        zip(
            liquidation_params,
            utils.send_eth_call(
                utils.contracts['liquidator'].functions.liquidations(
                    liquidation_id), None)))
    liquidation['state'] = liquidation_satates[liquidation['state']]
    liquidation['liquidationId'] = liquidation_id
    return liquidation


if __name__ == '__main__':
    main()
