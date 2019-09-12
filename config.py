import os
import json

def config_file_exists():
	root_directory = os.listdir('./')
	for file in root_directory:
		if file == 'settings.conf':
			return True
	return False

def create_config_file():
	host_name = input('Your AWS IoT Endpoint (can be found under settings in the AWS IoT dashboard): ')
	thing_name = input('Your Thing name: ')
	print('Thanks! If needed you can edit the config file at ./settings.conf\n')
	with open("settings.conf", 'w+') as config_file:
		config_json = {'host_name': host_name, 'thing_name': thing_name}
		config_file.write(json.dumps(config_json))

