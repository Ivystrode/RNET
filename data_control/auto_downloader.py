from selenium import webdriver
from selenium.webdriver.common.by import By
import argparse, os, requests, time

"""
Mass image downloader for model training
Still slightly buggy but good enough for now...
"""

# NEED TO MAKE DT1 AND 2 THE SAME FOR PATH
cdriver = "/home/main/Documents/File_Root/Main/Code/Projects/rnet/rnet/data_management/chromedriver"

wd = webdriver.Chrome(cdriver)
save_folder = ""

global_download_count = 0

def image_search(wd, subject, delay, n_images):
    url = f'https://www.google.com/search?q={subject}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwja3qmJwqX0AhU1RuUKHbnODqsQ_AUoAnoECAEQBA&biw=1920&bih=968&dpr=1'
    skipped_images = 0
    
    def scrolldown(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight)") # scroll down with a quick pause
        time.sleep(delay)
        
    wd.get(url) # load the page
    image_urls = set() # not a list so we dont get duplicates
    
    while len(image_urls) + skipped_images < n_images:
        scrolldown(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd") # dont know why chrome uses this as a class name
        
        # this stops us looping through thumbnails we've already looped through
        # we start looping only AFTER the ones we've already added to the list!
        for image in thumbnails[len(image_urls)+skipped_images: n_images]:
            try:
                image.click()
                time.sleep(delay)
                
            except:
                continue # just try the next...
            
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            
            for i in images:
                n_images += 1
                skipped_images += 1
                if i.get_attribute("src") in image_urls:
                    break
                
                if i.get_attribute('src') and 'http' in i.get_attribute('src'):
                    # if we can find a source add it to our image set
                    image_urls.add(i.get_attribute('src'))
                    print(f"Added {i.get_attribute('src')}")
                    
    return image_urls

def download_img(subject, img_url):
    global global_download_count
    global save_folder
    save_folder = str(subject)
    
    try:
        response = requests.get(img_url)
        
        if not os.path.exists("datasets"):
            os.mkdir("datasets")
            
        # don't like how DRY this is but it "just werks"
        if not os.path.exists(f"datasets/{save_folder}"):
            os.mkdir(f"datasets/{save_folder}")
            if not os.path.exists(f"datasets/{save_folder}/train"):
                os.mkdir(f"datasets/{save_folder}/train")
                if not os.path.exists(f"datasets/{save_folder}/train/1"):
                    os.mkdir(f"datasets/{save_folder}/train/1")
            
        filename = f"datasets/{save_folder}/train/1/{subject}_{global_download_count}.jpg"
        
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {global_download_count}")
        global_download_count += 1
        
    except Exception as e:
        print(f"Failed: {e}")
        
    # global_download_count += 1
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", "--subject", help="images of...?")
    parser.add_argument("-n", "--number", help="how many...?")
    args = parser.parse_args()
    print(vars(args)['subject'])
    
    images = image_search(wd,
                          vars(args)['subject'],
                          1,
                          int(vars(args)['number'])
                          )
    
    
    print(f"{len(images)} to download")
    time.sleep(2)
    
    for i, url in enumerate(images):
        print(url)
        download_img(vars(args)['subject'], url)
        
    random_images = input("Download random images to train against? y/n\n>>")
    if random_images == "y":

        if not os.path.exists(f"datasets/{vars(args)['subject']}/train/0"):
            os.mkdir(f"datasets/{vars(args)['subject']}/train/0")
        
        for i in range(int(vars(args)['number'])):
            url = "https://picsum.photos/200/200/?random"
            response = requests.get(url)
            filename = f"datasets/{vars(args)['subject']}/train/0/rands_{str(i)}.jpg"
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    print("saving: " + filename)
                    f.write(response.content)
                print(f"Downloaded {i}")
                    
    wd.quit()
    