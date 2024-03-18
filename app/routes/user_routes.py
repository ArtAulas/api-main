from typing import List
from fastapi import APIRouter, Response, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import engine,SessionLocal
from db.models import User as UsuariosModel
from schemas.user import User as UserInput
from sqlalchemy.orm import Session

from db.base import Base


#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/users")   

def get_db():
    try:
        db = SessionLocal()
        #TODO 
        yield db
    finally:
        db.close()

#post usando schema
#post usando schema
@router.post("/addComSchema", status_code=status.HTTP_201_CREATED, description='Adicionar usuário')
def add_user(request:UserInput, db: Session = Depends(get_db)):
        # produto_on_db = ProdutosModel(id=request.id, item=request.item, peso=request.peso, numero_caixas=request.numero_caixas)
        produto_on_db = UserInput(**request.dict())
        db.add(produto_on_db)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED)

@router.get("/{username}", description="Busca usuário pelo nome")
def get_username(username,db: Session = Depends(get_db)):
    usuario= db.query(UserInput).filter(UserInput.username == username).first()
    return usuario


@router.get("/listar")
def get_all_users(db: Session = Depends(get_db)):
    try:
        users= db.query(UsuariosModel).all()
    except Exception as e:
        print(e)
        input("breakk")        
    return users

#validação no código
@router.delete("/{id}", description="Deletar o usuário pelo id")
def delete_user(id: int, db: Session = Depends(get_db)):


    usuario = db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sem usuario com este id')
    db.delete(usuario)
    db.commit()
    return f"Usuário com id:{id} deletado com sucesso", Response(status_code=status.HTTP_200_OK)

@router.put('/update/{id}', description='Update user')
def update_user(
    id: int,
    user: UserInput,
    db: Session = Depends(get_db)
    
    ):
    user_no_db = db.query(UsuariosModel).filter_by(id=id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NNo user was found with the given id')
    
    user_no_db.username=user.username
    user_no_db.password=user.password
    user_no_db.age=user.age
    user_no_db.gender=user.gender

    db.add(user_no_db)
    db.commit()
    return "ok"
