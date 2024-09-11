import os
import shutil

def delete_folders(base_path, folders_to_delete):
    for root, dirs, files in os.walk(base_path):
        for folder in folders_to_delete:
            folder_path = os.path.join(root, folder)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                print(f"Deleting folder: {folder_path}")
                shutil.rmtree(folder_path)

if __name__ == "__main__":
    base_path = "../"
    folders_to_delete = ["build", "devel"]

    delete_folders(base_path, folders_to_delete)
    print("Deletion complete.")
