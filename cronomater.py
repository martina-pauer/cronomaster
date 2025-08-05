import os
import sys
import socket
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

def communication(loopback_ip: str, port: int):   
    '''
        Receive from the other active script 
        the new data for origin object.

        Parameters:
            loopback_ip, ip INET address for the other device (use 'ip addr' or 'ifconfig' in bash)
            port, a free listen port (use 'netstat -ln' in bash)
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as load:
        load.bind((loopback_ip, port))
        load.listen()
        load.accept()
        with load.accept() as connection:
            # Receive seconds and ID from the other script
            data = connection.recv(28)
            origin.senconds += int(data.decode('utf-8'))
            # After read bytes for seconds read bytes for hash ID
            data = connection.recv(62)
            origin.ID += data.decode('uft-8')
            # Send for other script    
            load.sendto (   [
                                destination.seconds, 
                                destination.ID
                            ],
                            loopback_ip
                        )                
# Show initial state
def save_wallet(first: TimeWallet, name: str):
    '''
        Save seconds from objects to
        a bytes file (binary file)
    '''
    with open(name, 'wb') as one:
        one.write(first.seconds.to_bytes())        

def show_wallets(start: TimeWallet, end: TimeWallet) -> str:
    '''
        Print in screen the objects info
    '''
    sep = ''
    for repeat in range(0, 29):
        sep += '-'
    result = f'\t{sep}\n\t{start.ID} [Your] wallet has {start.seconds}s\n\t[Waiting] wallet has {end.seconds}s'
    del sep
    print(result)
    return result
# First state
print('\n\t[CRONOMASTER]\n\nSend seconds between conected wallets')
show_wallets(origin, destination)    
# Make the right changes
option = 'y'
while option.lower() == 'y':
    # Ask for ip and port for get info
    try:
        communication(input('\n\tLoop Back IP from sender: '), int(input('\n\tFree LISTEN port: ')))
    except:
        print('\nConnection Fail: Write a valid cronomaster IP and free port')    
    # Send seconds and count more seconds only when has underrate
    origin.send(int(input(f'\n\tWrite seconds to send from {origin.ID}: ')), destination)
    # Next state after send seconds to destination
    show_wallets(origin, destination)
    #save_wallet(origin, 'first.dat')
    #save_wallet(destination, 'second.dat')
    option = input('\nContinue Y/n: ')
# Clean cache
os.system('rm -R __pycache__')    