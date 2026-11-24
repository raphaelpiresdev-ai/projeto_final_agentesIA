from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

app = FastAPI(
    title="SaaS B2B Admin API",
    description="Sistema base para gestão de empresas clientes, assinaturas e créditos de API.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/empresas", response_model=list[schemas.EmpresaOut])
def listar_empresas(
    nome: str | None = Query(default=None, description="Filtro parcial pelo nome fantasia da empresa"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Empresa)
    if nome:
        query = query.filter(models.Empresa.nome_fantasia.ilike(f"%{nome.strip()}%"))
    return query.all()


@app.get("/assinaturas/{empresa_id}", response_model=list[schemas.AssinaturaOut])
def consultar_assinaturas_empresa(empresa_id: int, db: Session = Depends(get_db)):
    assinaturas = (
        db.query(models.Assinatura)
        .filter(models.Assinatura.empresa_id == empresa_id)
        .all()
    )
    if not assinaturas:
        raise HTTPException(status_code=404, detail="Nenhuma assinatura encontrada para a empresa informada.")
    return assinaturas


@app.post("/assinaturas/{assinatura_id}/creditos", response_model=schemas.AssinaturaOut, status_code=201)
def incluir_creditos_assinatura(
    assinatura_id: int,
    payload: schemas.CreditoCreate,
    db: Session = Depends(get_db),
):
    assinatura = db.query(models.Assinatura).filter(models.Assinatura.id == assinatura_id).first()
    if not assinatura:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada.")

    if assinatura.status.upper() != "ATIVA":
        raise HTTPException(
            status_code=422,
            detail=f"Não é possível incluir créditos em assinatura com status '{assinatura.status}'.",
        )

    assinatura.saldo_creditos_api += payload.quantidade

    log_auditoria = models.AuditoriaCS(
        assinatura_id=assinatura.id,
        acao="INCLUSAO_CREDITOS",
        detalhes=f"+{payload.quantidade} créditos incluídos. Motivo: {payload.motivo}",
    )
    db.add(log_auditoria)
    db.commit()
    db.refresh(assinatura)
    return assinatura


@app.patch("/assinaturas/{assinatura_id}", response_model=schemas.AssinaturaOut)
def atualizar_plano_assinatura(
    assinatura_id: int,
    payload: schemas.AssinaturaUpdatePlano,
    db: Session = Depends(get_db),
):
    """Endpoint administrativo fora do escopo do agente (usado para validar menor privilégio)."""
    assinatura = db.query(models.Assinatura).filter(models.Assinatura.id == assinatura_id).first()
    if not assinatura:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada.")

    assinatura.plano = payload.plano
    assinatura.limite_usuarios = payload.limite_usuarios
    db.commit()
    db.refresh(assinatura)
    return assinatura


@app.get("/auditoria-cs", response_model=list[schemas.AuditoriaOut])
def listar_logs_auditoria(assinatura_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.AuditoriaCS)
    if assinatura_id:
        query = query.filter(models.AuditoriaCS.assinatura_id == assinatura_id)
    return query.order_by(models.AuditoriaCS.id.desc()).all()