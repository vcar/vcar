def set_main_algo(interfaces):
	main = """
import requests
from PIL import Image
from io import BytesIO

class GPI:
	def __init__(self):
		\"\"\"General Plugin Interface\"\"\"
		pass
		try:
			pass
		except Exception as e:
			print (\"Failed to get resources... {}\\n\".format(e))
	
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
	\"\"\"docstring for Main_algo\"\"\"
	def __init__(self):
		pass
		GPI.__init__(self)

	def currentProcessInfo(self, url):
		\"\"\"This is your First API Interface\"\"\"
		# To do !!
		return GPI.get_requests(self, url)
"""
	for interface in interfaces:
		args_dt="No args !!"
		args=""
		nb_args=len(interface["InputArgs"])
		if nb_args>0:
			args_dt=''''''
			i = 0
			args = args+", "
			for arg in interface["InputArgs"]:
				i=i+1
				name = str(arg["ArgName"])
				Type = str(arg["ArgType"])
				if name=="":
					name="arg_name_"+str(i)
				if Type=="":
					Type="your type"
				args = args+name

				args_dt = args_dt + '''Arg'''+str(i)+''' : 
					'''+name+''' ('''+Type+'''): ....
				'''
				if (i+0)<nb_args:
					args = args+", "
				

		main = main + '''
	def '''+str(interface["InterfaceName"])+'''(self'''+args+'''):
		\"\"\"
		docstring for '''+str(interface["InterfaceName"])+''' API Interface :
			Input :
				'''+args_dt+'''
			
			Output : Json Format

			Draw Format : This Output designed to be visualized as '''+str(interface["DrawFormat"])+'''

		\"\"\"
		# To do !!

		# Return your result in Json Format
		return {"key":"value"}
'''


	return main