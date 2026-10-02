#include "Server.hpp"

namespace netlab {
    int Server::createServer() {
        #if defined(_WIN32) || defined(_WIN64)

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

        std::cout << "Server listening at the port " << address.sin_port << std::endl;

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
            std::cout << "Message received: " << buffer << std::endl;
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