from pydantic import BaseModel
from pydantic import validator

class User(BaseModel):
    id: int
    username:str
    password: str
    age:int
    gender: str

    @validator('password')
    def validate_password(cls,value):
        if len(value)<8:
            raise ValueError('Senha Muito Curta')
        return value
    
    # @validator('gender')
    # def validate_gender(cls,value):
    #     if value not in ('Feminino','Masculino'):
    #         raise ValueError('Gênero Inválido')
    #     return value