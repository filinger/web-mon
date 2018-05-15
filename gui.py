from tkinter import *
from tkinter import ttk


class MonitoringFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        monitoring = ttk.Frame(parent)
        monitoring.grid_rowconfigure(0, weight=1)
        monitoring.grid_columnconfigure(0, weight=1)
        parent.add(monitoring, text='Monitoring')

        tree = ttk.Treeview(monitoring, columns=('timestamp', 'url', 'theme'), show='headings')
        tree.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

        tree.column('timestamp', anchor='center')
        tree.heading('timestamp', text='Timestamp')
        tree.column('url', anchor='center')
        tree.heading('url', text='Url')
        tree.column('theme', anchor='center')
        tree.heading('theme', text='Theme')
        self.tree = tree

    def add_record(self, rowid, timestamp, url, theme):
        str_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.tree.insert('', 'end', rowid, values=[str_time, url, theme])


class WebsitesFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        websites = ttk.Frame(parent)
        websites.grid_rowconfigure(0, weight=1)
        websites.grid_columnconfigure(0, weight=1)
        parent.add(websites, text='Websites')

        tree = ttk.Treeview(websites, columns=('url', 'depth'), show='headings')
        tree.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

        tree.column('url', anchor='center')
        tree.heading('url', text='Url')
        tree.column('depth',anchor='center')
        tree.heading('depth', text='Depth')
        self.tree = tree

    def add_website(self, rowid, url, depth):
        self.tree.insert('', 'end', rowid, values=[url, depth])


class ThemesFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        themes = ttk.Frame(parent)
        themes.grid_rowconfigure(0, weight=1)
        themes.grid_columnconfigure(0, weight=1)
        parent.add(themes, text='Themes')

        tree = ttk.Treeview(themes, columns=('name', 'keywords'), show='headings')
        tree.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

        tree.column('name', anchor='center')
        tree.heading('name', text='Name')
        tree.column('keywords', anchor='center')
        tree.heading('keywords', text='Keywords')
        self.tree = tree

    def add_theme(self, rowid, name, keywords):
        self.tree.insert('', 'end', rowid, values=[name, keywords])


class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title('Website Monitoring')
        parent.geometry('800x800')
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

        notebook = ttk.Notebook(parent)
        notebook.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

        self.parent = parent
        self.themes = ThemesFrame(notebook)
        self.websites = WebsitesFrame(notebook)
        self.monitoring = MonitoringFrame(notebook)

    @staticmethod
    def new_window():
        root = Tk()
        return App(root)

    def draw(self):
        self.parent.mainloop()
