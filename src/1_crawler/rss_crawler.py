# https://news.google.com/rss/search?q=기술&hl=ko&gl=KR&ceid=KR:ko
# https://news.google.com/rss/search?q=[검색어]&hl=[언어 코드]&gl=[국가 코드]&ceid=[국가 코드]:[언어 코드]

import feedparser
from datetime import datetime

def input_search():
    with open('data/search_keywords.txt', mode='r', newline='', encoding='utf-8') as file:
        # 파일의 내용을 읽어 변수에 저장
        content = file.read()

    # 읽어온 내용을 출력
    print(content)

    return content

def input_rss(content):
    # RSS 피드 링크를 설정합니다.
    rss_link = 'https://news.google.com/rss/search?q=' + content + '&hl=ko&gl=KR&ceid=KR:ko'

    # feedparser를 사용하여 뉴스 정보를 가져옵니다.
    return feedparser.parse(rss_link)

def output_rss(feed):
    with open('data/raw_data/rss.csv', mode='w', newline='', encoding='utf-8') as file:
        # 뉴스 항목을 순회하고 제목, 링크 및 게시 날짜를 출력합니다.
        file.write("Title;")
        file.write("Link;")
        file.write("Published")
        file.write("\n")
        for entry in feed.entries:
            # Wed, 31 May 2023 07:00:00 GMT -> 2023-05-42 07:00:00
            entry.published = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")

        feed.entries = sorted(feed.entries, key=lambda x: x.published, reverse=True)

        for entry in feed.entries:
            file.write(f"{entry.title};")
            file.write(f"{entry.link};")
            file.write(entry.published.strftime("%Y-%m-%d %H:%M:%S"))
            file.write("\n")

if __name__ == '__main__':
    content = input_search()
    feed = input_rss(content)
    output_rss(feed)