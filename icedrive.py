
import cloudscraper
from user import email, password

scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

###############################################################################

class	IceDrive():
	
	url = "https://icedrive.net/API/Internal/V1/"
	headers = { "Application": "application/json", "Content-Type": "application/json" }
	response:object

	# -------------------------------------------------------------------------------

	def __init__(self, *arg, **kwargs):
		self.login()

	def get(self, params):
		self.response = scraper.get(self.url, params=params, headers=self.headers)
		return self.response

	def post(self, params):
		self.response = scraper.post(self.url, params=params, headers=self.headers)
		return self.response

	def login(self):
		params = {
			"password": password,
			"email": email,
			"request": "login"
		}
		self.get(params)
		self.headers["Authorization"] = f"Bearer {self.response.json()['token']}"

	# -------------------------------------------------------------------------------

	def user_data(self):
		self.get({"request":"user-data"})

	def list_folders(self, fid=0):
		params = {
			"request": "collection",
			"type": "cloud",
			"folderId": fid,
		}
		self.get(params)
		for file in self.response.json()['data']:
			print(file['filename'], "->", file['id'])

	def share_details(self, item_id):
		params = {
			"request": "share-details",
			"itemId": item_id,
			"type": "folder" if "folder" in item_id else "file",
		}
		self.get(params)

	def public_toggle(self, item_id):
		params = {
			"request": "public-toggle",
			"itemId": item_id,
			"type": "folder" if "folder" in item_id else "file",
		}
		self.post(params)
		return self.response.json()["link"]

#