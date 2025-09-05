#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
# Add from upper folder the cronomaster module
import os
import sys
sys.path.append (
                    os.path.abspath
                    (
                        os.path.join
                        (
                            os.path.dirname(__file__),
                            # Set path to cronomaster.py file
                            '/usr/cronomaster/src'
                        )    
                    )
                )
import cronomaster
# Define style for GTK using the SDK
style = Gtk.CssProvider()

css_data = b'''style file content'''

with open(f'{cronomaster.prefix}src/graphics/gtk-theme.css','rb') as data:
    css_data = data.read()
# Load bytes from the file to the style
style.load_from_data(css_data)
# Create context for the style
style_context = Gtk.StyleContext()
# Define screen to apply style
screen = Gdk.Screen().get_default()
# Add style to the screen
style_context.add_provider_for_screen   (
                                            screen,
                                            style,
                                            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                                        )
# Define GTK window
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

def communicate(widget):
    '''
        Use set_communication function for
        send seconds to other time wallet.

        Callback function for Gtk event
        using connect method from widget.
    '''
    set_communication(panel.widgets[4], panel.widgets[5])
    # Update clock   
    get_seconds(panel.widgets[0])

def get_seconds(clock: Gtk.Label):
    '''
        Show as time in a Gtk.label
        the seconds to make a clock
    '''
    # Clock logic
    cronomaster.origin.count()
    sec = cronomaster.origin.seconds
    cronomaster.save_wallet(cronomaster.origin, f'{cronomaster.prefix}lib/data/first.dat')
    # Get Hours, Minutes and Seconds from the storaged seconds in wallet
    timer = clock.get_text().__str__().split(' : ')
    # Algorithm to convert seconds in hours with his remainders in minutes and seconds
    remainder = sec
    # Get hours
    while (remainder >= 3600):
        # Count each hour and decrease the remainder
        timer[0] = int(timer[0]) + 1
        remainder -= 3600
    # Get minutes with the remainder
    while (remainder >= 60):
        # Count minutes decreasing his remainder only to stop of count
        timer[1] = int(timer[1]) + 1
        remainder -= 60
    # The seconds are the remainder that start from the seconds now haven't hours and minutes
    timer[2] = remainder        
    # End of algorithm Turn Seconds into Hours with his Remainder in Minutes and Seconds (TSHRMS)
    # Fix time format for numbers less than 10 add one zero to left
    for position in range(0, 3):
        # Check hours, minutes and seconds and fix
        if timer[position] < 10:
            timer[position] = f'0{timer[position]}'
    # Load time to the clock label
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
    spinAdjust = Gtk.Adjustment (
                                # Set TCP port input range from 1024 to 10024
                                    value = 1.080e3,
                                    upper = 10.000e3,
                                    lower = 1.080e3,
                                # The numbers be each ten ports    
                                    step_increment = 1e3,
                                    page_increment = 1e3,
                                    page_size = 0.0
                                )
    panel.widgets[5].set_adjustment(spinAdjust)
    panel.widgets[4].set_placeholder_text('IP address x.x.x.x')
    panel.widgets[1].set_placeholder_text('Seconds to send')
    # Use callback for set_commuinication that take as parameter a Gtk.Button
    panel.widgets[2].connect('clicked', communicate)
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
    os.system(f'rm -R {cronomaster.prefix}src/__pycache__')
except:
    # When the cache has cleaned
    pass            