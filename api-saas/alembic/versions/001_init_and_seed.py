"""Cria tabelas iniciais do SaaS e popula dados de teste

Revision ID: 001_saas_init
Revises:
Create Date: 2026-11-24 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "001_saas_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    empresas_table = op.create_table(
        "empresas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome_fantasia", sa.String(length=150), nullable=False),
        sa.Column("cnpj", sa.String(length=20), nullable=False, unique=True),
        sa.Column("dominio_corporativo", sa.String(length=100), nullable=False, unique=True),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.func.now()),
    )

    assinaturas_table = op.create_table(
        "assinaturas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("empresa_id", sa.Integer(), sa.ForeignKey("empresas.id"), nullable=False),
        sa.Column("plano", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="ATIVA"),
        sa.Column("saldo_creditos_api", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("limite_usuarios", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("atualizado_em", sa.DateTime(), server_default=sa.func.now()),
    )

    auditoria_table = op.create_table(
        "auditoria_cs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assinatura_id", sa.Integer(), sa.ForeignKey("assinaturas.id"), nullable=False),
        sa.Column("acao", sa.String(length=50), nullable=False),
        sa.Column("detalhes", sa.Text(), nullable=False),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.func.now()),
    )

    # Seed inicial de empresas
    op.bulk_insert(
        empresas_table,
        [
            {
                "id": 1,
                "nome_fantasia": "Logística Sul",
                "cnpj": "11.222.333/0001-44",
                "dominio_corporativo": "logisticasul.com.br",
            },
            {
                "id": 2,
                "nome_fantasia": "TechFlow Soluções",
                "cnpj": "22.333.444/0001-55",
                "dominio_corporativo": "techflow.io",
            },
            {
                "id": 3,
                "nome_fantasia": "Alpha Varejo Brasil",
                "cnpj": "33.444.555/0001-66",
                "dominio_corporativo": "alphavarejo.com.br",
            },
            {
                "id": 4,
                "nome_fantasia": "Alpha Cloud Sistemas",
                "cnpj": "44.555.666/0001-77",
                "dominio_corporativo": "alphacloud.com.br",
            },
        ],
    )

    # Seed inicial de assinaturas (Ativa, Inativa e Ambíguas)
    op.bulk_insert(
        assinaturas_table,
        [
            {
                "id": 10,
                "empresa_id": 1,
                "plano": "STARTER",
                "status": "ATIVA",
                "saldo_creditos_api": 1200,
                "limite_usuarios": 10,
            },
            {
                "id": 11,
                "empresa_id": 2,
                "plano": "PRO",
                "status": "INATIVA",
                "saldo_creditos_api": 300,
                "limite_usuarios": 25,
            },
            {
                "id": 12,
                "empresa_id": 3,
                "plano": "STARTER",
                "status": "ATIVA",
                "saldo_creditos_api": 500,
                "limite_usuarios": 5,
            },
            {
                "id": 13,
                "empresa_id": 4,
                "plano": "ENTERPRISE",
                "status": "ATIVA",
                "saldo_creditos_api": 10000,
                "limite_usuarios": 100,
            },
        ],
    )

    op.bulk_insert(
        auditoria_table,
        [
            {
                "id": 1,
                "assinatura_id": 10,
                "acao": "ATIVACAO_INICIAL",
                "detalhes": "Carga inicial de 1.200 créditos na contratação do plano STARTER.",
            }
        ],
    )

    op.execute("SELECT setval('empresas_id_seq', (SELECT MAX(id) FROM empresas));")
    op.execute("SELECT setval('assinaturas_id_seq', (SELECT MAX(id) FROM assinaturas));")
    op.execute("SELECT setval('auditoria_cs_id_seq', (SELECT MAX(id) FROM auditoria_cs));")


def downgrade() -> None:
    op.drop_table("auditoria_cs")
    op.drop_table("assinaturas")
    op.drop_table("empresas")