import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Ajuste a string de conexão conforme seu banco
# Exemplo: postgresql://usuario:senha@localhost:5432/seubanco
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)


# Cria a tabela no banco (se não existir)
Base.metadata.create_all(bind=engine)


def adicionar_despesa(descricao, valor, categoria):
    session = SessionLocal()
    despesa = Despesa(descricao=descricao, valor=valor, categoria=categoria)
    session.add(despesa)
    session.commit()
    session.refresh(despesa)
    session.close()
    return {
        "id": despesa.id,
        "descricao": despesa.descricao,
        "valor": despesa.valor,
        "categoria": despesa.categoria
    }


def listar_despesas():
    session = SessionLocal()
    despesas = session.query(Despesa).all()
    resultado = [
        {"id": d.id, "descricao": d.descricao, "valor": d.valor, "categoria": d.categoria}
        for d in despesas
    ]
    session.close()
    return resultado


def atualizar_despesa(id, descricao=None, valor=None, categoria=None):
    session = SessionLocal()
    despesa = session.query(Despesa).filter(Despesa.id == id).first()
    if despesa:
        if descricao:
            despesa.descricao = descricao
        if valor:
            despesa.valor = valor
        if categoria:
            despesa.categoria = categoria
        session.commit()
        resultado = {
            "id": despesa.id,
            "descricao": despesa.descricao,
            "valor": despesa.valor,
            "categoria": despesa.categoria
        }
        session.close()
        return resultado
    session.close()
    return None


def remover_despesa(id):
    session = SessionLocal()
    despesa = session.query(Despesa).filter(Despesa.id == id).first()
    if despesa:
        session.delete(despesa)
        session.commit()
        session.close()
        return True
    session.close()
    return False
