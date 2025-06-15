import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from networkx.drawing.nx_agraph import graphviz_layout
from typing import Literal, Union
from tabulate import tabulate


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
            delay = max(0, period - period_map[code])
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
                delay = max(0, period, period_map[neighbor])
                queue.append((delay, neighbor))

        queue = deque(sorted(queue, reverse=True))

    return ordered

def get_elective_disciplines(data: list):
    elective = read_file("disc-opt.json")
    data = [disc for disc in data if not disc["obrigatorio"]]
    data.extend(elective)

    return data


def get_recommended_courses(disciplines: dict, top_order: list, student: dict) -> list:
    pending = student.get("disciplinas_pendentes")
    period = student.get("periodo")

    recommendations = []

    for code in top_order:
        discipline = disciplines.get(code)

        if not discipline:
            continue

        disc_period = discipline["periodo"]
        disc_mandatory = discipline["obrigatorio"]

        if period % 2 != disc_period % 2:
            continue

        disc_prereqs = discipline["requisitos"]
        
        skip_discipline = False

        for prereq in disc_prereqs:
            for disc in pending:
                skip_discipline = disc in prereq
                
                if skip_discipline:
                    break

        if skip_discipline:
            continue

        if disc_mandatory and disc_period <= period:
            item = {
                "sigla": code,
                "periodo": disc_period,
                "obrigatario": disc_mandatory,
                "ch": discipline["ch"],
                "prioridade": "HIGH"
            }

            recommendations.append(item)


    return recommendations
    

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


def show_recommendations(recommendations: list):
    headers = ["SIGLA", "PERIODO", "OBRIGATORIO", "CARGA HORARIA", "PRIORIDADE"]
    table = []

    for item in recommendations:
        workload = f"{item["ch"] * 16}h"
        mandatory = "Sim" if item["obrigatario"] else "Não"
        priority = "Alta" if item["prioridade"] else "Baixa"

        row = [
            item["sigla"],
            item["periodo"],
            mandatory,
            workload,
            priority
        ]

        table.append(row)


    print(tabulate(table, headers=headers, tablefmt="grid"))


def display_schedule_table():
    matrix = [[False for _ in range(5)] for _ in range(15)]
    headers = ["Horário", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    timetables = [
        "07:00", "07:55", "08:50", "10:10", "11:05",
        "13:30", "14:25", "15:45", "16:40", "17:35",
        "19:00", "19:50", "21:00", "21:50", "22:40"
    ]
    table = []

    for time, data in zip(timetables, matrix):
        row = [time, *data]

        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    students = read_file("students.json")
    student = students[0]

    course = student["curso"]
    period = student["periodo"]
    pending = student["disciplinas_pendentes"]

    data = read_file(f"disc-{course}.json")
    disciplines = {disc["sigla"]: disc for disc in data}

    top_order = topological_sorting(disciplines, pending, period)
    electives = get_elective_disciplines(data)
    recommendations = get_recommended_courses(disciplines, top_order, student)

    show_recommendations(recommendations)

