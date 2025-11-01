<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Users</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    <script>
        async function fetchUsers(usertype) {
            document.getElementById("userList").innerHTML = "<p>Loading...</p>";
            
            const response = await fetch(`/get_users/${usertype}`);
            const users = await response.json();

            if (users.length === 0) {
                document.getElementById("userList").innerHTML = "<p>No users found.</p>";
                return;
            }

            let html = `<h4 class='mt-3'>${usertype.charAt(0).toUpperCase() + usertype.slice(1)} List</h4>`;
            html += "<ul class='list-group'>";
            users.forEach(u => {
                html += `<li class='list-group-item d-flex justify-content-between align-items-center'>
                            ${u.Name} (${u.RegNo})
                            <button class='btn btn-sm btn-info' onclick="fetchDetails('${u.RegNo}')">View</button>
                         </li>`;
            });
            html += "</ul>";
            document.getElementById("userList").innerHTML = html;
        }

        async function fetchDetails(regno) {
            const response = await fetch(`/get_user_details/${regno}`);
            const user = await response.json();

            if (Object.keys(user).length === 0) {
                document.getElementById("details").innerHTML = "<p>No details found.</p>";
                return;
            }

            let html = `<h5 class='mt-3'>User Details</h5>
                        <table class='table table-bordered mt-2'>
                            <tr><th>RegNo</th><td>${user.RegNo}</td></tr>
                            <tr><th>User Type</th><td>${user.UserType}</td></tr>
                            <tr><th>Name</th><td>${user.Name}</td></tr>
                            <tr><th>Email</th><td>${user.Email}</td></tr>
                            <tr><th>Phone</th><td>${user.Phone}</td></tr>
                            <tr><th>Address</th><td>${user.Address}</td></tr>
                            <tr><th>DOB</th><td>${user.DOB}</td></tr>
                        </table>`;
            document.getElementById("details").innerHTML = html;
        }
    </script>
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h2 class="text-center mb-4">Search Registered Users</h2>

        <div class="text-center">
            <button class="btn btn-primary me-3" onclick="fetchUsers('teacher')">Show Teachers</button>
rom flask import Flask, render_template, request, jsonify
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
