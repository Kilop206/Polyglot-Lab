#pragma once

#include <cstdint>

#include "Frame.hpp"

namespace netlab {
    class Encoder {
        public :
        Frame& encode(const std::vector<std::uint8_t> encodedFrame);
    };
}