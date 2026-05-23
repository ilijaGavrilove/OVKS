from collections import defaultdict
import numpy as np

def radial_layout(G, center_node=None):
    """Радиальная укладка для графов с явным центром."""
    if center_node is None:
        # Выбираем узел с максимальной степенью как центр
        degrees = dict(G.degree())
        center_node = max(degrees, key=degrees.get)
    
    # Определяем расстояния от центра (BFS)
    levels = defaultdict(list)
    visited = {center_node: 0}
    queue = [center_node]
    while queue:
        u = queue.pop(0)
        for v in G.neighbors(u):
            if v not in visited:
                visited[v] = visited[u] + 1
                queue.append(v)
    for node, level in visited.items():
        levels[level].append(node)
    
    pos = {}
    for level, nodes in levels.items():
        if level == 0:
            pos[center_node] = (0, 0)
        else:
            n = len(nodes)
            radius = level * 2.0
            for i, node in enumerate(nodes):
                angle = 2 * np.pi * i / n
                pos[node] = (radius * np.cos(angle), radius * np.sin(angle))
    return pos