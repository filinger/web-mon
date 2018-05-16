from datetime import datetime, date, timedelta
from tkinter import *
from tkinter import ttk


def add_pane(parent, name):
    pane = ttk.Frame(parent)
    pane.grid_rowconfigure(0, weight=0)
    pane.grid_rowconfigure(1, weight=1)
    pane.grid_columnconfigure(0, weight=1)
    parent.add(pane, text=name)
    return pane


class MonitoringFrame(Frame):
    def __init__(self, parent, repo):
        Frame.__init__(self, parent)
        self.repo = repo
        self.from_date = StringVar(value=(date.today() - timedelta(1)).strftime('%Y-%m-%d'))
        self.to_date = StringVar(value=date.today().strftime('%Y-%m-%d'))

        monitoring = add_pane(parent, 'Monitoring')
        self.add_inputs(monitoring)
        self.tree = self.add_tree(monitoring)
        self.repopulate_from_repo()

    def add_inputs(self, parent):
        inputs = ttk.Frame(parent, heigh=10, padding="3 3 12 12")
        ttk.Label(inputs, text="From:").grid(row=0, column=0)
        ttk.Entry(inputs, textvariable=self.from_date).grid(row=0, column=1)
        ttk.Label(inputs, text="To:").grid(row=0, column=2)
        ttk.Entry(inputs, textvariable=self.to_date).grid(row=0, column=3)
        ttk.Button(inputs, text='Refresh', command=self.repopulate_from_repo_ranged).grid(row=0, column=4)
        inputs.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

    def add_tree(self, parent):
        tree = ttk.Treeview(parent, columns=('timestamp', 'url', 'theme'), show='headings', selectmode='browse')
        tree.grid(row=1, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))
        tree.column('timestamp', anchor='center')
        tree.heading('timestamp', text='Timestamp')
        tree.column('url', anchor='center')
        tree.heading('url', text='Url')
        tree.column('theme', anchor='center')
        tree.heading('theme', text='Theme')
        return tree

    def add_row(self, rowid, timestamp, url, theme):
        str_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.tree.insert('', 'end', rowid, values=[str_time, url, theme])

    def repopulate_from_repo(self):
        self.tree.delete(*self.tree.get_children())
        records = self.repo.get_all()
        for rowid, timestamp, url, theme in records:
            self.add_row(rowid, timestamp, url, theme)

    def repopulate_from_repo_ranged(self):
        try:
            from_date = datetime.strptime(self.from_date.get(), '%Y-%m-%d').date()
            to_date = datetime.strptime(self.to_date.get(), '%Y-%m-%d').date()
            self.tree.delete(*self.tree.get_children())
            records = self.repo.get_range(from_date, to_date)
            for rowid, timestamp, url, theme in records:
                self.add_row(rowid, timestamp, url, theme)
        except ValueError:
            # Ignore malformed input
            pass


class WebsitesFrame(Frame):
    def __init__(self, parent, repo):
        Frame.__init__(self, parent)
        self.repo = repo
        self.new_url = StringVar(value='http://example.com')
        self.new_depth = IntVar(value=1)

        websites = add_pane(parent, 'Websites')
        self.add_inputs(websites)
        self.tree = self.add_tree(websites)
        self.repopulate_from_repo()

    def add_inputs(self, parent):
        inputs = ttk.Frame(parent, heigh=10, padding="3 3 12 12")
        ttk.Label(inputs, text="Url:").grid(row=0, column=0)
        ttk.Entry(inputs, textvariable=self.new_url).grid(row=0, column=1)
        ttk.Label(inputs, text="Depth:").grid(row=0, column=2)
        ttk.Entry(inputs, textvariable=self.new_depth).grid(row=0, column=3)
        ttk.Button(inputs, text='Add', command=self.add_website).grid(row=0, column=4)
        ttk.Button(inputs, text='Remove', command=self.remove_website).grid(row=0, column=5)
        inputs.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

    def add_tree(self, parent):
        tree = ttk.Treeview(parent, columns=('url', 'depth'), show='headings', selectmode='browse')
        tree.grid(row=1, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))
        tree.column('url', anchor='center')
        tree.heading('url', text='Url')
        tree.column('depth', anchor='center')
        tree.heading('depth', text='Depth')
        return tree

    def add_row(self, rowid, url, depth):
        self.tree.insert('', 'end', rowid, values=[url, depth])

    def add_website(self):
        try:
            url = self.new_url.get()
            depth = max(1, min(self.new_depth.get(), 10))  # Clamp depth value to 0..10
            if url:
                self.repo.put(url, depth)
                self.repopulate_from_repo()
        except TclError:
            # Ignore malformed input
            pass

    def remove_website(self):
        selected = self.tree.selection()
        if len(selected) > 0:
            self.repo.remove(selected[0])
            self.tree.delete(selected[0])

    def repopulate_from_repo(self):
        self.tree.delete(*self.tree.get_children())
        websites = self.repo.get_all()
        for rowid, url, depth in websites:
            self.add_row(rowid, url, depth)


