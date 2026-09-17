from pathlib import Path

for source_kb in Path("data").iterdir():
        if source_kb.is_dir():
            for file in source_kb.iterdir():
                print(f"{source_kb.name}\n{file.name}")


