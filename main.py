import json
import requests
import random 



class UpdateDataBase:
    def UpdateDataBase(self, aadhar, phone, ps, district, name, category, description, confirm):
        rand = random.randint(1,4)
        dictionary = {
            "aadhar":aadhar,
            "phone":phone,
            "ps":ps,
            "district":district,
            "name":name,
            "category":category,
            "description":description,
            "confirm":confirm,
            "random":rand,

        }
        URL = 'http://a983b56561b0.ngrok.io/index'

        data = dictionary

        with open ('dictionary.json', 'w') as f:
            json.dump(dictionary, f)

        r = requests.get(url = URL, params=data)
        print(r.status_code)
        print(r.text)



#UpdateDataBase.UpdateDataBase(UpdateDataBase,"78787878787", "9963905554", "lalapet", "Guntur", "sandeep", "category", "description")
