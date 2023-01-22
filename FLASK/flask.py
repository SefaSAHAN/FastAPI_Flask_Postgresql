from flask import Flask, render_template, request,flash
import psycopg2

app = Flask(__name__)
app.secret_key="bp"  #this is for flash messages

#Add a name     
@app.route('/', methods=['POST','GET'])
def index():
    conn = psycopg2.connect(dbname='flask', user='postgres', password='postgres')    
    if request.method == "POST":
        # Get the user's input from the form
        input = request.form['user_input']
        cur = conn.cursor()
        cur.execute("INSERT INTO inputs (input) VALUES (%s)", (input,))
        conn.commit()
        cur.execute("SELECT * from inputs order by id")
        result=cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html',input=input,result=result)

    cur=conn.cursor()
    cur.execute("SELECT * from inputs order by id")
    result=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html',result=result)

#update a name
@app.route("/update", methods=['POST','GET'])
def update():
    conn = psycopg2.connect(dbname='flask', user='postgres', password='postgres')
    id= request.form['user_id']
    name=request.form['user_name']
    cur=conn.cursor()
    cur.execute(f"select * from inputs where id={id}")
    result=cur.fetchone()
    if result is not None:
        query=f"update inputs set input='{name}' where id={id}"
        cur.execute(query)
        conn.commit()
        cur.execute("SELECT * from inputs order by id")
        result=cur.fetchall()
        cur.close()
        conn.close() 
        return render_template('index.html',result=result,new_name=name)
    else:
        cur=conn.cursor()
        cur.execute("SELECT * from inputs order by id")
        result=cur.fetchall()
        cur.close()
        conn.close() 
        flash("There is no such id check your id please","danger")
        return render_template('index.html',result=result)

@app.route("/search", methods=['POST','GET'])
def search():
    conn = psycopg2.connect(dbname='flask', user='postgres', password='postgres')
    name=request.form['user_search']
    cur=conn.cursor()
    cur.execute(f"select * from inputs where input LIKE '{name}%' order by id")
    result=cur.fetchall()
    if len(result)>0:
        cur.close()
        conn.close() 
        return render_template('index.html',result=result,searched_name=name)
    else:
        cur=conn.cursor()
        cur.execute("SELECT * from inputs order by id")
        result=cur.fetchall()
        cur.close()
        conn.close() 
        flash("There is no such name in database ","danger")
        return render_template('index.html',result=result)
        
@app.route("/delete", methods=['POST','GET'])
def delete():
    conn = psycopg2.connect(dbname='flask', user='postgres', password='postgres')
    id=request.form['user_delete']    
    cur=conn.cursor()
    cur.execute(f"select * from inputs where id={id}")
    result=cur.fetchone()
    if result is not None:
        name=result[1]
        cur.execute(f"DELETE FROM inputs where id={id}")
        conn.commit()
        cur.execute("SELECT * from inputs order by id")
        result=cur.fetchall()
        cur.close()
        conn.close() 
        return render_template('index.html',result=result,deleted_name=name)
    else:
        cur=conn.cursor()
        cur.execute("SELECT * from inputs order by id")
        result=cur.fetchall()
        cur.close()
        conn.close() 
        flash("There is no such id in database ","danger")
        return render_template('index.html',result=result)
        

if __name__ == '__main__':
    app.run()

