import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango

from lib.io import Importer


class Main(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(self)
        self.main_box = self.builder.get_object("main_box")
        self.window = self.builder.get_object("main_window")
        self.portfolio_view = self.builder.get_object("portfolio_view")
        self.transactions_view = self.builder.get_object("transactions_view")
        self.build_portfolio()
        #self.build_transactions()
        """
        self.progress_bar = builder.get_object("progress_bar")
        self.header = builder.get_object("header")
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        self.header.pack_end(button)
        """
        self.window.show_all()

    def build_portfolio(self):
        store = Gtk.ListStore(str, str, float)
        store.append(["Datadog",
                         "DDOG", 70.05])
        portfolio_view = self.builder.get_object("portfolio_view")
        portfolio_view.set_model(store)

        renderer = Gtk.CellRendererText()
        italic_renderer = Gtk.CellRendererText(
            style=Pango.Style.ITALIC,
            alignment=Pango.Alignment.RIGHT,
        )
        columns = [
            Gtk.TreeViewColumn("Stock", renderer, text=0),
            Gtk.TreeViewColumn("Symbol", renderer, text=1),
            Gtk.TreeViewColumn("Price", italic_renderer, text=2),
        ]
        for col in columns:
            portfolio_view.append_column(col)

    def build_transactions(self):
        store = Gtk.ListStore(str, str, float)
        store.append(["The Art of Computer Programming",
                         "Donald E. Knuth", 25.46])
        transactions_view = self.builder.get_object("transactions_view")
        transactions_view.set_model(store)

        renderer = Gtk.CellRendererText()
        italic_renderer = Gtk.CellRendererText(
            style=Pango.Style.ITALIC,
            alignment=Pango.Alignment.RIGHT,
        )
        columns = [
            Gtk.TreeViewColumn("Title", renderer, text=0),
            Gtk.TreeViewColumn("Author", renderer, text=1),
            Gtk.TreeViewColumn("Price", italic_renderer, text=2),
        ]
        for col in columns:
            transactions_view.append_column(col)
        

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_button_clicked(self, button):
        #self.progress_bar.set_fraction(self.progress_bar.get_fraction() + 0.01)
        print("Hello World!")
    
    def on_import_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
        filter_text = Gtk.FileFilter()
        filter_text.set_name("CSV files")
        filter_text.add_mime_type("text/csv")
        dialog.add_filter(filter_text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            csv_file = dialog.get_filename()
            print("file selected:", csv_file)
            csv_importer = Importer(csv_file)
            out = csv_importer.import_csv()
            self.populate(
                self.transactions_view,
                out,
                [
                    "Date_Time",  # move to settings
                    "Product",
                    "Exchange",
                    "Number",
                    "Price",
                    "Local value",
                    "Value",
                    "Exchange rate",
                    "Fee",
                    "Total",
                ]
                )
        dialog.hide()

    def populate(self, view, data, cols=None):
        """Populates given view with the data"""
        if cols:
            data = data[cols]
        # create a store
        store = Gtk.ListStore(*([str] * len(data.columns)))
        for row in data.values:
            converted = [str(x) for x in row]
            store.append(converted)
        view.set_model(store)
        renderer = Gtk.CellRendererText()
        for index, column in enumerate(data.columns):
            view.append_column(
                Gtk.TreeViewColumn(column, renderer, text=index),
            )

if __name__ == "__main__":
    main = Main()
    Gtk.main()