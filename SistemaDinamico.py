import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

print("Configuración de la simulación")
try:
    m = float(input("Ingrese la masa (kg) [ej: 1]: ")) 
    F = float(input("Ingrese la fuerza externa (N) [ej: 1]: ")) 
    k = float(input("Ingrese la constante del resorte [ej: 10]: "))   
    t_sim = float(input("Ingrese el tiempo de simulacion [ej: 20]: ")) 
except ValueError:
    print("Error: ingrese solo números.")
    exit()

c = 0.7  #Fricción

def sistema_masa_resorte(z, t, m, c, k, F):
    x, v = z
    dxdt = v
    dvdt = (F - c*v - k*x) / m
    return [dxdt, dvdt]

#Estado inicial
z0 = [0.0, 0.0]
t = np.linspace(0, t_sim, 1000)

#Resolver la ODE
sol = odeint(sistema_masa_resorte, z0, t, args=(m, c, k, F))

#Posición y Velocidad
posicion = sol[:, 0]
velocidad = sol[:, 1]

#Calcular Aceleración 
aceleracion = (F - c*velocidad - k*posicion) / m

#Graficar
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

#Gráfico Posición
axs[0].plot(t, posicion, color='blue', label='Posición (x)')
axs[0].set_ylabel('Desplazamiento [m]')
axs[0].set_title('Dinámica del Sistema Masa-Resorte-Amortiguador')
axs[0].grid(True)
axs[0].legend()

#Gráfico Velocidad
axs[1].plot(t, velocidad, color='green', label='Velocidad (v)')
axs[1].set_ylabel('Velocidad [m/s]')
axs[1].grid(True)
axs[1].legend()

#Gráfico Aceleración
axs[2].plot(t, aceleracion, color='red', label='Aceleración (a)')
axs[2].set_ylabel('Aceleración [m/s^2]')
axs[2].set_xlabel('Tiempo [s]')
axs[2].grid(True)
axs[2].legend()

plt.tight_layout()
plt.show()