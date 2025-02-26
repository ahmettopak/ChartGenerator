import matplotlib.pyplot as plt
import re
from collections import defaultdict

# Log dosyasını oku
with open("logs.log", "r") as file:
    logs = file.read()

# Logları ayrıştırmak için dinamik regex (Timestamp ve başlıkları yakalamak için)
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+) .*?: Motor (\d+) - ((?:\w+: \d+,? ?)+)"
matches = re.findall(pattern, logs)

# Motor verilerini depolamak için defaultdict
motor_data = defaultdict(lambda: defaultdict(list))

# Timestampleri tutmak için ayrı bir yapı
timestamps = defaultdict(list)

# Verileri ayrıştır ve dinamik olarak başlıklara göre grupla
for match in matches:
    timestamp, motor_num, metrics = match
    motor_num = int(motor_num)  # Motor numarasını al
    timestamps[motor_num].append(timestamp)  # Timestamp'i kaydet

    metrics = metrics.split(", ")  # Verileri ayır
    for metric in metrics:
        key, value = metric.split(": ")
        motor_data[motor_num][key.lower()].append(
            int(value))  # Başlıkları küçük harfe çevir

# Grafiklerin stilini ayarla
plt.style.use('dark_background')  # Karanlık tema

# Her motor için ayrı grafik oluştur
for motor_num, data in motor_data.items():
    fig, ax = plt.subplots(figsize=(14, 8))  # Grafik boyutunu ayarla
    ax.set_title(f"Motor {motor_num} Metrics",
                 fontsize=18, fontweight='bold', color='white')
    ax.set_xlabel("Timestamp", fontsize=14, color='white')
    ax.set_ylabel("Values", fontsize=14, color='white')

    # X ekseni için timestampleri kullan
    x_ticks = timestamps[motor_num]

    for key, values in data.items():
        # Verileri çiz
        ax.plot(x_ticks, values, label=key.capitalize(), marker="o",
                linestyle='-', markersize=6, linewidth=1.5)

        # Maksimum, minimum ve ortalama değerler
        max_val = max(values)
        min_val = min(values)
        avg_val = sum(values) / len(values)
        max_idx = values.index(max_val)
        min_idx = values.index(min_val)

        # Highlight max and min points
        ax.scatter(x_ticks[max_idx], max_val, color='#FF5733',
                   label=f"Max {key.capitalize()}: {max_val}", zorder=5)
        ax.scatter(x_ticks[min_idx], min_val, color='#33C1FF',
                   label=f"Min {key.capitalize()}: {min_val}", zorder=5)

        # Draw the average line
        ax.axhline(avg_val, color='#FFC300', linestyle='--',
                   linewidth=1.2, alpha=0.8, zorder=4)
        ax.text(len(values) - 1, avg_val, f"Avg {key.capitalize()}: {avg_val:.2f}",
                fontsize=10, color='#FFC300', verticalalignment='center')

    # Grid ve legend ayarları
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # X ekseni için timestampleri döndür
    plt.xticks(rotation=45, fontsize=10, color='white')

# Tüm grafiklerin aynı anda gösterilmesini sağla
plt.tight_layout()
plt.show()
