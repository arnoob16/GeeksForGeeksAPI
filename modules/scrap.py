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
        
        def get_inner_text_list(element_list):
            result = []
            for element in element_list:
                try:
                    text = element.text
                    result.append(text.replace(" ", "_").lower())
                except:
                    result.append("")
            return result


        def extract_details(soup):
            # basic_details_by_index = ["institution", "languagesUsed"]
            # coding_scores_by_index = ["codingScore", "totalProblemsSolved", "monthlyCodingScore", "articlesPublished"]
            
            ## Get the elemets with details and score names
            basic_details_names = soup.find_all("div", class_ = "basic_details_name")
            score_card_names = soup.find_all("span", class_ = "score_card_name")

            ## Get the inner text list of the elements
            basic_details_by_index = get_inner_text_list(basic_details_names)
            coding_scores_by_index = get_inner_text_list(score_card_names)

            ## Get the elements with details and score values
            basic_details = soup.find_all("div", class_ = "basic_details_data")
            coding_scores = soup.find_all("span", class_ = "score_card_value")
            
            response = {}
            response["basic_details"] = extract_text_from_elements(basic_details, basic_details_by_index)
            response["coding_scores"] = extract_text_from_elements(coding_scores, coding_scores_by_index)
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
                for _key, _value in value.items():
                    generalInfo[_key] = _value

            for key, value in question_count_details.items():
                solvedStats[key.replace("#", "")] = value

            response["info"] = generalInfo
            response["solvedStats"] = solvedStats
            return response
        else:
            return {"error" : "Profile Not Found"}
