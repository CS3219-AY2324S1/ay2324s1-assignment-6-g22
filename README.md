[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)

# Testing (Local)

- The serverless function is written in Python and takes in http request calls.

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
