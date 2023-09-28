import ssl
import socket
import time
from datetime import datetime

# Function to perform an SSL handshake and measure latency
def measure_ssl_latency(fqdn):
    try:
        # Create a socket and set a timeout for the handshake
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Adjust the timeout as needed

        # Start measuring time
        start_time = time.time()

        # Perform SSL handshake
        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=fqdn) as ssock:
            ssock.connect((fqdn, 443))

        # Calculate latency in milliseconds with two decimal places
        latency = round((time.time() - start_time) * 1000, 2)

        return fqdn, latency

    except Exception as e:
        return fqdn, str(e)

# Input and output file paths
input_file = "input.txt"
output_file = "output.txt"

# Read loop_duration_minutes from the config file
with open("config.txt", "r") as config_file:
    loop_duration_minutes = int(config_file.read().strip())

# Read FQDNs from the input file
with open(input_file, "r") as file:
    fqdns = [line.strip() for line in file]

# Configuration for looping
loop_interval_seconds = 30

# Calculate the number of iterations based on the loop duration
num_iterations = (loop_duration_minutes * 60) // loop_interval_seconds

# Perform SSL handshake measurements in a loop
with open(output_file, "a") as file:
    file.write("Date Time\tFQDN\tLatency (ms)\n")  # Header

for iteration in range(num_iterations):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Iteration {iteration + 1}/{num_iterations} - {current_time}")
    
    with open(output_file, "a") as file:
        for fqdn in fqdns:
            result = measure_ssl_latency(fqdn)
            file.write(f"{current_time}\t{result[0]}\t{result[1]:.2f}\n")  # Format latency to two decimal places
            print(f"{result[0]} - Latency: {result[1]:.2f} ms")
        file.write('\n')  # Insert a blank line

    if iteration < num_iterations - 1:
        print(f"Waiting for {loop_interval_seconds} seconds before the next iteration...")
        time.sleep(loop_interval_seconds)

print("Latency measurement completed.")
