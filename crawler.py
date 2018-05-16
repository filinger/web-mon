import ssl
from datetime import datetime
from html.parser import HTMLParser
from urllib import parse
from urllib.request import urlopen


class LinkParser(HTMLParser):
    # "Fix" to ignore SSL errors
    ssl._create_default_https_context = ssl._create_unverified_context

    def __init__(self):
        super().__init__()
        self.links = []
        self.base_url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    url = parse.urlparse(value)
                    # Follow only same host pages
                    if not url.netloc:
                        new_url = parse.urljoin(self.base_url, url.path)
                        self.links.append(new_url)

    def parse(self, url):
        self.links = []
        self.base_url = url
        response = urlopen(url)

        if response.getheader('Content-Type') == 'text/html; charset=UTF-8':
            html_text = response.read().decode('utf-8')
            self.feed(html_text)
            return html_text, self.links
        else:
            return '', []

    def error(self, message):
        pass


class Crawler(object):
    def __init__(self, repo, themes, max_depth):
        self.repo = repo
        self.themes = themes
        self.max_depth = max_depth
        self.current_depth = 0
        self.visited = set()

    def crawl(self, urls):
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            return

        for url in urls:
            if url in self.visited:
                continue

            parser = LinkParser()
            data, links = parser.parse(url)
            for theme, words in self.themes:
                for word in words:
                    # Check only words with whitespaces as word boundaries
                    if data.find(' ' + word + ' ') > -1:
                        timestamp = datetime.now()
                        print('{}: found {} ({}) in {}'.format(timestamp, theme, word, url))
                        self.repo.put(timestamp, url, theme)

            self.visited.add(url)
            self.crawl(links)
