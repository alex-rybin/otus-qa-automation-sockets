from collections import defaultdict
from html.parser import HTMLParser


class HTMLStatsCollector(HTMLParser):
    _stats: dict = {'tags': defaultdict(int), 'most_frequent': None, 'links': [], 'images': []}

    def handle_starttag(self, tag, attrs):
        self._stats['tags'][tag] += 1

        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self._stats['links'].append(attr[1])
                    break

        elif tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self._stats['images'].append(attr[1])
                    break

    def close(self):
        super().close()
        self._stats['most_frequent'] = max(self._stats['tags'], key=self._stats['tags'].get)
        self._stats['links'] = set(self._stats['links'])
        self._stats['images'] = set(self._stats['images'])

    def get_result(self):
        self.close()
        return self._stats
