import platform
import socket
import webbrowser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        # Load the UI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("simple_gui_app.glade")

        # Get the widgets from the Glade file
        self.window = self.builder.get_object("windows1")
        self.button1 = self.builder.get_object("button1")
        self.button2 = self.builder.get_object("button2")
        self.button3 = self.builder.get_object("button3")
        self.search_entry = self.builder.get_object("search1")
        self.checkbox = self.builder.get_object("checkbox1")
        self.switch = self.builder.get_object("switch1")
        self.textbox1 = self.builder.get_object("textbox1")
        self.textbox2 = self.builder.get_object("textbox2")
        self.progressbar = self.builder.get_object("progressbar1")

        # Connect signals
        self.builder.connect_signals({
            "on_button1_clicked": self.on_button1_clicked,
            "on_button2_clicked": self.on_button2_clicked,
            "on_button3_clicked": self.on_button3_clicked,
            "on_checkbox1_toggled": self.on_checkbox1_toggled,
            "on_search1_activate": self.on_search1_activate,  
            "on_switch1_state_set": self.on_switch1_state_set
        })

        # Show the top-level window
        self.window.show_all()

    def on_button1_clicked(self, button):
        self.progressbar.set_fraction(0.0)
        self.progressbar.set_text("Loading...")

        # Simulate a long task
        GLib.timeout_add(100, self.update_progress, 0.05)

    def update_progress(self, fraction):
        new_fraction = self.progressbar.get_fraction() + fraction
        if new_fraction < 1.0:
            self.progressbar.set_fraction(new_fraction)
            return True
        else:
            self.progressbar.set_fraction(1.0)
            self.progressbar.set_text("Complete!")
            self.show_popup_dialog()
            return False

    def show_popup_dialog(self):
        dialog = Gtk.MessageDialog(parent=self,
        flags=0,
        type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        message_format="Task Complete!")
        dialog.run()
        dialog.destroy()
        self.progressbar.set_fraction(0.0)
        self.progressbar.set_text("0%")

    def on_button2_clicked(self, button):
        print("Button 2 Clicked")

    def on_button3_clicked(self, button):
        # Get information about the operating system
        os_info = platform.platform()
        self.textbox1.set_text(os_info)

        # Get the IP address of the system
        ip_address = self.get_ip_address()
        self.textbox2.set_text(ip_address)

    def get_ip_address(self):
        # Create a socket to get the IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                # Connect to a public server to get the IP address
                s.connect(('8.8.8.8', 80))
                ip_address = s.getsockname()[0]
            except Exception as e:
                print("Error:", e)
                ip_address = "Unknown"
        return ip_address

    def on_checkbox1_toggled(self, checkbox):
        if checkbox.get_active():
            print("Check button checked")
        else:
            print("Check button unchecked")

    def on_search1_activate(self, search_entry):  
        text = search_entry.get_text()
        if text:
            search_url = "https://www.google.com/search?q=" + text
            webbrowser.get('firefox').open(search_url)
    
    def on_switch1_state_set(self, switch, gparam):
        if switch.get_active():
            print("Switch activated")
        else:
            print("Switch deactivated")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
