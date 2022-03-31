# Coding Assessment Sheertex

## Requirements

1. Docker
2. A Github Account

## Test Cases

1. http://localhost:8080/common_followers?username1=657dfee0-116d-44b2-aec7-7e7f454ddaca&username2=benoitdelorme (non-existant user with existing user)
2. http://localhost:8080/common_followers?username1=fabpot&username2=benoitdelorme (user with a large number of followers with a user with a small amount of followers)
3. http://localhost:8080/common_followers?username1=asher-dev&username2=mildlywilde (provided example)
4. http://localhost:8080/common_followers?username1=wolever&username2=shazow (provided example)

## Instructions

To start the web server that finds common followers between two GitHub user, please make sure to add your GitHub username to the .env file for the variable **GITHUB_USER**. You'll also need to generate a Personal Access Token with Read-Access and put it in the same .env file for the variable **GITHUB_TOKEN**.

When you've completed this step, simply open a new terminal window and write the following command in the same directory of this project:

```
bash build_and_start.sh
```

This will build the Docker image and start a fresh container. After the script stops, your container should be ready to be used!

To validate the web server is up and running, head to [http://localhost:8080/health](http://localhost:8080/health) to verify the uptime. You should receive a JSON response with a float value representing the number of seconds the server has been up.
