from flask import Flask

# Import routes
from account.new.new import account_new_bp
from chat.new_message.new_message import chat_new_message_bp

# Initialize Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(account_new_bp, url_prefix='/account')
app.register_blueprint(chat_new_message_bp, url_prefix='/chat')

# Basic route for testing
@app.route('/', methods=['GET'])
def index():
    return "UUID Account Generator and Chat API is running"

if __name__ == '__main__':
    app.run(debug=True)