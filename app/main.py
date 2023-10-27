import socket
import threading
import argparse
import os

def handle_client(client, root_directory):
    # Read data from the client (the HTTP request)
    request = client.recv(1024).decode("utf-8")  # Decode the bytes to a string
    
    # Extract the path from the HTTP request
    path = get_path_from_request(request)
    
    # Determine the response based on the path
    response = b""  # Initialize response as bytes
    if path == "/":
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
    elif path == "/user-agent":
        user_agent = get_user_agent_from_request(request)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode("utf-8")
    elif path.startswith("/echo/"):
        random_string = path[6:]  # Extract the random string from the path
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}".encode("utf-8")
    elif path.startswith("/files/"):
        file_path = os.path.join(root_directory, path[7:])
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_contents = file.read()
            content_length = len(file_contents)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {content_length}\r\n\r\n".encode("utf-8") + file_contents
        else:
            # Respond with 404 Not Found if the file doesn't exist
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    
    # Send the response to the client
    client.sendall(response)
    
    # Close the connection
    client.close()

# Rest of the code remains the same

if __name__ == "__main__":
    main()
