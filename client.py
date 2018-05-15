from repo import WebsiteRepo, ThemeRepo, MonitoringRepo

sites = WebsiteRepo()
themes = ThemeRepo()
monitoring = MonitoringRepo()

sites.put('https://en.wikipedia.org/wiki/Animal')
themes.put('Cats', ['cat', 'tiger', 'puma'])
themes.put('Dogs', ['dog', 'wolf'])

print(monitoring.get_all())
