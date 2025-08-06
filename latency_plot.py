
import matplotlib.pyplot as plt

# Read latencies from the .txt file
with open('latency_data.txt') as f:
    latencies = [float(line.strip()) for line in f if line.strip()]

# Plot the latency data
plt.figure(figsize=(10, 5))
plt.plot(latencies, marker='o', linestyle='-', color='blue')
plt.title("Simulated Client Message Latency")
plt.xlabel("Message Number")
plt.ylabel("Latency (ms)")
plt.grid(True)
plt.tight_layout()
plt.savefig("latency_plot.png")
print("[Plot saved as latency_plot.png]")
