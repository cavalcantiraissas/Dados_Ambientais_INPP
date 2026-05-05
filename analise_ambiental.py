# IMPORTAÇÕES 
import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import seaborn as sns
from pathlib import Path

# Diretório de saída para figuras
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# DADOS BRUTOS 
RAW_CSV = """data,temperatura_c,nivel_rio_m,ndvi
2025-01-01,32.5,4.2,0.65
2025-01-02,33.1,4.3,0.67
2025-01-03,34.0,,0.66
2025-01-04,35.2,4.5,
2025-01-05,36.0,4.7,0.70
2025-01-06,35.5,4.8,0.72
2025-01-07,34.8,,0.71
2025-01-08,33.9,4.6,0.69
2025-01-09,32.7,4.4,
2025-01-10,31.8,4.3,0.66
"""

# LEITURA DOS DADOS 
print("=" * 60)
print("  ANÁLISE DE DADOS AMBIENTAIS")
print("=" * 60)

df_raw = pd.read_csv(
    io.StringIO(RAW_CSV),
    parse_dates=["data"],   # converte a coluna 'data' para datetime
    skipinitialspace=True   # ignora espaços após vírgulas
)

print("\n Dados brutos (antes do tratamento):")
print(df_raw.to_string(index=False))
print(f"\n Valores ausentes detectados:\n{df_raw.isnull().sum()}")

# TRATAMENTO DE VALORES AUSENTES
# Estratégia: interpolação linear por data.
#
# Justificativa:
#   • Os dados são uma série temporal com intervalos regulares de 1 dia.
#   • Remover linhas eliminaria observações válidas nas outras colunas.
#   • A interpolação linear é conservadora e adequada para séries
#     ambientais contínuas (temperatura, nível de rio, NDVI).
#   • Alternativa descartada: média global — ignora tendências locais.

df = df_raw.copy()
df = df.sort_values("data").reset_index(drop=True)

# Interpolação coluna a coluna (método linear, limite = 2 dias consecutivos)
for col in ["temperatura_c", "nivel_rio_m", "ndvi"]:
    df[col] = df[col].interpolate(method="linear", limit=2)

# Garantir tipos corretos
df["temperatura_c"] = df["temperatura_c"].round(2)
df["nivel_rio_m"]   = df["nivel_rio_m"].round(2)
df["ndvi"]          = df["ndvi"].round(3)

print("\n Dados após tratamento (interpolação linear):")
print(df.to_string(index=False))
print(f"\n Valores ausentes restantes:\n{df.isnull().sum()}")

# ESTATÍSTICAS BÁSICAS
stats = df[["temperatura_c", "nivel_rio_m", "ndvi"]].describe().T

print("\n Estatísticas descritivas completas:")
print(stats.round(4).to_string())

media_temp  = df["temperatura_c"].mean()
media_rio   = df["nivel_rio_m"].mean()
media_ndvi  = df["ndvi"].mean()

print("\n Médias principais:")
print(f"   • Temperatura média : {media_temp:.2f} °C")
print(f"   • Nível do rio médio: {media_rio:.2f} m")
print(f"   • NDVI médio        : {media_ndvi:.4f}")

# PALETA E ESTILO
PALETTE = {
    "temp" : "#E05C5C",   # vermelho suave
    "rio"  : "#4A90C4",   # azul
    "ndvi" : "#5BAD6F",   # verde
    "grid" : "#E8E8E8",
    "bg"   : "#FAFAFA",
}

sns.set_theme(style="whitegrid", font="DejaVu Sans")
plt.rcParams.update({
    "figure.facecolor": PALETTE["bg"],
    "axes.facecolor"  : PALETTE["bg"],
    "axes.spines.top" : False,
    "axes.spines.right": False,
    "axes.grid"       : True,
    "grid.color"      : PALETTE["grid"],
    "grid.linewidth"  : 0.8,
})

date_fmt = mdates.DateFormatter("%d/%m")

# GRÁFICO 1 — Painel triplo (série temporal) ─────────────
fig = plt.figure(figsize=(14, 10), facecolor=PALETTE["bg"])
fig.suptitle(
    "Monitoramento Ambiental — Janeiro 2025",
    fontsize=16, fontweight="bold", y=0.98, color="#333333"
)
gs = gridspec.GridSpec(3, 1, hspace=0.55)

# Temperatura 
ax1 = fig.add_subplot(gs[0])
ax1.plot(df["data"], df["temperatura_c"],
         color=PALETTE["temp"], linewidth=2.5, marker="o",
         markersize=7, label="Temperatura (°C)", zorder=3)
ax1.fill_between(df["data"], df["temperatura_c"],
                 alpha=0.15, color=PALETTE["temp"])
ax1.axhline(media_temp, color=PALETTE["temp"], linestyle="--",
            linewidth=1.2, label=f"Média: {media_temp:.2f} °C")
ax1.set_ylabel("Temperatura (°C)", fontsize=11)
ax1.set_title("Evolução da Temperatura", fontsize=12, fontweight="bold")
ax1.xaxis.set_major_formatter(date_fmt)
ax1.legend(fontsize=9, loc="upper right")
ax1.tick_params(axis="x", rotation=30)

# Nível do Rio
ax2 = fig.add_subplot(gs[1])
ax2.plot(df["data"], df["nivel_rio_m"],
         color=PALETTE["rio"], linewidth=2.5, marker="s",
         markersize=7, label="Nível do Rio (m)", zorder=3)
ax2.fill_between(df["data"], df["nivel_rio_m"],
                 alpha=0.15, color=PALETTE["rio"])
