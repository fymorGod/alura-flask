from flask import Flask, render_template, request, redirect, session, flash, url_for
class Jogo:
    def __init__(self, name:str, category:str, console:str):
        self.name = name
        self.category = category
        self.console = console

class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password

user1 = User('fylip', 'mufina', 'honkai')
user2 = User('camila', 'nila', 'paozinho')
user3 = User('tomas', 'tom', 'python_is_life')

users = {
    user1.nickname: user1,
    user2.nickname: user2,
    user3.nickname: user3
}

app = Flask(__name__)
app.secret_key = 'genshin' 

game_one = Jogo('Genshin', 'Adventure', 'PC')
game_two = Jogo('Elden Ring', 'RPG/Adventure', 'Xbox/PS5')
game_three = Jogo('Mario', 'Arcade', 'Nintendo')

lista = [game_one, game_two, game_three]

@app.route('/')
def index():
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
    
    #create object 
    game = Jogo(name=nome, category=categoria, console=console)
    lista.append(game)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def auth():
    if request.form['usuario'] in users:
        usuario = users[request.form['usuario']]
        if request.form['senha'] == usuario.password:
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