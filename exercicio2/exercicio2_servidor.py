import socket
import pickle
import threading
import time

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_primes(start, end):
    primes = [num for num in range(start, end + 1) if is_prime(num)]
    return primes

def worker_process(interval):
    start, end, workers = interval
    primes = find_primes(start, end)
    return primes

def save_to_file(interval, primes, elapsed_time, workers):
    with open(f"resultado_{workers}_{interval[0]}_{interval[1]}workers.txt", "w") as file:
        file.write(f"Intervalo: {interval}\n")
        file.write(f"Quantidade de Trabalhadores: {workers}\n")
        file.write("Números primos encontrados:\n")
        for prime in primes:
            file.write(f"{prime}\n")
        file.write(f"Tempo de execução: {elapsed_time} segundos\n")

def handle_client(client_socket, start_interval, end_interval, workers):
    interval = (start_interval, end_interval, workers)
    start_time = time.time()
    result = worker_process(interval)
    end_time = time.time()

    elapsed_time = end_time - start_time

    save_to_file(interval, result, elapsed_time, workers)

    serialized_result = pickle.dumps(result)
    client_socket.sendall(serialized_result)
    client_socket.close()

def start_server():
    host = 'localhost'
    port = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Servidor aguardando conexões em {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexão estabelecida com {addr}")
            data = client_socket.recv(1024)
            interval = pickle.loads(data)

            T = interval[2]
            interval_size = (interval[1] - interval[0] + 1) // T

            threads = []
            for i in range(T):
                start_interval = interval[0] + i * interval_size
                end_interval = start_interval + interval_size - 1 if i < T - 1 else interval[1]

                thread = threading.Thread(target=handle_client, args=(client_socket, start_interval, end_interval, T))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

if __name__ == "__main__":
    start_server()
