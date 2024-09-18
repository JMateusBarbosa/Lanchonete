"""Initial migration

Revision ID: 429db7590808
Revises: 
Create Date: 2024-09-17 18:31:13.188296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '429db7590808'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id_item', sa.Integer(), nullable=False),
    sa.Column('nome_item', sa.String(length=80), nullable=False),
    sa.Column('descricao', sa.String(length=200), nullable=True),
    sa.Column('preco', sa.Float(), nullable=False),
    sa.Column('disponivel', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id_item')
    )
    with op.batch_alter_table('itens_cardapio', schema=None) as batch_op:
        batch_op.alter_column('nome_item',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('disponivel',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True,
               existing_server_default=sa.text("'1'"))

    with op.batch_alter_table('itens_pedido', schema=None) as batch_op:
        batch_op.alter_column('id_pedido',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('id_item',
               existing_type=mysql.INTEGER(),
               nullable=False)

    with op.batch_alter_table('pedidos', schema=None) as batch_op:
        batch_op.alter_column('nome_cliente',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('status',
               existing_type=mysql.ENUM('Pendente', 'Em Preparação', 'Concluído'),
               type_=sa.String(length=50),
               existing_nullable=False,
               existing_server_default=sa.text("'Pendente'"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedidos', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=50),
               type_=mysql.ENUM('Pendente', 'Em Preparação', 'Concluído'),
               existing_nullable=False,
               existing_server_default=sa.text("'Pendente'"))
        batch_op.alter_column('nome_cliente',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)

    with op.batch_alter_table('itens_pedido', schema=None) as batch_op:
        batch_op.alter_column('id_item',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('id_pedido',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('itens_cardapio', schema=None) as batch_op:
        batch_op.alter_column('disponivel',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False,
               existing_server_default=sa.text("'1'"))
        batch_op.alter_column('nome_item',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)

    op.drop_table('item')
    # ### end Alembic commands ###