import socket

host = "localhost"
port = 7777

def game():
    while True:
        s = socket.socket()
        s.connect((host, port))

        try:
            # received the banner
            data = s.recv(1024)
            # print banner
            print(data.decode().strip())

            while True:
                # Get user input
                user_input = input("").strip()

                s.sendall(user_input.encode())
                reply = s.recv(1024).decode().strip()
                print(reply)
                # Repeats the game without disconnecting the client.
                if "Correct" in reply:
                    play_again = input("").strip().lower()
                    s.sendall(play_again.encode())
                    if play_again != "Y":
                        s.close()
                        return
                    else:
                        break  # Break out of the inner loop if the guess is correct
                elif "Goodbye" in reply:
                    s.close()
                    return

        except ConnectionResetError:
            print("The server closed the connection unexpectedly.")
            s.close()
            return

if __name__ == "__main__":
    game()
