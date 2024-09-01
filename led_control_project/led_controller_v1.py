from flask import Flask, render_template, request, jsonify
import board
import neopixel
import json
import os

app = Flask(__name__, template_folder='Database')

# Configuration
LED_PIN = board.D18
NUM_LEDS = 2000  # Total number of LEDs
ORDER = neopixel.GRB

# Create NeoPixel object
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, auto_write=False, pixel_order=ORDER)

# Initialize LED state
led_state = [(0, 0, 0)] * NUM_LEDS

@app.route('/')
def index():
    return render_template('index.html', num_leds=NUM_LEDS)

@app.route('/set_led', methods=['POST'])
def set_led():
    data = request.get_json()
    led_index = data['index']
    color = data['color']

    if color == 'red':
        pixels[led_index] = (255, 0, 0)
    elif color == 'green':
        pixels[led_index] = (0, 255, 0)
    elif color == 'blue':
        pixels[led_index] = (0, 0, 255)
    else:
        pixels[led_index] = (0, 0, 0)

    led_state[led_index] = pixels[led_index]
    pixels.show()
    return jsonify({'success': True})

@app.route('/save_configuration', methods=['POST'])
def save_configuration():
    config_name = request.form['name']
    with open(f'Database/{config_name}.json', 'w') as f:
        json.dump(led_state, f)
    return jsonify({'success': True})

@app.route('/load_configuration', methods=['GET'])
def load_configuration():
    config_name = request.args.get('name')
    with open(f'Database/{config_name}.json', 'r') as f:
        saved_state = json.load(f)
    for i in range(NUM_LEDS):
        pixels[i] = tuple(saved_state[i])
    pixels.show()
    return jsonify({'success': True})

@app.route('/list_configurations', methods=['GET'])
def list_configurations():
    files = [f for f in os.listdir('Database') if f.endswith('.json')]
    return jsonify(files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
