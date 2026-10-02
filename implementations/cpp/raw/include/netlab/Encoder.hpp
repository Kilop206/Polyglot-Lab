#pragma once

#include <vector>
#include <cstdint>

#include "Frame.hpp"

namespace netlab {
    class Encoder {
        std::vector<std::uint8_t> encode(const Frame& frame);
    };
}