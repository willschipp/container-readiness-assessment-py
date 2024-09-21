from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir,'static'),filename)



if __name__ == "__main__":
    app.run()