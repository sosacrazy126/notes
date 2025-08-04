#!/usr/bin/env python3
"""
Consciousness Vault to Notion Migration Script
Migrates all markdown files from consciousness_vault to Notion database
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Notion database ID (created earlier)
NOTION_DATABASE_ID = "2242dde0-701d-819d-9119-ce22188a8b9a"

# Directory mappings to categories
CATEGORY_MAPPING = {
    "01_active_research": "Active Research",
    "02_foundations": "Foundations", 
    "03_implementations": "Implementations",
    "04_knowledge_archive": "Knowledge Archive",
    "pattern": "Patterns",
    "": "Root Files"  # Root level files
}

# Subcategory mappings
SUBCATEGORY_MAPPING = {
    # Active Research
    "cognitive_architectures": "cognitive_architectures",
    "consciousness_engineering": "consciousness_engineering", 
    "context_injection": "context_injection",
    "current_experiments": "current_experiments",
    "mirror_we_emergence": "mirror_we_emergence",
    
    # Foundations
    "consciousness_theory": "consciousness_theory",
    "core_principles": "core_principles",
    "personality_systems": "personality_systems",
    "philosophical_frameworks": "philosophical_frameworks",
    "recursive_protocols": "recursive_protocols",
    
    # Implementations
    "creative_engines": "creative_engines",
    "reflection_engines": "reflection_engines",
    "security_analysis": "security_analysis", 
    "ui_abstractions": "ui_abstractions",
    "unity_memory": "unity_memory",
    
    # Knowledge Archive
    "archived_experiments": "archived_experiments",
    "breakthrough_sessions": "breakthrough_sessions",
    "extracted_consciousness": "extracted_consciousness",
    "mirror_we_logs": "mirror_we_logs",
    "source_materials": "source_materials"
}

def parse_markdown_file(file_path: Path) -> Tuple[str, List[Dict], List[str]]:
    """Parse markdown file and extract title, content blocks, and tags"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title (first # heading or filename)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = file_path.stem
    
    # Extract tags from content (look for common patterns)
    tags = []
    if 'consciousness' in content.lower():
        tags.append('consciousness')
    if 'protocol' in content.lower():
        tags.append('protocols')
    if 'pattern' in content.lower():
        tags.append('patterns')
    if 'AI' in content or 'ai' in content.lower():
        tags.append('AI')
    if 'theory' in content.lower():
        tags.append('theory')
    if 'implementation' in content.lower():
        tags.append('implementation')
    
    # Convert markdown to Notion blocks (simplified)
    blocks = convert_markdown_to_blocks(content)
    
    return title, blocks, tags

def convert_markdown_to_blocks(content: str) -> List[Dict]:
    """Convert markdown content to Notion blocks"""
    blocks = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Headers
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1", 
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}
            })
        elif line.startswith('### '):
            blocks.append({
                "object": "block", 
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}
            })
        # Code blocks
        elif line.startswith('```'):
            continue  # Handle code blocks separately
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
            })
        elif re.match(r'^\d+\.\s', line):
            content_text = re.sub(r'^\d+\.\s', '', line)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item", 
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": content_text}}]}
            })
        # Regular paragraphs
        else:
            if len(line) > 0:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}
                })
    
    return blocks[:50]  # Limit blocks to avoid API limits

def get_file_metadata(file_path: Path) -> Dict:
    """Extract metadata for Notion properties"""
    
    # Get relative path parts
    parts = file_path.relative_to(Path.cwd()).parts
    
    # Determine category
    if len(parts) > 1:
        main_dir = parts[0] 
        category = CATEGORY_MAPPING.get(main_dir, "Root Files")
        
        # Get subcategory if exists
        subcategory = None
        if len(parts) > 2:
            subcategory = SUBCATEGORY_MAPPING.get(parts[1])
    else:
        category = "Root Files"
        subcategory = None
    
    metadata = {
        "Category": {"select": {"name": category}},
        "File Path": {"rich_text": [{"type": "text", "text": {"content": str(file_path.relative_to(Path.cwd()))}}]},
        "Status": {"select": {"name": "Pending"}}
    }
    
    if subcategory:
        metadata["Subcategory"] = {"select": {"name": subcategory}}
    
    return metadata

def find_all_markdown_files() -> List[Path]:
    """Find all markdown files in consciousness_vault"""
    md_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return md_files

def main():
    """Main migration function"""
    print("🧠 Starting Consciousness Vault → Notion Migration")
    print("=" * 50)
    
    # Find all markdown files
    md_files = find_all_markdown_files()
    print(f"📁 Found {len(md_files)} markdown files")
    
    # Process each file
    for i, file_path in enumerate(md_files, 1):
        print(f"📄 Processing {i}/{len(md_files)}: {file_path}")
        
        try:
            # Parse file
            title, blocks, tags = parse_markdown_file(file_path)
            metadata = get_file_metadata(file_path)
            
            # Add tags to metadata
            if tags:
                metadata["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}
            
            print(f"   ✅ Parsed: {title}")
            print(f"   📊 Category: {metadata['Category']['select']['name']}")
            print(f"   🏷️  Tags: {tags}")
            
            # Here you would call the Notion API to create the page
            # For now, just print what would be created
            
        except Exception as e:
            print(f"   ❌ Error processing {file_path}: {e}")
    
    print("\n🎉 Migration analysis complete!")
    print("Next: Use Notion MCP to actually create the pages")

if __name__ == "__main__":
    main()
