# 🏢 职称申报登录助手 (Python版本)

基于 Python + WxPython + Playwright 的自动化登录工具，专门用于河南省职称管理服务平台-职称申报系统的自动登录操作。

## ✨ 功能特性

- 🖥️ **Windows 桌面应用** - 基于 WxPython 构建，界面简洁易用
- 🤖 **自动化登录** - 使用 Playwright 实现网页自动化操作
- 📊 **Excel 数据读取** - 支持从 Excel 文件读取多个账号信息
- 🔐 **验证码识别** - 集成超级鹰验证码识别服务
- ⚙️ **灵活配置** - 支持自定义超时时间、重试次数等
- 📝 **弹窗处理** - 自动处理登录后的各种弹窗
- 💾 **配置保存** - 自动保存用户配置，下次启动无需重新设置
- 📦 **一键打包** - 支持打包成独立的 Windows exe 可执行文件

## 🚀 快速开始

### 方式一：使用打包好的 exe 文件（推荐用户）

直接下载发布的 exe 文件包，无需安装 Python 环境。

1. **下载发布包**
   - 从 Releases 页面下载最新版本
   - 解压到任意目录

2. **首次配置**
   ```
   - 将 settings.json.example 重命名为 settings.json
   - 填写您的超级鹰账号信息
   - 准备 Excel 数据文件
   ```

3. **运行程序**
   ```
   双击 "职称申报登录助手.exe" 即可启动
   ```

### 方式二：从源码运行（开发者）

### 环境要求

- Python 3.7 或更高版本
- Windows 10/11 操作系统
- 网络连接（用于下载依赖和访问目标网站）

### 安装步骤

#### 方案1: 完整安装 (推荐)

#### 方案1: 完整安装 (推荐)

1. **克隆项目**
   ```bash
   git clone https://github.com/quying2024/Projects.git
   cd Projects/Autologin
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **运行程序**
   ```bash
   python main.py
   ```
   conda install -c conda-forge wxpython
   ```
   
   **方案B: 下载预编译包**
   - 访问: https://www.lfd.uci.edu/~gohlke/pythonlibs/#wxpython
   - 下载对应 Python 版本的 .whl 文件
   - 运行: `pip install 下载的文件名.whl`
   
   **方案C: 使用 Tkinter 版本 (无需额外安装)**
   ```bash
   python main_tkinter.py
   ```

4. **启动应用**
   ```bash
   # WxPython 版本 (如果安装成功)
   python main.py
   
   # Tkinter 版本 (如果 wxPython 安装失败)
   python main_tkinter.py
   ```

### 手动安装依赖

#### 完整依赖 (推荐)
```bash
# 基础依赖
pip install playwright==1.40.0 pandas==2.1.4 openpyxl==3.1.2 requests==2.31.0 Pillow==10.1.0
playwright install chromium

# wxPython (可选，如果安装失败可以使用 Tkinter 版本)
pip install wxPython
# 或者使用 conda
conda install -c conda-forge wxpython
```

#### 最小化依赖
```bash
# 只安装预编译包，避免编译问题
pip install requests==2.31.0 Pillow==10.1.0 openpyxl==3.1.2
pip install pandas  # 如果失败，程序会自动使用 CSV 格式
```
```bash
# 基础依赖
pip install playwright==1.40.0 pandas==2.1.4 openpyxl==3.1.2 requests==2.31.0 Pillow==10.1.0
playwright install chromium

# wxPython (可选，如果安装失败可以使用 Tkinter 版本)
pip install wxPython
# 或者使用 conda
conda install -c conda-forge wxpython
```

## 📖 使用说明

### 1. 配置超级鹰API

1. 点击程序界面中的"设置"按钮
2. 填写超级鹰账户信息：
   - **用户名**: 超级鹰注册用户名
   - **密码**: 超级鹰账户密码
   - **软件ID**: 超级鹰软件ID（可在超级鹰官网申请）
3. 点击"测试连接"验证配置
4. 点击"保存"完成配置

### 2. 准备账号信息文件

创建 Excel 文件，包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 姓名 | 用户真实姓名 | 张三 |
| 单位 | 所属单位 | XX大学 |
| 身份证号码 | 登录用户名 | 123456789012345678 |
| 密码 | 登录密码 | password123 |

