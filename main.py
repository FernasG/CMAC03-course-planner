import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from typing import Literal


def read_file(file: str):
    with open(file, "r") as file:
        data = json.load(file)

        return data


def json_to_adjacency_matrix(json: dict):
    matrix = {}

    for item in json:
        key = item["sigla"]
        req = item["requisitos"]

        values = []

        for el in req:
            req_list = el.split("-")
            values.extend(req_list)

        matrix[key] = values

    return matrix


def generate_graph_view(matrix: dict, view_mode: Literal["view", "img"]):
    G = nx.DiGraph()

    for discipline, prereqs in matrix.items():
        G.add_node(discipline)

        for prereq in prereqs:
            G.add_edge(prereq, discipline)

    plt.figure(figsize=(18, 14))

    # pos = nx.spring_layout(G, k=0.5, iterations=100)
    pos = graphviz_layout(G, prog="dot", args="-Grankdir=LR")  # LR = Left to Right
    
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=800)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrows=True, arrowsize=12, min_source_margin=15, min_target_margin=15, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title("Graph of Courses and Prerequisites", fontsize=14)
    plt.axis("off")
    plt.tight_layout()

    if view_mode == "view":
        plt.show()
    else:
        plt.savefig("graph.png", format="png", dpi=300)


if __name__ == "__main__":
    data = read_file("disc-sin.json")
    matrix = json_to_adjacency_matrix(data)
    generate_graph_view(matrix, "view")

    print(matrix)
