import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from networkx.drawing.nx_agraph import graphviz_layout
from functools import reduce
from tabulate import tabulate
from typing import Literal, Union
import entrada 


time_period_range = {
    "M": (0, 5),
    "T": (5, 10),
    "N": (10, 14)
}


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


def get_optatives_disciplines(data: list):
    optatives = read_file("disc-opt.json")
    data = [disc for disc in data if not disc["obrigatorio"]]
    data.extend(optatives)

    return data


def check_schedule_conflict(grid: list, discipline_timestamp: list):
    has_conflict = False

    for timestamp in discipline_timestamp:
        day = timestamp[0]
        period = timestamp[1]
        timetables = list(timestamp[2:])

        (start, end) = time_period_range[period]
        grid_period = grid[start:end]

        day_index = int(day) - 2

        if any(grid_period[int(time) - 1][day_index] for time in timetables):
            has_conflict = True
        
            break

    return has_conflict


def add_schedule_entry(grid: list, code: str, discipline_timestamp: list):
    for timestamp in discipline_timestamp:
        day = timestamp[0]
        period = timestamp[1]
        timetables = list(timestamp[2:])

        (start, end) = time_period_range[period]
        grid_period = grid[start:end]

        day_index = int(day) - 2

        for time in timetables:
            grid_period[int(time) - 1][day_index] = code


def get_optative_disciplines_for_period(optatives: list, grid: list, period: int, hours_pending: int) -> list:
    expected_hours = int(hours_pending) / (8 - int(period))
    reached_hours = 0
    max_optatives_per_period = 5
    optatives_selected = []

    for discipline in optatives:
        code = discipline["sigla"]
        disc_timestamp = discipline["horarios"]
        disc_period = discipline["periodo"]
        disc_wl = discipline["ch"]
        is_even_period = int(period) % 2

        if is_even_period and disc_period == -1:
            continue

        has_conflict = check_schedule_conflict(grid, disc_timestamp)

        if has_conflict:
            continue

        reached_hours += disc_wl
        optatives_selected.append(discipline)
        add_schedule_entry(grid, code, disc_timestamp)

        if reached_hours >= expected_hours or len(optatives_selected) == max_optatives_per_period:
            break


    return optatives_selected


def get_recommended_courses(disciplines: dict, optatives: list, top_order: list, student: dict) -> tuple:
    pending_opt_wl = student.get("ch_optativas_pendentes")
    pending = student.get("disciplinas_pendentes")
    period = student.get("periodo")

    recommendations = []
    conflicted_disciplines = []
    grid_matrix = [[False for _ in range(5)] for _ in range(15)]

    for code in top_order:
        discipline = disciplines.get(code)

        if not discipline:
            continue

        disc_period = discipline["periodo"]
        disc_mandatory = discipline["obrigatorio"]

        if (int(period) % 2 != int(disc_period) % 2):
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

        disc_timestamp = discipline["horarios"]

        has_conflict = check_schedule_conflict(grid_matrix, disc_timestamp)

        if has_conflict:
            conflicted_disciplines.append(disc)
            continue

        add_schedule_entry(grid_matrix, code, disc_timestamp)

        item = {
            "sigla": code,
            "periodo": disc_period,
            "obrigatario": disc_mandatory,
            "horarios": disc_timestamp,
            "ch": discipline["ch"],
            "prioridade": "HIGH"
        }

        recommendations.append(item)

    optatives_selected = get_optative_disciplines_for_period(optatives, grid_matrix, period, pending_opt_wl)

    for optative in optatives_selected:
        code = optative["sigla"]
        disc_period = optative["periodo"]
        disc_timestamp = optative["horarios"]

        item = {
            "sigla": code,
            "periodo": disc_period,
            "obrigatario": False,
            "horarios": disc_timestamp,
            "ch": discipline["ch"],
            "prioridade": "LOW"
        }

        recommendations.append(item)

    total_hours = sum([disc["ch"] * 16 for disc in recommendations])

    return (recommendations, conflicted_disciplines, total_hours, grid_matrix)


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


def display_recommendations(recommendations: list):
    headers = ["SIGLA", "PERIODO", "OBRIGATORIO", "CARGA HORARIA", "HORARIOS", "PRIORIDADE"]
    table = []

    for item in recommendations:
        
        workload = f'{item["ch"] * 16}h'
        mandatory = "Sim" if item["obrigatario"] else "Não"
        priority = "Alta" if item["prioridade"] == "HIGH" else "Baixa"
        timestamp = "-".join(item["horarios"])

        row = [
            item["sigla"],
            item["periodo"],
            mandatory,
            workload,
            timestamp,
            priority
        ]

        table.append(row)


    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def display_schedule_table(grid: list):
    headers = ["Horário", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    timetables = [
        "07:00", "07:55", "08:50", "10:10", "11:05",
        "13:30", "14:25", "15:45", "16:40", "17:35",
        "19:00", "19:50", "21:00", "21:50", "22:40"
    ]
    table = []

    for time, data in zip(timetables, grid):
        row = [time, *[item if item else "-" for item in data]]

        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    historico = input()
    entrada.escrever_json(historico)
    students = read_file("resultado.json")

    #for index, student in enumerate(students):
        #course = student["curso"]
        #period = student["periodo"]
        #pending = student["disciplinas_pendentes"]

        #print("{:02} - Curso: {} - Periodo: {} - Matérias Pendentes: {}".format(index + 1, course.upper(), period, len(pending)))

    #option = int(input("Escolha um dataset: "))
    #student = students[option - 1]

    course = students["curso"]
    period = students["periodo"]
    pending = students["disciplinas_pendentes"]

    data = read_file(f"disc-{course}.json")
    disciplines = {disc["sigla"]: disc for disc in data}
    top_order = topological_sorting(disciplines, pending, period)
    optatives = get_optatives_disciplines(data)

    (recommendations, conflicted, total, grid) = get_recommended_courses(disciplines, optatives, top_order, students)

    print("\nCurso: {} - Periodo: {} - Matérias Pendentes: {}".format(course.upper(), period, len(pending)))
    print("\n{} Matérias Sugeridas {}\n".format("*" * 20, "*" * 20))

    display_recommendations(recommendations)
    print(f"Carga Horaria Total: {total}h")

    print("\n{} Grade Horária Estimada {}\n".format("*" * 20, "*" * 20))
    display_schedule_table(grid)
    #print(conflicted)
