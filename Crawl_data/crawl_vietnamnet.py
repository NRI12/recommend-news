
import urllib.parse
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
    time_date_tag = soup.find("div", class_="bread-crumb-detail__time")
    time_date = time_date_tag.text.strip() if time_date_tag else None    
    image_urls = []
    figure_tags = soup.find_all("figure", class_="image vnn-content-image")
    for figure_tags in figure_tags:
        img_tag = figure_tags.find("img")
        if img_tag and img_tag.has_attr("data-original"):
            image_url = img_tag["data-original"]
            image_urls.append(image_url)
    image_urls_str = ', '.join(image_urls)
    #ouput
    output_path = os.path.join("data/","vietnamnet.csv")
    with open(output_path,'a',newline="",encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if os.stat(output_path).st_size == 0:
            writer.writerow(["URL","Title","Content","Time","Images","Thuộc loại"])
        writer.writerow([url,title,article.text,time_date,image_urls_str,category_url])
#print(crawl_by_url("https://vietnamnet.vn/hai-dai-tuong-kiem-tra-chi-dao-hop-luyen-dieu-binh-chien-thang-dien-bien-phu-2267066.html","test","thoi-su"))
def crawl_and_save(url, title, category_url):
    crawl_by_url(url, title, category_url)
    time.sleep(0.5)
def get_pages_urls_vietnamnet(base_url, num_pages):
    url_list = [base_url]
    for page in range(2, num_pages + 1):
        url_list.append('{}-page{}'.format(base_url, page))
    return url_list
# VIETNAMNET
def get_link_pages_vietnamnet(url):
    base_url = url
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    results = []

    try:
        header_tags = ['h1', 'h2', 'h3', 'h4']
        for tag in header_tags:
            header_all = soup.find_all(tag, class_="horizontalPost__main-title vnn-title title-bold")
            for header in header_all:
                a = header.find("a")
                if a:
                    title = a.get("title")
                    link = urllib.parse.urljoin(base_url,a.get("href"))
                    results.append([title, link])
    except AttributeError as e:
        print(f"Error: {e}. No 'title-news' class found. Skipping URL: {url}")
    return results
#print(get_link_pages_vietnamnet("https://vietnamnet.vn/chinh-tri-page1"))
#print(get_pages_urls_vietnamnet("https://vietnamnet.vn/chinh-tri",10))
def vietnamnet(base_url,num_page,category_url):
    page_urls = get_pages_urls_vietnamnet(base_url,num_page)
    num_posts = 0
    with open('log_vietnamnet.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"Danh sách các page của chủ đề: {page_urls}\n")
    print(f"Danh sách các page của chủ đề",page_urls)
    random.shuffle(page_urls)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for page in page_urls:
            with open('log_vietnamnet.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Đang crawler trang {page} của {category_url}\n")
                log_file.write("----------------------------------------------------------------------------------------------------------\n")
            print(f"Đang crawler trang {page} của {category_url}")
            print("----------------------------------------------------------------------------------------------------------")
            links = get_link_pages_vietnamnet(page)
            print("Số bài viết của chuyên mục",len(links))
            num_posts += len(links)
            print(f"Tổng số bài viết số bài viết hiện tại {num_posts}")
            print("----------------------------------------------------------------------------------------------------------")
            with open('log_vietnamnet.txt', 'a', encoding='utf-8') as log_file:
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
    'thong-tin-truyen-thong/cong-nghe': ' Công nghệ',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch',
    'thoi-su':'Thời sự'
}
for category_url, category_name in CATEGORIES.items():
    print(f"Đang crawler chuyên mục : {category_name}")
    vietnamnet(f'https://vietnamnet.vn/{category_url}',10,category_url)

