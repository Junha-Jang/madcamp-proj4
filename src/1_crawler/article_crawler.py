import pandas as pd
import numpy as np

from tqdm import tqdm

import requests
from bs4 import BeautifulSoup

import requests
from requests.exceptions import SSLError, RequestException

from urllib.parse import urlparse

def input_csv():
    return pd.read_csv('data/raw_data/rss.csv', sep=';')

def get_article_domain(url):
    domain = urlparse(url).netloc
    return domain

# 도메인-검색조건 맵핑 설정
domain_conditions_map = {
    "www.cj-ilbo.com": {'tag': 'article', 'id': 'article-view-content-div'},
    "www.mediatoday.asia": {'tag': 'div', 'id': 'textinput'},
    "www.inews365.com": {'tag': 'div', 'class': 'article'}
}

def find_article_body(soup, url):
    domain = get_article_domain(url)
    condition = domain_conditions_map.get(domain, {})

    if not condition:
        return None

    tag = condition.pop('tag')
    if tag:
        article_body = soup.find(tag, condition)
    else:
        article_body = soup.find(condition)

    return article_body

"""
    기사 본문이 여러 HTML 태그에 담겨 있을 때 처리 코드

    article_body = soup.new_tag("div")
    for body_condition in search_condition:
        tag = body_condition.pop('tag', None)
        if tag:
            article_body.append(soup.find(tag, body_condition))
        else:
            article_body.append(soup.find(body_condition))
    
    return article_title, article_body
"""

def get_article_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 클래스 이름 중에서 조건에 맞는 첫 번째 결과를 찾습니다.
        article_body = find_article_body(soup, url)

        if article_body is not None:
            article_image = article_body.find("img")
            if article_image is not None:
                article_image = article_image.get("src")

            article_body = article_body.get_text(separator=' ', strip=True).replace('\n', ' ')
        else:
            article_image = None

        return article_image, article_body
    else:
        return None, None

def append_article(df):
    redirect = []
    redirectLink = []
    articleImage = []
    articleBody = []
    
    with tqdm(total=9, unit="tasks", bar_format="{percentage:3.0f}% {bar} {n_fmt}/{total_fmt} [{elapsed}]") as progress_bar:
        for idx in range(1, 10):
            row = df.loc[idx]
            url = row[1]
            try:
                response = requests.get(url)
                article_image, article_body = get_article_text(response.url)

                redirect.append("True")
                redirectLink.append(response.url)
                articleImage.append(article_image if article_image is not None else np.nan)
                articleBody.append(article_body if article_body is not None else np.nan)
            except SSLError:
                redirect.append("False")
                redirectLink.append("SSLError")
                articleImage.append(np.nan)
                articleBody.append(np.nan)
            except RequestException:
                redirect.append("False")
                redirectLink.append("RequestException")
                articleImage.append(np.nan)
                articleBody.append(np.nan)
            # row.append(f";{get_article_text(row[1])}")

            progress_bar.update(1)  # 작업 완료 시 마다 progress bar를 1 증가시킵니다.

    df['redirect'] = pd.Series(redirect + [np.nan] * (len(df) - len(redirect)))
    df['redirectLink'] = pd.Series(redirectLink + [np.nan] * (len(df) - len(redirectLink)))
    df['articleImage'] = pd.Series(articleImage + [np.nan] * (len(df) - len(articleImage)))
    df['articleBody'] = pd.Series(articleBody + [np.nan] * (len(df) - len(articleBody)))

def output_csv(df):
    df.to_csv('data/raw_data/rss_copy.csv', sep=';', index=False)

if __name__ == '__main__':
    df = input_csv()
    append_article(df)
    output_csv(df)
