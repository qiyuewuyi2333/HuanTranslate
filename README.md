# AI Translator Web

## 项目简介

本项目是一个现代化的AI翻译Web应用，支持Word(docx)、Markdown文件的上传与翻译，界面美观，支持多服务商API配置，支持中文文件名上传与下载。

---

## 环境依赖
- Python 3.8+
- pip
- 推荐操作系统：Windows/Linux/Mac

---

## 安装依赖（推荐使用国内镜像源）

1. **克隆项目**
```bash
# 进入你的工作目录
cd ai_translator
```

2. **安装依赖（推荐阿里云镜像）**
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 字体准备（如需PDF中文支持，可选）
> 当前PDF翻译已关闭，如需支持请联系开发者。

1. 从 `C:\Windows\Fonts\simhei.ttf` 或 `msyh.ttc` 复制到 `static/fonts/` 目录下。
2. 若无该目录请手动创建。

---

## 数据库初始化

首次运行前请初始化数据库：
```bash
python init_db.py
```

---

## 启动项目

```bash
python app.py
```

访问：http://127.0.0.1:5000

---

## 常见问题

- **依赖安装慢/失败？**
  - 请务必加上 `-i https://mirrors.aliyun.com/pypi/simple/`。
- **docx/中文文件名上传失败？**
  - 已支持中文名，若仍有问题请反馈。
- **PDF暂不支持翻译？**
  - 前端和后端均有友好提示，后续如需支持请联系开发者。
- **API Key配置/多服务商？**
  - 请在"API配置"页面填写各服务商的API Key和Base URL。

---

## 目录结构

```
ai_translator/
  app.py
  init_db.py
  requirements.txt
  README.md
  static/
    fonts/
    ...
  templates/
    ...
  services/
    ...
  api/
    ...
  config/
    ...
  models/
    ...
  utils/
    ...
  uploads/
```

---

## 联系与反馈
如有问题或建议，请联系开发者。
