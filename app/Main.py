from app import app
from app import news
from app import weather

import threading

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)#, port=5000)

# suggested way
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''
## server on http://0.0.0.0:5000/
## visible across the network
## BaseUrl for Android http://<your ip address>:5000/blah/blah