from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import random

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['tale_teller']
stories_collection = db['stories']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create-story', methods=['GET', 'POST'])
def create_story():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form.get('author', 'Anonymous')  # Optional author field
        content = request.form['content']
        stories_collection.insert_one({"title": title, "author": author, "content": content})
        return redirect('/stories')
    return render_template('create_story.html')

@app.route('/auto-generate-story', methods=['GET', 'POST'])
def auto_generate_story():
    if request.method == 'POST':
        titles = ["A Journey Through Time", "The Lost Treasure", "Mystery of the Old Manor"]
        contents = [
            "Once upon a time, in a land far away, there lived a brave adventurer...",
            "In the depths of the ocean, a treasure awaited its seeker...",
            "An eerie silence filled the air as the detective entered the old manor..."
        ]
        title = random.choice(titles)
        content = random.choice(contents)
        stories_collection.insert_one({"title": title, "author": "AI", "content": content})
        return render_template('auto_generate_story.html', story={"title": title, "content": content})
    return render_template('auto_generate_story.html')

@app.route('/stories')
def get_stories():
    stories = list(stories_collection.find({}))
    for story in stories:
        story['_id'] = str(story['_id'])  # Convert ObjectId to string
    return render_template('stories.html', stories=stories)

if __name__ == '__main__':
    app.run(debug=True)
