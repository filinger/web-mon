from crawler import Crawler
from repo import MonitoringRepo, ThemeRepo, WebsiteRepo

monitoring_repo = MonitoringRepo()
themes = [(name, keywords) for _, name, keywords in ThemeRepo().get_all()]
for _, url, depth in WebsiteRepo().get_all():
    print('Crawling {} with depth {}'.format(url, depth))
    crawler = Crawler(monitoring_repo, themes, depth)
    crawler.crawl([url])
