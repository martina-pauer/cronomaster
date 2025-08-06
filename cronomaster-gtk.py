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
        self.containers: list = [
                                    Gtk.VBox(spacing = 4), 
                                    Gtk.VBox(spacing = 4),
                                ]
        self.widgets: list = []
        self.load_widgets()

    def load_widgets(self, widgets_limit: int):
        '''
            Add container and widgets from the list
            until one number of widgets per container.

            Parameter: 
                widgets limit per container from 1 to number of widgets
        '''
        for container in self.containers:
            # Add container to the window
            self.add(container)
        limit = 1    
        widgets_count = 0
        for widget in self.widgets:
            # Add until widgets limit on each container
            self.containers[limit - 1].add(widget)
            # Always increase the widgets counting
            widgets_count += 1
            # Increase the var used to select container
            if  (
                    widgets_count <= widgets_limit
                    and limit < self.containers.__len__()
                ):
                # Go to next container until be the last container
                limit += 1

if __name__ == '__main__':
    panel = Graphics('Cronomaster: Time Wallet', 200, 100)
    panel.widgets = [
                        Gtk.Entry(placeholder = 'Seconds to send')
                    ]
    try:
        panel.show_all()
        Gtk.main()
    except:
        panel.close()