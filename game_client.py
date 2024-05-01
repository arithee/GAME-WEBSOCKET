import socket

host = "localhost"
port = 7777

def game():
    while True:
        s = socket.socket()
        s.connect((host, port))

        # received the banner
        data = s.recv(1024)
        # print banner
        print(data.decode().strip())

        # Get difficulty choice from the user
        difficulty_choice = input("Enter your choice (a/b/c): ").strip().lower()
        s.sendall(difficulty_choice.encode())

        while True:
            # Get user input
            user_input = input("Enter your guess:").strip()

            s.sendall(user_input.encode())
            reply = s.recv(1024).decode().strip()
            print(reply)

            if "Correct" in reply:
                play_again = input("Do you want to play again? (yes/no): ").strip().lower()
                s.sendall(play_again.encode())
                if play_again != "yes":
                    s.close()
                    return
                else:
                    break  # Break out of the inner loop if the guess is correct
            elif "Goodbye" in reply:
                s.close()
                return

        s.close()

if __name__ == "__main__":
    game()
