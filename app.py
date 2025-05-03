from flask import Flask

# Create a Flask app instance
app = Flask(__name__)

# Define a simple route
@app.route('/')
def hello_world():
    return 'Hello, World! minimal app'

# Run the app with debug mode enabled
if __name__ == '__main__':
    app.run(debug=True)
