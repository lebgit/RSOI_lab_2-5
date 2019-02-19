from flask import Flask
import common.message_queue


app = Flask(__name__)
replay_request_queue = common.message_queue.MessageQueue()
