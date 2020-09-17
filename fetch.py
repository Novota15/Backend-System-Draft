# file fetching app
import requests
import datetime
import db
import re

# the Content-Disposition header contains filename info
def get_filename_from_cd(r, address):
	fname = ''
	if "Content-Disposition" in r.headers.keys():
		fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
	else:
		fname = address.split("/")[-1]
	return fname

# grab file from given url, update db, store
def fetch(session, url):
	try:
		r = requests.get(url.address, allow_redirects=True)
	except:
		print("invalid url")
		return

	db.update_url(session, url.address, "last_fetched", datetime.datetime.now())

	# get files from db associated with this url
	files = db.get_files_by_url(session, url.id)
	
	last_modified = r.headers.get('Last-Modified')
	for f in files:
		# check head to see when file was last modified and if it matches a file in the db
		if  last_modified == f.last_modified:
			return

	# if we make it here, no file's last modified value matched, so we have a new file version
	# get name and store
	filename = get_filename_from_cd(r, url.address)
	# print(r.content)
	print(filename)
	open("file_storage/" + filename, 'wb').write(r.content)

	# add file info to db
	db.add_file(session, filename, url.id, "file_storage"+filename, False, last_modified)

	# make call to verification apps
	
	return

def create_fetch_list(session, urls):
	# build list of URLs that need to be fetched based on their intervals
	fetch_list = []
	for url in urls:
		if check_url_interval(session, url) == True:
			fetch_list.append(url)
	return fetch_list

# check interval and compare with current hour
def check_url_interval(session, url):
	now = datetime.datetime.now()
	value = int(url.interval[:-1]) # get integer from interval
	if url.interval[-1] == 'h': # hour based interval
		if now.hour % value == 0:
			return True
	elif url.interval[-1] == 'd': # day based interval
		if (now.hour * 24) % value == 0:
			return True
	return False

def main():
	# init database
	session = db.init_session()

	# grab enabled urls
	urls = db.get_all_enabled_urls(session)

	# check for files needing to be fetched, add to queue
	fetch_list = create_fetch_list(session, urls)

	for url in fetch_list:
		fetch(session, url)

	# close db connection
	db.close(session)
	return

if __name__ == "__main__":
	main()