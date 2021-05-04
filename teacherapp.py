from flask import *
import os, re, sqlite3
from logging import FileHandler, WARNING


app = Flask(__name__)
app.secret_key = ('pass')
if not app.debug:
    file_handler = FileHandler('log.log')
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid Username or Password.'
            app.logger.info('failed to log in admin')
            return render_template('/login.html', error=error)
        else:
            session['logged_in'] = True      #start a session
            if session.get('logged_in') != None:
                print('session started')
            app.logger.info('logged in successfully admin')
            return redirect('/dashboard')
    else:
        app.logger.info('failed to log in admin')
        return render_template('/login.html', error=error)



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/teacher.db')
    cur = conn.cursor()
    # add grades table when it is in db

    
    cur.execute("SELECT * FROM grades")
    info_grades = cur.fetchall()
    #print(info_grades)
    
    cur.execute("SELECT * FROM studentinfo, quizinfo")
    info = cur.fetchall()   #introduce argument in render_template
    #print(info)
    for rows in info_grades:
        for rows_2 in range(len(info)):
            if rows[1] == info[rows_2][0] and rows[2] == info[rows_2][3] :
                if len(info[rows_2]) == 7:
                    info[rows_2] = info[rows_2] +rows
                else:
                    info[rows_2] = info[rows_2][:-4] +rows
            else:
                if len(info[rows_2]) == 7:
                    info[rows_2] = info[rows_2] + (0,0,0,0)
        
    conn.commit()
    app.logger.info('Data Fetching successful')
    return render_template('/dashboard.html', info=info)

@app.route('/student_add', methods=['GET','POST'])
def student_add():
    if request.method == 'GET':
        return render_template('student_add.html')
    elif request.method == 'POST': 
        fname = request.form["fname"]
        lname = request.form["lname"]
        try: 
            path = os.path.dirname(os.path.abspath(__file__))
            conn = sqlite3.connect(path+'/teacher.db')
            cur = conn.cursor()
            
            cur.execute("INSERT INTO studentinfo (fname,lname) VALUES (?,?)",(fname,lname))
            app.logger.info(fname+" "+lname+' Inserted as new student')
            conn.commit()
            return render_template('dashboard.html')
        except:
            flash('Request Failed: Try Again')
            print("Error: NOT ADDED TRY AGAIN")
        finally:
            flash('New Student successfully added')
            return redirect(url_for('dashboard'))

@app.route('/quiz_add', methods=['GET','POST'])
def quiz_add():
    if request.method == 'GET':
        print("HERE")
        return render_template('quiz_add.html')
    elif request.method == 'POST':
        print("HERE2")
        subject = request.form["SUBJECT"]
        number_of_ques = request.form["NUM_QUESTIONS"]
        quiz_date = request.form["QUIZ_DATE"]
        try: 
            path = os.path.dirname(os.path.abspath(__file__))
            conn = sqlite3.connect(path+'/teacher.db')
            cur = conn.cursor()
            print("###########")
            cur.execute("INSERT INTO quizinfo (subject,questions,date) VALUES (?,?,?)",(subject,number_of_ques,quiz_date))
            print("**************")
            conn.commit()
            return render_template('dashboard.html')
        except:
            flash('Request Failed: Try Again')
            print("Error: NOT ADDED TRY AGAIN")
        finally:
            flash('New quiz successfully added')
            return redirect(url_for('dashboard'))

@app.route('/result_add', methods=['GET','POST'])
def result_add():
    if request.method == 'GET':
        return render_template('result_add.html')
    elif request.method == 'POST':
        st_id = request.form["student"]
        q_id = request.form["quiz"]
        q_score = request.form["quiz_score"]
        try: 
            path = os.path.dirname(os.path.abspath(__file__))
            conn = sqlite3.connect(path+'/teacher.db')
            cur = conn.cursor()
            print("###########")
            cur.execute("INSERT INTO grades (studentid, quizid, score) VALUES (?,?,?)",(st_id, q_id, q_score))
            print("**************")
            conn.commit()
            return render_template('dashboard.html')
        except:
            flash('Request Failed: Try Again')
            print("Error: NOT ADDED TRY AGAIN")
        finally:
            flash('New quiz successfully added')
            return redirect(url_for('dashboard'))


if __name__== '__main__' :
    app.run()


