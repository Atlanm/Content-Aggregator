from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

space = requests.get('https://www.mehrnews.com/tag/%D8%A7%DA%A9%D8%AA%D8%B4%D8%A7%D9%81%D8%A7%D8%AA+%D9%81%D8%B6%D8%A7%DB%8C%DB%8C', verify=False)
sport = requests.get('https://www.mehrnews.com/tag/%D9%88%D8%B1%D8%B2%D8%B4', verify=False)
politics = requests.get('https://www.mehrnews.com/tag/%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C', verify=False)

space_soup = BeautifulSoup(space.content, 'html.parser')
sport_soup = BeautifulSoup(sport.content, 'html.parser')
politics_soup = BeautifulSoup(politics.content, 'html.parser')


# print(space_soup)
space_news = space_soup.find_all('div', class_='desc')
sport_news = sport_soup.find_all('div', class_='desc')
politics_news = politics_soup.find_all('div', class_='desc')
# print(space_news)
links = list('')
titles = list('')


def extract_link_and_title(html_finds):
    links=[]
    titles=[]
    for i in html_finds[0:9]:
        j = list(i.find_all('a'))
        # print(type(len(j)))
        if len(j) == 3:
            a_str = str(j[1])
        else:
            a_str = str(j[0])
        link = re.findall("href=\".*?\"", a_str)
        link = str(link)
        re_link = str(link[8:-3])
        title = re.findall(">.*?<", a_str)
        title = str(title)
        re_title = str(title[3:-3])
        # print(type(re_link), re_link)
        links.append(re_link)
        titles.append(re_title)
    return [links, titles]


[space_links, space_titles] = extract_link_and_title(space_news)
[sport_links, sport_titles] = extract_link_and_title(sport_news)
[politics_links, politics_titles] = extract_link_and_title(politics_news)
# for i in space_titles:
#     print(type(space_titles), i)
# print(type(space_links), space_links)
# print(space_titles)
# space_dict = dict()


def dict_gen(link, title):
    counter = 0
    jinja_use_dict = dict()
    for key in title:
        jinja_use_dict[key] = link[counter]
        counter += 1
    return jinja_use_dict


space_dict = dict_gen(space_links, space_titles)
sport_dict = dict_gen(sport_links, sport_titles)
politics_dict = dict_gen(politics_links, politics_titles)

# for i in space_dict:
#     print(i, space_dict[i])


@app.route('/')
def hello_world():
    return render_template('index.html', space_list=space_dict, sport_list=sport_dict, politics_list=politics_dict)


if __name__ == '__main__':
    app.run(debug=True)
