from flask import Flask, redirect, render_template, request
import psycopg2

app = Flask(__name__)

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="Games",
        user="postgres",
        password="senai",
        port="5432")
    return banco

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/jogo')
def jogos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, titulo, plataforma, ano, preco FROM jogo ORDER BY id")
    lista = cursor.fetchall()
    banco.close()
    return render_template("jogos.html", jogo=lista)

@app.route('/jogo/enviar', methods=['POST'])
def enviar_jogo():
    titulo = request.form.get('titulo')
    plataforma = request.form.get('plataforma')
    ano = request.form.get('ano')
    preco = request.form.get('preco')
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO jogo (titulo, plataforma, ano, preco) VALUES (%s, %s, %s, %s)""", (titulo, plataforma, ano, preco))
    banco.commit()
    banco.close()
    return redirect('/jogo')

@app.route('/jogo/editar/<int:id>')
def editar_jogo(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, titulo, plataforma, ano, preco FROM jogo WHERE id = %s", (id,))
    jogo = cursor.fetchone()
    banco.close()

    if jogo is None:
        return redirect('/jogo')
    return render_template("editar_jogo.html", jogo=jogo)

@app.route('/jogo/atualizar/<int:id>', methods=['POST'])
def atualizar_jogo(id):
    titulo = request.form.get('titulo')
    plataforma = request.form.get('plataforma')
    ano = request.form.get('ano')
    preco = request.form.get('preco')
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE jogo SET titulo = %s, plataforma = %s, ano = %s, preco = %s WHERE id = %s""", (titulo, plataforma, ano, preco, id))
    banco.commit()
    banco.close()
    return redirect('/jogo')

@app.route('/jogo/excluir/<int:id>', methods=['POST'])
def excluir_jogo(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""DELETE FROM jogo WHERE id = %s""", (id,))
    banco.commit()
    banco.close()
    return redirect('/jogo')



@app.route('/jogadores')
def jogadores():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, nick, email, nivel, data_cadastro FROM jogador ORDER BY id")
    lista = cursor.fetchall()
    banco.close()
    return render_template("jogadores.html", jogadores=lista)

@app.route('/jogadores/enviar', methods=['POST'])
def enviar_jogador():
    nick = request.form.get('nick')
    email = request.form.get('email')
    nivel = request.form.get('nivel')
    data_cadastro = request.form.get('data_cadastro')
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO jogador (nick, email, nivel, data_cadastro) VALUES (%s, %s, %s, %s)""", (nick, email, nivel, data_cadastro))
    banco.commit()
    banco.close()
    return redirect('/jogadores')

@app.route('/jogadores/editar/<int:id>')
def editar_jogador(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, nick, email, nivel, data_cadastro FROM jogador WHERE id = %s", (id,))
    jogador = cursor.fetchone()
    banco.close()

    if jogador is None:
        return redirect('/jogadores')
    return render_template("editar_jogador.html", jogador=jogador)

@app.route('/jogadores/atualizar/<int:id>', methods=['POST'])
def atualizar_jogador(id):
    nick = request.form.get('nick')
    email = request.form.get('email')
    nivel = request.form.get('nivel')
    data_cadastro = request.form.get('data_cadastro')
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE jogador SET nick = %s, email = %s, nivel = %s, data_cadastro = %s WHERE id = %s""", (nick, email, nivel, data_cadastro, id))
    banco.commit()
    banco.close()
    return redirect('/jogadores')

@app.route('/jogadores/excluir/<int:id>', methods=['POST'])
def excluir_jogador(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""DELETE FROM jogador WHERE id = %s""", (id,))
    banco.commit()
    banco.close()
    return redirect('/jogadores')


if __name__ == '__main__':
    app.run()