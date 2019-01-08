import sys
import click
from . import utils


@click.group()
def main():
    "Simple CLI for working with Ether dollar's bank"
    pass


@main.command()
@click.option(
    '--ether', type=float, required=True, help='The collateral amount in ETH')
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def send_eth(ether, private_key):
    "Get Ether dollar loan by sending ETH"

    tx_hash = utils.send_eth(utils.addresses['etherbank'], int(ether * 10**18),
                             private_key)
    return tx_hash


@main.command()
@click.option(
    '--ether', type=float, required=True, help='The collateral amount in ETH')
@click.option(
    '--dollar',
    type=float,
    required=True,
    help='The loan amount in Ether dollar')
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def get_loan(ether, dollar, private_key):
    "Get Ether dollar loan by depositing ETH"

    func = utils.contracts['etherbank'].functions.getLoan(int(dollar * 100))
    tx_hash = utils.send_transaction(func, int(ether * 10**18), private_key)
    return tx_hash


@main.command()
@click.option(
    '--ether', type=float, required=True, help='The collateral amount in ETH')
@click.option('--loan-id', type=int, required=True, help="The loan's ID")
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def increase_collateral(ether, loan_id, private_key):
    "Increase the loan's collateral"

    func = utils.contracts['etherbank'].functions.increaseCollateral(loan_id)
    tx_hash = utils.send_transaction(func, int(ether * 10**18), private_key)
    return tx_hash


@main.command()
@click.option('--loan-id', type=int, required=True, help="The loan's ID")
@click.option(
    '--ether', type=float, required=True, help='The collateral amount in ETH')
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def decrease_collateral(ether, loan_id, private_key):
    "Decrease the loan's collateral"

    func = utils.contracts['etherbank'].functions.decreaseCollateral(
        loan_id, int(ether * 10**18))
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
@click.option(
    '--dollar',
    type=float,
    required=True,
    help='The loan amount in Ether dollar')
@click.option('--loan-id', type=int, required=True, help="The loan's ID")
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def settle_loan(dollar, loan_id, private_key):
    "Settle the Ether dollar loan"

    loan = _loans_list(None, loan_id)
    if not loan:
        click.secho('Check the loanId.', fg='red')
        sys.exit()
    if loan['amount'] < dollar:
        click.secho('The amount exceeds the loan', fg='red')
        sys.exit()
    utils.approve_amount(utils.addresses['etherbank'], dollar, private_key)
    func = utils.contracts['etherbank'].functions.settleLoan(
        loan_id, int(dollar * 100))
    print('Settle loan')
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
@click.option('--loan-id', type=int, required=True, help='The loan id')
@click.option(
    '--private-key',
    callback=utils.check_account,
    help='The privat key to sign the transaction')
def liquidate(loan_id, private_key):
    "Start the liquidation proccess"

    func = utils.contracts['etherbank'].functions.liquidate(loan_id)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


@main.command()
def get_balance():
    "Get Ether dollar account's balance"

    account = utils.current_user()
    account = utils.w3.toChecksumAddress(account)
    func = utils.contracts['etherdollar'].functions.balanceOf(account)
    result = utils.send_eth_call(func, account)
    click.secho('Balance: {} dollar'.format(result / 100.0), fg='green')
    click.secho()
    return result


@main.command()
@click.option('--dollar', type=float, help="The account's address")
def min_collateral(dollar):
    "Count min collateral for the loan"

    func = utils.contracts['etherbank'].functions.minCollateral(
        int(dollar * 100))
    result = utils.send_eth_call(func, None)
    click.secho(
        'Minimum collateral for getting {0} dollars loan is {1} ETH'.format(
            dollar, result / 10.0**18),
        fg='green')
    click.secho()
    return result


@main.command()
@click.option('--owner', required=True, help="The account's address")
@click.option('--spender', required=True, help="The account's address")
def allowance(owner, spender):
    "Get Ether dollar account's balance"

    owner = utils.w3.toChecksumAddress(owner)
    spender = utils.w3.toChecksumAddress(spender)
    func = utils.contracts['etherdollar'].functions.allowance(owner, spender)
    result = utils.send_eth_call(func, spender)
    click.secho('Allowance: {} dollar'.format(result / 100.0), fg='green')
    click.secho()
    return result


@main.command()
@click.option('--loan-id', required=True, type=int, help='The loan id')
def show(loan_id):
    "Show the specified loan"

    result = _loans_list(loan_id=loan_id)
    if not result:
        click.secho('There is no loan.', fg='green')
    else:
        click.secho('loanId:\t\t{}'.format(result[0]['loanId']), fg='green')
        click.secho(
            'collateral:\t{} ether'.format(
                round(result[0]['collateral'] * 10**-18, 10)),
            fg='green')
        click.secho(
            'amount:\t\t{} dollar'.format(result[0]['amount'] * 10**-2),
            fg='green')
        click.secho()


