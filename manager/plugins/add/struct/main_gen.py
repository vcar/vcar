def set_main_algo(interfaces):
	main = """
class Main_algo():
    \"\"\"docstring for Main_algo\"\"\"
    def __init__(self):
        pass

    def salutation(self, somebody):
    	\"\"\"This is your First API Interface\"\"\"
        # To do !!
        return {"msg":"Hi "+somebody+"! Welcome to Vcar platform"}
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