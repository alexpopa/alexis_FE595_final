from app import flask_app as app
from flask import request, render_template
from flask import send_file


@app.route('/send/<fname>')
def send_any(fname):
    fname = fname.replace('&', '/')
    try:
        return send_file(fname)
    except Exception as e:
        print(e)

@app.route('/download_data')
def raw_data():
    try:
        return send_file("real_estate.csv")
    except:
        print(e)
