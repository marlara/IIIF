import re
import requests_cache
import json
import requests
import os
import tldextract
import argparse

requests_cache.install_cache('cache')

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'
headers = {'User-Agent': user_agent}

parser = argparse.ArgumentParser()
parser.add_argument('url', type = str)
args = parser.parse_args()

ext = tldextract.extract(args.url)

os.chdir(ext.domain)

file = open("list-manifest", "r")
for line in file:
	r = requests.get(line.strip("\n"), headers=headers, verify=False).json()
	name_search = re.search(r'([^\/]+)\/manifest$', line)
	name = name_search.group(1)+".json"
	print(name)
	f = open(name+".json", "w")
	json.dump(r, f)
	print(line)
print("Done")
