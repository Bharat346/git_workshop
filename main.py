from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math
import mplcursors as mc
 
app = Flask(__name__)

# Store cursor position globally for simplicity (in a real application, you might want to use session variables)
cursor_position = {'x': 0, 'y': 0}

def update_cursor_position(event):
    if event.xdata is not None and event.ydata is not None:
        cursor_position['x'] = event.xdata
        cursor_position['y'] = event.ydata

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    user_function = request.form['user_function']
    x_values = np.linspace(-10, 10, 1000)

    try:
        y_values = eval(user_function, {'np': np, 'x': x_values, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                                        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt, 'pi': math.pi})
    except SyntaxError as e:
        return jsonify({'error': 'SyntaxError: {}'.format(str(e))})
    except Exception as e:
        return jsonify({'error': 'Error evaluating the function: {}'.format(str(e))})

    plt.plot(x_values, y_values)
    plt.title('Curve Plot')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)

    img_data = BytesIO()
    
    try:
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
    except Exception as e:
        return jsonify({'error': 'Error saving the plot: {}'.format(str(e))})
    finally:
        plt.close()

    return jsonify({'img_base64': img_base64, 'user_function': user_function})

@app.route('/get_cursor_position')
def get_cursor_position():
    return jsonify(cursor_position)

if __name__ == '__main__':
    app.run(debug=True,port=3467)
