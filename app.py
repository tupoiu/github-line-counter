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
    lines = subprocess.run(["bash", "count-lines.sh", git_link], stdout=subprocess.PIPE, text=True)

    if (lines.stderr):
        return {"git_link": git_link, "error": lines.stderr}, 400
    else: 
        return {"git_link": git_link, "lines": lines.stdout.strip()}, 200
    
