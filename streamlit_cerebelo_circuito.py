import streamlit as st
import pandas as pd
import numpy as np

# --- Configuração da Página ---
st.set_page_config(page_title="Circuito Cerebelar Avançado", layout="wide")

# --- Título e Introdução ---
st.title("🧠 Circuito Cerebelar: Simulação Interativa Detalhada")
st.markdown("""
Bem-vindo a uma simulação mais detalhada do circuito cerebelar!
Controle a atividade das **Fibras Musgosas (FM)** e **Fibras Trepadeiras (FT)**,
e ajuste a **força da inibição da Célula de Purkinje (CP)** para observar
o impacto na frequência de disparos dos **Núcleos Cerebelares Profundos (NCP)**.
""")

# --- Diagrama Detalhado do Circuito (CORRIGIDO) ---
st.subheader("Diagrama do Circuito Cerebelar")
circuit_diagram_detailed = """
digraph CerebellarCircuitDetailed {
    rankdir=LR;
    node [shape=box, style="rounded,filled", fillcolor=lightgrey];

    subgraph cluster_Cortex {
        label = "Córtex Cerebelar";
        style = "filled";
        color = "lightyellow";
        node [fillcolor=white];

        GC [label="Células Granulares\n(Glutamato)"];
        CP [label="CÉLULA DE PURKINJE\n(GABA)", fillcolor=lightpink, shape=ellipse, style="filled,bold"];
        // Nota: Fibras Paralelas são os axônios das Células Granulares
    }

    FM [label="FIBRAS MUSGOSAS\n(Entrada Excitatória - Glutamato)", fillcolor=lightblue];
    FT [label="FIBRAS TREPADEIRAS\n(Entrada Excitatória - Aspartato/Glutamato)", fillcolor=lightcyan];
    NCP [label="NÚCLEOS CEREBELARES PROFUNDOS\n(Saída Excitatória - Glutamato)", fillcolor=lightgreen, shape=ellipse, style="filled,bold"];
    Output [label="Saída para outras áreas\ndo SNC (ex: Tálamo, Tronco)", shape=cds, fillcolor=gold];

    FM -> GC [label=" excita (+)"];
    GC -> CP [label=" excita (+)\n(via Fibras Paralelas)"]; // Representa a ação das Fibras Paralelas

    FT -> CP [label=" excita MUITO (+)\n(Picos Complexos)", color=purple, penwidth=2];

    FM -> NCP [label=" excita (+)\n(colateral)"];
    FT -> NCP [label=" excita (+)\n(colateral)", color=purple];

    CP -> NCP [label=" INIBE (-)", color=red, fontcolor=red, penwidth=2, style=bold];
    NCP -> Output [label=" modula"];

    {rank=same; FM; FT;}
    {rank=same; GC;}
    {rank=same; CP;}
    {rank=same; NCP;}
    {rank=same; Output;}
}
"""
st.graphviz_chart(circuit_diagram_detailed)
st.caption("""
**Legenda do Fluxograma:**
- **Fibras Musgosas (FM):** Principal via de entrada. Ativam Células Granulares (GC) e enviam colaterais para os NCP. (Neurotransmissor principal: Glutamato).
- **Células Granulares (GC):** Excitatórias. Seus axônios formam as Fibras Paralelas. (Neurotransmissor: Glutamato).
- **Fibras Paralelas:** Excita as Células de Purkinje, levando à geração de Picos Simples.
- **Fibras Trepadeiras (FT):** Originam-se da Oliva Inferior. Cada FT excita potentemente uma CP, gerando Picos Complexos, e envia colaterais aos NCP. (Neurotransmissor principal: Aspartato/Glutamato).
- **Célula de Purkinje (CP):** Única saída do córtex cerebelar. Inibitória. (Neurotransmissor: GABA).
- **Núcleos Cerebelares Profundos (NCP):** Principal via de saída do cerebelo. Excitatórios. (Neurotransmissor principal: Glutamato).
""")
st.markdown("---")

# --- Simulação Interativa ---
st.header("🔬 Simulação da Atividade Neuronal")

col_params, col_plot = st.columns([1, 2])

with col_params:
    st.subheader("Controles de Entrada")
    fm_strength = st.slider(
        "⚡ Intensidade da Ativação por Fibras Musgosas (FM)",
        min_value=0.0, max_value=10.0, value=5.0, step=0.1,
        help="Aumenta a excitação das Células Granulares (influenciando picos simples da CP) e excita diretamente os NCP."
    )
    ft_strength = st.slider(
        "🌋 Intensidade da Ativação por Fibras Trepadeiras (FT)",
        min_value=0.0, max_value=10.0, value=1.0, step=0.1,
        help="Aumenta a influência dos picos complexos da CP e excita diretamente os NCP."
    )
    pc_inhibition_scale = st.slider(
        "🛡️ Força da Inibição da Célula de Purkinje (CP) sobre os NCP",
        min_value=0.0, max_value=10.0, value=5.0, step=0.1,
        help="Controla o quão fortemente a atividade da Célula de Purkinje (resultante das FM e FT) inibe os Núcleos Cerebelares Profundos. 0 = sem inibição; 10 = inibição máxima."
    )

    # Parâmetros do Modelo (didáticos)
    NCP_BASELINE_ACTIVITY_HZ = 10 # Atividade tônica intrínseca dos NCP em Hz
    FM_TO_NCP_GAIN = 4.0          # Ganho da excitação das FM para os NCP
    FT_TO_NCP_GAIN = 6.0          # Ganho da excitação das FT para os NCP
    MAX_TOTAL_PC_INHIBITORY_POTENTIAL_HZ = 120


