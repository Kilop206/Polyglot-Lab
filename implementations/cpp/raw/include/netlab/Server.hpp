#pragma once

#include <iostream>

#if defined(_WIN32) || defined(_WIN64)

#else if defined(__linux__)

#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#endif

namespace netlab {
    struct Server {
        int createServer();
    };
}