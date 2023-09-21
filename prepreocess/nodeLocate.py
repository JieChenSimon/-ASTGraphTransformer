import ast
import json

# 指定JSON文件路径
json_file_path = '../sample_contracts/REAst/test.json'

# 读取JSON文件内容
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# 构建抽象语法树
# 将JSON数据对象转换为字符串
source_code = json.dumps(json_data)
tree = ast.parse(json_data)

# 为AST节点分配位置编码的函数
def assign_node_codes(node, parent_code=""):
    node.code = parent_code
    for i, child in enumerate(ast.iter_child_nodes(node)):
        child_code = f"{parent_code}.{i}"
        assign_node_codes(child, child_code)

# 初始化根节点编码
root_code = "0"

# 为AST树中的节点分配位置编码
assign_node_codes(tree, root_code)

# 打印每个节点的位置编码、类型和名称
for node in ast.walk(tree):
    node_type = type(node).__name__
    node_name = ""
    if isinstance(node, ast.Name):
        node_name = node.id
    print(f"Node Code: {node.code}, Node Type: {node_type}, Node Name: {node_name}")