# --- Cálculos do Modelo ---
ncp_excitation_from_fm = fm_strength * FM_TO_NCP_GAIN
ncp_excitation_from_ft = ft_strength * FT_TO_NCP_GAIN
total_direct_excitation_ncp = NCP_BASELINE_ACTIVITY_HZ + ncp_excitation_from_fm + ncp_excitation_from_ft
effective_pc_inhibition_on_ncp = (pc_inhibition_scale / 10.0) * MAX_TOTAL_PC_INHIBITORY_POTENTIAL_HZ
ncp_final_firing_rate_hz = total_direct_excitation_ncp - effective_pc_inhibition_on_ncp
ncp_final_firing_rate_hz = max(0, ncp_final_firing_rate_hz)

with col_params:
    st.markdown("---")
    st.subheader("Resultados Calculados")
    st.metric(label="Excitação Direta Total nos NCP", value=f"{total_direct_excitation_ncp:.1f} Hz")
    st.metric(label="Inibição Efetiva da CP nos NCP", value=f"{effective_pc_inhibition_on_ncp:.1f} Hz (redução)")
    st.metric(label="Taxa de Disparo Final Estimada (NCP)", value=f"{ncp_final_firing_rate_hz:.1f} Hz",
              delta=f"{(ncp_final_firing_rate_hz - NCP_BASELINE_ACTIVITY_HZ):.1f} Hz vs Basal",
              delta_color="off")

# --- Visualização do Potencial de Ação Estilo Livro ---
with col_plot:
    st.subheader("📈 Visualização dos Potenciais de Ação dos NCP (Esquemático)")

    DURATION_MS = 200
    TIME_STEP_MS = 1
    time_ms = np.arange(0, DURATION_MS, TIME_STEP_MS)
    RESTING_POTENTIAL_MV = -70
    SPIKE_PEAK_MV = 30
    spikes_per_ms = ncp_final_firing_rate_hz / 1000.0
    spike_train = np.random.rand(len(time_ms)) < spikes_per_ms
    voltage_trace = np.full_like(time_ms, RESTING_POTENTIAL_MV, dtype=float)
    voltage_trace[spike_train] = SPIKE_PEAK_MV
    df_voltage = pd.DataFrame({'Tempo (ms)': time_ms, 'Potencial de Membrana (mV)': voltage_trace})

    st.line_chart(df_voltage.set_index('Tempo (ms)'), height=300)
    
    if ncp_final_firing_rate_hz == 0:
        st.info("Os Núcleos Cerebelares Profundos estão silenciados.")
    elif ncp_final_firing_rate_hz > NCP_BASELINE_ACTIVITY_HZ * 1.5:
        st.success(f"Alta frequência de disparos nos NCP: {ncp_final_firing_rate_hz:.1f} Hz.")
    else:
        st.write(f"Frequência de disparos nos NCP: {ncp_final_firing_rate_hz:.1f} Hz.")
    st.caption(f"Simulação de {DURATION_MS} ms. Picos de {RESTING_POTENTIAL_MV}mV a {SPIKE_PEAK_MV}mV.")

st.markdown("---")
# --- Resumo do Fluxo de Informação e Neurotransmissores (SIMPLIFICADO) ---
st.subheader("📖 Resumo do Fluxo de Informação e Neurotransmissores Principais")
st.markdown("""
-   **Fibras Musgosas (FM):** Entrada excitatória principal para o cerebelo.
    -   Neurotransmissor: **Glutamato (+)**.
    -   Ativam:
        -   **Células Granulares (GC)** no córtex cerebelar.
        -   **Núcleos Cerebelares Profundos (NCP)** (via colaterais).

-   **Células Granulares (GC):** Interneurônios excitatórios no córtex cerebelar.
    -   Neurotransmissor: **Glutamato (+)**.
    -   Seus axônios, as **Fibras Paralelas**, excitam as Células de Purkinje.

-   **Fibras Trepadeiras (FT):** Entrada excitatória potente, originada da Oliva Inferior.
    -   Neurotransmissor: **Aspartato/Glutamato (+)**.
    -   Ativam:
        -   **Células de Purkinje (CP)** no córtex cerebelar (causando Picos Complexos).
        -   **Núcleos Cerebelares Profundos (NCP)** (via colaterais).

-   **Célula de Purkinje (CP):** Principal neurônio de projeção do córtex cerebelar. É inibitória.
    -   Neurotransmissor: **GABA (-)**.
    -   Inibe os **Núcleos Cerebelares Profundos (NCP)**.

-   **Núcleos Cerebelares Profundos (NCP):** Principal via de saída do cerebelo. São excitatórios.
    -   Neurotransmissor: **Glutamato (+)**.
    -   Projetam-se para diversas áreas motoras e não motoras do SNC (ex: Tálamo, Tronco Encefálico).

**Funcionamento Geral:** Os NCPs integram as aferências excitatórias diretas (FM, FT) e a potente inibição das CPs. Este balanço permite que o cerebelo module a atividade motora, contribuindo para a coordenação, precisão e aprendizado de movimentos.
""")

st.sidebar.header("Sobre o App")
st.sidebar.info(
    "Simulação interativa para demonstrar como as entradas cerebelares e a modulação pelas Células de Purkinje afetam a saída dos Núcleos Cerebelares Profundos."
    "\n\nCriado para fins didáticos."
)