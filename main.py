from flask import Flask, render_template, request, redirect

class Jogo:
    def __init__(self, name:str, category:str, console:str):
        self.name = name
        self.category = category
        self.console = console

app = Flask(__name__)

game_one = Jogo('Genshin', 'Adventure', 'PC')
game_two = Jogo('Elden Ring', 'RPG/Adventure', 'Xbox/PS5')
game_three = Jogo('Mario', 'Arcade', 'Nintendo')

lista = [game_one, game_two, game_three]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
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

app.run(debug=True, host='0.0.0.0', port=8080)