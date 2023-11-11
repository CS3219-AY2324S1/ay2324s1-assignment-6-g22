import functions_framework
import requests
import json
import html2text

LEETCODE_API_URL = "https://leetcode.com/graphql"
USER_SERVICE_URL = "http://localhost:3000/api/login"
QUESTION_SERVICE_URL = "http://localhost:3000/api/questions"

html2text.hn = lambda _:0
h = html2text.HTML2Text()
h.images_to_alt = True
h.single_line_break = True
h.ignore_emphasis = True
h.ignore_links = True
h.ignore_tables = True

def fetchToken():
    header = {
       'Content-Type': 'application/json'
    }
    data = {
       'username': 'maintainer',
       'password': 'test!Test1',
    }
    response = requests.post(USER_SERVICE_URL, headers=header, data=json.dumps(data))
    return response.json()['token']

def putIntoDB(question, token):
    header = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    response = requests.post(QUESTION_SERVICE_URL, headers=header, data=json.dumps(question))
    return response

def formatDescription(description):
   return h.handle((description))

def fetchLeetCodeQnsDesc(titleSlug):
    response = requests.get(LEETCODE_API_URL, json={"query": "\n    query questionContent($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    content\n    mysqlSchemas\n    dataSchemas\n  }\n}\n    ", "variables": {"titleSlug": titleSlug}, "operationName": "questionContent"}).json()
    return response["data"]["question"]["content"]

def fetchLeetCode(num):
    response = requests.get(LEETCODE_API_URL, json={"query": "query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}", "variables": {"categorySlug": "", "skip": 0, "limit": num, "filters": {}}})
    unformattedQuestions = response.json()["data"]["problemsetQuestionList"]["questions"]
    formattedQuestions = []
    for unformattedQuestion in unformattedQuestions:
        if unformattedQuestion["paidOnly"]:
            continue
        formattedQuestion = {}
        formattedQuestion["title"] = unformattedQuestion["title"]
        formattedQuestion["category"] = ','.join([tag["name"] for tag in unformattedQuestion["topicTags"]])
        formattedQuestion["complexity"] = unformattedQuestion["difficulty"]
        formattedQuestion["description"] = formatDescription(fetchLeetCodeQnsDesc(unformattedQuestion["titleSlug"]))
        formattedQuestion["tags"] = []
        formattedQuestions.append(formattedQuestion)
    return formattedQuestions

def updateQuestionsDB(num):
    questions = fetchLeetCode(num)
    token = fetchToken()

    count = 0
    for question in questions:
        response = putIntoDB(question, token)
        if response.status_code == 200:
            count += 1
        else:
            print("Error: ", response.json())

    return count

# functions-framework --target fetchLeetCodeToDB --debug
# curl http://localhost:8080
# http://localhost:8080/?num=2

# Register an HTTP function with the Functions Framework
@functions_framework.http
def fetchLeetCodeToDB(request):
  request_json = request.get_json(silent=True)
  request_args = request.args

  if request_json and "num" in request_json:
    num = int(request_json["num"])
  elif request_args and "num" in request_args:
    num = int(request_args["num"])
  else:
    num = 10

  if num > 0:  
    finalNum = updateQuestionsDB(num)
  else:
    finalNum = 0   

  # Return an HTTP response
  headers = {"Access-Control-Allow-Origin": "*"}
  return ("Fetched " + str(finalNum) + " questions from LeetCode", 200, headers)