### 3. 使用程序

1. **选择文件**: 点击"文件路径"按钮，选择包含账号信息的 Excel 文件
2. **输入姓名**: 在姓名输入框中输入要登录的用户姓名
3. **开始登录**: 点击"登录"按钮，程序将自动执行登录流程

### 4. 登录流程

程序会自动执行以下步骤：

1. 打开浏览器访问登录页面
2. 填写用户名（身份证号码）和密码
3. 识别并填写验证码（如果启用）
4. 点击登录按钮
5. 处理登录后的弹窗：
   - 修改密码弹窗：提示用户手动处理
   - 注意事项弹窗：自动关闭
   - 其他弹窗：尝试自动处理

## 🛠️ 技术架构

### 核心技术栈

- **WxPython** - 桌面应用框架
- **Playwright** - 网页自动化
- **Pandas** - Excel 文件处理
- **Requests** - HTTP 请求
- **超级鹰API** - 验证码识别

### 项目结构

```
Autologin/
├── main.py              # 主程序文件 (WxPython 版本)
├── config.py            # 配置管理
├── captcha_handler.py   # 验证码处理
├── settings_dialog.py   # 设置对话框
├── requirements.txt     # Python 依赖
├── README.md           # 项目说明
└── docs/               # 相关文档
    ├── 职称申报登录助手设计.docx
    ├── 超级鹰验证码识别说明文档.docx
    └── 2025职称申报账号信息.xlsx
```

## 🔧 配置说明

### 配置文件

程序会自动创建以下配置文件：

- `config.json` - 程序配置（超级鹰API、登录设置等）
- `app_config.txt` - 账号文件路径配置

### 超级鹰配置

在设置对话框中配置：

- **用户名**: 超级鹰注册用户名
- **密码**: 超级鹰账户密码  
- **软件ID**: 超级鹰软件ID

### 登录设置

- **超时时间**: 登录操作超时时间（秒）
- **重试次数**: 登录失败时的重试次数

## 🐛 故障排除

### 常见问题

1. **无法启动程序**
   - 检查 Python 版本是否为 3.7+
   - 确认已安装所有依赖包
   - 检查 WxPython 是否正确安装

2. **登录失败**
   - 验证账号信息是否正确
   - 检查网络连接
   - 确认目标网站是否可访问

3. **验证码识别失败**
   - 检查超级鹰API配置
   - 确认账户余额充足
   - 验证软件ID是否正确

4. **Excel 文件读取失败**
   - 确认文件格式为 .xlsx 或 .xls
   - 检查是否包含必需的列
   - 验证数据格式是否正确

### 调试模式

程序会在控制台输出详细的调试信息，包括：

- 登录流程的每个步骤
- 验证码识别结果
- 弹窗处理情况
- 错误信息

## � 打包发布

### 开发者打包指南

如果您需要将程序打包成 exe 文件：

1. **安装打包工具**
   ```bash
   pip install pyinstaller
   ```

2. **执行打包**
   ```bash
   # 完整打包流程
   .\打包程序.bat
   
   # 或快速打包
   .\快速打包.bat
   ```

3. **准备发布包**
   ```bash
   .\准备发布包.bat
   ```

4. **输出结果**
   ```
   dist\职称申报登录助手\
   ├── 职称申报登录助手.exe    (8.13 MB)
   └── _internal\              (160.31 MB)
   ```

详细打包说明请参阅：
- [打包发布指南.md](打包发布指南.md)
- [打包快速参考.md](打包快速参考.md)

## �📋 注意事项

1. **账号安全**: 请妥善保管账号信息，不要泄露给他人
2. **使用频率**: 避免频繁登录，以免被系统限制
3. **验证码**: 确保超级鹰账户有足够余额
4. **网络环境**: 确保网络连接稳定
5. **浏览器**: 程序使用 Chromium 浏览器，确保系统支持

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 项目地址：https://github.com/quying2024/Projects
- 邮箱：quandyang@gmail.com

---

**免责声明**: 本工具仅用于提高工作效率，请遵守相关网站的使用条款和法律法规。使用者需自行承担使用风险。
