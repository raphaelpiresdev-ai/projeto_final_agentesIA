from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome_fantasia: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    cnpj: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    dominio_corporativo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    assinaturas: Mapped[list["Assinatura"]] = relationship(back_populates="empresa")


class Assinatura(Base):
    __tablename__ = "assinaturas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    plano: Mapped[str] = mapped_column(String(50), nullable=False)  # STARTER, PRO, ENTERPRISE
    status: Mapped[str] = mapped_column(String(20), default="ATIVA", nullable=False)  # ATIVA, INATIVA
    saldo_creditos_api: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    limite_usuarios: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    empresa: Mapped["Empresa"] = relationship(back_populates="assinaturas")


class AuditoriaCS(Base):
    __tablename__ = "auditoria_cs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assinatura_id: Mapped[int] = mapped_column(ForeignKey("assinaturas.id"), nullable=False)
    acao: Mapped[str] = mapped_column(String(50), nullable=False)
    detalhes: Mapped[str] = mapped_column(Text, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())