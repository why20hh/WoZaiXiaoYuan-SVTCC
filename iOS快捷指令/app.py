from flask import Flask
import get_address
from gevent import pywsgi

app = Flask(__name__)


@app.route('/')
def get_dk_address():  # 返回打卡地址和认证信息
    dk = get_address.first_get_time()
    return dk

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=5233)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5233), app)
    server.serve_forever()
