#!/usr/bin/env python3
"""
Validation script for decouple-legacy plugin system.
Validates marketplace manifest, plugin manifests, skills, commands, and agents.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Validation result counters
passed = 0
warnings = 0
errors = 0

def log_pass(msg: str):
    global passed
    passed += 1
    print(f"{GREEN}[PASS]{RESET}: {msg}")

def log_warning(msg: str):
    global warnings
    warnings += 1
    print(f"{YELLOW}[WARNING]{RESET}: {msg}")

def log_error(msg: str):
    global errors
    errors += 1
    print(f"{RED}[ERROR]{RESET}: {msg}")

def log_section(title: str):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{title}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")

def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith('---\n'):
        return {}, content

    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_raw = parts[1]
    body = parts[2]

    # Simple YAML parser (supports basic key: value pairs)
    frontmatter = {}
    for line in frontmatter_raw.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, body

def validate_marketplace_manifest(root: Path) -> bool:
    """Validate .claude-plugin/marketplace.json."""
    log_section("Validating Marketplace Manifest")

    manifest_path = root / '.claude-plugin' / 'marketplace.json'

    if not manifest_path.exists():
        log_error(f"Marketplace manifest not found: {manifest_path}")
        return False

    log_pass(f"Marketplace manifest exists: {manifest_path}")

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in marketplace manifest: {e}")
        return False

    # Check required fields
    required_fields = ['name', 'version', 'description', 'plugins']
    for field in required_fields:
        if field not in manifest:
            log_error(f"Missing required field in marketplace manifest: {field}")
        else:
            log_pass(f"Marketplace manifest has required field: {field}")

    # Validate plugins array
    if 'plugins' in manifest:
        if not isinstance(manifest['plugins'], list):
            log_error("'plugins' field must be an array")
        else:
            for idx, plugin in enumerate(manifest['plugins']):
                if 'name' not in plugin:
                    log_error(f"Plugin #{idx} missing 'name' field")
                if 'source' not in plugin:
                    log_error(f"Plugin #{idx} missing 'source' field")
                elif 'name' in plugin:
                    # Check if source directory exists
                    source_path = root / plugin['source'].lstrip('./')
                    if not source_path.exists():
                        log_error(f"Plugin '{plugin['name']}' source directory not found: {source_path}")
                    else:
                        log_pass(f"Plugin '{plugin['name']}' source directory exists")

    return True

def validate_plugin_manifest(root: Path, plugin_name: str) -> bool:
    """Validate individual plugin manifest."""
    log_section(f"Validating Plugin: {plugin_name}")

    plugin_path = root / plugin_name
    manifest_path = plugin_path / '.claude-plugin' / 'plugin.json'

    if not manifest_path.exists():
        log_error(f"Plugin manifest not found: {manifest_path}")
        return False

    log_pass(f"Plugin manifest exists: {manifest_path}")

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in plugin manifest: {e}")
        return False

    # Check required fields
    required_fields = ['name', 'version', 'description', 'skills']
    for field in required_fields:
        if field not in manifest:
            log_error(f"Missing required field in plugin manifest: {field}")
        else:
            log_pass(f"Plugin manifest has required field: {field}")

    # Validate name matches directory
    if 'name' in manifest:
        if manifest['name'] != plugin_name:
            log_error(f"Plugin name '{manifest['name']}' does not match directory '{plugin_name}'")
        else:
            log_pass(f"Plugin name matches directory: {plugin_name}")

    # Validate skills array
    if 'skills' in manifest:
        if not isinstance(manifest['skills'], list):
            log_error("'skills' field must be an array")
        else:
            for skill_name in manifest['skills']:
                skill_path = plugin_path / 'skills' / skill_name / 'SKILL.md'
                if not skill_path.exists():
                    log_error(f"Skill not found: {skill_path}")
                else:
                    log_pass(f"Skill exists: {skill_name}")

    # Validate commands array (if present)
    if 'commands' in manifest:
        if not isinstance(manifest['commands'], list):
            log_error("'commands' field must be an array")
        else:
            for command_name in manifest['commands']:
                command_path = plugin_path / 'commands' / f'{command_name}.md'
                if not command_path.exists():
                    log_error(f"Command not found: {command_path}")
                else:
                    log_pass(f"Command exists: {command_name}")

    return True

def validate_skill(skill_path: Path) -> bool:
    """Validate individual skill."""
    skill_md = skill_path / 'SKILL.md'

    if not skill_md.exists():
        log_error(f"SKILL.md not found: {skill_md}")
        return False

    with open(skill_md, 'r') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    skill_name = skill_path.name

    # Check required frontmatter fields
    if 'name' not in frontmatter:
        log_error(f"Skill '{skill_name}' missing 'name' in frontmatter")
    elif frontmatter['name'] != skill_name:
        log_error(f"Skill name '{frontmatter['name']}' does not match directory '{skill_name}'")
    else:
        log_pass(f"Skill name matches directory: {skill_name}")

    if 'description' not in frontmatter:
        log_error(f"Skill '{skill_name}' missing 'description' in frontmatter")
    elif len(frontmatter['description']) < 30:
        log_warning(f"Skill '{skill_name}' description is too short (<30 chars)")
    else:
        log_pass(f"Skill '{skill_name}' has valid description")

    # Check for argument-hint (recommended)
    if 'argument-hint' not in frontmatter:
        log_warning(f"Skill '{skill_name}' missing 'argument-hint' (recommended)")
    else:
        log_pass(f"Skill '{skill_name}' has argument-hint")

    # Check body is not empty
    if not body.strip():
        log_error(f"Skill '{skill_name}' has empty body")
    else:
        log_pass(f"Skill '{skill_name}' has non-empty body")

    return True

def validate_command(command_path: Path, plugin_path: Path) -> bool:
    """Validate individual command."""
    if not command_path.exists():
        log_error(f"Command not found: {command_path}")
        return False

    with open(command_path, 'r') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    command_name = command_path.stem

    # Check required frontmatter fields
    if 'description' not in frontmatter:
        log_error(f"Command '{command_name}' missing 'description' in frontmatter")
    else:
        log_pass(f"Command '{command_name}' has description")

    # Check for argument-hint (recommended)
    if 'argument-hint' not in frontmatter:
        log_warning(f"Command '{command_name}' missing 'argument-hint' (recommended)")
    else:
        log_pass(f"Command '{command_name}' has argument-hint")

    # Check for skill references (e.g., **skill-name** skill)
    import re
    skill_refs = re.findall(r'\*\*([a-z-]+)\*\* skill', body)
    if skill_refs:
        skills_dir = plugin_path / 'skills'
        for skill_ref in skill_refs:
            skill_path = skills_dir / skill_ref / 'SKILL.md'
            if not skill_path.exists():
                log_warning(f"Command '{command_name}' references non-existent skill: {skill_ref}")
            else:
                log_pass(f"Command '{command_name}' skill reference valid: {skill_ref}")

    return True

def validate_agent(agent_path: Path) -> bool:
    """Validate individual agent."""
    if not agent_path.exists():
        log_error(f"Agent not found: {agent_path}")
        return False

    log_pass(f"Agent exists: {agent_path.name}")

    with open(agent_path, 'r') as f:
        content = f.read()

    # Check for required sections (basic check)
    if not content.strip():
        log_error(f"Agent '{agent_path.name}' has empty content")
    else:
        log_pass(f"Agent '{agent_path.name}' has content")

    return True

def validate_readme(plugin_path: Path) -> bool:
    """Validate plugin README.md."""
    readme_path = plugin_path / 'README.md'

    if not readme_path.exists():
        log_warning(f"README.md not found in {plugin_path.name}")
        return False

    log_pass(f"README.md exists in {plugin_path.name}")
    return True

def main():
    """Main validation entry point."""
    root = Path(__file__).resolve().parent

    if not root.exists():
        print(f"{RED}Error: Root directory not found: {root}{RESET}")
        sys.exit(1)

    print(f"{BOLD}Decouple-Legacy Plugin Validation{RESET}")
    print(f"Root: {root}\n")

    # 1. Validate marketplace manifest
    validate_marketplace_manifest(root)

    # 2. Get plugin list
    marketplace_path = root / '.claude-plugin' / 'marketplace.json'
    if marketplace_path.exists():
        with open(marketplace_path, 'r') as f:
            marketplace = json.load(f)

        plugins = [p['name'] for p in marketplace.get('plugins', [])]
    else:
        plugins = []

    # 3. Validate each plugin
    for plugin_name in plugins:
        plugin_path = root / plugin_name

        # Validate plugin manifest
        validate_plugin_manifest(root, plugin_name)

        # Validate skills
        skills_dir = plugin_path / 'skills'
        if skills_dir.exists():
            log_section(f"Validating Skills in {plugin_name}")
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    validate_skill(skill_dir)

        # Validate commands
        commands_dir = plugin_path / 'commands'
        if commands_dir.exists():
            log_section(f"Validating Commands in {plugin_name}")
            for command_file in commands_dir.glob('*.md'):
                validate_command(command_file, plugin_path)

        # Validate agents
        agents_dir = plugin_path / 'agents'
        if agents_dir.exists():
            log_section(f"Validating Agents in {plugin_name}")
            for agent_file in agents_dir.glob('*.md'):
                validate_agent(agent_file)

        # Validate README
        validate_readme(plugin_path)

    # 4. Summary
    log_section("Validation Summary")
    print(f"{GREEN}{passed} passed{RESET}, {YELLOW}{warnings} warnings{RESET}, {RED}{errors} errors{RESET}")

    if errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
