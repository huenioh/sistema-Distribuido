import socket
import pickle
import time

BUFFER_SIZE = 4096

def main(start, end, workers):
    host = 'localhost'
    port = 8000

    interval = (start, end, workers)
    serialized_interval = pickle.dumps(interval)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"Tentando se conectar a {host}:{port}")
        client_socket.connect((host, port))
        print(f"Conexão estabelecida com sucesso!")
        client_socket.sendall(serialized_interval)

        received_data = b''

        while True:
            data_chunk = client_socket.recv(BUFFER_SIZE)
            if not data_chunk:
                break

            received_data += data_chunk

        client_socket.shutdown(socket.SHUT_RDWR)

        primes = pickle.loads(received_data)
        print(f"Números primos encontrados: {primes}")

if __name__ == "__main__":
    start_time = time.time()

    N_values = [1000000, 2000000]
    T_values = [2, 4]

    for N in N_values:
        for T in T_values:
            main(1, N, T)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tempo total de execução: {elapsed_time} segundos")
