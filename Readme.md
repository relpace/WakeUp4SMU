# WakeUp4SMU
#### 更适合南医宝宝体质的WakeUp课表导入工具

## 使用方法
### 直接运行：从[Release页面](https://github.com/relpace/WakeUp4SMU/releases/latest)下载WakeUp4SMU.exe并运行
### 手动运行main.py:
1. `git clone`或手动下载仓库Zip并解压
2. 安装Python
3. 安装uv：`pip install uv`
4. 在仓库目录中执行:  
```
uv sync 
uv run main.py
```
### 脚本运行完毕后，将输出的**整条内容**发送给手机并粘贴到WakeUp课表中进行导入。

## 给Mac用户的保姆级教程：
1. 点击本页面上部的Code按钮-[Download Zip](https://github.com/relpace/WakeUp4SMU/archive/refs/heads/master.zip)下载Zip文件
2. 下载完成后双击解压Zip文件
3. 按command(⌘)+空格打开Spotlight，输入terminal打开终端
4. 在终端中依次运行：
```angular2html
    pip3 install uv -i  https://pypi.tuna.tsinghua.edu.cn/simple
    cd ~/Downloads/WakeUp4SMU-master
    uv sync
    uv run main.py
```