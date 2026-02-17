import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

print("Configuración de la simulación")
try:
    m = float(input("Ingrese la masa (kg) [ej: 1]: ") or 1) 
    F = float(input("Ingrese la fuerza externa (N) [ej: 1]: ") or 1) 
    k = float(input("Ingrese la constante del resorte [ej: 10]: ") or 10)   
    t_sim = float(input("Ingrese el tiempo de simulacion [ej: 20]: ") or 20) 
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
t = np.linspace(0, t_sim, 500) 

#Resolver la ODE
sol = odeint(sistema_masa_resorte, z0, t, args=(m, c, k, F))
posicion = sol[:, 0]
velocidad = sol[:, 1]
aceleracion = (F - c*velocidad - k*posicion) / m

fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot(3, 2, 1) #Posición
ax2 = plt.subplot(3, 2, 3) #Velocidad
ax3 = plt.subplot(3, 2, 5) #Aceleración
ax_anim = plt.subplot(1, 2, 2) 

for ax, label, color in zip([ax1, ax2, ax3], 
                             ['Posición [m]', 'Velocidad [m/s]', 'Aceleración [m/s²]'],
                             ['blue', 'green', 'red']):
    ax.set_xlim(0, t_sim)
    ax.set_ylim(min(sol.flatten())*1.2, max(sol.flatten())*1.5) 
    ax.set_ylabel(label)
    ax.grid(True)

ax3.set_xlabel('Tiempo [s]')

line1, = ax1.plot([], [], color='blue')
line2, = ax2.plot([], [], color='green')
line3, = ax3.plot([], [], color='red')
punto1, = ax1.plot([], [], 'o', color='blue')


ax_anim.set_xlim(-0.5, 2.5) 
ax_anim.set_ylim(-1, 1)
ax_anim.set_title("Movimiento del Bloque")
ax_anim.get_yaxis().set_visible(False)

#Dibujo
masa_rect = plt.Rectangle((0, -0.2), 0.4, 0.4, fc='gray', ec='black')
ax_anim.add_patch(masa_rect)
resorte, = ax_anim.plot([], [], color='black', lw=2) 
pared = ax_anim.axvline(x=-0.4, color='black', lw=5) 

#Funcion para actualizar los frames de animacion
def update(frame):
    
    line1.set_data(t[:frame], posicion[:frame])
    line2.set_data(t[:frame], velocidad[:frame])
    line3.set_data(t[:frame], aceleracion[:frame])
    
    punto1.set_data([t[frame]], [posicion[frame]])
    

    x_current = posicion[frame]
    masa_rect.set_xy((x_current, -0.2))
    
    resorte.set_data([-0.4, x_current], [0, 0])
    
    return line1, line2, line3, punto1, masa_rect, resorte

#Animación
ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=True)

plt.tight_layout()
plt.show()