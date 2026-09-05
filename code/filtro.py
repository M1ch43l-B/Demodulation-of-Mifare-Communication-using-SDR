import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

sample_rate = 2000000  # 2 MHz 
frecuencia_subportadora = 847500  # 847.5 kHz (ISO 14443A)
ancho_banda = 50000

print("Cargando datos crudos...")
raw_data = np.fromfile('captura_rfid.raw', dtype=np.uint8)
data = raw_data.astype(np.float32) - 127.5
iq_data = data[0::2] + 1j * data[1::2]

amplitud_total = np.abs(iq_data)

print("Aplicando filtro matemático para revelar la tarjeta...")
lowcut = frecuencia_subportadora - (ancho_banda / 2)
highcut = frecuencia_subportadora + (ancho_banda / 2)

nyq = 0.5 * sample_rate
low = lowcut / nyq
high = highcut / nyq

b, a = butter(4, [low, high], btype='band')

senal_filtrada = filtfilt(b, a, iq_data)

amplitud_tarjeta = np.abs(senal_filtrada)

inicio_grafico = 1000000
fin_grafico = 1010000

print("Generando gráficos...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Gráfico Superior: Lector (Proxmark3)
ax1.plot(amplitud_total[inicio_grafico:fin_grafico], color='blue')
ax1.set_title('Raw Signal (Reader Commands - OOK)')
ax1.set_ylabel('Total Amplitude')
ax1.grid(True)

# Gráfico Inferior: Tarjeta (Respuesta filtrada)
ax2.plot(amplitud_tarjeta[inicio_grafico:fin_grafico], color='red')
ax2.set_title('Filtered Signal at 847.5 kHz (Tag Response Revealed)')
ax2.set_ylabel('Subcarrier Amplitude')
ax2.set_xlabel('Samples')
ax2.grid(True)

plt.tight_layout()
plt.show()
