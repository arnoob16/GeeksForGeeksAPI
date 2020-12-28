from bs4 import BeautifulSoup as bs
import requests, json

from requests.models import Response

url = 'https://auth.geeksforgeeks.org/user/arnoob16/practice/'
username = 'arnoob16'

profilePage = requests.get(url)

if profilePage.status_code == 200:
    soup = bs(profilePage.content, 'html.parser')
    response = {}
    solvedStats = {}
    solvedStats["school"] = { "count" : soup.find(href="#School").text[soup.find(href="#School").text.index("(") + 1 : soup.find(href="#School").text.index(")")]}
    solvedStats["basic"] = { "count" : soup.find(href="#Basic").text[soup.find(href="#Basic").text.index("(") + 1 : soup.find(href="#Basic").text.index(")")]}
    solvedStats["easy"] = { "count" : soup.find(href="#Easy").text[soup.find(href="#Easy").text.index("(") + 1 : soup.find(href="#Easy").text.index(")")]}
    solvedStats["medium"] = { "count" : soup.find(href="#Medium").text[soup.find(href="#Medium").text.index("(") + 1 : soup.find(href="#Medium").text.index(")")]}
    solvedStats["hard"] = { "count" : soup.find(href="#Hard").text[soup.find(href="#Hard").text.index("(") + 1 : soup.find(href="#Hard").text.index(")")]}
    
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
    mdlGrids = soup.select(".userMainDiv > .mdl-grid")
    generalInfo["name"] = soup.select("#detail1 .mdl-grid .medText")[0].text
    generalInfo["username"] = username
    generalInfo["institution"] = soup.select("#detail1 .mdl-grid a")[0].text
    generalInfo["instituteRank"] = int(mdlGrids[2].text[mdlGrids[2].text.index("#")+1:])
    generalInfo["solved"] = int(solvedStats["school"]["count"]) + int(solvedStats["basic"]["count"]) + int(solvedStats["easy"]["count"]) + int(solvedStats["medium"]["count"]) + int(solvedStats["hard"]["count"])
    try:
        generalInfo["codingScore"] = int(mdlGrids[4].text.strip()[mdlGrids[4].text.index(":")+1:mdlGrids[4].text.index("P")-2])
    except:
        generalInfo["codingScore"] = int(mdlGrids[5].text.strip()[mdlGrids[5].text.index(":")+1:mdlGrids[5].text.index("P")-2])
    try:
        generalInfo["monthlyCodingScore"] = int(mdlGrids[5].text.strip()[mdlGrids[5].text.index(":")+1:mdlGrids[5].text.index("W")-2])
    except:
        generalInfo["monthlyCodingScore"] = int(mdlGrids[6].text.strip()[mdlGrids[6].text.index(":")+1:mdlGrids[6].text.index("W")-2])
    try:
        generalInfo["weeklyCodingScore"] = int(mdlGrids[5].text.strip()[mdlGrids[5].text.index("W"):][mdlGrids[5].text.strip()[mdlGrids[5].text.index("W"):].index(":")+1:])
    except:
        generalInfo["weeklyCodingScore"] = int(mdlGrids[6].text.strip()[mdlGrids[6].text.index("W"):][mdlGrids[6].text.strip()[mdlGrids[6].text.index("W"):].index(":")+1:])
    
    response["info"] = generalInfo
    response["solvedStats"] = solvedStats
    print(json.dumps(response, indent=4))