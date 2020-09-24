## happy path
* greet
  - utter_greet

## to register a complaint without accused
* registration
  - utter_say_need
  - form_aadhar
  - form{"aadhar":"form_aadhar"}
  - form{"aadhar":null}
  - utter_registration
  - registration_form
  - form{"name":"registration_form"}
  - form{"name":null}
  - utter_say_name
  - utter_say_cat
  - utter_say_ps
  - utter_goodbye
  - utter_again
  - action_restart
* cancel
  - action_deactivate_form






## asking station details with district
* ask_police_station
  - utter_i_can_help
  - form_finding_ps
  - utter_saying_ido
  - utter_goodbye
  - utter_again
  - action_restart
* cancel
  - action_deactivate_form

 

## say goodbye
* goodbye
  - utter_goodbye
  - action_restart
