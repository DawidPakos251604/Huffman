import socket
import pickle
import sys
from huffman import build_huffman_tree, generate_codes, encode

def send_file(filename, host='127.0.0.1', port=65432):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    root = build_huffman_tree(text)
    codebook = generate_codes(root)
    encoded_bits = encode(text, codebook)

    padding = 8 - len(encoded_bits) % 8
    encoded_bits += '0' * padding

    byte_data = bytearray()
    for i in range(0, len(encoded_bits), 8):
        byte = encoded_bits[i:i+8]
        byte_data.append(int(byte, 2))

    data = {
        'tree': root,
        'padding': padding,
        'data': byte_data
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Łączenie z serwerem {host}:{port}...")
        s.connect((host, port))
        s.sendall(pickle.dumps(data))
        print("Wysłano dane do serwera.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python send.py <IP_serwera> [port]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 65432
    send_file("input.txt", host, port)