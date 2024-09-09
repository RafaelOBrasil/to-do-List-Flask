from flask import Flask, redirect, render_template, request, session, url_for
from datetime import date, datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "To-do List"


# Cadastrar Novo Usuario
@app.route("/cadastro")
def telaCadastro():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=["POST"])
def novoUsuario():
    nome_usuario = ""
    senha_usuario = ""
    csenha_usuario = ""


    if request.method == "POST":

        nome = request.form["usuario"]
        senha = request.form["senha"]
        csenha = request.form["csenha"]

        nome_usuario = nome
        senha_usuario = senha
        csenha_usuario = csenha


        if nome == "" or senha == "" or csenha == "":
            return render_template("Cadastro.html", erro="Preencha Todos os Campos", nome_usuario = nome_usuario, senha_usuario = senha_usuario, csenha_usuario = csenha_usuario)
        elif senha != csenha:
            return render_template("Cadastro.html", erro="Erro ao Validar as Senhas", nome_usuario = nome_usuario, senha_usuario = senha_usuario, csenha_usuario = csenha_usuario)
        else:
            con = sqlite3.connect("./db/to_do_list.db")
            cur = con.cursor()

            cur.execute("INSERT INTO USER (nome, senha) VALUES (?, ?)", (nome, senha))

            con.commit()
            con.close()

            return render_template("login.html", nome_usuario = nome_usuario, senha_usuario = senha_usuario)


# Logar Usuário
@app.route("/", methods=["POST", "GET"])

def validarLogin():
    nome_usuario = ""
    senha_usuario = ""

    if request.method == "POST":

        nome = request.form["usuario"]
        senha = request.form["senha"]

        nome_usuario = nome
        senha_usuario = senha

        # Conectar ao banco de dados
        con = sqlite3.connect("./db/to_do_list.db")
        cur = con.cursor()

        # Buscar o usuário
        cur.execute("SELECT * FROM USER WHERE nome = ? AND senha = ?", (nome, senha))
        usuario_logado = cur.fetchone()
        con.close()

        if usuario_logado:
            session["id_user"] = usuario_logado[0]
            return redirect(url_for("listaTarefas"))
        else:
            return render_template("login.html", erro = "Usuario ou senha Incorretos", nome_usuario = nome_usuario, senha_usuario = senha_usuario)

    return render_template("login.html", nome_usuario = nome_usuario, senha_usuario = senha_usuario)


# Listar tarefas do usuário logado
@app.route("/listaTarefas", methods=["GET"])
def listaTarefas():

    data = date.today()
    data_atual = data.strftime("%d/%m/%Y")

    if "id_user" not in session:
        return redirect(url_for("validarLogin"))

    id_user = session["id_user"]
    status = "Pendente"


    # Conectar ao banco de dados
    con = sqlite3.connect("./db/to_do_list.db")
    cur = con.cursor()

    # Buscar as tarefas do usuário
    cur.execute("SELECT * FROM TAREFAS WHERE id_usuario = ? AND status = ?", (id_user, status))
    tarefas = cur.fetchall()
    con.close()

    return render_template("listatarefas.html", tarefas=tarefas, data_atual = data_atual)


# Listar tarefas concluidas do usuário logado
@app.route("/listaTarefasConcluidas", methods=["GET"])
def listaTarefasConcluidas():

    id_user = session["id_user"]
    status = "Concluido"

    # Conectar ao banco de dados
    con = sqlite3.connect("./db/to_do_list.db")
    cur = con.cursor()

    # Buscar as tarefas do usuário
    cur.execute(
        "SELECT * FROM TAREFAS WHERE id_usuario = ? AND status = ?", (id_user, status)
    )
    tarefas = cur.fetchall()
    con.close()

    return render_template("listaConcluidas.html", tarefas=tarefas)


@app.route("/", methods=["POST"])
def deslogarUsuario():

    return redirect(url_for("login.html"))


