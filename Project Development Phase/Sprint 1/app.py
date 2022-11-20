from flask import Flask, render_template, request,redirect, url_for,escape,jsonify
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import ibm_db 


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cpx90924;PWD=Wq27hQ1Veq7bFkKx",'','')
app=Flask(__name__)


@app.route('/')
def index():
    return render_template('Homepage.html')


@app.route('/signup',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        org=request.form['organization']
        location=request.form['location']
        pwd=request.form['password']
        stmt=ibm_db.prepare(conn,"Insert into RetailersInformation(Name,EmailId,OrganisationName,Location,Password) values(?,?,?,?,?)")
        ibm_db.bind_param(stmt,1,name)
        ibm_db.bind_param(stmt,2,email)
        ibm_db.bind_param(stmt,3,org)
        ibm_db.bind_param(stmt,4,location)
        ibm_db.bind_param(stmt,5,pwd)
        ibm_db.execute(stmt)
        return render_template('Signin.html')
    else:
        return render_template('Signup.html')


@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method=="POST":
        email=request.form["email"]
        pwd=request.form["password"]
        sql=f"select * from RetailersInformation where EmailId='{email}' and Password='{pwd}'"
        stmt=ibm_db.exec_immediate(conn,sql)
        flag=ibm_db.fetch_row(stmt)
        if flag > 0:
            return redirect(url_for("home"))
        else :
            return "Invalid id or password"
    else:
        return render_template("Signin.html")
        

@app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if request.method=="GET":
        return render_template("SendMail.html")
    elif request.method=="POST":
        email=request.form['email']
        sg = sendgrid.SendGridAPIClient(api_key="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")
        from_email = Email("dineshrs2002@gmail.com")  # Change to your verified sender
        to_email = To(email)  # Change to your recipient
        subject = "[Inventory Management] Please reset your password"
        content = Content("text/html", f"We heard that you lost your Inventory Management Portal password. Sorry about that!<br>But don’t worry! You can use the following button to reset your password:<br> <button><a href='http://127.0.0.1:5000/reset?email={email}'> reset</a></button>")
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        if response.status_code!=202:
            return "alert(Invalid mail)"
        else:
            return "<h1>Mail Sent Sucessfully</h1>"
        

@app.route('/reset', methods=["GET","POST"])
def reset_html():
    if request.method=="POST":
        email=request.args.get('email')
        pwd=request.form['password']
        sql=f"update RetailersInformation set password='{escape(pwd)}' where emailid='{email}'"
        stmt=ibm_db.exec_immediate(conn,sql)
        return redirect(url_for("signin")) 
    else:
        return render_template("ResetPassword.html")

  



if __name__=="__main__":
    app.run(debug=True)

#pending work: edit and delete function cant get id from url