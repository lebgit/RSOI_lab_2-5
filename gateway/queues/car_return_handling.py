import common.message_queue
import threading
import jsonpickle
import requests
from config import current_config
from gateway import app


class Request:
    def __init__(self, type, data):
        self.type = type
        self.data = data


class CarReturnHandling(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = common.message_queue.MessageQueue(["my_queue"], delay=5.0)
        self.queue.bind("my_queue", "car_return_handling_request")

    def run(self):
        while True:
            request_serialized = self.queue.receive_message("my_queue")
            request = jsonpickle.decode(request_serialized)
            if request.type == "CAR_RETURN":
                try:
                    response = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                                              "/%s" % request.data["fix_id"], jsonpickle.encode(request.data["payload"]))
                    if response.status_code == 201:
                        app.logger.info('Возврат успешно завершен')
                    else:
                        app.logger.warning('Возврат не может быть завершено')
                        self.queue.send_message(request_serialized, "car_return_handling_request")
                except:
                    app.logger.warning(
                        'Возврат не может быть завершено, добавление запроса в очередь')
                    self.queue.send_message(request_serialized, "car_return_handling_request")

