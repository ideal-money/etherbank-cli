#!/usr/local/bin/python3.7

import click
from . import utils


@click.group()
def main():
    "Simple CLI for oracles to work with Ether dollar"
    pass


@main.command()
@click.option('--ether-price', type=float, help="The variable type")
@click.option('--deposit-rate', type=float, help="The variable type")
@click.option('--liquidation-duration', type=int, help="The variable type")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def vote(ether_price, deposit_rate, liquidation_duration, private_key):
    "Vote on the variable for setting up Ether Bank"

    assert [ether_price, deposit_rate, liquidation_duration].count(None) == 2, "You should set one variable per vote"
    if ether_price:
        var_code = 0
        value = int(ether_price * 100)
    elif deposit_rate:
        var_code = 1
        value = int(deposit_rate * 1000)
    elif liquidation_duration:
        var_code = 2
        value = liquidation_duration * 60
    func = utils.oracles_contract.functions.vote(var_code, value)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
@click.option('--oracle', required=True, help="The oracle's address")
@click.option('--score', type=int, required=True, help="The oracle's score")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def set_score(oracle, score, private_key):
    "Edit oracle's score"

    oracle = utils.w3.toChecksumAddress(oracle)
    func = utils.oracles_contract.functions.setScore(oracle, score)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def finish_recruiting(private_key):
    "Set recruiting as finished"

    func = utils.oracles_contract.functions.finishRecruiting()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
def get_variables():
    "Get the current variables' value"

    result = {
        'depositRate': utils.etherbank_contract.call().depositRate() / 1000.0,
        'etherPrice': utils.etherbank_contract.call().etherPrice() / 100.0,
        'liquidationDuration': utils.etherbank_contract.call().liquidationDuration() / 60.0
    }
    click.secho('depositRate:\t\t{}'.format(result['depositRate']), fg='green')
    click.secho('etherPrice:\t\t{} $'.format(result['etherPrice']), fg='green')
    click.secho('liquidationDuration:\t{} Min'.format(result['liquidationDuration']), fg='green')
    click.secho()
    return(result)


if __name__ == '__main__':
    main()
