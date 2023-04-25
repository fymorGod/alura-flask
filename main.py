from flask import Flask, render_template, request, redirect, session, flash
class Jogo:
    def __init__(self, name:str, category:str, console:str):
        self.name = name
        self.category = category
        self.console = console

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
        return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
    #create object 
    game = Jogo(name=nome, category=categoria, console=console)
    lista.append(game)
    return redirect('/')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def auth():
    if 'alohomora' == request.form['senha']:
      session['user'] = request.form['usuario']
      flash(session['user'] + ' authentication sucesses!')
      next_page = request.form['proxima']
      return redirect('/{}'.format(next_page))
    else:
      flash('User is not authenticated')        
      return redirect('/login')    
    
@app.route('/logout')
def logout():
    session['user'] = None
    flash('User is left!')
    return redirect('/')

app.run(debug=True, host='0.0.0.0', port=8080)