<p align="center">
    <img src = "https://media.geeksforgeeks.org/wp-content/cdn-uploads/20190710102234/download3.png">
	<h1 align="center">Unofficial GFG API</h1>
	<h3 align="center">An unofficial API for GeeksForGeeks for developers to make cool stuff using GFG data.</h3>
</p>

<p align="center">
<img src="https://img.shields.io/github/issues-closed/arnoob16/GeeksForGeeksAPI?style=for-the-badge">
<img src="https://img.shields.io/github/issues-pr-closed/arnoob16/GeeksForGeeksAPI?color=green&style=for-the-badge">
</p>

---

## Functionalities
  -  [x]  Has all the relevant data from the GFG profile page.
  -  [x]  Has the count of all the problems solved based on difficulties.
  -  [x]  Has the links & names of all the problems solved by the user segregated based on difficulties.
  -  [x]  Methods supported - `GET`

---

## Endpoints

To access the API, there is only 1 endpoint, *https://geeks-for-geeks-api.vercel.app/yourGeeksForGeeksUsername*

`Sample URL` - https://geeks-for-geeks-api.vercel.app/arnoob16

## How was it built:
The API was built using Web Scraping the profile page and a server deployed on web.

<p align=center>
    <img src = "https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>
    <img src = "https://img.shields.io/badge/Flask-FF9800?style=for-the-badge&logo=flask"/>
    <img src = "https://img.shields.io/badge/Vercel-008080?style=for-the-badge&logo=vercel"/>
</p>

---

## Instructions to run on your local system

* Pre-requisites:
	- Python 3.x
    - Install all the required libraries using the *requirements.txt* file. 
    
    ``` pip install requirements.txt ```

* Directions to execute
    - ``` python server.py``` or ``` py server.py```
    - Open the browser of your choice and visit your localhost, *http://127.0.0.1:5000/yourGeeksForGeeksUsername*
    - See the API Response, understand it and build something with it.

---

### Sample API Responses
#### Success Response
```
{
    "info": {
        "name": "Arnab Deep",
        "username": "arnoob16",
        "institution": "SRM Institute of Science and Technology",
        "instituteRank": 62,
        "solved": 84,
        "codingScore": 190,
        "monthlyCodingScore": 4,
        "weeklyCodingScore": 0
    },
    "solvedStats": {
        "school": {
            "count": "0",
            "questions": []
        },
        "basic": {
            "count": "17",
            "questions": [
                {
                    "question": "Height of Binary Tree",
                    "link": "https://practice.geeksforgeeks.org/problems/height-of-binary-tree/1"
                },
                {
                    "question": "Reverse a String",
                    "link": "https://practice.geeksforgeeks.org/problems/reverse-a-string/1"
                },
                ....
            ]
        },
        "easy": {
            "count": "49",
            "questions": [
                {
                    "question": "Deque Implementations",
                    "link": "https://practice.geeksforgeeks.org/problems/deque-implementations/1"
                },
                {
                    "question": "The New Line - Java",
                    "link": "https://practice.geeksforgeeks.org/problems/the-new-line-java/1"
                },
                ....
            ]
        },
        "medium": {
            "count": "16",
            "questions": [
                {
                    "question": " Rearrange Array Alternately",
                    "link": "https://practice.geeksforgeeks.org/problems/-rearrange-array-alternately-1587115620/1"
                },
                {
                    "question": "Part of it.",
                    "link": "https://practice.geeksforgeeks.org/problems/part-of-it1016/1"
                },
                ....
            ]
        },
        "hard": {
            "count": "2",
            "questions": [
                {
                    "question": "QuickSort on Doubly Linked List",
                    "link": "https://practice.geeksforgeeks.org/problems/quicksort-on-doubly-linked-list/1"
                },
                {
                    "question": "Return two prime numbers",
                    "link": "https://practice.geeksforgeeks.org/problems/return-two-prime-numbers2509/1"
                }
            ]
        }
    }
}
``` 

#### Failure Response
```
{
    "error": "Profile Not Found"
}
```
---

#### Notes

- If you are using this, do mention about this repository in your readme, I'll also mention your project here in this repository.
- A star to the repository would be massive boost to a NOOB like me.


<p align=center>
<img src="https://forthebadge.com/images/badges/built-with-love.svg"/>
</p>
