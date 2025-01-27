import matplotlib.pyplot as plt
import re
from collections import defaultdict

with open("logs.log", "r") as file:
    logs = file.read()

pattern = r"Motor (\d+) - ((?:\w+: \d+,? ?)+)"
matches = re.findall(pattern, logs)

motor_data = defaultdict(lambda: defaultdict(list))

for match in matches:
    motor_num = int(match[0])
    metrics = match[1].split(", ")

    for metric in metrics:
        key, value = metric.split(": ")
        motor_data[motor_num][key.lower()].append(
            int(value))

plt.style.use('seaborn-darkgrid')

for motor_num, data in motor_data.items():
    fig = plt.figure(figsize=(10, 6))
    for key, values in data.items():
        plt.plot(values, label=key.capitalize(),
                 marker="o", linestyle='-', markersize=6)

    plt.title(f"Motor {motor_num} Metrics", fontsize=16, fontweight='bold')
    plt.xlabel("Log Index", fontsize=12)
    plt.ylabel("Values", fontsize=12)

    plt.legend(loc="upper right", fontsize=10)
    plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

plt.show()
