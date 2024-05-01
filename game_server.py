import socket
import random

host = "localhost"
port = 7777
banner = """
== Guessing Game Drill - IT6 ==
Select the difficulty level:
a. Easy (1 - 50)
b. Medium (1 - 100)
c. Hard (1 - 500)
Enter your guess:"""

def generate_random_int(low, high):
    return random.randint(low, high)

def get_difficulty_range(difficulty):
    if difficulty == "a":
        return 1, 50
    elif difficulty == "b":
        return 1, 100
    elif difficulty == "c":
        return 1, 500
    else:
        return None

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")

while True:
    conn, addr = s.accept()
    guessme = generate_random_int(1,100)
    print(f"new client: {addr[0]}")
    conn.sendall(banner.encode())

    while True:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b"Correct Answer! Would you like to play again? (Y/N): ")
            play_again = conn.recv(1024).decode().strip().lower()
            if play_again != "Y":
                conn.sendall(b"Goodbye!")
                conn.close()
                break
            else:
                guessme = generate_random_int(1,100)
                conn.sendall(banner.encode())
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nEnter your guess: ")
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nEnter your guess:")
