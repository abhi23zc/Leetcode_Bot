import requests, os
TOKEN = "6937290734:AAEw11iwOgFpD_o2nDnx6uhBJkuC1YRa-sY"
TOKEN = os.environ["TOKEN"]

api_data = None

def getData():
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
            result = f" Date: {question_data['date'] }\n Title : {question['title']} \n Difficulty: {question['difficulty']} \n  url: https://leetcode.com{url}"

            api_data =  (result)
            return api_data
        
        else:
            print("Could not fetch the problem of the day.")
    
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")



user_list = set()

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

mydata = (requests.get(url).json())["result"]
mydata = list(mydata)

for item in mydata:
    myid = (item["message"]["from"]["id"])
    user_list.add(myid)
    
def send_message_to_all():
    new_user_list = list(user_list)

    try:
        
        for item in new_user_list:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={item}&text={api_data or getData()}"
            print(requests.get(url).json()) # this sends the message
    except Exception as e:
        print(e)
    
def send_telegam_msg(message, chat_id):
    chat_id = "5709352941"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={api_data or getData()}"
    print(requests.get(url).json()) # this sends the message
    
# print(user_list)

# send_message_to_all("helo")