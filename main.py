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


def topological_sorting(disciplines: dict, pending: list, period: int) -> list:
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    period_map = {}

    pending = set(pending)

    for code in pending:
        if code not in disciplines.keys():
            continue

        disc_period = disciplines[code]["periodo"]
        prereqs = disciplines[code]["requisitos"]

        period_map[code] = disc_period

        for prereq in prereqs:
            if prereq not in pending:
                continue

            graph[prereq].append(code)
            in_degree[code] += 1

    queue = []

    for code in pending:
        if code not in disciplines.keys():
            continue

        if in_degree[code] == 0:
            delay = max(0, int(period) - int(period_map[code]))
            queue.append((delay, code))

    queue.sort(reverse=True)
    queue = deque(queue)

    ordered = []
    
    while queue:
        _, current = queue.popleft()
        ordered.append(current)
        
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1

            if in_degree[neighbor] == 0:
                delay = max(0, int(period), int(period_map[neighbor]))
                queue.append((delay, neighbor))

        queue = deque(sorted(queue, reverse=True))

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

    course = student["curso"]
    period = student["periodo"]
    pending = student["disciplinas_pendentes"]

    data = read_file(f"disc-{course}.json")
    disciplines = {disc["sigla"]: disc for disc in data}

    top_order = topological_sorting(disciplines, pending, period)


    print(top_order)

