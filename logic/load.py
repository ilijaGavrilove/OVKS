import json
import networkx as nx

def load_graph(file_path):
    """
    Загружает описание топологии из файла.
    Поддерживаемые форматы:
    - txt: список рёбер (каждая строка: u v [вес])
    - csv/matrix: матрица смежности (первая строка - заголовки узлов)
    - json: {"nodes": [id1, id2, ...], "edges": [[u, v, w], ...], "directed": true/false}
    Возвращает граф networkx (ориентированный или неориентированный)
    """
    print(f'file_path: {file_path}')
    ext = file_path.split('.')[-1].lower()
    print(f"ext: {ext}")
    
    if ext == 'json':
        with open(file_path, 'r') as f:
            data = json.load(f)
        directed = data.get('directed', False)
        G = nx.DiGraph() if directed else nx.Graph()
        G.add_nodes_from(data['nodes'])
        for edge in data['edges']:
            if len(edge) == 3:
                u, v, w = edge
                G.add_edge(u, v, weight=w)
            else:
                u, v = edge
                G.add_edge(u, v)
        return G

    elif ext in ['txt', 'csv']:
        # Предполагаем список рёбер
        edges = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
        # Если первая строка выглядит как матрица (много чисел), то это матрица смежности
        if len(lines) > 0 and len(lines[0].strip().split()) > 2:
            return _load_adjacency_matrix(lines)
        # Иначе список рёбер
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            u, v = parts[0], parts[1]
            w = float(parts[2]) if len(parts) >= 3 else 1.0
            edges.append((u, v, w))
        # По умолчанию создаём неориентированный граф (физическая топология)
        G = nx.Graph()
        for u, v, w in edges:
            G.add_edge(u, v, weight=w)
        return G
    else:
        raise ValueError("Неподдерживаемый формат файла")

def _load_adjacency_matrix(lines):
    """Загрузка из матрицы смежности."""
    # Первая строка может быть заголовком или нумерацией
    nodes = []
    matrix = []
    header = lines[0].strip().split()
    # Если первый элемент не число, считаем заголовками
    if not header[0].isdigit():
        nodes = header
        for line in lines[1:]:
            matrix.append([float(x) for x in line.strip().split()])
    else:
        # Номера строк = номера столбцов = 0..n-1
        n = len(header)
        nodes = [str(i) for i in range(n)]
        for line in lines:
            matrix.append([float(x) for x in line.strip().split()])
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    n = len(nodes)
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] != 0:
                G.add_edge(nodes[i], nodes[j], weight=matrix[i][j])
    return G
