import requests
import requests_cache

manifest_list = open("list-manifest", "w")

requests_cache.install_cache('cache')

user_agent = '' #your user agent
headers = {'User-Agent': user_agent}

def collections_search():
	global collection #you need this element to be global (same on the other functions)
	page1 = requests.get(collection["@id"], headers=headers, verify=False).json()
	print(collection["@id"])
	manifest_list.write("Collection: "+collection["@id"]+"\n")
	if "manifests" in page1:
		for el in page1["manifests"]:
			manifest = el["@id"]
			print(manifest)
			manifest_list.write(manifest)
			manifest_list.write("\n")
	elif "members" in page1:
		for el in page1["members"]:
			manifest = el["@id"]
			print(manifest)
			manifest_list.write(manifest)
			manifest_list.write("\n")
	else:
		try: #some collections could be completely empty
			for collection in page1["collections"]:
				collections_search()
		except:
			print(collection["@id"]+" empty")
			manifest_list.write("Collection: "+collection["@id"]+" empty\n")

def next_page():
	global page_next
	for element in page_next["manifests"]:
		manifest = element["@id"]
		print(manifest)
		manifest_list.write(manifest)
		manifest_list.write("\n")
	if "next" in page_next:
		page_next = requests.get(page_next["next"], headers=headers, verify=False).json()
		print(page_next["next"])
		next_page()
	else:
		pass

def collection_members_search():
	global member
	page1 = requests.get(member["@id"], headers=headers, verify=False).json()
	print(member["@id"])
	manifest_list.write("Collection: "+member["@id"]+"\n")
	if "manifests" in page1:
		manifest_search()
	else:
		for member in page1["members"]:
			manifest = member["@id"]
			print(manifest)
			manifest_list.write(manifest)
			manifest_list.write("\n")
 def manifest_search():
	global element
	for element in page["manifests"]:
			manifest = element["@id"]
			print(manifest)
			manifest_list.write(manifest)
			manifest_list.write("\n")


url_list = [] #list of collection endpoint (json)

for url in url_list:
	print(url)
	manifest_list.write("Url: "+url+"\n")
	try:
		page = requests.get(url.strip(), headers=headers, verify=False).json()
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
	except ValueError:
		print(url+ "Json Error")
		manifest_list.write(url + "Json Error"+"\n")
print("Done")
