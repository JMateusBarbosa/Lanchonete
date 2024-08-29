from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('index.html', active_page='home')

@bp.route('/cardapio')
def cardapio():
    return render_template('cardapio/cardapio.html', active_page='cardapio')

@bp.route('/anotar_pedido')
def anotar_pedido():
    return render_template('anotar_pedido.html', active_page='anotar_pedido')

@bp.route('/acompanhar_pedidos')
def acompanhar_pedidos():
    return render_template('acompanhar_pedidos.html', active_page='acompanhar_pedidos')

@bp.route('/relatorios_vendas')
def relatorios_vendas():
    return render_template('relatorios_vendas.html', active_page='relatorios_vendas')

#Telas do cardapio

@bp.route('/cardapio/adicionar')
def adicionar():
    return render_template('cardapio/adicionar.html', active_page='cardapio')

@bp.route('/cardapio/listagem')
def listagem():
    return render_template('cardapio/listagem.html', active_page='cardapio')