import os
import requests
from flask import Flask

app = Flask(__name__)

# ==========================================
# 1. CONFIGURAÇÕES (Lidas do Render por segurança)
# ==========================================
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

LIMITE_DISTANCIA_STH_RP = 0.05  
LIMITE_VOLUME_OPCOES = 2.0      

# ==========================================
# 2. FUNÇÕES DE EXTRAÇÃO (Sensores)
# ==========================================
def obter_dados_onchain():
    return {
        "preco_atual_btc": 64000,
        "sth_rp_suporte": 62500 
    }

def obter_options_flow_ibit():
    return {
        "racio_volume_open_interest": 2.5, 
        "sentimento": "BULLISH_CALL_SWEEPS"
    }

# ==========================================
# 3. NOTIFICAÇÃO (Alarme)
# ==========================================
def enviar_alerta_telegram(mensagem):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Erro: Tokens do Telegram não configurados no Render.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

# ==========================================
# 4. MOTOR LÓGICO (Cérebro)
# ==========================================
def analisar_mercado():
    onchain = obter_dados_onchain()
    opcoes = obter_options_flow_ibit()
    
    distancia_suporte = (onchain["preco_atual_btc"] - onchain["sth_rp_suporte"]) / onchain["preco_atual_btc"]
    
    if distancia_suporte <= LIMITE_DISTANCIA_STH_RP and opcoes["racio_volume_open_interest"] >= LIMITE_VOLUME_OPCOES:
        mensagem = (
            "🚨 <b>ALERTA DE CONVERGÊNCIA IBIT</b> 🚨\n\n"
            "<b>Sinal:</b> Alta Convicção (Potencial Ressalto)\n\n"
            f"<b>Preço BTC:</b> ${onchain['preco_atual_btc']}\n"
            f"<b>Suporte On-Chain (STH-RP):</b> ${onchain['sth_rp_suporte']}\n"
            f"<b>Anomalia Opções IBIT:</b> Volume {opcoes['racio_volume_open_interest']*100}% acima da média.\n"
            f"<b>Fluxo Institucional:</b> {opcoes['sentimento']}\n\n"
            "<i>Atenção: Valide o risco antes de executar a trade.</i>"
        )
        enviar_alerta_telegram(mensagem)
        return "Alerta enviado!"
    else:
        return "Sem convergência. Nenhum alerta."

# ==========================================
# 5. ROTAS WEB (Para o Render funcionar)
# ==========================================
@app.route('/')
def home():
    return "O radar do IBIT está online e a funcionar!"

@app.route('/executar')
def executar_bot():
    resultado = analisar_mercado()
    return f"Processo concluído: {resultado}"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)