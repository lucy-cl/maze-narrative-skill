import os
import yaml
import sys

def validate_maze_skill():
    print("🔍 Starting Maze Engine Skill Validation...")
    errors = []
    
    # 1. 检查目录结构规范
    # 官方标准：skills/<skill-name>/SKILL.md
    skill_root = "skills"
    if not os.path.exists(skill_root):
        errors.append("❌ Missing 'skills/' directory at root.")
        return errors
    
    skill_dirs = [d for d in os.listdir(skill_root) if os.path.isdir(os.path.join(skill_root, d))]
    if not skill_dirs:
        errors.append("❌ No skill directories found inside 'skills/'.")
    
    for skill_name in skill_dirs:
        # 检查命名规范 (小写 + 连字符)
        if not skill_name.islower() or " " in skill_name or "_" in skill_name:
            errors.append(f"⚠️ Skill folder '{skill_name}' should use kebab-case (e.g., 'maze-engine').")
            
        skill_file = os.path.join(skill_root, skill_name, "SKILL.md")
        if not os.path.exists(skill_file):
            errors.append(f"❌ Missing SKILL.md in '{skill_name}'.")
            continue
            
        # 2. 检查 Frontmatter (元数据)
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 简单的 Frontmatter 解析
            if not content.startswith("---"):
                errors.append(f"❌ '{skill_name}/SKILL.md' missing YAML frontmatter start (---).")
            
            # 提取 YAML 块
            yaml_part = content.split("---")[1]
            meta = yaml.safe_load(yaml_part)
            
            # 检查必要字段
            required_keys = ["name", "description"]
            for key in required_keys:
                if key not in meta:
                    errors.append(f"❌ '{skill_name}' missing required key: '{key}'.")
            
            # 检查 Description 质量 (你的三门协议之一)
            desc = meta.get("description", "")
            if len(desc) < 50:
                errors.append(f"⚠️ '{skill_name}' description is too short. Claude needs context to trigger it.")
                
            print(f"✅ '{skill_name}' structure and metadata passed.")
            
        except Exception as e:
            errors.append(f"❌ YAML Parsing error in '{skill_name}': {str(e)}")

    # 3. 检查资源引用 (Menu Approach Check)
    # 确保 SKILL.md 中引用的相对路径 (../../library) 是存在的
    # (此处为简化逻辑，可根据需要扩展正则检查)

    return errors

if __name__ == "__main__":
    validation_errors = validate_maze_skill()
    if validation_errors:
        print("\n🚫 Validation FAILED with errors:")
        for err in validation_errors:
            print(err)
        sys.exit(1)
    else:
        print("\n✨ All systems go! Skill is ready for release.")
        sys.exit(0)