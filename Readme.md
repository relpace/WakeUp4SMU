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
```
pip3 install uv -i  https://pypi.tuna.tsinghua.edu.cn/simple
cd ~/Downloads/WakeUp4SMU-master
uv sync
uv run main.py
```

这是一份为您准备的《使用指南》，您可以直接将其放入项目的 `README.md` 或发布在 Wiki 中。这份指南是基于您即将更新的“Gist 同步版”Workflow 编写的，步骤详细且面向非技术背景的同学。

---

# 📅 自动日历同步配置指南
**以下内容由Gemini生成，感谢Gemini 3 Pro，感谢Antigravity**
本指南将教你如何利用 GitHub Actions 每天自动抓取南医大教务系统课表，并同步到你的手机日历中。

> 通过本方法配置，你的账号密码仅存储在你个人的 GitHub 仓库中，生成的课表文件存储在私密的 Gist 中。**除了你自己，没有人能看到你的课表。**

## 准备工作
* 一个 GitHub 账号
* 你的南医大教务系统账号和密码

---

## 第一步：Fork 本仓库
1.  点击本页面右上角的 **`Fork`** 按钮。
2.  点击 `Create fork`，将这个项目复制到你自己的账号下。

## 第二步：创建私密 Gist (用于存放课表)
我们需要一个地方存放生成的课表文件，且不能公开。GitHub Gist 是最佳选择。

1.  登录 [gist.github.com](https://gist.github.com/)。
2.  **Gist description**：填写 `我的课表` (选填)。
3.  **Filename**：填写 **`schedule.ics`** (注意后缀必须是 .ics)。
4.  **Content**：随便写点什么，比如 `temp` (运行后会被自动覆盖)。
5.  点击右下角的 **`Create secret gist`** (⚠️注意：一定要选 **Secret**，不要选 Public)。
6.  创建成功后，看浏览器上方的地址栏，链接最后的一串字符就是你的 **Gist ID**。
    * 例如：`https://gist.github.com/你的名字/c09a8b7e6d5f4e3d2c1a`
    * 那么 **`c09a8b7e6d5f4e3d2c1a`** 就是你的 ID，请复制备用。

## 第三步：申请访问令牌 (Token)
为了让脚本能自动把课表写入你的 Gist，需要一把“钥匙”。

1.  进入 [GitHub Token 设置页面](https://github.com/settings/tokens/new)。
2.  **Note**：填写 `WakeUp4SMU`。
3.  **Expiration**：建议选择 `No expiration` (永不过期)，否则你需要定期更新。
4.  **Select scopes**：勾选 **`gist`** (Create gists)。
5.  点击页面底部的 `Generate token`。
6.  **⚠️ 立即复制显示的 Token** (以 `ghp_` 开头)，离开页面后它将不再显示。

## 第四步：配置项目参数
回到你刚才 **Fork 过来** 的仓库页面，点击上方的 **`Settings`** -> 左侧边栏 **`Secrets and variables`** -> **`Actions`**。

我们需要添加以下配置：

### 1. 添加 Secrets (加密数据)
点击 **`New repository secret`**，依次添加以下 4 个：

| Name (名称) | Secret (值) | 说明 |
| :--- | :--- | :--- |
| **ACCOUNT** | 你的学号 | 教务系统账号 |
| **PASSWORD** | 你的密码 | 教务系统密码 |
| **GIST_ID** | (第二步获取的ID) | 刚才复制的那串字符 |
| **GIST_TOKEN** | (第三步获取的Token) | `ghp_` 开头的那串字符 |

### 2. 添加 Variables (普通变量)
点击 **`Variables`** 选项卡 (在 Secrets 旁边)，点击 **`New repository variable`**，添加以下 2 个：

| Name (名称) | Value (值) | 说明 |
| :--- | :--- | :--- |
| **WEEKS** | `20` | 本学期总周数 (例如 20) |
| **START_DATE** | `2025-02-24` | 开学第一周周一的日期 (格式必须为 YYYY-M-D) |

---

## 第五步：启动自动更新
出于安全考虑，GitHub 默认会禁用 Fork 仓库的 Actions。

1.  点击仓库上方的 **`Actions`** 标签页。
2.  点击绿色的按钮 **`I understand my workflows, go ahead and enable them`**。
3.  在左侧点击 **`Schedule Update`**。
4.  点击右侧的 **`Run workflow`** -> **`Run workflow`** 手动触发一次。

等待几分钟，如果显示绿色的 `✅ Success`，说明配置成功！脚本以后每天会自动运行。

---

## 第六步：获取日历订阅链接
配置完成后，最后一步是获取链接并在手机上订阅。

1.  回到你的 [Gist 页面](https://gist.github.com/)，找到刚才创建的 `schedule.ics`。
2.  你会发现内容已经变成了长长的日历代码。点击右上角的 **`Raw`** 按钮。
3.  **关键步骤**：复制浏览器的地址栏链接，但要**删除中间的版本号**。
    * 原始链接长这样：
        `.../raw/823abc...123/schedule.ics`
    * **请修改为** (删除 `raw/` 和 `schedule.ics` 中间的那串乱码)：
        `https://gist.githubusercontent.com/你的用户名/你的GistID/raw/schedule.ics`
    * *为什么要改？* 因为不删除版本号的话，你的日历永远指向旧版本，不会自动更新。

4.  **订阅导出的课表**：
    * **iOS/MacOS**: 设置 -> 日历 -> 账户 -> 添加账户 -> 其他 -> 添加已订阅的日历 -> 粘贴链接。(我没有苹果手机啊你们自己找找，反正是可以的)
    * **Android**: 使用自带的系统日历或者通过 Google Calendar 添加URL订阅。
    * **Windows**: 可使用Outlook、网易邮箱大师、Thunderbird等邮件客户端添加日历订阅

---

### ❓ 常见问题

**Q: 运行失败，提示 `Login failed`？**
A: 请检查 Secrets 中的 `ACCOUNT` 和 `PASSWORD` 是否正确，或者教务系统是否正在维护。

**Q: 日历多久更新一次？**
A: 脚本默认每天凌晨自动运行一次。你也可以在 Actions 页面手动点击运行。

**Q: 为什么我的 Gist 里还是空的？**
A: 请检查 Actions 的运行日志。如果报错 `Resource not found`，通常是 `GIST_ID` 填错了；如果报错 `Bad credentials`，则是 `GIST_TOKEN` 填错或权限不足。