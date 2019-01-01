import click
from . import utils
import time


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

    dollar = _active_liquidations(private_key, liquidation_id)[0]['amount'] / 100.0
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
    '--liquidation-id', type=int, required=True, help="The liquidation's ID")
def get_best_bid(liquidation_id):
    "Get the best bid amount and the bidder's address for the liquidation"

    return _get_best_bid(liquidation_id)


def _get_best_bid(liquidation_id):
    keys = [
        'loanId', 'collateral', 'amount', 'endTime', 'bestBid', 'bestBidder',
        'state'
    ]
    res = utils.send_eth_call(
        utils.contracts['liquidator'].functions.liquidations(liquidation_id),
        None)
    result = dict(zip(keys, res))
    if result['bestBid']:
        click.secho(
            'bestBid:\t{0} ETH'.format(result['bestBid'] / 10.0**18), fg='green')
        click.secho('bidder:\t\t{0}'.format(result['bestBidder']), fg='green')
        click.secho()
    else:
        click.secho('There is no bid.', fg='green')
    return result


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
@click.option('--liquidation-id', type=int, help="The liquidation's ID")
def active_liquidations(liquidation_id):
    "Get list of active liquidations"

    return _active_liquidations(liquidation_id)


def _active_liquidations(liquidation_id=None):
    result = []
    filters = {'liquidationId': liquidation_id} if liquidation_id else None
    start_filter = utils.contracts[
        'liquidator'].events.LiquidationStarted.createFilter(
            fromBlock=1, toBlock='latest', argument_filters=filters)
    liquidations = utils.w3.eth.getLogs(start_filter.filter_params)
    for liquidation_bytes in liquidations:
        liquidation = start_filter.format_entry(liquidation_bytes)
        liquidation_id = liquidation['args']['liquidationId']
        stop_filter = utils.contracts[
            'liquidator'].events.LiquidationStopped.createFilter(
                fromBlock=1,
                toBlock='latest',
                argument_filters={'liquidationId': liquidation_id})
        stops = utils.w3.eth.getLogs(stop_filter.filter_params)
        if not stops:
            result.append(dict(liquidation['args']))
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
        _get_best_bid(int(liquidation['liquidationId']))
        click.secho()
    if not result:
        click.secho('There is no active liquidation.', fg='green')
    return result


if __name__ == '__main__':
    main()
