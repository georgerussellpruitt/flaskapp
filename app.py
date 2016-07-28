from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    
	return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
	return render_template('signup.html')

@app.route("/signUp")
def signUp():
    

if __name__ == "__main__":
		app.run(host='0.0.0.0')