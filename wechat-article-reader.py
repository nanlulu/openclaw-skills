#!/usr/bin/env python3
"""
微信公众号文章读取工具
多种方法尝试获取文章内容
"""

import requests
import re
import json
import time
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import sys

class WeChatArticleReader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extract_from_mp_weixin_qq(self, url):
        """方法1：直接请求mp.weixin.qq.com"""
        try:
            print(f"尝试方法1：直接请求 {url}")
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # 尝试提取文章内容
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 微信公众号文章通常的结构
                title = soup.find('h1', class_='rich_media_title')
                author = soup.find('span', class_='rich_media_meta rich_media_meta_text')
                content = soup.find('div', class_='rich_media_content')
                
                if title and content:
                    result = {
                        'method': 'direct_request',
                        'success': True,
                        'title': title.get_text(strip=True),
                        'author': author.get_text(strip=True) if author else '',
                        'content': content.get_text(strip=True),
                        'html_content': str(content),
                    }
                    return result
            else:
                print(f"请求失败，状态码：{response.status_code}")
                
        except Exception as e:
            print(f"方法1失败：{e}")
        
        return {'method': 'direct_request', 'success': False}
    
    def extract_using_mobile_ua(self, url):
        """方法2：使用移动端User-Agent"""
        try:
            print(f"尝试方法2：移动端User-Agent")
            
            mobile_headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.15(0x18000f29) NetType/WIFI Language/zh_CN',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
            }
            
            response = self.session.get(url, headers=mobile_headers, timeout=10)
            
            if response.status_code == 200:
                # 尝试提取JSON数据（微信公众号有时会内嵌JSON）
                content = response.text
                
                # 查找可能的JSON数据
                json_patterns = [
                    r'window\.__wxInfo\s*=\s*({.*?});',
                    r'var\s+msgList\s*=\s*\'({.*?})\'',
                    r'var\s+appmsg\s*=\s*({.*?});',
                ]
                
                for pattern in json_patterns:
                    match = re.search(pattern, content, re.DOTALL)
                    if match:
                        try:
                            json_str = match.group(1)
                            # 清理JSON字符串
                            json_str = json_str.replace('\\x', '\\u00')
                            data = json.loads(json_str)
                            
                            # 提取文章信息
                            if 'title' in data:
                                result = {
                                    'method': 'mobile_ua_json',
                                    'success': True,
                                    'title': data.get('title', ''),
                                    'author': data.get('author', ''),
                                    'content': data.get('content', ''),
                                    'raw_data': data,
                                }
                                return result
                        except:
                            continue
                
                # 如果没找到JSON，尝试HTML解析
                soup = BeautifulSoup(content, 'html.parser')
                
                # 尝试不同的选择器
                selectors = [
                    ('h1', {'id': 'activity-name'}),
                    ('h2', {'class': 'rich_media_title'}),
                    ('div', {'id': 'js_content'}),
                    ('div', {'class': 'rich_media_content'}),
                ]
                
                title = None
                content_div = None
                
                for tag, attrs in selectors:
                    element = soup.find(tag, attrs)
                    if element:
                        if tag == 'h1' or tag == 'h2':
                            title = element
                        else:
                            content_div = element
                
                if title and content_div:
                    result = {
                        'method': 'mobile_ua_html',
                        'success': True,
                        'title': title.get_text(strip=True),
                        'content': content_div.get_text(strip=True),
                        'html_content': str(content_div),
                    }
                    return result
                    
        except Exception as e:
            print(f"方法2失败：{e}")
        
        return {'method': 'mobile_ua', 'success': False}
    
    def extract_via_archive_services(self, url):
        """方法3：通过存档服务获取"""
        try:
            print(f"尝试方法3：存档服务")
            
            # 尝试通过archive.is等存档服务
            archive_urls = [
                f"https://archive.is/?run=1&url={url}",
                f"https://web.archive.org/save/{url}",
            ]
            
            for archive_url in archive_urls:
                try:
                    response = self.session.get(archive_url, timeout=15)
                    if response.status_code == 200:
                        # 简单提取文本
                        soup = BeautifulSoup(response.content, 'html.parser')
                        text = soup.get_text(strip=True)
                        
                        if len(text) > 500:  # 如果有足够的内容
                            result = {
                                'method': 'archive_service',
                                'success': True,
                                'url': archive_url,
                                'content': text[:5000],  # 限制长度
                            }
                            return result
                except:
                    continue
                    
        except Exception as e:
            print(f"方法3失败：{e}")
        
        return {'method': 'archive_service', 'success': False}
    
    def extract_using_public_apis(self, url):
        """方法4：使用公开API（如果有）"""
        try:
            print(f"尝试方法4：公开API")
            
            # 解析文章ID
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            if '__biz' in query_params and 'mid' in query_params and 'idx' in query_params:
                # 尝试构造API URL
                biz = query_params['__biz'][0]
                mid = query_params['mid'][0]
                idx = query_params['idx'][0]
                
                # 微信公众号的API格式（可能变化）
                api_urls = [
                    f"https://mp.weixin.qq.com/mp/getappmsgext?__biz={biz}&mid={mid}&idx={idx}",
                    f"https://mp.weixin.qq.com/s?__biz={biz}&mid={mid}&idx={idx}",
                ]
                
                for api_url in api_urls:
                    try:
                        response = self.session.get(api_url, timeout=10)
                        if response.status_code == 200:
                            # 尝试解析响应
                            data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                            
                            result = {
                                'method': 'public_api',
                                'success': True,
                                'api_url': api_url,
                                'data': data,
                            }
                            return result
                    except:
                        continue
                        
        except Exception as e:
            print(f"方法4失败：{e}")
        
        return {'method': 'public_api', 'success': False}
    
    def read_article(self, url):
        """主函数：尝试多种方法读取文章"""
        print(f"开始读取文章：{url}")
        print("-" * 50)
        
        methods = [
            self.extract_from_mp_weixin_qq,
            self.extract_using_mobile_ua,
            self.extract_via_archive_services,
            self.extract_using_public_apis,
        ]
        
        results = []
        
        for method in methods:
            result = method(url)
            results.append(result)
            
            if result['success']:
                print(f"✅ 方法成功：{result['method']}")
                return result
            
            time.sleep(1)  # 避免请求过快
        
        print("❌ 所有方法都失败了")
        return {
            'success': False,
            'methods_tried': [r['method'] for r in results],
            'error': '无法获取文章内容',
        }
    
    def save_result(self, result, filename=None):
        """保存结果到文件"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"wechat_article_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存到：{filename}")
        return filename

def main():
    if len(sys.argv) < 2:
        print("使用方法：python wechat-article-reader.py <文章URL>")
        print("示例：python wechat-article-reader.py https://mp.weixin.qq.com/s/tlMMkjHcKPSZX9OVS9WQLQ")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 验证URL格式
    if not url.startswith('http'):
        url = 'https://' + url
    
    reader = WeChatArticleReader()
    result = reader.read_article(url)
    
    if result['success']:
        print("\n" + "=" * 50)
        print("✅ 文章读取成功！")
        print(f"方法：{result['method']}")
        
        if 'title' in result:
            print(f"标题：{result['title']}")
        
        if 'content' in result:
            content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
            print(f"内容预览：{content_preview}")
        
        # 保存结果
        saved_file = reader.save_result(result)
        print(f"完整结果已保存到：{saved_file}")
    else:
        print("\n❌ 文章读取失败")
        print(f"尝试的方法：{result.get('methods_tried', [])}")
        print(f"错误：{result.get('error', '未知错误')}")

if __name__ == "__main__":
    main()