import streamlit as st
import pandas as pd
import altair as alt

# --- Configuração da Página ---
st.set_page_config(page_title="Cerebelo: Funções, Movimento e Lesões", layout="wide") # Título da página atualizado

# --- Título Principal do App ---
st.title("🧠 Cerebelo: Divisões Funcionais, Controle do Movimento e Efeitos de Lesões") # Título do app atualizado
st.markdown("""
Este aplicativo explora as três principais divisões funcionais do cerebelo,
como elas colaboram nas diferentes etapas de um movimento voluntário,
e as consequências de lesões em áreas específicas.
""")
st.markdown("---")

# --- Definição das Abas (com a nova aba) ---
tab_vestibular, tab_espinal, tab_cortical, tab_movimento, tab_lesoes = st.tabs([
    "🌐 Cerebelo Vestibular",
    "🚶 Cerebelo Espinal",
    "🎨 Cerebelo Cortical",
    "⏱️ Etapas do Movimento",
    "🩹 Efeitos de Lesões"  # Nova aba
])

# --- Dados Compartilhados / Constantes (para a nova aba também) ---
NOMES_DIVISOES_COMPLETO = ["Cerebelo Vestibular", "Cerebelo Espinal", "Cerebelo Cortical"] # Renomeado para evitar conflito
CORES_DIVISOES_COMPLETO = {"Cerebelo Vestibular": "#87CEEB", "Cerebelo Espinal": "#90EE90", "Cerebelo Cortical": "#FA8072"}
COR_LESIONADA = "#A9A9A9" # Cinza escuro para área lesionada

# --- Conteúdo da Aba: Cerebelo Vestibular ---
with tab_vestibular:
    st.header("🌐 Cerebelo Vestibular")
    st.markdown("""
    O Cerebelo Vestibular é crucial para o **equilíbrio**, a **postura** e a coordenação dos
    **movimentos oculares** com os movimentos da cabeça.
    Corresponde anatomicamente ao lobo floculonodular e partes da úvula.
    """)
    fluxograma_vestibular = """
    digraph G_Vestibular {
        rankdir=TB;
        node [shape=box, style="rounded,filled", fontname="Helvetica"];

        subgraph cluster_afferents {
            label = "Aferências Principais";
            fillcolor = "lightblue"; style="filled";
            A1 [label="Núcleos Vestibulares\n(Info: Posição/Movimento da Cabeça)"];
            A2 [label="Vias Visuais e Somatosensoriais\n(Contexto para equilíbrio)"];
        }

        subgraph cluster_nuclei {
            label = "Núcleos Cerebelares e Associados";
            fillcolor = "lightpink"; style="filled";
            NC [label="Núcleo Fastigial (parte medial)\nNúcleos Vestibulares (direto)"];
        }

        subgraph cluster_efferents {
            label = "Eferências (Tratos Motores)";
            fillcolor = "lightgreen"; style="filled";
            E1 [label="Tratos Vestibulospinais\n(Medial e Lateral)"];
            E2 [label="Conexões com Núcleos Oculomotores\n(via Fascículo Longitudinal Medial)"];
        }

        subgraph cluster_muscles {
            label = "Musculatura Controlada";
            fillcolor = "lightyellow"; style="filled";
            M1 [label="Músculos Axiais e Proximais Extensores\n(Postura, Equilíbrio)"];
            M2 [label="Músculos Extrínsecos do Olho\n(Estabilização do olhar - RVO)"];
        }

        A1 -> NC;
        A2 -> NC [style=dashed, label="modula"];
        NC -> E1;
        NC -> E2;
        E1 -> M1 [label="influencia"];
        E2 -> M2 [label="controla"];
    }
    """
    st.graphviz_chart(fluxograma_vestibular)
    st.caption("RVO: Reflexo Vestíbulo-Ocular.")


