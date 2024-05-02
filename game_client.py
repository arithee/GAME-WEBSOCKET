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
        difficulty_choice = input("\nEnter your choice (A/B/C): ").strip().upper()
        s.sendall(difficulty_choice.encode())

        # name from user {sends to server so txt file updates}
        name = input("Enter your name: ").strip()
        s.sendall(name.encode())

        while True:
            # get user input
            user_input = input("Enter your guess: ").strip()

            s.sendall(user_input.encode())
            reply = s.recv(1024).decode().strip()
            print(reply)

            if "Correct" in reply:
                play_again = input("Do you want to play again? (Y/N): ").strip().upper()
                s.sendall(play_again.encode())
                if play_again != "Y":
                    s.close()
                    return
                else:
                    break
            elif "Goodbye" in reply:
                s.close()
                return

        s.close()

if __name__ == "__main__":
    game()
