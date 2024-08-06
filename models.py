class SearchResult:
    def __init__(self, url, title, description, time):
        self.url = url
        self.title = title
        self.description = description
        self.time = time

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description}, time={self.time})"
