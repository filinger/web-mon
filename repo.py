import pickle
import sqlite3
from datetime import datetime


def adapt_pickle(items):
    return pickle.dumps(items)


class Repo(object):
    DB_NAME = 'web-mon.db'

    sqlite3.register_adapter(list, adapt_pickle)
    sqlite3.register_converter('list', pickle.loads)

    def __init__(self):
        self.con = sqlite3.connect(Repo.DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)


class WebsiteRepo(Repo):
    def __init__(self):
        super().__init__()
        with self.con as c:
            c.execute('CREATE TABLE IF NOT EXISTS websites (url text unique)')

    def get_all(self):
        with self.con as c:
            return c.execute('SELECT rowid, * FROM websites').fetchall()

    def put(self, url):
        with self.con as c:
            c.execute('INSERT OR IGNORE INTO websites VALUES (?)', (url,))

    def remove(self, url):
        with self.con as c:
            c.execute('DELETE FROM websites WHERE url = ?', (url,))


class ThemeRepo(Repo):
    def __init__(self):
        super().__init__()
        with self.con as c:
            c.execute('CREATE TABLE IF NOT EXISTS themes (name text unique, keywords list)')

    def get_all(self):
        with self.con as c:
            return c.execute('SELECT rowid, * FROM themes').fetchall()

    def put(self, name, keywords):
        with self.con as c:
            c.execute('INSERT OR REPLACE INTO themes VALUES (?, ?)', (name, keywords))

    def remove(self, name):
        with self.con as c:
            c.execute('DELETE FROM themes WHERE name = ?', (name,))


class MonitoringRepo(Repo):
    def __init__(self):
        super().__init__()
        with self.con as c:
            c.execute('CREATE TABLE IF NOT EXISTS monitoring (ts timestamp, url text, theme text)')

    def get_all(self):
        with self.con as c:
            return c.execute('SELECT * FROM monitoring').fetchall()

    def put(self, url, theme):
        timestamp = datetime.now()
        with self.con as c:
            c.execute('INSERT INTO monitoring VALUES (?, ?, ?)', (timestamp, url, theme))
