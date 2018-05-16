from gui import App
from repo import ThemeRepo, WebsiteRepo, MonitoringRepo

theme_repo = ThemeRepo()
website_repo = WebsiteRepo()
monitoring_repo = MonitoringRepo()


def load_example_data():
    website_repo.put('https://en.wikipedia.org/wiki/Animal', 2)
    website_repo.put('https://en.wikipedia.org/wiki/Car', 1)
    theme_repo.put('Cats', ['cat', 'tiger', 'puma'])
    theme_repo.put('Dogs', ['dog', 'wolf'])
    theme_repo.put('Cars', ['car', 'truck', 'jeep'])


def main():
    load_example_data()
    app = App.new(theme_repo, website_repo, monitoring_repo)
    app.themes.repopulate_from_repo()
    app.websites.repopulate_from_repo()
    app.monitoring.repopulate_from_repo()
    app.draw()


if __name__ == '__main__':
    main()
