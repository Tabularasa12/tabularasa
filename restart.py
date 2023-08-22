from flask import request
import subprocess
request.environ.get('werkzeug.server.shutdown')()
subprocess.run(['python3', 'run.py'])