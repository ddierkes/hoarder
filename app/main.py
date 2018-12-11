import json, tempfile, shutil, os
from pathlib import Path

from flask import Flask, send_file, jsonify, redirect, url_for, abort, render_template, send_from_directory

import cors_workaround
import filecache

app = Flask(__name__)

crossdomain = cors_workaround.crossdomain

##### Outside of Spec
@app.route("/")
def hello_world():
    return "Welcome to Hoarder, a IIIF image caching service."

@app.route("/robots.txt")
def go_away():
    return send_file("robots.txt")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/<filename>")
@crossdomain(origin="*")
def direct_to_info(filename):
    """
    From 2.1:
    When the base URI is dereferenced, the interaction should result in the image
    information document. It is recommended that the response be a 303 status
    redirection to the image information document’s URI.
    """
    return redirect(url_for("serve_file", path=f'{filename}/info.json'), code=303)

@app.route('/<path:path>')
def serve_file(path):
    if os.path.isfile('files/'+ path):
        Path('files/'+ path).touch()
    else:
        filecache.main(path)
    return send_from_directory('files', path)


#### error handling
@app.errorhandler(400)
@crossdomain(origin="*")
def bad_request(e):
    return render_template('400.html', message=e.description), 400

@app.errorhandler(404)
@crossdomain(origin="*")
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
@crossdomain(origin="*")
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
