import os
from chrono import TimeWallet
# Get storaged seconds from external source later
def read_wallet(name: str) -> int:
    with open(name, 'rb') as wallet:
        result = wallet.read().hex()
    return int(result, 16)
origin = TimeWallet(read_wallet('first.dat'))
destination = TimeWallet(read_wallet('second.dat'))
# Show initial state
def save_wallet(first: TimeWallet, name: str):
    with open(name, 'wb') as one:
        one.write(first.seconds.to_bytes())        

def show_wallets(start: TimeWallet, end: TimeWallet):
    sep = ''
    for repeat in range(0, 29):
        sep += '-'
    print(f'\t{sep}\n\t{start.ID} wallet has {start.seconds}s\n\t{end.ID} wallet has {end.seconds}s')
# First state
print('\t[CRONOMASTER]\n\nSend seconds between conected wallets')
show_wallets(origin, destination)    
# Make the right changes
option = 'y'
while option.lower() == 'y':
    # Send seconds and count more seconds only when has underrate
    origin.send(7, destination)
    # Next state after send 7s to destination
    show_wallets(origin, destination)
    save_wallet(origin, 'first.dat')
    save_wallet(destination, 'second.dat')
    option = input('\nContinue Y/n: ')
# Clean cacche
os.system('rm -R __pycache__')    