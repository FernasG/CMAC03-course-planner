import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from networkx.drawing.nx_agraph import graphviz_layout
from typing import Literal, Union


def read_file(file: str) -> Union[dict, list]:
    with open(file, "r") as file:
        data = json.load(file)

        return data


def json_to_adjacency_matrix(json: dict) -> dict:
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


def topological_sorting(graph: dict) -> list:
    in_degree = defaultdict(int)

    for prereqs in graph.values():
        for pr in prereqs:
            in_degree[pr] += 0

    for discipline, prereqs in graph.items():
        in_degree[discipline] += len(prereqs)

    queue = deque([m for m in graph if in_degree[m] == 0])
    ordered = []
    
    while queue:
        current = queue.popleft()
        ordered.append(current)
        
        for neighbor, prereqs in graph.items():
            if current in prereqs:
                in_degree[neighbor] -= 1

                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return ordered


def get_recommended_courses(top_order: list, student: dict) -> list:
    ch_optatives = student.get("ch_optativas_pendentes")
    disciplines = student.get("disciplinas_pendentes")
    period = student.get("periodo")
    
    print(top_order, ch_optatives, disciplines, period)
    


def generate_graph_view(matrix: dict, view_mode: Literal["view", "img"]) -> None:
    G = nx.DiGraph()

    for discipline, prereqs in matrix.items():
        G.add_node(discipline)

        for prereq in prereqs:
            G.add_edge(prereq, discipline)

    plt.figure(figsize=(18, 14))

    # pos = nx.spring_layout(G, k=0.5, iterations=100)
    pos = graphviz_layout(G, prog="dot", args="-Grankdir=LR")
    
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
    students = read_file("students.json")
    student = students[0]
    course = student.get("curso")


    data = read_file(f"disc-{course}.json")

    # limpa materias feitas, limpa materia periodo par/impar

    matrix = json_to_adjacency_matrix(data)
    top_order = topological_sorting(matrix)
    
    print(matrix)
    recommendation = get_recommended_courses(top_order, student)
