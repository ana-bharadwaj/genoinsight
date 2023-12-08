from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

#Dummy user data (replace with a database in a real application)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

#Function to check user credentials
def check_credentials(username, password):
    return username in users and users[username] == password

#Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    return render_template('login.html')

#Dashboard route (protected)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome, {session['username']}! This is your dashboard."
    return redirect(url_for('login'))

#Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == 'main':
    app.run(debug=True)