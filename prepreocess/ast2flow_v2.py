import json
import re
import subprocess
import solcx
from solcx import compile_standard
import os
import signal
import time

def timeout_handler(signum, frame):
    raise TimeoutError("Execution took longer than 1 hour")

signal.signal(signal.SIGALRM, timeout_handler)

def solidity_to_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    input_json = {
        "language": "Solidity",
        "sources": {
            "source code": {
                "content": content
            }
        },
        "settings": {
            "optimizer": {
                "enabled": True,
                "runs": 200
            },
            "evmVersion": "byzantium",
            "metadata": {
                "useLiteralContent": True
            },
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode", "evm.bytecode.sourceMap"
                    ],
                    "": [
                        "ast"
                    ]
                }
            }
        }
    }

    return input_json
def switch_solc_version(solidity_file_path):
    with open(solidity_file_path, "r") as file:
        solidity_code = file.read()

    pragma_version = re.search(r'pragma solidity (\^?[\d.]+);', solidity_code)
    if pragma_version:
        version = pragma_version.group(1)
        version = version.replace('^', '')

        # 获取可用版本列表
        available_versions_output = subprocess.run(["solc-select", "versions"], capture_output=True, text=True)
        available_versions = available_versions_output.stdout.split()

        # 检查所需版本是否已安装
        if version not in available_versions:
            # 安装缺失的版本
            print(f"Installing solc {version}...")
            subprocess.run(["solc-select", "install", version], check=True)

        # 切换到所需版本
        print(f"Switching to solc {version}...")
        subprocess.run(["solc-select", "use", version], check=True)
    else:
        raise ValueError("Cannot find the Solidity version pragma in the source code.")




# 依此读取RE_deduplication_smart_contracts文件夹下的中的所有sol文件
for root, dirs, files in os.walk("../sample_contracts/test_sol"):
    for file in files:
        if file.endswith(".sol"):
            print(f"Processing {file}...")
            solidity_file_path = os.path.join(root, file)

            #加一个异常处理,如果下面的solc命令出错,则跳过这个sol文件
            try:
                # 为单次执行设置1小时的超时
                signal.alarm(60 * 5)
                start_time = time.time()
                switch_solc_version(solidity_file_path)
                # solc_command = f"solc --ast-json {solidity_file_path}"
                # solc_output = subprocess.check_output(solc_command, shell=True, text=True)
                # print(type(solc_output))
                input_json = solidity_to_json(solidity_file_path)
                input_json= solcx.compile_standard(input_json)
                end_time = time.time()

                #将solc_output写入一个文件夹下的中的sol文件同名的json文件中
                # 获取 JSON 文件名（与 Solidity 文件同名，只是后缀改成 .json）
                json_file_path = os.path.join("../sample_contracts/REAst", file[:-4] + ".json")
                print(json_file_path)
                
            except TimeoutError as te:
                print(f"Skipping {solidity_file_path} due to timeout: {te}")
                with open("../sample_contracts/log/skipped_files.txt", "a") as file:
                    file.write(f"{solidity_file_path}\n")
            except Exception as e:
                print(f"Failed to extract AST from {solidity_file_path}: {e}")
                with open("../sample_contracts/log/failed_files.txt", "a") as file:
                    file.write(f"{solidity_file_path}\n")

            
            # with open(json_file_path, 'w', encoding='utf-8') as f:
            #     json.dump(input_json, f, ensure_ascii=False, indent=2)
            
            # #输出当前sol已经生成AST完成
            # print(f"AST Finished processing {file}.")
            # print("--------------------------------------------------")
            else:
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(input_json, f, ensure_ascii=False, indent=2)

                processing_time = end_time - start_time
                print(f"AST Finished processing {file}.")
                print("--------------------------------------------------")
                
                with open("../sample_contracts/log/successful_time_record.txt", "a") as file:
                    file.write(f"{solidity_file_path} - {processing_time:.2f} seconds\n")
            
            #将solc_output写入一个新建在dataset文件夹里的json文件



# # 将solc_output字符串转换为Python字典
# output_json = json.loads(solc_output)
# ast = output_json["sources"]["example.sol"]["AST"]

# # 递归遍历AST，提取控制流和数据流信息
# def process_node(node):
#     if node["nodeType"] == "FunctionDefinition":
#         print(f"Function: {node['name']}")

#     elif node["nodeType"] == "VariableDeclaration":
#         print(f"Variable: {node['name']}")

#     elif node["nodeType"] == "IfStatement":
#         print("If statement")

#     for key, value in node.items():
#         if isinstance(value, dict):
#             process_node(value)
#         elif isinstance(value, list):
#             for item in value:
#                 if isinstance(item, dict):
#                     process_node(item)

# process_node(ast)