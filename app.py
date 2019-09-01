# import the Flask class from the flask module
from flask import Flask, request, render_template
from flask import Flask, render_template

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/test')
def my_form():
    return render_template('my-form.html')

@app.route('/test', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