ax2.axhline(media_rio, color=PALETTE["rio"], linestyle="--",
            linewidth=1.2, label=f"Média: {media_rio:.2f} m")
ax2.set_ylabel("Nível do Rio (m)", fontsize=11)
ax2.set_title("Evolução do Nível do Rio", fontsize=12, fontweight="bold")
ax2.xaxis.set_major_formatter(date_fmt)
ax2.legend(fontsize=9, loc="upper left")
ax2.tick_params(axis="x", rotation=30)

# NDVI
ax3 = fig.add_subplot(gs[2])
ax3.plot(df["data"], df["ndvi"],
         color=PALETTE["ndvi"], linewidth=2.5, marker="^",
         markersize=7, label="NDVI", zorder=3)
ax3.fill_between(df["data"], df["ndvi"],
                 alpha=0.15, color=PALETTE["ndvi"])
ax3.axhline(media_ndvi, color=PALETTE["ndvi"], linestyle="--",
            linewidth=1.2, label=f"Média: {media_ndvi:.4f}")
ax3.set_ylabel("NDVI", fontsize=11)
ax3.set_xlabel("Data", fontsize=11)
ax3.set_title("Evolução do NDVI (Índice de Vegetação)", fontsize=12, fontweight="bold")
ax3.xaxis.set_major_formatter(date_fmt)
ax3.legend(fontsize=9, loc="upper left")
ax3.tick_params(axis="x", rotation=30)

path_g1 = OUTPUT_DIR / "grafico1_series_temporais.png"
fig.savefig(path_g1, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\n Gráfico 1 salvo → {path_g1}")

# GRÁFICO 2 — Correlação + Distribuições
fig2, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor=PALETTE["bg"])
fig2.suptitle(
    "Distribuição e Correlação das Variáveis Ambientais",
    fontsize=14, fontweight="bold", y=1.02, color="#333333"
)

pairs = [
    ("temperatura_c", "nivel_rio_m",
     "Temperatura (°C)", "Nível do Rio (m)",
     PALETTE["temp"], PALETTE["rio"]),
    ("temperatura_c", "ndvi",
     "Temperatura (°C)", "NDVI",
     PALETTE["temp"], PALETTE["ndvi"]),
    ("nivel_rio_m", "ndvi",
     "Nível do Rio (m)", "NDVI",
     PALETTE["rio"], PALETTE["ndvi"]),
]

for ax, (x_col, y_col, x_lbl, y_lbl, cx, cy) in zip(axes, pairs):
    ax.scatter(df[x_col], df[y_col],
               color=cx, edgecolors=cy, linewidths=1.5,
               s=90, zorder=3, alpha=0.85)
    # linha de tendência
    z = pd.DataFrame({"x": df[x_col], "y": df[y_col]}).dropna()
    if len(z) > 1:
        coef = pd.Series(z["x"]).corr(pd.Series(z["y"]))
        fit  = pd.Series(z["x"]).rank()  # usado só para referência visual
        m, b = pd.np.polyfit(z["x"], z["y"], 1) if hasattr(pd, "np") \
               else __import__("numpy").polyfit(z["x"], z["y"], 1)
        xs = pd.Series([z["x"].min(), z["x"].max()])
        ax.plot(xs, m * xs + b, "--", color="#888", linewidth=1.3,
                label=f"r = {coef:.2f}")
    ax.set_xlabel(x_lbl, fontsize=10)
    ax.set_ylabel(y_lbl, fontsize=10)
    ax.set_title(f"{x_lbl} × {y_lbl}", fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_facecolor(PALETTE["bg"])

fig2.tight_layout()
path_g2 = OUTPUT_DIR / "grafico2_correlacoes.png"
fig2.savefig(path_g2, dpi=150, bbox_inches="tight")
plt.close(fig2)
print(f" Gráfico 2 salvo → {path_g2}")

# GRÁFICO 3 — Heatmap de correlação 
fig3, ax = plt.subplots(figsize=(7, 5), facecolor=PALETTE["bg"])
corr = df[["temperatura_c", "nivel_rio_m", "ndvi"]].corr()
mask = pd.DataFrame(False, index=corr.index, columns=corr.columns)

sns.heatmap(
    corr, ax=ax,
    annot=True, fmt=".2f", annot_kws={"size": 13},
    cmap="RdYlGn", vmin=-1, vmax=1,
    linewidths=0.5, linecolor="white",
    cbar_kws={"shrink": 0.8, "label": "Coeficiente de Pearson"}
)
ax.set_title("Matriz de Correlação — Variáveis Ambientais",
             fontsize=13, fontweight="bold", pad=14)
ax.set_xticklabels(["Temperatura (°C)", "Nível do Rio (m)", "NDVI"],
                   rotation=20, ha="right", fontsize=10)
ax.set_yticklabels(["Temperatura (°C)", "Nível do Rio (m)", "NDVI"],
                   rotation=0, fontsize=10)

path_g3 = OUTPUT_DIR / "grafico3_heatmap_correlacao.png"
fig3.savefig(path_g3, dpi=150, bbox_inches="tight")
plt.close(fig3)
print(f" Gráfico 3 salvo → {path_g3}")

# EXPORTAR DADOS TRATADOS 
path_csv = OUTPUT_DIR / "dados_tratados.csv"
df.to_csv(path_csv, index=False, date_format="%Y-%m-%d")
print(f" CSV tratado salvo → {path_csv}")

print("\n Pipeline concluído com sucesso!")
print("=" * 60)
