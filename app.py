from flask import Flask, request, jsonify
import subprocess
import RPi.GPIO as GPIO

app = Flask(__name__)

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

@app.route('/run_taser', methods=['POST'])
def run_taser():
    data = request.get_json()
    number = data.get('number')
    print(f"Received number: {number}")

    try:
        if number == 10 or number == 1:
            # Win action: trigger GPIO pin 20
            print("Triggering GPIO pin 20 for win")
            GPIO.output(20, GPIO.HIGH)
            subprocess.run(["echo", "You win!"], check=True)
            return jsonify({"status": "success", "message": "You win!"}), 200
        else:
            # Loss action: trigger GPIO pin 16
            print("Triggering GPIO pin 16 for loss")
            GPIO.output(16, GPIO.HIGH)
            subprocess.run(["echo", "Taser activated!"], check=True)
            return jsonify({"status": "success", "message": "Taser activated!"}), 200
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset_pins', methods=['POST'])
def reset_pins():
    # Reset GPIO pins
    print("Resetting GPIO pins")
    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    return jsonify({"status": "success", "message": "Pins reset!"}), 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()