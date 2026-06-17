import os
import shutil

def cleanup_dataset():
    # Path to your training data
    base_dir = os.path.join(os.path.dirname(__file__), 'dataset', 'train')
    
    # Map the long Bing query folders to your clean folder names
    folder_mapping = {
        "car check engine light dashboard panel close up": "engine",
        "car battery warning light dashboard symbol close up": "battery",
        "car low fuel indicator warning light close up": "fuel",
        "car oil pressure warning light dashboard symbol": "oil"
    }
    
    print("--- Starting Directory Cleanup ---")
    
    for long_name, short_name in folder_mapping.items():
        source_dir = os.path.join(base_dir, long_name)
        target_dir = os.path.join(base_dir, short_name)
        
        # Ensure the target clean directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        # If the messy folder exists, move its contents
        if os.path.exists(source_dir):
            files = os.listdir(source_dir)
            moved_count = 0
            
            for file_name in files:
                source_file = os.path.join(source_dir, file_name)
                target_file = os.path.join(target_dir, file_name)
                
                # Move the file if it's not already in the target directory
                if not os.path.exists(target_file):
                    shutil.move(source_file, target_file)
                    moved_count += 1
            
            print(f"[Success] Moved {moved_count} images into '{short_name}' folder.")
            
            # Remove the now-empty long folder
            try:
                os.rmdir(source_dir)
                print(f"          Deleted empty folder: '{long_name}'")
            except OSError:
                print(f"          Warning: Could not delete '{long_name}' (it might not be empty).")
        else:
            print(f"[Skip] Folder '{long_name}' not found. Already cleaned?")

if __name__ == "__main__":
    cleanup_dataset()