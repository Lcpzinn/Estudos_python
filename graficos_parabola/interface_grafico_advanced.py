from __future__ import annotations

import os
import tkinter as tk
from io import StringIO
from pathlib import Path
from tkinter import filedialog, ttk

import matplotlib
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


class AppGraficoAvancado(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Plotador Avançado de Dados")
        self.geometry("1100x780")
        self.minsize(900, 650)

        self.file_path_1 = tk.StringVar(value="")
        self.file_path_2 = tk.StringVar(value="")
        self.separator_var = tk.StringVar(value="auto")
        self.chart_type_var = tk.StringVar(value="linha")
        self.title_var = tk.StringVar(value="Gráfico de x e y")
        self.x_label_var = tk.StringVar(value="x")
        self.y_label_var = tk.StringVar(value="y")
        self.status_var = tk.StringVar(value="Selecione um arquivo CSV, TXT ou DAT ou cole os dados abaixo")
        self.df_1 = None
        self.df_2 = None

        self._build_ui()

    def _build_ui(self) -> None:
        top = ttk.Frame(self, padding=12)
        top.pack(fill="x")

        ttk.Button(top, text="Arquivo 1", command=lambda: self._selecionar_arquivo(1)).pack(side="left")
        ttk.Entry(top, textvariable=self.file_path_1, width=35).pack(side="left", padx=(8, 10), fill="x", expand=True)

        ttk.Button(top, text="Arquivo 2", command=lambda: self._selecionar_arquivo(2)).pack(side="left")
        ttk.Entry(top, textvariable=self.file_path_2, width=35).pack(side="left", padx=(8, 10), fill="x", expand=True)

        ttk.Button(top, text="Gerar gráfico", command=self._gerar_grafico).pack(side="left", padx=(0, 8))
        ttk.Button(top, text="Salvar PNG", command=self._salvar_imagem).pack(side="left")

        controls = ttk.Frame(self, padding=(12, 0, 12, 12))
        controls.pack(fill="x")

        ttk.Label(controls, text="Separador:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(
            controls,
            textvariable=self.separator_var,
            values=["auto", ",", ";", "\t", " "],
            width=10,
            state="readonly",
        ).grid(row=0, column=1, sticky="w", padx=(0, 20), pady=4)

        ttk.Label(controls, text="Tipo:").grid(row=0, column=2, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(
            controls,
            textvariable=self.chart_type_var,
            values=["linha", "barra", "dispersao", "histograma"],
            width=12,
            state="readonly",
        ).grid(row=0, column=3, sticky="w", padx=(0, 20), pady=4)

        ttk.Label(controls, text="Título:").grid(row=0, column=4, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(controls, textvariable=self.title_var, width=28).grid(row=0, column=5, sticky="w", pady=4)

        ttk.Label(controls, text="Eixo X:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(controls, textvariable=self.x_label_var, width=20).grid(row=1, column=1, sticky="w", pady=4)

        ttk.Label(controls, text="Eixo Y:").grid(row=1, column=2, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(controls, textvariable=self.y_label_var, width=20).grid(row=1, column=3, sticky="w", pady=4)

        ttk.Label(self, textvariable=self.status_var, foreground="darkblue").pack(fill="x", padx=12, pady=(0, 8))

        data_frame = ttk.LabelFrame(self, text="Dados colados (opcional)", padding=10)
        data_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.data_text = tk.Text(data_frame, height=8, width=120)
        self.data_text.insert("1.0", "x;y\n0;0\n1;2\n2;4\n3;6\n4;8\n5;10")
        self.data_text.pack(fill="both", expand=True)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.fig = Figure(figsize=(9, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.container)
        self.toolbar.update()
        self.toolbar.pack(side="bottom", fill="x")

    def _selecionar_arquivo(self, numero: int) -> None:
        arquivo = filedialog.askopenfilename(
            title=f"Escolha o arquivo {numero}",
            filetypes=[
                ("CSV, TXT, DAT", "*.csv;*.txt;*.dat"),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if arquivo:
            if numero == 1:
                self.file_path_1.set(arquivo)
            else:
                self.file_path_2.set(arquivo)
            self.status_var.set(f"Arquivo {numero} selecionado: {os.path.basename(arquivo)}")

    def _ler_dados(self, caminho: str) -> pd.DataFrame:
        if not caminho.strip():
            raise ValueError("Selecione um arquivo antes de gerar o gráfico.")

        path = Path(caminho)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        separadores = [self.separator_var.get()] if self.separator_var.get() != "auto" else [",", ";", "\t", " "]

        for separador in separadores:
            for header in [0, None]:
                try:
                    df = pd.read_csv(path, sep=separador, engine="python", comment="#", header=header)
                    if df.shape[1] < 2:
                        continue

                    df = df.iloc[:, :2].copy()
                    df.columns = ["x", "y"]
                    df["x"] = pd.to_numeric(df["x"], errors="coerce")
                    df["y"] = pd.to_numeric(df["y"], errors="coerce")
                    df = df.dropna().reset_index(drop=True)

                    if not df.empty:
                        return df
                except Exception:
                    continue

        raise ValueError(
            "Arquivo inválido para dados em x e y. "
            "Use duas colunas com valores numéricos e separador adequado."
        )

    def _parse_texto_dados(self, texto: str) -> pd.DataFrame:
        text = texto.strip()
        if not text:
            raise ValueError("Cole os dados em formato x e y antes de gerar o gráfico.")

        separadores = [self.separator_var.get()] if self.separator_var.get() != "auto" else [",", ";", "\t", " "]

        for separador in separadores:
            try:
                df = pd.read_csv(StringIO(text), sep=separador, engine="python", comment="#")
                if df.shape[1] < 2:
                    continue
                df = df.iloc[:, :2].copy()
                df.columns = ["x", "y"]
                df["x"] = pd.to_numeric(df["x"], errors="coerce")
                df["y"] = pd.to_numeric(df["y"], errors="coerce")
                df = df.dropna().reset_index(drop=True)
                if not df.empty:
                    return df
            except Exception:
                continue

        raise ValueError(
            "Os dados colados não estão no formato correto. "
            "Use algo como: x;y\n0;0\n1;2\n2;4"
        )

    def _gerar_grafico(self) -> None:
        try:
            texto_colado = self.data_text.get("1.0", "end").strip()

            if texto_colado:
                self.df_1 = self._parse_texto_dados(texto_colado)
                self.df_2 = None
            else:
                if self.file_path_1.get().strip():
                    self.df_1 = self._ler_dados(self.file_path_1.get())
                else:
                    self.df_1 = None

                if self.file_path_2.get().strip():
                    self.df_2 = self._ler_dados(self.file_path_2.get())
                else:
                    self.df_2 = None

            if self.df_1 is None and self.df_2 is None:
                raise ValueError("Selecione um arquivo ou cole os dados para plotar.")

            self.ax.clear()
            tipo = self.chart_type_var.get()

            if tipo == "barra":
                if self.df_1 is not None and self.df_2 is not None:
                    self.ax.bar(self.df_1["x"], self.df_1["y"], alpha=0.7, label="Arquivo 1")
                    self.ax.bar(self.df_2["x"], self.df_2["y"], alpha=0.7, label="Arquivo 2")
                    self.ax.legend()
                elif self.df_1 is not None:
                    self.ax.bar(self.df_1["x"], self.df_1["y"], alpha=0.8)
                else:
                    self.ax.bar(self.df_2["x"], self.df_2["y"], alpha=0.8)

            elif tipo == "dispersao":
                if self.df_1 is not None:
                    self.ax.scatter(self.df_1["x"], self.df_1["y"], label="Dados", s=50)
                if self.df_2 is not None:
                    self.ax.scatter(self.df_2["x"], self.df_2["y"], label="Arquivo 2", s=50)
                if self.df_1 is not None or self.df_2 is not None:
                    self.ax.legend()

            elif tipo == "histograma":
                valores = []
                if self.df_1 is not None:
                    valores.extend(self.df_1["y"].tolist())
                if self.df_2 is not None:
                    valores.extend(self.df_2["y"].tolist())
                self.ax.hist(valores, bins=10, color="steelblue", edgecolor="black")

            else:
                if self.df_1 is not None:
                    self.ax.plot(self.df_1["x"], self.df_1["y"], marker="o", linewidth=2, label="Dados")
                if self.df_2 is not None:
                    self.ax.plot(self.df_2["x"], self.df_2["y"], marker="s", linewidth=2, label="Arquivo 2")
                if self.df_1 is not None or self.df_2 is not None:
                    self.ax.legend()

            self.ax.set_title(self.title_var.get())
            self.ax.set_xlabel(self.x_label_var.get())
            self.ax.set_ylabel(self.y_label_var.get())
            self.ax.grid(True, linestyle="--", alpha=0.5)
            self.fig.tight_layout()
            self.canvas.draw()
            self.status_var.set(f"Gráfico {tipo} gerado com sucesso.")
        except Exception as exc:
            self.status_var.set(f"Erro: {exc}")
            self.ax.clear()
            self.ax.set_title("Erro ao carregar dados")
            self.ax.text(0.5, 0.5, str(exc), ha="center", va="center", transform=self.ax.transAxes)
            self.fig.tight_layout()
            self.canvas.draw()

    def _salvar_imagem(self) -> None:
        caminho = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("PDF", "*.pdf"),
                ("SVG", "*.svg"),
            ],
        )
        if not caminho:
            return

        try:
            self.fig.savefig(caminho, dpi=300, bbox_inches="tight")
            self.status_var.set(f"Imagem salva em: {os.path.basename(caminho)}")
        except Exception as exc:
            self.status_var.set(f"Erro ao salvar: {exc}")


def main() -> None:
    app = AppGraficoAvancado()
    app.mainloop()


if __name__ == "__main__":
    main()
