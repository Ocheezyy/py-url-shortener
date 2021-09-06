from flask import Flask, request, redirect, flash, url_for, render_template
from flask_cors import CORS
import dbUtils
import os

template_dir = os.path.abspath("/workspace/Templates/")
app = Flask(__name__, template_folder=template_dir)
CORS(app)

# root_path = os.path.dirname(os.path.abspath(__file__)) 

################################
#   ROUTES
################################

def get_template(template_name):
    return template_name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.jinja2')

    if request.method == 'POST':
        url = request.form['urlToAdd']
        if not url:
            urlCreated = request.form['urlCreated']
            if urlCreated == "urlCreated":
                return render_template(get_template('index.jinja2'), url_created=False)

            flash('The url is required')
            return redirect(url_for('index'))
        
        result = dbUtils.create_url(url, request.base_url)    
        return render_template(get_template('index.jinja2'), url_created=True, created_url=result)


@app.route("/stats", methods=["GET", "POST"])
def url_stats():
    if request.method == 'GET':
        return render_template('url_stats.jinja2', urlFetched=False)
    if request.method == 'POST':
        url_to_fetch = request.form['urlToFetch']
        if ".com" in url_to_fetch or ".dev" in url_to_fetch:
            url_to_fetch = url_to_fetch.split('/u/')[1]
        result = dbUtils.get_url_stats(url_to_fetch)
        return render_template(get_template('url_stats.jinja2'), stats=result, urlFetched=True)

@app.route("/u/<string:url>", methods=["GET"])
def get_url(url):
    if url is not None:
        result = dbUtils.get_url(url)
        if result is None:
            return 404
        return redirect(result)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)