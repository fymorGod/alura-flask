from flask import render_template, request, redirect, session, flash, url_for
from main import app, db
from models.models import Jogos, Usuarios

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