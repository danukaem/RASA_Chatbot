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

class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        if tracker.get_slot('user_name') is not None:
            print("user name is " + tracker.get_slot('user_name'))

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

        response_message = 'please, can you sign in again and do chat..'
        if tracker.get_slot('user_id') is not None and tracker.get_slot('session_id') is not None:
            user_requirement = UserRequirement()
            response_message = user_requirement.get_user_requirements(tracker.get_slot('user_id'),
                                                                      tracker.get_slot('session_id'))

        dispatcher.utter_message(text=response_message)

        return []
        # return [SlotSet("item_extract_id", response.text)]


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
        if tracker.get_slot('user_name') is not None:
            user_name = tracker.get_slot('user_name')

        dispatcher.utter_message(text="successfully saved ")

        return [SlotSet("user_name", user_name), SlotSet("session_id", session_id)]


class UserRequirement:

    def get_user_requirements(self, user_id, session_id):
        query_params = {'user_id': user_id, 'session_id': session_id}
        response = requests.get('http://localhost:8080/item/getChatItemRequirements', query_params)
        res_message = ''
        if response.json()['itemCategory'] == '':
            res_message = 'can\'t recognize the item . there are only phones and laptops'
        elif response.json()['ram'] == '':
            res_message = "what is your expected ram size of the {}? ".format(response.json()['itemCategory'])
        elif response.json()['screen'] == '':
            res_message = "what is your expected screen size of the {}? ".format(response.json()['itemCategory'])
        elif response.json()['price'] == '':
            res_message = "can you tell me about the budget for the {}? ".format(response.json()['itemCategory'])
        elif response.json()['brand'] == '':
            res_message = "which brand is you looking for the {} ? ".format(response.json()['itemCategory'])
        elif response.json()['color'] == '':
            res_message = "what is your expected color for the {}? ".format(response.json()['itemCategory'])
        else:
            res_message = "please look at the suggested items that are forecasted according to your requirements. did that help you ?"

        return res_message
