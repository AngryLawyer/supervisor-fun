from routes.main_handler import MainHandler
from routes.list_handler import ListHandler

def make_routes(database, main_queue):
    return [
        ('/list', ListHandler, {'database': database}),
        (r'/', MainHandler, {'database': database}),
    ]
