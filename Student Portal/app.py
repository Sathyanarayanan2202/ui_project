from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
FILE_PATH = 'data.xlsx'

# Create Excel file automatically if not exists
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=['RegNo', 'UserType', 'Name', 'Email', 'Phone', 'Address', 'DOB'])
    df.to_excel(FILE_PATH, index=False, engine='openpyxl')

# Function to generate automatic RegNo
def generate_regno():
    df = pd.read_excel(FILE_PATH, engine='openpyxl')
    if df.empty:
        return "R001"
    last_reg = df['RegNo'].iloc[-1]
    num = int(last_reg[1:]) + 1
    return f"R{num:03d}"

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usertype = request.form['usertype']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        dob = request.form['dob']

        regno = generate_regno()

        new_entry = pd.DataFrame([[regno, usertype, name, email, phone, address, dob]],
                                 columns=['RegNo', 'UserType', 'Name', 'Email', 'Phone', 'Address', 'DOB'])

        df = pd.read_excel(FILE_PATH, engine='openpyxl')
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(FILE_PATH, index=False, engine='openpyxl')

        return render_template('success.html', regno=regno, name=name, usertype=usertype)

    return render_template('register.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/get_users/<usertype>')
def get_users(usertype):
    df = pd.read_excel(FILE_PATH, engine='openpyxl')
    filtered = df[df['UserType'].str.lower() == usertype.lower()]
    users = filtered[['Name', 'RegNo']].to_dict(orient='records')
    return jsonify(users)

@app.route('/get_user_details/<regno>')
def get_user_details(regno):
    df = pd.read_excel(FILE_PATH, engine='openpyxl')
    user = df[df['RegNo'] == regno]
    if user.empty:
        return jsonify({})
    return jsonify(user.iloc[0].to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
