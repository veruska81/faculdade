from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect

aplicativo = Flask(__name__)
#aplicativo.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:toledo22@localhost:3306/mydb'
aplicativo.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://branquinhodiogo:toledo22@branquinhodiogo.mysql.pythonanywhere-services.com:3306/branquinhodiogo$mydb'
aplicativo.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

banco_dados = SQLAlchemy(aplicativo)

class UsuarioModelo(banco_dados.Model):
    __tablename__ = "usuario"
    identificador = banco_dados.Column('usu_id', banco_dados.Integer, primary_key=True)
    nome_usuario = banco_dados.Column('usu_nome', banco_dados.String(256))
    email_usuario = banco_dados.Column('usu_email', banco_dados.String(256))
    senha_usuario = banco_dados.Column('usu_senha', banco_dados.String(256))
    endereco_usuario = banco_dados.Column('usu_endereco', banco_dados.String(256))

    def __init__(self, nome_usuario, email_usuario, senha_usuario, endereco_usuario):
        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.senha_usuario = senha_usuario
        self.endereco_usuario = endereco_usuario

class CategoriaModelo(banco_dados.Model):
    __tablename__ = "categoria"
    identificador = banco_dados.Column('cat_id', banco_dados.Integer, primary_key=True)
    nome_categoria = banco_dados.Column('cat_nome', banco_dados.String(256))
    descricao_categoria = banco_dados.Column('cat_descricao', banco_dados.String(256))

    def __init__ (self, nome_categoria, descricao_categoria):
        self.nome_categoria = nome_categoria
        self.descricao_categoria = descricao_categoria

class AnuncioModelo(banco_dados.Model):
    __tablename__ = "anuncio"
    identificador = banco_dados.Column('anu_id', banco_dados.Integer, primary_key=True)
    nome_anuncio = banco_dados.Column('anu_nome', banco_dados.String(256))
    descricao_anuncio = banco_dados.Column('anu_descricao', banco_dados.String(256))
    quantidade_anuncio = banco_dados.Column('anu_qtd', banco_dados.Integer)
    preco_anuncio = banco_dados.Column('anu_preco', banco_dados.Float)
    categoria_id = banco_dados.Column('cat_id', banco_dados.Integer, banco_dados.ForeignKey("categoria.cat_id"))
    usuario_id = banco_dados.Column('usu_id', banco_dados.Integer, banco_dados.ForeignKey("usuario.usu_id"))

    def __init__(self, nome_anuncio, descricao_anuncio, quantidade_anuncio, preco_anuncio, categoria_id, usuario_id):
        self.nome_anuncio = nome_anuncio
        self.descricao_anuncio = descricao_anuncio
        self.quantidade_anuncio = quantidade_anuncio
        self.preco_anuncio = preco_anuncio
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id

@aplicativo.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('pagina_nao_encontrada.html')

@aplicativo.route("/")
def pagina_inicial():
    return render_template('index.html')

@aplicativo.route("/cadastro/usuario")
def pagina_usuario():
    return render_template('usuario.html', usuarios=UsuarioModelo.query.all(), titulo="Usuario")

@aplicativo.route("/usuario/criar", methods=['POST'])
def criar_usuario():
    novo_usuario = UsuarioModelo(request.form.get('user'), request.form.get('email'), request.form.get('senha'), request.form.get('endereco'))
    banco_dados.session.add(novo_usuario)
    banco_dados.session.commit()
    return redirect(url_for('pagina_usuario'))

@aplicativo.route("/usuario/detalhar/<int:identificador>")
def buscar_usuario(identificador):
    usuario = UsuarioModelo.query.get(identificador)
    return usuario.nome_usuario

@aplicativo.route("/usuario/editar/<int:identificador>", methods=['GET','POST'])
def editar_usuario(identificador):
    usuario = UsuarioModelo.query.get(identificador)
    if request.method == 'POST':
        usuario.nome_usuario = request.form.get('user')
        usuario.email_usuario = request.form.get('email')
        usuario.senha_usuario = request.form.get('senha')
        usuario.endereco_usuario = request.form.get('endereco')
        banco_dados.session.add(usuario)
        banco_dados.session.commit()
        return redirect(url_for('pagina_usuario'))

    return render_template('editar_usuario.html', usuario=usuario, titulo="Usuario")

@aplicativo.route("/usuario/deletar/<int:identificador>")
def deletar_usuario(identificador):
    usuario = UsuarioModelo.query.get(identificador)
    banco_dados.session.delete(usuario)
    banco_dados.session.commit()
    return redirect(url_for('pagina_usuario'))

@aplicativo.route("/cadastro/anuncio")
def pagina_anuncio():
    return render_template('anuncio.html', anuncios=AnuncioModelo.query.all(), categorias=CategoriaModelo.query.all(), titulo="Anuncio")

@aplicativo.route("/anuncio/criar", methods=['POST'])
def criar_anuncio():
    novo_anuncio = AnuncioModelo(request.form.get('nome'), request.form.get('descricao'), request.form.get('qtd'), request.form.get('preco'), request.form.get('cat'), request.form.get('uso'))
    banco_dados.session.add(novo_anuncio)
    banco_dados.session.commit()
    return redirect(url_for('pagina_anuncio'))

@aplicativo.route("/anuncios/pergunta")
def pagina_pergunta():
    return render_template('pergunta.html')

@aplicativo.route("/anuncios/compra")
def realizar_compra():
    print("Anuncio comprado")
    return ""

@aplicativo.route("/anuncio/favoritos")
def pagina_favoritos():
    print("Favorito inserido")
    return f"<h4>Comprado</h4>"

@aplicativo.route("/configuracao/categoria")
def pagina_categoria():
    return render_template('categoria.html', categorias=CategoriaModelo.query.all(), titulo='Categoria')

@aplicativo.route("/categoria/criar", methods=['POST'])
def criar_categoria():
    nova_categoria = CategoriaModelo(request.form.get('nome'), request.form.get('descricao'))
    banco_dados.session.add(nova_categoria)
    banco_dados.session.commit()
    return redirect(url_for('pagina_categoria'))

@aplicativo.route("/relatorios/vendas")
def relatorio_vendas():
    return render_template('relatorio_vendas.html')

@aplicativo.route("/relatorios/compras")
def relatorio_compras():
    return render_template('relatorio_compras.html')

if __name__ == 'BBB':
    banco_dados.create_all()
    aplicativo.run()
