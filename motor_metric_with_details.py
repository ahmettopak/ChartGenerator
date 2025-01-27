import matplotlib.pyplot as plt
import re
from collections import defaultdict

# Log dosyasını oku
with open("logs.log", "r") as file:
    logs = file.read()

# Logları ayrıştırmak için dinamik regex (Başlıkları yakalamak için)
pattern = r"Motor (\d+) - ((?:\w+: \d+,? ?)+)"
matches = re.findall(pattern, logs)

# Motor verilerini depolamak için defaultdict
motor_data = defaultdict(lambda: defaultdict(list))

# Verileri ayrıştır ve dinamik olarak başlıklara göre grupla
for match in matches:
    motor_num = int(match[0])  # Motor numarasını al
    metrics = match[1].split(", ")  # Verileri ayır

    for metric in metrics:
        key, value = metric.split(": ")
        motor_data[motor_num][key.lower()].append(
            int(value))  # Başlıkları küçük harfe çevir

# Grafiklerin stilini ayarla
plt.style.use('dark_background')  # Karanlık tema

# Her motor için ayrı grafik oluştur
for motor_num, data in motor_data.items():
    fig = plt.figure(figsize=(12, 8))  # Grafik boyutunu ayarla
    plt.title(f"Motor {motor_num} Metrics", fontsize=18,
              fontweight='bold', color='white')
    plt.xlabel("Log Index", fontsize=14, color='white')
    plt.ylabel("Values", fontsize=14, color='white')

    for key, values in data.items():
        # Verileri çiz
        plt.plot(values, label=key.capitalize(),
                 marker="o", linestyle='-', markersize=6, linewidth=1.5)

        # Maksimum, minimum ve ortalama değerler
        max_val = max(values)
        min_val = min(values)
        avg_val = sum(values) / len(values)
        max_idx = values.index(max_val)
        min_idx = values.index(min_val)

        # Highlight max and min points
        plt.scatter(max_idx, max_val, color='#FF5733',
                    label=f"Max {key.capitalize()}: {max_val}", zorder=5)
        plt.scatter(min_idx, min_val, color='#33C1FF',
                    label=f"Min {key.capitalize()}: {min_val}", zorder=5)

        # Draw the average line
        plt.axhline(avg_val, color='#FFC300', linestyle='--',
                    linewidth=1.2, alpha=0.8, zorder=4)
        plt.text(len(values) - 1, avg_val, f"Avg {key.capitalize()}: {avg_val:.2f}",
                 fontsize=10, color='#FFC300', verticalalignment='center')
    # Grid ve legend ayarları
    plt.legend(loc="best", fontsize=10)
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Tüm grafiklerin aynı anda gösterilmesini sağla
plt.show()
