from flask import Flask, render_template

app = Flask(__name__) #to determine the root path

@app.route('/') #connecting a webpage; "/" = the root directory aka the homepage of our website
                #this is tying an url on our website to a Python function

def home(): #because it's just the homepage, we may name it home
    return render_template("home.HTML")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/shellpred_test")
def shellpred_test():
    return render_template("shellpred_test.html")

@app.route("/sinopecpred")
def sinopecpred():
    return render_template("sinopecpred.html")

@app.route("/lukoilpred")
def lukoilpred():
    return render_template("lukoilpred.html")

@app.route("/exxonpred")
def exxonpred():
    return render_template("exxonpred.html")

if __name__ == "__main__":
    app.run(debug=True)


