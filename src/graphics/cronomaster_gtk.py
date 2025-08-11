#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# Add from upper folder the cronomaster module
import os
import sys
sys.path.append (
                    os.path.abspath
                    (
                        os.path.join
                        (
                            os.path.dirname(__file__),
                            '..'
                        )    
                    )
                )
import cronomaster

class Graphics(Gtk.Window):
    def __init__(self, name: str, width: int, height: int):
        '''
            Delegate logic to objects for create
            windows easierly
        '''
        super().__init__(title = name)
        self.set_size_request(width, height)
        self.widgets: list = []

    def load_widgets(self):
        '''
            Add container and widgets from the list.
        '''
        all_containers = Gtk.HBox()
        
        first_half = Gtk.VBox()
        second_half = Gtk.VBox()

        for left_widget in self.widgets[0 : self.widgets.__len__() // 2]:
            # Add widgets to the container
            first_half.add(left_widget)

        for right_widget in self.widgets[self.widgets.__len__() // 2 :: ]:
            second_half.add(right_widget)

        for container in [first_half, second_half]:
            all_containers.add(container)
            
        self.add(all_containers)       

def set_communication(first_input: Gtk.Entry, second_input: Gtk.SpinButton):
    '''
        Take two values from Gtk inputs
        and make a cronomaster communication
    '''
    # Getting the values from protocol form
    address = first_input.get_text().__str__()
    port = second_input.get_value_as_int()
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
    # Clock logic
    cronomaster.origin.count()
    sec = cronomaster.origin.seconds
    cronomaster.save_wallet(cronomaster.origin, 'lib/data/first.dat')
    # Get Hours, Minutes and Seconds from the storaged seconds in wallet
    timer = clock.get_text().__str__().split(' : ')
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
    panel.widgets[1].set_placeholder_text('Seconds to send')
    panel.widgets[2].connect('clicked', lambda click_1, click_2 : set_communication(panel.widgets[4], panel.widgets[5]))
    # Without this event the window don't show on
    panel.connect('delete-event', Gtk.main_quit)
    try:
        panel.load_widgets()
        # Count seconds while continuosly reload the graphical interface
        get_seconds(panel.widgets[0])
        panel.show_all()
        Gtk.main()
    except:
        panel.close()
try:
    os.system('rm -R __pycache__')
except:
    # When the cache has cleaned
    pass            