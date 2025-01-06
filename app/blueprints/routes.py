# =============================================================================
# Define rotas e lógica de controle para o sistema.
# =============================================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app import db
from app.models.models import Pedido, ItemPedido, ItemCardapio, Feedback, Mesa, RelatorioVendas
from app.forms.addCardapio import ItemForm
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from app import csrf

bp = Blueprint('main', __name__)

# =============================================================================
# Rotas principais
# =============================================================================

@bp.route('/')
@bp.route('/home')
def home():
    """Rota para a página inicial."""
    return render_template('index.html', active_page='home')


@bp.route('/cardapio')
def cardapio():
    """Rota para a página do cardápio."""
    return render_template('cardapio/cardapio.html', active_page='cardapio')


# =============================================================================
# Rotas relacionadas a pedidos
# =============================================================================

@bp.route('/anotar-pedido', methods=['GET', 'POST'])
def anotar_pedido():
    """
    Rota para a tela de anotação de pedidos.
    Permite adicionar um pedido, associar itens e incluir feedback do cliente.
    """
    if request.method == 'POST':
        try:
            data = request.json
            # Coletar dados do pedido
            customer_name = data.get('customer_name') or None
            table_number = data.get('table_number') or None
            feedback = data.get('feedback')
            items = data.get('items', [])
            total_pedido = data.get('total_pedido', 0.0)

            # Criar novo pedido
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

            # Adicionar feedback, se fornecido
            if feedback:
                feedback_record = Feedback(id_pedido=pedido.id_pedido, nota=feedback)
                db.session.add(feedback_record)

            db.session.commit()
            return jsonify({'success': True})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)})

    # GET request: Exibir formulário para anotação
    try:
        mesas = Mesa.query.all()
        itens = ItemCardapio.query.all()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        mesas = [{'numero_mesa': '1'}, {'numero_mesa': '2'}]  # Dados fictícios
        itens = [{'id_item': 1, 'nome_item': 'Item Fictício 1'}, {'id_item': 2, 'nome_item': 'Item Fictício 2'}]

    return render_template('anotar_pedido.html', active_page='anotar_pedido', mesas=mesas, itens=itens)


@bp.route('/get-item-price/<int:item_id>', methods=['GET'])
def get_item_price(item_id):
    """
    Rota para retornar o preço de um item específico.
    Utilizada para cálculo dinâmico de preços ao anotar pedidos.
    """
    item = ItemCardapio.query.get(item_id)
    if item:
        return jsonify({'price': str(item.preco)})
    return jsonify({'error': 'Item não encontrado'}), 404


# =============================================================================
# Rotas para acompanhamento e atualização de pedidos
# =============================================================================

@bp.route('/acompanhar_pedidos', methods=['GET', 'POST'])
def acompanhar_pedidos():
    """
    Rota para acompanhar pedidos em tempo real com filtros de status, tempo e busca.
    Suporta requisições AJAX para atualizar a tabela de pedidos.
    """
    status = request.args.get('status', 'all')
    time_filter = request.args.get('time', 'all')
    search_query = request.args.get('search', '')

    pedidos_query = Pedido.query

    # Aplicar filtros de status
    if status == 'pending':
        pedidos_query = pedidos_query.filter_by(status='Pendente')
    elif status == 'completed':
        pedidos_query = pedidos_query.filter_by(status='Concluído')

    # Aplicar filtros de tempo
    now = datetime.utcnow()
    if time_filter == '30m':
        pedidos_query = pedidos_query.filter(Pedido.data_pedido >= (now - timedelta(minutes=30)))
    elif time_filter == '1h':
        pedidos_query = pedidos_query.filter(Pedido.data_pedido >= (now - timedelta(hours=1)))
    elif time_filter == 'today':
        pedidos_query = pedidos_query.filter(Pedido.data_pedido >= now.replace(hour=0, minute=0, second=0))

    # Aplicar busca
    if search_query:
        pedidos_query = pedidos_query.filter(
            db.or_(
                Pedido.nome_cliente.ilike(f'%{search_query}%'),
                Pedido.numero_mesa.ilike(f'%{search_query}%')
            )
        )

    try:
        pedidos = pedidos_query.all()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        pedidos = []

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('components/table_rows.html', pedidos=pedidos)

    return render_template('acompanhar_pedidos.html', pedidos=pedidos, active_page='acompanhar_pedidos')


@bp.route('/concluir-pedido/<int:pedido_id>', methods=['POST'])
def concluir_pedido(pedido_id):
    """
    Rota para atualizar o status de um pedido para 'Concluído'.
    """
    try:
        pedido = Pedido.query.get(pedido_id)
        if pedido:
            pedido.status = 'Concluído'
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Pedido não encontrado.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# Função para formatação de moeda
# Utilizada para formatar valores numéricos em formato de moeda (R$)
def format_currency(value):
    return f"R$ {value:,.2f}".replace('.', ',')


