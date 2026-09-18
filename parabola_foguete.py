import numpy as np
import matplotlib.pyplot as plt

dados = np.loadtxt("lancamento.dat")

posicao_x = dados[:, 1]
posicao_y = dados[:, 2]

plt.plot(posicao_x, posicao_y)
plt.xlabel("X(m)")
plt.ylabel("Y(m)")
plt.title("Trajetória do Foguete")
plt.show()