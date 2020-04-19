import argparse

from html_parser import HTMLStatsCollector
from http_client import HttpClient

argp = argparse.ArgumentParser()
argp.add_argument('-n', '--hostname', help='Host to request. For example: "python.org"')
argp.add_argument(
    '-p', '--path', help='URL path after hostname. For example: "search/?q=macos&submit="'
)
args = argp.parse_args()

client = HttpClient()
response = client.request('GET', host=args.hostname, path=args.path)

parser = HTMLStatsCollector()
parser.feed(response.body)
result = parser.get_result()

print('Tags:')
for key, value in result['tags'].items():
    print(f'{key}: {value}')
print()
print(f'Most frequent tag: {result["most_frequent"]}\n')
print('Links:')
for link in result['links']:
    print(link)
print()
print('Images:')
for image in result['images']:
    print(image)
