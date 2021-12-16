from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

import requests


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hashing_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

# connect_db(app)
# db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get("/api/ping")
def ping():
    """pings api to ensure route works"""
    response = {"success": True}
    return jsonify(response)



@app.get("/api/posts")
def return_posts():
    """gets posts from api"""
    
    def sortFunc(item):
        """sort the items that we get back from API"""
        return item[sort_by]
    
    # optional arguments, return none if not included
    sort_by=request.args.get('sortBy')
    direction = request.args.get('direction')

    # we know we will have tags, and throw error if not
    tags = request.args['tags'] 


    if direction is None or direction == 'asc':
        reverse=True
    else:
        reverse=False

    
    posts=[]

    tags_list = tags.split(',')


    for tag in tags_list:
        posts_data = requests.get(f"https://api.hatchways.io/assessment/blog/posts?tag={tag}")
        posts.append(posts_data.json()['posts'])

    breakpoint()

    # sort posts as needed, set reverse to T/F depending on direction
    if sort_by is not None:
        if direction is None or direction == 'asc':
            reverse=True
        else:
            reverse=False

        posts[0].sort(reverse=reverse,key=sortFunc)


    return jsonify({'posts':posts[0]})