# Rota para exibir o relatório de vendas
# Esta rota exibe um relatório detalhado das vendas feitas em um intervalo de datas
@bp.route('/relatorios_vendas', methods=['GET', 'POST'])
def relatorios_vendas():
    total_vendas = 0
    total_pedidos = 0
    media_por_venda = 0
    produto_mais_vendido = "N/A"
    
    if request.method == 'POST':
        # Coletando as datas de início e fim fornecidas pelo usuário
        data_inicio = request.form.get('data-inicio')
        data_fim = request.form.get('data-fim')

        if data_inicio and data_fim:
            # Conversão de string para datetime para as datas
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

            # Executando a consulta para gerar o relatório
            relatorios = db.session.execute(text("""
                SELECT
                    COUNT(p.id_pedido) AS total_pedidos,
                    SUM(COALESCE(p.total_pedido, 0)) AS total_vendas,
                    AVG(COALESCE(p.total_pedido, 0)) AS media_por_venda,
                    (SELECT i.nome_item
                    FROM itens_cardapio i
                    JOIN itens_pedido ip ON i.id_item = ip.id_item
                    GROUP BY i.nome_item
                    ORDER BY COUNT(ip.quantidade) DESC
                    LIMIT 1) AS produto_mais_vendido
                FROM pedidos p
                WHERE p.data_pedido BETWEEN :data_inicio AND :data_fim + INTERVAL '1 DAY'
                AND p.status = 'Concluído'
            """), {"data_inicio": data_inicio, "data_fim": data_fim})


            relatorio = relatorios.fetchone()

            # Verificando os dados retornados pela consulta
            if relatorio:
                total_vendas = relatorio.total_vendas or 0
                total_pedidos = relatorio.total_pedidos or 0
                media_por_venda = relatorio.media_por_venda or 0
                produto_mais_vendido = relatorio.produto_mais_vendido or "N/A"

                # Formatando os valores para o padrão monetário
                total_vendas = format_currency(total_vendas)
                media_por_venda = format_currency(media_por_venda)


    return render_template('relatorios_vendas.html', 
                           total_vendas=total_vendas, 
                           total_pedidos=total_pedidos, 
                           media_por_venda=media_por_venda, 
                           produto_mais_vendido=produto_mais_vendido,
                           active_page='relatorios_vendas')

# =============================================================================
# Rotas para realizar GRUD de items do cardapio
# =============================================================================


# Rota para adicionar um novo item ao cardápio
# Recebe dados através de um formulário e adiciona um novo item à tabela de cardápio
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

            # Adiciona o novo item ao banco de dados
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


# Rota para listar todos os itens do cardápio
# Exibe a lista de itens cadastrados no cardápio
@bp.route('/cardapio/listagem')
def listagem():
    try:
        itens = ItemCardapio.query.all()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        itens = []  # Retorne uma lista vazia como fallback
    
    return render_template('cardapio/listagem.html', itens=itens, active_page='cardapio')


# Rota para editar um item do cardápio
# Permite editar os dados de um item existente no cardápio
@bp.route('/cardapio/editar/<int:id>', methods=['GET', 'POST'])
def editar_item(id):
    item = ItemCardapio.query.get_or_404(id)
    form = ItemForm(obj=item)
    
    if form.validate_on_submit():
        # Atualiza os dados do item no banco
        item.nome_item = form.nome_item.data
        item.preco = form.preco_item.data
        item.descricao = form.descricao_item.data
        item.disponivel = form.disponivel.data
        db.session.commit()
        flash('Item atualizado com sucesso!', 'success')
        return redirect(url_for('main.listagem'))
    
    return render_template('cardapio/editar.html', form=form, item=item, active_page='cardapio')


# Rota para excluir um item do cardápio
# Permite excluir um item do cardápio após confirmação
@bp.route('/cardapio/excluir/<int:id>', methods=['POST'])
def excluir_item(id):
    item = ItemCardapio.query.get_or_404(id)
    try:
        # Exclui o item do banco de dados
        db.session.delete(item)
        db.session.commit()
        flash('Item excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao excluir o item: {str(e)}', 'error')
    return redirect(url_for('main.listagem'))


# Rota para buscar itens no cardápio
# Permite realizar buscas por nome de item na tela de listagem do cardápio
@bp.route('/buscar_itens')
def buscar_itens():
    query = request.args.get('q', '', type=str)
    if query:
        # Realiza a busca filtrando pelo nome do item
        itens = ItemCardapio.query.filter(ItemCardapio.nome_item.ilike(f'%{query}%')).all()
    else:
        itens = ItemCardapio.query.all()

    # Prepara os dados dos itens para retornar como resposta JSON
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





