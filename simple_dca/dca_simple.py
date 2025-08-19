import bittensor
import simple_utils as utils
from ..config import WALLET_PATH, WALLET_NAME, NETWORK, NETUIDS_TO_STAKE_SIMPLE, STAKE_AMOUNT_SIMPLE


# Setup wallet and subtensor
try:
    wallet = bittensor.wallet(path=WALLET_PATH, name=WALLET_NAME)
    subtensor = bittensor.subtensor(network=NETWORK)

except:
    print('Something went wrong connecting to the Bittensor network')
    
wallet_info = utils.WalletOperationFunctionality(wallet, subtensor) # Create wallet functionality object

wallet_info.print_balances()
wallet_info.check_netuids_to_stake(NETUIDS_TO_STAKE_SIMPLE, STAKE_AMOUNT_SIMPLE)

utils.continue_check('Correct?')

wallet_info.check_balances_for_stake()
wallet_info.organise_hotkeys_to_stake()

utils.continue_check('Continue?')

wallet_info.make_stakes()

wallet_info.__init__(wallet, subtensor) # Re-initialise wallet
wallet_info.print_balances()

