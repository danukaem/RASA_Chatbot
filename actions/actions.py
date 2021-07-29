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
        item_name = None
        print(entities)
        print("***********entities***************")
        print(tracker.slots)
        print("**************slots************")
        if tracker.get_slot('user_name') is not None:
            print("user name is " + tracker.get_slot('user_name'))

        # if tracker.get_slot('item') is not None:
        #     item_name = tracker.get_slot('item')
        # query_params = {'user_id': 'test_user_id_1', 'user_name': 'test_user_name_1'}
        # response = requests.get('http://localhost:8080/chatMessage/testEndPoint', query_params)
        # print("res**************************")
        # print(response.json())
        # print("res**************************")
        item = ''
        ram = ''
        screen = ''
        price = ''
        brand = ''
        color = ''
        storage = ''
        user_id = ''
        item_extract_id = ''
        session_id = ''
        # if tracker.get_slot('item') is not None:
        #     item = tracker.get_slot('item')
        # if tracker.get_slot('ram') is not None:
        #     ram = tracker.get_slot('ram')
        # if tracker.get_slot('screen') is not None:
        #     screen = tracker.get_slot('screen')
        # if tracker.get_slot('price') is not None:
        #     price = tracker.get_slot('price')
        # if tracker.get_slot('brand') is not None:
        #     brand = tracker.get_slot('brand')
        # if tracker.get_slot('color') is not None:
        #     color = tracker.get_slot('color')
        # if tracker.get_slot('storage') is not None:
        #     storage = tracker.get_slot('storage')
        if tracker.get_slot('user_id') is not None:
            user_id = tracker.get_slot('user_id')
        if tracker.get_slot('item_extract_id') is not None:
            item_extract_id = tracker.get_slot('item_extract_id')
        if tracker.get_slot('session_id') is not None:
            session_id = tracker.get_slot('session_id')

        for entity in entities:
            if entity['entity'] == 'item':
                item = entity['value']
            if entity['entity'] == 'ram':
                ram = entity['value']
            if entity['entity'] == 'screen':
                screen = entity['value']
            if entity['entity'] == 'price':
                price = entity['value']
            if entity['entity'] == 'brand':
                brand = entity['value']
            if entity['entity'] == 'color':
                color = entity['value']
            if entity['entity'] == 'storage':
                storage = entity['value']

        query_params = {'item': item, 'ram': ram,
                        'screen': screen, 'price': price,
                        'brand': brand, 'color': color,
                        'storage': storage, 'user_id': user_id,
                        'item_extract_id': item_extract_id, 'session_id': session_id}
        response = requests.get('http://localhost:8080/chatMessage/itemExtractRasaDataSave', query_params)
        print(response.text)


        for e in entities:
            if e['entity'] == "item" and e['value'] == 'hard':
                item_name = 'there is no hard disk'

        dispatcher.utter_message(text="any other requirement ?")

        return [SlotSet("item_extract_id", response.text)]
        # return [SlotSet("price",75000)]


class ActionSaveUserData(Action):

    def name(self) -> Text:
        return "action_save_user_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('user_id') is not None and tracker.get_slot('user_name') is not None and tracker.get_slot(
                'session_id') is not None:
            item_name = 'action-> user id is ' + tracker.get_slot('user_id') + " and user name is " + tracker.get_slot(
                'user_name') + ' and session is ' + tracker.get_slot('session_id')

        # print('user name '+tracker.get_slot('user_name'))
        # print('user id '+tracker.get_slot('user_id'))
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

        user_name = ''
        session_id = ''
        if tracker.get_slot('user_id') is not None:
            query_params = {'userId': tracker.get_slot('user_id')}
            response = requests.get('http://localhost:8080/user/getUserNameByUserId', query_params)
            user_name = response.json()['user_name']
            session_id = response.json()['session_id']
            print("88888888888888888888")
            print(response.json())
            print(response.json()['user_name'])
            print(response.json()['session_id'])
            print("88888888888888888888")
        if tracker.get_slot('user_name') is not None:
            user_name = tracker.get_slot('user_name')

        dispatcher.utter_message(text="successfully saved ")

        return [SlotSet("user_name", user_name), SlotSet("session_id", session_id)]