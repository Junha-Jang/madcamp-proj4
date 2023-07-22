import csv
import requests
from bs4 import BeautifulSoup

# import ssl
# from urllib3.contrib import pyopenssl

# SSL 인증서 검증 줄이기
# ssl._create_default_https_context = ssl._create_unverified_context
# pyopenssl.inject_into_urllib3()

import ssl
import socket
from ssl import CertificateError

def input_csv():
    table_data = []

    with open('data/raw_data/rss.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')

        for row in csv_reader:
            table_data.append(row)

    return table_data

def get_article_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        article_body = soup.find('div', {'class': 'article_content'})

        content = article_body.get_text()

        return content
    else:
        return None

def check_cert(host, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.getpeercert()
        print("SSL certificate is valid")
        return True
    except CertificateError as e:
        print(f"SSL certificate error: {e}")
        return False
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
        return False
    except Exception as e:
        print(f"Other error occurred: {e}")
        return False
"""
# Test with a valid domain
domain = "www.example.com"
if check_cert(domain):
    response = requests.get(f"https://{domain}")
    print(response.content)

# Test with a domain with SSL certificate issues
domain = "www.eduyonhap.com"
if check_cert(domain):
    response = requests.get(f"https://{domain}")
    print(response.content)
"""
def append_article(table_data):
    table_data[0] += ";description"
    for row in table_data[1:]:
        url = row[1]
        if url.startswith('http://') or url.startswith('https://'):
            response = requests.get(url)
            print(response.url)

        # row.append(f";{get_article_text(row[1])}")

def output_csv(table_data):
    with open('data/raw_data/rss_copy.csv', mode='w', newline='', encoding='utf-8') as file:
        # 뉴스 항목을 순회하고 제목, 링크 및 게시 날짜를 출력합니다.
        for row in table_data:
            row_as_string = ";".join(row) + '\n'
            file.write(row_as_string)

if __name__ == '__main__':
    # response = requests.get("https://news.google.com/rss/articles/CBMiMGh0dHBzOi8vd3d3LmVkdXlvbmhhcC5jb20vbmV3cy92aWV3LnBocD9ubz03NDg5N9IBAA?oc=5")
    
    table_data = input_csv()
    append_article(table_data)
    output_csv(table_data)
"""
    url = 'https://news.google.com/rss/articles/CBMiO2h0dHBzOi8vd3d3LmNlb3Njb3JlZGFpbHkuY29tL3BhZ2Uvdmlldy8yMDIzMDcyMTEwMjk0MjIxOTQ00gEA?oc=5'
    text = get_article_text(url)

    # 파일을 쓰기 모드로 열기
    file = open('data/raw_data/article.txt', 'w')
    
    if text:
        file.write(text)
    else:
        print("Error retrieving article text.")

    # 파일을 닫기
    file.close()
"""
