#pragma once

#include <cstdint>

#include "Frame.hpp"

namespace netlab {
    class Decoder {
        const Frame& decode(const std::vector<std::uint8_t> encodedFrame);
    };
}