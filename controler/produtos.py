
from flask import render_template, request, url_for, redirect, Blueprint, Response
import flask
import json
from models.produtos import db, Product, Category

app = Blueprint("produtos", __name__)

# ROOT


@app.route("/", methods=['GET', 'POST'])
def root():
    produto = Product.query.all()
    print(produto)
    categoria = Category.query.all()
    tabela = "Produtos"
    action_button = "/"
    resultado = [p.to_dict() for p in produto]
    if request.method == "POST":
        tabela = request.form.get("table")
        if request.form.get("add_prod") == "Adicionar":
            return redirect(url_for("produtos.page_adicionar", tabela="Produtos"))
        elif request.form.get("add_cat") == "Adicionar":
            return redirect(url_for("produtos.page_adicionar", tabela="Categoria"))

    return render_template('index.html', produtos=produto, tabela=tabela, categorias=categoria, action_button=action_button)


# Page Adicionar
@app.route("/add", methods=['GET', 'POST'])
def page_adicionar():
    tipo_tabela = request.args.get('tabela')
    print(tipo_tabela)
    categoria = Category.query.all()
    action_button = "/add"
    form_id_prod = ["nome_produto", "codigo_produto",
                    "qualidade_produto", "disponibilidade_produto", "categoria_produto"]
    form_label = ["Nome do Produto", "Código do Produto", "Qualidade do Produto",
                  "Disponibilidade do produto", "Categoria do produto"]
    form = zip(form_id_prod, form_label)
    title = "ADICIONAR PRODUTO"

    if request.method == "POST":

        if request.form.get("table") == "Produtos":
            tipo_tabela = "Produtos"
            return render_template("adicionar.html", form=form, tipo_tabela=tipo_tabela, action_button=action_button, categorias=categoria, title=title)
        elif request.form.get("table") == "Categoria":
            tipo_tabela = "Categoria"
            title = "ADICIONAR CATEGORIA"
            return render_template("adicionar.html", form=form, tipo_tabela=tipo_tabela, action_button=action_button, categorias=categoria, title=title)
        else:
            return render_template("adicionar.html", form=form, tipo_tabela=tipo_tabela, action_button=action_button, categorias=categoria, title=title)

    return render_template("adicionar.html", form=form, tipo_tabela=tipo_tabela, action_button=action_button, categorias=categoria, title=title)


# Pagina para adicionar produto
@app.route("/adicionar_produto", methods=["GET", "POST", "PUT"])
def add_produto():
    if request.method == "POST":
        produto = Product(request.form.get("nome_produto"), request.form.get("codigo_produto"), request.form.get(
            "qualidade_produto"), request.form.get("disponibilidade_produto"), request.form.get("categoria_produto"))

        db.session.add(produto)
        db.session.commit()
    return redirect(url_for("produtos.root"))


# EDIT PRODUTO
@app.route("/edit/produto/<int:id>", methods=['GET', 'POST', "PUT"])
def edit_produto(id):
    title = "EDITAR PRODUTO"
    produto = Product.query.get(id)
    categoria = Category.query.all()
    action_button = "/add"
    form_id_prod = ["nome_produto", "codigo_produto",
                    "qualidade_produto", "disponibilidade_produto", "categoria_produto"]
    form_label = ["Nome do Produto", "Código do Produto", "Qualidade do Produto",
                  "Disponibilidade do produto", "Categoria do produto"]
    form = zip(form_id_prod, form_label)
    tipo_tabela = "Produtos"

    if request.method == "POST":
        produto.nome_produto = request.form["nome_produto"]
        produto.code_produto = request.form.get("codigo_produto")
        produto.quality_produto = request.form.get("qualidade_produto")
        produto.is_active_produto = request.form.get("disponibilidade_produto")
        produto.category_id = request.form.get("categoria_produto")
        if produto.is_active_produto == "True":
            produto.is_active_produto = 1
        elif produto.is_active_produto == None:
            produto.is_active_produto = 0

        db.session.commit()

        return redirect(url_for("produtos.root"))
    return render_template("edit.html", form=form, tipo_tabela=tipo_tabela, action_button=action_button, categorias=categoria, produto=produto, title=title)


# EXCLUIR PRODUTO
@app.route("/excluir/produto/<int:id>", methods=['GET', 'POST', "DELETE"])
def del_produto(id):
    produto = Product.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for("produtos.root"))


# Pagina para adicionar categoria
@app.route("/adicionar_categoria", methods=["GET", "POST", "PUT"])
def add_categoria():
    if request.method == "POST":
        print(request.form.get("nome_categoria"))
        categ = Category(request.form.get("nome_categoria"))
        db.session.add(categ)
        db.session.commit()
    return redirect(url_for("produtos.root"))


# EDIT CATEGORIA
@app.route("/edit/categoria/<int:id>", methods=['GET', 'POST', "PUT"])
def edit_categoria(id):
    categoria = Category.query.get(id)
    title = "EDITAR CATEGORIA"
    tipo_tabela = "Categoria"
    action_button = "/add"
    if request.method == "POST":
        categoria.nome_categoria = request.form.get("nome_categoria")
        db.session.commit()
        return redirect(url_for("produtos.root"))

    return render_template("edit.html", tipo_tabela=tipo_tabela, action_button=action_button, categoria=categoria, title=title)


# EXCLUIR CATEGORIA
@app.route("/excluir/categoria/<int:id>", methods=['GET', 'POST', "DELETE"])
def del_category(id):
    categoria = Category.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for("produtos.root"))
