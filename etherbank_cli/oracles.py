#!/usr/local/bin/python3.7
import sha3
import click
from web3.auto import w3
from . import utils
from . import ganache as network
# import infura as network

ETHER_PRICE = 0
DEPOSIT_RATE = 1
LIQUIDATION_DURATION = 2


@click.group()
def main():
    "Simple CLI for oracles to work with Ether dollar"
    pass


@main.command()
@click.option('--ether-price', type=int, help="The variable type")
@click.option('--deposit-rate', type=int, help="The variable type")
@click.option('--liquidation-duration', type=int, help="The variable type")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def vote(ether_price, deposit_rate, liquidation_duration, private_key):
    'Vote on the variable for setting up Ether Bank'

    assert [ether_price, deposit_rate, liquidation_duration].count(None) == 2, "You should set one variable per vote"
    if ether_price:
        part2 = utils.pad32(0)
        part3 = utils.pad32(ether_price * 100)
    elif deposit_rate:
        part2 = utils.pad32(1)
        part3 = utils.pad32(deposit_rate * 1000)
    elif liquidation_duration:
        part2 = utils.pad32(2)
        part3 = utils.pad32(liquidation_duration * 60)
    part1 = sha3.keccak_256(b'vote(uint8,uint256)').hexdigest()[:8]
    data = '0x{0}{1}{2}'.format(part1, part2, part3)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['oracles'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')


@main.command()
@click.option('--oracle', required=True, help="The oracle's address")
@click.option('--score', type=int, required=True, help="The oracle's score")
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def set_score(oracle, score, private_key):
    "Edit oracle's score"

    part1 = sha3.keccak_256(b'setScore(address,uint64)').hexdigest()[:8]
    part2 = utils.pad32(utils.hex2int(oracle))
    part3 = utils.pad32(score)
    data = '0x{0}{1}{2}'.format(part1, part2, part3)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['oracles'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')


@main.command()
@click.option('--private-key', callback=utils.check_account, help='The privat key to sign the transaction')
def finish_recruiting(private_key):
    'Set recruiting as finished'

    part1 = sha3.keccak_256(b'finishRecruiting()').hexdigest()[:8]
    data = '0x{0}'.format(part1)
    raw_transaction = utils.sign_transaction(utils.cfg['addresses']['oracles'], 0, data, private_key)
    result = network.send_raw_transaction(raw_transaction)
    click.secho(result, fg='green')


@main.command()
def get_variables():
    contract = w3.eth.contract(
        address=utils.cfg['addresses']['etherbank'], abi=utils.abies['etherbank'])
    result = {
        'depositRate': contract.call().depositRate() / 1000.0,
        'etherPrice': contract.call().etherPrice() / 100.0,
        'liquidationDuration': contract.call().liquidationDuration() / 60.0
    }
    click.secho(str(result), fg='green')
    return(result)


if __name__ == '__main__':
    main()
