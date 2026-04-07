# app.py - Flask Backend for Rock Paper Scissors Game
# This file handles the game logic on the server side.

from flask import Flask, render_template, request, jsonify
import random  # Used to randomly pick the computer's choice

# Initialize the Flask application
app = Flask(__name__)

# The three possible choices in the game
CHOICES = ["rock", "paper", "scissors"]

# Game rules: each choice beats one other choice
# Key beats Value (e.g., rock beats scissors)
WINS_AGAINST = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock"
}

@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():
    """
    Game endpoint.
    - Receives the user's choice via POST request (JSON)
    - Randomly selects the computer's choice
    - Determines the winner
    - Returns the result as JSON
    """
    # Get JSON data from the request body
    data = request.get_json()

    # Extract the user's choice (e.g., "rock", "paper", or "scissors")
    user_choice = data.get("choice", "").lower()

    # Validate: make sure the user sent a valid choice
    if user_choice not in CHOICES:
        return jsonify({"error": "Invalid choice. Must be rock, paper, or scissors."}), 400

    # Randomly pick the computer's choice from the list
    computer_choice = random.choice(CHOICES)

    # Determine the result
    if user_choice == computer_choice:
        result = "tie"   # Both chose the same thing
    elif WINS_AGAINST[user_choice] == computer_choice:
        result = "win"   # User's choice beats computer's choice
    else:
        result = "lose"  # Computer's choice beats user's choice

    # Return the result as a JSON response
    return jsonify({
        "user": user_choice,
        "computer": computer_choice,
        "result": result
    })


# Run the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
