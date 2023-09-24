## 感谢以下项目
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=hect0x7&repo=JMComic-Crawler-Python)]([https://github.com/tonquer/JMComic-qt](https://github.com/hect0x7/JMComic-Crawler-Python)https://github.com/hect0x7/JMComic-Crawler-Python)
## 功能说明
将下载好的图片（本子）转换为PDF
## 使用说明
1. 先安装JMComic-Crawler
2. 需要安装第三方库：
  ```shell
  pip install jmcomic -i https://pypi.org/project --upgrade
  pip install pillow
  pip install pyyaml 
  ```
3. 下载好本子之后，可直接使用main.py进行下载和转换：
4. 预先配置好config路径,
```shell
manhua = ['146417']  
for id in manhua:
  jmcomic.download_album(id,loadConfig)
```
可取消上述代码注释，manhua = ['146417']  中可填写多个需要下载的本子，格式:['12314545','2321415']以此类推；

## 注意
批量转换会预先将图片写入内存中，因此本子超过150话以上的，如果电脑内存小于32G，尽量不要尝试了(暂时没想到很好的解决办法）
