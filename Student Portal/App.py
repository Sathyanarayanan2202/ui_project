from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
FILE_PATH = 'data.txt'

# Create text file if it doesn't exist
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w') as f:
        f.write("RegNo,UserType,Name,Email,Phone,Address,DOB\n")

# Function to read data from text file into a list of dicts
def read_data():
    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()[1:]  # skip header
    data = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 7:
            data.append({
                'RegNo': parts[0],
                'UserType': parts[1],
                'Name': parts[2],
                'Email': parts[3],
                'Phone': parts[4],
                'Address': parts[5],
                'DOB': parts[6]
            })
    return data

# Function to write a new record to the text file
def write_data(entry):
    with open(FILE_PATH, 'a') as f:
        f.write(','.join(entry) + '\n')

# Function to auto-generate registration numbers
def generate_regno():
    data = read_data()
    if not data:
        return "R001"
    last_reg = data[-1]['RegNo']
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

        # Save data into text file
        write_data([regno, usertype, name, email, phone, address, dob])

        return render_template('success.html', regno=regno, name=name, usertype=usertype)

    return render_template('register.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/get_users/<usertype>')
def get_users(usertype):
    data = read_data()
    filtered = [u for u in data if u['UserType'].lower() == usertype.lower()]
    users = [{'Name': u['Name'], 'RegNo': u['RegNo']} for u in filtered]
    return jsonify(users)

@app.route('/get_user_details/<regno>')
def get_user_details(regno):
    data = read_data()
    for user in data:
        if user['RegNo'] == regno:
            return jsonify(user)
    return jsonify({})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
