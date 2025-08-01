from chrono import TimeWallet
# Get storaged seconds from external source later
origin = TimeWallet(10)
destination = TimeWallet(5)
# Show initial state
def show_wallets(start: TimeWallet, end: TimeWallet):
    print(f'\n\t{start.ID} wallet has {start.seconds}s\n\t{end.ID} wallet has {end.seconds}s')
# Make the right changes
option = 'y'
while option.lower() == 'y':
    origin.send(7, destination)
    show_wallets(origin, destination)
    option = input('\nContinue Y/n: ')