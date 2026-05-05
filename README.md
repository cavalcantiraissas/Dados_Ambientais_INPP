# Análise de Dados Ambientais

Projeto de análise de dados ambientais desenvolvido em Python, cobrindo as etapas de leitura, tratamento de valores ausentes, cálculo de estatísticas descritivas e visualização de séries temporais.

---

## Estrutura do Projeto

```
.
├── analise_ambiental.py
├── README.md
└── output/
    ├── dados_tratados.csv
    ├── grafico1_series_temporais.png
    ├── grafico2_correlacoes.png
    └── grafico3_heatmap_correlacao.png
```

---

## Requisitos

- Python 3.8 ou superior
- pip

Bibliotecas utilizadas:

| Biblioteca   | Finalidade                                              |
|--------------|---------------------------------------------------------|
| pandas       | Leitura, tratamento e estatísticas dos dados            |
| matplotlib   | Construção dos gráficos de séries temporais e dispersão |
| seaborn      | Heatmap da matriz de correlação                         |

---

## Instalação e Execução

**1. Instalar as dependências:**

```bash
pip install pandas matplotlib seaborn
```

**2. Executar o script:**

```bash
python3 analise_ambiental.py
```

Os arquivos de saída serão gerados automaticamente na pasta `output/`.

---

## Tratamento de Dados Ausentes

O dataset original continha 4 valores ausentes distribuídos em duas colunas:

| Coluna        | Valores ausentes | Datas afetadas         |
|---------------|-----------------|------------------------|
| nivel_rio_m   | 2               | 2025-01-03, 2025-01-07 |
| ndvi          | 2               | 2025-01-04, 2025-01-09 |

**Estratégia adotada: interpolação linear.**

Como os dados formam uma série temporal com intervalo regular de um dia, a interpolação linear é a abordagem mais adequada por dois motivos principais. Primeiro, preserva todas as 10 observações, evitando a perda de dados válidos presentes nas demais colunas da mesma linha. Segundo, respeita a tendência local da série, produzindo estimativas mais precisas do que a substituição pela média global, que ignora a variação temporal.

Um parâmetro `limit=2` foi aplicado para evitar extrapolação em lacunas longas.

---

## Resultados

### Estatísticas Descritivas

|               | count | mean    | std    | min   | 25%    | 50%    | 75%    | max   |
|---------------|-------|---------|--------|-------|--------|--------|--------|-------|
| temperatura_c | 10    | 33.9500 | 1.4105 | 31.80 | 32.800 | 33.950 | 35.100 | 36.00 |
| nivel_rio_m   | 10    | 4.4900  | 0.2025 | 4.20  | 4.3250 | 4.4500 | 4.6750 | 4.80  |
| ndvi          | 10    | 0.6815  | 0.0231 | 0.65  | 0.6625 | 0.6775 | 0.6975 | 0.72  |

### Médias Principais

| Variável     | Média    |
|--------------|----------|
| Temperatura  | 33.95 °C |
| Nível do Rio | 4.49 m   |
| NDVI         | 0.6815   |

### Correlações (Pearson)

| Par de variáveis               | r    | Interpretação         |
|--------------------------------|------|-----------------------|
| Temperatura x Nível do Rio     | 0.85 | Correlação forte      |
| Temperatura x NDVI             | 0.78 | Correlação forte      |
| Nível do Rio x NDVI            | 0.97 | Correlação muito forte|

A correlação de 0.97 entre nível do rio e NDVI indica que o aumento da disponibilidade hídrica está fortemente associado ao crescimento da vegetação no período analisado. A temperatura também apresenta correlação positiva com ambas as variáveis, sugerindo que o aquecimento no início do período favoreceu tanto o volume do rio quanto o desenvolvimento vegetal.

---

## Visualizações

**Gráfico 1 - Séries Temporais**
Painel com três subgráficos exibindo a evolução diária de temperatura, nível do rio e NDVI entre 01/01 e 10/01/2025. Cada painel inclui a linha de média como referência visual. A variação de temperatura foi de 31.8 °C a 36.0 °C, com pico em 05/01. O nível do rio variou entre 4.2 m e 4.8 m, com pico em 06/01.

**Gráfico 2 - Dispersão entre Variáveis**
Três gráficos de dispersão com linha de tendência (mínimos quadrados) e coeficiente de Pearson, analisando os pares: Temperatura x Nível do Rio (r=0.85), Temperatura x NDVI (r=0.78) e Nível do Rio x NDVI (r=0.97).

**Gráfico 3 - Matriz de Correlação**
Heatmap com escala de cores RdYlGn (vermelho para correlações negativas, verde para positivas) exibindo os coeficientes de Pearson entre todas as variáveis. Todas as correlações identificadas são positivas e de magnitude elevada.

---

## Decisões Técnicas

- **pandas** foi escolhido por oferecer o método `interpolate()` nativamente integrado ao índice temporal, simplificando o tratamento da série.
- **matplotlib com GridSpec** permitiu compor o painel triplo com controle preciso de proporções entre subgráficos.
- **seaborn** foi utilizado exclusivamente para o heatmap, onde sua integração com matplotlib e o suporte nativo a anotações e paletas divergentes representam vantagem sobre soluções manuais.
- O estilo visual foi centralizado em um dicionário de paleta (`PALETTE`), facilitando manutenção e consistência entre os gráficos.
- O uso de `pathlib.Path` garante compatibilidade de caminhos entre sistemas operacionais (Windows, macOS e Linux).
