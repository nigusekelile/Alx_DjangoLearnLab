# fix_duplicate_registration.py
import os
import shutil

def fix_duplicate_registration():
    print("🔧 Fixing duplicate CustomUser registration...")
    
    # Clean cache files
    print("1. Cleaning cache files...")
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
                print(f"   Deleted: {os.path.join(root, dir_name)}")
        for file_name in files:
            if file_name.endswith('.pyc'):
                os.remove(os.path.join(root, file_name))
                print(f"   Deleted: {os.path.join(root, file_name)}")
    
    # Check relationship_app/admin.py for CustomUser registration
    print("2. Checking relationship_app/admin.py...")
    admin_file = 'relationship_app/admin.py'
    if os.path.exists(admin_file):
        with open(admin_file, 'r') as f:
            content = f.read()
        
        # Remove CustomUser registration if it exists
        if '@admin.register(CustomUser)' in content or 'CustomUser' in content:
            print("   Found CustomUser in relationship_app/admin.py - fixing...")
            # Create a clean version without CustomUser
            lines = content.split('\n')
            clean_lines = []
            skip_next = False
            for i, line in enumerate(lines):
                if '@admin.register(CustomUser)' in line:
                    skip_next = True
                    continue
                if skip_next and line.strip().startswith('class ') and 'Admin' in line:
                    skip_next = False
                    continue
                if not skip_next:
                    clean_lines.append(line)
            
            with open(admin_file, 'w') as f:
                f.write('\n'.join(clean_lines))
            print("   ✅ Fixed relationship_app/admin.py")
        else:
            print("   ✅ relationship_app/admin.py is clean")
    
    print("✅ Fix completed!")

if __name__ == "__main__":
    fix_duplicate_registration()
