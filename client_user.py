import secrets
from flask import Flask, jsonify, request, redirect, url_for

app = Flask(__name__)

# ... (Existing code for ops_users, client_users, uploaded_files, and authentication function)


# Generate random token for email verification
def generate_verification_token():
    return secrets.token_urlsafe(16)


# Endpoint for Client User signup
@app.route("/signup", methods=["POST"])
def signup():
    auth = request.authorization
    if (
        not auth
        or not auth.username
        or not auth.password
        or not request.json.get("email")
    ):
        return jsonify({"message": "Username, password, and email required!"}), 400

    # Check if the username is already taken
    for user in client_users:
        if user["username"] == auth.username:
            return jsonify({"message": "Username already exists!"}), 409

    # Generate a verification token (for demonstration purposes, not actual email sending)
    verification_token = generate_verification_token()

    # Save user details and verification token in the database (in a real system, this data would be stored securely)
    client_users.append(
        {
            "username": auth.username,
            "password": auth.password,
            "email": request.json["email"],
            "verification_token": verification_token,
            "verified": False,
        }
    )

    # Return an encrypted URL (verification token as an example)
    return jsonify({"verification_url": f"/verify-email/{verification_token}"}), 201


# Endpoint for email verification
@app.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    # Find the user by verification token (in a real system, this would validate against the database)
    for user in client_users:
        if user["verification_token"] == token:
            user["verified"] = True
            return jsonify({"message": "Email verified successfully!"})
    return jsonify({"message": "Invalid verification token!"}), 404


# Endpoint for Client User login
@app.route("/client-login", methods=["POST"])
def client_login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Username and password required!"}), 400

    user_type = authenticate(auth.username, auth.password)
    if user_type != "client":
        return jsonify({"message": "Invalid credentials!"}), 401

    return jsonify({"message": "Client User logged in successfully!"})


# Endpoint to list uploaded files for Client User
@app.route("/list-uploaded-files", methods=["GET"])
def list_uploaded_files():
    # Retrieve files uploaded by Client Users
    client_uploaded_files = [
        file
        for file in uploaded_files
        if file["uploaded_by"] in [user["username"] for user in client_users]
    ]
    return jsonify({"uploaded_files": client_uploaded_files})


# ... (Existing code for file upload and ops user login)

if __name__ == "__main__":
    app.run(debug=True)
