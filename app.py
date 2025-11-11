from flask import Flask, render_template, request, redirect
import sqlite3

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

def dog_links_db():
    conn = sqlite3.connect("dog_links.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, 
            url TEXT NOT NULL, 
            score INTEGER NOT NULL DEFAULT 1, 
            hidden INTEGER NOT NULL DEFAULT 0, 
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    c.execute("SELECT COUNT(*) FROM posts")
    count = c.fetchone()[0]

    if count == 0:
        for link in dog_links:
            c.execute("INSERT INTO posts (title, url, score, hidden) VALUES (?, ?, ?, ?)", 
                      (link["title"], link["url"], link["score"], int(link["hidden"])))
        conn.commit()
    conn.close()

@app.get("/")
def homepage():
    conn = sqlite3.connect("dog_links.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE hidden = 0 ORDER BY score DESC")
    visible = c.fetchall()
    c.execute("SELECT * FROM posts WHERE hidden = 1 ORDER BY created_at DESC")
    hidden = c.fetchall()
    conn.close()
    return render_template("index.html", links=visible, hidden_links=hidden)

@app.post("/vote/<path:link_title>")
def vote(link_title):
    vote = request.form.get("vote")
    conn = sqlite3.connect("dog_links.db")
    c = conn.cursor()
    for i, title in enumerate(dog_links):
        if title["title"] == link_title:
            if vote == "up":
                c.execute("UPDATE posts SET score = score + 1 WHERE title = ?", (link_title,))
                #dog_links[i]["score"] += 1
            elif vote == "down":
                c.execute("UPDATE posts SET score = score - 1 WHERE title = ?", (link_title,))
                #dog_links[i]["score"] -= 1
            break
    dog_links.sort(key=lambda x: x["score"], reverse=True)
    conn.commit()
    conn.close()
    return redirect("/")

@app.post("/add_link")
def add_link():
    title = request.form.get("title")
    url = request.form.get("url")
    if title and "http" in url:
        #dog_links.append({"title": title, "url": url, "score": 1, "hidden": False})
        #dog_links.sort(key=lambda x: x["score"], reverse=True)
        conn = sqlite3.connect("dog_links.db")
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, url, score, hidden) VALUES (?, ?, 1, 0)", (title, url))
        conn.commit()
        conn.close()
        return redirect("/")
    else:
        error = "Error: Title and URL are required."
        return render_template("index.html", links=dog_links, error=error)
    
@app.post("/hide/<path:link_title>")
def hide_link(link_title):
    conn = sqlite3.connect("dog_links.db")
    c = conn.cursor()
    c.execute("UPDATE posts SET hidden = 1 WHERE title = ?", (link_title,))
    conn.commit()
    conn.close()
    #for i, title in enumerate(dog_links):
    #    if title["title"] == link_title:
    #        dog_links[i]["hidden"] = True
    #        break
    return redirect("/")

@app.post("/unhide/<path:link_title>")
def unhide_link(link_title):
    conn = sqlite3.connect("dog_links.db")
    c = conn.cursor()
    c.execute("UPDATE posts SET hidden = 0 WHERE title = ?", (link_title,))
    conn.commit()
    conn.close()
    #for i, title in enumerate(dog_links):
    #    if title["title"] == link_title:
    #        dog_links[i]["hidden"] = False
    #        break
    return redirect("/")

dog_links_db()

if __name__ == "__main__":
    app.run(debug=True)