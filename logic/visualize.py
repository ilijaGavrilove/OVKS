import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from logic import load, sugiyama_layout, radial_layout

def visualize_network(input_file, output_file=None, method='sugiyama'):
    """
    Основная функция: загружает сеть, применяет выбранный метод и сохраняет результат.
    """
    G = load.load_graph(input_file)
    
    # Проверка на типичную звёздную топологию (центральный узел + листья)
    if method == 'auto':
        degrees = dict(G.degree())
        if len(G) > 2 and max(degrees.values()) == len(G)-1 and list(degrees.values()).count(1) == len(G)-1:
            method = 'radial'
        else:
            method = 'sugiyama'
    
    if method == 'radial':
        pos = radial_layout.radial_layout(G)
        fig, ax = plt.subplots(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color='gray',
                node_size=800, font_size=10, ax=ax)
        ax.set_title("Радиальная визуализация сети")
        ax.axis('equal')
    else:
        layout = sugiyama_layout.SugiyamaLayout(G)
        layout.run()
        fig, ax = layout.draw()
        # Вывод метрик
        total_edges = G.number_of_edges()
        # Приблизительное число пересечений (не вычисляем точно, в реализации оно минимизировано)
        print(f"Визуализация завершена. Узлов: {G.number_of_nodes()}, рёбер: {total_edges}")
    
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file, dpi=150)
        print(f"Схема сохранена в {output_file}")
    plt.show()