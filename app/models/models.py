from app import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Modelo para a tabela itens_cardapio
class ItemCardapio(db.Model):
    __tablename__ = 'itens_cardapio'
    id_item = Column(Integer, primary_key=True)
    nome_item = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco = Column(db.Numeric(10, 2), nullable=False)
    disponivel = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=func.now())
    ultima_atualizacao = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<ItemCardapio(id_item={self.id_item}, nome_item={self.nome_item}, preco={self.preco})>"

# Modelo para a tabela pedidos
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=True)  # Nome do cliente pode ser NULL
    numero_mesa = db.Column(db.Integer, db.ForeignKey('mesas.numero_mesa'), nullable=True)  # Chave estrangeira para a tabela de mesas
    status = db.Column(db.String(50), nullable=False, default='Pendente')
    data_pedido = db.Column(db.DateTime, default=db.func.now())
    total_pedido = db.Column(db.Float, nullable=False, default=0.0)  # Coluna total do pedido, iniciando com valor 0.0

    # Relacionamento com a tabela 'Mesa'
    mesa = db.relationship('Mesa', back_populates='pedidos')
    
    # Relacionamento com a tabela itens_pedido
    itens_pedido = db.relationship('ItemPedido', back_populates='pedido')
    
    # Relacionamento com feedback (opcional), define que cada pedido pode ter um feedback
    feedback = db.relationship('Feedback', uselist=False, back_populates='pedido')

    def __repr__(self):
        return f"<Pedido(id_pedido={self.id_pedido}, nome_cliente={self.nome_cliente}, status={self.status}, total_pedido={self.total_pedido})>"


# Modelo para a tabela itens_pedido
class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id_item_pedido = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'), nullable=False)  # Referência para o pedido
    id_item = Column(Integer, ForeignKey('itens_cardapio.id_item'), nullable=False)  # Referência para o item do cardápio
    quantidade = Column(Integer, nullable=False)  # Quantidade do item no pedido
    preco_item = Column(db.Numeric(10, 2), nullable=False)  # Preço do item no momento do pedido
    
    # Relacionamento com a tabela pedidos
    pedido = relationship('Pedido', back_populates='itens_pedido')
    
    # Relacionamento com a tabela itens_cardapio
    item = relationship('ItemCardapio')

    def __repr__(self):
        return f"<ItemPedido(id_item_pedido={self.id_item_pedido}, id_pedido={self.id_pedido}, id_item={self.id_item}, quantidade={self.quantidade})>"

# Modelo para a tabela mesas
class Mesa(db.Model):
    __tablename__ = 'mesas'
    numero_mesa = db.Column(db.Integer, primary_key=True)
    status_mesa = db.Column(db.String(50), nullable=False)

    # Relacionamento com a tabela 'Pedido'
    pedidos = db.relationship('Pedido', back_populates='mesa')

    def __repr__(self):
        return f"<Mesa(numero_mesa={self.numero_mesa}, status_mesa={self.status_mesa})>"

# Modelo para a tabela feedback
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id_feedback = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'))
    nota = Column(Text, nullable=True)

    pedido = relationship('Pedido', back_populates='feedback')

    def __repr__(self):
        return f"<Feedback(id_feedback={self.id_feedback}, id_pedido={self.id_pedido})>"

## Modelo atualizado para a tabela relatorios_vendas
class RelatorioVendas(db.Model):
    __tablename__ = 'relatorios_vendas'
    
    id_relatorio = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    total_vendas = Column(db.Numeric(10, 2), nullable=False)
    total_pedidos = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<RelatorioVendas(id_relatorio={self.id_relatorio}, data_inicio={self.data_inicio}, data_fim={self.data_fim}, total_vendas={self.total_vendas}, total_pedidos={self.total_pedidos})>"

class Item(db.Model):
    id_item = db.Column(db.Integer, primary_key=True)
    nome_item = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
