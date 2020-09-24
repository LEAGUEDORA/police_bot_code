# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
import numpy as np
import pandas as pd
from rasa_sdk.events import FollowupAction
import json
import requests
import random
from main import UpdateDataBase







class sendSMS():
    def sms(self, number, otp):
        message = 'Your generated OTP is: ' + str(otp)
        url = 'https://www.fast2sms.com/dev/bulk'
        my_data = {
            'sender_id' : 'FSTSMS',
            'message' : message,
            'language' : 'english',
            'route' : 'p',
            'numbers' : number,

        }

        headers = {
            'authorization' : '8Cxo0gHnmhkGe3fqA6UcVKMJLDrzIt59Zvlj1iFBWa7Np4yduSpLRzHXKO6GhPNSfCIq5YZkVjlTJsno',
            'Content - Type' : "application/x-www-form-urlencoded",
            'Cache - Control' : 'no-cache',
        }

        response = requests.request("POST", url, data = my_data, headers = headers)

        returned_msg = json.loads(response.text)
        print(returned_msg['message'])



data = pd.read_csv('DataBase ready - DataBase.csv')
class psDataBase():

    otplist = []
    @staticmethod
    def otps(self, otp):
        psDataBase.otplist.append(otp)

    @staticmethod
    def check_in_ps(ps_name):
        ps_name = ps_name.lower().replace(" ","")
        print(ps_name)
        ans = -1
        for index, value in enumerate(data['Train'], 0):
            if (data['Train'].iloc[index] == ps_name):
                ans = index
        return ans
    
    def dual_dist(self, ps_name) :
        duals = {'atmakur': ['Anantapur', 'Kurnool', 'Nellore'],
        'devarapalli': ['West Godavari', 'Chittoor']}

        return [len(duals[ps_name]), duals[ps_name]]
        

    def get_list(self, dist_name):
        lst = []
        for index, value in enumerate(data['District'], 0):
            if data['District'].iloc[index] == dist_name:
                lst.append(index)
        return lst

    def get_details(self, ps_row):
        row = [data['Police Station Name'].iloc[ps_row], data['District'].iloc[ps_row], data['Address'].iloc[ps_row], data['Phone'].iloc[ps_row], data['Email'].iloc[ps_row], data['Pincode'].iloc[ps_row]]
        return row
    

            