@main.command()
def loans_list():
    "Get list of account's loans"

    account = utils.current_user()
    result = _loans_list(account=account)
    for loan in sorted(result, key=lambda loan: loan['loanId']):
        click.secho('loanId:\t\t{}'.format(loan['loanId']), fg='green')
        click.secho(
            'collateral:\t{} ether'.format(
                round(loan['collateral'] * 10**-18, 10)),
            fg='green')
        click.secho(
            'amount:\t\t{} dollar'.format(loan['amount'] * 10**-2), fg='green')
        click.secho()
    if not result:
        click.secho('There is no loan.', fg='green')
    click.secho()


@main.command()
def liquidatable_loans():
    "Get list of liquidatable loans"

    result = []
    var = _get_variables()
    res = _loans_list()
    for loan in sorted(res, key=lambda loan: loan['loanId']):
        if loan['collateral'] * 10**-18 * var['etherPrice'] * 100.0 < var[
                'collateralRatio'] * loan['amount']:
            result.append(loan)
            click.secho('loanId:\t\t{}'.format(loan['loanId']), fg='green')
            click.secho(
                'collateral:\t{} ether'.format(
                    round(loan['collateral'] * 10**-18, 10)),
                fg='green')
            click.secho(
                'amount:\t\t{} dollar'.format(loan['amount'] * 10**-2),
                fg='green')
            click.secho()
    if not result:
        click.secho('There is no liquidatable loan.', fg='green')
    click.secho()


def _loans_list(account=None, loan_id=None):
    result = {}
    if loan_id:
        filters = {'loanId': loan_id}
    elif account:
        filters = {'recipient': account}
    else:
        filters = None
    loan_filter = utils.contracts['etherbank'].events.LoanGot.createFilter(
        fromBlock=1, toBlock='latest', argument_filters=filters)
    loans = utils.w3.eth.getLogs(loan_filter.filter_params)
    for loan_bytes in loans:
        loan = loan_filter.format_entry(loan_bytes)
        loan_id = loan['args']['loanId']
        result[loan_id] = dict(loan['args'])

        settle_filter = utils.contracts[
            'etherbank'].events.LoanSettled.createFilter(
                fromBlock=1,
                toBlock='latest',
                argument_filters={'loanId': loan_id})
        settles = utils.w3.eth.getLogs(settle_filter.filter_params)
        for settle_bytes in settles:
            settle = settle_filter.format_entry(settle_bytes)
            result[loan_id]['collateral'] -= settle['args']['collateral']
            result[loan_id]['amount'] -= settle['args']['amount']

        increase_filter = utils.contracts[
            'etherbank'].events.CollateralIncreased.createFilter(
                fromBlock=1,
                toBlock='latest',
                argument_filters={'loanId': loan_id})
        increases = utils.w3.eth.getLogs(increase_filter.filter_params)
        for increase_bytes in increases:
            increase = increase_filter.format_entry(increase_bytes)
            result[loan_id]['collateral'] += increase['args']['collateral']

        decrease_filter = utils.contracts[
            'etherbank'].events.CollateralDecreased.createFilter(
                fromBlock=1,
                toBlock='latest',
                argument_filters={'loanId': loan_id})
        decreases = utils.w3.eth.getLogs(decrease_filter.filter_params)
        for decrease_bytes in decreases:
            decrease = decrease_filter.format_entry(decrease_bytes)
            result[loan_id]['collateral'] -= decrease['args']['collateral']
    return list(result.values())


@main.command()
def get_variables():
    "Get the current variables' value"

    result = _get_variables()
    click.secho(
        'collateralRatio:\t{}'.format(result['collateralRatio']), fg='green')
    click.secho(
        'etherPrice:\t\t{} dollar'.format(result['etherPrice']), fg='green')
    click.secho(
        'liquidationDuration:\t{} minute'.format(
            result['liquidationDuration']),
        fg='green')
    click.secho()


def _get_variables():
    result = {
        'collateralRatio':
        utils.send_eth_call(
            utils.contracts['etherbank'].functions.collateralRatio(),
            None) / 1000.0,
        'etherPrice':
        utils.send_eth_call(
            utils.contracts['etherbank'].functions.etherPrice(), None) / 100.0,
        'liquidationDuration':
        utils.send_eth_call(
            utils.contracts['etherbank'].functions.liquidationDuration(), None)
        / 60.0
    }
    return (result)


if __name__ == '__main__':
    main()
