from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models.models import ItemCardapio
from app.forms.addCardapio import ItemForm

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

@bp.route('/cardapio/adicionar', methods=['GET', 'POST'])
def adicionar():
    form = ItemForm()
    if form.validate_on_submit():
        try:
            novo_item = ItemCardapio(
                nome_item=form.nome_item.data,
                preco=form.preco_item.data,
                descricao=form.descricao_item.data
            )

            db.session.add(novo_item)
            db.session.commit()

            flash('Item adicionado com sucesso!', 'success')
            return redirect(url_for('main.listagem'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao adicionar o item: {str(e)}', 'error')

    return render_template('cardapio/adicionar.html', form=form, active_page='cardapio')


@bp.route('/cardapio/listagem')
def listagem():
    itens = ItemCardapio.query.all()
    return render_template('cardapio/listagem.html', itens=itens, active_page='cardapio')

@bp.route('/cardapio/editar/<int:id>', methods=['GET', 'POST'])
def editar_item(id):
    item = ItemCardapio.query.get_or_404(id)
    form = ItemForm(obj=item)
    
    if form.validate_on_submit():
        item.nome_item = form.nome_item.data
        item.preco = form.preco_item.data
        item.descricao = form.descricao_item.data
        item.disponivel = form.disponivel.data
        db.session.commit()
        flash('Item atualizado com sucesso!', 'success')
        return redirect(url_for('main.listagem'))
    
    return render_template('cardapio/editar.html', form=form, item=item, active_page='cardapio')

@bp.route('/cardapio/excluir/<int:id>', methods=['POST'])
def excluir_item(id):
    item = ItemCardapio.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Item excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao excluir o item: {str(e)}', 'error')
    return redirect(url_for('main.listagem'))

# Rota de busca para search-bar da tela de listagem

@bp.route('/buscar_itens')
def buscar_itens():
    query = request.args.get('q', '', type=str)
    if query:
        itens = ItemCardapio.query.filter(ItemCardapio.nome_item.ilike(f'%{query}%')).all()
    else:
        itens = ItemCardapio.query.all()

    itens_data = [
        {
            'id_item': item.id_item,
            'nome_item': item.nome_item,
            'descricao': item.descricao,
            'preco': f'{item.preco:.2f}',
            'disponivel': 'Sim' if item.disponivel else 'Não'
        }
        for item in itens
    ]

    return jsonify(itens_data)




