# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests


#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        slots = tracker.get_slot('item')
        item_name = None
        print(entities)
        print("***********entities***************")
        print()
        print("**************slots************")
        print(slots)
        print("**************************")
        if tracker.get_slot('user_name') is not None:
            print("user name is " + tracker.get_slot('user_name'))

        if tracker.get_slot('item') is not None:
            item_name = tracker.get_slot('item')
        item_price = 100000
        query_params = {'user_id': 'test_user_id_1', 'user_name': 'test_user_name_1'}
        response = requests.get('http://localhost:8080/chatMessage/testEndPoint', query_params)
        print("res**************************")
        print(response.json())
        print("res**************************")

        for e in entities:
            if e['entity'] == "item" and e['value'] == 'hard':
                item_name = 'there is no hard disk'

        dispatcher.utter_message(text=item_name)

        return [SlotSet("price", item_price)]


class ActionSaveUserData(Action):

    def name(self) -> Text:
        return "action_save_user_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('user_id') is not None and tracker.get_slot('user_name') is not None:
            item_name = 'action-> user id is ' + tracker.get_slot('user_id') + " and user name is " + tracker.get_slot(
                'user_name')
        SlotSet("user_name", tracker.get_slot('user_name'))

        ############################ get request test
        # query_params = {'user_id': tracker.get_slot('user_id'), 'user_name': tracker.get_slot('user_name')}
        # response = requests.get('http://localhost:8080/chatMessage/testEndPoint', query_params)
        # print(response.json())
        # res = response.json()
        # print(res['address'])
        # print(res['address']['country'])
        # print(res['name'])
        # print(res['id'])

        ###################### post request test
        # obj = {
        #     'name': 'danuka',
        #     'id': '50',
        #     'address': {'no': 160, 'country': 'Sri Lanka', 'city': 'Colombo'}
        # }
        # response = requests.post('http://localhost:8080/chatMessage/testPostEndPoint',
        #                          json=obj)
        # print(response.json())

        dispatcher.utter_message(text="successfully saved")

        return []
