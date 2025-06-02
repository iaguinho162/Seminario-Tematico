from fastapi import APIRouter, HTTPException
from models import Usuario

router = APIRouter()

banco_usuarios = {}
contador_usuario = 1

@router.post("/usuarios/", response_model=Usuario)
def criar_usuario(usuario: Usuario):
    global contador_usuario
    usuario.id = contador_usuario
    banco_usuarios[usuario.id] = usuario
    contador_usuario += 1
    return usuario

@router.get("/usuarios/")
def listar_usuarios():
    return list(banco_usuarios.values())

@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def obter_usuario(usuario_id: int):
    usuario = banco_usuarios.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

#Atualizar usuário
@router.put("/usuarios/{usuario_id}", response_model=Usuario)
def atualizar_usuario(usuario_id: int, dados_usuario: Usuario):
    if usuario_id not in banco_usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    dados_usuario.id = usuario_id
    banco_usuarios[usuario_id] = dados_usuario
    return dados_usuario

#Excluir usuário
@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    if usuario_id not in banco_usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    del banco_usuarios[usuario_id]
    return {"detail": "Usuário deletado com sucesso"}
