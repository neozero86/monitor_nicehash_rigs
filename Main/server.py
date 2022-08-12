from flask import Flask, render_template
import os
import time

app = Flask(__name__)
LOG_FILE = 'logs/out.log'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def logs():
    def generate(): 
        logfile = open(LOG_FILE,"rb")
        try:
            logfile.seek(-2000, os.SEEK_END)
        except OSError:
            logfile.seek(0)
        while True:
            line = logfile.readline().decode()
            if not line:
                time.sleep(0.05)
                continue

            yield line  

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