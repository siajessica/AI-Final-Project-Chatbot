# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from bert import question_answer

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

from pathlib import Path

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = Path('./corpus/test_corp.txt').read_text()
        ans = question_answer("What are the symptoms for covid?", text)
        dispatcher.utter_message(text=ans)

        return []
