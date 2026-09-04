import numpy as np
import matplotlib.pyplot as plt

# 1. Leer el archivo binario generado por rtl_sdr (son enteros sin signo de 8 bits)
raw_data = np.fromfile('captura_rfid.raw', dtype=np.uint8)

# 2. Convertir los datos a formato complejo (I + jQ)
# El SDR guarda los datos intercalados: I, Q, I, Q...
# Restamos 127.5 para centrar la señal en cero (ya que venía de 0 a 255)
data = raw_data.astype(np.float32) - 127.5
iq_data = data[0::2] + 1j * data[1::2]

# 3. Calcular la magnitud (envolvente AM de la señal)
amplitud = np.abs(iq_data)

# 4. Seleccionar un fragmento pequeño para graficar (ej. 10,000 muestras = 5 milisegundos)
# Si graficas todo, la memoria de tu PC colapsará.
fragmento = amplitud[1000000:1010000] 

# 5. Graficar
plt.figure(figsize=(12, 4))
plt.plot(fragmento, color='blue')
plt.title('Modulación de Amplitud (ASK) - Comunicación Lector-Tarjeta 13.56 MHz')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()
