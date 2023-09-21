import json
import networkx as nx
import matplotlib.pyplot as plt

# 从JSON文件加载数据并构建数据结构树
def build_tree(data):
    if isinstance(data, dict):
        return {key: build_tree(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [build_tree(item) for item in data]
    else:
        return data

def print_tree(tree, indent=0):
    if isinstance(tree, dict):
        for key, value in tree.items():
            print("  " * indent + f"Key: {key}")
            print_tree(value, indent + 1)
    elif isinstance(tree, list):
        for item in tree:
            print_tree(item, indent)
    else:
        print("  " * indent + f"Value: {tree}")

# 绘制树结构
def draw_tree(tree):

    G = nx.DiGraph()

    def add_nodes_edges(graph, parent_name, tree_data):
        #加异常处理
        try:
            assert isinstance(tree_data, (dict, list))
        except:
            print("tree_data is not a dict or list!")
        if isinstance(tree_data, dict):
            #exception handling
            try:
                assert len(tree_data.keys()) == 1
            except:
                print("tree_data.keys() is not 1!")
            for key, value in tree_data.items():
                node_name = f"{parent_name}_{key}"
                graph.add_node(node_name, label=key)
                graph.add_edge(parent_name, node_name)
                add_nodes_edges(graph, node_name, value)
        elif isinstance(tree_data, list):
            for idx, item in enumerate(tree_data):
                node_name = f"{parent_name}_{idx}"
                graph.add_node(node_name, label=f"[{idx}]")
                graph.add_edge(parent_name, node_name)
                add_nodes_edges(graph, node_name, item)
        else:
            graph.add_node(parent_name, label=str(tree_data))

    add_nodes_edges(G, "Root", tree)
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, "label")
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=800, node_color="lightblue", font_size=10, font_color="black", font_weight="bold", arrows=True, arrowstyle="->")
    plt.show()

# 指定JSON文件路径
json_file_path = '../sample_contracts/REAst/test.json'

# 从JSON文件加载数据
try:
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # 构建数据结构树
    data_tree = build_tree(json_data)

    # 打印数据结构树
    print_tree(data_tree)

    # 绘制数据结构树
    draw_tree(data_tree)

except FileNotFoundError:
    print(f"JSON文件 '{json_file_path}' 未找到。")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")


# import json
# import networkx as nx
# import matplotlib.pyplot as plt

# def build_tree(data):
#     if isinstance(data, dict):
#         return {key: build_tree(value) for key, value in data.items()}
#     elif isinstance(data, list):
#         return [build_tree(item) for item in data]
#     else:
#         return data

# def print_tree(tree, indent=0):
#     if isinstance(tree, dict):
#         for key, value in tree.items():
#             print("  " * indent + f"Key: {key}")
#             print_tree(value, indent + 1)
#     elif isinstance(tree, list):
#         for item in tree:
#             print_tree(item, indent)
#     else:
#         print("  " * indent + f"Value: {tree}")

# # 指定JSON文件路径
# json_file_path = '../sample_contracts/REAst/test.json'

# # 从JSON文件加载数据
# try:
#     with open(json_file_path, 'r') as json_file:
#         json_data = json.load(json_file)

#     # 构建数据结构树
#     data_tree = build_tree(json_data)

#     # 打印数据结构树
#     print_tree(data_tree)
# except FileNotFoundError:
#     print(f"JSON文件 '{json_file_path}' 未找到。")
# except json.JSONDecodeError as e:
#     print(f"JSON解析错误: {e}")


# # 创建一个有向图对象
# G = nx.DiGraph()

# # 添加节点
# G.add_node("Root")
# G.add_node("Node1")
# G.add_node("Node2")
# G.add_node("Node3")

# # 添加边连接节点
# G.add_edge("Root", "Node1")
# G.add_edge("Root", "Node2")
# G.add_edge("Node2", "Node3")

# # 使用布局算法布置节点位置
# pos = nx.spring_layout(G)

# # 绘制树结构
# nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", font_size=10, font_color="black", font_weight="bold", arrows=True, arrowstyle="->")
# plt.show()