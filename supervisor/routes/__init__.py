from routes.main_handler import MainHandler
from routes.callback_handler import CallbackHandler
from routes.list_handler import ListHandler

def make_routes(database):
    return [
        ('/callback', CallbackHandler, {'database': database}),
        ('/list', ListHandler, {'database': database}),
        (r'/', MainHandler, {'database': database}),
    ]
