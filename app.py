from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
app = Flask(__name__)
db = SQLAlchemy()
@app.route("/")
def hello_world():
    return render_template('index.html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/registration'
# # initialize the app with the extension
db.init_app(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mail_id'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



class Registration(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    cont = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=True)
    lang = db.Column(db.String(255), nullable=True)


    
@app.route("/registration", methods=['GET','POST'])
           
def registration():
    def hashing(passsworrrd):
        passsworrrd=list(passsworrrd)
        lst=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','y','z','1','2','3','4','5','6','7','8','9','0','#','%','@','&','*','!','a','b','c','s','d','e','$','v','f','f','5','4','4','d','f','5']
        word1=''
        for i in passsworrrd:
            if i in lst:
                worrd=lst.index(i)
                final=lst[abs(worrd+3)]+lst[abs(worrd+9)]+lst[abs(worrd+10)]+lst[abs(worrd+12)]
                word1+=final
        return word1

    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        dob = request.form.get('dob')
        cont = request.form.get('cont')
        address = request.form.get('address')
        state = request.form.get('state')
        lang = request.form.get('lang')
        hashed=hashing(password)
        entry = Registration(name = name,email = email,password = hashed, dob = dob, cont=cont , address=address,state = state, lang = lang)
        db.session.add(entry)
        db.session.commit()
        msg = Message(subject='confirmation mail!', sender='photovphactory@gmail.com', recipients=[email])
        msg.body = "Hey {0},thanks for submiting the form \n this is a auto generated message".format(name)
        mail.send(msg)
    return render_template('sucess.html',name=name)



    

if __name__=="__main__":
    app.run(debug=True)