# visualize.py
from pyvis.network import Network
import json
import os
from pathlib import Path

def visualize_network(G, positions, output_path="network_viz.html", scale=150):
    # Загрузка путей к иконкам (безопасный путь относительно ЭТОГО файла)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_file = os.path.join(base_dir, 'images.json')
    with open(images_file, 'r') as f:
        images = json.load(f)

    net = Network(height="700px", width="100%",
                  directed=G.is_directed(),
                  notebook=False)

    # Отключаем физику и включаем автоматический fit при старте
    options = {
        "physics": {
            "enabled": False
        },
        "interaction": {
            "zoomView": True,
            "dragView": True
        },
        "layout": {
            "hierarchical": False
        },
        "autoResize": True,
        "fit": True  # явно указываем подгонять вид под данные
    }
    net.set_options(json.dumps(options))  # передаём как JSON-строку

    for node in G.nodes():
        x, y = positions[node]
        node_type = G.nodes[node].get('type', 'default')
        image_path = images.get(node_type)  # путь к файлу иконки

        # Если нужна иконка, используем base64 (безопасно для локального HTML)
        if image_path and os.path.exists(image_path):
            import base64
            with open(image_path, 'rb') as img_file:
                encoded = base64.b64encode(img_file.read()).decode('utf-8')
            mime = 'image/png' if image_path.endswith('.png') else 'image/jpeg'
            image_url = f'data:{mime};base64,{encoded}'
            net.add_node(node, label=str(node),
                         x=x * scale, y=y * scale,
                         shape='image', image=image_url,
                         physics=False, size=25)
        else:
            net.add_node(node, label=str(node),
                         x=x * scale, y=y * scale,
                         physics=False, size=25)

    for u, v, data in G.edges(data=True):
        weight = data.get('weight', '')
        title = f"Вес: {weight}" if weight else ""
        net.add_edge(u, v, title=title)

    net.save_graph(output_path)

    if not os.path.isabs(output_path):
    # Сохраняем в папку Documents текущего пользователя
        home = os.path.expanduser("~")
        output_path = os.path.join(home, "Documents", output_path)
    # Патч: добавляем принудительный fit после загрузки страницы
    with open(output_path, 'a') as f:
        f.write('''
<script>
  window.addEventListener('load', function() {
    if (window.network) {
      window.network.fit({ animation: true });
    }
  });
</script>
''')
    print(f"Интерактивная схема сохранена в {output_path}")