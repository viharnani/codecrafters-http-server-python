import socket

def main():
    # You can use print statements as follows for debugging; they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    # Create a server socket and listen on localhost at port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    # Accept a connection from a client (this will block until a client connects)
    client, addr = server_socket.accept()
    
    # Read data from the client (you can ignore it for now)
    client.recv(1024)
    
    # Send an HTTP/1.1 200 OK response to the client
    response = b"HTTP/1.1 200 OK\r\n\r\n"
    client.sendall(response)

if __name__ == "__main__":
    main()
