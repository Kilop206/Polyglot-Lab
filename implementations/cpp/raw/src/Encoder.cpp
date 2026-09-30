#include "Encoder.hpp"

#include <bitset>
#include <vector>

namespace netlab {

    std::vector<std::uint8_t> encode(const Frame& frame) {

        auto version = std::bitset<8>(frame.version);
        auto type = std::bitset<8>(static_cast<uint8_t>(frame.type));
        auto flags = std::bitset<8>(frame.flags);
        auto request_id = std::bitset<8>(frame.request_id);
        
        std::vector<std::bitset<8>> payloads;

        for (auto n : frame.payload) {
            payloads.push_back(std::bitset<8>(n));
        }
    }
}