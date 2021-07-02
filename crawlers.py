import logging
from requests_html import HTMLSession
from lxml import html
from urllib.parse import urljoin
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup as bs4
import psycopg2
import webbrowser
import time
import sys
import io
session = HTMLSession()

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',#date time
    level=logging.INFO)
class Crawler:
    global c_id,n,counts,check_domain
    c_id = 11006
    n = 0
    counts=[]
    check_domain=[]
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
    def download_url(self, url):
        p = 0
        d = addDatabase()
        t = requests.get(url).text
        global c_id,n,strcount
        r = requests.get(url)
        strcount = str(c_id)
        response = requests.get(url, stream=True)
        file_date = response.headers.get("date")
        file_size = sys.getsizeof(t)
        url = Form(urls=[url]).run(strcount=strcount)  
        html_bytes = r.text
        soup2 = bs4(html_bytes, 'html.parser')
        L_html=str(soup2)
        token = soup2.find('div').get_text().strip()
        d.insert_data(strcount=strcount,url = url,token=token,file_date=file_date,file_size=file_size,L_html=L_html)
        print(f'Crawling so : {c_id}\n')
        return t
    def get_linked_urls(self, url, html):
        global strcount
        soup = bs4(html, 'html.parser')
        linked_url = []
        p = addDatabase()
        for link in soup.find_all('a'):
            path = link.get('href')
            linked_url.append(path)
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path
        p.insert_link(strcount=strcount,url = url,linked_url=linked_url)
    def add_url_to_visit(self, url):#add url after check url in array
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)
    
    def run(self):
        while self.urls_to_visit:
            global c_id
            finish = time.perf_counter()
            finish_time = int(finish-start)
            if finish_time>=timer:
                print(f'Crawling all : {c_id}')
                print(f'finished in {round(finish-start, 2)} second(s)')
                break
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                robots = urljoin(url,"robots.txt")
                html_robots = requests.get(robots).text
                soup2 = bs4(html_robots, 'html.parser').text
                s_dis = soup2.find("Disallow: ")+10
                posi_dis = soup2[s_dis:s_dis+10]
            except:
                pass
            try:
                self.crawl(url)
                time.sleep(3)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)
            c_id =c_id+1
        print("finish")

class Form:
    def __init__(self, urls=[]):
        self.urls_to_visit = urls
    def get_all_forms(self,url):#########
        res = session.get(url)
        soup = bs4(res.html.html, "html.parser")
        #print(soup.find_all("form"))
        return soup.find_all("form")
    def get_form_details(self,form):##########
        details = {}
        action = form.attrs.get("action")#.lower()
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value =input_tag.attrs.get("value", "")
            inputs.append({"type": input_type, "name": input_name, "value": input_value})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details
    def run(self,strcount):
        p = addDatabase()
        url = self.urls_to_visit.pop(0)
        forms = self.get_all_forms(url)
        domain = urlparse(url).netloc
        domain_name = '.'.join(domain.split('.')[1:])
        str_form = str(forms)
        if forms != []:
            p.insert_form(strcount=strcount,str_form=str_form)
        for i, form in enumerate(forms, start=1):
            form_details = self.get_form_details(form)
            #print("="*50, f"form #{i}", "="*50)
            #print(form_details)
        data = {}
        try:
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden":
                      data[input_tag["name"]] = input_tag["value"]
                elif input_tag["type"] != "submit":
                    with open('test.txt','r',encoding='utf8') as file: 
                        for line in file:
                            for word in line.split():
                                word_lower = word.lower()
                                if word_lower not in counts:
                                    counts.append(word_lower)
                    for word_domain in counts:
                        word_dd = word_domain
                        p=0
                        if not check_domain:
                            check_domain.append((word_domain,domain_name))
                            value = counts[n]
                            print(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): {value}")
                            data[input_tag["name"]] = value
                            break
                        else:
                            count_domain = len(check_domain)
                            for i in range(count_domain):
                                if word_dd in check_domain[i] and domain_name in check_domain[i]:
                                    p = p + 1
                            if p == 0:
                                check_domain.append((word_domain,domain_name))
                                value = counts[n]
                                print(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): {value}")
                                data[input_tag["name"]] = value
                            else:                            
                                data[input_tag["name"]] = input_tag["value"]

                    if len(counts) == n:
                        n = 0
                    n =n+1

            ########################################
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = session.post(url, data=data)
            elif form_details["method"] == "get":
                res = session.get(url, params=data)
                soup = bs4(res.content, "html.parser")
            #open("page.html", "w",encoding="utf-8").write(str(soup))
            #webbrowser.open("page.html") 
        except:
            pass
        return url
class addDatabase:
    def insert_data(self,strcount,url,token,file_date,file_size,L_html):
        con = psycopg2.connect(database="Crawler", user="postgres"
                       , password="Ppt6030300571@"
                       , host="127.0.0.1", port="5432")
        cur = con.cursor()
        cur.execute("INSERT INTO data_url(id,url) VALUES (%s,%s)",(strcount,url))
        cur.execute("INSERT INTO data_html(id,html_data,date,size,l_html) VALUES (%s,%s,%s,%s,%s)",(strcount,token,file_date,file_size,L_html))
        con.commit()
        con.close()
    def insert_link(self,strcount,url,linked_url):
        con = psycopg2.connect(database="Crawler", user="postgres"
                       , password="Ppt6030300571@"
                       , host="127.0.0.1", port="5432")
        cur = con.cursor()
        cur.execute("INSERT INTO url_linked(id,url,linked) VALUES (%s,%s,%s)",(strcount,url,linked_url))
        con.commit()
        con.close()
    def insert_form(self,strcount,str_form):
        con = psycopg2.connect(database="Crawler", user="postgres"
                       , password="Ppt6030300571@"
                       , host="127.0.0.1", port="5432")
        cur = con.cursor()
        cur.execute("INSERT INTO data_form(id,form_data) VALUES (%s,%s)",(strcount,str_form))
        con.commit()
        con.close()
if __name__ == '__main__':
    get_input=input('Enter URL:')
    timer = int(input('Time : '))*3600
    start = time.perf_counter()
    Crawler(urls=[get_input]).run()
