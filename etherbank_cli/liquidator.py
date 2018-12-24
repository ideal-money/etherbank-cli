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
    'Place a bid on the liquidation'

    dollar = _active_liquidations(liquidation_id)[0]['loanAmount'] / 100.0
    utils.approve_amount(utils.addresses['liquidator'], dollar, private_key)
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
    'Stop the finalized liquidation'

    func = utils.contracts['liquidator'].functions.stopLiquidation(
        liquidation_id)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
@click.option(
    '--liquidation-id', type=int, required=True, help="The liquidation's ID")
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def get_best_bid(liquidation_id, private_key):
    "Get the best bid amount and the bidder's address for the liquidation"

    func = utils.contracts['liquidator'].functions.getBestBid(liquidation_id)
    result = utils.send_eth_call(func, utils.priv2addr(private_key))
    click.secho('Best bid:\t{0} ETH'.format(result[1] / 10.0**18), fg='green')
    click.secho('Bidder:\t\t{0}'.format(result[0]), fg='green')
    click.secho()
    return result


@main.command()
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def withdraw(private_key):
    'Withdraw the leftover Ether dollar from liquidations'

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
        'liquidator'].events.StartLiquidation.createFilter(
            fromBlock=1, toBlock='latest', argument_filters=filters)
    liquidations = utils.w3.eth.getLogs(start_filter.filter_params)
    for liquidation_bytes in liquidations:
        liquidation = start_filter.format_entry(liquidation_bytes)
        liquidation_id = liquidation['args']['liquidationId']
        stop_filter = utils.contracts[
            'liquidator'].events.StopLiquidation.createFilter(
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
                liquidation['collateralAmount'] * 10**-18),
            fg='green')
        click.secho(
            'loan:\t\t{} dollar'.format(liquidation['loanAmount'] * 10**-2),
            fg='green')
        click.secho(
            'startTime:\t{}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(liquidation['startTime']))),
            fg='green')
        click.secho(
            'endTime:\t{}'.format(
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(liquidation['endTime']))),
            fg='green')
        click.secho()
    if not result:
        click.secho('There is no active liquidation.', fg='green')
    click.secho()
    return result


if __name__ == '__main__':
    main()
