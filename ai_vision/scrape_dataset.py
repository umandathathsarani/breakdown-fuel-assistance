import os
import time
import requests
from duckduckgo_search import DDGS

def build_dataset(base_dir, categories, images_per_category=50):
    """
    Automates the downloading of images for CNN training using DuckDuckGo.
    """
    print("Starting automated dataset ingestion...")
    
    # Initialize the DuckDuckGo search client
    ddgs = DDGS()

    for category, query in categories.items():
        # 1. Create the specific folder for the category
        folder_path = os.path.join(base_dir, category)
        os.makedirs(folder_path, exist_ok=True)
        
        print(f"\nSearching for: '{query}' -> Saving to {folder_path}/")
        
        # 2. Fetch image URLs via API
        try:
            results = list(ddgs.images(
                keywords=query,
                region="wt-wt",
                safesearch="on",
                max_results=images_per_category + 20 # Buffer for broken links
            ))
        except Exception as e:
            print(f"Failed to fetch search results for {category}: {e}")
            continue

        # 3. Download the images
        download_count = 0
        for i, result in enumerate(results):
            if download_count >= images_per_category:
                break
                
            image_url = result.get("image")
            if not image_url:
                continue

            try:
                # Request the image with a timeout to prevent hanging
                response = requests.get(image_url, timeout=5)
                
                # Only save if the request was successful
                if response.status_code == 200:
                    # Professional practice: ensure it's actually an image
                    content_type = response.headers.get('Content-Type', '')
                    if 'image' not in content_type:
                        continue

                    # Determine file extension
                    ext = ".jpg"
                    if "png" in content_type:
                        ext = ".png"

                    file_path = os.path.join(folder_path, f"{category}_{download_count:03d}{ext}")
                    
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                        
                    download_count += 1
                    print(f"  [+] Downloaded: {file_path}")
                    
                    # Be polite to the servers (prevents IP blocking)
                    time.sleep(0.5)
                    
            except Exception as e:
                # Silently skip broken links or timeouts
                print(f"  [-] Skipped broken link: {image_url[:50]}...")

        print(f"Completed {category}: {download_count} images downloaded.")

if __name__ == "__main__":
    # Define where the images should go
    # This automatically targets: breakdown-fuel-assistance/ai_vision/dataset/train/
    target_directory = os.path.join(os.path.dirname(__file__), 'dataset', 'train')
    
    # Define your classes and the specific search queries to get accurate data
    dashboard_classes = {
        "engine": "car check engine warning light dashboard",
        "battery": "car battery warning light dashboard",
        "fuel": "car low fuel warning light dashboard",
        "oil": "car oil pressure warning light dashboard"
    }
    
    # Run the ingestion (fetching 40 images per category to start)
    build_dataset(base_dir=target_directory, categories=dashboard_classes, images_per_category=40)