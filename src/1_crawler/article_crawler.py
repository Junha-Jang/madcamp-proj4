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

import requests
from requests.exceptions import SSLError, RequestException

def input_csv():
    table_data = []

    with open('data/raw_data/rss.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')

        for row in csv_reader:
            table_data.append(row)
            print(row)

    return table_data

def get_article_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # article_body = soup.find('div', {'class': 'article_content'})
        class_names = [
            'viewConts', #세계타임즈
            'landing-box', #KBS뉴스
            'article_cont_wrap', #경기일보
            'class4'
        ]  # 클래스 이름 목록을 추가합니다.

        # 클래스 이름 중에서 조건에 맞는 첫 번째 결과를 찾습니다.
        article_body = next(
            (
                soup.find('div', {'class': class_name})
                for class_name in class_names
                if soup.find('div', {'class': class_name}) is not None
            ), None
        )

        if article_body is not None:
            content = article_body.get_text().replace('\n', ' ')
        else:
            content = ""

        return content
    else:
        return ""

def append_article(table_data):
    table_data[0].append("redirect")
    table_data[0].append("redirectLink")
    table_data[0].append("description")
    
    for row in table_data[1:10]:
        url = row[1]
        try:
            response = requests.get(url)
            row.append("True")
            row.append(response.url)
            row.append(get_article_text(response.url))
            print(response.url)
        except SSLError:
            row.append("False")
            row.append("SSLError")
            row.append("SSLError")
            print("SSLError")
        except RequestException:
            row.append("False")
            row.append("RequestException")
            row.append("RequestException")
            print("RequestException")

        # row.append(f";{get_article_text(row[1])}")

def output_csv(table_data):
    with open('data/raw_data/rss_copy.csv', mode='w', newline='', encoding='utf-8') as file:
        # 뉴스 항목을 순회하고 제목, 링크 및 게시 날짜를 출력합니다.
        for row in table_data:
            row_as_string = ";".join(row) + '\n'
            file.write(row_as_string)

if __name__ == '__main__':
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
