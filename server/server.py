#this file starts up the server and connects request/event types with event handlers
import routes
import cherrypy
from reset_controller import ResetController
from dorm_controller import DormController # getting our classes
from dorm_library import _dorm_database

def start_service():

    # create dispatcher
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    ddb = _dorm_database()

    resetController = ResetController(ddb=ddb)
    dormController = DormController(ddb=ddb)

    # use dispatcher to connect resources to event handlers
    # connect(out_tag, http resource, class object with handler, event handler name, what type of HTTP request to serve)
    dispatcher.connect('get_dorm','/dorms/:d_id/', controller=dormController, action='GET_DORM', conditions=dict(method=['GET']))
    dispatcher.connect('delete_dorm','/dorms/:d_id/', controller=dormController, action='DELETE_DORM', conditions=dict(method=['DELETE']))
    dispatcher.connect('put_dorm','/dorms/:d_id/', controller=dormController, action='PUT_DORM', conditions=dict(method=['PUT']))
    dispatcher.connect('get_index','/dorms/', controller=dormController, action='GET_INDEX', conditions=dict(method=['GET']))
    dispatcher.connect('delete_index','/dorms/', controller=dormController, action='DELETE_INDEX', conditions=dict(method=['DELETE']))
    dispatcher.connect('post_index','/dorms/', controller=dormController, action='POST_INDEX', conditions=dict(method=['POST']))

    # connect to reset controller
    dispatcher.connect('reset_index_put', '/reset/', controller=resetController, action = 'PUT_INDEX', conditions=dict(method=['PUT']))

    # default OPTIONS handler for CORS, direct to same place
    dispatcher.connect('dict_options', '/dictionary/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('dict_key_options', '/dictionary/:key', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))

    # set up configuration
    conf = {
        'global' : {
            'server.socket_host' : 'localhost', #'student04.cse.nd.edu',
            'server.socket_port' : 51023,
            },
        '/' : {
            'request.dispatch' : dispatcher,
            'tools.CORS.on' : True, # configuration for CORS
            }
    }

    # update with new configuration
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf) # create app
    cherrypy.quickstart(app)    # start app

# CORS class
class optionsController:
    def OPTIONS(self, *args, **kwargs):
        return ""

# CORS function
def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"


if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS) # CORS
    start_service()

