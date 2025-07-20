import os
import subprocess
import shutil
import sys
import time

def build_exe():
    """使用PyInstaller打包应用程序为单个.exe文件"""
    print("开始构建应用程序...")

    # 确保资源目录存在
    if not os.path.exists("resources"):
        print("错误：资源目录不存在！")
        return False

    # 图标路径
    icon_path = os.path.abspath(os.path.join("resources", "icon.png"))

    # 检查图标是否存在
    if not os.path.exists(icon_path):
        print(f"警告：图标文件不存在: {icon_path}")
        print("将使用默认图标继续...")
        icon_option = ""
    else:
        icon_option = f"--icon={icon_path}"

    # 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包为单个文件
        "--noconsole",  # 不显示控制台窗口
        "--clean",  # 清理临时文件
        "--name=MouseAutoClicker",  # 输出文件名
        icon_option,
        "--add-data=resources;resources",  # 添加资源文件
        "--hidden-import=PyQt5.QtGui",  # 确保QtGui模块被包含
        "--hidden-import=PyQt5.QtWidgets",  # 确保QtWidgets模块被包含
        "--hidden-import=PyQt5.sip",  # 确保sip模块被包含
        "--collect-all=PyQt5",  # 收集所有PyQt5相关的模块和插件
        "--uac-admin",  # 以管理员权限运行
        "main.py"  # 主程序文件
    ]

    # 过滤掉空选项
    cmd = [option for option in cmd if option]

    # 执行命令
    try:
        # 清理dist目录
        dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
        exe_path = os.path.join(dist_path, 'MouseAutoClicker.exe')

        if os.path.exists(dist_path):
            try:
                if os.path.exists(exe_path):
                    print("尝试删除现有的EXE文件...")
                    os.remove(exe_path)
                else:
                    print("没有找到现有的EXE文件")
            except PermissionError:
                print("警告: 无法删除现有的EXE文件，它可能正在运行")
                print("请关闭所有应用程序实例后再尝试构建")
                exit(1)
                
        subprocess.run(cmd, check=True)
        print("应用程序构建成功！")

        # 显示输出文件位置
        output_path = os.path.abspath(os.path.join("dist", "MouseAutoClicker.exe"))
        if os.path.exists(output_path):
            print(f"可执行文件位置: {output_path}")

        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False

if __name__ == "__main__":
    build_exe()