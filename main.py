import base64
import os

import mysql.connector
import cv2
from tkinter import *
from flask import *
from tkinter import messagebox
from PIL import Image
from io import BytesIO

#iris libraries

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input



STATIC_FOLDER = 'templates/assets'
app = Flask(__name__,static_folder=STATIC_FOLDER)

app.secret_key = "not so secret key"


# funcs
#iris funcs
def preprocess_iris(image, target_size=(224, 224)):
    resized = cv2.resize(image, target_size)
    preprocessed = preprocess_input(resized)

    return np.expand_dims(preprocessed, axis=0)


def extract_features(image_path, model):
    image = cv2.imread(image_path)
    preprocessed_image = preprocess_iris(image)

    features = model.predict(preprocessed_image)
    return features.squeeze()


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)
def ValidateImages(image1_path,image2_path):
    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

    features1 = extract_features(image1_path, model)
    features2 = extract_features(image2_path, model)

    similarity = cosine_similarity(features1, features2)
    print(similarity)
    threshold = 0.72
    # ValidateImages('C:/Users/kanar/Documents/GitHub/cng492/ImageDb/b/b3.jpg','C:/Users/kanar/Documents/GitHub/cng492/captured-image/captured-image.jpg')
    print("Same person?", similarity > threshold)
    return similarity>threshold

# web functions
@app.route("/")   #yorum yaptım, github yükledim, hehee. :)
@app.route("/index")
def ana_index():
    if "TC" in session:
        session.pop("TC")
    return render_template("main_index.html")
@app.route("/admin_index")
def loginpage():
    if "admin_login" not in session:
        session["admin_login"]=0
    if session["admin_login"]==1:
        return redirect(url_for("show_admin_panel"))
    else:
        return render_template("index.html")

@app.route("/candidate_add")
def add_candidate():
    return render_template("React App.html")
@app.route("/login", methods=["GET", "POST"])
def login():  # does the login operation. Connects with database end checks it. Puts username in to the session if password and username from request matches with DB.
    admin_id = request.form.get("user_name")  # gets user name and password from login form in homepage
    admin_password = request.form.get("user_password")

    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM admin")
    records = cursor.fetchall()
    for data in records:
        print(data)
        if data[0] == admin_id:
            if data[1] == admin_password:
                print("connected")
                session["admin_login"]=1
                return redirect(url_for("show_admin_panel"))
            else:
                print("wrong password")
                return redirect(url_for("loginpage"))
        else:
            print("there is no admin with that username")
            return redirect(url_for("loginpage"))

    if db.is_connected():
        cursor.close()
    return redirect(url_for("login"))
@app.route("/admin_panel",methods=["GET", "POST"])
def show_admin_panel():
    if session["admin_login"]==1:
        return render_template("admin_panel.html")
    else:
        return redirect(url_for(loginpage))
@app.route("/create_candidate",methods=["GET", "POST"])
def register_candidate():
    id = request.form.get("id")
    ballot_id = request.form.get("ballot")
    fullname = request.form.get("candidate_name")
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    # insert election
    sql = (
        "INSERT INTO president(id,vote_ballot_id,fullname,keyword)"
        "VALUES (%s, %s, %s, %s)"
    )
    data = (fullname+id,ballot_id,fullname,fullname)
    # Executing the SQL command
    cursor.execute(sql, data)
    # Commit your changes in the database
    db.commit()
    return redirect(url_for("show_admin_panel"))
@app.route("/show_ongoing_election")
def show_ongoing():
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute("SELECT id FROM election WHERE status='ongoing' ")
    ongoing_elections = cursor.fetchall()
    return render_template("ongoing_elections.html",elections=ongoing_elections)
@app.route("/admin_logout")
def admin_logout():
    session["admin_login"]=0
    return redirect(url_for("loginpage"))
@app.route("/manage_election")
def update_election_status():
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM election")
    records = cursor.fetchall()
    return render_template("manage_election.html",elections=records)
