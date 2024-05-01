import socket
import random 

host = "localhost"
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your guess:"""

def generate_random_int(low, high):
    return random.randint(low, high)

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")
guessme = 0
conn = None
while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        guessme = generate_random_int(1,100)
        print(f"new client: {addr[0]}")
        # cheat_str = f"==== number to guess is {guessme} \n" + banner 
        # conn.sendall(cheat_str.encode())
        conn.sendall(banner.encode())
    else:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b"Correct Answer!")
            conn.close()
            conn = None
            continue
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nEnter guess: ")
            continue
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nEnter guess:")
            continue