class AadharData(FormAction):
    def name(self) -> Text:
        return "form_aadhar"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("required_slots(tracker: Tracker)")
        return ['aadhar', 'number', 'otp']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""

        return {
            "aadhar": [self.from_entity(entity = "aadhar", intent = "aadhar_entry"), self.from_text()],
            "number" : [self.from_entity(entity = "number",  not_intent= "aadhar_entry"), self.from_text()], 
            "otp" : [self.from_entity(entity = "otp"), self.from_text()],
        }


    
    def validate_aadhar(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        value = str(value).replace(" ", "").lower()
        if len(str(value)) == 12:
            return {"aadhar":value}
        else:
            dispatcher.utter_message(text = 'Please enter a correct 12 digit Aadhar Number')
            return {"aadhar":None}
    

    def finalOtp(self, otp):
        otpFinal = otp
        return otpFinal

    def validate_number(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        generated_otp = ""
        if str(value).startswith('+91'):
            (value) = value[3:]
        if len(str(value)) == 10:
            generated_otp_temp = self.aaotp()
            generated_otp = generated_otp_temp
            #sendSMS.sms(self,value, generated_otp)
            print("Number = ", value, "Otp = ", generated_otp)
            self.finalOtp(generated_otp)
            return {"number":value}
        else:
            dispatcher.utter_message(text= "Please check your mobile number again")
            return {"number":None}

    
    def aaotp(self):
        temp = ""
        accept = False
        while accept is False:
            o1 = str(random.randint(0,9))
            o2 = str(random.randint(0,9))
            o3 = str(random.randint(0,9))
            o4 = str(random.randint(0,9))
            o5 = str(random.randint(0,9))
            o6 = str(random.randint(0,9))
            tempotp = o1+o2+o3+o4+o5+o6
            if tempotp in psDataBase.otplist:
                accept = False
            else:
                accept = True
                psDataBase.otps(self, tempotp)
            print(tempotp)
            # sendSMS.sms(self, tracker.get_slot("number"), value)
            return tempotp

    def send(self, number, otp, tracker: Tracker):
        sendSMS.sms(self, number, otp)
    

    
    def validate_otp(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        
        
        if len(str(value)) < 6: 
            #print(otp)
            dispatcher.utter_message(text= "Please give me a valid 6 digit otp sent to your mobile number")
            return {"otp": None}
        else:
            #ans = tracker.latest_message['text']
            print("ans : ",psDataBase.otplist[-1],  "value : ", value)
            if psDataBase.otplist[-1] == (value):
                return {"otp":value}
            else:
                dispatcher.utter_message(text= "Sorry you have enterd the wrong otp. Try again")
                return {"otp":None}


    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        return []





class action_finding_ps(FormAction):
    def name(self) -> Text:
        return "form_finding_ps"

    @staticmethod
    def dist_names(self, name):
        dist_names = ['Srikakulam', 'Vishakapatnam', 'Vizayanagaram', 'West Godavari', 'East Godavari', 'Krishna', 'Guntur', 'Prakasam', 'Nellore', 'Anantapur', 'Kadapa', 'Kurnool', 'Chittor']
        if name in dist_names:
            return True
        else:
            return False

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("required_slots(tracker: Tracker)")
        return ['dist']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""

        return {
            "dist": [self.from_entity(entity = "dist", intent = "dist_entry")],
        }
    
    def validate_dist(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if self.dist_names(self, value.title()) is True:
            dispatcher.utter_message(text=  "Yes! I found the details")
            dispatcher.utter_message(text = "Name and Address of police stations in {} district are".format(value))
            ans = psDataBase.get_list(self, value)
            for i in ans:
                dispatcher.utter_message(text = "Name {}\n Address {}\n".format(data['Police Station Name'].iloc[i],data['Address'].iloc[i]))
            return {"dist":value}
        else:
            dispatcher.utter_message(text = "Sorry check your district name")
            return {"dist":None}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        return []






class ActionRegistration(FormAction):
    district = ["None"]
    def name(self) -> Text: 
        return "registration_form"

    @staticmethod
    def required_slots(tracker: Tracker)  -> List[Text]:
        print("required_slots(tracker: Tracker)")
        return ["name", "ps","category" ,"details" ,"confirm"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""

        return {
            "ps": [self.from_entity(entity="ps",  not_intent = "ps_entry"), self.from_text()],
            "name": [self.from_entity(entity = "name", not_intent = "ps_entry"), self.from_text()],
            "confirm" :  [self.from_entity(entity = "confirm"), self.from_text()],
            "details" : [self.from_entity(entity= "details"), self.from_text()],
            "category" : [self.from_entity(entity="category", intent= "category_entry")],
            
        }


    
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:


        temp = UpdateDataBase.UpdateDataBase(self, tracker.get_slot("aadhar"), tracker.get_slot("number"), tracker.get_slot("ps"), ActionRegistration.district[0] , tracker.get_slot("name"), tracker.get_slot("category"), tracker.get_slot("details"), tracker.get_slot("confirm"))

        #dispatcher.utter_message(text="We have submitted your data")

        return []

    @staticmethod
    def dist_names(self, name):
        dist_names = ['Srikakulam', 'Vishakapatnam', 'Vizayanagaram', 'West Godavari', 'East Godavari', 'Krishna', 'Guntur', 'Prakasam', 'Nellore', 'Anantapur', 'Kadapa', 'Kurnool', 'chittor']
        if name in dist_names:
            return True
        else:
            return False


    def validate_confirm(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        value = value.lower()
        if value == "yes" or value == "ok" or value == "sure":
            dispatcher.utter_message(text= "Your complaint is filed")
            dispatcher.utter_message(text="We have submitted your data")
            return {"confirm":"Yes"}

        else:
            dispatcher.utter_message(text= "You had withdrawn your complaint. But your details are stored within our data base. 'No' further action will be taken")
            return {"confirm":"No"}



    def validate_details(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if len(str(value)) > 0:
            return {"details":value}
        else:
            dispatcher.utter_message(text= "Details cannot be empty")
            return {"details":None}


    def validate_name(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:  
        name = ""
        print(value)
        for i in value:
            name += i.lower()
        if name.startswith("he is") or name.startswith("she is"):

            ans = name[5:]
            return {"name":ans}
        elif name.startswith("his name is") or name.startswith("her name is"):
            ans = name[11:]
            return {"name":ans.title()}
        else:
            return {"name":name}

    def validate_ps(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        value = value.replace(" ", "").lower()
        print(value)
        if value.endswith('policestation'):
            value = value[0:13]
        elif value.endswith('station'):
            value = value[0:7]
        if value.startswith('at ') or value.startswith('in '):
            value = value[3:]

        doubles = ['atmakur', 'devarapalli']
        towns = ['ANANTAPURAM', 'DHARMAVRAM', 'AMALAPURAM', 'ELURU', 'BHIMAVARAM', 'ANAKAPALLI', 'ICHAPURAM', 'RAJAHMUNDRY', 'KANDUKUR', 'CHIRALA', 'GUDUR', 'DHONE', 'ALLAGADDA', 'ADONI', 'KAIKALURU', 'GUDIVADA', 'MANGALAGIRI', 'CHILAKALURIPET', 'CHITTOOR', 'BAPATLA', 'VIJAYAWADA', 'KAKINADA', 'VISAKHAPATNAM']
        if value.upper() in towns:
            dispatcher.utter_message(text = "There are several Police Stations in the given area.\nTry to specify town number/urban or rural etc.,\nExample:Bhimavaram 1 Town or Bhimavaram Rural")
            return {"ps":None}


        if value in doubles:
            if value == 'atmakur':
                num = 7
            else:
                num = 11
            number, lst = psDataBase.dual_dist(self, value[0:num])
            dispatcher.utter_message(text= "This name police station matches with police stations in {} districts.".format(number))
            dispatcher.utter_message(text = "They are in")
            for i in lst:
                dispatcher.utter_message(text = "{}".format(i))
            dispatcher.utter_message(text= 'So please "re-enter" the police station name combined with district.\nExample: atmakur Anantapur')
            return {"ps":None}
        check = psDataBase.check_in_ps(value.replace(" ","").lower())
        


        if check != -1 :
            answer= psDataBase.get_details(self, check)
            dispatcher.utter_message(text = "Police station found. Fetching their details. please wait\nSo you selected for {}\nAddress is {}\nIt is in {} District\nYou can contact them via phone - {}\nVia Email {}".format(answer[0], answer[1], answer[2], answer[3], answer[4]))   
            ActionRegistration.district[0] = answer[2]
            return {"ps":answer[0]}
            
        else:
            dispatcher.utter_message(text= "Please check the police staion details by asking me :)")
            return {"ps":None}

###end here