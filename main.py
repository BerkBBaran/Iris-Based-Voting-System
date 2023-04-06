import mysql.connector
import cv2
from tkinter import *
from mysql.connector import Error
from flask import *
from tkinter import messagebox
from tensorflow.keras.models import load_model


def draw_boundary(img,classifier, scaleFactor, minNeighbors,color,text):
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #rgb resimi gray scale image a çeviriyor
    features = classifier.detectMultiScale(gray_img,scaleFactor,minNeighbors) #uzaktaki yüzün karesini scaleliyor.
    coords= []
    for(x,y,w,h) in features:   #karenin kordinatları
        cv2.rectangle(img,(x,y), (x+w,y+h),color,2)  #rectangle ı belirtilen kordinatlarda çiz
        cv2.putText(img,text,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA) #karenin adı
        coords = [x,y,w,h] #update the cordinates
    return coords
def boundary(img,classifier,scaleFactor,minNeighbors):   #görünmez kare, göz resmi çekmek için
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    for (x, y, w, h) in features:  # karenin kordinatları
        coords = [x, y, w, h]  # update the cordinates
    return coords
def detect(img,faceCascade,eyeCascade):
    color = {"blue" : (255,0,0), "red" : (0,0,255), "green": (0,255,0)} #color dictionary
    coords = draw_boundary(img,eyeCascade,1.1,10,color["blue"],"Eye") #kareyi çiz
    #if len(coords) == 4:   #karenin içinde gözleri arıyoruz
        #roi_img = img[coords[1]:coords[1]+coords[3],coords[0]:coords[0]+coords[2]]
        #coords = draw_boundary(roi_img,eyeCascade,1.1,10,color["red"], "eyes") #kareyi çiz
    return img
def take_eye(img,eyesCascade):
    coords = boundary(img, eyesCascade, 1.1, 10)
    roi_img = img[coords[1]:coords[1]+coords[3],coords[0]:coords[0]+coords[2]]
    return roi_img

STATIC_FOLDER = 'templates/assets'
app = Flask(__name__,static_folder=STATIC_FOLDER)

app.secret_key = "not so secret key"


# funcs

# web functions
@app.route("/")   #yorum yaptım, github yükledim, hehee. :)
@app.route("/index")
def ana_index():
    if "election_id" not in session:
        session["election_id"]="Election not configured"
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
        return render_template("admin_panel.html",session_election=session["election_id"])
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
    citizen_id= request.form.get("TC")
    session["TC"]=citizen_id
    print(citizen_id)
    return redirect(url_for("citizen_index"))
    video_capture = cv2.VideoCapture(0)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    eyesCascade = cv2.CascadeClassifier("haarcascade_eye.xml")


    eye_png_counter = 0

    while True:
        _, img = video_capture.read()  # kamerayı açıp img olarak okuyacak.
        img = detect(img, faceCascade, eyesCascade)
        cv2.imshow("face detection", img)  # kamerayı göster, içindeki string window un adı
        if cv2.waitKey(1) & 0xFF == ord('q'):  # klavyeden q tuşuna bastığında kapanıcak
            img = take_eye(img, eyesCascade)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # rgb resimi gray scale image a çeviriyor
            image_name = "eye_{}.png".format(eye_png_counter)  #
            # image_name = "eye_.png"
            cv2.imwrite(image_name, img)
            eye_png_counter += 1
            break
    video_capture.release()
    cv2.destroyAllWindows()



    return redirect(url_for("citizen_index"))
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
@app.route("/citizen_index")
def citizen_index():
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute(("SELECT * FROM president WHERE vote_ballot_id = %s" % 12))
    records = cursor.fetchall()
    return render_template("citizen_index.html",candidates=records)
@app.route("/register_vote/<candidate_id>/<candidate_keyword>")
def register_vote(candidate_id,candidate_keyword):
    citizen_tc = session["TC"]
    print(citizen_tc,candidate_id,candidate_keyword)
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    # insert election
    sql = (
        "INSERT INTO vote(ssn,vote_ballot_id,selection)"
        "VALUES (%s, %s, %s)"
    )
    election_data = (citizen_tc,"12",candidate_keyword)
    # Executing the SQL command
    try:
        cursor.execute(sql, election_data)
    except:
        messagebox.showerror('Voting ERROR', 'You voted already')
        redirect(url_for("ana_index"))
    # Commit your changes in the database
    db.commit()
    session.pop("TC")
    return redirect(url_for("ana_index"))
app.run()