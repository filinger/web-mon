from gui import App
from repo import WebsiteRepo, ThemeRepo, MonitoringRepo

website_repo = WebsiteRepo()
theme_repo = ThemeRepo()
monitoring_repo = MonitoringRepo()

website_repo.put('https://en.wikipedia.org/wiki/Animal', 1)
theme_repo.put('Cats', ['cat', 'tiger', 'puma'])
theme_repo.put('Dogs', ['dog', 'wolf'])

app = App.new_window()

themes = theme_repo.get_all()
for rowid, name, keywords in themes:
    app.themes.add_theme(rowid, name, keywords)

websites = website_repo.get_all()
for rowid, url, depth in websites:
    app.websites.add_website(rowid, url, depth)

records = monitoring_repo.get_all()
for rowid, timestamp, url, theme in records:
    app.monitoring.add_record(rowid, timestamp, url, theme)


def main():
    app.draw()


if __name__ == '__main__':
    main()
