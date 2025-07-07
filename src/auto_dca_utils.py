import bittensor

class FullWalletInfo:
    def __init__(self, wallet, subtensor):
        self.wallet = wallet
        self.subtensor = subtensor
        self.free_tao = float(self.subtensor.get_balance(address=self.wallet.coldkeypub.ss58_address)) # Gets free tao balance
        
        self.delegated_info = self.subtensor.get_delegated(coldkey_ss58=self.wallet.coldkeypub.ss58_address)
        self.delegated_info.sort(key=lambda info: info.netuid)  # Sort by netuid

        self.root_stake = 0
        self.alpha_stake = 0
        for info in self.delegated_info:
            if info.netuid == 0:
                self.root_stake += float(info.stake) # Sums root stake

            else:
                subnet_info = self.subtensor.subnet(netuid=info.netuid)
                self.alpha_stake += float(info.stake) * float(subnet_info.price) # Converts alpha stake to tao and sums

    def print_balances(self):
        print(f'\nFor coldkey: {self.wallet.coldkeypub.ss58_address}')
        print(f'Free tao: τ{self.free_tao} | Root stake: τ{self.root_stake} | Alpha stake: τ{self.alpha_stake}')
        print(f'Total: τ{self.free_tao + self.root_stake + self.alpha_stake}')

    def check_netuids_to_stake(self, netuids_to_stake, stake_amount):
        self.netuids_to_stake = netuids_to_stake
        self.stake_amount = stake_amount
        print(f'\nYou would like to stake into the following {len(self.netuids_to_stake)} subnets:')
        for i in range(len(self.netuids_to_stake)):
            print(self.netuids_to_stake[i])
        print(f'Requiring τ{self.stake_amount*len(self.netuids_to_stake)}')

    def check_balances_for_stake(self, total_stake_amount):
        if total_stake_amount < self.free_tao:
            pass

        # If total stake amount < free tao and root stake, unstake remander from root
        elif total_stake_amount < self.free_tao + self.root_stake:
            root_unstake_needed = total_stake_amount - self.free_tao
            print('Not enough free tao')
            continue_check(f'Would you like to unstake {root_unstake_needed} from root?')

            root_unstake_made = 0
            i = 0
            while root_unstake_made < root_unstake_needed:
                if self.delegated_info[i].netuid == 0:
                    this_stake_amount = float(self.delegated_info[i].stake)
                    if root_unstake_made + this_stake_amount > root_unstake_needed:
                        unstake_amount = root_unstake_needed - root_unstake_made
                        self.subtensor.unstake(
                            wallet=self.wallet,
                            netuid=0,
                            hotkey_ss58=self.delegated_info[i].hotkey_ss58,
                            amount=bittensor.Balance(unstake_amount)
                        )
                    else:
                        self.subtensor.unstake(
                            wallet=self.wallet,
                            netuid=0,
                            hotkey_ss58=self.delegated_info[i].hotkey_ss58,
                            amount=self.delegated_info[i].stake
                        )
                i += 1

        else:
            print(f'Free tao and root stake insufficient to make stake')
            exit()
                
    def organise_hotkeys_to_stake(self):
        self.netuid_hotkey_pairs = []
        self.no_stake_flag = False

        for netuid in self.netuids_to_stake:
            found_flag = False
            for info in self.delegated_info:
                if netuid == info.netuid:
                    print(f'Subnet {netuid} staked to: {info.hotkey_ss58}')
                    self.netuid_hotkey_pairs.append((netuid, info.hotkey_ss58)) # Create list of tuples
                    found_flag = True
                    break
            if not found_flag:
                print(f'No stake for subnet: {netuid}')
                self.no_stake_flag = True

        if self.no_stake_flag:
            print('Need to make an initial stake on each subnet before using this program')
            exit()

    def make_stakes(self):
        for pair in self.netuid_hotkey_pairs:
            netuid, hotkey = pair
            stake_success = self.subtensor.add_stake(
                wallet=self.wallet,
                netuid=netuid,
                hotkey_ss58=hotkey,
                amount=bittensor.Balance(self.stake_amount)
            )
            if stake_success:
                print(f'Stake on subnet {netuid} to {hotkey} successful')
            else:
                print(f'Failed to make a stake on subnet {netuid} to {hotkey}')


def continue_check(message):
    continue_check = str(input(f'{message} (y/n): '))
    if not (continue_check == 'y' or continue_check == 'Y'):
        exit()