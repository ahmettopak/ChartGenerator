import matplotlib.pyplot as plt
import re

with open("logs.log", "r") as file:
    logs = file.read()

pattern = r"Current: (\d+), Bus: (\d+), Volt: (\d+), RPM: (\d+)"
matches = re.findall(pattern, logs)

current, bus, volt, rpm = zip(
    *[(int(m[0]), int(m[1]), int(m[2]), int(m[3])) for m in matches])

plt.figure(figsize=(10, 6))
plt.plot(current, label="Current", marker="o")
plt.plot(bus, label="Bus", marker="o")
plt.plot(volt, label="Volt", marker="o")
plt.plot(rpm, label="RPM", marker="o")
plt.xlabel("Log Index")
plt.ylabel("Values")
plt.title("Log Metrics Visualization")
plt.legend()
plt.grid()
plt.show()
