#!/usr/bin/env python3
"""
更新Roblox案例分析库
将新的案例分析整合到主技能文件中
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class CaseStudyUpdater:
    def __init__(self, skill_dir="skills/roblox-game-dev"):
        self.skill_dir = Path(skill_dir)
        self.case_studies_dir = self.skill_dir / "case-studies"
        self.skill_file = self.skill_dir / "SKILL.md"
        
        # 确保目录存在
        self.case_studies_dir.mkdir(exist_ok=True)
    
    def find_new_case_studies(self):
        """查找新的案例分析文件"""
        case_files = list(self.case_studies_dir.glob("*.md"))
        
        # 读取现有的案例列表（从技能文件中提取）
        existing_cases = self.extract_existing_cases()
        
        # 找出新的案例
        new_cases = []
        for case_file in case_files:
            case_name = self.extract_case_name(case_file)
            if case_name not in existing_cases:
                new_cases.append((case_file, case_name))
        
        return new_cases
    
    def extract_case_name(self, case_file):
        """从案例文件中提取游戏名称"""
        try:
            with open(case_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找游戏名称
            name_match = re.search(r'游戏名称[:：]\s*(.+)', content)
            if name_match:
                return name_match.group(1).strip()
            
            # 或者从标题中提取
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()
            
            return case_file.stem
            
        except Exception as e:
            print(f"❌ 读取案例文件失败 {case_file}: {e}")
            return case_file.stem
    
    def extract_existing_cases(self):
        """从技能文件中提取现有的案例名称"""
        existing_cases = []
        
        try:
            with open(self.skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找案例标题
            case_pattern = r'###\s*(?:📊\s*)?([^\n]+)'
            matches = re.findall(case_pattern, content)
            
            for match in matches:
                # 清理标题
                case_name = match.strip()
                if case_name and len(case_name) > 2:  # 过滤掉太短的
                    existing_cases.append(case_name)
        
        except Exception as e:
            print(f"❌ 读取技能文件失败: {e}")
        
        return existing_cases
    
    def parse_case_study(self, case_file):
        """解析案例分析文件，提取结构化数据"""
        try:
            with open(case_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            case_data = {
                'file': str(case_file),
                'extracted_at': datetime.now().isoformat(),
                'game_info': {},
                'metrics': {},
                'design_principles': [],
                'technical_insights': [],
                'business_insights': [],
                'development_lessons': []
            }
            
            # 提取游戏信息
            name_match = re.search(r'游戏名称[:：]\s*(.+)', content)
            type_match = re.search(r'游戏类型[:：]\s*(.+)', content)
            
            if name_match:
                case_data['game_info']['name'] = name_match.group(1).strip()
            if type_match:
                case_data['game_info']['type'] = type_match.group(1).strip()
            
            # 提取指标
            metric_pattern = r'\*\*\s*([^:]+)[:：]\s*\*\*([^\n]+)'
            metric_matches = re.findall(metric_pattern, content)
            
            for metric_name, metric_value in metric_matches:
                if '访问量' in metric_name or 'visits' in metric_name.lower():
                    case_data['metrics']['total_visits'] = metric_value.strip()
                elif '增长率' in metric_name or 'growth' in metric_name.lower():
                    case_data['metrics']['growth_rate'] = metric_value.strip()
                elif '排名' in metric_name or 'rank' in metric_name.lower():
                    case_data['metrics']['global_rank'] = metric_value.strip()
            
            # 提取设计原则
            design_section = self.extract_section(content, '设计原则')
            if design_section:
                principles = re.findall(r'###\s*([^\n]+)', design_section)
                for principle in principles:
                    case_data['design_principles'].append(principle.strip())
            
            # 提取技术洞察
            tech_section = self.extract_section(content, '技术实现洞察')
            if tech_section:
                insights = re.findall(r'###\s*([^\n]+)', tech_section)
                for insight in insights:
                    case_data['technical_insights'].append(insight.strip())
            
            # 提取商业洞察
            business_section = self.extract_section(content, '商业与运营洞察')
            if business_section:
                insights = re.findall(r'###\s*([^\n]+)', business_section)
                for insight in insights:
                    case_data['business_insights'].append(insight.strip())
            
            return case_data
            
        except Exception as e:
            print(f"❌ 解析案例分析失败 {case_file}: {e}")
            return None
    
    def extract_section(self, content, section_title):
        """从内容中提取特定章节"""
        pattern = rf'##[^#]*{re.escape(section_title)}(.*?)(?=##|$)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else None
    
    def generate_case_study_markdown(self, case_data):
        """生成案例研究的Markdown格式"""
        if not case_data or 'game_info' not in case_data:
            return ""
        
        game_name = case_data['game_info'].get('name', '未知游戏')
        game_type = case_data['game_info'].get('type', '未知类型')
        
        markdown = f"### 📊 {game_name}\n"
        markdown += f"**类型**: {game_type}\n"
        markdown += f"**分析文件**: {Path(case_data['file']).name}\n"
        markdown += f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 添加指标
        if case_data['metrics']:
            markdown += "**关键指标**:\n"
            for key, value in case_data['metrics'].items():
                markdown += f"- {key}: {value}\n"
            markdown += "\n"
        
        # 添加设计原则
        if case_data['design_principles']:
            markdown += "**设计原则**:\n"
            for principle in case_data['design_principles'][:3]:  # 取前3个
                markdown += f"- {principle}\n"
            markdown += "\n"
        
        # 添加技术洞察
        if case_data['technical_insights']:
            markdown += "**技术实现**:\n"
            for insight in case_data['technical_insights'][:2]:  # 取前2个
                markdown += f"- {insight}\n"
            markdown += "\n"
        
        # 添加商业洞察
        if case_data['business_insights']:
            markdown += "**商业策略**:\n"
            for insight in case_data['business_insights'][:2]:  # 取前2个
                markdown += f"- {insight}\n"
            markdown += "\n"
        
        # 添加启示
        if case_data['development_lessons']:
            markdown += "**开发启示**:\n"
            for lesson in case_data['development_lessons'][:3]:  # 取前3个
                markdown += f"- {lesson}\n"
        
        return markdown
    
    def update_skill_file(self):
        """更新技能文件，添加新的案例分析"""
        print("🔄 开始更新Roblox技能库...")
        
        # 查找新的案例
        new_cases = self.find_new_case_studies()
        
        if not new_cases:
            print("ℹ️  没有发现新的案例分析")
            return 0
        
        print(f"📄 发现 {len(new_cases)} 个新的案例分析:")
        
        # 读取现有的技能文件内容
        try:
            with open(self.skill_file, 'r', encoding='utf-8') as f:
                skill_content = f.read()
        except Exception as e:
            print(f"❌ 读取技能文件失败: {e}")
            return 0
        
        # 找到案例库部分的位置
        case_library_section = "## 8. 成功案例库"
        case_library_end = "## 9. 自动化分析工具"
        
        # 找到案例库部分
        start_index = skill_content.find(case_library_section)
        end_index = skill_content.find(case_library_end)
        
        if start_index == -1 or end_index == -1:
            print("❌ 找不到案例库部分")
            return 0
        
        # 构建新的内容

        new_content = skill_content[:start_index + len(case_library_section)]
        new_content += "\n\n"
        
        # 添加现有案例

        existing_section = skill_content[start_index + len(case_library_section):end_index]
        new_content += existing_section
        
        # 添加新的案例

        for case_file, case_name in new_cases:
            print(f"  添加: {case_name}")
            
            # 解析案例

            case_data = self.parse_case_study(case_file)
            if case_data:
                case_markdown = self.generate_case_study_markdown(case_data)
                new_content += case_markdown
        
        # 添加剩余内容

        new_content += skill_content[end_index:]
        
        # 备份原文件

        backup_file = self.skill_file.with_suffix('.md.backup')
        import shutil
        shutil.copy2(self.skill_file, backup_file)
        print(f"✅ 备份创建: {backup_file}")
        
        # 写入新内容

        with open(self.skill_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 技能文件已更新")
        
        return len(new_cases)
    
    def create_case_study_index(self):
        """创建案例分析索引文件"""
        case_files = list(self.case_studies_dir.glob("*.md"))
        
        index_content = "# Roblox 案例分析索引\n\n"
        index_content += f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for case_file in case_files:
            case_name = self.extract_case_name(case_file)
            case_data = self.parse_case_study(case_file)
            
            index_content += f"## {case_name}\n"
            index_content += f"- **文件**: {case_file.name}\n"
            index_content += f"- **类型**: {case_data['game_info'].get('type', '未知') if case_data else '未知'}\n"
            index_content += f"- **提取时间**: {case_data['extracted_at'] if case_data else '未知'}\n"
            
            if case_data and case_data['metrics']:
                index_content += "- **关键指标**:\n"
                for key, value in case_data['metrics'].items():
                    index_content += f"  - {key}: {value}\n"
            
            index_content += "\n"
        
        index_file = self.skill_dir / "CASE_STUDIES_INDEX.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"✅ 案例分析索引已创建: {index_file}")
        
        return index_file

def main():
    print("🚀 Roblox 案例分析更新工具")
    print("=" * 60)
    
    updater = CaseStudyUpdater()
    
    # 更新技能文件

    updated_count = updater.update_skill_file()
    
    if updated_count > 0:
        # 创建索引

        updater.create_case_study_index()
        
        print(f"\n🎉 更新完成! 添加了 {updated_count} 个新的案例分析")
        print(f"📁 案例文件位置: {updater.case_studies_dir}")
        print(f"📄 技能文件: {updater.skill_file}")
        
        # 显示更新后的案例列表

        existing_cases = updater.extract_existing_cases()
        print(f"\n📋 当前案例分析库 ({len(existing_cases)} 个案例):")
        for i, case in enumerate(existing_cases[:10], 1):
            print(f"  {i}. {case}")
        
        if len(existing_cases) > 10:
            print(f"  ... 还有 {len(existing_cases) - 10} 个案例")
    
    else:
        print("\nℹ️  没有需要更新的案例分析")

if __name__ == "__main__":
    main()