from flask import Flask
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

import os
import requests

application = app = Flask(__name__)

xray_recorder.configure(service='Flask app from daemon test')
XRayMiddleware(app, xray_recorder)
patch_all()

# test http instrumentation
@app.route('/outgoing-http-call')
def callHTTP():
    requests.get("https://aws.amazon.com")
    return "Ok! tracing outgoing http call"

@app.route('/')
def default():
    return "healthcheck"


if __name__ == "__main__":
    address = os.environ.get('LISTEN_ADDRESS')

    if address is None:
        host = '127.0.0.1'
        port = '5000'
    else:
        host, port = address.split(":")
    app.run(host=host, port=int(port), debug=True)
