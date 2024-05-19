# Mysterio Game

Mysterio is a Flask-based web application where players guess a hidden word by revealing parts of an image. The game features a scoring system, input history, and a leaderboard.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Logic](#game-logic)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- Reveal parts of an image to guess the hidden word
- Keep track of input history
- Scoring system based on the accuracy of guesses
- Leaderboard to display personal top scores

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ashwath-muppa/Mysterio
    cd mysterio-game
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    python3 app.py
    ```

## Usage

- Open a web browser and go to `http://127.0.0.1:5000/`
- Read instructions and play as accorded!

## Game Logic

- The game picks a random word from a predefined list.
- An image corresponding to the word is processed to hide parts of it.
- Players guess the word by submitting their inputs.
- The similarity between the guessed word and the target word is calculated using the Universal Sentence Encoder.
- Scores are adjusted based on the accuracy of the guesses.

## File Structure

 - Images and CSS files are located in the static folder
 - html files are located in templates
 - app.py and requirements are located in Mysterio