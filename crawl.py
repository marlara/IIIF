import requests
import requests_cache
import argparse
import tldextract
import json
import os



requests_cache.install_cache('cache')

user_agent = '' #your user agent
headers = {'User-Agent': user_agent}

def collections_search():
	global collection #you need this element to be global (same on the other functions)
	global file
	page1 = requests.get(collection["@id"], headers=headers, verify=False).json()
	print(collection["@id"])
	file.write("Subcollection: "+collection["@id"])
	n = 0
	if "manifests" in page1:
		for el in page1["manifests"]:
			manifest = el["@id"]
			print(manifest)
			manifest_list.write(manifest+"\n")
			n+=1
			
	elif "members" in page1:
		for el in page1["members"]:
			n = 0
			manifest = el["@id"]
			print(manifest)
			manifest_list.write(manifest)
			n+=1
	else:
		try: #some collections could be completely empty
			for collection in page1["collections"]:
				collections_search()
		except:
			print(collection["@id"]+" empty")
			file.write("Subcollection: "+collection["@id"])
	file.write(" Items:"+str(n)+"\n")

def next_page():
	global page_next
	for element in page_next["manifests"]:
		manifest = element["@id"]
		print(manifest)
		manifest_list.write(manifest+"\n")
	if "next" in page_next:
		page_next = requests.get(page_next["next"], headers=headers, verify=False).json()
		print(page_next["next"])
		next_page()
	else:
		pass

def collection_members_search():
	global member
	global file
	page1 = requests.get(member["@id"], headers=headers, verify=False).json()
	print(member["@id"])
	file.write("Subcollection: "+member["@id"]+"\n")
	n = 0
	if "manifests" in page1:
		manifest_search()
	else:
		for member in page1["members"]:
			manifest = member["@id"]
			print(manifest)
			manifest_list.write(manifest+"\n")
			n+=1
	file.write(" Items:"+str(n)+"\n")


def manifest_search():
	global element
	n = 0
	for element in page["manifests"]:
			manifest = element["@id"]
			print(manifest)
			manifest_list.write(manifest+"\n")
			n+=1
	file.write(" Items:"+str(n)+"\n")

parser = argparse.ArgumentParser()
parser.add_argument('url', type = str)
args = parser.parse_args()

ext = tldextract.extract(args.url)
print(ext.domain)
os.mkdir(ext.domain) #create a directory named after the general url domain
os.chdir(ext.domain) #change into that directory

manifest_list = open("list-manifest", "w")
file = open(ext.domain+".readme", "w")

page = requests.get(args.url, headers=headers, verify=False).json()
file.write("Collection id: "+args.url+"\n")
if "manifests" in page:
	print("manifest type")
	
elif "members" in page:
	print("members type")
	for member in page["members"]:
		if member["@type"] == "sc:Collection":
			collection_members_search()
		else:
			manifest = member["@id"]
			print(manifest)
			manifest_list.write(manifest)
			manifest_list.write("\n")
elif "collections" in page:
	for collection in page["collections"]:
		collections_search()
elif "first" in page:
	page_next = requests.get(page["first"], headers=headers, verify=False).json()
	next_page()
else:
	print("type unknown")
print("Done")
