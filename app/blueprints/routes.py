from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app import db
from app.models.models import Pedido, ItemPedido, ItemCardapio, Feedback, Mesa, RelatorioVendas
from app.forms.addCardapio import ItemForm
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app import csrf
from datetime import datetime
import locale

bp = Blueprint('main', __name__)

# Defina a localidade para formatação em Real (R$)
#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('index.html', active_page='home')

@bp.route('/cardapio')
def cardapio():
    return render_template('cardapio/cardapio.html', active_page='cardapio')

# Tela anotar pedido
@bp.route('/anotar-pedido', methods=['GET', 'POST'])
def anotar_pedido():
    if request.method == 'POST':
        data = request.json
        
        # Coletando os dados
        customer_name = data.get('customer_name')
        table_number = data.get('table_number')
        feedback = data.get('feedback')
        items = data.get('items')
        total_pedido = data.get('total_pedido', 0.0)

        customer_name = customer_name if customer_name else None
        table_number = table_number if table_number else None

        # Criar um novo pedido com total_pedido
        pedido = Pedido(
            nome_cliente=customer_name, 
            numero_mesa=table_number, 
            status='Pendente',
            total_pedido=total_pedido  
        )
        db.session.add(pedido)
        db.session.commit()
        
        # Adicionar itens ao pedido
        for item in items:
            item_id = item['itemId']
            quantity = item['quantity']
            item_cardapio = ItemCardapio.query.get(item_id)
            item_pedido = ItemPedido(
                id_pedido=pedido.id_pedido, 
                id_item=item_id, 
                quantidade=quantity, 
                preco_item=item_cardapio.preco
            )
            db.session.add(item_pedido)
        
        if feedback:
            feedback_record = Feedback(id_pedido=pedido.id_pedido, nota=feedback)
            db.session.add(feedback_record)
        
        db.session.commit()
        
        return jsonify({'success': True})
    
    # GET request
    try:
        mesas = Mesa.query.all()
        itens = ItemCardapio.query.all()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        # Dados fictícios em caso de falha
        mesas = [{'numero_mesa': '1'}, {'numero_mesa': '2'}]
        itens = [{'id_item': 1, 'nome_item': 'Item Fictício 1'}, {'id_item': 2, 'nome_item': 'Item Fictício 2'}]
    
    return render_template('anotar_pedido.html', active_page='anotar_pedido', mesas=mesas, itens=itens)


# Rota para  retornar o preço dos itens
@bp.route('/get-item-price/<int:item_id>', methods=['GET'])
def get_item_price(item_id):
    item = ItemCardapio.query.get(item_id)
    if item:
        return jsonify({'price': str(item.preco)})
    return jsonify({'error': 'Item não encontrado'}), 404

# Acompanhar pedidos com filtros e busca
@bp.route('/acompanhar_pedidos', methods=['GET', 'POST'])
def acompanhar_pedidos():
    status = request.args.get('status', 'all')
    time_filter = request.args.get('time', 'all')
    search_query = request.args.get('search', '')

    # Base query para todos os pedidos
    pedidos_query = Pedido.query

    # Filtro por status
    if status == 'pending':
        pedidos_query = pedidos_query.filter_by(status='Pendente')
    elif status == 'completed':
        pedidos_query = pedidos_query.filter_by(status='Concluído')

    # Filtro de tempo (últimos 30 minutos, última hora, hoje)
    if time_filter == '30m':
        pedidos_query = pedidos_query.filter(Pedido.data_pedido >= (datetime.utcnow() - timedelta(minutes=30)))
    elif time_filter == '1h':
        pedidos_query = pedidos_query.filter(Pedido.data_pedido >= (datetime.utcnow() - timedelta(hours=1)))
    elif time_filter == 'today':
        pedidos_query = pedidos_query.filter(Pedido.data_pedido >= datetime.utcnow().replace(hour=0, minute=0, second=0))

    # Filtro de busca por mesa ou cliente
    if search_query:
        pedidos_query = pedidos_query.filter(
            db.or_(
                Pedido.nome_cliente.ilike(f'%{search_query}%'),
                Pedido.numero_mesa.ilike(f'%{search_query}%')
            )
        )

    try:
        # Obter os pedidos filtrados
        pedidos = pedidos_query.all()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")  # Log de erro
        pedidos = []  # Caso de erro, inicializa como lista vazia

    # Resposta AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Verifica se a requisição é AJAX
       return render_template('components/table_rows.html', pedidos=pedidos)

    return render_template('acompanhar_pedidos.html', pedidos=pedidos, active_page='acompanhar_pedidos')
