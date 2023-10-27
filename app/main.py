import socket
import threading

def handle_client(client):
    # Read data from the client (the HTTP request)
    request = client.recv(1024).decode("utf-8")  # Decode the bytes to a string
    
    # Extract the path from the HTTP request
    path = get_path_from_request(request)
    
    # Determine the response based on the path
    response = ""
    if path == "/":
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
    elif path == "/user-agent":
        user_agent = get_user_agent_from_request(request)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
    elif path.startswith("/echo/"):
        random_string = path[6:]  # Extract the random string from the path
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}".format(len(random_string), random_string)
    else:
        # Respond with 404 Not Found for paths that do not match "/echo/" or "/user-agent"
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    
    # Send the response to the client
    client.sendall(response.encode("utf-8"))  # Encode the string to bytes
    
    # Close the connection
    client.close()

def main():
    # Create a server socket and listen on localhost at port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:  # Add an infinite loop to keep the server running
        # Accept a connection from a client
        client, addr = server_socket.accept()
        
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

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

def get_user_agent_from_request(request):
    # Split the request into lines and find the User-Agent header
    lines = request.split("\r\n")
    for line in lines:
        if line.startswith("User-Agent:"):
            return line.split("User-Agent:")[1].strip()
    
    # If the User-Agent header is not found, return a default value
    return "Unknown User Agent"

if __name__ == "__main__":
    main()
