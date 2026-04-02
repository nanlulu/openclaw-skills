---
name: roblox-game-dev
description: "Roblox游戏开发分析与最佳实践技能。基于《Sailor Piece》等爆款游戏的成功经验，提供从赛道选择、游戏设计、运营增长到商业化的完整指导。"
---

# Roblox 游戏开发技能

基于《Sailor Piece》（半年登顶Roblox全球第二）等成功案例的实战经验总结。

## 快速开始

```bash
# 查看Roblox游戏开发检查清单
cat checklist.txt

# 分析游戏设计文档
analyze-game-design game-design.md

# 生成开发路线图
generate-roadmap --phase=冷启动
```

## 核心模块

### 1. 赛道分析工具

**选择已验证的成功赛道：**

```python
# 赛道评估公式
def evaluate_niche(ip_power, market_size, competition, cultural_fit):
    """
    ip_power: IP影响力 (1-10)
    market_size: 市场规模 (1-10)
    competition: 竞争程度 (1-10, 越低越好)
    cultural_fit: 文化契合度 (1-10)
    """
    score = (ip_power * 0.3 + 
             market_size * 0.25 + 
             (10 - competition) * 0.25 + 
             cultural_fit * 0.2)
    return score

# 示例：海贼王赛道
score = evaluate_niche(ip_power=9, market_size=8, competition=6, cultural_fit=9)
# 得分：8.0（优秀赛道）
```

**推荐赛道：**
1. **已验证IP改编**：动漫、电影、游戏IP
2. **社交模拟**：生活模拟、角色扮演
3. **竞技挑战**：技能向、排行榜驱动
4. **创意建造**：UGC深度、创作工具

### 2. 游戏设计检查清单

创建 `game-design-checklist.txt`：

```markdown
# Roblox游戏设计检查清单

## 核心玩法（必须满足）
- [ ] 30秒内理解基础操作
- [ ] 首次5分钟获得正反馈
- [ ] 明确的核心循环（收集、建造、战斗等）
- [ ] 社交互动点设计（至少3个）

## 技术可行性
- [ ] 目标设备性能评估（低端手机30fps）
- [ ] 网络同步方案（延迟<200ms）
- [ ] 数据存储设计（玩家数据安全）
- [ ] 反作弊基础机制

## 内容规划
- [ ] 首发内容量：20+小时核心体验
- [ ] 更新节奏：每周小更新，每月大更新
- [ ] UGC支持：玩家创作工具
- [ ] 赛季规划：3个月一个主题赛季
```

### 3. 开发阶段指导

#### 阶段1：原型验证（1-2周）
```bash
# 创建最小可行产品
create-mvp --features="核心玩法,基础社交,简单UI"

# 测试指标
- 核心玩法留存率 > 40%
- 平均会话时长 > 15分钟
- 社交功能使用率 > 30%
```

#### 阶段2：内容填充（4-8周）
```bash
# 扩展游戏内容
add-content --type="任务系统,收集要素,社交功能"

# 质量检查
- 内容消耗速率：2-3小时/周
- 付费点测试：转化率 > 2%
- 性能监控：内存<500MB
```

#### 阶段3：增长运营（持续）
```bash
# 运营活动模板
create-event --type="节日活动,赛季更新,联动合作"

# 数据分析
- DAU/MAU > 0.3
- 7日留存 > 25%
- 付费ARPU > $0.5
```

### 4. 商业化设计工具

**收入模型配置：**

```json
{
  "revenue_model": {
    "primary": "cosmetic_items",
    "secondary": "battle_pass",
    "tertiary": "convenience_items",
    "advertising": "optional"
  },
  "pricing_strategy": {
    "low_tier": "$0.99-$2.99",
    "mid_tier": "$4.99-$9.99",
    "high_tier": "$19.99-$49.99",
    "bundles": ["starter_pack", "season_bundle"]
  },
  "promotion_schedule": {
    "weekly": "限时折扣",
    "monthly": "新物品发布",
    "quarterly": "大型活动"
  }
}
```

**变现健康度检查：**
```python
def check_monetization_health(arpu, conversion_rate, refund_rate):
    """
    ARPU: 平均每用户收入
    conversion_rate: 付费转化率
    refund_rate: 退款率
    """
    if arpu < 0.3:
        return "警告：收入过低，需优化付费设计"
    if conversion_rate < 0.02:
        return "警告：付费转化率低，需降低付费门槛"
    if refund_rate > 0.05:
        return "警告：退款率过高，需检查产品质量"
    return "变现模型健康"
```

### 5. 社区运营模板

**Discord服务器结构：**
```
📢 公告频道
   ├── 更新日志
   ├── 活动通知
   └── 重要公告

🎮 游戏讨论
   ├── 游戏反馈
   ├── bug报告
   ├── 功能建议
   └── 玩家创作

👥 社交互动
   ├── 组队招募
   ├── 公会招募
   └── 语音频道

🎨 创作者社区
   ├── 作品展示
   ├── 教程分享
   └── 工具交流
```

