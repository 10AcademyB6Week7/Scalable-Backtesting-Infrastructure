from inspect import Parameter
from flask import *
import os

app = Flask(__name__)

@app.route('/get_backtest_scene', methods=['POST'])
def get_backtest_scene():
    if request.method == 'POST':
        start_data = request.form.get("start_data")
        end_data = request.form.get("end_data")
        indicator = request.form.get("indicator")
        parameter_range = request.form.get("headline")
        return jsonify({"status": "success","file_path":'backtest running'})
    else:
            return{
                "status": "error",
                "message": f"{request.method} is not allowed"
            }


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', debug=True, port=port)