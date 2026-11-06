"""Adiciona a descrição dos objetos de cada coleta."""

from alembic import op
import sqlalchemy as sa


revision = "0002_adiciona_descricao_coleta"
down_revision = "0001_cria_tabelas"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "coletas",
        sa.Column("descricao", sa.String(length=500), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_column("coletas", "descricao")
