"""Cria as tabelas iniciais do sistema.

Revision ID: 0001_cria_tabelas
Revises:
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_cria_tabelas"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # NOVO: migration inicial dos grupos de usuários e das coletas.
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("tipo", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("senha_hash", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "coletas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("morador_id", sa.Integer(), nullable=False),
        sa.Column("endereco", sa.String(length=200), nullable=False),
        sa.Column("dia", sa.Date(), nullable=False),
        sa.Column("materiais", sa.String(length=200), nullable=False),
        sa.Column("situacao", sa.String(length=20), nullable=False),
        sa.Column("pontos", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["morador_id"], ["usuarios.id"], name="fk_coletas_morador"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pesagens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("coleta_id", sa.Integer(), nullable=False),
        sa.Column("material", sa.String(length=20), nullable=False),
        sa.Column("quilos", sa.Float(), nullable=False),
        sa.Column("pontos", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["coleta_id"], ["coletas.id"], name="fk_pesagens_coleta"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # NOVO: remove na ordem inversa para respeitar as chaves estrangeiras.
    op.drop_table("pesagens")
    op.drop_table("coletas")
    op.drop_table("usuarios")
