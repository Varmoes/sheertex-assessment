import os
from flask import Flask
from flask import Response
from flask import request
from dotenv import load_dotenv
import time
import requests
import json
import logging

START_TIME = time.time()

app = Flask(__name__)

load_dotenv()

logging.basicConfig(filename='app.log', level=logging.INFO)


def get_user_followers(user):

    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

    url = "https://api.github.com/users/" + user + \
        "/followers?simple=yes&per_page=100&page=1"
    response = requests.get(url, auth=(
        GITHUB_USERNAME, GITHUB_TOKEN))
    followers = response.json()

    if isinstance(followers, dict) and followers.get('message') == 'Not Found':
        logging.error("User not found")
        return []

    while 'next' in response.links.keys():
        logging.info("Getting followers for user: " + user +
                     ", page: " + str(response.links['next']['url']))
        response = requests.get(response.links['next']['url'], auth=(
            GITHUB_USERNAME, GITHUB_TOKEN))
        followers.extend(response.json())

    logging.info("Found " + str(len(followers)) + " followers for " + user)
    return followers


def get_common_followers(user1Followers, user2Followers):
    commonFollowers = []
    for user1Follower in user1Followers:
        if user1Follower in user2Followers:
            commonFollowers.append(user1Follower)
    return commonFollowers


@app.route("/common_followers", methods=["GET"])
def common_followers():

    username1 = request.args.get('username1')
    username2 = request.args.get('username2')

    if username1 == username2:
        response = json.dumps({'error': "Usernames cannot be the same"})
        return Response(response, status=400, mimetype='text/plain')

    if username1 == "":
        response = json.dumps({'error': "Username 1 cannot be blank"})
        return Response(response, status=400, mimetype='text/plain')

    if username2 == "":
        response = json.dumps({'error': "Username 2 cannot be blank"})
        return Response(response, status=400, mimetype='text/plain')

    first_user_followers = get_user_followers(username1)
    second_user_followers = get_user_followers(username2)

    common_followers = get_common_followers(
        first_user_followers, second_user_followers)

    logging.info("Found " + str(len(common_followers)) +
                 " common followers for " + username1 + " and " + username2)

    response = json.dumps({'common_followers': common_followers})

    return Response(response, status=200, mimetype='application/json')


@app.route('/health', methods=['GET'])
def health():
    uptime = time.time() - START_TIME
    response = json.dumps({'uptime': uptime})
    return Response(response, status=200, mimetype='application/json')
