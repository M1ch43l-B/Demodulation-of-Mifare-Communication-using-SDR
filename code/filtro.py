import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# --- 1. Parámetros de la Señal ---
sample_rate = 2000000  # 2 MHz (lo que pusiste en rtl_sdr)
frecuencia_subportadora = 847500  # 847.5 kHz (Estándar ISO 14443A)
ancho_banda = 50000 # 150 kHz de tolerancia para captar la modulación Manchester

# --- 2. Cargar y convertir los datos I/Q crudos ---
print("Cargando datos crudos...")
raw_data = np.fromfile('captura_rfid.raw', dtype=np.uint8)
data = raw_data.astype(np.float32) - 127.5
iq_data = data[0::2] + 1j * data[1::2]

# --- 3. Aislar la envolvente de Amplitud (Lo que tenías antes) ---
amplitud_total = np.abs(iq_data)

# --- 4. Diseño del Filtro Pasabanda ---
print("Aplicando filtro matemático para revelar la tarjeta...")
# Definimos los límites del filtro (frecuencia de corte inferior y superior)
lowcut = frecuencia_subportadora - (ancho_banda / 2)
highcut = frecuencia_subportadora + (ancho_banda / 2)

# Normalizamos las frecuencias según el teorema de Nyquist (mitad de la tasa de muestreo)
nyq = 0.5 * sample_rate
low = lowcut / nyq
high = highcut / nyq

# Creamos un filtro Butterworth de orden 4
b, a = butter(4, [low, high], btype='band')

# --- 5. Aplicar el filtro ---
# Filtramos directamente la señal compleja original (no la amplitud) para mantener la fase
senal_filtrada = filtfilt(b, a, iq_data)

# Calculamos la amplitud de la señal que ya fue limpiada
amplitud_tarjeta = np.abs(senal_filtrada)

# --- 6. Graficar el "Antes" y el "Después" ---
# Seleccionamos el mismo fragmento interesante de tu captura anterior (ej. 2000 a 10000)
inicio_grafico = 1000000
fin_grafico = 1010000


print("Generando gráficos...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Gráfico Superior: Lector (Proxmark3)
ax1.plot(amplitud_total[inicio_grafico:fin_grafico], color='blue')
ax1.set_title('Señal Cruda (Se ven los comandos del Lector - ASK al 100%)')
ax1.set_ylabel('Amplitud Total')
ax1.grid(True)

# Gráfico Inferior: Tarjeta (Respuesta filtrada)
ax2.plot(amplitud_tarjeta[inicio_grafico:fin_grafico], color='red')
ax2.set_title('Señal Filtrada a 847.5 kHz (Se revela la respuesta de la Tarjeta)')
ax2.set_ylabel('Amplitud Subportadora')
ax2.set_xlabel('Muestras')
ax2.grid(True)

plt.tight_layout()
plt.show()