# Nova tarefa
@app.route("/novaTarefa", methods=["POST", "GET"])
def novaTarefa():
    if request.method == "GET":
        data = date.today()
        data_atual = data.strftime("%d/%m/%Y")
        return render_template("novaTarefa.html", data_atual=data_atual)

    elif request.method == "POST":

        dataInf = request.form["data"]
        data_formatada = datetime.strptime(dataInf, "%Y-%m-%d").date()
        data_formatada = data_formatada.strftime("%d/%m/%Y")
        data = date.today()
        data_atual = data.strftime("%d/%m/%Y")

        if data_formatada < data_atual:
            return render_template(
                "novaTarefa.html", erro="A data de vencimento deve ser no futuro"
            )
        else:
            tituloInf = request.form["titulo"]
            descricaoInf = request.form["descricao"]
            dataInf = request.form["data"]
            data_formatada = datetime.strptime(dataInf, "%Y-%m-%d").date()
            data_formatada = data_formatada.strftime("%d/%m/%Y")

            status = request.form["status"]
            id_user = session["id_user"]

            con = sqlite3.connect("./db/to_do_list.db")
            cur = con.cursor()

            cur.execute(
                "INSERT INTO TAREFAS (titulo, descricao, data, status, id_usuario) VALUES (?, ?,?,?,?)",
                (tituloInf, descricaoInf, data_formatada, status, id_user),
            )
            data = date.today()
            data_atual = data.strftime("%d/%m/%Y")
            con.commit()
            con.close()

            status = "Pendente"
            # Conectar ao banco de dados
            con = sqlite3.connect("./db/to_do_list.db")
            cur = con.cursor()

            # Buscar as tarefas do usuário
            cur.execute("SELECT * FROM TAREFAS WHERE id_usuario = ? AND status = ?", (id_user, status))
            tarefas = cur.fetchall()
            con.close()

            return render_template("listatarefas.html", tarefas=tarefas, data_atual=data_atual)

# Deletar tarefa
@app.route("/deletar", methods=["POST"])
def deletarTarefa():
    if request.method == "POST":

        id_tarefa = request.form.get("id_tarefa")

        con = sqlite3.connect("./db/to_do_list.db")
        cur = con.cursor()

        cur.execute("DELETE FROM TAREFAS WHERE id = ?", (id_tarefa,))

        con.commit()
        con.close()

    data = date.today()
    data_atual = data.strftime("%d/%m/%Y")
    id_user = session["id_user"]

    # Conectar ao banco de dados
    con = sqlite3.connect("./db/to_do_list.db")
    cur = con.cursor()

    # Buscar as tarefas do usuário
    cur.execute("SELECT * FROM TAREFAS WHERE id_usuario = ?", (id_user,))
    tarefas = cur.fetchall()
    con.close()

    return render_template("listatarefas.html", tarefas=tarefas,data_atual=data_atual)


# Concluir tarefa
@app.route("/Concluir", methods=["POST"])
def concluirTarefa():

    if request.method == "POST":

        data_tarefa = request.form.get("data_tarefa")
        data = date.today()
        data_atual = data.strftime("%d/%m/%Y")

        #Apenas não marca como concluido se o prazo vencer.
        if data_atual < data_tarefa:
            id_tarefa = request.form.get("id_tarefa")
            status = "Concluido"

            con = sqlite3.connect("./db/to_do_list.db")
            cur = con.cursor()

            cur.execute("UPDATE TAREFAS SET status = ? WHERE id = ?", (status, id_tarefa))

            con.commit()
            con.close()
        else:
            id_user = session["id_user"]
            status = "Pendente"

            # Conectar ao banco de dados
            con = sqlite3.connect("./db/to_do_list.db")
            cur = con.cursor()

            # Buscar as tarefas do usuário
            cur.execute("SELECT * FROM TAREFAS WHERE id_usuario = ? AND status = ?", (id_user, status))
            tarefas = cur.fetchall()
            con.close()

            return render_template("listatarefas.html", tarefas=tarefas,data_atual=data_atual)
                
    id_user = session["id_user"]
    status = "Pendente"

    # Conectar ao banco de dados
    con = sqlite3.connect("./db/to_do_list.db")
    cur = con.cursor()

    # Buscar as tarefas do usuário
    cur.execute("SELECT * FROM TAREFAS WHERE id_usuario = ? AND status = ?", (id_user, status))
    tarefas = cur.fetchall()
    con.close()

    return render_template("listatarefas.html", tarefas=tarefas, data_atual=data_atual)
