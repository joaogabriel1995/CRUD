from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column('Nome do Produto', db.String(150))
    code_produto = db.Column('Codigo do Produto', db.String(150))
    quality_produto = db.Column('Qualidade do Produto', db.String(150))
    is_active_produto = db.Column(
        'Produto ativo', db.Boolean, default=False, nullable=False)
    category_id = db.Column("Categoria_id", db.Integer,
                            db.ForeignKey("category.id"))

    def __init__(self, nome_produto, code_produto, quality_produto, is_active_produto, category_id):

        self.nome_produto = nome_produto
        self.code_produto = code_produto
        self.quality_produto = quality_produto
        self.is_active_produto = self.to_bolean(is_active_produto)
        self.category_id = category_id

    def to_dict(self, columns=[]):
        if not columns:
            return {"id": self.id, "nome_produto": self.nome_produto, "code_produto": self.code_produto, "quality_produto": self.quality_produto, "is_active_produto": self.is_active_produto, "category_id": self.category_id}
        else:
            return {col: getattr(self, col) for col in columns}

    def to_bolean(self, variavel):
        if variavel == "1":
            variavel = 1
            return variavel
        elif variavel == "None":
            variavel = 0
            return variavel

        return


class Category(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome_categoria = db.Column('Nome da categoria', db.String(150))
    fore_key = db.relationship('Product', backref="category")

    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria
