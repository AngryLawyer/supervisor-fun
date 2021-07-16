from routes.main_handler import MainHandler
from routes.list_handler import ListHandler
from routes.action_handler import ActionHandler

def make_routes(database, main_queue):
    return [
        (r'/([A-Za-z0-9_%-]+)/action', ActionHandler, {'queue': main_queue}),
        ('/list', ListHandler, {'database': database}),
        (r'/', MainHandler),
    ]
