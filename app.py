from flask import Flask, render_template, request, redirect

app = Flask(__name__)

dog_links = [
    {
        "title": "30 Fun and Fascinating Dog Facts",
        "url": "https://www.akc.org/expert-advice/lifestyle/dog-facts/",
        "score": 10,
        "hidden": False,
    },
    {
        "title": "Why Do Dogs Tilt Their Heads?",
        "url": "https://www.sciencefocus.com/nature/why-do-dogs-tilt-their-head-when-you-speak-to-them",
        "score": 5,
        "hidden": False,
    },
    {
        "title": "r/dogs — top posts",
        "url": "https://www.reddit.com/r/dogs/",
        "score": 3,
        "hidden": False,
    },
    {
        "title": "Basic Dog Training Guide",
        "url": "https://www.animalhumanesociety.org/resource/how-get-most-out-training-your-dog",
        "score": 2,
        "hidden": False,
    },
    {
        "title": "The Dogist (photo stories)",
        "url": "https://thedogist.com/",
        "score": 1,
        "hidden": False,
    },
]


@app.get("/")
def homepage():
    return render_template("index.html", links=dog_links)

@app.post("/vote/<path:link_title>")
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

@app.post("/add_link")
def add_link():
    title = request.form.get("title")
    url = request.form.get("url")
    if title and "http" in url:
        dog_links.append({"title": title, "url": url, "score": 1, "hidden": False})
        dog_links.sort(key=lambda x: x["score"], reverse=True)
        return redirect("/")
    else:
        error = "Error: Title and URL are required."
        return render_template("index.html", links=dog_links, error=error)
    
@app.post("/hide/<path:link_title>")
def hide_link(link_title):
    for i, title in enumerate(dog_links):
        if title["title"] == link_title:
            dog_links[i]["hidden"] = True
            break
    return redirect("/")

@app.post("/unhide/<path:link_title>")
def unhide_link(link_title):
    for i, title in enumerate(dog_links):
        if title["title"] == link_title:
            dog_links[i]["hidden"] = False
            break
    return redirect("/")