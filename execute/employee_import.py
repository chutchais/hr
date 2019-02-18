import os.path
import os

def upload_employee(data):
	try :
		url = "http://127.0.0.1:8000/employee/upload"
		service = 'employee'
		import urllib3
		http = urllib3.PoolManager()
		import json
		print (data)
		# import requests
		os.environ['NO_PROXY'] = url
		headers = {'Content-type': 'application/json'}
		# headers = urllib3.util.make_headers(basic_auth='admin:lcb12017',content_type='application/json')
		url_service = url
		# print (url_service)
		r = http.request('POST', url_service,headers=headers,body=json.dumps(data))
		# print (r.data)
		return json.loads(r.data.decode('utf-8'))
	except:
		print ('Error on upload function : %s' % sys.exc_info()[0])
		r = {'msg':sys.exc_info()[0],
							'created':False}
		return json.loads(r)

import sys
from openpyxl import load_workbook
wb2 = load_workbook('C:\\Users\\Chutchai\\Documents\\Project Plan\\2019\\HR-OT system\\Namelist-ENG2.xlsx',read_only=True)
ws = wb2['Sheet1']
first_row = True
for row in ws.rows :
	if first_row :
		first_row = False
		continue
	en 	= row[1].value
	first_name 	=  row[2].value
	last_name 	=  row[3].value
	section 	=  row[6].value
	company 	=  row[7].value
	data ={
		'username' : ('%s.%s')%(first_name,last_name[:1]),
		'en' : en,
		'first_name' : first_name,
		'last_name'  : last_name,
		'section'	: section,
		'company' : company
	}
	s=upload_employee(data)
	print (s)
	# sys.exit()


