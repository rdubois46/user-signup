from flask import Flask, redirect, request, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True

@app.route("/")
def index():    

    name_error = ""
    password_error ="" 
    verification_error =""
    email_error ="" 
    
    return render_template("index.html", name_err=name_error, password_err=password_error, verify_err=verification_error, email_err=email_error)

@app.route("/submission", methods=['POST'])
def process_submission():
    user_name = request.form['username']
    password = request.form['password']
    verification = request.form['verify']
    email_address = request.form['email']

    name_error = ""
    password_error = ""
    verification_error = ""
    email_error = ""

    errors_present = False

    # data_list = [user_name, password, verification, email_address]
    # error_list = [name_error, password_error, verify_error, email_error]
    # required_list = [user_name, password, verification]

    # data_dict ={username: name_error, password: password_error, verification: verification_error, email_address: email_error}
  
    
    if not 2 < len(user_name) < 21 or " " in user_name:
        name_error = "Must contain no spaces and be 3-20 characters."
        errors_present = True

    if not 2 < len(password) < 21 or " " in password:
        password_error = "Must contain no spaces and be 3-20 characters." 
        errors_present = True

    if verification != password:
        verification_error = "The passwords do not match."
        errors_present = True

    if email_address:

        spaces = False
        periods = 0
        at_signs = 0

        for char in email_address:
            if char == " ":
                spaces = True
                break
            if char == ".":
                periods += 1
                continue
            if char == "@":
                at_signs += 1       

        if periods != 1 or at_signs != 1 or spaces:
            email_error = "Must contain one '@', one '.', and no spaces."
            errors_present = True

    
    if not user_name or not password or not verification:
        errors_present = True        
        if not user_name:
            name_error = "This field is required."
        if not password:
            password_error = "This field is required."
        if not verification:
            verification_error = "This field is required."

    if not errors_present:
        return render_template("success.html", username=user_name)
    else:
        return redirect("/error?username=" + user_name + "&email=" + email_address + "&name_err=" + name_error + "&password_err=" + password_error + "&verify_err=" + verification_error + "&email_err=" + email_error)

@app.route("/error", methods=['POST', 'GET'])
def error():
    user_name = request.args.get("username")
    email_address = request.args.get("email")

    name_error = request.args.get("name_err")
    password_error = request.args.get("password_err")
    verification_error = request.args.get("verify_err")
    email_error = request.args.get("email_err")

    return render_template("index.html", username=user_name, email=email_address, name_err=name_error, password_err=password_error, verify_err=verification_error, email_err=email_error)

app.run()

