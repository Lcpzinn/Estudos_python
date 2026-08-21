import matplotlib.pyplot as plt

plt.plot([-4, -1, 0, 1, 2, 3, 4], [-16, -1, 0, 1, 4, 9, 16])

plt.title ("Gráfico de uma função quadrática")
plt.xlabel ("x")
plt.ylabel ("f(x)")
plt.grid (True)
plt.savefig("grafico.png", dpi=300, bbox_inches="tight")
plt.show ()