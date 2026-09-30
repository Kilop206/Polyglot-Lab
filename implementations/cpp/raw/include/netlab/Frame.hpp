#pragma once

#include <cstdint>
#include <vector>

namespace netlab {
    enum class MessageType : std::uint8_t {
        Hello      = 0x01,
        HelloAck   = 0x02,
        
        Ping       = 0x11,
        Pong       = 0x12,

        Echo       = 0x21,
        EchoResult = 0x22,

        Info       = 0x31,
        InfoResult = 0x32,

        Error      = 0xFF
    };

    struct Frame {
        std::uint8_t version = 1;
        MessageType type;
        std::uint16_t flags = 0;
        std::uint32_t request_id = 0;
        std::vector<std::uint8_t> payload;
    };
}