# ********** Please fill: **********

# E.g.
# your_wallet_path = '/enter/your/wallet/path'
# your_wallet_name = 'Wallet name'
# your_network = 'finney' # or 'test' for testnet
#
# stake_amount = 0.1 # Amount (tao) to stake per subnet
# netuids_to_stake = [1, 3, 56, 64] # List of subnets to stake into

your_wallet_path = ''
your_wallet_name = ''
your_network = 'finney'

stake_amount = 0.1
netuids_to_stake = []

# **********************************

import bittensor
import auto_dca_utils as custom

# Setup wallet
wallet = bittensor.wallet(path=your_wallet_path, name=your_wallet_name)
subtensor = bittensor.subtensor(network=your_network)

wallet_info = custom.FullWalletInfo(wallet, subtensor)

print(f'\nFor coldkey: {wallet.coldkeypub.ss58_address}')
print(f'Free tao: {wallet_info.free_tao} | Root stake: {wallet_info.root_stake} | Alpha stake: {wallet_info.alpha_stake}')
print(f'Total: {wallet_info.free_tao + wallet_info.root_stake + wallet_info.alpha_stake}')

print(f'\nYou would like to stake into the following {len(netuids_to_stake)} subnets:')
for i in range(len(netuids_to_stake)):
    print(netuids_to_stake[i])
print(f'Requiring {bittensor.Balance(stake_amount*len(netuids_to_stake))} free')

continue_check = str(input('\nCorrect? (y/n): '))
if not (continue_check == 'y' or continue_check == 'Y'):
    exit()

wallet_info.check_balances(stake_amount*len(netuids_to_stake))

wallet_info.organise_hotkeys_to_stake(netuids_to_stake)


print('\n')
if wallet_info.no_stake_flag == True:
    print('Need to make an initial stake on each subnet before using this program')
    exit()
else:
    continue_check = str(input('Correct? (y/n): '))
    if not (continue_check == 'y' or continue_check == 'Y'):
        exit()

subtensor.add_stake_multiple(wallet=wallet, netuids=netuids_to_stake, hotkey_ss58s=hotkeys_to_stake, amounts=amounts_to_stake)
print('Your stakes have been made!')

wallet_balance = wallet_info.__init__(wallet, subtensor)
print(f'Free tao: {wallet_info.free_tao} | Root stake: {wallet_info.root_stake} | Alpha stake: {wallet_info.alpha_stake}')
print(f'Total: {wallet_info.free_tao + wallet_info.root_stake + wallet_info.alpha_stake}')