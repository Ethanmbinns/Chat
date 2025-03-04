from flask import Flask

# Import routes
from account.new.new import account_new_bp

# Initialize Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(account_new_bp, url_prefix='/account')

# Basic route for testing
@app.route('/', methods=['GET'])
def index():
    return "UUID Account Generator API is running"

if __name__ == '__main__':
    app.run(debug=True)