# --- Conteúdo da Aba: Cerebelo Espinal ---
with tab_espinal:
    st.header("🚶 Cerebelo Espinal")
    st.markdown("""
    O Cerebelo Espinal está envolvido na **regulação do tônus muscular**, na **coordenação da marcha**
    e na **correção de movimentos em execução**, comparando o comando motor com o feedback sensorial.
    Corresponde anatomicamente ao verme e às zonas paravermais (intermediárias) dos hemisférios.
    """)
    fluxograma_espinal = """
    digraph G_Espinal {
        rankdir=TB;
        node [shape=box, style="rounded,filled", fontname="Helvetica"];

        subgraph cluster_afferents_spinal {
            label = "Aferências Principais";
            fillcolor = "lightblue"; style="filled";
            AS1 [label="Medula Espinal\n(Tratos Espinocerebelares: propriocepção, tato)"];
            AS2 [label="Córtex Motor e Pré-Motor\n(Cópia dos comandos - via núcleos pontinos, oliva)"];
            AS3 [label="Núcleos do Tronco Encefálico"];
        }

        subgraph cluster_nuclei_spinal {
            label = "Núcleos Cerebelares Envolvidos";
            fillcolor = "lightpink"; style="filled";
            NCS_Verme [label="Núcleo Fastigial\n(Verme)"];
            NCS_Paraverme [label="Núcleos Interpostos\n(Globoso e Emboliforme)\n(Zonas Paravermais)"];
        }

        subgraph cluster_efferents_spinal {
            label = "Eferências (Tratos Motores)";
            fillcolor = "lightgreen"; style="filled";
            ES_Verme [label="Sistemas Motores Medial Descendentes\n(ex: Tratos Vestibulospinais, Reticulospinais)"];
            ES_Paraverme [label="Sistemas Motores Lateral Descendentes\n(ex: Trato Rubrospinal, Trato Corticospinal Lateral)"];
        }

        subgraph cluster_muscles_spinal {
            label = "Musculatura Controlada";
            fillcolor = "lightyellow"; style="filled";
            MS_Verme [label="Músculos Axiais e Proximais\n(Postura e locomoção)"];
            MS_Paraverme [label="Músculos Distais dos Membros\n(Coordenação e correção de movimentos)"];
        }

        AS1 -> NCS_Verme; AS1 -> NCS_Paraverme;
        AS2 -> NCS_Verme; AS2 -> NCS_Paraverme;
        AS3 -> NCS_Verme; AS3 -> NCS_Paraverme;

        NCS_Verme -> ES_Verme;
        NCS_Paraverme -> ES_Paraverme;

        ES_Verme -> MS_Verme [label="influencia"];
        ES_Paraverme -> MS_Paraverme [label="influencia"];
    }
    """
    st.graphviz_chart(fluxograma_espinal)

# --- Conteúdo da Aba: Cerebelo Cortical ---
with tab_cortical:
    st.header("🎨 Cerebelo Cortical")
    st.markdown("""
    O Cerebelo Cortical é fundamental para o **planejamento**, **iniciação** e
    **'timing' preciso de movimentos voluntários complexos e sequenciais**, especialmente aqueles que
    requerem aprendizado e habilidade. Também está implicado em algumas **funções cognitivas**.
    Corresponde anatomicamente às porções laterais dos hemisférios cerebelares.
    """)
    fluxograma_cortical = """
    digraph G_Cortical {
        rankdir=TB;
        node [shape=box, style="rounded,filled", fontname="Helvetica"];

        subgraph cluster_afferents_cortical {
            label = "Aferências Principais";
            fillcolor = "lightblue"; style="filled";
            AC1 [label="Córtex Cerebral (Áreas Motoras, Pré-Motoras, Associação)\n(Via Núcleos Pontinos - Trato Cortico-Ponto-Cerebelar)"];
        }

        subgraph cluster_nuclei_cortical {
            label = "Núcleo Cerebelar Envolvido";
            fillcolor = "lightpink"; style="filled";
            NCC [label="Núcleo Denteado"];
        }

        subgraph cluster_efferents_cortical {
            label = "Eferências (Influência sobre Tratos Motores)";
            fillcolor = "lightgreen"; style="filled";
            EC1 [label="Córtex Motor Primário e Pré-Motor\n(Via Núcleo Ventrolateral do Tálamo)"];
        }

        subgraph cluster_muscles_cortical {
            label = "Musculatura Controlada (Indiretamente)";
            fillcolor = "lightyellow"; style="filled";
            MC1 [label="Músculos Distais dos Membros\n(Movimentos habilidosos, precisos, sequenciais)"];
            MC2 [label="Musculatura da Fala\n(Articulação precisa)"];
        }

        AC1 -> NCC;
        NCC -> EC1 [label="projeta para"];
        EC1 -> MC1 [label="controla via Trato Corticospinal"];
        EC1 -> MC2 [label="controla via Trato Corticobulbar"];
    }
    """
    st.graphviz_chart(fluxograma_cortical)


