from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from schemas import (
    LivroDB,
    LivroList,
    LivroPublic,
    LivroSchema,
    Message,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return Message(message='Olá, mundo!')


@app.post(
    '/livros/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroPublic,
)
def create_livro(livro: LivroSchema):
    livro_com_id = LivroDB(id=len(database) + 1, **livro.model_dump())

    database.append(livro_com_id)

    return livro_com_id


@app.get('/livros/', response_model=LivroList)
def read_livros():
    return LivroList(livros=database)


@app.get('/livros/{livro_id}', response_model=LivroPublic)
def read_livro(livro_id: int):
    if livro_id < 1 or livro_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado',
        )

    return database[livro_id - 1]


@app.put('/livros/{livro_id}', response_model=LivroPublic)
def update_livro(livro_id: int, livro: LivroSchema):
    if livro_id < 1 or livro_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado',
        )

    livro_com_id = LivroDB(**livro.model_dump(), id=livro_id)
    database[livro_id - 1] = livro_com_id

    return livro_com_id


@app.delete('/livros/{livro_id}', response_model=Message)
def delete_livro(livro_id: int):
    if livro_id < 1 or livro_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado',
        )

    del database[livro_id - 1]

    return Message(message='Livro deletado')
