import json
import requests
from bs4 import BeautifulSoup


class Club:
    def __init__(self, name, abbr, position, match_data, badge="", website="", played=0, won=0, draw=0, lost=0, points=0, goals_difference=0):
        self.website = "https://www.premierleague.com/" + website
        self.name = name
        self.abbr = abbr
        self.badge = badge
        self.position = position
        self.played = played
        self.won = won
        self.draw = draw
        self.lost = lost
        self.points = points
        self.goals_difference = goals_difference
        self.match_data = match_data.find_all("div", class_="resultWidget")
        self.players = {}
        self.scrape_players_data()

    def get_club_data(self):
        team_data = {
            "Team name": self.name,
            "Abbreviation": self.abbr,
            "Badge": self.badge,
            "Table position": self.position,
            "Matches player": self.played,
            "Matches won": self.won,
            "Matcher draw": self.draw,
            "Matches lost": self.lost,
            "Points": self.points,
            "Goal difference": self.goals_difference,
            "Next match": self.next_match(),
            "Previous match": self.prev_match(),
            "Players": self.players
        }
        return team_data

    def scrape_players_data(self):
        soup = BeautifulSoup(requests.get(self.website).content, 'html.parser')
        club_overview = soup.find("nav", class_="heroPageLinks").find("a", attrs={"href": "squad"})["href"]
        soup = BeautifulSoup(requests.get(self.website[:-8]+club_overview).content, 'html.parser')
        players_info = soup.find_all("span", class_="playerCardInfo")
        for player_info in players_info:
            player_name = player_info.find("h4", class_="name").text
            player_nr = player_info.find("span", class_="number").text
            player_pos = player_info.find("span", class_="position").text
            self.players[player_name] = {"player_number": player_nr, "player_position": player_pos}

    def prev_match(self):
        for data in self.match_data:
            if data.find("strong").text == "Recent Result":
                time = data.find("div", class_="label").text
                opponents = data.find_all("span", class_="teamName")
                score = data.find("span", class_="score").text
                for element in opponents:
                    if element.text != self.abbr:
                        opponent = element.text
                        if opponents[0].text == opponent:
                            return f"{time} \n{opponent} - {self.name}\n  {score}"
                        else:
                            return f"{time} \n{self.name} - {opponent}\n  {score}"

    def next_match(self):
        for data in self.match_data:
            if data.find("strong").text == "Next Fixture":
                time = data.find("time").text
                date = data.find("div", class_="label").text[14:]
                team_names = data.find_all("span", class_="teamName")
                for enemy in team_names:
                    if enemy.text != self.abbr:
                        return f"{self.name}'s next match takes place: {time, date} against = {enemy.text}"

