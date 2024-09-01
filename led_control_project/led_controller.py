from flask import Flask, render_template, request, jsonify
import board
import neopixel
import json
import os
import time

app = Flask(__name__, template_folder='/home/jkenagy/led_control_project/Database')

# Configuration
LED_PIN = board.D18
NUM_LEDS = 1500  # Total number of LEDs
ORDER = neopixel.RGB

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
    with open(f'/home/jkenagy/led_control_project/Database/{config_name}.json', 'w') as f:
        json.dump(led_state, f)
    return jsonify({'success': True})

@app.route('/load_configuration', methods=['GET'])
def load_configuration():
    config_name = request.args.get('name')
    with open(f'/home/jkenagy/led_control_project/Database/{config_name}.json', 'r') as f:
        saved_state = json.load(f)
    for i in range(NUM_LEDS):
        pixels[i] = tuple(saved_state[i])
    pixels.show()
    return jsonify({'success': True})

@app.route('/list_configurations', methods=['GET'])
def list_configurations():
    files = [f for f in os.listdir('/home/jkenagy/led_control_project/Database') if f.endswith('.json')]
    return jsonify(files)

@app.route('/test_mode/<mode>', methods=['GET'])
def test_mode(mode):
    if mode == 'red':
        pixels.fill((255, 0, 0))
    elif mode == 'green':
        pixels.fill((0, 255, 0))
    elif mode == 'blue':
        pixels.fill((0, 0, 255))
    elif mode == 'white':
        pixels.fill((255, 255, 255))
    elif mode == 'off':
        pixels.fill((0, 0, 0))
    elif mode == 'brightness_low':
        pixels.brightness = 0.1
        pixels.fill((255, 255, 255))
    elif mode == 'brightness_medium':
        pixels.brightness = 0.5
        pixels.fill((255, 255, 255))
    elif mode == 'brightness_high':
        pixels.brightness = 1.0
        pixels.fill((255, 255, 255))
    elif mode == 'snake':
        snake_animation()
    else:
        return jsonify({'error': 'Invalid test mode'}), 400

    pixels.show()
    return jsonify({'success': True})

def snake_animation():
    # Forward snake movement
    for i in range(NUM_LEDS):
        
        pixels[(i*24132)%NUM_LEDS]=(255,255,255)
        time.sleep(0.005)  # Adjust speed as necessary

    # Reverse snake movement
    for i in range(NUM_LEDS - 1, -1, -1):
        pixels.fill((0, 0, 0))  # Turn off all LEDs
        pixels[i] = (0, 255, 0)  # Turn on the current LED (green)
        pixels.show()
        time.sleep(0.00005)  # Adjust speed as necessary

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
