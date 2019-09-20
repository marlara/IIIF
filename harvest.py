import os
import tldextract
import requests_cache
import requests
import hashlib
import json

requests_cache.install_cache('cache')


file = open("list-manifest", "r")

def save_manifest():
	user_agent = '' #your user agent
	headers = {'User-Agent': user_agent}
	h = hashlib.sha256()
	global file
	
	next(file) #go to the next line
	for line in file:
		if "Collection:" in line:
			os.chdir("..")
			collection_url = line.strip("Collection: ").strip("\n")
			cl_ext = collection_url.split("/")[-1] #create a subfolder with the name of the collection (this logic is not perfect)
			print(cl_ext)
			os.mkdir(cl_ext)
			os.chdir(cl_ext)
			break
		else:
			r = requests.get(line.strip("\n"), headers=headers, verify=False).json()
			f = open(h.hexdigest()+".json", "w")
			json.dump(r, f)
			print(line)


for line in file:
	if "Url:" in line:
		url = line.strip("Url: ")
		print(url)
		ext = tldextract.extract(url)
		print(ext.domain)
		os.mkdir(ext.domain) #create a directory named after the general url domain
		os.chdir(ext.domain) #change into that directory
	elif "Collection:" in line:
		collection_url = line.strip("Collection: ").strip("\n") #create a subfolder with the name of the collection
		cl_ext = collection_url.split("/")[-1]
		print(cl_ext)
		os.mkdir(cl_ext)
		os.chdir(cl_ext)
		save_manifest()
	else:
		save_manifest()
print("Done")
file.close()
