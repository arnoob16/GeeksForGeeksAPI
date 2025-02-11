import requests
import json
from bs4 import BeautifulSoup as bs

class scrap():
    def __init__(self, username):
        self.username = username
    
    def fetchResponse(self):
        BASE_URL = f'https://auth.geeksforgeeks.org/user/{self.username}/practice/'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        profilePage = requests.get(BASE_URL, headers=headers)

        if profilePage.status_code != 200:
            return {"error": "Profile Not Found"}

        soup = bs(profilePage.content, 'html.parser')

        # Find the script tag containing JSON data
        script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
        if not script_tag:
            return {"error": "Could not find user data"}

        # Parse the JSON data
        try:
            user_data = json.loads(script_tag.string)
            user_info = user_data["props"]["pageProps"]["userInfo"]
            user_submissions = user_data["props"]["pageProps"]["userSubmissionsInfo"]
        except (KeyError, json.JSONDecodeError):
            return {"error": "Failed to parse user data"}

        # Extract general information
        generalInfo = {
            "userName": self.username,
            "fullName": user_info.get("name", ""),
            "profilePicture": user_info.get("profile_image_url", ""),
            "institute": user_info.get("institute_name", ""),
            "instituteRank": user_info.get("institute_rank", ""),
            "currentStreak": user_info.get("pod_solved_longest_streak", "00"),
            "maxStreak": user_info.get("pod_solved_global_longest_streak", "00"),
            "codingScore": user_info.get("score", 0),
            "monthlyScore": user_info.get("monthly_score", 0),
            "totalProblemsSolved": user_info.get("total_problems_solved", 0),
        }

        # Extract solved questions by difficulty
        solvedStats = {}
        for difficulty, problems in user_submissions.items():
            questions = [
                {
                    "question": details["pname"],
                    "questionUrl": f"https://practice.geeksforgeeks.org/problems/{details['slug']}"
                }
                for details in problems.values()
            ]
            solvedStats[difficulty.lower()] = {"count": len(questions), "questions": questions}

        return {
            "info": generalInfo,
            "solvedStats": solvedStats
        }