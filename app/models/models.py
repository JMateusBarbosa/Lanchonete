from app import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# =============================================================================
# MODELO: ItemCardapio
# Representa os itens do cardápio, incluindo detalhes como nome, preço e disponibilidade.
# =============================================================================
class ItemCardapio(db.Model):
    __tablename__ = 'itens_cardapio'  # Nome da tabela no banco de dados.

    # Campos da tabela
    id_item = Column(Integer, primary_key=True)  # Identificador único.
    nome_item = Column(String(100), nullable=False)  # Nome do item (obrigatório).
    descricao = Column(Text)  # Descrição opcional do item.
    preco = Column(db.Numeric(10, 2), nullable=False)  # Preço do item (obrigatório).
    disponivel = Column(Boolean, default=True)  # Indica se o item está disponível no cardápio.
    data_criacao = Column(DateTime, default=func.now())  # Data de criação automática.
    ultima_atualizacao = Column(DateTime, onupdate=func.now())  # Atualizado automaticamente em cada modificação.

    # Método para representação amigável do objeto no terminal
    def __repr__(self):
        return f"<ItemCardapio(id_item={self.id_item}, nome_item={self.nome_item}, preco={self.preco})>"

# =============================================================================
# MODELO: Pedido
# Representa os pedidos realizados, vinculados a mesas e itens do cardápio.
# =============================================================================
class Pedido(db.Model):
    __tablename__ = 'pedidos'

    # Campos da tabela
    id_pedido = Column(Integer, primary_key=True)  # Identificador único do pedido.
    nome_cliente = Column(String(100), nullable=True)  # Nome do cliente (opcional).
    numero_mesa = Column(Integer, ForeignKey('mesas.numero_mesa'), nullable=True)  # Referência à mesa (opcional).
    status = Column(String(50), nullable=False, default='Pendente')  # Status do pedido.
    data_pedido = Column(DateTime, default=func.now())  # Data do pedido.
    total_pedido = Column(db.Float, nullable=False, default=0.0)  # Total calculado do pedido.

    # Relacionamentos
    mesa = relationship('Mesa', back_populates='pedidos')  # Associação com a tabela de mesas.
    itens_pedido = relationship('ItemPedido', back_populates='pedido')  # Itens do pedido.
    feedback = relationship('Feedback', uselist=False, back_populates='pedido')  # Feedback único opcional.

    def __repr__(self):
        return f"<Pedido(id_pedido={self.id_pedido}, status={self.status}, total_pedido={self.total_pedido})>"

# =============================================================================
# MODELO: ItemPedido
# Representa os itens associados a um pedido, armazenando detalhes como quantidade e preço.
# =============================================================================
class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'

    # Campos da tabela
    id_item_pedido = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'), nullable=False)  # Pedido ao qual o item pertence.
    id_item = Column(Integer, ForeignKey('itens_cardapio.id_item'), nullable=False)  # Item do cardápio.
    quantidade = Column(Integer, nullable=False)  # Quantidade solicitada.
    preco_item = Column(db.Numeric(10, 2), nullable=False)  # Preço do item no momento do pedido.

    # Relacionamentos
    pedido = relationship('Pedido', back_populates='itens_pedido')  # Associação com o pedido.
    item = relationship('ItemCardapio')  # Associação com o item do cardápio.

    def __repr__(self):
        return f"<ItemPedido(id_item_pedido={self.id_item_pedido}, id_pedido={self.id_pedido}, id_item={self.id_item})>"

# =============================================================================
# MODELO: Mesa
# Representa as mesas do estabelecimento, associadas a pedidos.
# =============================================================================
class Mesa(db.Model):
    __tablename__ = 'mesas'

    # Campos da tabela
    numero_mesa = Column(Integer, primary_key=True)  # Número único da mesa.
    status_mesa = Column(String(50), nullable=False)  # Status atual da mesa.

    # Relacionamentos
    pedidos = relationship('Pedido', back_populates='mesa')  # Associação com pedidos feitos na mesa.

    def __repr__(self):
        return f"<Mesa(numero_mesa={self.numero_mesa}, status_mesa={self.status_mesa})>"

# =============================================================================
# MODELO: Feedback
# Representa os feedbacks associados a pedidos específicos.
# =============================================================================
class Feedback(db.Model):
    __tablename__ = 'feedback'

    # Campos da tabela
    id_feedback = Column(Integer, primary_key=True)  # Identificador único do feedback.
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'))  # Pedido ao qual o feedback pertence.
    nota = Column(Text, nullable=True)  # Texto opcional contendo a avaliação.

    # Relacionamento
    pedido = relationship('Pedido', back_populates='feedback')  # Associação com o pedido.

    def __repr__(self):
        return f"<Feedback(id_feedback={self.id_feedback}, id_pedido={self.id_pedido})>"

# =============================================================================
# MODELO: RelatorioVendas
# Armazena informações de relatórios de vendas para análise de dados.
# =============================================================================
class RelatorioVendas(db.Model):
    __tablename__ = 'relatorios_vendas'

    # Campos da tabela
    id_relatorio = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime, nullable=False)  # Período inicial do relatório.
    data_fim = Column(DateTime, nullable=False)  # Período final do relatório.
    total_vendas = Column(db.Numeric(10, 2), nullable=False)  # Total arrecadado no período.
    total_pedidos = Column(Integer, nullable=False)  # Total de pedidos realizados.

    def __repr__(self):
        return f"<RelatorioVendas(id_relatorio={self.id_relatorio}, data_inicio={self.data_inicio}, total_vendas={self.total_vendas})>"
