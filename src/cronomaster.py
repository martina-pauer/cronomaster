#!/usr/bin/python3
import os
import socket
# Add from lib/chrono.py the needed module
import sys
# Cronomaster dir when is installed for more standarization and less errors
prefix = '/usr/cronomaster/'
sys.path.append (
                    os.path.abspath
                    (
                        os.path.join 
                        (
                            os.path.dirname(__file__),
                            f'{prefix}lib/'
                        )
                    )
                )
from chrono import TimeWallet, seconds_limit

# Get storaged seconds from external source later
def read_wallet(name: str) -> int:
    '''
        Get seconds from a bytes file (binary file)
    '''
    with open(name, 'rb') as wallet:
        result = wallet.read().hex()
    return int(result, 16)

origin = TimeWallet(read_wallet(f'{prefix}lib/data/first.dat'))
destination = TimeWallet(read_wallet(f'{prefix}lib/data/second.dat'))

def communication(loopback_ip: str, port: int):   
    '''
        Receive from the other active script 
        the new data for origin object.

        Parameters:
            loopback_ip, ip INET address for the other device (use 'ip addr' or 'ifconfig' in bash)
            port, a free listen port (use 'netstat -ln' in bash)
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as load:
        print('Connecting...')
        load.connect((loopback_ip, port))
        load.listen()
        # Send for other script first seconds and later ID    
        load.sendto (  
                        bytes((destination.seconds).__str__().encode('utf-8')),
                        (
                            loopback_ip,
                             port
                        )    
                    )
        print(f'\tSend {destination.seconds} seconds to {destination.ID}')
        # Send data like bytes to IP address in the listening port
        load.sendto (
                        bytes(destination.ID.encode('utf-8')),
                        (
                            loopback_ip,
                            port
                        )
                    )        
        with load.accept() as connection:
            print('Receiving seconds...')
            # Receive seconds and ID from the other script in sort
            data: int = int(connection.recv(28).decode('utf-8'))
            if (origin.seconds + data) <= seconds_limit:
                origin.senconds += data
            else:
                print(f'\n{seconds_limit} secs limit reached')
            # After read bytes for seconds read bytes for hash ID
            data: str = connection.recv(8).decode('utf-8')
            origin.ID = data
        # End communication for don't stuck the program with an unnecessary connection    
        connection.close()    
    print('End of the communication.')
# Show initial state
def save_wallet(first: TimeWallet, name: str):
    '''
        Save seconds from objects to
        a bytes file (binary file)
    '''
    with open(name, 'wb') as one:
        if first.seconds <= seconds_limit:
            one.write(first.seconds.to_bytes(28, 'little'))            

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
if __name__ == '__main__':
    # Only run it when run directly the script, not when import from a graphical tool
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
        if (origin.seconds // destination.seconds) <= (seconds_limit // 2):
            # Only save when the seconds are between the limit
            save_wallet(origin, f'{prefix}lib/data/first.dat')
            save_wallet(destination, f'{prefix}lib/data/second.dat')
        else:
            print(f'Extra seconds sended then don\'t are storaged.\n Overpased {seconds_limit} seconds limit.\n')    
        option = input('\nContinue Y/n: ')
# Clean cache
try:
    os.system(f'rm -R {prefix}lib/__pycache__')
except:
    pass