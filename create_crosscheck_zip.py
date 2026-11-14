import os
import zipfile
import fnmatch

def create_zip(source_dir, output_zip_path, installer_path=None):
    # Exclusion patterns
    EXCLUDE_DIRS = {
        'node_modules',
        'target',
        '.pytest_cache',
        '__pycache__',
        '.git',
        '.vscode',
        '.idea',
        'dist',
        'build'
    }
    
    EXCLUDE_EXTS = {
        '.pyc',
        '.pyo',
        '.pyd',
        '.log'
    }

    # Specifically avoid duplicating desktop-app/src-tauri/resources
    EXCLUDE_PATHS = [
        os.path.normpath(os.path.join(source_dir, 'desktop-app', 'src-tauri', 'resources'))
    ]

    print(f"Creating archive: {output_zip_path}")
    count = 0
    total_uncompressed = 0

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Normalize root path
            norm_root = os.path.normpath(root)

            # Prune excluded dirs
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            # Check if root is in excluded paths
            skip = False
            for ep in EXCLUDE_PATHS:
                if norm_root == ep or norm_root.startswith(ep + os.sep):
                    skip = True
                    break
            if skip:
                continue

            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in EXCLUDE_EXTS:
                    continue
                
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, os.path.dirname(source_dir))
                
                file_size = os.path.getsize(full_path)
                total_uncompressed += file_size
                zipf.write(full_path, arcname=rel_path)
                count += 1

        # Optionally add the compiled installer if it exists
        if installer_path and os.path.exists(installer_path):
            installer_name = os.path.basename(installer_path)
            arcname = os.path.join('BASIL', 'installer', installer_name)
            installer_size = os.path.getsize(installer_path)
            total_uncompressed += installer_size
            print(f"Adding installer: {installer_path} -> {arcname} ({installer_size} bytes)")
            zipf.write(installer_path, arcname=arcname)
            count += 1

    zip_size = os.path.getsize(output_zip_path)
    print(f"\nArchive creation complete!")
    print(f"Files packaged: {count}")
    print(f"Total uncompressed size: {total_uncompressed / (1024*1024):.2f} MB")
    print(f"Compressed archive size: {zip_size / (1024*1024):.2f} MB ({zip_size} bytes)")
    return zip_size

if __name__ == '__main__':
    base_dir = r"C:\Users\abys7\Downloads\BASIL-starter"
    basil_dir = os.path.join(base_dir, "BASIL")
    output_zip = os.path.join(base_dir, "BASIL_CrossCheck_Package.zip")
    installer = os.path.join(basil_dir, "desktop-app", "src-tauri", "target", "release", "bundle", "nsis", "BASIL_4.1.0_x64-setup.exe")
    
    create_zip(basil_dir, output_zip, installer)
