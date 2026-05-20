import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

class SugiyamaLayout:
    """
    Реализация пяти этапов метода Сугиямы для иерархической визуализации.
    """
    def __init__(self, G):
        self.original_graph = G.copy()
        self.G = G.copy()
        self.layers = []          # список списков узлов по слоям
        self.positions = {}       # итоговые координаты {узел: (x, y)}
        self.edges_virtual = []   # рёбра с виртуальными узлами для отрисовки
        
    def run(self):
        """Выполнение всех этапов."""
        # Этап 1: Разрешение циклов
        self._break_cycles()
        # Если граф стал пустым по рёбрам (все были в циклах), используем исходный
        if self.G.number_of_edges() == 0:
            self.G = self.original_graph.copy()
        # Этап 2: Слоистое размещение
        self._assign_layers()
        # Этап 3: Минимизация пересечений
        self._minimize_crossings()
        # Этап 4: Позиционирование узлов
        self._assign_coordinates()
        # Этап 5: Рисование рёбер (формирование виртуальных узлов для полилиний)
        self._prepare_edges()
        
    # ----------------------------------------------
    # ЭТАП 1: РАЗРЕШЕНИЕ ЦИКЛОВ (п. 2.3.1)
    # ----------------------------------------------
    def _break_cycles(self):
        """
        Преобразует орграф (или неориентированный граф) в ациклический.
        Для неориентированного графа произвольно задаём направление,
        затем разворачиваем часть рёбер для устранения циклов.
        """
        # Если граф неориентированный, делаем его ориентированным (произвольное направление)
        if not self.G.is_directed():
            self.G = self.G.to_directed()
        # Удаляем циклы: ищем рёбра, участие которых в циклах минимально,
        # и временно разворачиваем их (сохраняем оригинальные для последующей отрисовки)
        while True:
            try:
                cycle = nx.find_cycle(self.G, orientation='original')
                # Выбираем ребро с наименьшим весом (или первое) для разворота
                edge_to_flip = min(cycle, key=lambda e: self.G.edges[e[0], e[1]].get('weight', 1))
                u, v, _ = edge_to_flip
                # Разворачиваем ребро
                self.G.remove_edge(u, v)
                self.G.add_edge(v, u, flipped=True, weight=self.original_graph.edges[u, v].get('weight', 1))
            except nx.NetworkXNoCycle:
                break

    # ----------------------------------------------
    # ЭТАП 2: СЛОИСТОЕ РАЗМЕЩЕНИЕ (п. 2.3.2)
    # ----------------------------------------------
    def _assign_layers(self):
        """
        Назначает слои, стремясь минимизировать высоту схемы.
        Использует алгоритм "длиннейшего пути" от истоков до стоков.
        """
        if not self.G.is_directed():
            self.G = self.G.to_directed()
        
        # Топологическая сортировка невозможна для графа с циклами, но мы их уже убрали
        # Находим все источники (нет входящих рёбер)
        in_degree = dict(self.G.in_degree())
        sources = [n for n, deg in in_degree.items() if deg == 0]
        if not sources:
            # Если источников нет (полный цикл, но мы их развернули), берём все узлы
            sources = list(self.G.nodes())
        
        # Обход в ширину с накоплением максимального расстояния
        layer_of = {}
        queue = []
        for s in sources:
            layer_of[s] = 0
            queue.append(s)
        while queue:
            u = queue.pop(0)
            for v in self.G.successors(u):
                new_layer = layer_of[u] + 1
                if v not in layer_of or layer_of[v] < new_layer:
                    layer_of[v] = new_layer
                    queue.append(v)
        
        # Обрабатываем узлы, не достигнутые из источников (изолированные)
        for n in self.G.nodes():
            if n not in layer_of:
                layer_of[n] = 0
        
        # Группируем узлы по слоям
        max_layer = max(layer_of.values())
        self.layers = [[] for _ in range(max_layer + 1)]
        for n, l in layer_of.items():
            self.layers[l].append(n)

    # ----------------------------------------------
    # ЭТАП 3: МИНИМИЗАЦИЯ ПЕРЕСЕЧЕНИЙ (п. 2.3.3)
    # ----------------------------------------------
    def _minimize_crossings(self):
        """
        Применяет барицентрическую эвристику и жадный обмен
        для уменьшения числа пересечений между соседними слоями.
        """
        # Число итераций вверх-вниз
        for iteration in range(10):
            # Проход сверху вниз
            for i in range(len(self.layers) - 1):
                self._barycenter_order(i, i+1)
            # Проход снизу вверх
            for i in range(len(self.layers)-1, 0, -1):
                self._barycenter_order(i, i-1)
            # Жадное улучшение на каждом слое
            for i in range(len(self.layers)):
                self._greedy_swap(i)

    def _barycenter_order(self, fixed_layer_idx, free_layer_idx):
        """Упорядочивает узлы free_layer по среднему арифметическому позиций соседей из fixed_layer."""
        fixed_layer = self.layers[fixed_layer_idx]
        free_layer = self.layers[free_layer_idx]
        # Вычисляем барицентрические веса
        bary = {}
        for node in free_layer:
            if fixed_layer_idx > free_layer_idx:
                # соседи сверху (предшественники)
                neighbors = list(self.G.predecessors(node))
            else:
                # соседи снизу (последователи)
                neighbors = list(self.G.successors(node))
            # Позиция соседа в fixed_layer (индекс)
            positions = [fixed_layer.index(n) for n in neighbors if n in fixed_layer]
            if positions:
                bary[node] = np.mean(positions)
            else:
                bary[node] = float('inf')  # узлы без соседей прижимаем к левому краю
        # Сортируем свободный слой по барицентру
        self.layers[free_layer_idx] = sorted(free_layer, key=lambda n: bary[n])

    def _greedy_swap(self, layer_idx):
        """Жадно меняет пары узлов на одном слое, если это уменьшает общее число пересечений."""
        layer = self.layers[layer_idx]
        changed = True
        while changed:
            changed = False
            for i in range(len(layer)-1):
                # Текущее количество пересечений с соседними слоями
                crossings_before = self._layer_crossings(layer_idx)
                # Меняем местами
                layer[i], layer[i+1] = layer[i+1], layer[i]
                crossings_after = self._layer_crossings(layer_idx)
                if crossings_after < crossings_before:
                    changed = True
                else:
                    # Возвращаем обратно
                    layer[i], layer[i+1] = layer[i+1], layer[i]

    def _layer_crossings(self, layer_idx):
        """Подсчёт числа пересечений рёбер между слоем layer_idx и соседними."""
        total = 0
        if layer_idx > 0:
            total += self._crossings_between(layer_idx-1, layer_idx)
        if layer_idx < len(self.layers)-1:
            total += self._crossings_between(layer_idx, layer_idx+1)
        return total

    def _crossings_between(self, top_idx, bottom_idx):
        """Число пересечений рёбер между двумя соседними слоями."""
        top = self.layers[top_idx]
        bottom = self.layers[bottom_idx]
        # Собираем рёбра: (позиция_в_верхнем_слое, позиция_в_нижнем_слое)
        edges = []
        for u in top:
            for v in self.G.successors(u):
                if v in bottom:
                    edges.append((top.index(u), bottom.index(v)))
        # Считаем инверсии
        crossings = 0
        for (a1, b1), (a2, b2) in combinations(edges, 2):
            if (a1 - a2) * (b1 - b2) < 0:
                crossings += 1
        return crossings

    # ----------------------------------------------
    # ЭТАП 4: ПОЗИЦИОНИРОВАНИЕ УЗЛОВ (п. 2.3.4)
    # ----------------------------------------------
    def _assign_coordinates(self):
        """Назначает точные координаты (x, y) с учётом компактности и симметрии."""
        num_layers = len(self.layers)
        # Вертикальное расстояние между слоями
        y_gap = 2.0
        # Горизонтальный интервал между узлами
        x_gap = 1.0
        
        for i, layer in enumerate(self.layers):
            y = -i * y_gap  # верхний слой вверху (положительный y в matplotlib вниз)
            n = len(layer)
            if n == 0:
                continue
            # Равномерно распределяем узлы по горизонтали с центрированием
            for j, node in enumerate(layer):
                # Центрирование: общая ширина (n-1)*x_gap, смещение на половину
                x = (j - (n-1)/2.0) * x_gap
                self.positions[node] = (x, y)

    # ----------------------------------------------
    # ЭТАП 5: ПОДГОТОВКА РЁБЕР (п. 2.3.5)
    # ----------------------------------------------
    def _prepare_edges(self):
        """
        Преобразует исходные рёбра в ломаные линии с виртуальными точками
        на каждом пересекаемом слое, чтобы избежать прохода сквозь узлы.
        """
        self.edge_paths = {}  # (u, v) -> список точек (x,y)
        for u, v in self.original_graph.edges():
            # Определяем слои узлов (могут отсутствовать, если узел был удалён)
            layer_u = None
            layer_v = None
            for i, layer in enumerate(self.layers):
                if u in layer:
                    layer_u = i
                if v in layer:
                    layer_v = i
            if layer_u is None or layer_v is None:
                continue  # узел не участвует в визуализации
            
            # Убедимся, что ребро направлено вниз (layer_u < layer_v)
            if layer_u > layer_v:
                u, v = v, u
                layer_u, layer_v = layer_v, layer_u
            
            points = [self.positions[u]]
            # Добавляем промежуточные точки на каждом слое между layer_u и layer_v
            for l in range(layer_u + 1, layer_v):
                # Виртуальный узел в центре слоя l по горизонтали
                # Определяем x-координату как среднее между соседними реальными узлами
                x_mid = np.mean([self.positions[n][0] for n in self.layers[l]])
                y = -l * 2.0
                points.append((x_mid, y))
            points.append(self.positions[v])
            self.edge_paths[(u, v)] = points

    # ----------------------------------------------
    # ВИЗУАЛИЗАЦИЯ
    # ----------------------------------------------
    def draw(self, title="Визуализация компьютерной сети (метод Сугиямы)"):
        """Отрисовывает граф с использованием matplotlib."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Рисуем рёбра полилиниями
        for (u, v), path in self.edge_paths.items():
            xs = [p[0] for p in path]
            ys = [p[1] for p in path]
            ax.plot(xs, ys, 'k-', linewidth=1.2, alpha=0.7, zorder=1)
        
        # Рисуем узлы
        for node, (x, y) in self.positions.items():
            ax.scatter(x, y, s=500, c='lightblue', edgecolors='navy', zorder=2)
            ax.text(x, y, str(node), ha='center', va='center', fontsize=9, zorder=3)
        
        ax.set_title(title, fontsize=14)
        ax.axis('equal')
        ax.axis('off')
        plt.tight_layout()
        return fig, ax