import requests
import pandas as pd
import csv

from urllib.parse import urlencode
from bs4 import BeautifulSoup, NavigableString


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_detail(soup):
    detail_mode = soup.find(id="details-module", class_="module toggle-wrap")

    mode_name = detail_mode.h4.string
    value_dicts = detail_mode.select("li")
    dict = {}
    for value in value_dicts:
        type_ = value.find(class_="name").string
        name_ = value.find(class_="value").text
        name_ = "".join(name_.strip().split())
        dict[type_] = name_
    return mode_name, dict


def parse_description(soup):
    description_mode = soup.find(id="descriptionmodule", class_="module toggle-wrap")

    mode_name = description_mode.h4.string
    String = ""
    user_content = description_mode.find(class_="user-content-block")
    contents = user_content.children
    for child in contents:

        if not isinstance(child, NavigableString):
            if child.name == "p":
                String += child.text
            else:
                code_children = child.find(class_="code-java").children
                for temp in code_children:
                    if isinstance(temp, NavigableString):
                        String += temp.string
                    else:
                        String += temp.text
    return mode_name, String


def parse_people(soup):
    people_mode = soup.find(id="peoplemodule", class_="module toggle-wrap")

    mode_name = people_mode.h4.string
    dict = {}
    people_details = people_mode.find(class_="mod-content")
    dls = people_details.select("dl")
    for dl in dls:
        name_ = dl.find(name="dt").text
        value_ = dl.find(name="dd").text
        value_ = "".join(value_.strip().split())
        dict[name_] = value_

    return mode_name, dict


def parse_date(soup):
    date_mode = soup.find(id="datesmodule", class_="module toggle-wrap")

    mode_name = date_mode.h4.string
    dict = {}
    date_details = date_mode.find(class_="mod-content")
    dls = date_details.select("dl")
    for dl in dls:
        name_ = dl.find(name="dt").text
        value_ = dl.find(name="dd").text
        value_ = "".join(value_.strip().split())
        dict[name_] = value_

    return mode_name, dict


def parse_comment():
    headers = {
        'issue': "issues.apache.org",
        'Referer': "https://issues.apache.org/jira/browse/CAMEL-10597?page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel&_=1581243064077",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    params = {
        'page': 'com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel',
        '_': "1581243253858"
    }
    base_url = "https://issues.apache.org/jira/browse/CAMEL-10597?"

    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers)
    # print (type(response.content))
    content = response.content
    soup = BeautifulSoup(response.content, "lxml")
    comments = soup.find_all(class_="issue-data-block activity-comment twixi-block expanded")

    # comments = comment_mode.find_all(class_="issue-data-block activity-comment twixi-block  expanded")
    String = ""
    for comment in comments:
        content = comment.find(class_="twixi-wrap verbose actionContainer")
        children = content.children
        for child in children:
            if isinstance(child, NavigableString):
                if child.string == '\n':
                    pass
                else:
                    String += child.string.strip()
            else:
                String += child.text
    return "comments", String



def main():
    url = "https://issues.apache.org/jira/browse/CAMEL-10597"
    html = get_page(url)
    soup = BeautifulSoup(html, "lxml")
    detail_mode, detail_dict = parse_detail(soup)
    description_mode, description_string = parse_description(soup)
    people_mode, people_dict = parse_people(soup)
    date_mode, date_dict = parse_date(soup)
    comment_mode, comment_string = parse_comment()

    with open("data.csv", "w") as f:
        writer = csv.writer(f, delimiter=",")
        for name, value in detail_dict.items():
            writer.writerow([name, value])
        writer.writerow(['description', description_string])
        for name, value in people_dict.items():
            writer.writerow([name, value])
        for name, value in date_dict.items():
            writer.writerow([name, value])
        writer.writerow(["comments", comment_string])








if __name__ == "__main__":
    main()

    # print ("\n")
