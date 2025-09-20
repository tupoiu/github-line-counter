from datetime import datetime
import os
import shutil
import sys
from flask import Flask, render_template, request
import subprocess
from pathlib import Path

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/loc")
def loc():
    git_link = request.args.get('git_link')
    # git_link = "https://github.com/huertatipografica/HTLetterspacer.git"
    return count_lines(git_link)
    
def count_lines(git_link: str):
    if not git_link:
        return "", 400

    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    os.makedirs(current_time)

    # Git clone into the new dir
    subprocess.run(["git", "clone", git_link, current_time], check=True)

    # Get all files in the directory
    directory = Path(current_time)
    files = [p for p in directory.rglob("*") if p.is_file()]
    print(files[:10])

    total_lines_per_extension = {}

    for file in files:
        extension = file.suffix
        if extension not in total_lines_per_extension:
            total_lines_per_extension[extension] = 0

        with open(file, "r") as f:
            try:
                lines = sum(1 for _line in f)
                total_lines_per_extension[extension] += lines
            except Exception as e:
                print(e)
                pass
    total_lines_per_extension[".*"] = sum(v for v in total_lines_per_extension.values())
    shutil.rmtree(current_time, ignore_errors=True)

    return {"git_link": git_link, "lines": total_lines_per_extension}, 200

    # Count the lines and put the result in a variable
    # lines = subprocess.run(["bash", "count-lines.sh", git_link], stdout=subprocess.PIPE, text=True)

    if (lines.stderr):
        return {"git_link": git_link, "error": lines.stderr}, 400
    else: 
        return {"git_link": git_link, "lines": lines.stdout.strip()}, 200
    
if __name__ == "__main__":
    git_link = sys.argv[1]
    lines = count_lines(git_link)

    print(lines)