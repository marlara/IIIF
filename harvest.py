import re
import requests_cache
import json
import requests
import os
import tldextract
import argparse

requests_cache.install_cache('cache')

user_agent = ''
headers = {'User-Agent': user_agent}

parser = argparse.ArgumentParser()
parser.add_argument('url', type = str)
args = parser.parse_args()

ext = tldextract.extract(args.url)

os.chdir(ext.domain)

file = open("list-manifest", "r")
for line in file:
	r = requests.get(line.strip("\n"), headers=headers, verify=False).json()
	name_search = re.search(r'([^\/]+)\/manifest$', line) #get manifest id from url
	name = name_search.group(1)+".json"
	print(name)
	f = open(name+".json", "w")
	json.dump(r, f) #dump and save json in file
	print(line)
print("Done")
