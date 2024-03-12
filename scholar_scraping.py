import serpapi
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
import mechanize
from bs4 import BeautifulSoup
import requests
import warnings

def profile_results(name):
    
    # get interests
    params = {
        "api_key": "a8a16be34ca58692c0f730cb0310d5d58fca29ad3c031d68fc671eca0c408b68",                     # https://serpapi.com/manage-api-key
        "engine": "google_scholar_profiles",  # profile results search engine
        "mauthors": name,               # search query
    }
    profile_results = serpapi.search(params)
    profile_results_data = []

    profile = profile_results.get("profiles", [])[0]

    print(f'Currently extracting {profile.get("name")} with {profile.get("author_id")} ID.')
    print(profile)

    name = profile.get("name")
    link = profile.get("link")
    cited_by = profile.get("cited_by")
    interests = [profile.get("interests")[i]['title'] for i in range(len(profile.get("interests")))]

    profile_results_data.append({
        "name": name,
        "link": link,
        "cited_by": cited_by,
        "interests": interests
    })

    # get papers
    author_article_results_data = []

    params = {
        "api_key": "a8a16be34ca58692c0f730cb0310d5d58fca29ad3c031d68fc671eca0c408b68",                    # https://serpapi.com/manage-api-key
        "engine": "google_scholar_author",   # author results search engine
        "hl": "en",                          # language
        "sort": "pubdate",                   # sort by year
        "author_id": profile.get("author_id")  # search query
    }
    results = serpapi.search(params)
    for article in results.get("articles", []):
        title = article.get("title")
        link = article.get("link")
        citation_id = article.get("citation_id")

        authors = article.get("authors")
        authors_split = authors.split(',')
        pos = 0
        last_name = name.split()[-1]
        for i in range(len(authors_split)):
            if last_name in authors_split[i]:
                pos = i

        if pos > 0:
            continue

        publication = article.get("publication")
        cited_by_value = article.get("cited_by", {}).get("value")
        cited_by_link = article.get("cited_by", {}).get("link")
        cited_by_cites_id = article.get("cited_by", {}).get("cites_id")
        year = article.get("year")

        # get abstract
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(link)
        content = br.response().read()
        soup = BeautifulSoup(content, "html.parser")
        abstracts_orig = soup.find_all('div', {'class': ['gsh_small', 'gsh_csp']})
        abstracts = [abstracts_orig[i].contents[0] for i in range(len(abstracts_orig))]
        abstracts_filtered = []
        for input in abstracts:
            if input != None:
                curr = ''
                for c in str(input):
                    if c.isalpha() or c == ' ':
                        curr += c
                abstracts_filtered.append(curr)
        
        author_article_results_data.append({
            "article_title": title,
            'article_abstract': abstracts_filtered[abstracts_filtered.index(max(abstracts_filtered, key=len))],
            "article_link": link,
            "article_year": year,
            # "article_citation_id": citation_id,
            "article_authors": authors,
            # "article_publication": publication,
            # "article_cited_by_value": cited_by_value,
            # "article_cited_by_link": cited_by_link,
            # "article_cited_by_cites_id": cited_by_cites_id,
        })

    for i in range(len(author_article_results_data)):
        print(author_article_results_data[i])
        print()

profile_results('Danil Akhtiamov')