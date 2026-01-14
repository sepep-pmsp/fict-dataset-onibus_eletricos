import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import time
import numpy as np
import streamlit_mermaid as stmd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from utils.load_csv import load_csv
from utils.load_shp import load_shp


 
# Layout
st.set_page_config(layout="wide")
 
 
 
# Sidebar
with st.sidebar:
    st.markdown("<h3 style='color: black;'>Sobre</h3>", unsafe_allow_html=True)
 
    st.markdown("""<div style = 'text-align: justify; color: black;' >
                    Este dashboard faz parte do projeto da Prefeitura Municipal de São Paulo com a Bloomberg.
                    As visualizações apresentam informações sobre o transporte público a ônibus como frotas, trajetos e emissões de poluentes.
                    </div><br>""",
                unsafe_allow_html=True)
 
    @st.dialog("Metodologia")
    def metodologia():
        columns = st.columns(2)
        with columns[0]:
            stmd.st_mermaid("""
                        %%{ init: {
                            'theme': 'base',
                            'themeVariables': {
                                'fontSize': '20px',
                                'primaryColor': '#F1EBDD'}}}%%
                                        
                        flowchart TD
                        A[Extração dos limites<br/>administrativos<br/>dos distritos<br/>da cidade] --> B[Extração dos dados<br/>da API do Olho Vivo]
                        B --> C[Tratamento dos dados]
                        C --> D[Cálculo das emissões<br/>de poluentes<br/>e da distância percorrida<br/>por ônibus]
                        D --> E[Agregação dos dados<br/>por distrito]
                        E --> F[Visualização dos dados]
                        F --> G[Elaboração do dashboard<br/>interativo]
                        """, height=540, width=170)
        with columns[1]:
            st.markdown(
            """<div style='text-align: justify; color: black;'>
            A metodologia do projeto foi organizada em etapas sequenciais,
            da extração dos limites administrativos dos distritos até a construção
            do dashboard interativo em Streamlit. Os dados da API do Olho Vivo foram extraídos,
            tratados e estruturados em Python, com uso das bibliotecas para manipulação e visualização de dados.
            Após processos de limpeza, agregação, cruzamento e cálculo de indicadores,
            estimaram-se emissões de poluentes e distâncias percorridas por ônibus, organizadas por distrito.
            Todo o fluxo utilizou ferramentas open source, garantindo
            transparência, reprodutibilidade e livre acesso no projeto.
            </div>""",
            unsafe_allow_html=True
        )


    st.markdown("<h3 style='color: black;'>Metodologia</h3>", unsafe_allow_html=True)
    if st.button("Acessar"):
        metodologia()

    st.markdown("<br>", unsafe_allow_html=True)
 
    with st.expander("Fonte"):
        st.markdown("""<div style = 'text-align: justify; color: black;' >
                    SPTrans - API do Olho Vivo, 2025.
                    </div> <br>""",
                    unsafe_allow_html=True)
 
 

