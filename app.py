from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from autosuggest import *

app = Flask(__name__)
bootstrap = Bootstrap(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autosuggest', methods=['POST'])
def autosuggest():
    user_input = request.form['user_input']
    towns = load_data("towns/towns.csv")
    
    matches = find_matching_towns(user_input, towns)
    # print(matches)
    return render_template('autosuggest.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
