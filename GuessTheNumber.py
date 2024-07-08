from flask import Flask, render_template, request, session
import random
from urllib.parse import urljoin


def initializeGifs(fileName):
    # reading in all the gifs codes
    gifs = {}
    with open(fileName, "r") as file:
        for line in file:
            section, path = line.strip().split("*")
            gifs.setdefault(section, []).append(path)
    return gifs

def randomNumber():
  return random.randint(0, 9)

def randomGif(section):
  # returns a random gif from the section selected
  if section in gifs:
    return random.choice(gifs[section])
  else:
    return gifs["stWentWrong"]
  
def GifURL(Gif):
   # combines the gif code with the rest of the url
   baseURL = "https://imgur.com/"
   return urljoin(baseURL, Gif)


app = Flask(__name__)
app.secret_key = "csRe"
gifs = initializeGifs("static/Gifs.txt")

# enumerating the colors for each guess (each page will be colored according to the users guess)
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
    session["num"] = randomNumber() # initializing a random number as the computers choice
    turnsLeft = 3
    session["turnsLeft"] = turnsLeft # keeping count of turns in the session - so that it doesn't restart every time
    return render_template("mm.html", turnsLeft = turnsLeft)


@app.post("/guess")
def guess():
    try:
        guess = int(request.form["guess"]) # reading in the users guess
    except ValueError: # incase the users enters something other than a number
       message = "Please enter a number"
       return render_template("result.html", message = message, Gif = randomGif("Won"), colors = colors, guess = guess)

    session["turnsLeft"] -= 1 # keeping count of turns left
    turnsLeft = session["turnsLeft"]
    num = session["num"]

    # figuring out what message, gif and page to show according to the user's guess
    if guess == num:
        end = True
        message = "You found me!\nYou Win!!!!"
        Gif = randomGif("Won")
    elif turnsLeft == 0:
        end = True
        message = "Out of guesses :(\nYou Lose..."
        Gif = randomGif("Lost")
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
