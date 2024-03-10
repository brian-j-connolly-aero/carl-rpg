# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:53:33 2024

@author: cavsf
"""
import json
from openai import OpenAI
from typing import List
from pydantic import BaseModel, Field
from xml_parse import get_category
import tiktoken


enc = tiktoken.encoding_for_model("gpt-4")

cheevos=get_category('Achievements')

class Achievement(BaseModel):
    tone: str = Field(..., description="Select from these tones: sarcastic unimpressed, mildly impressed, begrudginly impressed, hugely impressed]")
    name: str
    description: str
    reward: str = Field(
        ..., description="If reward is not justified, describe why reward is not justified. If reward is justified, respond in this format: {You've received a bronze/silver/gold/platium/legendary/celestial {insert box type relevant to activity} box}.")


Achievement.schema()
GPT_MODEL = "gpt-4-turbo"
client = OpenAI()


messages = [{"role": "system", "content": "You are a snarky, mildly cruel AI who curses a bit. Please generate an achievement for the user based on their actions"},
            #{"role":"system","content":f"Here are example achievements: {cheevos}"},
            {"role": "user", "content": "I went back country skiing and fell over because I trusted a 'no wax' ski treatment!"}]
tools = [{"type": "function",
          "function": {
              "name": "return_achivement",
              "description": "Returns name, description, and reward of an achievement.",
              "parameters": Achievement.schema()
          }
          }
         ]
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {
        "name": "return_achivement"}},
)
test_dict=json.loads(response.choices[0].message.tool_calls[0].function.arguments)
#%%
print(f"New Achievement!: {test_dict['name']}. <break time=\".75s\" />")
print(f"{test_dict['description']}")
print(f"Reward: {test_dict['reward']}")