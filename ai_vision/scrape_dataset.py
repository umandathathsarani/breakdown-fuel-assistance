import os
from bing_image_downloader import downloader

def build_dataset(output_directory, categories, limit_per_category=40):
    """
    Professional data ingestion pipeline using Bing's media indexing engine.
    Bypasses signature verification rate-limits.
    """
    print("--- Initializing Resilient Dataset Ingestion Pipeline ---")
    
    for category_name, search_query in categories.items():
        print(f"\n[Task] Ingesting Category: '{category_name}' using query: '{search_query}'")
        
        try:
            # The downloader automatically handles folder generation, timeout loops, user-agent spoofing, and link checking.
            downloader.download(
                search_query,
                limit=limit_per_category,
                output_dir=output_directory,
                adult_filter_off=True,
                force_replace=False,
                timeout=60,
                verbose=True
            )
            
            # Professional Cleanup: Bing saves folders matching the full query string. We rename the folder to match our exact required clean class names: battery, engine, fuel, oil.
            raw_folder_path = os.path.join(output_directory, search_query)
            target_folder_path = os.path.join(output_directory, category_name)
            
            if os.path.exists(raw_folder_path):
                # If target folder exists from previous attempts, merge or handle it cleanly
                if os.path.exists(target_folder_path):
                    for file in os.listdir(raw_folder_path):
                        src_file = os.path.join(raw_folder_path, file)
                        dst_file = os.path.join(target_folder_path, file)
                        if not os.path.exists(dst_file):
                            os.rename(src_file, dst_file)
                    os.rmdir(raw_folder_path)
                else:
                    os.rename(raw_folder_path, target_folder_path)
                    
            print(f"[Success] Category '{category_name}' processing finalized.")
            
        except Exception as e:
            print(f"[Error] Failed to securely process category '{category_name}': {e}")

if __name__ == "__main__":
    # Point directly to your active training directory tree
    target_dir = os.path.join(os.path.dirname(__file__), 'dataset', 'train')
    
    # Highly specific keyword structures ensuring professional, clean image returns
    dashboard_classes = {
        "engine": "car check engine light dashboard panel close up",
        "battery": "car battery warning light dashboard symbol close up",
        "fuel": "car low fuel indicator warning light close up",
        "oil": "car oil pressure warning light dashboard symbol"
    }
    
    # Execute the collection loop
    build_dataset(output_directory=target_dir, categories=dashboard_classes, limit_per_category=40)