from crawler import Crawler
from repo import MonitoringRepo, ThemeRepo, WebsiteRepo

urls = [url for _, url in WebsiteRepo().get_all()]
themes = [(name, keywords) for _, name, keywords in ThemeRepo().get_all()]
crawler = Crawler(MonitoringRepo(), themes, 1)

crawler.crawl(urls)
