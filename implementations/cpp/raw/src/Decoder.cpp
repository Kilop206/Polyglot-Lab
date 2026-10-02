#include "Encoder.hpp"

#include <bitset>
#include <vector>

namespace netlab {

    const Frame& decode(const std::vector<std::uint8_t> encodedFrame) {

        auto encodedFrameVersion = std::bitset<8>(encodedFrame[0]).to_ulong();
        auto version = static_cast<std::uint8_t>(encodedFrameVersion);

        auto encodedFrameType = std::bitset<8>(encodedFrame[1]).to_ulong();
        auto type = static_cast<MessageType>(static_cast<std::uint8_t>(encodedFrameType));

        std::uint16_t flags = (static_cast<std::uint16_t>(encodedFrame[2]) << 8) | encodedFrame[3];

        std::uint32_t request_id = (static_cast<std::uint32_t>(encodedFrame[4]) << 24) |
                                (static_cast<std::uint32_t>(encodedFrame[5]) << 16) |
                                (static_cast<std::uint32_t>(encodedFrame[6]) << 8)  |
                                    encodedFrame[7];

        
        std::vector<std::uint8_t> payload;

        for (int i = 8; i < encodedFrame.size(); i++) {
            payload.push_back(static_cast<std::uint8_t>(encodedFrame[i]));
        }

        return Frame(version, type, flags, request_id, payload);
    }
}