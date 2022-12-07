import random
from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('DOOM', 'FPS', 'PS4')
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "123")

usuarios = {usuario1.nickname: usuario1, usuario2.nickname: usuario2, usuario3.nickname: usuario3}

app = Flask(__name__)

def secret_key():
    """Cria a chave secreta para a session"""
    lista_parte_chave=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','y','w','z']
    lista_parte_chave2=['!','@','#','$','%','&','*','?']
    a = random.choice(lista_parte_chave)
    b = random.randint(1000000000, 9000000000)
    c = random.choice(lista_parte_chave)
    d = random.choice(lista_parte_chave2)
    key = str(a) + str(d) + str(b) + str(c)
    return key

app.secret_key = secret_key()

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=["POST",])
def criar():
    """
    rota que irá enviar os parâmetros do form contido em novo.html para a lista,
    e redirecionará para lista.html, que irá conter a nova informação cadastrada
    """
    # request pega a informação da tag que contém o atributo nome definido
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    """Rota do login"""
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    """Autentica dados do login"""
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ', você foi logado com sucesso!', )
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Falha ao efetuar login')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Efetua o logout do usuário"""
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))


app.run(debug=True)
# app.run(host='0.0.0.0', port=8080)
# definição manual de porta e host
# pode ser deixado em branco, o exemplo é para fins de desenvolvimento e não de produção

