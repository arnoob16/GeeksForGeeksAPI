from bs4 import BeautifulSoup as bs
from flask import request, redirect, jsonify

import requests, json

def fetchResponse(username):
    url = 'https://auth.geeksforgeeks.org/user/{}/practice/'.format(username)
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
        
        try:
            mdlGrids = soup.select(".userMainDiv > .mdl-grid")
            noOfMdlGrids = len(mdlGrids)
            generalInfo["name"] = mdlGrids[0].text[6:mdlGrids[0].text.index("\n", 6)]
            generalInfo["username"] = username
            generalInfo["institution"] = soup.select("#detail1 .mdl-grid a")[0].text
            generalInfo["instituteRank"] = int(mdlGrids[2].text[mdlGrids[2].text.index("#")+1:])
            generalInfo["solved"] = int(solvedStats["school"]["count"]) + int(solvedStats["basic"]["count"]) + int(solvedStats["easy"]["count"]) + int(solvedStats["medium"]["count"]) + int(solvedStats["hard"]["count"])
            generalInfo["codingScore"] = int(mdlGrids[noOfMdlGrids - 3].text.strip()[mdlGrids[noOfMdlGrids - 3].text.index(":")+1:mdlGrids[noOfMdlGrids - 3].text.index("P")-2])
            generalInfo["monthlyCodingScore"] = int(mdlGrids[noOfMdlGrids - 2].text.strip()[mdlGrids[noOfMdlGrids - 2].text.index(":")+1:mdlGrids[noOfMdlGrids - 2].text.index("W")-2])
            generalInfo["weeklyCodingScore"] = int(mdlGrids[noOfMdlGrids - 2].text.strip()[mdlGrids[noOfMdlGrids - 2].text.index("W"):][mdlGrids[noOfMdlGrids - 2].text.strip()[mdlGrids[noOfMdlGrids - 2].text.index("W"):].index(":")+1:])
            response["info"] = generalInfo
            response["solvedStats"] = solvedStats
        except:
            return {"error" : "Profile Not Found"}

        return response
    else:
        return {"error" : "Profile Not Found"}
