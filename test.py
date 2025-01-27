import matplotlib.pyplot as plt
import re

logs = """
2025-01-27 21:15:13.344 [INFO]: Metrics - Current: 43, Bus: 91, Volt: 84, RPM: 2995
2025-01-27 21:15:13.455 [INFO]: Metrics - Current: 54, Bus: 68, Volt: 72, RPM: 3127
2025-01-27 21:15:13.566 [INFO]: Metrics - Current: 33, Bus: 59, Volt: 22, RPM: 718
2025-01-27 21:15:13.670 [INFO]: Metrics - Current: 19, Bus: 49, Volt: 41, RPM: 4185
2025-01-27 21:15:13.773 [INFO]: Metrics - Current: 18, Bus: 40, Volt: 56, RPM: 1132
2025-01-27 21:15:13.876 [INFO]: Metrics - Current: 7, Bus: 4, Volt: 40, RPM: 722
2025-01-27 21:15:13.980 [INFO]: Metrics - Current: 25, Bus: 89, Volt: 36, RPM: 1360
"""

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
