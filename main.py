from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'genshin' 

#configuração de conexão com o db
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "{SGBD}://{user}:{password}@{server}/{database}".format(
        SGBD = "mysql+mysqlconnector",
        user = "root",
        password = "root",
        server = "localhost",
        database = "jogoteca"
    )
#instancia do db com SQLAlchemy
db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.name
    
class Usuarios(db.Model):
    nome = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(8), nullable=False, primary_key=True)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.name

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash("Jogo is already exists")
        return redirect(url_for('index'))
    
    #instanciar a criação de um novo jogo
    novo_jogo = Jogos(name=nome, category=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def auth():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['user'] = usuario.nickname
            flash(usuario.nickname + ' authentication sucesses!')
            next_page = request.form['proxima']
            return redirect(next_page)
    else:
      flash('User is not authenticated')        
      return redirect(url_for('login'))    
    
@app.route('/logout')
def logout():
    session['user'] = None
    flash('User is left!')
    return redirect(url_for('index'))

app.run(debug=True, host='0.0.0.0', port=8080)