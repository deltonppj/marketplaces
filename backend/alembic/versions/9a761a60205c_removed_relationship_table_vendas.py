"""Removed relationship table vendas

Revision ID: 9a761a60205c
Revises: 02fa54de42ac
Create Date: 2022-07-19 19:29:52.916281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a761a60205c'
down_revision = '02fa54de42ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loja_programa_pontos_venda')
    op.drop_table('produtos_venda')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produtos_venda',
    sa.Column('id_venda', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id_produto', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_produto'], ['produtos.id'], name='produtos_venda_id_produto_fkey'),
    sa.ForeignKeyConstraint(['id_venda'], ['vendas.id'], name='produtos_venda_id_venda_fkey')
    )
    op.create_table('loja_programa_pontos_venda',
    sa.Column('id_venda', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id_loja_programa_pontos', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_loja_programa_pontos'], ['loja_programa_pontos.id'], name='loja_programa_pontos_venda_id_loja_programa_pontos_fkey'),
    sa.ForeignKeyConstraint(['id_venda'], ['vendas.id'], name='loja_programa_pontos_venda_id_venda_fkey')
    )
    # ### end Alembic commands ###