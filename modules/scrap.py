from bs4 import BeautifulSoup as bs
import requests
import re

class scrap():
    def __init__(self, username):
        self.username = username
    
    def fetchResponse(self):
        BASE_URL = 'https://auth.geeksforgeeks.org/user/{}/practice/'.format(self.username)

        def extract_text_from_elements(elements, element_keys):
            result = {}
            index = 0
            for element in elements:
                try:
                    inner_text = element.text
                    if inner_text == '_ _':
                        result[element_keys[index]] = ""
                    else:
                        result[element_keys[index]] = inner_text
                except: 
                    result[element_keys[index]] = ""
                index += 1
            return result

        def extract_details(soup):
            basic_details_by_index = ["institution", "languagesUsed", "campusAmbassador"]
            coding_scores_by_index = ["codingScore", "totalProblemsSolved", "monthlyCodingScore", "articlesPublished"]
            basic_details = soup.find_all("div", class_ = "basic_details_data")
            coding_scores = soup.find_all("span", class_ = "score_card_value")

            score_divs = soup.find_all('div', class_='scoreCard_head_left--score__oSi_x')
            all_div_values = [div.get_text(strip=True) for div in score_divs]
            if len(all_div_values) > 2 and all_div_values[2] == "__":
                all_div_values[2] = "N/A"

            gfgrating = all_div_values[2] if len(all_div_values) > 2 else 'N/A'

            # Convert gfgrating to int: if it's "N/A", set to 0; otherwise, convert to an integer
            gfgrating = 0 if gfgrating == "N/A" else int(gfgrating)




            response = {}
            response["basic_details"] = extract_text_from_elements(basic_details, basic_details_by_index)
            response["coding_scores"] = extract_text_from_elements(coding_scores, coding_scores_by_index)
            response["gfgrating"] = gfgrating
            return response 
            
        def extract_questions_by_difficulty(soup, difficulty):
            try: 
                response = {}
                questions = []
                question_list_by_difficulty_tag = soup.find("div", id = difficulty.replace("#", "")).find_all("a")
                response["count"] = len(question_list_by_difficulty_tag)
                
                for question_tag in question_list_by_difficulty_tag:
                    question = {}
                    question["question"] = question_tag.text
                    question["questionUrl"] = question_tag["href"]
                    questions.append(question)

                response["questions"] = questions
                return response
            except:
                return { "count": 0, "questions": [] }

        def extract_questions_solved_count(soup):
            difficulties = ["#school", "#basic", "#easy", "#medium", "#hard"]
            result = {}
            for difficulty in difficulties:
                result[difficulty] = extract_questions_by_difficulty(soup, difficulty)
                
            return result

        profilePage = requests.get(BASE_URL)

        if profilePage.status_code == 200:
            response = {}
            solvedStats = {}
            generalInfo = {}
            soup = bs(profilePage.content, 'html.parser')

            generalInfo["userName"] = self.username
            
            profile_pic = soup.find("img", class_ = "profile_pic")
            institute_rank = soup.find("span", class_ = "rankNum")
            streak_count = soup.find("div", class_ = "streakCnt")

            try:
                generalInfo["profilePicture"] = profile_pic["src"]
            except:
                generalInfo["profilePicture"] = ""

            try:
                generalInfo["instituteRank"] = institute_rank.text
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
                if isinstance(value, dict):  # Only attempt to use .items() on dictionaries
                    for _key, _value in value.items():
                        generalInfo[_key] = _value
                else:  # Handle the case where value is a string (or other non-dict)
                    generalInfo[_] = value

            for key, value in question_count_details.items():
                solvedStats[key.replace("#", "")] = value

            response["info"] = generalInfo
            response["solvedStats"] = solvedStats
            return response
        else:
            return {"error" : "Profile Not Found"}
