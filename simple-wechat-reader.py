#!/usr/bin/env python3
"""
简化版微信公众号文章读取工具
使用标准库，无需外部依赖
"""

import urllib.request
import urllib.error
import re
import json
import sys
import time

def fetch_url(url, user_agent=None):
    """获取URL内容"""
    headers = {
        'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return content
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def extract_content_simple(html):
    """简单的内容提取"""
    # 尝试提取标题
    title_patterns = [
        r'<h1[^>]*>(.*?)</h1>',
        r'<title>(.*?)</title>',
        r'og:title["\']\s*content=["\'](.*?)["\']',
        r'<h2[^>]*>(.*?)</h2>',
    ]
    
    title = None
    for pattern in title_patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            title = re.sub('<[^>]*>', '', match.group(1)).strip()
            if title and len(title) > 5:
                break
    
    # 尝试提取内容
    content_patterns = [
        r'<div[^>]*class=["\']rich_media_content["\'][^>]*>(.*?)</div>',
        r'<div[^>]*id=["\']js_content["\'][^>]*>(.*?)</div>',
        r'<article[^>]*>(.*?)</article>',
        r'<div[^>]*class=["\']article-content["\'][^>]*>(.*?)</div>',
    ]
    
    content = None
    for pattern in content_patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            # 移除HTML标签
            content = re.sub('<[^>]*>', ' ', match.group(1))
            # 合并多个空格
            content = re.sub(r'\s+', ' ', content).strip()
            if content and len(content) > 100:
                break
    
    return title, content

def extract_json_data(html):
    """尝试提取JSON数据"""
    json_patterns = [
        r'window\.__wxInfo\s*=\s*({.*?});',
        r'var\s+msgList\s*=\s*\'(.*?)\'',
        r'var\s+appmsg\s*=\s*({.*?});',
        r'<script[^>]*>.*?({.*?}).*?</script>',
    ]
    
    for pattern in json_patterns:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                json_str = match.group(1)
                # 清理JSON字符串
                json_str = json_str.replace('\\x', '\\u00')
                data = json.loads(json_str)
                return data
            except:
                continue
    
    return None

def try_methods(url):
    """尝试多种方法"""
    methods = [
        # 方法1: 桌面浏览器
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', "桌面浏览器"),
        
        # 方法2: 移动端
        ('Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15', "iPhone微信"),
        
        # 方法3: 微信内置浏览器
        ('Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36', "Android微信"),
        
        # 方法4: 简单User-Agent
        ('Mozilla/5.0', "简单UA"),
    ]
    
    for ua, method_name in methods:
        print(f"尝试方法: {method_name}")
        
        html = fetch_url(url, ua)
        if not html:
            print(f"  ✗ 请求失败")
            continue
        
        # 检查是否有内容
        if len(html) < 1000:
            print(f"  ✗ 内容过短 ({len(html)} 字符)")
            continue
        
        # 提取内容
        title, content = extract_content_simple(html)
        
        if content and len(content) > 200:
            print(f"  ✓ 成功获取内容")
            print(f"    标题: {title or '未提取到'}")
            print(f"    内容长度: {len(content)} 字符")
            print(f"    内容预览: {content[:200]}...")
            return {
                'success': True,
                'method': method_name,
                'title': title,
                'content': content,
                'content_length': len(content),
            }
        
        # 尝试提取JSON
        json_data = extract_json_data(html)
        if json_data:
            print(f"  ✓ 成功提取JSON数据")
            # 尝试从JSON中提取内容
            if isinstance(json_data, dict):
                title = json_data.get('title') or json_data.get('Title')
                content = json_data.get('content') or json_data.get('Content')
                
                if content:
                    return {
                        'success': True,
                        'method': f"{method_name} (JSON)",
                        'title': title,
                        'content': str(content)[:5000],  # 限制长度
                        'content_length': len(str(content)),
                        'raw_json': json_data,
                    }
        
        print(f"  ✗ 未提取到有效内容")
        time.sleep(1)  # 避免请求过快
    
    return {'success': False, 'error': '所有方法都失败了'}

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 simple-wechat-reader.py <文章URL>")
        print("示例: python3 simple-wechat-reader.py https://mp.weixin.qq.com/s/tlMMkjHcKPSZX9OVS9WQLQ")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 验证URL
    if not url.startswith('http'):
        url = 'https://' + url
    
    print(f"开始读取文章: {url}")
    print("=" * 60)
    
    result = try_methods(url)
    
    print("\n" + "=" * 60)
    if result['success']:
        print("✅ 文章读取成功！")
        print(f"使用方法: {result['method']}")
        
        # 保存结果
        output_file = f"wechat_article_{int(time.time())}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"标题: {result.get('title', '')}\n")
            f.write(f"URL: {url}\n")
            f.write(f"获取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"使用方法: {result['method']}\n")
            f.write("=" * 60 + "\n")
            f.write(result.get('content', ''))
        
        print(f"结果已保存到: {output_file}")
        
        # 显示内容预览
        if 'content' in result:
            preview = result['content']
            if len(preview) > 500:
                preview = preview[:500] + "..."
            print(f"\n内容预览:\n{preview}")
    else:
        print("❌ 文章读取失败")
        print(f"错误: {result.get('error', '未知错误')}")
        
        print("\n建议:")
        print("1. 检查URL是否正确")
        print("2. 文章可能需要微信登录")
        print("3. 尝试手动复制文章内容")
        print("4. 使用浏览器打开后保存页面")

if __name__ == "__main__":
    main()