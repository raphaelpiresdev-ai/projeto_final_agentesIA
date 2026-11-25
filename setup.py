from pathlib import Path

base_dir = Path("saas-agent")

files = [
    "agent/__init__.py",
    "agent/prompts.py",
    "agent/tools.py",
    "agent/state.py",
    "agent/graph.py",
    "api/__init__.py",
    "api/server.py",
    ".env",
    ".env.example",
    ".gitignore",
    "pyproject.toml",
    "README.md",
]

for file_path in files:
    full_path = base_dir / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.touch(exist_ok=True)

# Adiciona conteúdo padrão ao .gitignore
gitignore_content = """__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env
dist/
build/
*.egg-info/
.DS_Store
"""
(base_dir / ".gitignore").write_text(gitignore_content, encoding="utf-8")

print(f"Estrutura '{base_dir}' criada com sucesso!")