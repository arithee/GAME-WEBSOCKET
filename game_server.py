import socket
import random

host = "localhost"
port = 7777
banner = """
== Guessing Game Drill - IT6 (Atienza) ==
Select the difficulty level:
a. Easy (1-50)
b. Medium (1-100)
c. Hard (1-500)
"""

leaderboard = {}

def generate_random_int(low, high):
    return random.randint(low, high)

#Difficulty Range
def get_difficulty_range(difficulty):
    if difficulty == "a":
        return 1, 50
    elif difficulty == "b":
        return 1, 100
    elif difficulty == "c":
        return 1, 500
    else:
        return None

def update_leaderboard(name, score):
    if name in leaderboard:
        leaderboard[name] = min(leaderboard[name], score)
    else:
        leaderboard[name] = score

def save_leaderboard():
    with open("leaderboard.txt", "w") as file:
        for name, score in leaderboard.items():
            file.write(f"{name}: {score}\n")

def load_leaderboard():
    try:
        with open("leaderboard.txt", "r") as file:
            for line in file:
                name, score = line.strip().split(": ")
                leaderboard[name] = int(score)
    except FileNotFoundError:
        print("Leaderboard file cannot be found. Creating a new one.")

def display_leaderboard():
    print("\n== Guessing Game Leaderboard ==")
    for name, score in sorted(leaderboard.items(), key=lambda x: x[1]):
        print(f"{name}: {score} guesses ")

load_leaderboard()

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening in port {port}")

while True:
    conn, addr = s.accept()
    print(f"New Client: {addr[0]}")
    conn.sendall(banner.encode())

    # Get difficulty choice from the client
    difficulty_choice = conn.recv(1024).decode().strip().lower()
    difficulty_range = get_difficulty_range(difficulty_choice)

    if difficulty_range is None:
        conn.sendall(b"Invalid difficulty choice. Please select again.")
        conn.close()
        continue

    # Generate random number within the chosen difficulty range
    guessme = generate_random_int(*difficulty_range)
    tries = 0

    conn.sendall(b"")
    name = conn.recv(1024).decode().strip()

    while True:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        tries += 1
        print(f"User [{name}] guess attempt {tries}: {guess}")

        if guess == guessme:
            update_leaderboard(name, tries)
            conn.sendall(b"Correct Answer!")
            play_again = conn.recv(1024).decode().strip().lower()
            if play_again != "yes":   # 1st Feature (Client can play again without reconnecting or restarting the program)
                save_leaderboard()
                conn.close()
                display_leaderboard()
                break
            else:
                conn.sendall(banner.encode())
                difficulty_choice = conn.recv(1024).decode().strip().lower()
                difficulty_range = get_difficulty_range(difficulty_choice)
                if difficulty_range is None:
                    conn.sendall(b"Invalid difficulty choice. Please select again.")
                    conn.close()
                    break
                guessme = generate_random_int(*difficulty_range)
                tries = 0

        elif guess > guessme:
            conn.sendall(b"Guess Lower!")
        elif guess < guessme:
            conn.sendall(b"Guess Higher!")
