import base64
import mysql.connector
from tkinter import *
from flask import *
from PIL import Image
from io import BytesIO
from model import *
import random

STATIC_FOLDER = 'templates/assets'
app = Flask(__name__,static_folder=STATIC_FOLDER)
app.secret_key = "not so secret key"


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
    if session["admin_login"]!=1:
        return redirect(url_for('ana_index'))
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute("SELECT id FROM election WHERE status != 'ongoing' ")
    records = cursor.fetchall()
    for data in records:
        print(data)
    elections = [data[0] for data in records]
    return render_template("add_candidate.html",elections=elections)
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
                error = "Wrong admin crediantials, try again."
                return render_template("error_hub.html", error=error)
        else:
            error = "Wrong admin crediantials, try again."
            return render_template("error_hub.html", error=error)

    if db.is_connected():
        cursor.close()
    return redirect(url_for("login"))
@app.route("/admin_panel",methods=["GET", "POST"])
def show_admin_panel():
    if session["admin_login"]==1:
        return render_template("admin_panel.html")
    else:
        return redirect(url_for("ana_index"))
@app.route("/create_candidate",methods=["GET", "POST"])
def register_candidate():
    ballot_id = request.form.get("election_select")
    fullname = request.form.get("candidate_name")
    print(ballot_id)
    print(fullname)
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    # insert election
    sql = (
        "INSERT INTO president(id,vote_ballot_id,fullname,keyword)"
        "VALUES (%s, %s, %s, %s)"
    )
    data = (fullname,ballot_id,fullname,fullname)
    # Executing the SQL command
    try:
        cursor.execute(sql, data)
        db.commit()
        return redirect(url_for("show_admin_panel"))
    except:
        return render_template("error_hub.html", error="Database error check your variables")
@app.route("/show_ongoing_election")
def show_ongoing():
    if "TC" not in session:
        return redirect(url_for("ana_index"))
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
    if session["admin_login"]!=1:
        return redirect(url_for('ana_index'))
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
    captured_id=session["TC"] + ".jpg"
    image.save(os.path.join('captured-image', captured_id))
    return jsonify(success=True)
@app.route("/validate_image",methods=["GET", "POST"])
def validate_image():
    return redirect(url_for('show_ongoing'))
    if ValidateImages('C:/Users/kanar/Documents/GitHub/cng492/ImageDb/b/k1.jpg',
                      'C:/Users/kanar/Documents/GitHub/cng492/captured-image/captured-image.jpg'):
        return redirect(url_for('show_ongoing'))
    else:
       return redirect(url_for('ana_index'))


@app.route("/take_photo_test",methods=["GET", "POST"])
def take_photo_test():
    citizen_id = request.form.get("TC")
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    if(citizen_id != ""):
        cursor.execute(("SELECT ssn FROM citizen where ssn = %s" % citizen_id))
        records = cursor.fetchall()
        if records == []:
            error = "This citizen ID does not exists."
            return render_template("error_hub.html", error=error)
    if(citizen_id.isnumeric()!=1):
        error = "Invalid citizen id, please try again."
        return render_template("error_hub.html",error=error)
    session["TC"] = citizen_id
    return render_template("take_pic.html")
@app.route("/test",methods=["GET", "POST"])
def test():
    return render_template("casia_selection.html")
@app.route("/create_election")
def create_election_form():
    if session["admin_login"]!=1:
        return redirect(url_for('ana_index'))
    return render_template("election2.html")
@app.route("/show_elections")
def show_elections():
    if session["admin_login"]!=1:
        return redirect(url_for('ana_index'))
    db = mysql.connector.connect(host='localhost', database='cng491', user='root', password='root')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM election")
    records = cursor.fetchall()
    return render_template("all_elections.html",elections=records)
@app.route("/see_election_results/<election_id>")
def show_election_result(election_id):
    if session["admin_login"]!=1:
        return redirect(url_for('ana_index'))
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
    try:
        election_data = (election_id, start_date, end_date, "ongoing")
        # Executing the SQL command
        cursor.execute(sql, election_data)
        # Commit your changes in the database
        db.commit()

        # insert vote ballot
        sql = (
            "INSERT INTO vote_ballot(id,election_id,type)"
            "VALUES (%s, %s, %s )"
        )
        vote_ballot_data = (election_id, election_id, option)
        cursor.execute(sql, vote_ballot_data)
        db.commit()

        db.close()
        return redirect(url_for("show_admin_panel"))
    except:
        error="Election already exists in the database!, Try to add an another election."
        return render_template("error_hub.html",error=error)
@app.route("/citizen_tc")
def get_tc():
    return render_template("get_tc.html")
@app.route("/citizen_index/<election_id>")
def citizen_index(election_id):
    if "TC" not in session:
        return redirect(url_for("ana_index"))
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
    except Exception as e:
        print(e)
        error = "You cant vote on the same election twice"
        return render_template("error_hub.html", error=error)
    # Commit your changes in the database
    db.commit()
    msg = "You voted successfully, returning to homepage."
    return render_template("error_hub.html",error=msg)
@app.route("/validate_new",methods=["GET", "POST"])
def validate_new():
    print(session["TC"])
    try:
        highest_similarity, highest_similarity_image=search_single_folder(str(session["TC"]))
        threshold = 0.60
        if(highest_similarity>=threshold):
            return redirect(url_for('show_ongoing'))
        else:
            return redirect(url_for("ana_index"))
    except:
        error="This person does not have registered iris image."
        return render_template("error_hub.html", error=error)
@app.route("/validate_new_test",methods=["GET", "POST"])
def validate_new_test():
    entered_id = request.form.get("id")
    selected_image = request.form.get("image")
    print(entered_id)
    print(selected_image)
    try:
        highest_similarity, highest_similarity_image=search_single_folder_test(str(entered_id),str(selected_image))
        threshold = 0.60
        if(highest_similarity>=threshold):
            error = "login success"
            return render_template("error_hub.html", error=error,sim=str(highest_similarity))
        else:
            error = "login failed"
            return render_template("error_hub.html", error=error, sim=str(highest_similarity))
    except:
        error="This person does not have registered iris image."
        return render_template("error_hub.html", error=error)
@app.route("/wait_model",methods=["GET", "POST"])
def wait_model():
    if "TC" not in session:
        return redirect(url_for("ana_index"))
    election_tips = [
        "Research the candidates and their positions before casting your vote.",
        "Make sure you are registered to vote and know your polling location.",
        "Consider the impact of your vote on key issues like healthcare, education, and the economy.",
        "Encourage your friends and family to exercise their right to vote.",
        "Stay informed about current events and political developments.",
        "Volunteer or support organizations that promote voter registration and participation.",
        "Attend local town halls or debates to learn more about the candidates.",
        "Understand the voting process in your area, including early voting and mail-in ballot options.",
        "Engage in respectful discussions with others about different political perspectives.",
        "Vote not only in national elections but also in local and state-level elections."
    ]
    random_tip = random.choice(election_tips)
    return render_template("wait_model.html",random_tip=random_tip)
if __name__ == '__main__':
    app.run()