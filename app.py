from flask import Flask, render_template, request, redirect

app = Flask(__name__)

dog_links = [
    {
        "title": "30 Fun and Fascinating Dog Facts",
        "url": "https://www.akc.org/expert-advice/lifestyle/dog-facts/",
        "score": 10,
    },
    {
        "title": "Why Do Dogs Tilt Their Heads?",
        "url": "https://www.sciencefocus.com/nature/why-do-dogs-tilt-their-head-when-you-speak-to-them",
        "score": 5,
    },
    {
        "title": "r/dogs — top posts",
        "url": "https://www.reddit.com/r/dogs/",
        "score": 3,
    },
    {
        "title": "Basic Dog Training Guide",
        "url": "https://www.animalhumanesociety.org/resource/how-get-most-out-training-your-dog",
        "score": 2,
    },
    {
        "title": "The Dogist (photo stories)",
        "url": "https://thedogist.com/",
        "score": 1,
    },
]


@app.get("/")
def homepage():
    return render_template("index.html", links=dog_links)

@app.post("/vote/<link_title>")
def vote(link_title):
    vote = request.form.get("vote")
    for i, title in enumerate(dog_links):
        if title["title"] == link_title:
            if vote == "up":
                dog_links[i]["score"] += 1
            elif vote == "down":
                dog_links[i]["score"] -= 1
            break
    dog_links.sort(key=lambda x: x["score"], reverse=True)
    return redirect("/")
