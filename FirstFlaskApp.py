"""
Basic Flask web server.
Run this program to start the web server, press CTRL+C to stop.
"""
__author__ = "Charlie Friend"

import random, hashlib

from flask import Flask, render_template, request, redirect

dad_jokes = [
"Did you hear about the restaurant on the moon? Great food, no atmosphere.",
"Want to hear a joke about paper? Nevermind it's tearable. ",
"What do you call a fake noodle? An Impasta.",
"What did the grape do when he got stepped on? He let out a little wine.",
"5/4 of people admit that they’re bad with fractions.",
"I thought about going on an all-almond diet. But that's just nuts"
]



app = Flask(__name__)


usernames = []
passwords = []




@app.route('/home')
def main():
    user_id = request.cookies.get('userID')
    print(user_id)
    user_password = request.cookies.get('user_pword')
    print(user_password)
    if user_id == None or user_password == None:
        return "You must log in to view this page."
    else:
        return render_template("hello.html")
    # OR put this here:return "Welcome " + user_id + "!"

@app.route("/joke")
def joke():
    user_id = request.cookies.get('userID')
    print(user_id)
    user_password = request.cookies.get('user_pword')
    print(user_password)
    if user_id == None or user_password == None:
        return "You must log in to view this page."
    else:
        next_joke = random.choice(dad_jokes)
        return render_template("jokegenerator.html", thejoke=next_joke)


@app.route('/welcome')
def welcome():
    myName = request.args.get("name")
    user_id = request.cookies.get('userID')
    print(user_id)
    user_password = request.cookies.get('user_pword')
    print(user_password)
    if user_id == None or user_password == None:
        return "You must log in to view this page."
    else:
         if myName == None:
            return "Hello, welcome to my web server!" + "\n" + render_template("welcome.html")
         else:
            return "Hello " + myName + ", welcome to my web server!" + "\n" + render_template("welcome.html")



@app.route('/hello')
def hello():
    user_id = request.cookies.get('userID')
    print(user_id)
    user_password = request.cookies.get('user_pword')
    print(user_password)
    if user_id == None or user_password == None:
        return "You must log in to view this page."
    else:
        return render_template("hi.html")

@app.route('/2048')
def game():
    user_id = request.cookies.get('userID')
    print(user_id)
    user_password = request.cookies.get('user_pword')
    print(user_password)
    if user_id == None or user_password == None:
        return "You must log in to view this page."
    else:
        return render_template("2048.html")


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    # If we are POSTing to the /login route, then check the credentials!
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        password_bin = password.encode()
        password_hash = hashlib.sha256(password_bin).hexdigest()


        for i in range(0,len(usernames)):
            if password_hash == passwords[i] and username == usernames[i]:
                response = redirect("/home")
                response.set_cookie('userID', username)
                response.set_cookie('user_pword', password)
                return response
            else:
                error = "Incorrect username or password! Please try again!"
                print("Login failed!")


    return render_template('login.html', error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
   error = None

   # If we are POSTing to the /login route, then check the credentials!
   if request.method == "POST":
       requested_username = request.form['suusername']
       requested_password = request.form['supassword']

       password_bin = requested_password.encode()
       password_hash = hashlib.sha256(password_bin).hexdigest()

       # Write the username to a file
       with open("all_usernames.txt", "a") as outfile:
           outfile.write(requested_username)
           outfile.write("\n")
           usernames.append(requested_username)

       # Write the password hash to a file
       with open("all_passwords.txt", "a") as outfile:
           outfile.write(password_hash)
           outfile.write("\n")
           passwords.append(password_hash)

       return redirect("/")

   return render_template('signup.html', error=error)










# Only run the app if this is the script being run. Otherwise importing this
# file will start the web server.
#
# Using host='0.0.0.0' causes the app to listen on all interfaces, so you
# should be able to access it from other computers on the local network.
if __name__ == "__main__":
   #read in file, and store usernames and passwords in the usernames and passwords lists
   try:
       with open("all_usernames.txt", "r") as infile:
           for line in infile:
	     #strips off the ‘return’ character  - this is not part of the username!
               line = line.rstrip('\n')
               usernames.append(line)
   except:
       print("no username file created yet ")

   try:
       with open("all_passwords.txt", "r") as infile:
           for line in infile:
               line = line.rstrip('\n')
               passwords.append(line)
   except:
       print("no passwords file created yet")

   app.run(host='0.0.0.0', ssl_context=("mypublickey.pem", "myprivatekey.pk"))

