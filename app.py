from flask import Flask, render_template, json, request, session, redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'shh its a secret!!!!?'

# MySQL configurations

#attempt at grabbing env vars
app.config['MYSQL_DATABASE_USER'] = os.environ['DB_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['DB_PASS']
app.config['MYSQL_DATABASE_DB'] = os.environ['DB_NAME']
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_HOST'] = os.environ['DB_HOST']
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/showSignin')
def showSignin():
	return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
	try:
		_username = request.form['inputEmail']
		_password = request.form['inputPassword']
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_validateLogin',(_username,))
		data = cursor.fetchall()
		
		if len(data) > 0:
			if check_password_hash(str(data[0][3]),_password):
				session['user'] = data[0][0]
				return redirect('/userHome')
			else:
				return render_template('error',error = 'Wrong Email address or Password.')
	
	except Exception as e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()
		conn.close()
		
@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)