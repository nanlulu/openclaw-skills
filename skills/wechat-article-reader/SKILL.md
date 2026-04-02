---
name: wechat-article-reader
description: "读取微信公众号文章的技能，支持多种获取方法，处理验证和内容提取。"
---

# 微信公众号文章读取技能

专门用于读取微信公众号文章的工具集，解决反爬虫、登录验证等问题。

## 快速开始

```bash
# 方法1: 使用Python脚本
python3 /root/.openclaw/workspace/wechat-article-reader.py "https://mp.weixin.qq.com/s/文章ID"

# 方法2: 使用Shell脚本
bash /root/.openclaw/workspace/wechat-reader.sh "https://mp.weixin.qq.com/s/文章ID"

# 方法3: 直接调用（在OpenClaw中）
wechat-read "文章URL"
```

## 功能特点

### 1. 多方法尝试
- **直接请求**：标准HTTP请求
- **移动端模拟**：使用微信浏览器User-Agent
- **存档服务**：通过archive.is等获取
- **API尝试**：尝试微信公众号的API接口

### 2. 智能处理
- 自动处理重定向
- 尝试绕过简单反爬虫
- 内容提取和清洗
- 错误重试机制

### 3. 输出格式
- 纯文本提取
- HTML格式保留
- JSON结构化数据
- Markdown转换

## 使用方法

### 基本用法
```python
# 在Python中调用
from wechat_article_reader import WeChatArticleReader

reader = WeChatArticleReader()
result = reader.read_article("https://mp.weixin.qq.com/s/文章ID")

if result['success']:
    print(f"标题: {result['title']}")
    print(f"内容: {result['content'][:500]}...")
```

### 命令行使用
```bash
# 读取文章并保存为JSON
wechat-read "https://mp.weixin.qq.com/s/文章ID" --output article.json

# 只提取文本内容
wechat-read "https://mp.weixin.qq.com/s/文章ID" --text-only

# 保存为Markdown
wechat-read "https://mp.weixin.qq.com/s/文章ID" --format markdown
```

### OpenClaw集成
```bash
# 在OpenClaw会话中直接使用
!wechat-read 文章URL

# 或者通过技能调用
use wechat-article-reader --url "文章URL"
```

## 配置选项

### 环境变量
```bash
# 设置User-Agent
export WECHAT_UA="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"

# 设置超时时间
export WECHAT_TIMEOUT=30

# 设置代理（如果需要）
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
```

### 配置文件
创建 `~/.wechat-reader/config.yaml`：
```yaml
user_agent:
  desktop: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  mobile: "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)"

timeout: 30
retry_times: 3
delay_between_retries: 2

output:
  default_format: "json"
  text_length_limit: 10000
  save_html: false

archive_services:
  - "https://archive.is"
  - "https://web.archive.org"
```

## 高级功能

### 批量处理
```bash
# 从文件读取URL列表
wechat-read --batch urls.txt --output-dir articles/

# 从CSV读取
wechat-read --csv articles.csv --column url
```

### 内容分析
```bash
# 提取关键词
wechat-read "文章URL" --extract-keywords

# 生成摘要
wechat-read "文章URL" --summarize

# 情感分析
wechat-read "文章URL" --sentiment
```

### 数据导出
```bash
# 导出到数据库
wechat-read "文章URL" --export sqlite:///articles.db

# 导出到Elasticsearch
wechat-read "文章URL" --export es://localhost:9200/wechat

# 导出到CSV
wechat-read "文章URL" --export-csv articles.csv
```

## 故障排除

### 常见问题

**问题1：返回空白内容**
```bash
# 解决方案：尝试不同的User-Agent
wechat-read "文章URL" --ua mobile
wechat-read "文章URL" --ua wechat
```

**问题2：需要登录验证**
```bash
# 解决方案1：使用cookie
wechat-read "文章URL" --cookie "your_cookie_string"

# 解决方案2：手动登录后导出cookie
# 在浏览器中登录微信，使用EditThisCookie等扩展导出
```

**问题3：访问频率限制**
```bash
# 解决方案：增加延迟
wechat-read "文章URL" --delay 5
```

**问题4：验证码拦截**
```bash
# 解决方案：使用存档服务
wechat-read "文章URL" --use-archive
```

### 调试模式
```bash
# 启用详细日志
wechat-read "文章URL" --verbose

# 保存原始HTML
wechat-read "文章URL" --save-raw

# 显示HTTP请求详情
wechat-read "文章URL" --debug
```

## 性能优化

### 缓存机制
```bash
# 启用缓存
wechat-read "文章URL" --cache

# 清除缓存
wechat-read --clear-cache

# 查看缓存状态
wechat-read --cache-status
```

### 并发处理
```bash
# 并发读取多篇文章
wechat-read --batch urls.txt --concurrent 5

# 限制并发数
wechat-read --batch urls.txt --max-concurrent 3
```

### 资源限制
```bash
# 限制内存使用
wechat-read "文章URL" --max-memory 256M

# 限制CPU使用
wechat-read "文章URL" --cpu-limit 50%
```

## 扩展开发

### 添加新的获取方法
```python
# 在wechat-article-reader.py中添加新类
class NewExtractionMethod:
    def extract(self, url):
        # 实现新的提取逻辑
        pass
```

### 自定义内容处理器
```python
# 创建自定义处理器
class CustomContentProcessor:
    def process(self, html_content):
        # 自定义内容清洗和提取
        pass
```

### 插件系统
```bash
# 加载插件
wechat-read "文章URL" --plugin my_plugin.py

# 开发插件模板
# 参考: plugins/template.py
```

## 安全注意事项

1. **遵守Robots协议**：尊重网站的爬虫规则
2. **控制访问频率**：避免对服务器造成压力
3. **版权尊重**：仅用于个人学习研究
4. **数据保护**：不要存储敏感个人信息
5. **合法使用**：遵守相关法律法规

## 更新日志

### v1.0.0 (2026-04-01)
- 初始版本发布
- 支持4种获取方法
- 基础内容提取功能
- 命令行界面

### 计划功能
- [ ] 浏览器自动化集成
- [ ] OCR图片文字识别
- [ ] 多语言支持
- [ ] 分布式爬虫
- [ ] 实时监控新文章

## 贡献指南

欢迎提交Issue和Pull Request：
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License - 详见LICENSE文件

## 技术支持

- 文档：查看本文件
- 问题：GitHub Issues
- 讨论：GitHub Discussions
- 邮件：开发者邮箱

---

**提示**：对于需要登录的公众号文章，建议先在浏览器中登录微信，然后导出cookie供脚本使用。