**社区活动日历：**
```yaml
weekly:
  monday: "开发者问答"
  wednesday: "玩家创作展示"
  friday: "周末活动预告"
  sunday: "社区投票"

monthly:
  first_week: "赛季更新发布"
  second_week: "创作者挑战赛"
  third_week: "玩家见面会"
  fourth_week: "数据分享会"
```

### 6. 数据分析仪表板

**关键指标监控：**
```sql
-- 每日核心指标
SELECT 
  date,
  dau,
  mau,
  dau/mau as stickiness,
  avg_session_minutes,
  retention_day7,
  conversion_rate,
  arpu
FROM game_metrics
WHERE date >= CURRENT_DATE - 30
ORDER BY date DESC;
```

**增长漏斗分析：**
```python
# 用户旅程漏斗
funnel_stages = [
    "曝光",
    "点击",
    "下载",
    "注册",
    "首次游戏",
    "核心玩法体验",
    "社交互动",
    "首次付费",
    "重复付费"
]

# 优化建议生成
def generate_optimization_suggestions(funnel_data):
    suggestions = []
    if funnel_data["曝光->点击"] < 0.1:
        suggestions.append("优化商店页面展示")
    if funnel_data["下载->注册"] < 0.7:
        suggestions.append("简化注册流程")
    if funnel_data["首次游戏->核心玩法"] < 0.5:
        suggestions.append("改进新手引导")
    return suggestions
```

### 7. 风险管理工具

**常见风险检查表：**
```markdown
## 技术风险
- [ ] 服务器稳定性（目标：99.9% uptime）
- [ ] 数据安全（加密、备份、恢复）
- [ ] 第三方服务依赖（支付、分析等）

## 运营风险
- [ ] 社区管理（ moderation 工具和策略）
- [ ] 内容审核（UGC 内容安全）
- [ ] 法律合规（年龄分级、数据隐私）

## 市场风险
- [ ] 竞争分析（每月更新）
- [ ] 用户偏好变化（季度调研）
- [ ] 平台政策变化（实时关注）
```

### 8. 成功案例库

**《Sailor Piece》关键成功因素分析：**
```yaml
game: "Sailor Piece"
success_factors:
  - ip_selection: "海贼王（全球知名IP）"
  - social_design: "强公会系统+组队玩法"
  - content_pipeline: "稳定季度大更新"
  - community_engagement: "核心玩家深度参与设计"
  - monetization: "皮肤销售+赛季通行证"

metrics:
  time_to_top: "6个月"
  peak_dau: "未公开（估计>50万）"
  revenue_model: "F2P + IAP"
  retention_day30: "估计>15%"
```

**其他参考案例：**
- `Adopt Me!`: 宠物养成社交模型
- `Brookhaven`: 角色扮演深度优化
- `Tower of Hell`: 挑战类游戏变现
- `MeepCity`: 社交枢纽设计

## 实用脚本

### 游戏性能检查脚本
```bash
#!/bin/bash
# roblox-performance-check.sh

echo "=== Roblox游戏性能检查 ==="

# 检查脚本复杂度
echo "1. 脚本复杂度分析..."
find . -name "*.lua" -exec wc -l {} + | sort -nr | head -10

# 检查模型面数
echo "2. 模型复杂度检查..."
# 添加自定义检查逻辑

# 网络优化建议
echo "3. 网络优化建议..."
echo "- 远程事件频率：建议<10次/秒"
echo "- 数据包大小：建议<1KB"
echo "- 同步策略：状态同步+事件同步混合"
```

### 更新发布检查清单
```bash
#!/bin/bash
# pre-release-checklist.sh

checklist=(
  "版本号更新"
  "更新日志编写"
  "商店页面更新"
  "社交媒体预告"
  "社区公告准备"
  "客服FAQ更新"
  "数据监控配置"
  "回滚方案准备"
)

for item in "${checklist[@]}"; do
  read -p "✅ 完成: $item? (y/n): " answer
  if [[ $answer != "y" ]]; then
    echo "⚠️  请先完成: $item"
  fi
done
```

## 资源链接

### 官方资源
- [Roblox开发者文档](https://developer.roblox.com/)
- [Roblox开发者论坛](https://devforum.roblox.com/)
- [Roblox创作者集市](https://create.roblox.com/marketplace)

### 学习资源
- [Roblox Lua最佳实践](https://roblox.github.io/lua-style-guide/)
- [性能优化指南](https://developer.roblox.com/articles/optimization)
- [商业化设计案例](https://developer.roblox.com/en-us/articles/monetization)

### 工具推荐
- **Rojo**: Roblox项目同步工具
- **Wally**: Roblox包管理器
- **Selene**: Lua静态分析工具
- **TestEZ**: 测试框架

## 更新计划

- [ ] 添加更多成功案例分析
- [ ] 开发自动化分析工具
- [ ] 创建模板项目
- [ ] 集成A/B测试框架

---

**使用提示**：在游戏开发的不同阶段，使用对应的模块进行检查和优化。定期回顾成功案例，避免常见陷阱。