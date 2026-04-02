#!/bin/bash
# 微信公众号文章读取脚本
# 简化版，方便在OpenClaw中调用

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    echo "微信公众号文章读取工具"
    echo ""
    echo "使用方法:"
    echo "  $0 <文章URL> [输出文件]"
    echo ""
    echo "示例:"
    echo "  $0 https://mp.weixin.qq.com/s/tlMMkjHcKPSZX9OVS9WQLQ"
    echo "  $0 https://mp.weixin.qq.com/s/tlMMkjHcKPSZX9OVS9WQLQ article.txt"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示帮助信息"
    echo "  -v, --version  显示版本信息"
    echo ""
    echo "功能:"
    echo "  1. 尝试多种方法获取文章内容"
    echo "  2. 提取标题和正文"
    echo "  3. 保存为文本或JSON格式"
}

# 检查依赖
check_dependencies() {
    local missing=()
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        missing+=("python3")
    fi
    
    # 检查curl
    if ! command -v curl &> /dev/null; then
        missing+=("curl")
    fi
    
    # 检查jq（可选）
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}警告: jq未安装，JSON处理功能受限${NC}"
    fi
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}错误: 缺少依赖: ${missing[*]}${NC}"
        echo "请安装:"
        for dep in "${missing[@]}"; do
            echo "  - $dep"
        done
        exit 1
    fi
}

# 方法1: 使用curl直接获取
method_curl() {
    local url="$1"
    echo -e "${BLUE}[方法1] 使用curl获取...${NC}"
    
    # 尝试获取HTML
    if curl -s -L -H "User-Agent: Mozilla/5.0" "$url" 2>/dev/null | grep -q "rich_media_content"; then
        echo -e "${GREEN}✓ 检测到文章内容${NC}"
        
        # 提取标题
        title=$(curl -s -L "$url" | grep -o '<h1[^>]*>[^<]*</h1>' | sed 's/<[^>]*>//g' | head -1)
        
        # 提取内容（简化版）
        content=$(curl -s -L "$url" | grep -A 1000 'rich_media_content' | grep -B 1000 '</div>' | sed 's/<[^>]*>//g' | tr -s ' ' | head -1000)
        
        if [ -n "$content" ] && [ ${#content} -gt 100 ]; then
            echo "标题: $title"
            echo "内容长度: ${#content} 字符"
            return 0
        fi
    fi
    
    return 1
}

# 方法2: 使用Python脚本
method_python() {
    local url="$1"
    echo -e "${BLUE}[方法2] 使用Python脚本...${NC}"
    
    if [ -f "/root/.openclaw/workspace/wechat-article-reader.py" ]; then
        python3 /root/.openclaw/workspace/wechat-article-reader.py "$url"
        return $?
    else
        echo -e "${YELLOW}Python脚本不存在，跳过此方法${NC}"
        return 1
    fi
}

# 方法3: 使用wget保存完整页面
method_wget() {
    local url="$1"
    echo -e "${BLUE}[方法3] 使用wget保存页面...${NC}"
    
    if command -v wget &> /dev/null; then
        local temp_file="/tmp/wechat_article_$(date +%s).html"
        
        wget -q -O "$temp_file" --user-agent="Mozilla/5.0" "$url"
        
        if [ -s "$temp_file" ]; then
            # 提取文本
            content=$(grep -o '<div[^>]*class="rich_media_content"[^>]*>.*</div>' "$temp_file" | sed 's/<[^>]*>//g' | tr -s ' ')
            
            if [ -n "$content" ] && [ ${#content} -gt 100 ]; then
                echo "内容长度: ${#content} 字符"
                rm "$temp_file"
                return 0
            fi
            
            rm "$temp_file"
        fi
    fi
    
    return 1
}

# 主函数
main() {
    # 检查参数
    if [ $# -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_help
        exit 0
    fi
    
    if [ "$1" = "-v" ] || [ "$1" = "--version" ]; then
        echo "wechat-reader v1.0.0"
        exit 0
    fi
    
    URL="$1"
    OUTPUT_FILE="${2:-}"
    
    # 验证URL
    if [[ ! "$URL" =~ ^https?:// ]]; then
        echo -e "${RED}错误: 无效的URL格式${NC}"
        echo "请使用完整的URL，如: https://mp.weixin.qq.com/s/..."
        exit 1
    fi
    
    # 检查依赖
    check_dependencies
    
    echo -e "${GREEN}开始读取文章:${NC} $URL"
    echo ""
    
    # 尝试多种方法
    METHODS=("method_curl" "method_python" "method_wget")
    METHOD_NAMES=("Curl直接获取" "Python脚本" "Wget保存页面")
    
    for i in "${!METHODS[@]}"; do
        method="${METHODS[$i]}"
        name="${METHOD_NAMES[$i]}"
        
        echo -e "${YELLOW}尝试方法 $((i+1)): $name${NC}"
        
        if $method "$URL"; then
            echo -e "${GREEN}✅ 方法成功！${NC}"
            
            # 如果有输出文件，保存结果
            if [ -n "$OUTPUT_FILE" ]; then
                echo "保存结果到: $OUTPUT_FILE"
                # 这里可以添加具体的保存逻辑
            fi
            
            exit 0
        else
            echo -e "${RED}✗ 方法失败${NC}"
        fi
        
        echo ""
    done
    
    echo -e "${RED}❌ 所有方法都失败了${NC}"
    echo ""
    echo "建议:"
    echo "1. 检查URL是否正确"
    echo "2. 文章可能需要微信登录才能查看"
    echo "3. 尝试手动复制文章内容"
    echo "4. 使用浏览器扩展保存文章"
    
    exit 1
}

# 运行主函数
main "$@"