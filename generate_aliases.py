#!/usr/bin/env python3
import os

# Root directories to scan for projects
SCAN_DIRS = [
    '/home/hod/IdeaProjects',
    '/mnt/c/Users/dhaup/IdeaProjects'
]

# Excluded directory names (do not recurse into these)
EXCLUDE_DIRS = {
    'node_modules', 'build', 'dist', 'out', 'target', 'bin', 'obj', 'tmp', 'temp',
    'phone', 'screenshots', '.git', '.idea', '.venv', '.gradle', '.kotlin'
}

# Explicit overrides for project names mapped by absolute path
PATH_NAME_OVERRIDES = {
    '/home/hod/IdeaProjects/lights_2026': 'lights',
    '/home/hod/IdeaProjects/serious/lights': 'serious_lights',
}

# Directories that are not git repositories but should be considered projects
NON_GIT_PROJECTS = {
    '/mnt/c/Users/dhaup/IdeaProjects/ML',
}

def scan_projects(root_dir):
    projects = []
    
    # We walk the directory tree.
    for root, dirs, files in os.walk(root_dir):
        # Filter out excluded directories in-place to prevent os.walk from recursing
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        # Check if the current directory is a project
        is_git_project = '.git' in dirs or os.path.exists(os.path.join(root, '.git'))
        is_non_git_project = root in NON_GIT_PROJECTS
        
        if is_git_project or is_non_git_project:
            # We found a project! Do not recurse further
            dirs[:] = []
            projects.append(root)
            
    return projects

def get_alias_name(path):
    if path in PATH_NAME_OVERRIDES:
        return PATH_NAME_OVERRIDES[path]
    
    # Leaf folder name
    leaf = os.path.basename(path)
    # Normalize: lowercase, replace hyphen with underscore
    name = leaf.lower().replace('-', '_')
    return name

def main():
    all_projects = []
    for scan_dir in SCAN_DIRS:
        if os.path.isdir(scan_dir):
            all_projects.extend(scan_projects(scan_dir))
            
    # Sort projects by alias name for consistent output
    project_mappings = []
    for p in all_projects:
        name = get_alias_name(p)
        project_mappings.append((name, p))
        
    project_mappings.sort(key=lambda x: x[0])
    
    # Generate the alias file content
    lines = []
    lines.append("alias co='codex --dangerously-bypass-approvals-and-sandbox'")
    lines.append("")
    
    # Codex aliases
    lines.append("# Project shortcuts")
    lines.append("alias CO_roguerocketriot='cd /home/hod/IdeaProjects/roguerocketriot && codex --dangerously-bypass-approvals-and-sandbox'")
    for name, path in project_mappings:
        lines.append(f"alias co_{name}='cd {path} && codex --dangerously-bypass-approvals-and-sandbox'")
    lines.append("")
    
    # Claude Code aliases
    lines.append("# Claude Code project shortcuts")
    for name, path in project_mappings:
        lines.append(f"alias cc_{name}='cd {path} && claude --dangerously-skip-permissions'")
    lines.append("")
    
    # Antigravity aliases
    lines.append("# Antigravity project shortcuts")
    for name, path in project_mappings:
        lines.append(f"alias ag_{name}='cd {path} && agy --dangerously-skip-permissions'")
    lines.append("")
    
    # OpenCode aliases
    lines.append("# OpenCode (DeepSeek) project shortcuts")
    for name, path in project_mappings:
        lines.append(f"alias oc_{name}='cd {path} && opencode'")
    lines.append("")
    
    content = "\n".join(lines)
    
    # Write to target files
    home_path = os.path.expanduser('~/.bash_aliases')
    repo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.bash_aliases')
    
    with open(home_path, 'w') as f:
        f.write(content)
    print(f"Successfully updated {home_path}")
    
    with open(repo_path, 'w') as f:
        f.write(content)
    print(f"Successfully updated {repo_path}")

if __name__ == '__main__':
    main()
