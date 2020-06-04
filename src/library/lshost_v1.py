#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import urllib3
def spectrum_auth(module,username,password,config_ip):
	
	headers = {
			"X-Auth-Username":username,
			"X-Auth-Password":password,
		}
	
	url = 'https://{0}/rest/auth'.format(config_ip)
	
	try:
		response = fetch_url (module, url, headers=headers,method ='POST',verify_certs=False)
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
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	rc, auth_content, error = spectrum_auth(module, username,password,config_ip)
	if rc==0:
		module.exit_json(changed = True, meta = auth_token)
	else:
		module.fail_json(msg = 'Error in repo', meta = error)

if __name__ == '__main__':
	main()
