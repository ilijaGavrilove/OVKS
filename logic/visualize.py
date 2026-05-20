from pyvis.network import Network

def visualize_network(G, positions, output_path="network_viz.html", scale=150):
    print(positions)
    """
    Создаёт интерактивную HTML-визуализацию.
    Аргумент scale умножает координаты, чтобы узлы не слипались.
    """
    net = Network(height="700px", width="100%",
                  directed=G.is_directed(),
                  notebook=False)

    # Отключаем физику, чтобы узлы оставались на заданных местах
    net.toggle_physics(False)

    for node in G.nodes():
        x, y = positions[node]
        # Умножаем координаты на масштаб и разворачиваем Y (если нужно)
        # В ваших координатах y отрицателен для нижних слоёв.
        # PyVis по умолчанию направляет Y вверх, но это не критично.
        # Просто масштабируем.
        net.add_node(node, label=str(node),
                     x=x * scale,
                     y=y * scale,
                     physics=False,
                     size=25)

    for u, v, data in G.edges(data=True):
        weight = data.get('weight', '')
        title = f"Вес: {weight}" if weight else ""
        net.add_edge(u, v, title=title)

    # Дополнительно фиксируем область отображения, чтобы не было автоцентрирования
    net.set_options("""
    var options = {
      "layout": {
        "hierarchical": false
      },
      "physics": {
        "enabled": false
      },
      "interaction": {
        "zoomView": true,
        "dragView": true
      }
    }
    """)

    net.save_graph(output_path)
    print(f"Интерактивная схема сохранена в {output_path}")