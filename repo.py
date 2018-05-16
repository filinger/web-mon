import pickle
import sqlite3


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
            c.execute('CREATE TABLE IF NOT EXISTS websites (url text unique, depth int)')

    def get_all(self):
        with self.con as c:
            return c.execute('SELECT rowid, * FROM websites').fetchall()

    def put(self, url, depth):
        with self.con as c:
            cur = c.cursor()
            cur.execute('INSERT OR REPLACE INTO websites VALUES (?, ?)', (url, depth))
            return cur.lastrowid

    def remove(self, rowid):
        with self.con as c:
            c.execute('DELETE FROM websites WHERE rowid = ?', (rowid,))


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
            cur = c.cursor()
            cur.execute('INSERT OR REPLACE INTO themes VALUES (?, ?)', (name, keywords))
            return cur.lastrowid

    def remove(self, rowid):
        with self.con as c:
            c.execute('DELETE FROM themes WHERE rowid = ?', (rowid,))


class MonitoringRepo(Repo):
    def __init__(self):
        super().__init__()
        with self.con as c:
            c.execute('CREATE TABLE IF NOT EXISTS monitoring (ts timestamp, url text, theme text)')

    def get_all(self):
        with self.con as c:
            return c.execute('SELECT rowid, * FROM monitoring').fetchall()

    def get_range(self, from_date, to_date):
        with self.con as c:
            return c.execute('SELECT rowid, * FROM monitoring WHERE date(ts) >= ? AND date(ts) <= ?',
                             (from_date, to_date)).fetchall()

    def put(self, ts, url, theme):
        with self.con as c:
            cur = c.cursor()
            cur.execute('INSERT INTO monitoring VALUES (?, ?, ?)', (ts, url, theme))
            return cur.lastrowid
