from src.handlers import request_handler
from japronto import Application
import os

def handler(req):
    return req.Response(text=request_handler.handle_request(req.json))


app = Application()
print(os.environ)
app.router.add_route('/api', handler)
app.run(host='0.0.0.0', debug=True, worker_num=5, port=8080)
