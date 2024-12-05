from bs4 import BeautifulSoup as bs
import requests
import re

class scrap():
    def __init__(self, username):
        self.username = username
    
    def fetchResponse(self):
        BASE_URL = 'https://www.geeksforgeeks.org/user/{}/'.format(self.username)

        def extract_details(soup):
            basic_details_by_index = ["institution", "languagesUsed", "campusAmbassador"]
            coding_scores_by_index = ["codingScore", "totalProblemsSolved", "monthlyCodingScore", "articlesPublished"]
            
            institution = soup.find("div", class_ = "educationDetails_head_left--text__tgi9I")
            lang_used = soup.find("div", class_ = "educationDetails_head_right--text__lLOHI")
            campusAmbas = soup.find("div", class_ = "basicUserDetails_head_CA--text__IoHEU")

            score_card = soup.find_all("div", class_ = "scoreCard_head_left--score__oSi_x")

            response = {}
            response["basic_details"] = { 
                basic_details_by_index[0]: institution.text if institution else '', 
                basic_details_by_index[1]: lang_used.text if lang_used else '',
                basic_details_by_index[2]: campusAmbas.text if campusAmbas else ''
            }
            
            response["coding_scores"] = {
                coding_scores_by_index[0]: score_card[0].text if score_card[0] else '',
                coding_scores_by_index[1]: score_card[1].text if score_card[1] else '',
                coding_scores_by_index[2]: score_card[2].text if score_card[2] and score_card[2].text != "__" else ''
            }

            return response 
            

        def extract_questions_solved_count(soup):

            difficulties = ["school", "basic", "easy", "medium", "hard"]
            result = {}

            # Structure data
            for difficulty in difficulties:
                result[difficulty] = { "count": 0, "questions": []}

            question_header = soup.find_all( "div", class_ = "problemNavbar_head_nav--text__UaGCx" )
            
            for el in question_header:
                match = re.search(r'([A-Za-z]+)\s*\(\s*(\d+)\s*\)', el.text)
                if match:
                    cat_name = match.group(1).lower()
                    cat_count = int(match.group(2))
                    result[cat_name]["count"] = cat_count


            return result


            
        
        profilePage = requests.get(BASE_URL)

        if profilePage.status_code == 200:
            response = {}
            solvedStats = {}
            generalInfo = {}
            soup = bs(profilePage.content, 'html.parser')

            generalInfo["userName"] = self.username
            
            profile_pic = soup.findAll("img", alt = self.username)[-1]
            institute_rank = soup.find("span", class_ = "educationDetails_head_left_userRankContainer--text__wt81s")
            streak_count = soup.find("div", class_ = "circularProgressBar_head_mid_streakCnt__MFOF1 tooltipped")


            try:
                generalInfo["profilePicture"] = "https://www.geeksforgeeks.org/" + profile_pic["src"]
            except:
                generalInfo["profilePicture"] = ""

            try:
                generalInfo["instituteRank"] = institute_rank.text.split(" ")[0]
            except:
                generalInfo["instituteRank"] = ""

            try:
                streak_details = streak_count.text.replace(" ", "").split("/")
                generalInfo["currentStreak"] = streak_details[0]
                generalInfo["maxStreak"] = streak_details[1]
            except:
                generalInfo["currentStreak"] = "00"
                generalInfo["maxStreak"] = "00"


            additional_details = extract_details(soup)
            question_count_details = extract_questions_solved_count(soup)
            
            for _ , value in additional_details.items():
                for _key, _value in value.items():
                    generalInfo[_key] = _value

            for key, value in question_count_details.items():
                solvedStats[key] = value

            response["info"] = generalInfo
            response["solvedStats"] = solvedStats
            return response
        else:
            return {"error" : "Profile Not Found"}
