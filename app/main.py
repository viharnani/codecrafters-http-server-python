import socket

def main():
    # Create a server socket and listen on localhost at port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:  # Add an infinite loop to keep the server running
        # Accept a connection from a client
        client, addr = server_socket.accept()
        
        # Read data from the client (the HTTP request)
        request = client.recv(1024).decode("utf-8")  # Decode the bytes to a string
        
        # Extract the path from the HTTP request
        path = get_path_from_request(request)
        
        # Determine the response based on the path
        response = ""
        if path.startswith("/echo/"):
            random_string = path[6:]  # Extract the random string from the path
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}".format(len(random_string), random_string)
        else:
            # Respond with 200 OK for the root path ("/")
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
        
        # Send the response to the client
        client.sendall(response.encode("utf-8"))  # Encode the string to bytes
        
        # Close the connection
        client.close()

def get_path_from_request(request):
    # Split the request into lines and extract the path from the first line
    lines = request.split("\r\n")
    if lines:
        # The first line should look like "GET /echo/abc HTTP/1.1"
        parts = lines[0].split(" ")
        if len(parts) > 1:
            return parts[1]
    
    # If the path cannot be extracted, return a default value
    return "/"

if __name__ == "__main__":
    main()
