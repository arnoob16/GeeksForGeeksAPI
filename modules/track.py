from flask import json
from .scrap import scrap
import os

class track():

    def __init__(self, user):
        self.user = user
    
    def solve(self):
        scrapper = scrap(self.user)
        data = scrapper.fetchResponse()

        if(data != {"error" : "Profile Not Found"}):
            details = []
            links = []
            for key in data['solvedStats'].keys():
                for i in range(len(data['solvedStats'][key]['questions'])):
                    link = data['solvedStats'][key]['questions'][i]['link']
                    data['solvedStats'][key]['questions'][i]['fromBabbar450Sheet'] = False
                    links.append(link)
                    details.append((key, i))

            file = os.path.join("..","ques.json")
            with open(file, 'r') as file:
                babbar = json.loads(file.read())

            for key in babbar.keys():
                blink = babbar[key]['l']
                if(blink.endswith('/')):
                    babbar[key]['l'] = blink[:len(blink)-1]

            babbar_link = [[],[]]
            for key in babbar.keys():
                blink = babbar[key]['l']
                babbar_link[0].append(blink)
                babbar_link[1].append(key)

            for i, link in enumerate(links):
                if(link in babbar_link[0]):
                    detail = details[i]
                    data['solvedStats'][detail[0]]['questions'][detail[1]]['status'] = True

            return data
        
        else:
            return data