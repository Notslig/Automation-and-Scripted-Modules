from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    pass 

def run():
    app.run(host='0.0.0.0', port=8080)
    
def keepalive():
    thread = Thread(target=run)
    thread.start()