from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
import os
import csv
import time
import random
import random
import time
import concurrent.futures

def crawl_by_url(url,title,category_url):
    #Tạo thư mục
    if not os.path.exists("data"):
        os.makedirs("data")

    if 'video' in url:
        return
    article = Article(url,language="vi")
    article.download()
    article.parse()
    
    soup = BeautifulSoup(article.html, "html.parser")
    time_date_tag = soup.find("span", class_="date")
    time_date = time_date_tag.text.strip() if time_date_tag else None    
    
    image_urls = []
    for img_tag in soup.find_all("img", itemprop="contentUrl"):
        image_url = img_tag.get("data-src")
        if image_url:
            image_urls.append(image_url)
    image_urls_str = ', '.join(image_urls)
    #ouput
    output_path = os.path.join("data/","vnexpress.csv")
    with open(output_path,'a',newline="",encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if os.stat(output_path).st_size == 0:
            writer.writerow(["URL","Title","Content","Time","Images","Thuộc loại"])
        writer.writerow([url,title,article.text,time_date,image_urls_str,category_url])
def get_pages_urls_vnexpress(base_url, num_pages):
    url_list = [base_url]
    for page in range(2, num_pages + 1):
        url_list.append('{}-p{}'.format(base_url, page))
    return url_list
#print(get_pages_urls_vnexpress("http://vnexpress.net/thoi-su",4))
def crawl_and_save(url, title, category_url):
    crawl_by_url(url, title, category_url)
    time.sleep(0.5)
def get_link_pages_vnexpress(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,"html.parser")
    results = []
    
    try:
        h2_all = soup.find_all("h2", class_="title-news")
        h3_all = soup.find_all("h3", class_="title-news")

        for h2 in h2_all:
            a = h2.find("a")
            title = a.get("title")
            link = a.get("href")
            results.append([title, link])

        for h3 in h3_all:
            a = h3.find("a")
            title = a.get("title")
            link = a.get("href")
            results.append([title, link])

    except AttributeError as e:
        print(f"Error: {e}. No 'title-news' class found. Skipping URL: {url}")
    return results
#print(get_link_pages_vnexpress("http://vnexpress.net/thoi-su-p2"))
def vnexpress(base_url,num_page,category_url):
    page_urls = get_pages_urls_vnexpress(base_url,num_page)
    num_posts = 0
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"Danh sách các page của chủ đề: {page_urls}\n")
    print(f"Danh sách các page của chủ đề",page_urls)
    random.shuffle(page_urls)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for page in page_urls:
            with open('log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Đang crawler trang {page} của {category_url}\n")
                log_file.write("----------------------------------------------------------------------------------------------------------\n")
            print(f"Đang crawler trang {page} của {category_url}")
            print("----------------------------------------------------------------------------------------------------------")
            links = get_link_pages_vnexpress(page)
            print("Số bài viết của chuyên mục",len(links))
            num_posts += len(links)
            print(f"Tổng số bài viết số bài viết hiện tại {num_posts}")
            print("----------------------------------------------------------------------------------------------------------")
            with open('log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Số bài viết của chuyên mục: {len(links)}\n")
                log_file.write(f"Tổng số bài viết số bài viết hiện tại: {num_posts}\n")
                log_file.write("----------------------------------------------------------------------------------------------------------\n")
            for link in links:
                title = link[0]
                url = link[1]
                futures.append(executor.submit(crawl_and_save(url,title,category_url)))
                #delay_time = random.randint(1, 2) 
CATEGORIES = {
    'suc-khoe': 'Sức khoẻ - Y tế',
    'giao-duc': 'Giáo dục',
    'khoa-hoc': 'Khoa học',
    'so-hoa': ' Công nghệ',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch',
    'thoi-su':'Thời sự'
}
for category_url, category_name in CATEGORIES.items():
    print(f"Đang crawler chuyên mục : {category_name}")
    vnexpress(f'http://vnexpress.net/{category_url}',10,category_url)