# Atualizar status do pedido
@bp.route('/concluir-pedido/<int:pedido_id>', methods=['POST'])
def concluir_pedido(pedido_id):
    try:
        pedido = Pedido.query.get(pedido_id)
        if pedido:
            pedido.status = 'Concluído'
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Pedido não encontrado.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

#Converção moeda
def format_currency(value):
    return f"R$ {value:,.2f}".replace('.', ',')


# Tela relatorio de vendas
@bp.route('/relatorios_vendas', methods=['GET', 'POST'])
def relatorios_vendas():
    total_vendas = 0
    total_pedidos = 0
    media_por_venda = 0
    produto_mais_vendido = "N/A"
    
    if request.method == 'POST':
        data_inicio = request.form.get('data-inicio')
        data_fim = request.form.get('data-fim')

        if data_inicio and data_fim:
            # Conversão de string para datetime
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

            # Executando a query dinâmica para gerar o relatório
            relatorios = db.session.execute(text("""
                SELECT 
                    COUNT(p.id_pedido) AS total_pedidos,
                    SUM(COALESCE(p.total_pedido, 0)) AS total_vendas,
                    AVG(COALESCE(p.total_pedido, 0)) AS media_por_venda,
                    (SELECT i.nome_item FROM itens_cardapio i 
                    JOIN itens_pedido ip ON i.id_item = ip.id_item 
                    GROUP BY ip.id_item 
                    ORDER BY COUNT(ip.quantidade) DESC 
                    LIMIT 1) AS produto_mais_vendido
                FROM 
                    pedidos p
                WHERE 
                    p.data_pedido BETWEEN :data_inicio AND :data_fim + INTERVAL 1 DAY
                    AND p.status = 'Concluído'
            """), {'data_inicio': data_inicio, 'data_fim': data_fim})

            relatorio = relatorios.fetchone()

            # Verificar se a consulta retornou dados
            if relatorio:
                total_vendas = relatorio.total_vendas or 0
                total_pedidos = relatorio.total_pedidos or 0
                media_por_venda = relatorio.media_por_venda or 0
                produto_mais_vendido = relatorio.produto_mais_vendido or "N/A"

                # Formatar os valores para o padrão monetário
                total_vendas = format_currency(total_vendas)
                media_por_venda = format_currency(media_por_venda)


    return render_template('relatorios_vendas.html', 
                           total_vendas=total_vendas, 
                           total_pedidos=total_pedidos, 
                           media_por_venda=media_por_venda, 
                           produto_mais_vendido=produto_mais_vendido,
                           active_page='relatorios_vendas')



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
            # Retorna para a mesma tela de adicionar
            return render_template('cardapio/adicionar.html', form=form, active_page='cardapio')

        except Exception as e:
            db.session.rollback()
            error_message = "Ocorreu um erro ao adicionar o item. Por favor, tente novamente."
            flash(error_message, 'error')

    return render_template('cardapio/adicionar.html', form=form, active_page='cardapio')


@bp.route('/cardapio/listagem')
def listagem():
    try:
        itens = ItemCardapio.query.all()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        itens = []  # Retorne uma lista vazia como fallback
    
    return render_template('cardapio/listagem.html', itens=itens,active_page='cardapio')

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




