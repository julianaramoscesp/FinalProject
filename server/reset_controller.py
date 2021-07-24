import cherrypy
import re, json
from dorm_library import _dorm_database

class ResetController(object):
	
	def __init__(self, ddb=None):
		if ddb is None:
			self.ddb = _dorm_database()
		else:
			self.ddb = ddb

	def PUT_INDEX(self):
		output = {'result': 'success'}

		data = json.loads(cherrypy.request.body.read().decode())

		self.ddb.__init__()
		self.ddb.load_dorms('dorm.dat')
		self.ddb.get_dorms()

		return json.dumps(output)
