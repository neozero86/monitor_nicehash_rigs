from flask import Flask, Response, render_template
from pygtail import Pygtail
import time

app = Flask(__name__)
LOG_FILE = 'logs/out.log'
reader = Pygtail(LOG_FILE, every_n=1)
reader.readlines()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def logs():
    def generate():      
        while True:
            for line in reader:
                if not line:
                    string = '\n'
                else:
                    string = str(line)
                yield string
                time.sleep(0.05)  

    return app.response_class(generate(), mimetype='text/event-stream')

@app.route('/daily')
def daily():
    return app.send_static_file('daily.html')

@app.route('/weekly')
def weekly():
    return app.send_static_file('weekly.html')

@app.route('/monthly')
def monthly():
    return app.send_static_file('monthly.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)