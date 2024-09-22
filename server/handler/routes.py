from flask import Blueprint, send_from_directory, render_template, request, jsonify
import os

from ..model.form import Form

main = Blueprint('main',__name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir,'static'),"index.html")    

@main.route('/api/order',methods=['POST'])
def submit_files():
    if request.is_json:
        data = request.get_json()

        form = Form(**data)

        return jsonify({
            "orderid":"blah"
        }), 200
    else:
        return jsonify({
            "error":"parsing json"
        }), 400