from bs4 import BeautifulSoup as bs
import requests
import re

class scrap():

    def __init__(self,username):
        self.username = username
    
    def fetchResponse(self):
        url = 'https://auth.geeksforgeeks.org/user/{}/practice/'.format(self.username)
        profilePage = requests.get(url)

        if profilePage.status_code == 200:
            soup = bs(profilePage.content, 'html.parser')
            response = {}
            solvedStats = {}
            try:
                solvedStats["school"] = { "count" : soup.find(href="#School").text[soup.find(href="#School").text.index("(") + 1 : soup.find(href="#School").text.index(")")]}
            except:
                solvedStats["school"] = { "count" : 0 }
            try:    
                solvedStats["basic"] = { "count" : soup.find(href="#Basic").text[soup.find(href="#Basic").text.index("(") + 1 : soup.find(href="#Basic").text.index(")")]}
            except:
                solvedStats["basic"] = { "count" : 0 }
            try: 
                solvedStats["easy"] = { "count" : soup.find(href="#Easy").text[soup.find(href="#Easy").text.index("(") + 1 : soup.find(href="#Easy").text.index(")")]}
            except:
                solvedStats["easy"] = { "count" : 0 }
            try:
                solvedStats["medium"] = { "count" : soup.find(href="#Medium").text[soup.find(href="#Medium").text.index("(") + 1 : soup.find(href="#Medium").text.index(")")]}
            except:
                solvedStats["medium"] = { "count" : 0 }
            try:
                solvedStats["hard"] = { "count" : soup.find(href="#Hard").text[soup.find(href="#Hard").text.index("(") + 1 : soup.find(href="#Hard").text.index(")")]}
            except:
                solvedStats["hard"] = { "count" : 0 }

            questionTags = []

            if soup.select("#School .page-content ul") != []:
                questionTags = soup.select("#School .page-content ul li a")
                questionList = []
                for questionTag in questionTags:
                    questionList.append({ "question" : questionTag.text, "link" : questionTag.get("href")})
                solvedStats["school"]["questions"] = questionList
            else:
                solvedStats["school"]["questions"] = []

            if soup.select("#Basic .page-content ul") != []:
                questionTags = soup.select("#Basic .page-content ul li a")
                questionList = []
                for questionTag in questionTags:
                    questionList.append({ "question" : questionTag.text, "link" : questionTag.get("href")})
                solvedStats["basic"]["questions"] = questionList
            else:
                solvedStats["basic"]["questions"] = []

            if soup.select("#Easy .page-content ul") != []:
                questionTags = soup.select("#Easy .page-content ul li a")
                questionList = []
                for questionTag in questionTags:
                    questionList.append({ "question" : questionTag.text, "link" : questionTag.get("href")})
                solvedStats["easy"]["questions"] = questionList
            else:
                solvedStats["easy"]["questions"] = []

            if soup.select("#Medium .page-content ul") != []:
                questionTags = soup.select("#Medium .page-content ul li a")
                questionList = []
                for questionTag in questionTags:
                    questionList.append({ "question" : questionTag.text, "link" : questionTag.get("href")})
                solvedStats["medium"]["questions"] = questionList
            else:
                solvedStats["medium"]["questions"] = []

            if soup.select("#Hard .page-content ul") != []:
                questionTags = soup.select("#Hard .page-content ul li a")
                questionList = []
                for questionTag in questionTags:
                    questionList.append({ "question" : questionTag.text, "link" : questionTag.get("href")})
                solvedStats["hard"]["questions"] = questionList
            else:
                solvedStats["hard"]["questions"] = []

            generalInfo = {}

            def extract_detail(key, soup):
                try:
                    return next(filter(
                        lambda div: key.lower() in div.text.lower(),
                        soup.select(".userMainDiv > div")
                    )).select_one("div:nth-child(2)").text.strip()
                except Exception:
                    return ""

            def extract_num(query, soup):
                try:
                    tag = soup.find_all(lambda tag: query.lower() in tag.text.lower() and list(
                        tag.select("div")) == [])[0]
                    return re.search(r'\d+', tag.text).group()
                except Exception:
                    return ""

            generalInfo["name"] = extract_detail("Name", soup)
            generalInfo["username"] = self.username
            generalInfo["institution"] = extract_detail("Institution", soup)
            try:
                generalInfo["instituteRank"] = re.search(r'\d+', extract_detail(
                    "Rank in Institute", soup)).group()
            except Exception:
                generalInfo["instituteRank"] = ""
            generalInfo["solved"] = extract_num("Problems Solved", soup)
            generalInfo["codingScore"] = extract_num(
                "Overall Coding Score", soup)
            generalInfo["monthlyCodingScore"] = extract_num(
                "Monthly Coding Score", soup)
            generalInfo["weeklyCodingScore"] = extract_num(
                "Weekly Coding Score", soup)
            response["info"] = generalInfo
            response["solvedStats"] = solvedStats

            return response
        else:
            return {"error" : " The Profile GFG NOt Found"}
