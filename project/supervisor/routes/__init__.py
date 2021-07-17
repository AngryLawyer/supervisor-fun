from supervisor.routes.main_handler import MainHandler
from supervisor.routes.list_handler import ListHandler
from supervisor.routes.action_handler import ActionHandler


def make_routes(database, main_queue):
    """
    Creates handlers for routes for the webserver to consume
    """

    return [
        (r'/([A-Za-z0-9_%-]+)/action', ActionHandler, {'queue': main_queue}),
        ('/list', ListHandler, {'database': database}),
        (r'/', MainHandler),
    ]
