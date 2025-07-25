import bittensor

MINIMUM_TAO_BALANCE = 0.0000005

class WalletOperationFunctionality:
    def __init__(self, wallet, subtensor):
        self.WALLET = wallet
        self.SUBTENSOR = subtensor

        try:
            self.free_tao = float(self.SUBTENSOR.get_balance(address=self.WALLET.coldkeypub.ss58_address))
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            raise

        try:
            self.delegated_info = self.SUBTENSOR.get_delegated(coldkey_ss58=self.WALLET.coldkeypub.ss58_address)
        except Exception as e:
            print(f"Error getting delegated info: {str(e)}")
            raise

        self.delegated_info.sort(key=lambda info: info.netuid)
        self.root_stake = 0
        self.alpha_stake = 0
        self.raw_alpha_stakes_info = dict()

        for delegated_info in self.delegated_info:
            if delegated_info.netuid == 0:
                self.root_stake += float(delegated_info.stake) # Sums root stake
            else:
                try:
                    subnet_info = self.SUBTENSOR.subnet(netuid=delegated_info.netuid)

                    # Create dictionary of netuid keys and values of staking information
                    self.raw_alpha_stakes_info[delegated_info.netuid] = {
                        'netuid_name': subnet_info.subnet_name,
                        'price': subnet_info.price,
                        'delegator_hotkey': delegated_info.hotkey_ss58,
                        'delegator_owner': delegated_info.owner_ss58
                    }

                    self.alpha_stake += float(delegated_info.stake) * float(subnet_info.price)
                except Exception as e:
                    print(f"Error getting subnet {delegated_info.netuid} info: {str(e)}")
                    raise


    def print_balances(self):
        print(f'\nFor coldkey: {self.WALLET.coldkeypub.ss58_address}')
        print(f'Free tao: τ{round(self.free_tao, 4)} | Root stake: τ{round(self.root_stake, 4)} | Alpha stake: τ{round(self.alpha_stake, 4)}')
        print(f'Total: τ{self.free_tao + self.root_stake + self.alpha_stake}')

    def config_stake_operations(self, stake_config):
        self.STAKE_CONFIG = stake_config
        self.stakes_to_make_info = dict()
        self.no_stake_netuids = []

        # Cycle through subnets to stake into
        for netuid, config in self.STAKE_CONFIG.items():
            if netuid in self.raw_alpha_stakes_info:
                self.stakes_to_make_info[netuid] = self.raw_alpha_stakes_info[netuid] # Append stake info to stakes to be made 
                stake_amount = config['stake_amount']
                if config['multipliers'] is not None:
                    multiplied_stake_amount = stake_amount
                    for level, multiplier in config['multipliers']:
                        if self.stakes_to_make_info[netuid]['price'] <= level:
                            multiplied_stake_amount = stake_amount * multiplier
                    stake_amount = multiplied_stake_amount
                self.stakes_to_make_info[netuid]['amount'] = stake_amount
            else:
                self.no_stake_netuids.append(netuid)

    def confirm_stake_operations(self):
        print(f'\nReady to stake into the following {len(self.stakes_to_make_info)} subnets:')
        self.total_stake_amount = 0

        # Print the list of stakes to be made
        for netuid, info in self.stakes_to_make_info.items(): 
            try:
                delegator_name = self.SUBTENSOR.query_identity(info['delegator_owner'])
            except Exception as e:
                print(f"Error getting subnet {netuid} name: {str(e)}")
                raise

            if delegator_name is not None:
                info['delegator_name'] = delegator_name
            else:
                info['delegator_name'] = '[Name not found]'

            print(f'({netuid}) {info['netuid_name']} delegated to {info['delegator_hotkey']} ({info['delegator_name'][:6]}...): τ{info['amount']}')
            self.total_stake_amount += info['amount']
        print(f'Requiring τ{self.total_stake_amount} total')

        if self.no_stake_netuids:
            print(f'\nHowever you must manually make an initial stake into netuids {self.no_stake_netuids} first')
            exit()

    # Check through this for errors, or possible improvements
    # free tao and root stake slightly off?
    def check_balances_for_stake(self):
        if self.total_stake_amount <= (self.free_tao - MINIMUM_TAO_BALANCE): # If free tao is sufficent amount required for stake
            pass

        # If possible, unstake required amount from root
        elif self.total_stake_amount < (self.free_tao - MINIMUM_TAO_BALANCE) + (self.root_stake - MINIMUM_TAO_BALANCE):
            root_unstake_needed = self.total_stake_amount - (max(self.free_tao - MINIMUM_TAO_BALANCE, 0))
            print('\nNot enough free tao')
            continue_check(f'Would you like to unstake τ{round(root_unstake_needed, 4)} from root?')

            print('\n')
            root_unstake_made = 0
            i = 0
            while root_unstake_made < root_unstake_needed:
                # Check for subnet root and enough stake
                if self.delegated_info[i].netuid == 0 and float(self.delegated_info[i].stake) > (2 * MINIMUM_TAO_BALANCE):
                    this_stake_amount = float(self.delegated_info[i].stake - MINIMUM_TAO_BALANCE)

                    # Stake more then needed, unstake required amount
                    if root_unstake_made + this_stake_amount > root_unstake_needed:
                        unstake_amount = root_unstake_needed - root_unstake_made
                    else:
                        unstake_amount = this_stake_amount

                    try:
                        unstake_successful = self.SUBTENSOR.unstake(
                            wallet=self.WALLET,
                            netuid=0,
                            hotkey_ss58=self.delegated_info[i].hotkey_ss58,
                            amount=bittensor.Balance(float(unstake_amount))
                        )
                    except Exception as e:
                        print(f"Unstake error: {str(e)}")
                        continue
                    else:
                        if unstake_successful:
                            root_unstake_made += unstake_amount
                            print(f'τ{round(unstake_amount, 4)} unstaked from: {self.delegated_info[i].hotkey_ss58}')
                        else:
                            print(f'Unsuccessful unstaking τ{round(unstake_amount, 4)} from: {self.delegated_info[i].hotkey_ss58}')
                            quit()
                i += 1

        else:
            print(f'\nFree tao and root stake insufficient to make stake')
            exit()

    def make_stakes(self):
        # Cycle through subnet validator pairs
        for netuid, info in self.stakes_to_make_info.items():
            try:
                stake_successful = self.SUBTENSOR.add_stake(
                    wallet=self.WALLET,
                    netuid=netuid,
                    hotkey_ss58=info['delegator_hotkey'],
                    amount=bittensor.Balance(float(info['amount']))
                )
            except Exception as e:
                # Need to fix formatting if error
                print(f"Stake error on subnet {netuid}: {str(e)}")
                continue_check('Would you like to continue?')
            else:
                if stake_successful:
                    print(f'Successfully staked on ({netuid}) {info['netuid_name']} to {info['delegator_name']} ({info['delegator_hotkey'][:6]}...): {info['amount']}')
                else:
                    print(f'Failed to make a stake on ({netuid}) {info['netuid_name']} to {info['delegator_name']} ({info['delegator_hotkey'][:6]}...)')
                    continue_check('Would you like to continue?')


# Gets user input to clarify continuation
def continue_check(message):
    continue_check = str(input(f'{message} (y/n): '))
    if not (continue_check.lower() == 'y'):
        exit()