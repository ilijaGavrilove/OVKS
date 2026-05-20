import networkx as nx
from sugiyama_layout import SugiyamaLayout
from gui import visualize_network
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Создадим тестовый граф, моделирующий трёхуровневую сеть Cisco (ядро, распределение, доступ)
    test_graph = nx.DiGraph()
    # Уровень ядра
    test_graph.add_node("Core1", layer=0)
    test_graph.add_node("Core2", layer=0)
    # Уровень распределения
    test_graph.add_node("Dist1", layer=1)
    test_graph.add_node("Dist2", layer=1)
    # Уровень доступа
    test_graph.add_node("Acc1", layer=2)
    test_graph.add_node("Acc2", layer=2)
    test_graph.add_node("Acc3", layer=2)
    # Связи
    test_graph.add_edges_from([
        ("Core1", "Dist1"), ("Core1", "Dist2"),
        ("Core2", "Dist1"), ("Core2", "Dist2"),
        ("Dist1", "Acc1"), ("Dist1", "Acc2"),
        ("Dist2", "Acc2"), ("Dist2", "Acc3"),
    ])
    
    # Запуск визуализации
    layout = SugiyamaLayout(test_graph)
    layout.run()
    fig, ax = layout.draw("Пример трёхуровневой сети (Cisco)")
    plt.savefig("network_sugiyama.png", dpi=150)
    plt.show()