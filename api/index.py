from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import Base, Figurinha
from .schemas import FigurinhaCreate, FigurinhaUpdate, FigurinhaResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Figurinhas da Copa",
    description="API para cadastro e consulta de figurinhas do álbum da Copa.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "mensagem": "API de Figurinhas da Copa está online!"
    }


@app.post("/figurinhas", response_model=FigurinhaResponse)
def cadastrar_figurinha(
    figurinha: FigurinhaCreate,
    db: Session = Depends(get_db)
):
    figurinha_existente = db.query(Figurinha).filter(
        Figurinha.numero_album == figurinha.numero_album
    ).first()

    if figurinha_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma figurinha com esse número no álbum."
        )

    nova_figurinha = Figurinha(
        numero_album=figurinha.numero_album,
        nome=figurinha.nome,
        pais=figurinha.pais,
        ordem_pais=figurinha.ordem_pais
    )

    db.add(nova_figurinha)
    db.commit()
    db.refresh(nova_figurinha)

    return nova_figurinha


@app.get("/figurinhas", response_model=list[FigurinhaResponse])
def listar_figurinhas(db: Session = Depends(get_db)):
    figurinhas = db.query(Figurinha).order_by(
        Figurinha.ordem_pais,
        Figurinha.numero_album
    ).all()
    return figurinhas


@app.get("/figurinhas/numero/{numero_album}", response_model=FigurinhaResponse)
def buscar_figurinha_por_numero(
    numero_album: str,
    db: Session = Depends(get_db)
):
    figurinha = db.query(Figurinha).filter(
        Figurinha.numero_album == numero_album
    ).first()

    if not figurinha:
        raise HTTPException(
            status_code=404,
            detail="Figurinha não encontrada."
        )

    return figurinha


@app.get("/figurinhas/pais/{pais}", response_model=list[FigurinhaResponse])
def listar_figurinhas_por_pais(
    pais: str,
    db: Session = Depends(get_db)
):
    figurinhas = db.query(Figurinha).filter(
        Figurinha.pais.ilike(f"%{pais}%")
    ).order_by(
        Figurinha.ordem_pais,
        Figurinha.numero_album
    ).all()

    return figurinhas


@app.get("/figurinhas/{figurinha_id}", response_model=FigurinhaResponse)
def buscar_figurinha_por_id(
    figurinha_id: int,
    db: Session = Depends(get_db)
):
    figurinha = db.query(Figurinha).filter(
        Figurinha.id == figurinha_id
    ).first()

    if not figurinha:
        raise HTTPException(
            status_code=404,
            detail="Figurinha não encontrada."
        )

    return figurinha


@app.put("/figurinhas/{figurinha_id}", response_model=FigurinhaResponse)
def atualizar_figurinha(
    figurinha_id: int,
    dados: FigurinhaUpdate,
    db: Session = Depends(get_db)
):
    figurinha = db.query(Figurinha).filter(
        Figurinha.id == figurinha_id
    ).first()

    if not figurinha:
        raise HTTPException(
            status_code=404,
            detail="Figurinha não encontrada."
        )

    numero_usado = db.query(Figurinha).filter(
        Figurinha.numero_album == dados.numero_album,
        Figurinha.id != figurinha_id
    ).first()

    if numero_usado:
        raise HTTPException(
            status_code=400,
            detail="Já existe outra figurinha com esse número no álbum."
        )

    figurinha.numero_album = dados.numero_album
    figurinha.nome = dados.nome
    figurinha.pais = dados.pais
    figurinha.ordem_pais = dados.ordem_pais

    db.commit()
    db.refresh(figurinha)

    return figurinha


@app.delete("/figurinhas/{figurinha_id}")
def deletar_figurinha(
    figurinha_id: int,
    db: Session = Depends(get_db)
):
    figurinha = db.query(Figurinha).filter(
        Figurinha.id == figurinha_id
    ).first()

    if not figurinha:
        raise HTTPException(
            status_code=404,
            detail="Figurinha não encontrada."
        )

    db.delete(figurinha)
    db.commit()

    return {
        "mensagem": "Figurinha removida com sucesso."
    }
@app.post("/figurinhas/lote", response_model=list[FigurinhaResponse])
def cadastrar_figurinhas_em_lote(
    figurinhas: list[FigurinhaCreate],
    db: Session = Depends(get_db)
):
    novas_figurinhas = []

    for figurinha in figurinhas:
        figurinha_existente = db.query(Figurinha).filter(
            Figurinha.numero_album == figurinha.numero_album
        ).first()

        if figurinha_existente:
            raise HTTPException(
                status_code=400,
                detail=f"Já existe uma figurinha com o número {figurinha.numero_album}."
            )

        nova_figurinha = Figurinha(
            numero_album=figurinha.numero_album,
            nome=figurinha.nome,
            pais=figurinha.pais,
            ordem_pais=figurinha.ordem_pais
        )

        db.add(nova_figurinha)
        novas_figurinhas.append(nova_figurinha)

    db.commit()

    for figurinha in novas_figurinhas:
        db.refresh(figurinha)

    return novas_figurinhas