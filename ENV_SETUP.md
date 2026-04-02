# 环境变量安全设置指南

## 🎯 已完成的安全设置

✅ **你的 GitHub 个人访问令牌已安全存储：**

1. **`.env` 文件已创建** - 包含你的 GitHub 令牌
2. **`.gitignore` 已配置** - 确保 `.env` 不会被提交到代码仓库
3. **`.env.example` 已创建** - 作为模板供其他开发者使用
4. **Git 提交已处理** - 只有 `.gitignore` 和 `.env.example` 被提交

## 🔐 你的 GitHub 令牌信息

- **令牌类型**: Personal Access Token (以 `ghp_` 开头)
- **令牌长度**: 40 个字符
- **存储位置**: `.env` 文件（本地，不上传）
- **安全状态**: ✅ 安全，未提交到 Git

## 📁 文件结构

```
.
├── .env                    # 你的实际令牌（本地，不上传）
├── .env.example           # 令牌模板（已提交）
├── .gitignore            # 忽略规则（已提交）
└── ENV_SETUP.md          # 本说明文档
```

## 🚀 如何使用

### 1. 在代码中读取令牌

**Python 示例：**

```python
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取令牌
github_token = os.getenv('GITHUB_TOKEN')

if github_token:
    # 安全使用令牌
    print(f"Token loaded: {github_token[:4]}...{github_token[-4:]}")
```

### 2. 安装依赖（如果需要）

```bash
# 安装 python-dotenv
pip install python-dotenv

# 或使用 requirements.txt
echo "python-dotenv" >> requirements.txt
```

### 3. 分享项目时

1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 中填入实际的令牌
3. **永远不要提交 `.env` 文件**

## ⚠️ 安全注意事项

### ✅ 应该做的：
- 将 `.env` 添加到 `.gitignore`
- 使用 `.env.example` 作为模板
- 定期轮换令牌
- 使用最小权限范围的令牌

### ❌ 不应该做的：
- 将 `.env` 提交到版本控制
- 将令牌硬编码在代码中
- 在公开场合分享令牌
- 使用过期的令牌

## 🔄 令牌管理

### 创建新令牌：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择适当的权限范围
4. 复制新令牌到 `.env` 文件

### 轮换令牌：
1. 生成新令牌
2. 更新 `.env` 文件
3. 测试新令牌
4. 撤销旧令牌

## 🆘 故障排除

### 问题：令牌无法读取
- 检查 `.env` 文件是否存在
- 确认文件路径正确
- 验证文件格式：`KEY=VALUE`

### 问题：令牌无效
- 检查令牌是否过期
- 确认权限范围足够
- 在 GitHub 设置中验证令牌状态

### 问题：.env 被意外提交
```bash
# 从 Git 中移除但不删除文件
git rm --cached .env

# 提交更改
git commit -m "Remove .env from tracking"

# 确保 .env 在 .gitignore 中
echo ".env" >> .gitignore
```

## 📞 支持

如果遇到任何问题：
1. 检查本文档
2. 验证文件结构
3. 确认令牌有效性
4. 联系技术支持

---

**记住：安全第一！永远保护你的访问令牌。**