# --- Conteúdo da Aba: Etapas do Movimento (COM DESCRIÇÕES DETALHADAS) ---
with tab_movimento:
    st.header("⏱️ Etapas do Movimento: Contribuição Dinâmica do Cerebelo")
    st.markdown("""
    Use o controle deslizante para avançar pelas fases de um movimento e observe como a
    contribuição relativa de cada divisão cerebelar se altera.
    """)

    # Renomeado para evitar conflito com NOMES_DIVISOES_COMPLETO
    nomes_divisoes_mov = ["Cerebelo Vestibular", "Cerebelo Espinal", "Cerebelo Cortical"]
    # Renomeado para evitar conflito com CORES_DIVISOES_COMPLETO
    cores_divisoes_mov = {"Cerebelo Vestibular": "#87CEEB", "Cerebelo Espinal": "#90EE90", "Cerebelo Cortical": "#FA8072"}


    fases_contrib = {
        "Planejamento": {
            "desc_geral": "O cérebro define o objetivo, sequência, força e 'timing' do movimento.",
            "contrib": {"Cerebelo Vestibular": 1, "Cerebelo Espinal": 2, "Cerebelo Cortical": 5},
            "detalhes": [
                "**Cerebelo Cortical:** Recebe a intenção do movimento das áreas de associação do córtex cerebral (via trato cortico-ponto-cerebelar para o núcleo denteado). Elabora o plano motor (sequência e 'timing') e o envia de volta ao córtex motor (via tálamo).",
                "**Cerebelo Espinal:** Recebe informações do plano motor e ajusta o tônus muscular preparatório dos músculos proximais e axiais (via núcleo fastigial e interpostos).",
                "**Cerebelo Vestibular:** Mantém a estabilidade postural básica necessária para iniciar o movimento (via núcleo fastigial e tratos vestibulospinais)."
            ]
        },
        "Início": {
            "desc_geral": "O córtex motor envia o comando e o movimento começa. O cerebelo monitora.",
            "contrib": {"Cerebelo Vestibular": 3, "Cerebelo Espinal": 4, "Cerebelo Cortical": 4},
            "detalhes": [
                "**Cerebelo Cortical:** Assegura o 'timing' correto para o início da sequência de contrações musculares, conforme planejado.",
                "**Cerebelo Espinal:** Recebe uma cópia do comando motor (descarga corolária) e o feedback inicial do movimento (via tratos espinocerebelares para os núcleos interpostos). Inicia a comparação para garantir suavidade.",
                "**Cerebelo Vestibular:** Realiza ajustes posturais antecipatórios para compensar o início do movimento e manter o equilíbrio."
            ]
        },
        "Execução": {
            "desc_geral": "O movimento está em andamento. O cerebelo compara continuamente o plano com a realidade.",
            "contrib": {"Cerebelo Vestibular": 4, "Cerebelo Espinal": 5, "Cerebelo Cortical": 3},
            "detalhes": [
                "**Cerebelo Espinal:** É o principal ator. Compara o feedback sensorial contínuo (propriocepção dos tratos espinocerebelares) com o comando motor. Se houver discrepância, envia sinais corretivos imediatos aos sistemas motores descendentes (ex: trato rubrospinal, corticospinal) via núcleos interpostos (membros distais) e fastigial (tronco/proximal).",
                "**Cerebelo Vestibular:** Monitora ativamente o equilíbrio e a orientação espacial, fazendo ajustes posturais através dos tratos vestibulospinais. Coordena os movimentos oculares (RVO) para manter a estabilidade visual.",
                "**Cerebelo Cortical:** Monitora a progressão geral do movimento em relação ao plano, podendo intervir se ajustes mais globais forem necessários."
            ]
        },
        "Correção": {
            "desc_geral": "Ajustes são feitos se o movimento desviar do curso ou se surgirem perturbações.",
            "contrib": {"Cerebelo Vestibular": 3, "Cerebelo Espinal": 5, "Cerebelo Cortical": 2},
            "detalhes": [
                "**Cerebelo Espinal:** Detecta rapidamente os erros entre o movimento desejado e o real. Modifica a atividade dos neurônios motores para corrigir a trajetória e a força, crucial para se adaptar a resistências inesperadas.",
                "**Cerebelo Vestibular:** Se uma perturbação causar desequilíbrio, ele ativa respostas posturais corretivas rápidas.",
                "**Cerebelo Cortical:** Menos envolvido em correções rápidas, mas pode ser recrutado se o erro for grande e exigir um replanejamento da estratégia motora."
            ]
        },
        "Fim/Aprendizado": {
            "desc_geral": "O movimento é concluído. A experiência é analisada para refinar futuras ações e habilidades.",
            "contrib": {"Cerebelo Vestibular": 1, "Cerebelo Espinal": 2, "Cerebelo Cortical": 5},
            "detalhes": [
                "**Cerebelo Cortical:** É fundamental para o aprendizado motor. Compara o resultado final do movimento com a intenção. Sinais de erro (possivelmente via fibras trepadeiras para o núcleo denteado e córtex cerebelar) induzem plasticidade sináptica, refinando os programas motores para maior precisão e eficiência em futuras tentativas.",
                "**Cerebelo Espinal:** Adapta os ganhos e parâmetros de controle dos reflexos e movimentos com base na experiência recente.",
                "**Cerebelo Vestibular:** Adapta os reflexos vestibulares e posturais, melhorando a capacidade de manter o equilíbrio em situações semelhantes no futuro."
            ]
        }
    }
    lista_fases = list(fases_contrib.keys())

    fase_selecionada_mov = st.select_slider(
        "Selecione a Fase do Movimento:",
        options=lista_fases,
        value=lista_fases[0]
    )

    info_fase_atual = fases_contrib[fase_selecionada_mov]
    dados_grafico_fase = []
    for divisao in nomes_divisoes_mov: # Usando nomes_divisoes_mov
        dados_grafico_fase.append({
            "Divisão": divisao,
            "Contribuição": info_fase_atual["contrib"][divisao],
            "cor": cores_divisoes_mov[divisao] # Usando cores_divisoes_mov
        })
    df_fase = pd.DataFrame(dados_grafico_fase)

    chart = alt.Chart(df_fase).mark_bar().encode(
        x=alt.X('Contribuição:Q', title="Nível de Contribuição (0-5)", scale=alt.Scale(domain=[0, 5])),
        y=alt.Y('Divisão:N', sort=None, title="Divisão Cerebelar"),
        color=alt.Color('Divisão:N', scale=alt.Scale(domain=nomes_divisoes_mov, range=[cores_divisoes_mov[d] for d in nomes_divisoes_mov]), legend=None),
        tooltip=['Divisão', 'Contribuição']
    ).properties(
        title=f"Atividade Relativa na Fase: {fase_selecionada_mov}",
        height=220
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown(f"#### Detalhes da Fase: {fase_selecionada_mov}")
    st.markdown(f"**Visão Geral:** {info_fase_atual['desc_geral']}")
    for detalhe in info_fase_atual['detalhes']:
        st.markdown(f"- {detalhe}")
    st.caption("Este gráfico é uma representação esquemática da intensidade relativa da contribuição de cada divisão.")


# --- Conteúdo da Aba: Efeitos de Lesões ---
with tab_lesoes:
    st.header("🩹 Efeitos de Lesões Cerebelares")
    st.markdown("""
    Lesões em diferentes partes do cerebelo resultam em síndromes clínicas distintas,
    refletindo a função especializada de cada divisão. Selecione uma área para
    visualizar os sintomas e o impacto funcional.
    """)

    lesoes_sintomas = {
        "Nenhuma (Funcionamento Normal)": {
            "sintomas": ["Nenhum sintoma, coordenação motora preservada."],
            "impacto_fases": "Todas as fases do movimento ocorrem de forma coordenada e precisa.",
            "grafico_contrib_modificada": None
        },
        "Cerebelo Vestibular": {
            "sintomas": [
                "🤸‍♂️ **Movimentos Irregulares das Pernas (Ataxia da Marcha):** Dificuldade em manter uma marcha estável, base alargada.",
                "🍂 **Tendência a Quedas:** Especialmente com mudanças de direção ou olhos fechados.",
                "⚖️ **Perda do Equilíbrio (Desequilíbrio Truncal):** Dificuldade em manter a postura ereta.",
                "😵‍💫 **Nistagmo e Perda do Controle Ocular:** Dificuldade em fixar o olhar, movimentos oculares anormais, especialmente durante rotação da cabeça (RVO prejudicado)."
            ],
            "impacto_fases": """
            - **Planejamento:** Postura de base pode ser instável.
            - **Início:** Ajustes posturais antecipatórios deficientes, levando a desequilíbrio.
            - **Execução:** Equilíbrio e coordenação olho-cabeça severamente comprometidos. Marcha instável.
            - **Correção:** Dificuldade em corrigir desequilíbrios.
            - **Fim/Aprendizado:** Adaptação de reflexos posturais e vestibulares prejudicada.
            """,
            "grafico_contrib_modificada": {"Cerebelo Vestibular": 0.1}
        },
        "Cerebelo Espinal": {
            "sintomas": [
                "💪 **Ataxia dos Membros:** Movimentos desajeitados e imprecisos dos braços e pernas.",
                "📉 **Redução do Tônus Muscular (Hipotonia):** Músculos mais flácidos, menor resistência ao movimento passivo.",
                "🗣️ **Alteração da Fala (Disartria Cerebelar):** Fala arrastada, escandida, com variações de volume."
            ],
            "impacto_fases": """
            - **Planejamento:** Dificuldade em ajustar o tônus muscular inicial.
            - **Início:** Movimentos podem ser hesitantes ou mal direcionados.
            - **Execução:** Principalmente afetada. Incapacidade de corrigir erros em tempo real, levando a movimentos atáxicos, dismétricos.
            - **Correção:** Capacidade de ajuste fino durante o movimento severamente reduzida.
            - **Fim/Aprendizado:** Dificuldade em calibrar a força e precisão dos movimentos.
            """,
            "grafico_contrib_modificada": {"Cerebelo Espinal": 0.1}
        },
        "Cerebelo Cortical": {
            "sintomas": [
                "⏳ **Atraso no Início dos Movimentos (Adiadococinesia):** Dificuldade em iniciar movimentos rapidamente.",
                "🧩 **Decomposição do Movimento:** Movimentos multiarticulares são realizados de forma segmentada.",
                "🔄 **Disdiadococinesia:** Dificuldade em realizar movimentos rápidos e alternados.",
                "👋 **Tremor de Intenção:** Tremor que surge ou piora ao tentar realizar um movimento preciso.",
                "🎯 **Dismetria:** Erro no alcance de um alvo (hipermetria ou hipometria)."
            ],
            "impacto_fases": """
            - **Planejamento:** Severamente afetado. Dificuldade em sequenciar, 'timar' e selecionar programas motores.
            - **Início:** Atrasado e desajeitado.
            - **Execução:** Movimentos perdem a suavidade e o 'timing'.
            - **Correção:** Dificuldade em replanejar ou ajustar estratégias motoras complexas.
            - **Fim/Aprendizado:** Aprendizado de novas habilidades motoras prejudicado.
            """,
            "grafico_contrib_modificada": {"Cerebelo Cortical": 0.1}
        }
    }

    lista_lesoes = list(lesoes_sintomas.keys())
    area_lesada_selecionada = st.selectbox(
        "Selecione a Área Cerebelar Lesada para Simulação:",
        options=lista_lesoes,
        index=0
    )

    info_lesao_atual = lesoes_sintomas[area_lesada_selecionada]

    st.markdown(f"### Sintomatologia Principal da Lesão no **{area_lesada_selecionada}**")
    if area_lesada_selecionada == "Nenhuma (Funcionamento Normal)":
        st.success(info_lesao_atual["sintomas"][0])
    else:
        for sintoma in info_lesao_atual["sintomas"]:
            st.markdown(f"- {sintoma}")

    st.markdown("---")
    st.markdown(f"### Impacto Funcional da Lesão no **{area_lesada_selecionada}**")

    fase_exemplo_lesao = "Execução" # Mantendo a fase de Execução como exemplo para o gráfico
    
    # Verificar se fases_contrib está definida (deve estar, pois a aba de movimento é processada antes)
    if 'fases_contrib' in locals() or 'fases_contrib' in globals():
        contrib_normal_fase_exemplo = fases_contrib[fase_exemplo_lesao]["contrib"]
        dados_grafico_lesao = []
        modificador_lesao = info_lesao_atual["grafico_contrib_modificada"]

        for divisao in NOMES_DIVISOES_COMPLETO: # Usar a lista completa de nomes
            contrib = contrib_normal_fase_exemplo.get(divisao, 0) # .get para segurança
            cor = CORES_DIVISOES_COMPLETO.get(divisao, "#CCCCCC") # .get para segurança

            if modificador_lesao and divisao in modificador_lesao:
                contrib = modificador_lesao[divisao]
                cor = COR_LESIONADA

            dados_grafico_lesao.append({
                "Divisão": divisao,
                "Contribuição (Execução)": contrib,
                "cor_barra": cor
            })
        df_lesao = pd.DataFrame(dados_grafico_lesao)

        chart_lesao = alt.Chart(df_lesao).mark_bar().encode(
            x=alt.X('Contribuição (Execução):Q', title="Nível de Contribuição (0-5)", scale=alt.Scale(domain=[0, 5])),
            y=alt.Y('Divisão:N', sort=None, title="Divisão Cerebelar"),
            color=alt.Color('cor_barra:N', scale=None, legend=None),
            tooltip=['Divisão', 'Contribuição (Execução)']
        ).properties(
            title=f"Contribuição Relativa Simulada na Fase de Execução com Lesão em: {area_lesada_selecionada}",
            height=220
        )
        st.altair_chart(chart_lesao, use_container_width=True)
        st.caption(f"O gráfico acima mostra um exemplo de como a contribuição das divisões seria afetada durante a fase de **{fase_exemplo_lesao}** se o **{area_lesada_selecionada}** estivesse lesionado. A área cinza representa a função comprometida.")
    else:
        st.warning("Dados da aba 'Etapas do Movimento' não carregados para gerar o gráfico de lesão.")


    st.markdown("#### Impacto nas Etapas do Movimento (Resumido):")
    st.markdown(info_lesao_atual["impacto_fases"])


st.sidebar.info(
    "Este aplicativo é uma representação simplificada para fins didáticos. "
    "A neurofisiologia do cerebelo é vasta e complexa."
)