import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import subprocess
import sys
import getpass
import time

# Path to your Firebase service account key
SERVICE_ACCOUNT_PATH = 'serviceAccountKey.json'

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

# Connect to Firestore database
db = firestore.client()

# Auto update and upgrade system (Termux)
def auto_update_upgrade():
    print("Starting auto-update and upgrade...")
    os.system('pkg update -y && pkg upgrade -y')
    print("System update and upgrade completed.")

# Function to register a new user
def register_user():
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")

    try:
        user = auth.create_user(email=email, password=password)
        print(f"User {email} successfully registered!")
        return user.uid
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Function to login an existing user
def login_user():
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")

    try:
        # Authenticate user using Firebase Auth REST API
        user = auth.get_user_by_email(email)
        print(f"Login successful! Welcome, {email}.")
        return user.uid
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

# Send a message from one user to another
def send_message(sender_uid, receiver_email, message):
    try:
        receiver = auth.get_user_by_email(receiver_email)
        message_data = {
            'sender': sender_uid,
            'receiver': receiver.uid,
            'message': message,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        db.collection('messages').add(message_data)
        print(f"Message sent to {receiver_email}: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Get messages for the logged-in user
def get_messages(user_uid):
    messages = db.collection('messages').where('receiver', '==', user_uid).stream()

    print("Your messages:")
    for msg in messages:
        msg_data = msg.to_dict()
        sender = auth.get_user(msg_data['sender'])
        print(f"From {sender.email}: {msg_data['message']}")

# Main CLI Menu
def chat_cli():
    print("Welcome to Firebase CLI Chat")
    auto_update_upgrade()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Choose an option: ")

        if choice == '1':
            user_uid = register_user()
        elif choice == '2':
            user_uid = login_user()
            if user_uid:
                while True:
                    print("\n1. Send Message")
                    print("2. View Messages")
                    print("3. Logout")
                    chat_choice = input("Choose an option: ")

                    if chat_choice == '1':
                        receiver_email = input("Enter receiver's email: ")
                        message = input("Enter your message: ")
                        send_message(user_uid, receiver_email, message)
                    elif chat_choice == '2':
                        get_messages(user_uid)
                    elif chat_choice == '3':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice, try again.")
        elif choice == '3':
            sys.exit()
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    chat_cli()
