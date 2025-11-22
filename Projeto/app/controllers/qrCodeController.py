import qrcode
import os

def gerar_qrcode_evento(conteudo, nome_arquivo):
    
    pasta = os.path.join("app", "static", "qrcodes")

    # cria pasta se não existir
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    caminho_completo = os.path.join(pasta, nome_arquivo)

    img = qrcode.make(conteudo)
    img.save(caminho_completo)

    return f"/static/qrcodes/{nome_arquivo}"
