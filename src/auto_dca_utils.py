import bittensor

class FullWalletInfo:
    def __init__(self, wallet, subtensor):
        self.wallet = wallet
        self.subtensor = subtensor
        self.free_tao = self.subtensor.get_balance(address=self.wallet.coldkeypub.ss58_address) # Gets free tao balance
        
        self.delegated_info = self.subtensor.get_delegated(coldkey_ss58=self.wallet.coldkeypub.ss58_address)
        self.delegated_info.sort(key=lambda info: info.netuid)  # Sort by subnet ID

        self.root_stake = 0
        self.alpha_stake = 0
        for info in self.delegated_info:
            if info.netuid == 0:
                self.root_stake += info.stake # Sums root stake

            else:
                subnet_info = self.subtensor.subnet(netuid=info.netuid)
                self.alpha_stake += bittensor.Balance(float(info.stake) * float(subnet_info.price)) # Converts alpha stake to tao and sums

    def print_balances(self):
        print(f'\nFor coldkey: {self.wallet.coldkeypub.ss58_address}')
        print(f'Free tao: {self.free_tao} | Root stake: {self.root_stake} | Alpha stake: {self.alpha_stake}')
        print(f'Total: {self.free_tao + self.root_stake + self.alpha_stake}')

    def check_netuids_to_stake(self, netuids_to_stake, stake_amount):
        self.netuids_to_stake = netuids_to_stake
        self.stake_amount = stake_amount
        print(f'\nYou would like to stake into the following {len(self.netuids_to_stake)} subnets:')
        for i in range(len(self.netuids_to_stake)):
            print(self.netuids_to_stake[i])
        print(f'Requiring {bittensor.Balance(self.stake_amount*len(self.netuids_to_stake))} free')

    def check_balances_for_stake(self, total_stake_amount):
        if total_stake_amount < float(self.free_tao):
            pass
        elif total_stake_amount < float(self.free_tao) + float(self.root_stake):
            root_unstake_needed = total_stake_amount - float(self.free_tao)
            print('Not enough free tao')
            continue_check = str(input(f'Would you like to unstake {root_unstake_needed} from root? (y/n): '))
            if (continue_check == 'y' or continue_check == 'Y'):
                self.subtensor.unstake(wallet=self.wallet, netuid=0, amount=root_unstake_needed)
            else:
                exit()
        else:
            print(f'Free tao and root stake insufficient to make stake')
            exit()
                
    def organise_hotkeys_to_stake(self):
        self.hotkeys_to_stake = []
        self.amounts_to_stake = []
        self.no_stake_flag = False

        for netuid in self.netuids_to_stake:
            for i in range(len(self.delegated_info)):
                if netuid == self.delegated_info[i].netuid:
                    print(f'Subnet {netuid} staked to: {self.delegated_info[i].hotkey_ss58}')
                    self.hotkeys_to_stake.append(self.delegated_info[i].hotkey_ss58)
                    self.amounts_to_stake.append(self.stake_amount)
                    break
                elif i == len(self.delegated_info) - 1:
                    print(f'No stake for subnet: {netuid}')
                    self.no_stake_flag = True      
                
        if self.no_stake_flag == True:
            print('Need to make an initial stake on each subnet before using this program')
            exit()

    def make_stakes(self):
        for netuid in self.netuids_to_stake:
            for i in range(len(self.delegated_info)):
                if netuid == self.delegated_info[i].netuid:
                    stake_success = self.subtensor.add_stake(wallet=self.wallet, netuid=netuid, hotkey_ss58=self.hotkeys_to_stake[i], amount=bittensor.Balance(self.stake_amount))
                    if stake_success == True:
                        print(f'Stake on subnet {netuid} successful')
                    else:
                        print(f'(1) Failed to make a stake for subnet: {netuid} ')
                    break
                elif i == len(self.delegated_info) - 1:
                    print(f'(2) Failed to make a stake for subnet: {netuid} ')

def continue_check(message):
    continue_check = str(input(f'{message} (y/n): '))
    if not (continue_check == 'y' or continue_check == 'Y'):
        exit()