@app.route("/manage_election_after",methods=["GET", "POST"])
def manage_election_after():
    a=request.form.get("election_select")
    a=a.split()
    print(a)
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    sql = "UPDATE election SET status='%s' WHERE id='%s'" %(a[0],a[1])
    print(sql)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for("show_admin_panel"))
@app.route("/take_photo",methods=["GET", "POST"])
def take_photo():
    data = request.get_json()
    image_data = data['image']
    image_data = base64.b64decode(image_data.split(',')[1])

    # Save the image to a file or process it
    image = Image.open(BytesIO(image_data))
    image.save(os.path.join('captured-image', 'captured-image.jpg'))
    return jsonify(success=True)
@app.route("/validate_image",methods=["GET", "POST"])
def validate_image():
    if ValidateImages('C:/Users/kanar/Documents/GitHub/cng492/ImageDb/b/b1.jpg',
                      'C:/Users/kanar/Documents/GitHub/cng492/captured-image/captured-image.jpg'):
        return redirect(url_for('show_ongoing'))
    else:
       return redirect(url_for('ana_index'))


@app.route("/take_photo_test",methods=["GET", "POST"])
def take_photo_test():
    citizen_id = request.form.get("TC")
    print(citizen_id)
    session["TC"] = citizen_id

    return render_template("take_pic.html")
@app.route("/create_election")
def create_election_form():
    return render_template("election.html")
@app.route("/show_elections")
def show_elections():
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM election")
    records = cursor.fetchall()
    return render_template("all_elections.html",elections=records)
@app.route("/see_election_results/<election_id>")
def show_election_result(election_id):
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute(("SELECT * FROM vote WHERE vote_ballot_id = %s" % election_id ))
    records = cursor.fetchall()
    results = {}
    for vote in records:
        if vote[2] not in results:
            results[str(vote[2])]=0
        results[str(vote[2])]+=1
    labels = []
    values = []
    for key in results.keys():
        values.append(results[key])
        labels.append(key)
    return render_template("chart.html",title='Election Result',max=20, values=values,labels=labels)
@app.route("/create_election_submit",methods=["GET", "POST"])
def create_election():
    election_id = request.form.get("election_id")
    start_date = request.form.get("s_time")
    end_date = request.form.get("e_time")
    option = request.form.get("option")

    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    #insert election
    sql= (
        "INSERT INTO election(id,start_time,end_time,status)"
        "VALUES (%s, %s, %s, %s)"
    )
    election_data = (election_id,start_date,end_date,"ongoing")
    # Executing the SQL command
    cursor.execute(sql,election_data)
    # Commit your changes in the database
    db.commit()

    # insert vote ballot
    sql = (
        "INSERT INTO vote_ballot(id,election_id,type)"
        "VALUES (%s, %s, %s )"
    )
    vote_ballot_data = (election_id,election_id,option)
    cursor.execute(sql,vote_ballot_data)
    db.commit()

    db.close()
    return redirect(url_for("show_admin_panel"))
@app.route("/citizen_tc")
def get_tc():
    return render_template("get_tc.html")
@app.route("/citizen_index/<election_id>")
def citizen_index(election_id):
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    print(election_id)
    cursor.execute(("SELECT * FROM president WHERE vote_ballot_id = %s" % election_id))
    records = cursor.fetchall()
    return render_template("citizen_index.html",candidates=records)
@app.route("/register_vote/<candidate_id>/<candidate_keyword>/<election_id>")
def register_vote(candidate_id,candidate_keyword,election_id):
    citizen_tc = session["TC"]
    print(citizen_tc,candidate_id,candidate_keyword)
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    # insert election
    sql = (
        "INSERT INTO vote(ssn,vote_ballot_id,selection)"
        "VALUES (%s, %s, %s)"
    )
    election_data = (citizen_tc,str(election_id),candidate_keyword)
    # Executing the SQL command
    try:
        cursor.execute(sql, election_data)
    except:
        messagebox.showerror('Voting ERROR', 'You voted already')
        redirect(url_for("ana_index"))
    # Commit your changes in the database
    db.commit()
    return redirect(url_for("ana_index"))
app.run()