# CSS para Header e Footer
st.markdown("""
<style>
    /* HEADER FIXO */
    .custom-header {
        position: fixed;
        top: 2.5rem;
        left: 0;
        width: 100%;
        background-color: #F1EBDD;
        z-index: 1000;
        padding: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        text-align: center;
    }
 
    /* Compensar espaço do header no conteúdo */
    .main-content {
        padding-top: 6rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
 
    /* FOOTER FIXO */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #F1EBDD;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: medium;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    .footer img {
        height: 30px;
        vertical-align: middle;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)
 
 
 
# Header
st.markdown("""
<div class="custom-header">
    <h1 style='color: black; margin: 0;'>Dashboard - Protótipo</h1>
    <p style='font-size: 1.5rem; color: black; margin: 0;'>PMSP / Bloomberg</p>
</div>
""", unsafe_allow_html=True)



# Footer
st.markdown("""
<div class="footer">
    <img src="https://prefeitura.sp.gov.br/documents/34276/25188012/logo_PrefSP__horizontal_fundo+claro+%281%29.png">
    Copyleft 2025 | Prefeitura de São Paulo © 2025
</div>
""", unsafe_allow_html=True)
 
 
 
st.markdown("<br>", unsafe_allow_html=True)
 
 
 
# Conteúdo
st.markdown('<div class="main-content">', unsafe_allow_html=True)
 
 
 
# Carregar dados
@st.cache_data
def carregar_dados():
    gdf_final = load_csv("gdf_final.csv")
    df_trips = load_csv("df_trips.csv")
    distritos_final = load_shp("distritos_final.shp")
    df_posicoes = load_csv("df_posicoes_dagster.csv")
    sim_dagster = load_csv('calculo-emissao-poluentes-diario_2026-01-01_silver.csv')
    pop_afetada_onibus = load_csv('pop_afetada_onibus.csv')
    pop_afetada_linha = load_csv('pop_afetada_linha.csv')
    gdf = load_shp('pop_afetada_distritos.shp')
    return gdf_final, df_trips, distritos_final, df_posicoes, sim_dagster, pop_afetada_onibus, pop_afetada_linha, gdf

gdf_final, df_trips, distritos_final, df_posicoes, sim_dagster, pop_afetada_onibus, pop_afetada_linha, gdf = carregar_dados()
 
 
# ----- GRÁFICOS 1 -----
st.markdown("## Sobre os ônibus")


df_unique = gdf_final.drop_duplicates(subset="id_onibus")


# Tipo de ônibus
contagem_eletrico = df_unique["is_eletrico"].value_counts().reset_index()
contagem_eletrico.columns = ["Tipo de ônibus", "Quantidade"]
mapeamento = {False: "Não elétrico", True: "Elétrico"}
contagem_eletrico["Tipo de ônibus"] = contagem_eletrico["Tipo de ônibus"].map(mapeamento)
total_onibus = df_unique["id_onibus"].nunique()

fig1 = px.pie(
    contagem_eletrico,
    values="Quantidade",
    names="Tipo de ônibus",
    title="Distribuição por tipo de ônibus",
    color="Tipo de ônibus",
    color_discrete_map={
        "Não elétrico": "#d53e4f",
        "Elétrico": "#00cc96"
    },
    hole=0.5
)
fig1.update_traces(textinfo="none", hovertemplate="%{percent}")
fig1.add_annotation(
    text=f"<b>Total:<br>{total_onibus}</b>",
    x=0.5, y=0.5,
    font=dict(size=20, color="black"),
    showarrow=False
)
fig1.update_layout(
    legend=dict(orientation="v", font=dict(size=14, color="black"),
                yanchor="middle", y=0.5, xanchor="left", x=1.05),
    hoverlabel=dict(font=dict(color="black"), bgcolor="white")
)


# Modelos de ônibus elétricos
onibus_eletricos = df_unique[df_unique["is_eletrico"] == True]
contagem_modelo = onibus_eletricos["modelo"].value_counts().reset_index()
contagem_modelo.columns = ["Modelo de ônibus", "Quantidade"]
total_onibus_eletricos = onibus_eletricos["id_onibus"].nunique()

fig2 = px.pie(
    contagem_modelo,
    values="Quantidade",
    names="Modelo de ônibus",
    title="Distribuição de ônibus elétricos por modelo de ônibus",
    hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig2.update_traces(textinfo="none", hovertemplate="%{percent}")
fig2.add_annotation(
    text=f"<b>Total:<br>{total_onibus_eletricos}</b>",
    x=0.5, y=0.5,
    font=dict(size=20, color="black"),
    showarrow=False
)
fig2.update_layout(
    legend=dict(orientation="v", font=dict(size=14, color="black"),
                yanchor="middle", y=0.5, xanchor="left", x=1.15),
    hoverlabel=dict(font=dict(color="black"), bgcolor="white")
)


with st.expander("Clique para as visualizações"):
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)
 
 
 
st.markdown("<br>", unsafe_allow_html=True)
 
 
 
# ----- GRÁFICOS 2 -----
st.markdown("## Sobre as emissões de CO₂")
gdf_final["momento_inicial"] = pd.to_datetime(gdf_final["momento_inicial"])
gdf_final["hora_min"] = gdf_final["momento_inicial"].dt.strftime("%H:%M")
df_eletricos = gdf_final[gdf_final["is_eletrico"] == True]
df_nao_eletricos = gdf_final[gdf_final["is_eletrico"] == False]
 
emissoes = df_nao_eletricos.groupby("hora_min")["emissao_co2"].sum().cumsum().sort_index().reset_index()
emissoes.columns = ["Horário do dia", "Emissões de CO₂ (t)"]
 
emissoes_evitadas = df_eletricos.groupby("hora_min")["emissao_co2"].sum().cumsum().sort_index().reset_index()
emissoes_evitadas.columns = ["Horário do dia", "Emissões de CO₂ (t)"]
 
 
# Emissões acumuladas
fig3 = px.line(emissoes, x="Horário do dia", y="Emissões de CO₂ (t)", markers=True,
               title="Emissões de CO₂ acumuladas ao longo do dia - ônibus não elétricos")
fig3.update_traces(line_color="#d53e4f", hovertemplate="Emissões: %{y:.5f} (t)<extra></extra>",
                   hoverlabel=dict(font_color="black", bgcolor="white"))
fig3.update_layout(plot_bgcolor="white",
                   xaxis=dict(title_font_color="black", tickfont_color="black", tickangle=45),
                   yaxis=dict(title_font_color="black", tickfont_color="black"))
 
 
# Emissões evitadas
fig4 = px.line(emissoes_evitadas, x="Horário do dia", y="Emissões de CO₂ (t)", markers=True,
               title="Emissões de CO₂ evitadas ao longo do dia - ônibus elétricos")
fig4.update_traces(line_color="#00cc96", hovertemplate="Emissões: %{y:.5f} (t)<extra></extra>",
                   hoverlabel=dict(font_color="black", bgcolor="white"))
fig4.update_layout(plot_bgcolor="white",
                   xaxis=dict(title_font_color="black", tickfont_color="black", tickangle=45),
                   yaxis=dict(title_font_color="black", tickfont_color="black"))
 
with st.expander("Clique para as visualizações"):
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig3, use_container_width=True)
    col2.plotly_chart(fig4, use_container_width=True)
 
 
 
st.markdown("<br>", unsafe_allow_html=True)
 
 
 
# ----- MAPAS POR DISTRITO -----
st.markdown("## Mapas coropléticos por distrito")
 
distritos_final["emissao_nao_eletricos"] = np.where(
    distritos_final["is_eletric"] == False,
    distritos_final["emissao_co"],
    0
)
 
distritos_final["emissao_eletricos"] = np.where(
    distritos_final["is_eletric"] == True,
    distritos_final["emissao_co"],
    0
)
 
distritos_final = distritos_final.set_crs(epsg=31983, allow_override=True)
distritos_final = distritos_final.to_crs(epsg=4326)
 
abas = st.tabs([
    "Distância percorrida",
    "Emissão de CO₂ - ônibus não elétricos",
    "Emissão de CO₂ evitada - ônibus elétricos"
])
 
custom_cols = ["nm_distrit"]
 
 
# Distância
with abas[0]:
    with st.expander("Clique para a visualização"):
        fig_dist = px.choropleth_mapbox(
            distritos_final,
            geojson=distritos_final.geometry.__geo_interface__,
            locations=distritos_final.index,
            color="distancia",
            color_continuous_scale="Blues",
            range_color=[
                distritos_final["distancia"].min(),
                distritos_final["distancia"].max()
            ],
            mapbox_style="carto-positron",
            center={"lat": -23.7, "lon": -46.63},
            zoom=9,
            opacity=0.8,
            custom_data=custom_cols + ["distancia"]
        )
        fig_dist.update_traces(
            hovertemplate="<b>Distrito</b>: %{customdata[0]}<br>Distância: %{customdata[1]:.0f} (km)<extra></extra>",
            hoverlabel=dict(font=dict(color="black"), bgcolor="white"
        ))
        fig_dist.update_coloraxes(colorbar_title="Distância (km)", colorbar_title_side="right",
                                  colorbar_title_font=dict(color="black"),
                                  colorbar_tickfont=dict(color="black"))
        fig_dist.update_layout(margin={"r":300,"t":0,"l":300,"b":0}, height=600)
        st.plotly_chart(fig_dist, use_container_width=True)
 
 
# Emissão não elétricos
with abas[1]:
    with st.expander("Clique para a visualização"):
        fig_nao = px.choropleth_mapbox(
            distritos_final,
            geojson=distritos_final.geometry.__geo_interface__,
            locations=distritos_final.index,
            color="emissao_nao_eletricos",
            color_continuous_scale="Reds",
            range_color=[
                distritos_final["emissao_nao_eletricos"].min(),
                distritos_final["emissao_nao_eletricos"].max()
            ],
            mapbox_style="carto-positron",
            center={"lat": -23.7, "lon": -46.63},
            zoom=9,
            opacity=0.8,
            custom_data=custom_cols + ["emissao_nao_eletricos"]
        )
        fig_nao.update_traces(
            hovertemplate="<b>Distrito</b>: %{customdata[0]}<br>Emissão: %{customdata[1]:,.5f} (t)<extra></extra>",
            hoverlabel=dict(font=dict(color="black"), bgcolor="white"
        ))
        fig_nao.update_coloraxes(colorbar_title="Emissão de CO₂ (t)", colorbar_title_side="right",
                                 colorbar_title_font=dict(color="black"),
                                 colorbar_tickfont=dict(color="black"))
        fig_nao.update_layout(margin={"r":300,"t":0,"l":300,"b":0}, height=600)
        st.plotly_chart(fig_nao, use_container_width=True)
 
 
# Emissão elétricos
with abas[2]:
    with st.expander("Clique para a visualização"):
        fig_ele = px.choropleth_mapbox(
            distritos_final,
            geojson=distritos_final.geometry.__geo_interface__,
            locations=distritos_final.index,
            color="emissao_eletricos",
            color_continuous_scale="Greens",
            range_color=[
                distritos_final["emissao_eletricos"].min(),
                distritos_final["emissao_eletricos"].max()
            ],
            mapbox_style="carto-positron",
            center={"lat": -23.7, "lon": -46.63},
            zoom=9,
            opacity=0.8,
            custom_data=custom_cols + ["emissao_eletricos"]
        )
        fig_ele.update_traces(
            hovertemplate="<b>Distrito</b>: %{customdata[0]}<br>Emissão evitada: %{customdata[1]:,.5f} (t)<extra></extra>",
            hoverlabel=dict(font=dict(color="black"), bgcolor="white"
        ))
        fig_ele.update_coloraxes(colorbar_title="Emissão de CO₂ evitada (t)", colorbar_title_side="right",
                                 colorbar_title_font=dict(color="black"),
                                 colorbar_tickfont=dict(color="black"))
        fig_ele.update_layout(margin={"r":300,"t":0,"l":300,"b":0}, height=600)
        st.plotly_chart(fig_ele, use_container_width=True)
 
 
 
st.markdown("<br>", unsafe_allow_html=True)



# --- IMPACTO SAÚDE --- #

st.markdown("## Impacto na saúde da população")

# =========================
# POPULAÇÃO AFETADA POR ÔNIBUS
# =========================
top10_onibus = (
    pop_afetada_onibus
    .sort_values("pop_buffer", ascending=False)
    .head(10)
)

top10_onibus["onibus_cat"] = top10_onibus["cd_onibus"].astype(str)
ordem_onibus = top10_onibus["onibus_cat"].tolist()[::-1]

fig_onibus = go.Figure()

fig_onibus.add_bar(
    x=top10_onibus["pop_buffer"],
    y=top10_onibus["onibus_cat"],
    orientation="h",
    marker=dict(color="#1f77b4"),
    hovertemplate=(
        "<b>Ônibus:</b> %{y}<br>"
        "<b>População:</b> %{x:.0f}<extra></extra>"
    )
)

fig_onibus.update_layout(
    title=dict(
        text="Top 10 ônibus a diesel com maior população potencialmente afetada",
        font=dict(size=18, weight="bold", color="black")
    ),
    xaxis=dict(
        title="População potencialmente afetada",
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.25)",
        griddash="dash",
        range=[0, top10_onibus["pop_buffer"].max() * 1.1]
    ),
    yaxis=dict(
        title="Código do ônibus",
        tickfont=dict(color="black"),
        type="category",
        categoryorder="array",
        categoryarray=ordem_onibus
    ),
    xaxis_title_font=dict(color="black"),
    yaxis_title_font=dict(color="black"),
    plot_bgcolor="white",
    font=dict(size=13, color="black"),
    bargap=0.25,
    height=520,
    margin=dict(l=90, r=60, t=70, b=50)
)

# =========================
# POPULAÇÃO AFETADA POR LINHA
# =========================
top10_linha = (
    pop_afetada_linha
    .sort_values("pop_buffer", ascending=False)
    .head(10)
)

top10_linha["linha_cat"] = top10_linha["nm_linha"].astype(str)
ordem_linha = top10_linha["linha_cat"].tolist()[::-1]

fig_linha = go.Figure()

fig_linha.add_bar(
    x=top10_linha["pop_buffer"],
    y=top10_linha["linha_cat"],
    orientation="h",
    marker=dict(color="#1f77b4"),
    hovertemplate=(
        "<b>Linha:</b> %{y}<br>"
        "<b>População:</b> %{x:.0f}<extra></extra>"
    )
)

fig_linha.update_layout(
    title=dict(
        text="Top 10 linhas de ônibus a diesel com maior população potencialmente afetada",
        font=dict(size=18, weight="bold", color="black")
    ),
    xaxis=dict(
        title="População potencialmente afetada",
        tickfont=dict(color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.25)",
        griddash="dash",
        range=[0, top10_linha["pop_buffer"].max() * 1.1]
    ),
    yaxis=dict(
        title="Linha de ônibus",
        tickfont=dict(color="black"),
        type="category",
        categoryorder="array",
        categoryarray=ordem_linha
    ),
    xaxis_title_font=dict(color="black"),
    yaxis_title_font=dict(color="black"),
    plot_bgcolor="white",
    font=dict(size=13, color="black"),
    bargap=0.25,
    height=520,
    margin=dict(l=120, r=60, t=70, b=50)
)

# =========================
# MAPA
# =========================
gdf = gdf.set_crs(epsg=31983, allow_override=True)
gdf = gdf.to_crs(epsg=4326)

fig_mapa_saude = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry.__geo_interface__,
    locations=gdf.index,
    color="pop_buffer",
    color_continuous_scale="OrRd",
    range_color=[gdf["pop_buffer"].min(), gdf["pop_buffer"].max()],
    mapbox_style="carto-positron",
    center={"lat": -23.7, "lon": -46.63},
    zoom=9,
    opacity=0.8,
    custom_data=["nm_distrit", "pop_buffer"]
)

fig_mapa_saude.update_traces(
    hovertemplate=(
        "<b>Distrito:</b> %{customdata[0]}<br>"
        "<b>População potencialmente afetada:</b> %{customdata[1]:.0f}"
        "<extra></extra>"
    ),
    hoverlabel=dict(font=dict(color="black"), bgcolor="white")
)

fig_mapa_saude.update_coloraxes(
    colorbar=dict(
        title=dict(
            text="População potencialmente afetada",
            side="right",
            font=dict(color="black")
        ),
        tickfont=dict(color="black")
    )
)

fig_mapa_saude.update_layout(
    title=dict(
        text="População potencialmente afetada por distrito",
        font=dict(size=18, weight="bold", color="black"),
        x=0.4
    ),
    margin={"r":300, "t":60, "l":300, "b":0},
    height=650
)

# =========================
# LAYOUT
# =========================
with st.expander("Clique para as visualizações"):
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_onibus, use_container_width=True)
    col2.plotly_chart(fig_linha, use_container_width=True)

    st.plotly_chart(fig_mapa_saude, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)



# ----- SIMULAÇÃO DE EMISSÕES EVITADAS (MONTE CARLO) -----

st.markdown("## Simulação de Monte Carlo")

# Converter kg para toneladas
sim_dagster[['emissao_co2', 'emissao_nox', 'emissao_mp']] /= 1000  

POLUENTES = {
    "emissao_co2": "CO₂ (t/dia)",
    "emissao_nox": "NOx (t/dia)",
    "emissao_mp": "MP (t/dia)"
}


# ======================================================
# FUNÇÃO DE SIMULAÇÃO MONTE CARLO
# ======================================================
def sim_monte_carlo(
    sim_dagster,
    Y,
    poluentes,
    N=2000,
    dias=365
):

    resultados_diarios = {p: [] for p in poluentes}

    for _ in range(N):
        amostra = sim_dagster.sample(n=Y, replace=False)

        for p in poluentes:
            resultados_diarios[p].append(amostra[p].sum())

    for p in poluentes:
        resultados_diarios[p] = np.array(resultados_diarios[p])

    resultados_acumulados = {
        p: resultados_diarios[p] * dias
        for p in poluentes
    }

    impacto_medio = {
        p: resultados_diarios[p].mean()
        for p in poluentes
    }

    impacto_maximo = {
        p: sim_dagster.nlargest(Y, p)[p].sum()
        for p in poluentes
    }

    return {
        "Y": Y,
        "dias": dias,
        "impacto_medio_dia": impacto_medio,
        "impacto_maximo_dia": impacto_maximo,
        "impacto_medio_acumulado": {
            p: resultados_acumulados[p].mean()
            for p in poluentes
        },
        "resultados_diarios": resultados_diarios
    }


# ======================================================
# FUNÇÃO PARA ESTIMAR FROTA NECESSÁRIA (META POR POLUENTE)
# ======================================================
def estimar_frota_para_meta(
    sim_dagster,
    metas_por_poluente: dict,
    poluentes,
    N=2000,
    Y_min=1,
    Y_max=None,
    passo=1,
    percentil=75
):

    if Y_max is None:
        Y_max = len(sim_dagster)

    resultados = []

    for Y in range(Y_min, Y_max + 1, passo):

        sim = sim_monte_carlo(
            sim_dagster,
            Y,
            poluentes=poluentes,
            N=N,
            dias=1
        )

        pctl = {
            p: np.percentile(sim["resultados_diarios"][p], percentil)
            for p in poluentes
        }

        resultados.append({
            "Quantidade de ônibus elétricos": Y,
            **{f"{POLUENTES[p]} (P{percentil})": pctl[p] for p in poluentes}
        })

        if all(
            pctl[p] >= metas_por_poluente.get(p, 0)
            for p in poluentes
        ):
            break

    return pd.DataFrame(resultados)


# ======================================================
# INTERFACE STREAMLIT
# ======================================================
with st.expander("Clique para simular"):

    modo = st.radio(
        "Escolha o tipo de simulação:",
        [
            "Novos ônibus elétricos",
            "Emissões evitadas"
        ]
    )

    dias = st.number_input(
        "Período da projeção (em dias):",
        min_value=1,
        value=365,
        format="%d"
    )

    if modo == "Novos ônibus elétricos":

        Y = st.number_input(
            "Quantidade de novos ônibus elétricos:",
            min_value=1,
            max_value=len(sim_dagster),
            format="%d"
        )

        executar = st.button("Executar simulação")

    else:
        st.markdown("### Metas diárias de emissões evitadas (t/dia)")

        meta_por_poluente = {}

        for p, label in POLUENTES.items():
            meta_por_poluente[p] = st.number_input(
                f"{label}:",
                min_value=0.0,
                format="%.4f",
                key=f"meta_{p}"
            )

        executar = st.button("Estimar frota necessária")


    # ======================================================
    # EXECUÇÃO DA SIMULAÇÃO
    # ======================================================
    if executar:

        try:

            if modo == "Emissões evitadas":

                df_meta = estimar_frota_para_meta(
                    sim_dagster,
                    metas_por_poluente=meta_por_poluente,
                    poluentes=list(POLUENTES.keys())
                )

                Y = int(df_meta.iloc[-1]["Quantidade de ônibus elétricos"])

                metas_txt = ", ".join([
                    f"{POLUENTES[p]} ≥ {meta_por_poluente[p]:.4f} t/dia"
                    for p in POLUENTES
                    if meta_por_poluente[p] > 0
                ])

                st.success(
                    f"Para atingir as metas diárias de emissões evitadas "
                    f"({metas_txt}), estima-se a necessidade de "
                    f"**{Y} novos ônibus elétricos**, considerando "
                    f"75% dos cenários simulados."
                )

                st.dataframe(df_meta.round(5), use_container_width=True)

            resultado = sim_monte_carlo(
                sim_dagster,
                Y,
                poluentes=list(POLUENTES.keys()),
                dias=dias
            )

            # ----- MENSAGEM DE SUCESSO (NOVOS ÔNIBUS ELÉTRICOS) -----
            if modo == "Novos ônibus elétricos":

                impacto_txt = ", ".join([
                    f"**{resultado['impacto_medio_dia'][p]:.4f} t/dia** de {label.split('(')[0].strip()}"
                    for p, label in POLUENTES.items()
                ])

                st.success(
                    f"Com a incorporação de **{Y} novos ônibus elétricos**, "
                    f"estima-se um impacto médio diário de emissões evitadas de "
                    f"{impacto_txt}."
                )

            # ----- RESUMO -----
            resumo = {
                "Quantidade de ônibus elétricos": Y
            }

            for p, label in POLUENTES.items():
                resumo[f"{label} – média diária"] = resultado["impacto_medio_dia"][p]

                if modo == "Emissões evitadas":
                    resumo[f"{label} – P75 diário"] = np.percentile(
                        resultado["resultados_diarios"][p], 75
                    )

                resumo[f"{label} – cenário máximo"] = resultado["impacto_maximo_dia"][p]
                resumo[f"{label} – acumulado no período"] = resultado["impacto_medio_acumulado"][p]

            tabela_resumo = pd.DataFrame([resumo]).round(5)

            st.markdown("### Resumo da simulação")
            st.dataframe(tabela_resumo, use_container_width=True)

            # ----- PROJEÇÃO TEMPORAL -----
            for p, label in POLUENTES.items():

                df_proj = pd.DataFrame({
                    "Dias": range(1, dias + 1),
                    "Emissões evitadas (t)": (
                        resultado["impacto_medio_dia"][p]
                        * np.arange(1, dias + 1)
                    )
                })

                fig = px.line(
                    df_proj,
                    x="Dias",
                    y="Emissões evitadas (t)",
                    title=f"Projeção acumulada – {label}",
                    markers=True
                )

                fig.update_layout(plot_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)

            # ----- DISTRIBUIÇÕES -----
            for p, label in POLUENTES.items():

                densidade = gaussian_kde(resultado["resultados_diarios"][p])

                x_vals = np.linspace(
                    resultado["resultados_diarios"][p].min(),
                    resultado["resultados_diarios"][p].max(),
                    300
                )

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=densidade(x_vals),
                    mode="lines",
                    fill="tozeroy",
                    name=label
                ))

                fig.add_vline(
                    x=resultado["impacto_medio_dia"][p],
                    line_dash="dash",
                    annotation_text="Média"
                )

                if modo == "Emissões evitadas":
                    fig.add_vline(
                        x=np.percentile(resultado["resultados_diarios"][p], 75),
                        line_dash="dot",
                        annotation_text="P75"
                    )

                fig.update_layout(
                    title=f"Distribuição das emissões evitadas – {label}",
                    xaxis_title=label,
                    yaxis_title="Densidade",
                    plot_bgcolor="white"
                )

                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error(
                "Erro: a quantidade de ônibus selecionada excede o total disponível na frota a diesel."
            )



st.markdown("<br>", unsafe_allow_html=True)



# ----- MAPA TRAJETOS -----
st.markdown("## Mapa de trajeto dos ônibus")

# =========================
# PREPARAÇÃO DOS DADOS
# =========================
df_trips = df_trips[['coordinates', 'timestamps', 'is_eletrico']].copy()

df_trips['coordinates'] = df_trips['coordinates'].apply(eval)
df_trips['timestamps'] = df_trips['timestamps'].apply(eval)

df_trips["color"] = df_trips["is_eletrico"].apply(
    lambda x: [0, 255, 0] if x else [255, 0, 0]
)

max_time = max(df_trips['timestamps'].apply(max))

trail_length = 800
time_step = 80
frame_delay = 2


# =========================
# CONTROLE DE ESTADO
# =========================
if "animar_trajetos" not in st.session_state:
    st.session_state.animar_trajetos = False


# =========================
# BOTÃO
# =========================
col_left, col_center, col_right = st.columns([1, 5, 1])

with col_center:
    if st.button("Iniciar animação dos trajetos"):
        st.session_state.animar_trajetos = True


# =========================
# EXECUÇÃO DA ANIMAÇÃO
# =========================
if st.session_state.animar_trajetos:

    with col_center:
        map_placeholder = st.empty()

        current_time = 0
        while current_time <= max_time:

            trips_layer = pdk.Layer(
                "TripsLayer",
                data=df_trips,
                get_path="coordinates",
                get_timestamps="timestamps",
                get_color="color",
                opacity=0.8,
                width_min_pixels=5,
                rounded=True,
                trail_length=trail_length,
                current_time=current_time,
            )

            view_state = pdk.ViewState(
                latitude=-23.7,
                longitude=-46.63,
                zoom=10,
                pitch=45,
            )

            r = pdk.Deck(
                layers=[trips_layer],
                initial_view_state=view_state,
            )

            map_placeholder.pydeck_chart(r, height=600)

            current_time += time_step
            time.sleep(frame_delay)

        # Opcional: impedir que rode novamente sem novo clique
        st.session_state.animar_trajetos = False