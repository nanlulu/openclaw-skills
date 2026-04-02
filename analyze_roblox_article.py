#!/usr/bin/env python3
"""
分析Roblox文章，提取关键知识点
"""

import json
import re
from datetime import datetime

def load_article():
    """加载文章内容"""
    with open('wechat_article_20260402_112542.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_key_insights(content):
    """从文章内容中提取关键见解"""
    insights = {
        'game_title': 'Get Fat to Splash',
        'game_type': '休闲物理模拟',
        'success_metrics': {},
        'core_mechanics': [],
        'design_principles': [],
        'technical_insights': [],
        'business_insights': [],
        'development_lessons': []
    }
    
    # 提取成功指标
    metrics_patterns = [
        (r'总访问量突破(\d+)万次', 'total_visits'),
        (r'增长率高达\s*([\d.]+)%', 'growth_rate'),
        (r'全球排名\s*(\d+)位', 'global_rank')
    ]
    
    for pattern, key in metrics_patterns:
        match = re.search(pattern, content)
        if match:
            if key == 'total_visits':
                insights['success_metrics'][key] = int(match.group(1)) * 10000
            elif key == 'growth_rate':
                insights['success_metrics'][key] = float(match.group(1))
            elif key == 'global_rank':
                insights['success_metrics'][key] = int(match.group(1))
    
    # 提取核心机制
    if '吃胖→跳池→炸水花' in content:
        insights['core_mechanics'].append({
            'name': '魔性物理循环',
            'description': '吃胖→跳池→炸水花的闭环设计',
            'key_points': ['物理爽感最大化', '简单易懂的操作', '即时反馈']
        })
    
    if '进食增肥→高台跳水→水花结算→升级解锁' in content:
        insights['core_mechanics'].append({
            'name': '无断点循环',
            'description': '进食增肥→高台跳水→水花结算→升级解锁的无缝循环',
            'key_points': ['新手2秒上手', '零压力操作', '持续的正向反馈']
        })
    
    # 提取设计原则
    design_patterns = [
        (r'反常识目标.*更容易快速破圈', '反常识设计', '打破常规，创造独特体验'),
        (r'数值的膨胀可视化为了.*物理体积.*膨胀', '可视化成长', '将抽象数值转化为可见的物理变化'),
        (r'越强越痛苦，但痛苦本身很好笑', '矛盾乐趣', '在限制中创造新的游戏乐趣'),
        (r'不要试图用复杂的系统去教育玩家', '简化系统', '利用人性本能而非复杂教学')
    ]
    
    for pattern, name, desc in design_patterns:
        if re.search(pattern, content):
            insights['design_principles'].append({
                'name': name,
                'description': desc,
                'example': 'Get Fat to Splash的成功应用'
            })
    
    # 提取技术洞察
    if '物理引擎' in content:
        insights['technical_insights'].append({
            'topic': '物理引擎应用',
            'insight': '利用物理引擎创造核心游戏体验',
            'implementation': '体重→水花大小的物理计算'
        })
    
    if '碰撞箱' in content or 'Hitbox' in content:
        insights['technical_insights'].append({
            'topic': '动态碰撞系统',
            'insight': '角色碰撞箱随数值动态变化',
            'implementation': '体重增加→碰撞箱变大→产生新的游戏障碍'
        })
    
    # 提取商业洞察
    business_patterns = [
        (r'社交传播属性', '社交传播', '利用社交分享扩大用户基数'),
        (r'小团队爆款模型', '小团队模式', '验证了小团队也能创造爆款'),
        (r'撬动了数百万的流量', '低成本获客', '通过核心玩法而非营销获客')
    ]
    
    for pattern, name, desc in business_patterns:
        if re.search(pattern, content):
            insights['business_insights'].append({
                'name': name,
                'description': desc,
                'impact': '高ROI的用户获取'
            })
    
    # 提取开发经验
    dev_lessons = [
        "将数值成长可视化（体重→体积）",
        "创造反常识但有趣的核心玩法",
        "利用物理引擎创造独特的游戏体验",
        "设计简单但富有深度的循环系统",
        "平衡成长与限制（越强越慢但越有趣）",
        "重视社交分享和病毒传播",
        "关注玩家本能喜好而非复杂教学"
    ]
    
    for lesson in dev_lessons:
        if any(keyword in content for keyword in lesson[:10].split()):
            insights['development_lessons'].append(lesson)
    
    return insights

def create_skill_content(insights):
    """创建技能内容"""
    skill_content = f"""---
name: roblox-get-fat-to-splash-analysis
description: "《Get Fat to Splash》游戏深度分析 - Roblox爆款案例分析"
source: "https://mp.weixin.qq.com/s/EmVYl8yURlFWEptoRKBjUg"
extracted_at: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
---

# 《Get Fat to Splash》Roblox爆款案例分析

## 🎮 游戏概述

**游戏名称**: {insights['game_title']}
**游戏类型**: {insights['game_type']}
**分析来源**: 开物社公众号文章

## 📊 成功数据

"""
    
    # 添加成功指标
    for key, value in insights['success_metrics'].items():
        if key == 'total_visits':
            skill_content += f"- **总访问量**: {value:,} 次\n"
        elif key == 'growth_rate':
            skill_content += f"- **7日最高在线增长率**: {value}%\n"
        elif key == 'global_rank':
            skill_content += f"- **全球排名**: 第{value}位\n"
    
    skill_content += """
## 🔧 核心游戏机制

"""
    
    # 添加核心机制
    for mechanic in insights['core_mechanics']:
        skill_content += f"### {mechanic['name']}\n"
        skill_content += f"{mechanic['description']}\n\n"
        skill_content += "**关键特点**:\n"
        for point in mechanic['key_points']:
            skill_content += f"- {point}\n"
        skill_content += "\n"
    
    skill_content += """
## 🎨 设计原则

"""
    
    # 添加设计原则
    for principle in insights['design_principles']:
        skill_content += f"### {principle['name']}\n"
        skill_content += f"**描述**: {principle['description']}\n"
        skill_content += f"**案例**: {principle['example']}\n\n"
    
    skill_content += """
## 💻 技术实现洞察

"""
    
    # 添加技术洞察
    for tech in insights['technical_insights']:
        skill_content += f"### {tech['topic']}\n"
        skill_content += f"**洞察**: {tech['insight']}\n"
        skill_content += f"**实现方式**: {tech['implementation']}\n\n"
    
    skill_content += """
## 💰 商业与运营洞察

"""
    
    # 添加商业洞察
    for business in insights['business_insights']:
        skill_content += f"### {business['name']}\n"
        skill_content += f"**描述**: {business['description']}\n"
        skill_content += f"**影响**: {business['impact']}\n\n"
    
    skill_content += """
## 🎯 给开发者的启示

"""
    
    # 添加开发经验
    for i, lesson in enumerate(insights['development_lessons'], 1):
        skill_content += f"{i}. {lesson}\n"
    
    skill_content += """
## 📋 可复用的爆款模型

基于《Get Fat to Splash》的成功，可以总结出以下可复用的模型：

### 1. 核心循环设计
```
反常识目标 → 物理可视化反馈 → 社交分享传播
```

### 2. 技术实现要点
- 利用Roblox物理引擎创造核心体验
- 动态碰撞系统增加游戏深度
- 简单的数值→可视化转换

### 3. 用户增长策略
- 依靠玩法本身而非营销获客
- 设计易于分享的"史诗时刻"
- 低门槛高上限的难度曲线

## 🛠️ 实践建议

### 对于新项目
1. **从简单物理互动开始** - 不要过度复杂化
2. **测试反常识概念** - 打破常规可能带来突破
3. **重视社交传播设计** - 每个功能都考虑分享价值

### 对于现有项目
1. **检查数值可视化** - 抽象数值能否转化为可见体验
2. **简化新手引导** - 2秒上手是理想目标
3. **强化物理反馈** - 让玩家"感受"到游戏机制

## 🔍 深度分析要点

### 成功因素分解
1. **市场时机**: 在"治愈系"泛滥时推出"油腻"反套路
2. **技术应用**: 充分利用Roblox物理引擎的潜力
3. **心理洞察**: 抓住玩家对"破坏"和"反差"的本能喜好
4. **社交设计**: 每个游戏时刻都具备分享价值

### 风险评估
1. **创新风险**: 反常识设计可能不被主流接受
2. **技术风险**: 物理引擎的稳定性和性能
3. **市场风险**: 小众主题可能限制用户规模

## 📈 数据驱动决策建议

基于该案例的成功，建议关注以下指标：
- **用户留存率**: 特别是第1、7、30日留存
- **社交分享率**: 每用户平均分享次数
- **物理互动深度**: 玩家对物理机制的探索程度
- **内容创作率**: 用户生成内容的数量和质量

## 🔮 未来趋势预测

1. **物理交互游戏**将成为Roblox下一个增长点
2. **反常识设计**在饱和市场中更具竞争力
3. **小团队精品**通过精准定位挑战大厂产品

---

*本分析基于开物社公众号文章，提取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*适用于Roblox游戏开发者、产品经理、投资人参考*
"""
    
    return skill_content

def main():
    print("🔍 分析Roblox文章内容...")
    print("=" * 60)
    
    # 加载文章
    article = load_article()
    print(f"📄 文章标题: {article['title']}")
    print(f"👤 作者: {article['author']}")
    print(f"📏 内容长度: {len(article['content'])} 字符")
    
    # 提取关键见解
    insights = extract_key_insights(article['content'])
    
    print(f"\n📊 提取的见解:")
    print(f"  - 成功指标: {len(insights['success_metrics'])} 项")
    print(f"  - 核心机制: {len(insights['core_mechanics'])} 个")
    print(f"  - 设计原则: {len(insights['design_principles'])} 条")
    print(f"  - 技术洞察: {len(insights['technical_insights'])} 个")
    print(f"  - 商业洞察: {len(insights['business_insights'])} 个")
    print(f"  - 开发经验: {len(insights['development_lessons'])} 条")
    
    # 创建技能内容
    skill_content = create_skill_content(insights)
    
    # 保存技能文件
    output_file = "get-fat-to-splash-analysis.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(skill_content)
    
    print(f"\n✅ 分析完成!")
    print(f"📁 技能文件已保存: {output_file}")
    print(f"📝 文件大小: {len(skill_content)} 字符")
    
    # 显示预览
    print(f"\n📋 内容预览:")
    preview_lines = skill_content.split('\n')[:20]
    for line in preview_lines:
        print(f"  {line}")
    
    print("...")

if __name__ == "__main__":
    main()