
import cloudscraper
from user import email, password

scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

###############################################################################

class	ContentList():
	arr = []

	def __init__(self, *arg, **kwargs):
		pass

	def new_arr(self, array):
		i:int = 0
		self.arr = []
		for file in array:
			self.arr.append(file)
			print(f"{i}.	{file['id']}	->	{file['filename']}")
			i += 1

	def select(self, id):
		print(f"[INFO  ]: selected item -> {self.arr[id]['uid']} ({self.arr[id]['filename']})")
		return self.arr[id]['uid']

###############################################################################

class	IceDrive():
	
	url = "https://icedrive.net/API/Internal/V1/"
	headers = { "Application": "application/json", "Content-Type": "application/json" }
	response:object
	content:ContentList = ContentList()

	# -------------------------------------------------------------------------------

	def __init__(self, *arg, **kwargs):
		self.login()

	def error(self) -> bool:
		if self.response.json()['error']:
			print("[ERROR ]: ", self.response.json())
			return True
		return False

	def get(self, params) -> bool:
		self.response = scraper.get(self.url, params=params, headers=self.headers)
		if not self.error():
			return True
		return False

	def post(self, params) -> bool:
		self.response = scraper.post(self.url, params=params, headers=self.headers)
		if not self.error():
			return True
		return False

	def login(self):
		params = {
			"password": password,
			"email": email,
			"request": "login"
		}
		if self.get(params):
			print("[INFO  ]: Logged in")
			self.headers["Authorization"] = f"Bearer {self.response.json()['token']}"


	# -------------------------------------------------------------------------------

	def user_data(self):
		self.get({"request":"user-data"})

	def list_folders(self, fid=0, list_id=-1):
		if list_id != -1: fid = self.content.select(list_id)
		params = {
			"request": "collection",
			"type": "cloud",
			"folderId": fid,
		}
		if self.get(params):
			self.content.new_arr(self.response.json()['data'])

	def share_details(self, item_id=0, list_id=-1):
		if list_id != -1: item_id = self.content.select(list_id)
		params = {
			"request": "share-details",
			"itemId": item_id,
			"type": "folder" if "folder" in item_id else "file",
		}
		if self.get(params):
			print("{")
			json = self.response.json()
			for key in json:
				print(f"	{key}:	{json[key]},")
			print("}")

	def public_toggle(self, item_id=0, list_id=-1, password=""):
		if list_id != -1: item_id = self.content.select(list_id)
		params = {
			"request": "public-toggle",
			"itemId": item_id,
			"type": "folder" if "folder" in item_id else "file",
		}
		if self.post(params):
			if "link" in self.response.json():
				print(self.response.json()["link"])
				return self.response.json()["link"]
			else:
				print("[INFO  ]: Disabled public-link for file/folder")
				return "none"

#