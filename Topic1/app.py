from flask import Flask,request,redirect,render_template,url_for

app = Flask(__name__)

USER_DATA_FILE = 'users.txt'

def load_users():  
    users = {}
    try:
        with open(USER_DATA_FILE,'r') as f:
            for line in f:
                username,password = line.strip().split(',')
                users[username] = password
    except FileNotFoundError:
        pass
    return users

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            return redirect('/success')
        else :
            return 'Failed'
    return render_template('login.html')

@app.route('/success')
def success():
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)