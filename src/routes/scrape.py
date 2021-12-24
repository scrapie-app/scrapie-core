import requests
from schema import website

class ScrapeRoute:
    def __init__(self, app, options) -> None:
        @app.post("/scrape/ping")
        def testWebsite(website: website.Website):
            options['appLogger'].debug(f'Testing website connection for {website}')
            try:
                r = requests.get(website.url, timeout=10)
                website.url = r.url
                website.protocol = r.url[:r.url.find(':')]
                if r.status_code == 200:
                    website.body = r.text
                    website.reachable = True
                    website.dnsResolved = True
            except requests.exceptions.TooManyRedirects as te:
                website.reachable = False
                website.dnsResolved = True
            except requests.ConnectionError as e:
                if 'nodename nor servname provided, or not known' in str(e):
                    website.dnsResolved = False
            except requests.exceptions.RequestException:
                pass
            return website