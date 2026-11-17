from pydantic import BaseModel


class Message(BaseModel):
    message: str


class LivroSchema(BaseModel):
    titulo: str
    autor: str
    isbn: str
    ano_publicacao: int


class LivroPublic(LivroSchema):
    id: int


class LivroDB(LivroPublic):
    pass


class LivroList(BaseModel):
    livros: list[LivroPublic]
