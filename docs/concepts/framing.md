# Why Framing Exists

TCP has no concept of a NetLab message boundary.

NetLab uses a fixed header containing a payload length. Once 14 header bytes are
available, the parser knows exactly how many additional bytes belong to the
frame.

This approach is commonly called length-prefixed framing.
