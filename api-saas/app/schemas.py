from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class EmpresaOut(BaseModel):
    id: int
    nome_fantasia: str
    cnpj: str
    dominio_corporativo: str

    model_config = {"from_attributes": True}


class AssinaturaOut(BaseModel):
    id: int
    empresa_id: int
    plano: str
    status: str
    saldo_creditos_api: int
    limite_usuarios: int

    model_config = {"from_attributes": True}


class AssinaturaUpdatePlano(BaseModel):
    plano: Literal["STARTER", "PRO", "ENTERPRISE"]
    limite_usuarios: int = Field(..., gt=0)


class CreditoCreate(BaseModel):
    quantidade: int = Field(..., gt=0, description="Quantidade positiva de créditos de API a incluir")
    motivo: str = Field(..., min_length=3, description="Justificativa da inclusão de créditos")


class AuditoriaOut(BaseModel):
    id: int
    assinatura_id: int
    acao: str
    detalhes: str
    criado_em: datetime

    model_config = {"from_attributes": True}