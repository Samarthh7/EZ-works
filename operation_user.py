from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample user data (for demonstration purposes, not for production)
ops_users = [{"username": "opsuser", "password": "ops_password"}]
client_users = [{"username": "clientuser", "password": "client_password"}]
uploaded_files = []


# Authentication using simple username/password (not recommended for production)
def authenticate(username, password):
    for user in ops_users:
        if user["username"] == username and user["password"] == password:
            return "ops"
    for user in client_users:
        if user["username"] == username and user["password"] == password:
            return "client"
    return None


# Endpoint for Ops User login
@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Authorization required!"}), 401

    user_type = authenticate(auth.username, auth.password)
    if user_type == "ops":
        return jsonify({"message": "Ops User logged in successfully!"})
    elif user_type == "client":
        return jsonify({"message": "Client User logged in successfully!"})
    else:
        return jsonify({"message": "Invalid credentials!"}), 401


# Endpoint for Ops User to upload files
@app.route("/upload-file", methods=["POST"])
def upload_file():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Authorization required!"}), 401

    user_type = authenticate(auth.username, auth.password)
    if user_type != "ops":
        return (
            jsonify({"message": "Unauthorized! Only Ops Users can upload files."}),
            403,
        )

    uploaded_file = request.files["file"]
    if uploaded_file.filename.split(".")[-1] not in ["pptx", "docx", "xlsx"]:
        return (
            jsonify({"message": "Invalid file format! Only pptx, docx, xlsx allowed."}),
            400,
        )

    # Save the file securely

    uploaded_files.append(
        {"file_name": uploaded_file.filename, "uploaded_by": auth.username}
    )
    return jsonify({"message": "File uploaded successfully!"})


if __name__ == "__main__":
    app.run(debug=True)
