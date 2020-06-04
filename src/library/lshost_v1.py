#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
def spectrum_auth(username,password,config_ip):
	
	request_type = 'POST'
	headers = {
			"X-Auth-Username":username,
			"X-Auth-Password":password,
		}
	
	url = 'https://{0}/rest/auth'.format(config_ip)
	
	try:
		response = open_url (url,headers=headers,method = request_type,verify=False)
		data = json.loads(response.read())
		if data['status']['message']=='Authentication failed':
			return 1,None, "Authentication failed"	
		else:
			auth_content = data

	except Exception as e:
		return 1, None, e
	return 0, auth_content, None
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
	
	rc, auth_token, error = spectrum_auth(username,password,config_ip)
	if rc==0:
		module.exit_json(changed = True, meta = result)
	else:
		module.fail_json(msg = 'Error in repo', meta = result)

if __name__ == '__main__':
	main()