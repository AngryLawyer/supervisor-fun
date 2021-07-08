from routes.main_handler import MainHandler
from routes.callback_handler import CallbackHandler

def make_routes(database):
    return [
        ('/callback', CallbackHandler, {'database': database}),
        (r'/', MainHandler, {'database': database}),
    ]
