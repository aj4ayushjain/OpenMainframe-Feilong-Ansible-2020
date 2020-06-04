#!/usr/bin/python

from ansible.module_utils.basic  import *
import requests

def authenticate(username,password,config_ip):
	headers = {
	"X-Auth-Username":"{0}".format(username),
	"X-Auth-Password":"{0}".format(password),
	}
	print config_ip
	url = "{0}{1}{2}{3}".format('https://',config_ip,':7443','/rest/auth')
	response = requests.post(url,headers=headers,verify=False)
	return response.text

def main():
	
	fields = {
		"api_username": {"required":True,"type":"str"},
		"api_password": {"required":True,"type":"str"},
		"storage_config_ip": {"required":True,"type":"str"}
	}
	module = AnsibleModule(argument_spec=fields)
	username = module.params['api_username']
	password = module.params['api_password']
	config_ip = module.params['storage_config_ip']			
	url = "{0}{1}{2}{3}".format('https://',config_ip,':7443','/rest/lshost')
	

	headers = {
		"X-Auth-Token": authenticate(username,password,config_ip),
	}
	
	response =  requests.post(url,headers = headers,verify = False)	
	module.exit_json(changed=False,meta=response)

if __name__ == '__main__':
	main()
