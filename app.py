from flask import *

app = Flask(__name__)

@app.route('/templates')
def bonjour():
    return render_template("page_d'accueil.html")

@app.route('/templates')
def interface():
    return render_template("/index.html")


if __name__ == '__main__':
    app.run(debug=True)