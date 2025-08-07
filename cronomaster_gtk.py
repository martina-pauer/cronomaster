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
        limit = 1    
        widgets_count = 0
        for widget in self.widgets:
            # Add until widgets limit on each container
            self.containers[limit - 1].add(widget)
            # Always increase the widgets counting
            widgets_count += 1
            # Increase the var used to select container
            if  (
                    widgets_count <= widgets_limit[limit - 1]
                    and limit < self.containers.__len__()
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

if __name__ == '__main__':
    panel = Graphics('Cronomaster: Time Wallet', 200, 100)
    panel.widgets = [
                        # 0 Timer with the representation of total seconds in origin wallet
                            Gtk.Label(label = 'HH : MM : SS'),
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