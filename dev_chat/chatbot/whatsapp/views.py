from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

EVOLUTION_API_TOKEN = "7431242"
EVOLUTION_API_URL = "http://localhost:8080/message"

@csrf_exempt
def webhook_whatsapp(request):
     if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        numero = data["message"]["from"]
        mensagem = data["message"]["body"].strip()

        print(f"📥 De: {numero} - {mensagem}")

        resposta = gerar_resposta(mensagem)

        # Envia a resposta pelo Evolution API
        requests.post(
            "http://localhost:8080/message",
            headers={"Authorization": f"Bearer {EVOLUTION_API_TOKEN}"},
            json={"number": numero, "message": resposta}
        )

        # Envia mensagem para todos os clientes WebSocket conectados
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chat",
            {
                "type": "receber_mensagem",
                "content": {
                    "de": numero,
                    "mensagem": mensagem
                }
            }
        )
        #return JsonResponse({"status": "ok"})
        return HttpResponse("Hello world!")

def gerar_resposta(mensagem):
    mensagem = mensagem.lower()
    if mensagem in ["oi", "olá"]:
        return "Olá! Digite:\n1 - Suporte\n2 - Consultar pedido"
    elif mensagem == "1":
        return "Você escolheu suporte. Um atendente vai te chamar."
    elif mensagem == "2":
        return "Digite o número do seu pedido:"
    else:
        return "Desculpe, não entendi. Digite 1 ou 2."


def painel_chat(request):
    #return render(request, "whatsapp/painel.html")
    template = loader.get_template('whatsapp/painel.html')
    return HttpResponse(template.render(request))

