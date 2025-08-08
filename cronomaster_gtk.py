#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cronomaster

class Graphics(Gtk.Window):
    def __init__(self, name: str, width: int, height: int):
        '''
            Delegate logic to objects for create
            windows easierly
        '''
        super().__init__(title = name)
        self.set_size_request(width, height)
        self.containers: list = []
        self.widgets: list = []

    def load_widgets(self, widgets_limit: list[int]):
        '''
            Add container and widgets from the list
            until one number of widgets per container.

            Parameter: 
                widgets limit per container from 1 to number of widgets
        '''
        for container in range(0, widgets_limit.__len__()):
            # Add container to the window
            self.add(Gtk.VBox(spacing = 4))
        limit = 0    
        widgets_count = 0
        for widget in self.widgets:
            # Add until widgets limit on each container
            self.containers[limit].add(widget)
            # Always increase the widgets counting
            widgets_count += 1
            # Increase the var used to select container
            if  (
                    widgets_count <= widgets_limit[limit]
                    and (limit - 1) < self.containers.__len__()
                ):
                # Go to next container until be the last container
                limit += 1

def set_communication(first_input, second_input):
    '''
        Take two values from Gtk inputs
        and make a cronomaster communication
    '''
    # Getting the values from protocol form
    address = first_input.get_text().__str__()
    port = int(second_input.get_text())
    # Set communication
    try:
        cronomaster.communication(address, port)
        panel.widgets[6].set_text('Yes')
    except:
        panel.widgets[6].set_text('No')    

def get_seconds(clock: Gtk.Label):
    '''
        Show as time in a Gtk.label
        the seconds to make a clock
    '''
    timer = clock.get_text().__str__().split(' : ')
    # Clock logic
    cronomaster.origin.count()
    sec = cronomaster.origin.seconds
    cronomaster.save_wallet(cronomaster.origin, 'first.dat')
    # Get Hours, Minutes and Seconds from the storaged seconds in wallet
    timer[0] = sec // 3600
    timer[1] = sec // 60 - timer[0] * 60
    timer[2] = sec - timer[1] * 60 - timer[0] * 3600

    clock.set_text(f'{timer[0]} : {timer[1]} : {timer[2]}')

if __name__ == '__main__':
    panel = Graphics('Cronomaster: Time Wallet', 200, 100)
    panel.widgets = [
                        # 0 Timer with the representation of total seconds in origin wallet
                            Gtk.Label(label = '00 : 00 : 00'),
                        # 1 Input for the seconds number to send
                            Gtk.Entry(),
                        # 2 Sending button
                            Gtk.Button(label = 'Send'),
                        # 3 Description text for protocol form
                            Gtk.Label(label = 'Connection To other Time Wallet'),
                        # 4 Input for IP address ('ip addr' in bash)
                            Gtk.Entry(),
                        # 5 Input for TCP listening free port ('netstat -nt' in bash when isn't TIME_WAIT)
                            Gtk.SpinButton(),
                        # 6 Connection state text set 'Yes' only when has been connect
                            Gtk.Label(label = 'No')
                    ]
    # Setting of widgets
    panel.widgets[4].set_placeholder_text('IP address x.x.x.x')
    panel.widgets[4].connect(
                                'changed',
                                # Change the Seconds to send and connection data 
                                panel.widgets[1].connect(
                                                            'changed',
                                                            panel.widgets[5].connect(
                                                                'changed',
                                                                set_communication(
                                                                    panel.widgets[4],
                                                                    panel.widgets[5]
                                                                )
                                                            )
                                                        )
                            )
    panel.widgets[1].set_placeholder_text('Seconds to send')
    try:
        panel.load_widgets  ( 
                                [
                                    2, 2, 
                                    3, 2
                                ]    
                            )
        panel.show_all()
        Gtk.main()
    except:
        panel.close()