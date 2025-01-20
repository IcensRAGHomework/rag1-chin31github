import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

import re
from langchain_core.output_parsers import JsonOutputParser
import sys

import requests
#5from googletrans import Translator

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def generate_hw01(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    match = re.search(r'(\d{4})年台灣(\d{1,2})月', question)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2) 
        #print(year)
        #print(month)
        prompt = f"列出{year}年台灣{month}月的所有紀念日，並以JSON格式呈現，每個紀念日包含日期和名稱，例如：{{'date': '年份-月份-日期', 'name': '紀念日名稱'}}。"
        response = llm.invoke(prompt)
 
        json_parser = JsonOutputParser()
        json_output = json_parser.invoke(response)
        result = {"Result": json_output}
    else:
        result = {"Result": []}
 
 
    print(result)
    return json.dumps(result, ensure_ascii=False, indent=2)
    pass
    
#import asyncio
#from googletrans import Translator
#
#async def translate_text(question):
#    async with Translator() as translator:
#        result = await translator.translate(question, dest='zh-tw')
#        #print(result)
#        return result.text
        
def get_holidays(api_key, country, year, month, target_language="zh-CN"):
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key":api_key,
        "country":country,
        "year":year,
        "month":month
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        #1return response
        #2return response.json()
        #3holidays_data = response.json().get('response', {}).get('holidays', [])
        #3return holidays_data
        #4holidays_data = response.json().get('response', {}).get('holidays', [])
        #4holidays = [{"date": holiday["date"]["iso"], "name": holiday["name"]} for holiday in holidays_data]
        #4return {"Result": holidays}
        holidays_data = response.json().get('response', {}).get('holidays', [])
        #translator = Translator()
        holidays = []
        for holiday in holidays_data:
            #translated_name = asyncio.run(translate_text(holiday["name"]))
            holidays.append({"date": holiday["date"]["iso"], "name": holiday["name"]})
        return {"Result": holidays}
    else:
        return {"error": "Failed to fetch holidays"}
    pass
        
def generate_hw02(question):
    api_key = "1jj5V9ATLm23h5HbHBeaCY4O2adaieCX"
    country = "TW"
    match = re.search(r'(\d{4})年台灣(\d{1,2})月', question)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2) 
        holidays = get_holidays(api_key, country, year, month)
        print(holidays)
        return json.dumps(holidays, ensure_ascii=False, indent=2)
    else:
        result = {"Result": []}
#1response --> <Response [200]>
#2response.json() --> {'meta': {'code': 200}, 'response': {'holidays': [{'name': 'National Day', 'description': 'National Day is a national holiday in Taiwan', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-10', 'datetime': {'year': 2024, 'month': 10, 'day': 10}}, 'type': ['National holiday'], 'primary_type': 'National holiday', 'canonical_url': 'https://calendarific.com/holiday/taiwan/national-day', 'urlid': 'taiwan/national-day', 'locations': 'All', 'states': 'All'}, {'name': 'Double Ninth Day', 'description': 'Double Ninth Day is a observance in Taiwan', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-11', 'datetime': {'year': 2024, 'month': 10, 'day': 11}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/double-ninth-day', 'urlid': 'taiwan/double-ninth-day', 'locations': 'All', 'states': 'All'}, {'name': 'Overseas Chinese Day', 'description': 'Overseas Chinese Day is a observance in Taiwan', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-21', 'datetime': {'year': 2024, 'month': 10, 'day': 21}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/overseas-chinese-day', 'urlid': 'taiwan/overseas-chinese-day', 'locations': 'All', 'states': 'All'}, {'name': "Taiwan's Retrocession Day", 'description': "Taiwan's Retrocession Day is a observance in Taiwan", 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-25', 'datetime': {'year': 2024, 'month': 10, 'day': 25}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/taiwan-retrocession-day', 'urlid': 'taiwan/taiwan-retrocession-day', 'locations': 'All', 'states': 'All'}, {'name': 'Halloween', 'description': 'Halloween is a festive occasion that is celebrated in many countries on October 31 each year.', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-31', 'datetime': {'year': 2024, 'month': 10, 'day': 31}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/halloween', 'urlid': 'taiwan/halloween', 'locations': 'All', 'states': 'All'}]}}
#3response.json().get('response', {}).get('holidays', []) --> [{'name': 'National Day', 'description': 'National Day is a national holiday in Taiwan', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-10', 'datetime': {'year': 2024, 'month': 10, 'day': 10}}, 'type': ['National holiday'], 'primary_type': 'National holiday', 'canonical_url': 'https://calendarific.com/holiday/taiwan/national-day', 'urlid': 'taiwan/national-day', 'locations': 'All', 'states': 'All'}, {'name': 'Double Ninth Day', 'description': 'Double Ninth Day is a observance in Taiwan', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-11', 'datetime': {'year': 2024, 'month': 10, 'day': 11}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/double-ninth-day', 'urlid': 'taiwan/double-ninth-day', 'locations': 'All', 'states': 'All'}, {'name': 'Overseas Chinese Day', 'description': 'Overseas Chinese Day is a observance in Taiwan', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-21', 'datetime': {'year': 2024, 'month': 10, 'day': 21}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/overseas-chinese-day', 'urlid': 'taiwan/overseas-chinese-day', 'locations': 'All', 'states': 'All'}, {'name': "Taiwan's Retrocession Day", 'description': "Taiwan's Retrocession Day is a observance in Taiwan", 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-25', 'datetime': {'year': 2024, 'month': 10, 'day': 25}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/taiwan-retrocession-day', 'urlid': 'taiwan/taiwan-retrocession-day', 'locations': 'All', 'states': 'All'}, {'name': 'Halloween', 'description': 'Halloween is a festive occasion that is celebrated in many countries on October 31 each year.', 'country': {'id': 'tw', 'name': 'Taiwan'}, 'date': {'iso': '2024-10-31', 'datetime': {'year': 2024, 'month': 10, 'day': 31}}, 'type': ['Observance'], 'primary_type': 'Observance', 'canonical_url': 'https://calendarific.com/holiday/taiwan/halloween', 'urlid': 'taiwan/halloween', 'locations': 'All', 'states': 'All'}]
#4{"Result": holidays} --> {'Result': [{'date': '2024-10-10', 'name': 'National Day'}, {'date': '2024-10-11', 'name': 'Double Ninth Day'}, {'date': '2024-10-21', 'name': 'Overseas Chinese Day'}, {'date': '2024-10-25', 'name': "Taiwan's Retrocession Day"}, {'date': '2024-10-31', 'name': 'Halloween'}]}
    pass
    
def generate_hw03(question2, question3):
    pass
    
def generate_hw04(question):
    pass
    
def demo(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    message = HumanMessage(
            content=[
                {"type": "text", "text": question},
            ]
    )
    response = llm.invoke([message])
    
    return response
    pass

#2024年台灣10月紀念日有哪些?
#generate_hw01(sys.argv[1])
#generate_hw02(sys.argv[1])
