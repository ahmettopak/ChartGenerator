import matplotlib.pyplot as plt
import numpy as np
import re
import datetime
from collections import defaultdict

# Ayarlar
ENABLE_DOWNSAMPLING = True
ENABLE_SUMMARIZATION = False
SAMPLING_RATE = 10  
SUMMARY_STEP = 10  

print("🚀 Log dosyası okunuyor...")
try:
    with open("logs.log", "r") as file:
        logs = file.read()
    print("✅ Log dosyası başarıyla okundu.")
except Exception as e:
    print(f"❌ Log dosyası okunurken hata oluştu: {e}")
    exit()

# Logları ayrıştırmak için regex
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+) .*?: Motor (\d+) - ((?:\w+: \d+,? ?)+)"
matches = re.findall(pattern, logs)

print(f"🔍 {len(matches)} adet log kaydı bulundu.")

# Motor verilerini depolamak için defaultdict
motor_data = defaultdict(lambda: defaultdict(list))
timestamps = defaultdict(list)

# Verileri ayrıştır ve kaydet
for match in matches:
    try:
        timestamp_str, motor_num, metrics = match
        motor_num = int(motor_num)

        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        timestamps[motor_num].append(timestamp)

        metrics = metrics.split(", ")
        for metric in metrics:
            key, value = metric.split(": ")
            motor_data[motor_num][key.lower()].append(int(value))
        
        print(f"✅ Motor {motor_num} verileri başarıyla işlendi.")
    
    except Exception as e:
        print(f"❌ Hata! Motor {motor_num} verileri işlenirken sorun çıktı: {e}")

# Örnekleme fonksiyonu
def downsample(data, step):
    print(f"🔽 Downsampling uygulanıyor (step={step})...")
    return data[::step]

# Özetleme fonksiyonu
def summarize(data, step):
    print(f"📊 Özetleme uygulanıyor (step={step})...")
    return [np.mean(data[i:i + step]) for i in range(0, len(data), step) if i + step <= len(data)]

# Grafiklerin stilini ayarla
plt.style.use('dark_background')

# Her motor için ayrı grafik oluştur
for motor_num, data in motor_data.items():
    print(f"📈 Motor {motor_num} için grafik çiziliyor...")

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_title(f"Motor {motor_num} Metrics", fontsize=18, fontweight='bold', color='white')
    ax.set_xlabel("Timestamp", fontsize=14, color='white')
    ax.set_ylabel("Values", fontsize=14, color='white')

    time_data = timestamps[motor_num]
    if not time_data:
        print(f"⚠️ Uyarı: Motor {motor_num} için zaman verisi eksik, grafik çizilemez!")
        continue

    if ENABLE_DOWNSAMPLING:
        time_data = downsample(time_data, SAMPLING_RATE)
    elif ENABLE_SUMMARIZATION:
        time_data = summarize(time_data, SUMMARY_STEP)

    for key, values in data.items():
        if ENABLE_DOWNSAMPLING:
            y_values = downsample(values, SAMPLING_RATE)
        elif ENABLE_SUMMARIZATION:
            y_values = summarize(values, SUMMARY_STEP)
        else:
            y_values = values

        min_length = min(len(time_data), len(y_values))
        if min_length == 0:
            print(f"⚠️ Uyarı: Motor {motor_num}, {key} için yeterli veri yok, çizim atlandı!")
            continue

        time_data = time_data[:min_length]
        y_values = y_values[:min_length]

        print(f"🔹 {key.capitalize()} verisi çiziliyor... (Veri noktası: {len(y_values)})")
        ax.plot(time_data, y_values, label=key.capitalize(), marker="o", linestyle='-', markersize=6, linewidth=1.5)

        if y_values:
            max_val = max(y_values)
            min_val = min(y_values)
            avg_val = sum(y_values) / len(y_values)

            max_idx = y_values.index(max_val)
            min_idx = y_values.index(min_val)

            ax.scatter(time_data[max_idx], max_val, color='#FF5733', label=f"Max {key.capitalize()}: {max_val}", zorder=5)
            ax.scatter(time_data[min_idx], min_val, color='#33C1FF', label=f"Min {key.capitalize()}: {min_val}", zorder=5)

            ax.axhline(avg_val, color='#FFC300', linestyle='--', linewidth=1.2, alpha=0.8, zorder=4)
            ax.text(time_data[-1], avg_val, f"Avg {key.capitalize()}: {avg_val:.2f}", fontsize=10, color='#FFC300', verticalalignment='center')

    ax.legend(loc="best", fontsize=10)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    plt.xticks(rotation=45, fontsize=10, color='white')
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))

plt.tight_layout()
plt.show()
