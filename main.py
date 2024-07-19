from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit


# Create Flask app and set secret key 
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Set your secret key
socketio = SocketIO(app)         # Create a SocketIO object

code_blocks = {                   #code blocks -"list of at least 4 items which represents code blocks"
    "PrintExample": {
        "title": "Print Example",
        "code": "function printData() {\n    console.log('Hello, World!');\n}"
    },
    "AdditionExample": {
        "title": "Addition Example",
        "code": "function addNumbers(a, b) {\n    return a + b;\n}\n\nconsole.log(addNumbers(2, 3));"
    },
    "SubtractionExample": {
        "title": "Subtraction Example",
        "code": "function subtractNumbers(a, b) {\n    return a - b;\n}\n\nconsole.log(subtractNumbers(5, 2));"
    },
    "MultiplicationExample": {
        "title": "Multiplication Example",
        "code": "function multiplyNumbers(a, b) {\n    return a * b;\n}\n\nconsole.log(multiplyNumbers(3, 4));"
    }
}

# Track the first user for each code block - "Both users should enter this page. (2 different clients)
Assume that the first user who opens the code block page is the mentor, after that, any other user will be counted as a student."

mentors = {}

#@app.route("/")              
#def index():s
#    return render_template("index.html")

@app.route("/")                  #The function home() is defined to handle requests to the root URL.
def home():                     
    return render_template('index.html')

@app.route('/code/<block_name>')       #The functionis defined to handle User choices requests 
def code_block(block_name):
    requested_block = code_blocks.get(block_name)

    if block_name not in mentors:          ## Determine the user role as mentor or student
        mentors[block_name] = session['user_id'] = request.remote_addr  # Assign mentor role to first user

    user_role = 'mentor' if session.get('user_id') == mentors[block_name] else 'student'

    print(f"Requested block: {block_name}")  # Not necessary but makes it easier to know what state the user is in 
    print(f"Client IP: {request.remote_addr}, Role: {user_role}")

    if requested_block:   #Handling Missing Code Block:
        return render_template('code_block.html', title=requested_block['title'], code=requested_block['code'], user_role=user_role)
    else:
        return "Code block not found", 404

@socketio.on('join_code_block')
def handle_join_code_block(block_name):
    if block_name not in mentors:
        mentors[block_name] = request.sid  # First user becomes the mentor
        emit('mentor_assigned', room=request.sid)
    print(f"User {request.sid} joined block {block_name}. Mentor: {mentors[block_name]}")

@socketio.on('update_code')
def handle_update_code(updated_code):
    print(f"Updating code: {updated_code}")  # Log the updated code
    emit('code_update', updated_code, broadcast=True)  # Send updated code to all clients

if __name__ == "__main__":        #check ensures that certain code is only executed when the script is run directly, not when it is imported.
    socketio.run(app, debug=True)
    app.run(port=5000)           # port for app 
