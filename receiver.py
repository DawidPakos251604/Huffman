import socket
import pickle
from huffman import decode

def start_server(host='0.0.0.0', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Serwer nasłuchuje na porcie {port}...")
        conn, addr = s.accept()
        with conn:
            print("Połączono z:", addr)
            data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk

            received = pickle.loads(data)
            root = received['tree']
            padding = received['padding']
            byte_data = received['data']

            bit_string = ''.join(f"{byte:08b}" for byte in byte_data)
            bit_string = bit_string[:-padding]

            decoded_text = decode(bit_string, root)

            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(decoded_text)
            print("Zapisano plik output.txt")

if __name__ == "__main__":
    start_server()