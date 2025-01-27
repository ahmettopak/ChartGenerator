import re
from collections import defaultdict
import plotly.graph_objects as go
import plotly.io as pio

# Tarayıcıda grafiklerin açılması için:
pio.renderers.default = "browser"

# Log dosyasını oku
try:
    with open("logs.log", "r") as file:
        logs = file.read()
except FileNotFoundError:
    print("Log dosyası bulunamadı!")
    exit()

# Logları ayrıştırmak için dinamik regex
pattern = r"Motor (\d+) - ((?:\w+: \d+,? ?)+)"
matches = re.findall(pattern, logs)

if not matches:
    print("Log dosyasındaki format regex ile uyuşmuyor!")
    exit()

# Motor verilerini depolamak için defaultdict
motor_data = defaultdict(lambda: defaultdict(list))

# Verileri ayrıştır ve dinamik olarak başlıklara göre grupla
for match in matches:
    motor_num = int(match[0])  # Motor numarasını al
    metrics = match[1].split(", ")  # Verileri ayır

    for metric in metrics:
        try:
            key, value = metric.split(": ")
            motor_data[motor_num][key.lower()].append(
                int(value))  # Başlıkları küçük harfe çevir
        except ValueError:
            print(f"Veri hatası: {metric}")

# Her motor için etkileşimli grafik oluştur
for motor_num, data in motor_data.items():
    fig = go.Figure()  # Plotly figür nesnesi

    for key, values in data.items():
        # Maksimum, minimum ve ortalama değerler
        max_val = max(values)
        min_val = min(values)
        avg_val = sum(values) / len(values)
        max_idx = values.index(max_val)
        min_idx = values.index(min_val)

        # Verileri çiz
        fig.add_trace(go.Scatter(
            x=list(range(len(values))),
            y=values,
            mode="lines+markers",
            name=f"{key.capitalize()}",
            line=dict(width=2),
            marker=dict(size=6)
        ))

        # Maksimum ve minimum noktaları ekle
        fig.add_trace(go.Scatter(
            x=[max_idx],
            y=[max_val],
            mode="markers+text",
            name=f"Max {key.capitalize()}: {max_val}",
            marker=dict(color="red", size=10),
            text=[f"Max: {max_val}"],
            textposition="top center"
        ))

        fig.add_trace(go.Scatter(
            x=[min_idx],
            y=[min_val],
            mode="markers+text",
            name=f"Min {key.capitalize()}: {min_val}",
            marker=dict(color="blue", size=10),
            text=[f"Min: {min_val}"],
            textposition="bottom center"
        ))

        # Ortalama çizgisi
        fig.add_trace(go.Scatter(
            x=list(range(len(values))),
            y=[avg_val] * len(values),
            mode="lines",
            name=f"Avg {key.capitalize()}: {avg_val:.2f}",
            line=dict(dash="dash", color="orange")
        ))

    # Grafik düzeni
    fig.update_layout(
        title=f"Motor {motor_num} Metrics",
        xaxis_title="Log Index",
        yaxis_title="Values",
        template="plotly_dark",
        legend=dict(font=dict(size=10)),
        hovermode="x unified"
    )

    # Grafik gösterimi
    fig.show()
