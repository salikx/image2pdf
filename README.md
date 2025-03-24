## 感谢以下项目
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=hect0x7&repo=JMComic-Crawler-Python)]([https://github.com/tonquer/
JMComic-qt](https://github.com/hect0x7/JMComic-Crawler-Python)https://github.com/hect0x7/JMComic-Crawler-Python)
## 功能说明
将下载好的图片（本子）转换为PDF
## 使用方法

1. 确保已安装所有依赖
    ```bash
  pip install -r requirements.txt
  ```
2. 配置`config.yml`文件（可选）
3. 运行主程序：

```python
from main import process_manga

下载漫画并转换为PDF（PDF文件会生成在相同目录下，使用漫画名称命名）
manga_ids = ['61572', '36267']  # 漫画ID列表
process_manga(manga_ids, should_convert_pdf=True)

仅下载漫画，不转换为PDF
process_manga(manga_ids, should_convert_pdf=False)
```

## 配置说明

  参考https://jmcomic.readthedocs.io/zh-cn/latest/option_file_syntax/

## 许可证

MIT License
