from __future__ import annotations

import json
import socket
import struct
from dataclasses import dataclass

MAGIC = b"NL"
VERSION = 1
HEADER_SIZE = 14
MAX_PAYLOAD = 1_048_576

TYPES = {
    "HELLO": 0x01,
    "HELLO_ACK": 0x02,
    "PING": 0x10,
    "PONG": 0x11,
    "ECHO": 0x20,
    "ECHO_RESULT": 0x21,
    "INFO": 0x30,
    "INFO_RESULT": 0x31,
    "ERROR": 0xFF,
}
TYPE_NAMES = {value: key for key, value in TYPES.items()}

@dataclass
class Frame:
    version: int
    message_type: int
    flags: int
    request_id: int
    payload: bytes

    @property
    def type_name(self) -> str:
        return TYPE_NAMES.get(self.message_type, f"0x{self.message_type:02X}")

def encode_frame(message_type: str | int, request_id: int, payload: bytes = b"",
                 *, version: int = VERSION, flags: int = 0, magic: bytes = MAGIC) -> bytes:
    if isinstance(message_type, str):
        message_type = TYPES[message_type]
    return (
        magic
        + bytes([version, message_type])
        + struct.pack(">HII", flags, len(payload), request_id)
        + payload
    )

def recv_exact(sock: socket.socket, count: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < count:
        part = sock.recv(count - len(chunks))
        if not part:
            raise ConnectionError("peer closed connection")
        chunks.extend(part)
    return bytes(chunks)

def recv_frame(sock: socket.socket) -> Frame:
    header = recv_exact(sock, HEADER_SIZE)
    if header[:2] != MAGIC:
        raise ValueError("invalid magic in response")
    version = header[2]
    message_type = header[3]
    flags, length, request_id = struct.unpack(">HII", header[4:14])
    if length > MAX_PAYLOAD:
        raise ValueError("response payload too large")
    payload = recv_exact(sock, length) if length else b""
    return Frame(version, message_type, flags, request_id, payload)

def decode_error_payload(payload: bytes) -> tuple[int, str]:
    if len(payload) < 2:
        raise ValueError("ERROR payload shorter than 2 bytes")
    code = struct.unpack(">H", payload[:2])[0]
    return code, payload[2:].decode("utf-8", errors="replace")

def decode_info(payload: bytes) -> dict:
    return json.loads(payload.decode("utf-8"))
