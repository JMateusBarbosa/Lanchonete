# models.py

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
    id_pedido = Column(Integer, primary_key=True)
    nome_cliente = Column(String(100), nullable=True)
    numero_mesa = Column(Integer, ForeignKey('mesas.numero_mesa'))
    status = Column(Enum('Pendente', 'Em Preparação', 'Concluído'), default='Pendente')
    data_pedido = Column(DateTime, default=func.now())

    mesa = relationship('Mesa', back_populates='pedidos')
    itens_pedido = relationship('ItemPedido', back_populates='pedido')
    feedback = relationship('Feedback', uselist=False, back_populates='pedido')

    def __repr__(self):
        return f"<Pedido(id_pedido={self.id_pedido}, nome_cliente={self.nome_cliente}, status={self.status})>"

# Modelo para a tabela itens_pedido
class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id_item_pedido = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'))
    id_item = Column(Integer, ForeignKey('itens_cardapio.id_item'))
    quantidade = Column(Integer, nullable=False)
    preco_item = Column(db.Numeric(10, 2), nullable=False)

    pedido = relationship('Pedido', back_populates='itens_pedido')
    item = relationship('ItemCardapio')

    def __repr__(self):
        return f"<ItemPedido(id_item_pedido={self.id_item_pedido}, id_pedido={self.id_pedido}, id_item={self.id_item}, quantidade={self.quantidade})>"

# Modelo para a tabela mesas
class Mesa(db.Model):
    __tablename__ = 'mesas'
    numero_mesa = Column(Integer, primary_key=True)
    status_mesa = Column(String(50), nullable=False)

    pedidos = relationship('Pedido', back_populates='mesa')

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

# Modelo para a tabela relatorios_vendas
class RelatorioVendas(db.Model):
    __tablename__ = 'relatorios_vendas'
    id_relatorio = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    total_vendas = Column(db.Numeric(10, 2), nullable=True)

    def __repr__(self):
        return f"<RelatorioVendas(id_relatorio={self.id_relatorio}, data_inicio={self.data_inicio}, data_fim={self.data_fim})>"

