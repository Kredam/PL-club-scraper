# from PIL import Image
# import climage
from Club import *
import requests
from bs4 import BeautifulSoup

import urllib.request

URL = "https://www.premierleague.com/tables"
premier_league = requests.get(URL)
teams = []
teams_dict = dict([])
teams_standing = dict([])

soup = BeautifulSoup(premier_league.content, "html.parser")
container = soup.find("div", class_="table wrapper col-12")
Clubs = soup.find("nav", class_="clubNavigation").find_all("span", class_="name")
Clubs = [club.get_text().rstrip() for club in Clubs]


def scrape_clubs_data():
    for club in Clubs:
        if club == "Brighton & Hove Albion":
            club = "Brighton and Hove Albion"
        badge = soup.find("tr", attrs={"data-filtered-table-row-name": club}).find("span", attrs={"data-size": 25}).findChild("img")["src"]
        position = soup.find("tr", attrs={"data-filtered-table-row-name": club})['data-position']
        team_stat = soup.find("tr", attrs={"data-filtered-table-row-name": club}).findChildren("td", class_=False)
        points = soup.find("tr", attrs={"data-filtered-table-row-name": club}).find("td", class_="points").text
        abbr = soup.find("tr", attrs={"data-filtered-table-row-name": club}).find("span", class_="short").text
        played_games = team_stat[0].text
        wins = team_stat[1].text
        draw = team_stat[2].text
        loss = team_stat[3].text
        team_website = soup.find("tr", attrs={"data-filtered-table-row-name": club}).find("td", class_="team").find("a")["href"]
        match_data = soup.find("tr", attrs={
            "data-filtered-table-row-expander": soup.find("tr", attrs={"data-filtered-table-row-name": club})[
                "data-filtered-table-row"]})
        teams_standing[club] = int(points)
        current_club = Club(club, abbr, int(position), match_data, badge, website=team_website, points=int(points),
                          played=int(played_games), won=int(wins), draw=int(draw), lost=int(loss))
        teams_dict[club] = current_club.get_club_data()


def club_statistics():
    leaderboard = sorted(teams_standing.items(), key=lambda kv: kv[1], reverse=True)
    while True:
        print("write exit to quit")
        user_input = input("Your club's name you want information about")
        if user_input == "exit":
            break
        for team_name in teams:
            if user_input == team_name:
                team_name.get_players()
                team_name.get_club_data()
# def print_badge_to_terminal():
#     for team in teams:
#         urllib.request.urlretrieve(team.badge, "badge.png")
#         output = climage.convert('badge.png')
#         img = Image.open('badge.png')
#
#         print(output, end="")
#         print(f" {team.name} position {team.position} {team.badge}")


def write_to_json(this_dir):
    with open('Teams.json', 'w') as outfile:
        json.dump(this_dir, outfile, indent=4)


scrape_clubs_data()
# club_statistics()
write_to_json(teams_dict)
