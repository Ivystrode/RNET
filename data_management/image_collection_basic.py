import os, requests
from bs4 import BeautifulSoup

"""
Most search engines make this scraper of negligible utility ie can only get 21 images at a time (of low quality as well)
"""

google_url = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

user_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

save_folder = "media"

def main():
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
        
    provider = input("Choose provider:\n- ddg\n- google\n>>")
    get_images(provider)
    
def get_images(provider):
    data = input("Pictures of: ")
    n_images = int(input("How many: "))
    print("Searching...")
    if provider == "google":
        search_url = f"{google_url}q={data}"
    elif provider == "ddg":
        search_url = f"https://duckduckgo.com/?t=lm&q={data}&iax=images&ia=images"
    else:
        print("oops")
    print(f"Searching {provider}")

    response = requests.get(search_url, headers=user_agent)
    page_source = response.text
    
    # crawl the html and extract the images
    soup = BeautifulSoup(page_source, 'html.parser')
    if provider == "google":
        results = soup.select('img', {'class':'rg_i'}, limit=n_images) # the class names may change/update
    elif provider == "ddg":
        results = soup.select('img', {'class':'tile--img__img'}, limit=n_images) 
    else:
        print("oops")
    images = [result['src'] for result in results]
    
    print(f"Found {len(images)} images")
    
    print("Downloading...")
    downloaded = 0
    for i, image in enumerate(images):
        try:
            response = requests.get(image)
            
            filename = f"{save_folder}/{data}_{i}.jpg"
            with open(filename, "wb") as f:
                f.write(response.content)
                
            downloaded += 1
        except Exception as e:
            print(f"Error: {e}")
            
    print(f"Downloaded {downloaded} images of: {data} from {provider}")
    
    



if __name__ == '__main__':
    main()