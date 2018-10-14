
import requests
from PIL import Image
from io import BytesIO

class GPI:
	def __init__(self):
		"""General Plugin Interface"""
		pass
		try:
			pass
		except Exception as e:
			print ("Failed to get resources... {}\n".format(e))
	
	#HTTP requests
	def get_requests(self, url):
		request = requests.get(str(url))
		#### request to json ####
		return request.json()

	def post_requests(self, url, data = {'key':'value'}):
		request = requests.post(str(url), data)
		#### Final URL location of Response. ####
		return request.url

	def delete_requests(self, url):
		request = requests.delete(str(url))
		#### Integer Code of responded HTTP Status, e.g. 404 or 200. ####
		return request.status_code
	
	def head_requests(self, url):
		request = requests.head(str(url))
		#### Textual reason of responded HTTP Status, e.g. "Not Found" or "OK". ####
		return request.reason

	def options_requests(self, url):
		request = requests.options(str(url))
		#### Content of the response, in unicode ####
		return request.text

	def binary_request_to_IMG(self, request):
		img = Image.open(BytesIO(request.content))
		return img


class Main_algo(GPI):
	"""docstring for Main_algo"""
	def __init__(self):
		pass
		GPI.__init__(self)

	def currentProcessInfo(self, url):
		"""This is your First API Interface"""
		# To do !!
		return GPI.get_requests(self, url)
