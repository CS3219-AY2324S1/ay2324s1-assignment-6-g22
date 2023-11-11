[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)

# Testing (Local)

- The serverless function is written in Python and takes in http request calls.
- The serverless function aims to populate PeerPrep's question bank with a large number of questions from Leetcode.
- The serverless function fetches questions from Leetcode in order of their question list. This means that everytime the function is run, it will start inserting from the same first question in Leetcode's list (assuming the list has no changes).
- For testing purposes, it is recommended to fetch only a small number of questions from Leetcode. But due to the previous point, as PeerPrep will not accept duplicate questions, you will have to increase the number of fetched questions or delete previously inserted questions for repeated testing.
- The PeerPrep question database you will be interacting with is hosted in the cloud. Please avoid deleting the first 9 questions and only delete questions you have inserted.

### Setup

- To setup dependencies, please run

```
pip install -r requirements.txt
```

- To setup PeerPrep for the serverless function to insert LeetCode questions into, please visit our [PeerPrep repo](https://github.com/CS3219-AY2324S1/ay2324s1-course-assessment-g22)

### Run

- To start the serverless function, please run

```
functions-framework --target fetchLeetCodeToDB --debug
```

- Start PeerPrep (follow instructions from the PeerPrep repo)

### Use

- Send a http request call to the serverless function at localhost:8080 using curl or your browser

```
http://localhost:8080/?num=2
```

- Indicate the number of questions to fetch using num=#
- The final number of questions inserted may not be the same as num due to several reasons
- 1. Premium Questions
- 2. Question is already in PeerPrep
