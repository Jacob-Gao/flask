from flask import Flask, render_template, request, flash,get_flashed_messages, session,redirect,url_for,make_response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://jacob:jacob@127.0.0.1/flask_sql'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = 'agfafgasdgaz'


app.config.from_object('settings.Config')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password','密码填入的不一致')])
    submit = SubmitField('提交')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role: %s %s>' % (self.name, self.id)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, index=True)
    email = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User: %s %s %s %s>' % (self.name, self.id, self.email, self.password)

@app.before_first_request
def first(*args,**kwargs):
    pass

@app.before_request
def process_request(*args, **kwargs):
    print("进来了")

@app.after_request
def process_response(response):
    return response

@app.errorhandler(404)
def error_404(*args):
    print(*args)
    return '404'


@app.route('/form', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if login_form.validate_on_submit():
            return 'gcp'
        else:
            flash('尤物')

    return render_template('gaochenpeng/index.html', form=login_form)


@app.route('/detail/<int:nid>',methods=['GET'])
def detail(nid):
    return redirect(url_for('index1'))
#    return str(nid)

@app.route('/cookie')
def set_cookie():
    response = make_response("dsfagfa")
    response.set_cookie('key', 'value')
    flash('超时错误', category="x1")
    return response

@app.route('/session')
def set_session():
    session['k1'] = 'v1'
    session['k2'] = 'v2'
    data = get_flashed_messages(category_filter=['x1'])
    return data




@app.route('/', methods=['GET', 'POST'],endpoint='index1')
def index():
    login_form = LoginForm()
    return render_template('gaochenpeng/index.html', form=login_form)


@app.route('/orders/<order_id>')
#@app.route('/orders/<int:order_id>')
def get_order_id(order_id):
    return 'order_id %s' % order_id





    # 删除表
db.drop_all()
    # 创建表
db.create_all()

if __name__ == '__main__':
    app.run()
