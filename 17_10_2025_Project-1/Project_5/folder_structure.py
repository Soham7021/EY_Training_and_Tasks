from pathlib import Path


base_dir = Path(".")


folders = [
    base_dir / "data" / "daily_summaries",
    base_dir / "modules" / "crud_operations",
    base_dir / "modules" / "rest_api",
    base_dir / "modules" / "etl_pipeline",
    base_dir / "modules" / "queue_system",
    base_dir / "modules" / "logging_system",
    base_dir / "modules" / "analytics" / "reports",
    base_dir / "modules" / "scheduler",
    base_dir / "utils",
    base_dir / "logs",
]


for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)


files = {
    base_dir / "create_csv.py": "",
    base_dir / "requirements.txt": "",
    base_dir / "README.md": "# Project_5\n",
    base_dir / "logs" / "app.log": "",
    base_dir / "logs" / "error.log": "",
}


init_paths = [
    base_dir / "modules",
    base_dir / "modules" / "crud_operations",
    base_dir / "modules" / "rest_api",
    base_dir / "modules" / "etl_pipeline",
    base_dir / "modules" / "queue_system",
    base_dir / "modules" / "logging_system",
    base_dir / "modules" / "analytics",
    base_dir / "modules" / "scheduler",
    base_dir / "utils",
]

for init in init_paths:
    (init / "__init__.py").touch()


for file_path, content in files.items():
    file_path.write_text(content)

print("Folder structure created successfully in the current directory!")
