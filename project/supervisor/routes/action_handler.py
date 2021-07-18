from tornado.web import RequestHandler
from tornado.escape import url_unescape
from datetime import datetime
from validation import ActionValidation, ValidationException
import json
import logging


logger = logging.getLogger(__name__)


class ActionHandler(RequestHandler):
    """
    Handle the frontend sending commands to
    an individual Machine
    """

    validator = ActionValidation()

    def initialize(self, queue):
        self.queue = queue

    async def post(self, service_name):
        try:
            data = json.loads(self.request.body)
            self.validator.validate(data)
            logger.info(f"Received valid message {data} for {service_name} from web")
            self.set_status(204)  # NO CONTENT
            await self.queue.put({**data, "id": url_unescape(service_name)})
        except json.JSONDecodeError as e:
            logger.warn(
                f"Got malformed message {message} for {service_name} from web - {e}"
            )
            self.set_status(400)  # BAD REQUEST
        except ValidationException as e:
            logger.warn(
                f"Message {message} for {service_name} failed to validate from web - {e}"
            )
            self.set_status(400)  # BAD REQUEST
