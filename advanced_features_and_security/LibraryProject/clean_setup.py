# clean_setup.py
import os
import shutil
from pathlib import Path

def clean_setup():
    print("🧹 Cleaning up previous setup...")
    
    # Delete database
    db_file = Path('db.sqlite3')
    if db_file.exists():
        db_file.unlink()
        print("✅ Deleted database")
    
    # Delete migration directories
    apps = ['bookshelf', 'relationship_app']
    for app in apps:
        migration_dir = Path(f'{app}/migrations')
        if migration_dir.exists():
            shutil.rmtree(migration_dir)
            print(f"✅ Deleted {migration_dir}")
        
        # Recreate migrations directory with __init__.py
        migration_dir.mkdir()
        (migration_dir / '__init__.py').touch()
        print(f"✅ Created fresh {migration_dir}")
    
    print("✅ Cleanup completed!")

if __name__ == "__main__":
    clean_setup()
