from mitmproxy import ctx
import importlib.util
import json
import base64
import os
import atexit
import sys

# 打开并读取文件内容
def resource_path(relative_path):
    try:
        # PyInstaller 创建打包文件后的临时文件夹
        base_path = sys._MEIPASS
    except AttributeError:
        # 未打包时的路径
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 使用 resource_path 函数获取 data.txt 文件的路径
data_file_path = resource_path("data.txt")


def create_and_load_temp_module(file_name, func_name):
    temp_module_name = f"temp_module_{os.path.splitext(os.path.basename(file_name))[0]}"
    temp_module_path = f"/tmp/{temp_module_name}.py"
    
    # 读取文件内容并写入临时文件
    with open(file_name, "r",encoding='utf-8') as f:
        code = f.read()
    with open(temp_module_path, "w",encoding='utf-8') as f:
        f.write(code)

    # 动态加载临时模块
    spec = importlib.util.spec_from_file_location(temp_module_name, temp_module_path)
    temp_module = importlib.util.module_from_spec(spec)
    sys.modules[temp_module_name] = temp_module
    spec.loader.exec_module(temp_module)
    # 在脚本结束时清理临时文件
    atexit.register(os.remove, temp_module_path)    
    # 返回模块名和函数名（如果函数存在的话）
    if hasattr(temp_module, func_name):
        return temp_module_name, func_name
    else:
        ctx.log.error(f"{func_name} and {file_name}")
        return None, None
# 读取 IP 和端口
ip, port = None, None
try:
    with open(data_file_path, 'r') as file:
        line = file.readline().strip()
        parts = line.split(':')
        if len(parts) == 2:
            ip = parts[0].strip()
            port = int(parts[1].strip())
        else:
            ctx.log.error("Error: The file content does not match the expected format (IP:Port)")
except Exception as e:
    ctx.log.error(f"Error reading data.txt: {e}")

class Mimit:
    # 处理来自Burp的请求，通常在这里对请求进行加密
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        Requestencryption_method=resource_path("Requestencryption_method.txt")
        Responsedecryption_method=resource_path("Responsedecryption_method.txt")
        # 创建和加载第一个临时模块
        self.module1_name, self.func1_name = create_and_load_temp_module(Requestencryption_method, "Requestencryption_data")
        # 创建和加载第二个临时模块
        self.module2_name, self.func2_name = create_and_load_temp_module(Responsedecryption_method, "Responsedecryption_data")
    def request(self, flow):
        print(ip)
        if flow.request.host == f"{self.ip}" and flow.request.port == self.port and flow.request.method == "POST":
            try:
                # 加密请求数据
                getattr(sys.modules[self.module1_name], self.func1_name)(flow)
            except :
                ctx.log.error("1")
    #处理返回给客户端的响应，通常在这里对响应进行解密
    def response(self, flow):
        if flow.request.host == f"{self.ip}" and flow.request.port == self.port:
            try:
                # 解密响应数据
                getattr(sys.modules[self.module2_name], self.func2_name)(flow)
            except Exception as e:
                ctx.log.error(f"处理请求时出错: {e}")

# 创建 Mimit 实例（如果 IP 和端口有效）
addons = []
if ip and port:
    addons.append(Mimit(ip, port))
else:
    ctx.log.error("Failed to initialize Mimit instance due to invalid IP or port from data.txt.")