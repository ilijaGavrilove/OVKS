import json
import networkx as nx
from logic import sugiyama_layout, radial_layout

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

        for node_data in data['nodes']:
            # Поддержка двух форматов:
            if isinstance(node_data, str):
                # Старый формат: просто имя узла
                node_id = node_data
                node_type = 'default'
            elif isinstance(node_data, dict):
                # Новый формат: {"id": "Router1", "type": "router"}
                node_id = node_data['id']
                node_type = node_data.get('type', 'default')
            else:
                raise ValueError(f"Неверный формат узла: {node_data}")
        
            G.add_node(node_id, type=node_type)

        for edge in data['edges']:
            u, v = edge[0], edge[1]
            weight = edge[2] if len(edge) > 2 else 1.0
            G.add_edge(u, v, weight=weight)

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

def compute_layout(G, method='auto', center_node=None):
    """
    Автоматически выбирает и применяет лучший метод визуализации.
    Пользователь может принудительно задать 'sugiyama' или 'radial',
    но по умолчанию ('auto') программа анализирует топологию сама.
    """
    if method == 'auto':
        # Автоматическое определение (как в visualize_network)
        degrees = dict(G.degree())
        if len(G) > 2 and max(degrees.values()) == len(G) - 1 \
                and list(degrees.values()).count(1) == len(G) - 1:
            method = 'radial'
        else:
            method = 'sugiyama'
    
    if method == 'radial':
        return radial_layout.radial_layout(G, center_node)
    else:  # sugiyama
        layout = sugiyama_layout.SugiyamaLayout(G)
        layout.run()
        return layout.positions