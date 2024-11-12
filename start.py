import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

class EnAndDeProxyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EnAndDe加解密代理")
        self.width, self.height = 900, 650
        self.position_window()
        self.create_widgets()
        self.load_config()

    #中间
    def position_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - self.height / 2)
        position_right = int(screen_width / 2 - self.width / 2)
        self.root.geometry(f'{self.width}x{self.height}+{position_right}+{position_top}')

    def load_config(self):
        try:
            with open('data.txt', 'r') as file:
                content = file.read().strip()
                if ':' in content:
                    ip, port_str = content.split(':')
                    self.ip_var.set(ip)
                    self.target_port_var.set(port_str)
        except FileNotFoundError:
            pass
    def save_file_content(self, file_path, text_widget):
        content = text_widget.get(1.0, tk.END).strip()
        if content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            messagebox.showwarning("无内容可保存", "文本框内容为空，未进行保存。")

    def handle_save(self):
        Requestencryption_method_path = "Requestencryption_method.txt"
        Requestdecryption_method_path = "Requestdecryption_method.txt"
        Responseencryption_method_path = "Responseencryption_method.txt"
        Responsedecryption_method_path = "Responsedecryption_method.txt"
        self.save_file_content(Requestencryption_method_path, self.text_box1)
        self.save_file_content(Requestdecryption_method_path, self.text_box2)
        self.save_file_content(Responseencryption_method_path, self.text_box3)
        self.save_file_content(Responsedecryption_method_path, self.text_box4)
    #端口
    def validate_port(self, port):
        try:
            port = int(port)
            if 1 <= port <= 65535:
                return port
            else:
                raise ValueError("端口号必须在1到65535之间")
        except ValueError:
            raise ValueError("端口号必须是有效的整数")

    #创建组件
    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # 输入框和标签
        tk.Label(self.frame, text="请求的域名（IP）:",font=5).grid(row=0, column=0, sticky='e',padx=10, pady=10)
        self.ip_var = tk.StringVar()
        self.ip_entry = tk.Entry(self.frame, textvariable=self.ip_var)
        self.ip_entry.grid(row=0, column=1, sticky='w')

        tk.Label(self.frame, text="目标端口 (默认80):",font=5).grid(row=0, column=2, sticky='e',padx=10, pady=10)
        self.target_port_var = tk.StringVar()
        self.target_port_entry = tk.Entry(self.frame, textvariable=self.target_port_var)
        self.target_port_entry.insert(0, "80")
        self.target_port_entry.grid(row=0, column=3, sticky='w')

        tk.Label(self.frame, text="浏览器代理端口 (默认7070):",font=5).grid(row=1, column=1, sticky='e',padx=10, pady=10)
        self.port1_var = tk.StringVar()
        self.port1_entry = tk.Entry(self.frame, textvariable=self.port1_var)
        self.port1_entry.insert(0, "7070")
        self.port1_entry.grid(row=1, column=2, sticky='w')

        tk.Label(self.frame, text="Burp本地端口 (默认8080):",font=5).grid(row=2, column=1, sticky='e',padx=10, pady=10)
        self.port2_var = tk.StringVar()
        self.port2_entry = tk.Entry(self.frame, textvariable=self.port2_var)
        self.port2_entry.insert(0, "8080")
        self.port2_entry.grid(row=2, column=2, sticky='w')

        tk.Label(self.frame, text="Burp上游代理端口 (默认9090):",font=5).grid(row=3, column=1, sticky='e',padx=10, pady=10)
        self.burp_port_var = tk.StringVar()
        self.burp_entry = tk.Entry(self.frame, textvariable=self.burp_port_var)
        self.burp_entry.insert(0, "9090")
        self.burp_entry.grid(row=3, column=2, sticky='w')
        
        
        # Text小部件
        tk.Label(self.root, text="Requestencryption_data请求包解密方法",font=8).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.text_box1 = scrolledtext.ScrolledText(self.root, width=50, height=10, wrap=tk.WORD)
        self.text_box1.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

        tk.Label(self.root, text="Requestdecryption_data请求包加密方法",font=8).grid(row=3, column=1, padx=10, pady=10, sticky='e')
        self.text_box2 = scrolledtext.ScrolledText(self.root, width=50, height=10, wrap=tk.WORD)
        self.text_box2.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')
        
        # Text小部件
        tk.Label(self.root, text="Responseencryption_data响应包加密方法",font=8).grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.text_box3 = scrolledtext.ScrolledText(self.root, width=50, height=10, wrap=tk.WORD)
        self.text_box3.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')

        tk.Label(self.root, text="Responsedecryption_data响应包解密方法",font=8).grid(row=5, column=1, padx=10, pady=10, sticky='e')
        self.text_box4 = scrolledtext.ScrolledText(self.root, width=50, height=10, wrap=tk.WORD)
        self.text_box4.grid(row=6, column=1, padx=10, pady=10, sticky='nsew')

        # 启动按钮
        self.start_button = tk.Button(self.root, text="一键启动", command=self.handle_save_and_start)
        self.start_button.grid(row=7, column=0, columnspan=2, pady=20, sticky='nsew')
    
    #先保存加解密方法再启动
    def handle_save_and_start(self):
        # 假设我们有两个标志变量来跟踪保存是否成功
        Requestencrypt_save_success = False
        Requestdecrypt_save_success = False
        Responseencrypt_save_success = False
        Responsedecrypt_save_success = False
 
        # 请求加密方法
        try:
            self.save_file_content("Requestencryption_method.txt", self.text_box1)
            Requestencrypt_save_success = True  # 假设如果没有抛出异常，则保存成功
        except Exception as e:
            messagebox.showerror("保存加密方法失败", f"无法保存加密方法: {e}")
 
        # 请求解密方法
        try:
            self.save_file_content("Requestdecryption_method.txt", self.text_box2)
            Requestdecrypt_save_success = True  # 假设如果没有抛出异常，则保存成功
        except Exception as e:
            messagebox.showerror("保存解密方法失败", f"无法保存解密方法: {e}")
        
        # 响应加密方法
        try:
            self.save_file_content("Responseencryption_method.txt", self.text_box3)
            Responseencrypt_save_success = True  # 假设如果没有抛出异常，则保存成功
        except Exception as e:
            messagebox.showerror("保存加密方法失败", f"无法保存加密方法: {e}")
        # 响应解密方法
        try:
            self.save_file_content("Responsedecryption_method.txt", self.text_box4)
            Responsedecrypt_save_success = True  # 假设如果没有抛出异常，则保存成功
        except Exception as e:
            messagebox.showerror("保存加密方法失败", f"无法保存加密方法: {e}")
        # 如果两者都保存成功，则启动代理
        if Requestencrypt_save_success and Requestdecrypt_save_success and Responseencrypt_save_success and Responsedecrypt_save_success:
            self.start_proxies()
        else:
            messagebox.showwarning("启动失败", "由于保存失败，无法启动EnAndDe代理。")
    #启动
    def start_proxies(self):
        try:
            ip = self.ip_var.get()
            target_port = self.validate_port(self.target_port_var.get())
            port1 = self.validate_port(self.port1_var.get())
            port2 = self.validate_port(self.port2_var.get())
            burp_port = self.validate_port(self.burp_port_var.get())

            # 启动代理线程
            threading.Thread(target=self.start_dec_thread, args=(port1, port2, ip, target_port)).start()
            threading.Thread(target=self.start_enc_thread, args=(burp_port, ip, target_port)).start()

            messagebox.showinfo("成功", "EnAndDe 启动成功！")
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {e}")

    def start_dec_thread(self, port, burp_port, ip, target_port):
        data = f"{ip}:{target_port}"
        with open('data.txt', 'w') as file:
            file.write(data)
        cmd = [
            "mitmdump", "-p", str(port), "-s", "dec.py", "--mode", f"upstream:http://127.0.0.1:{burp_port}", "--ssl-insecure"
        ]
        subprocess.Popen(cmd)

    def start_enc_thread(self, port, ip, target_port):
        data = f"{ip}:{target_port}"
        with open('data.txt', 'w') as file:
            file.write(data)
        cmd = [
            "mitmdump", "-p", str(port), "-s", "enc.py", "--ssl-insecure"
        ]
        subprocess.Popen(cmd)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnAndDeProxyApp(root)
    root.mainloop()