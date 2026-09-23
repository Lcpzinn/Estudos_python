import numpy as np
import matplotlib.pyplot as plt

# 1. Carregar os dados do arquivo
dados = np.loadtxt("lancamento.dat")

tempo = dados[:, 0]
posicao_x = dados[:, 1]
posicao_y = dados[:, 2]

# 2. Calcular parâmetros iniciais
dt = tempo[1] - tempo[0]
v0_x = (posicao_x[1] - posicao_x[0]) / dt
v0_y = (posicao_y[1] - posicao_y[0]) / dt

v0 = np.sqrt(v0_x**2 + v0_y**2)
angulo_graus = np.degrees(np.arctan2(v0_y, v0_x))

coeficientes = np.polyfit(tempo, posicao_y, 2)
g = -2 * coeficientes[0]

# 3. Trajetória 1: Sem Resistência do Ar (Modelo Ideal)
t_sim = np.linspace(0, max(tempo), 200)
x_sem_ar = v0_x * t_sim
y_sem_ar = v0_y * t_sim - 0.5 * g * (t_sim**2)

# Trajetória 2: Dados Calculados/Medidos
x_com_ar = posicao_x
y_com_ar = posicao_y

# --- CÁLCULO DOS PONTOS NOTÁVEIS ---
# Altura máxima nos dados reais
idx_ymax = np.argmax(y_com_ar)
x_ymax = x_com_ar[idx_ymax]
ymax = y_com_ar[idx_ymax]

# --- 4. CONFIGURAÇÃO AVANÇADA DO GRÁFICO ---
plt.figure(figsize=(11, 6))

# Trajetórias
plt.plot(x_sem_ar, y_sem_ar, '--', label="Ideal (Sem Resistência do Ar)", color="navy", linewidth=2)
plt.plot(x_com_ar, y_com_ar, '-', label="Real (Com Resistência do Ar)", color="firebrick", linewidth=2)

# Ponto de Altura Máxima
plt.plot(x_ymax, ymax, 'ro', markersize=8)
plt.annotate(f' Altura Máx: {ymax:.2f}m', 
             xy=(x_ymax, ymax), 
             xytext=(x_ymax + 1, ymax),
             fontweight='bold',
             fontsize=9)

# Caixa de texto com os parâmetros calculados no gráfico
texto_info = (f"Parâmetros:\n"
              f"• $v_0$ = {v0:.2f} m/s\n"
              f"• $\\theta$ = {angulo_graus:.1f}°\n"
              f"• $g$ = {g:.2f} m/s²")

plt.gca().text(0.03, 0.95, texto_info, transform=plt.gca().transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))

# Estilização do Gráfico
plt.title("Comparativo da Trajetória do Foguete", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Posição Horizontal - X (m)", fontsize=11)
plt.ylabel("Posição Vertical - Y (m)", fontsize=11)

# Ajuste do eixo Y para não ficar negativo
plt.ylim(bottom=0)

plt.axhline(0, color='black', linewidth=1) # Linha destacada do solo
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right', frameon=True)

plt.tight_layout()
plt.show()