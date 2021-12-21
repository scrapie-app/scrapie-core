class ScrapeRoute:
    def __init__(self, app, options) -> None:
        @app.get("/scrape")
        def root():
            options.appLogger.debug('reached scrape root')
            return { 'hello': 'yeah' }