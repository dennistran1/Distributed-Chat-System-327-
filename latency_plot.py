import csv
import matplotlib.pyplot as plt

# Load latency data from CSV
latencies = []
with open('latency_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
        latencies.append(float(row[1]))

# Plot latency distribution
plt.figure(figsize=(10, 5))
plt.plot(latencies, marker='o', linestyle='-', label='Latency per Message')
plt.xlabel('Message Index')
plt.ylabel('Latency (ms)')
plt.title('Message Latency Over Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('performance_graphs/latency_plot.png')
plt.show()
