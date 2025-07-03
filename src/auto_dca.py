'''Before using enter the following:
    wallet name and path
    stake_amount (tao amount per subnet)
    netuids_to_stake (subnets to DCA into)'''



import bittensor as bt
from bittensor.utils.balance import Balance

# Setup wallet
wallet = bt.wallet(path="enter/your/wallet/path", name="Wallet Name")
subtensor = bt.subtensor(network='finney') # Or use (network='test') for testnet

# Values for staking operation
stake_amount = 0.1 # Amount (tao) to stake per subnet
netuids_to_stake = [] # List of subnets to stake into, e.g. [3, 4, 56, 64]

hotkeys_to_stake = [] # Leave empty
amounts_to_stake = [] # Leave empty


# Show balance and subnets to stake into
wallet_balance = subtensor.get_balance(address=wallet.coldkeypub.ss58_address)
print(f'Your wallet balance is: {wallet_balance}\n')

print(f'You would like to stake into the following {len(netuids_to_stake)} subnets:')
for i in range(len(netuids_to_stake)):
    print(netuids_to_stake[i])

continue_check = str(input('Correct? (y/n): '))
if not (continue_check == 'y' or continue_check == 'Y'):
    exit()

# Check required balance for stake
print(f'Requiring {stake_amount*len(netuids_to_stake)}τ free')

if stake_amount*len(netuids_to_stake) > wallet_balance:
    print('Tao balance insufficient')
    exit()
else:
    print('\n')


# Get delegation data a sort by subnet number
delegated_info = subtensor.get_delegated(coldkey_ss58=wallet.coldkeypub.ss58_address)
delegated_info.sort(key=lambda info: info.netuid)  # Sort by subnet ID

no_stake_flag = False
for netuid in netuids_to_stake:
    for i in range(len(delegated_info)):
        if netuid == delegated_info[i].netuid:
            print(f'Subnet {netuid} staked to: {delegated_info[i].hotkey_ss58}')
            hotkeys_to_stake.append(delegated_info[i].hotkey_ss58)
            amounts_to_stake.append(Balance.from_tao(stake_amount))
            break
        elif i == len(delegated_info) - 1:
            print(f'No stake for subnet: {netuid}')
            no_stake_flag = True
print('\n')

if no_stake_flag == True:
    print('Need to make an initial stake on each subnet before using this program')
    exit()

subtensor.add_stake_multiple(wallet=wallet, netuids=netuids_to_stake, hotkey_ss58s=hotkeys_to_stake, amounts=amounts_to_stake)
print('Your stakes have been made!')

wallet_balance = subtensor.get_balance(address=wallet.coldkeypub.ss58_address)
print(f'Your wallet balance is now: {wallet_balance}')