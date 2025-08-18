import bittensor
import advanced_utils as utils
from ..config import WALLET_PATH, WALLET_NAME, NETWORK, STAKE_CONFIG_ADVANCED

# Setup wallet and subtensor
try:
    wallet = bittensor.wallet(path=WALLET_PATH, name=WALLET_NAME)
    subtensor = bittensor.subtensor(network=NETWORK)

except:
    print('\nSomething went wrong connecting to the Bittensor network')
    quit()

else:
    print('\nConnection to Bittensor network successful')
    
# Create wallet functionality object
wallet_operations = utils.WalletOperationFunctionality(wallet, subtensor) 

wallet_operations.print_balances()
utils.continue_check('Correct?')

wallet_operations.config_stake_operations(STAKE_CONFIG_ADVANCED)
wallet_operations.confirm_stake_operations()
utils.continue_check('Correct?')

wallet_operations.check_balances_for_stake()
utils.continue_check('Make stakes?')

wallet_operations.make_stakes()

wallet_operations.__init__(wallet, subtensor) # Re-initialise wallet
wallet_operations.print_balances()
