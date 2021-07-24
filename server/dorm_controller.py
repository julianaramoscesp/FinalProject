import json
import cherrypy
from dorm_library import _dorm_database

class DormController(object):

    def __init__(self, ddb=None):
        if ddb is None:
            self.ddb = _dorm_database()
        else:
            self.ddb = ddb
            
        self.ddb.load_dorms('/Users/julianaramos/paradigms/ComplexRESTServer/dorm.dat')


    # event handlers
    def GET_DORM(self, d_id):
        # default output
        output = {'result': 'success'}
        d_id = int(d_id)
        
        try:
            dorm = self.ddb.get_dorm(d_id)
            if dorm is not None:
                output['name'] = dorm[0]
                output['year'] = dorm[1]
                output['gender'] = dorm[2]
                output['quad'] = dorm[3]
                output['mascot'] = dorm[4]
            else:
                output['result'] = 'error'
                output['message'] = 'no dorm found'
        except KeyError as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)
   

    def PUT_DORM(self, d_id):
        output = {'result':'success'}
        d_id = int(d_id)
        # extract msg from body
        data = cherrypy.request.body.read().decode('utf-8')
        print(data)
        data = json.loads(data)

        dorm = list()
        dorm.append(data['name'])
        dorm.append(data['year'])
        dorm.append(data['gender'])
        dorm.append(data['quad'])
        dorm.append(data['mascot'])

        self.ddb.set_dorm(d_id, dorm)

        return json.dumps(output)

    def DELETE_DORM(self, d_id):
        output = {'result':'success'}
        d_id = int(d_id)
        
        try:
            self.ddb.delete_dorm(d_id)
        except KeyError as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        
        return json.dumps(output)

    def POST_INDEX(self):
        output = {'result':'success'}
        #d_id = int(d_id)
        # extract msg from body
        data = cherrypy.request.body.read().decode('utf-8')
        print(data)
        data = json.loads(data)

        try:
            dorms = list(self.ddb.get_dorms())
            newID = int(dorms[-1]) + 1
            output['id'] = newID

            dorm = list()
            dorm.append(data['name'])
            dorm.append(data['year'])
            dorm.append(data['gender'])
            dorm.append(data['quad'])
            dorm.append(data['mascot'])

            self.ddb.set_dorm(newID, dorm)

        #return json.dumps(output)
        #output = {'result':'success'}
        # extract msg from body
        #data = cherrypy.request.body.read().decode('utf-8')
        #data = json.loads(data)
        #print("body data: " + str(data))

        #try:
            #dorms = list(self.ddb.get_dorms())
            #newID = int(dorms[-1]) + 1
            #self.ddb.dorm_info[newID] = data
            #output['id'] = newID
            
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)

    def GET_INDEX(self):

        output = {'result' : 'success'}
        try:
            for d_id in self.ddb.get_dorms():
                dorm = self.ddb.get_dorm(d_id)
                d_dorm = {'name': dorm[0], 'year': dorm[1], 'gender': dorm[2], 'quad': dorm[3], 'mascot': dorm[4]}
                output[d_id] = d_dorm

        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)

    def DELETE_INDEX(self):
        output = {'result':'success'}
        try:
            #for key, value in self.myd.items():
            allDorms = list(self.ddb.get_dorms())
            for d_id in allDorms:
                self.ddb.delete_dorm(d_id)

        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        
        return json.dumps(output)