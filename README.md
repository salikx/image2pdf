## 感谢以下项目
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=hect0x7&repo=JMComic-Crawler-Python)]([https://github.com/tonquer/JMComic-qt](https://github.com/hect0x7/JMComic-Crawler-Python)https://github.com/hect0x7/JMComic-Crawler-Python)


# 📄 图片批量转换为 PDF 脚本

该项目用于将分章节存储的图片合并为单个 PDF 文件，支持自动遍历指定目录下的所有文件夹，避免高内存占用问题。

---

## 📌 功能介绍

* 遍历指定根目录，处理子文件夹中的图片并生成对应的 PDF。
* 支持图片格式：`JPG` / `JPEG` / `PNG` / `WEBP` / `BMP`。
* 数字顺序排序子目录和图片，确保页码正确。
* 检测已生成的 PDF，避免重复转换。
* 错误处理和日志提示，自动跳过异常图片或空子目录。
* 内存优化：使用生成器逐张处理图片，避免一次性加载所有图片。

---

## 📂 目录结构示例

```
root_directory/
├── 001/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── …
├── 002/
│   ├── 1.png
│   ├── 2.png
│   └── …
├── Chapter3/
│   ├── 01.webp
│   ├── 02.webp
│   └── …
└── script.py
```

生成的 PDF 将保存在 `root_directory` 下：

```
root_directory/
├── 001.pdf
├── 002.pdf
├── Chapter3.pdf
└── …
```

---

## ⚙️ 环境依赖

请确保安装以下依赖：

```bash
pip install pillow pyyaml jmcomic
```

> **备注：** `jmcomic` 用于加载配置文件。确保使用前已正确安装或替换为自己的配置获取逻辑。

---

## 📄 使用方法

1. **克隆或下载代码。**

2. **确保配置文件存在并正确设置：**

配置文件路径需在脚本中指定：

```python
config_path = "D:/18comic_down/code/config.yml"
```

配置文件需要包含根目录设置：

```yaml
dir_rule:
  base_dir: "D:/your_base_directory"
```

3. **运行脚本：**

```bash
python script.py
```

> 如果需要自定义参数或路径，请修改 `config_path` 和相关参数。

---

## 🔧 参数说明

| 参数            | 说明            | 备注      |
| ------------- | ------------- | ------- |
| `config_path` | 配置文件路径        | YAML 格式 |
| `base_dir`    | 根目录，存放图片文件夹位置 | 必须存在    |

---

## 🚩 功能细节

* **内存优化：**

  * 使用生成器逐张加载图片，仅在处理时占用内存，有效防止内存泄露。
* **排序规则：**

  * 子文件夹按纯数字排序，非数字文件夹排在最后。
  * 图片文件名根据数字部分排序，确保正确顺序合成 PDF。
* **异常处理：**

  * 跳过非数字子目录。
  * 跳过无法读取或损坏的图片文件。
  * 检查目标 PDF 是否已存在，避免重复转换。

---

## 📑 日志输出示例

```
📄 转换中：001
开始生成PDF：D:\your_base_directory\001.pdf
✅ 成功生成PDF：D:\your_base_directory\001.pdf
处理完成，耗时 5.23 秒

跳过已有PDF：002.pdf

📄 转换中：Chapter3
开始生成PDF：D:\your_base_directory\Chapter3.pdf
✅ 成功生成PDF：D:\your_base_directory\Chapter3.pdf
处理完成，耗时 8.47 秒
```

---

## ❓ 常见问题

1. **配置文件加载失败：**

   * 请检查 `config_path` 路径是否正确。
   * 确保 `config.yml` 存在且格式正确。

2. **未找到图片文件：**

   * 确保子目录内存在支持的图片类型。
   * 检查子目录命名是否为纯数字，如 `001`、`002`。

3. **内存占用高：**

   * 脚本已使用生成器优化，如仍有问题请检查图片分辨率或尝试拆分图片文件夹。

---

## 📬 联系

如有问题或建议，请在仓库提交 issue 反馈。
