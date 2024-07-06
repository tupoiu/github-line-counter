from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/loc")
def loc():
    git_link = request.args.get('git_link')
    # git_link = "https://github.com/huertatipografica/HTLetterspacer.git"
    if not git_link:
        return "", 400

    # Count the lines and put the result in a variable
    # lines = subprocess.(["bash", "count-lines.sh", git_link])
    lines = subprocess.run(["bash", "count-lines.sh", git_link], stdout=subprocess.PIPE, text=True)

    if (lines.stderr):
        return {"git_link": git_link, "error": lines.stderr}, 400
    else: 
        return {"git_link": git_link, "lines": lines.stdout.strip()}, 200
    
# if __name__ == "__main__":
#     # This is used when running locally only. When deploying to Google App
#     # Engine, a webserver process such as Gunicorn will serve the app. This
#     # can be configured by adding an `entrypoint` to app.yaml.
#     # Flask's development server will automatically serve static files in
#     # the "static" directory. See:
#     # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
#     # App Engine itself will serve those files as configured in app.yaml.
#     app.run(host="127.0.0.1", port=8080, debug=True)

