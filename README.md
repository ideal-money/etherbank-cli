# etherbank-cli
Command line interfaces to work with etherbank, oracles and liquidator smart contracts

### Prerequisite
- Python3.6+

### Install
```
git clone https://github.com/ideal-money/etherbank-cli.git
cd etherbank-cli
pip install .
```

### Run

You can use this client to work with `etherbank`, `oracles` and `liquidator` smart contracts which are deployed on ropsten network.

```
$ export ETHERBANK_PRIVATEKEY="YOUR PRIVATE KEY"

$ etherbank get-loan --ether 0.5 --dollar 20
tx: 0x884f4707e67571e48dff17ed77ef6d5739db577c414c332fe26db6cf4a169b6c

$ etherbank loans-list
loadId:		3
collateral:	0.5 ether
amount:		20.0 dollar

$ etherbank increase-collateral --ether 0.2 --loan-id 3
tx: 0xa9ecc44fdde2fcec4f0f70fb5c90d060c95bf4803e9c44f05a81e097620824c1

$ etherbank loans-list
loadId:		3
collateral:	0.7 ether
amount:		20.0 dollar

$ etherbank get-balance
Balance: 20.0 dollar

$ etherbank settle-loan --dollar 10 --loan-id 3
Approve transferring 10.0 dollars from your account by the contract
tx: 0x388e369388b45665275e31672294bb4c7a1aa4bdd78ef06adf97a149616c0b8c

Settle loan
tx: 0xf0fdd0fe43412e77c30e49a2bcc81fc32cb3570384e6edba9d4dc2f8cc63ab67

$ etherbank get-balance
Balance: 10.0 dollar

$ etherbank loans-list
loadId:		3
collateral:	0.35 ether
amount:		10.0 dollar

$ etherbank settle-loan --dollar 10 --loan-id 3
Approve transferring 10.0 dollars from your account by the contract
tx: 0x13cb4dbbe4c38629ed3cc25f748ba28daadda1a5f1ab0c41aba8fedbc1ed8f83

Settle loan
tx: 0x48d4c6c03700f0c642ccb5043198b213a0cf3a081fd289bf909f5036e77b2c32

$ etherbank loans-list
loadId:		3
collateral:	0.0 ether
amount:		0.0 dollar
```


### Commands List 

| etherbank               |                                             |
| ----------------------- | ------------------------------------------- |
|  `allowance`            | Get Ether dollar account's balance          |
|  `get-balance`          | Get Ether dollar account's balance          |
|  `get-loan`             | Get Ether dollar loan by depositing ETH     |
|  `get-variables`        | Get the current variables' value            |
|  `increase-collateral`  | Increase the loan's collateral              |
|  `liquidate`            | Start the liquidation proccess              |
|  `loans-list`           | Get the account's loans or the specify loan |
|  `settle-loan`          | Settle the Ether dollar loan                |

| liquidator              |                                                         |
| ------------------------|---------------------------------------------------------|
|  `active-liquidations`  | Get list of active liquidations                         |  
|  `get-best-bid`         | Get the best bid amount and the bidder's address for... |
|  `place-bid`            | Place a bid on the liquidation                          |
|  `stop-liquidation`     | Stop the finalized liquidation                          |
|  `withdraw`             | Withdraw the leftover Ether dollar from liquidations    |

| oracles              |                                                |
|----------------------|------------------------------------------------|
| `finish-recruiting`  | Set recruiting as finished                     |
|  `get-variables`     | Get the current variables' value               |
|  `set-score`         | Edit oracle's score                            |
|  `vote`              | Vote on the variable for setting up Ether Bank |


To find more information about each command, you can use --help. For example:
```
$ etherbank get-loan --help
Usage: etherbank get-loan [OPTIONS]

  Get Ether dollar loan by depositing ETH

Options:
  --ether FLOAT       The collateral amount in ETH  [required]
  --dollar FLOAT      The loan amount in Ether dollar  [required]
  --private-key TEXT  The privat key to sign the transaction
  --help              Show this message and exit
```

