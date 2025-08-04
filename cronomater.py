import os
import sys
from chrono import TimeWallet
# Get storaged seconds from external source later
def read_wallet(name: str) -> int:
    '''
        Get seconds from a bytes file (binary file)
    '''
    with open(name, 'rb') as wallet:
        result = wallet.read().hex()
    return int(result, 16)
origin = TimeWallet(0)#read_wallet('first.dat'))
destination = TimeWallet(0)#read_wallet('second.dat'))
# Show initial state
def save_wallet(first: TimeWallet, name: str):
    '''
        Save seconds from objects to
        a bytes file (binary file)
    '''
    with open(name, 'wb') as one:
        one.write(first.seconds.to_bytes())        

def show_wallets(start: TimeWallet, end: TimeWallet):
    '''
        Print in screen the objects info
    '''
    sep = ''
    for repeat in range(0, 29):
        sep += '-'
    print(f'\t{sep}\n\t{start.ID} [Your] wallet has {start.seconds}s\n\t[Waiting] wallet has {end.seconds}s')
# First state
print('\n\t[CRONOMASTER]\n\nSend seconds between conected wallets')
show_wallets(origin, destination)    
# Make the right changes
option = 'y'
while option.lower() == 'y':
    # Send seconds and count more seconds only when has underrate
    origin.send(int(input(f'\n\tWrite seconds to send from {origin.ID}: ')), destination)
    # Next state after send seconds to destination
    show_wallets(origin, destination)
    #save_wallet(origin, 'first.dat')
    #save_wallet(destination, 'second.dat')
    option = input('\nContinue Y/n: ')
def communication():   
    '''
        Receive from the other active script the new data for origin object
    '''    
    bridge = input('\nWrite hash id for receptor wallet: ').__str__()
    #bridge.receive()
    # Send later to the script with ID from destination to origin object
    #bridge.send(destination, bridge.source.origin)
# Clean cache
os.system('rm -R __pycache__')    