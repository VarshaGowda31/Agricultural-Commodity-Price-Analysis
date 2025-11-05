from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import csv
import os

app = Flask(__name__)
app.secret_key = 'cropcast_secret_key'

df = pd.read_csv('dataset/096f32cf-2033-464c-a90d-73f338493971.csv')

# Create users.csv if not exists
if not os.path.exists('users.csv'):
    with open('users.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username', 'password'])

@app.route('/')
def home():
    if 'username' in session:
        states = df['State'].unique()
        commodities = df['Commodity'].unique()
        return render_template('index.html', states=states, commodities=commodities, username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    session['username'] = username
                    return redirect(url_for('home'))
        return "Invalid credentials. <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        with open('users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    return "User already exists. <a href='/signup'>Try again</a>"

        with open('users.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password])
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' in session:
        state = request.form['state']
        commodity = request.form['commodity']
        avg_price = df[(df['State'] == state) & (df['Commodity'] == commodity)]['Modal_x0020_Price'].mean()
        return render_template('prediction.html', state=state, commodity=commodity, price=avg_price)
    else:
        return redirect(url_for('login'))

@app.route('/dataset-info')
def dataset_info():
    if 'username' in session:
        columns = df.columns.tolist()
        row_count = df.shape[0]
        return render_template('dataset_info.html', columns=columns, row_count=row_count)
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
