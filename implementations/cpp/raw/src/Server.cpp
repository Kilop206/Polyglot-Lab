#include "Server.hpp"

#include "Decoder.hpp"
#include "Encoder.hpp"

namespace netlab {
    int Server::createServer() {

        Decoder decoder;
        Encoder encode;

        #if defined(_WIN32) || defined(_WIN64)

        // Initialize Winsock
        WSADATA wsaData;
        int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
        if (result != 0) {
            std::cerr << "Error at initializing the Winsock: " << result << std::endl;
            return 1;
        }

        struct addrinfo* hints = NULL;
        struct addrinfo* ptr = NULL;
        struct addrinfo zeroHints;

        ZeroMemory(&zeroHints, sizeof(zeroHints));
        zeroHints.ai_family = AF_INET;       // IPv4
        zeroHints.ai_socktype = SOCK_STREAM; // TCP
        zeroHints.ai_protocol = IPPROTO_TCP;
        zeroHints.ai_flags = AI_PASSIVE;     // Bind to local IP

        // Resolve the address and the port
        result = getaddrinfo(NULL, "7000", &zeroHints, &hints);
        if (result != 0) {
            std::cerr << "getaddrinfo failed: " << result << std::endl;
            WSACleanup();
            return 1;
        }

        // Create the listening socket
        SOCKET listenSocket = INVALID_SOCKET;
        listenSocket = socket(hints->ai_family, hints->ai_socktype, hints->ai_protocol);
        if (listenSocket == INVALID_SOCKET) {
            std::cerr << "Error creating the socket: " << WSAGetLastError() << std::endl;
            freeaddrinfo(hints);
            WSACleanup();
            return 1;
        }

        // Bind the socket
        result = bind(listenSocket, hints->ai_addr, (int)hints->ai_addrlen);
        if (result == SOCKET_ERROR) {
            std::cerr << "Build error: " << WSAGetLastError() << std::endl;
            freeaddrinfo(hints);
            closesocket(listenSocket);
            WSACleanup();
            return 1;
        }

        freeaddrinfo(hints);

        // Listen by connections
        if (listen(listenSocket, SOMAXCONN) == SOCKET_ERROR) {
            std::cerr << "Error listening: " << WSAGetLastError() << std::endl;
            closesocket(listenSocket);
            WSACleanup();
            return 1;
        }

        std::cout << "Server running at the port 7000. Awating connection" << std::endl;

        // Accept a client connection
        SOCKET clientSocket = INVALID_SOCKET;
        clientSocket = accept(listenSocket, NULL, NULL);
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "Error accepting the client connection" << WSAGetLastError() << std::endl;
            closesocket(listenSocket);
            WSACleanup();
            return 1;
        }

        std::cout << "Client connected" << std::endl;
        closesocket(listenSocket);

        // Receive and send data
        char buffer[1024] = {0};
        int bytesReceived = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
        if  (bytesReceived > 0) {
            std::cout << "Message received from the client: " << decoder.decode(buffer) << std::endl;
            
            const char* response = "Hello!";
            send(clientSocket, response, strlen(response), 0);
        }

        // Cleaning and finishing
        closesocket(listenSocket);
        closesocket(clientSocket);
        WSACleanup();

        #else if defined(__linux__)

        // Creates the socket server
        int server_fd = socket(AF_INET, SOCK_STREAM, 0); 
        if (server_fd < 0) {
            std::cerr << "Error at creating socket" << std::endl;
            close(server_fd);
            return 1;
        }

        // Configures the address and the port
        sockaddr_in address{};
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY; // Accepts conections from any IP of the machine
        address.sin_port = htons(7000);       // Server's port (7000)

        // Bind socket to IP and Port
        if (bind(server_fd, (struct sockadddr*)&address, sizeof(address)) < 0) {
            std::cerr << "Error at binding the port" <<std::endl;
            close(server_fd);
            return 1
        }

        // Put server on listen mode
        if (listen(server_fd, 1) < 0) {
            std::cerr << "Error at listening" << std::endl;
            close(server_fd);
            return 1;
        }

        std::cout << "Server running at the port 7000. Awating connection" << std::endl;

        // Accept a client connection
        socklen_t addrlen = sizeof(address);
        int client_fd = accept(server_fd, (struct sockaddr*)&address, &addrlen);
        if (client_fd < 0) {
            std::cerr << "Error at accepting a client connection" << std::endl;
            close(server_fd);
            return 1;
        }

        std::cout << "Client connected!" << std::endl;

        // Read data sent by the client
        char buffer[1024] = {0};
        ssize_t bytes_read = read(client_fd, buffer, sizeof(buffer) - 1);
        if (bytes_read > 0) {
            std::cout << "Message received: " << decoder.decode(bytes_read) << std::endl;
        }

        // Answer the client
        const char* response = "Hello!";
        send(client_fd, response, strlen(response), 0);
        std::cout << "Answer sent to the client" << std::endl;

        // Close the sockets
        close(client_fd);
        close(sercer_fd);

        #endif
    }
}