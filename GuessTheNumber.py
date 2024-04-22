from flask import Flask, render_template, request, session
import random
from urllib.parse import urljoin


def initializeGifs(fileName):
    gifs = {}
    with open(fileName, "r") as file:
        for line in file:
            section, path = line.strip().split("*")  # Better to use csv and csv reader as we learnt in the course
            gifs.setdefault(section, []).append(path)
    return gifs

def randomNumber():
  return random.randint(0, 9)

def randomGif(section):
  if section in gifs:
    return random.choice(gifs[section])
  else:
    return gifs["stWentWrong"]
  
def GifURL(Gif):
   baseURL = "https://imgur.com/"
   return urljoin(baseURL, Gif)


app = Flask(__name__)
app.secret_key = "csRe"
gifs = initializeGifs("static/Gifs.txt")

colors = {
    0: "red",
    1: "orange",
    2: "yellowgreen",
    3: "green",
    4: "teal",
    5: "blue",
    6: "indigo",
    7: "rust",
    8: "purple",
    9: "black"
}

@app.get("/")
def home():
    session["num"] = randomNumber()
    turnsLeft = 3
    session["turnsLeft"] = turnsLeft
    return render_template("mm.html", turnsLeft = turnsLeft)


@app.post("/guess")
def guess():
    try:
        guess = int(request.form["guess"])
    except ValueError:
       message = "Please enter a number"
       return render_template("result.html", message = message, Gif = randomGif("Won"), colors = colors, guess = guess)

    session["turnsLeft"] -= 1
    turnsLeft = session["turnsLeft"]
    num = session["num"]
    if guess == num:
        end = True
        message = "You found me!\nYou Win!!!!"
        Gif = Gif = randomGif("Won")
    elif turnsLeft == 0:
        end = True
        message = "Out of guesses :(\nYou Lose..."
        Gif = Gif = randomGif("Lost")
    elif guess < num:
        end = False
        message = "Oops! Too Low..."
        Gif = Gif = randomGif("Low")
    elif guess > num:
        end = False
        message = "Oops! Too High..."
        Gif = Gif = randomGif("High")
    if end == True:
       return render_template("result.html", message = message, Gif = Gif, colors = colors, guess = guess)
    elif end == False:
       return render_template("guess.html", message = message, Gif = Gif, colors = colors,turnsLeft = turnsLeft, guess = guess)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True , port=5002)
