import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from grafo_disciplinas_si import grafoCCO

def gerar_pesos_das_arestas(grafo):
    dependencias = {disc: 0 for disc in grafo}
    for dados in grafo.values():
        for pre in dados["pre_requisitos"]:
            dependencias[pre] += 1
    pesos = {}
    for destino, dados in grafo.items():
        for origem in dados["pre_requisitos"]:
            pesos[(origem, destino)] = dependencias[origem]
    return pesos

# Configurações do grafo
pesos = gerar_pesos_das_arestas(grafoCCO)
G = nx.DiGraph()

for d, dados in grafoCCO.items():
    G.add_node(d, label=dados["nome"], semestre=dados["semestre"])
    for pre in dados["pre_requisitos"]:
        G.add_edge(pre, d, weight=pesos.get((pre, d), 1))

# Layout organizado por semestres
semestres = defaultdict(list)
for node, dados in grafoCCO.items():
    semestres[dados["semestre"]].append(node)

pos = {}
vertical_spacing = 3.0
horizontal_spacing = 4.0

for semestre, nos in sorted(semestres.items()):
    x = semestre * horizontal_spacing
    total_nodes = len(nos)
    for i, node in enumerate(sorted(nos)):
        y = -(i - total_nodes/2) * vertical_spacing
        pos[node] = (x, y)

# Criação da figura
plt.figure(figsize=(25, 15))
ax = plt.gca()
ax.set_title("Grafo de Disciplinas - Curso CCO", fontsize=20, pad=25)

# 1. Primeiro desenhamos os nós de fundo branco (para contraste)
for semestre in semestres:
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=semestres[semestre],
        node_size=3100,
        node_color='white',
        edgecolors='none',
        ax=ax
    )

# 2. Desenhamos as ARESTAS com SETAS BEM VISÍVEIS
edges = nx.draw_networkx_edges(
    G, pos,
    arrows=True,
    arrowsize=20,  # Tamanho aumentado
    arrowstyle='-|>',  # Estilo moderno
    width=2.5,  # Linha mais grossa
    edge_color='#555555',  # Cor mais escura
    alpha=0.9,
    connectionstyle='arc3,rad=0.3',
    ax=ax,
    node_size=3000,  # Importante para o cálculo das setas
    min_source_margin=20,  # Espaço da seta no nó origem
    min_target_margin=20   # Espaço da seta no nó destino
)

# 3. Desenhamos os NÓS coloridos por cima
colors = plt.cm.tab20.colors
for semestre in semestres:
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=semestres[semestre],
        node_size=2000,
        node_color=[colors[semestre % len(colors)]],
        edgecolors='black',
        linewidths=2,
        ax=ax,
        label=f"\n  Semestre {semestre}\n"
    )

# 4. Adicionamos os PESOS das arestas
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=12,
    font_color='darkred',
    bbox=dict(
        facecolor='white',
        edgecolor='none',
        alpha=0.9,
        boxstyle='round,pad=0.3'
    ),
    rotate=False,
    ax=ax
)

# 5. Rótulos dos nós
node_labels = {node: f"{node}" for node in G.nodes()}
nx.draw_networkx_labels(
    G, pos,
    labels=node_labels,
    font_size=10,
    font_weight='bold',
    verticalalignment='center',
    ax=ax
)

# Grade de referência
for semestre in sorted(semestres.keys()):
    plt.axvline(x=semestre * horizontal_spacing, color='lightgray', linestyle='--', alpha=0.3)

plt.legend(scatterpoints=1, frameon=True, title="Semestres", fontsize=12, title_fontsize=13)
plt.grid(False)
plt.axis("off")
plt.tight_layout()
plt.savefig("grafo_setas_visiveis.png", dpi=300, bbox_inches='tight')
plt.show()