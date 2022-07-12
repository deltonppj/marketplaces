"""Initial revision

Revision ID: 88c6e41f1fb3
Revises: 
Create Date: 2022-07-12 09:08:13.204864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88c6e41f1fb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lojas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('programas_pontos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('loja_programa_pontos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('id_loja', sa.Integer(), nullable=True),
    sa.Column('id_programas_pontos', sa.Integer(), nullable=True),
    sa.Column('preco_por_real', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['id_loja'], ['lojas.id'], ),
    sa.ForeignKeyConstraint(['id_programas_pontos'], ['programas_pontos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_loja_programa_pontos_CreatedAt'), 'loja_programa_pontos', ['CreatedAt'], unique=False)
    op.create_table('produtos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_sku', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('product_name', sa.String(length=250), nullable=False),
    sa.Column('product_price_sale', sa.Float(), nullable=False),
    sa.Column('product_url', sa.String(length=250), nullable=False),
    sa.Column('id_loja', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_loja'], ['lojas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_produtos_created_at'), 'produtos', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_produtos_created_at'), table_name='produtos')
    op.drop_table('produtos')
    op.drop_index(op.f('ix_loja_programa_pontos_CreatedAt'), table_name='loja_programa_pontos')
    op.drop_table('loja_programa_pontos')
    op.drop_table('programas_pontos')
    op.drop_table('lojas')
    # ### end Alembic commands ###