class ThemesFrame(Frame):
    def __init__(self, parent, repo):
        Frame.__init__(self, parent)
        self.repo = repo
        self.new_name = StringVar(value='Example')
        self.new_keywords = StringVar(value='space separated keywords')

        themes = add_pane(parent, 'Themes')
        self.add_inputs(themes)
        self.tree = self.add_tree(themes)
        self.repopulate_from_repo()

    def add_inputs(self, parent):
        inputs = ttk.Frame(parent, heigh=10, padding="3 3 12 12")
        ttk.Label(inputs, text="Name:").grid(row=0, column=0)
        ttk.Entry(inputs, textvariable=self.new_name).grid(row=0, column=1)
        ttk.Label(inputs, text="Keywords:").grid(row=0, column=2)
        ttk.Entry(inputs, textvariable=self.new_keywords).grid(row=0, column=3)
        ttk.Button(inputs, text='Add', command=self.add_theme).grid(row=0, column=4)
        ttk.Button(inputs, text='Remove', command=self.remove_theme).grid(row=0, column=5)
        inputs.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

    def add_tree(self, themes):
        tree = ttk.Treeview(themes, columns=('name', 'keywords'), show='headings', selectmode='browse')
        tree.grid(row=1, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))
        tree.column('name', anchor='center')
        tree.heading('name', text='Name')
        tree.column('keywords', anchor='center')
        tree.heading('keywords', text='Keywords')
        return tree

    def add_row(self, rowid, name, keywords):
        self.tree.insert('', 'end', rowid, values=[name, keywords])

    def add_theme(self):
        name = self.new_name.get()
        keywords = self.new_keywords.get().split()
        if name and len(keywords) > 0:
            self.repo.put(name, keywords)
            self.repopulate_from_repo()

    def remove_theme(self):
        selected = self.tree.selection()
        if len(selected) > 0:
            self.repo.remove(selected[0])
            self.tree.delete(selected[0])

    def repopulate_from_repo(self):
        self.tree.delete(*self.tree.get_children())
        themes = self.repo.get_all()
        for rowid, name, keywords in themes:
            self.add_row(rowid, name, keywords)


class App(Frame):
    def __init__(self, parent, theme_repo, website_repo, monitoring_repo):
        Frame.__init__(self, parent)

        parent.title('Website Monitoring')
        parent.geometry('800x400')
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

        notebook = ttk.Notebook(parent)
        notebook.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=(N, S, W, E))

        self.parent = parent
        self.themes = ThemesFrame(notebook, theme_repo)
        self.websites = WebsitesFrame(notebook, website_repo)
        self.monitoring = MonitoringFrame(notebook, monitoring_repo)

    @staticmethod
    def new(theme_repo, website_repo, monitoring_repo):
        root = Tk()
        return App(root, theme_repo, website_repo, monitoring_repo)

    def draw(self):
        self.parent.mainloop()
