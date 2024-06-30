from flask import Flask, jsonify
import requests
from telegram_bot import send_message_to_all

app = Flask(__name__)

def fetch_leetcode_problem_of_the_day():
    url = 'https://leetcode.com/graphql'
    headers = {
        'Content-Type': 'application/json',
    }
    query = '''
    {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
                title
                titleSlug
                difficulty
                questionFrontendId
            }
        }
    }
    '''
    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'activeDailyCodingChallengeQuestion' in data['data']:
            question_data = data['data']['activeDailyCodingChallengeQuestion']
            question = question_data['question']
            url = question_data['link']
            url = url[:len(url)-1]

            result = {"date": question_data['date'], "title":question['title'], "difficulty": question['difficulty'], "url":"https://leetcode.com"+url}
            return jsonify(result)
            
        
        else:
            print("Could not fetch the problem of the day.")
    
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

@app.route("/fetch")
def home():
    send_message_to_all()
    return "API Version 1.0"

@app.route("/api/v1/")
def leetcode_bot():
    result = fetch_leetcode_problem_of_the_day()
    if(result):
        return result
    return("hello")

if __name__ == "main":
    app.run("0.0.0.0", debug=True)
