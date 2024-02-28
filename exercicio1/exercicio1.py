import threading
import time

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_primes(start, end, result_list):
    primes = [num for num in range(start, end) if is_prime(num)]
    result_list.extend(primes)

def write_results_to_file(N, num_threads, result_list, execution_time):
    filename = f"resultado_exercicio_1_{N}_{num_threads}_threads.txt"
    with open(filename, 'w') as file:
        file.write(f"Prime numbers between 1 and {N} with {num_threads} threads:\n")
        file.write(f"Result: {result_list}\n")
        file.write(f"Execution time: {execution_time:.4f} seconds\n")

def main(N, num_threads):
    chunk_size = N // num_threads
    threads = []
    result_list = []

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i < num_threads - 1 else N + 1
        thread = threading.Thread(target=find_primes, args=(start, end, result_list))
        threads.append(thread)

    start_time = time.time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    write_results_to_file(N, num_threads, result_list, end_time - start_time)

if __name__ == "__main__":
    N_values = [1000000, 2000000]
    X_threads = [1, 4, 8]

    for N in N_values:
        for X in X_threads:
            main(N, X)
