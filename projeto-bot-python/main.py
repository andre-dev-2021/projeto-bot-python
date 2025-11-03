from telegram import get_updates, send_message
from weather import weather_forecast, weather_now
import time


if __name__ == "__main__":
    last_update_id = None
    last_choice = None

    while True:
        try:
            offset = (last_update_id + 1) if last_update_id is not None else None
            chat_id, text, update_id, msg_type = get_updates(offset=offset, timeout=60)

            if update_id is not None:
                if last_update_id is None or update_id > last_update_id:
                    last_update_id = update_id
                    
                    if msg_type == 'bot_command':
                        match text:
                            case '/start':
                                send_message(chat_id,"""👋 Olá, sou Skybot 🤖!
Digite '/help' para conhecer os comandos disponíveis.""")
                            
                            case '/clima':
                                last_choice = "clima"
                                send_message(chat_id, "Para qual cidade você deseja?")
                            
                            case '/previsao':
                                last_choice = "previsao"
                                send_message(chat_id, "🤔 Para qual cidade você deseja?")

                            case '/help':
                                send_message(chat_id, """
                            COMANDOS:
                                             
/clima: Receba o clima atual
/previsao: Receba a previsão do tempo para os próximos 5 dias
/help: Verifique os comandos disponiveis.
                            """)
                    else:
                        if last_choice == "clima":
                            txt = weather_now(text)
                            send_message(chat_id, txt)

                        if last_choice == "previsao":
                            txt = weather_forecast(text)
                            send_message(chat_id, txt)

                continue

        except Exception as e:
            send_message(chat_id, "🤔 Não entendi sua pergunta, digite '/help' para saber como utilizar este chatbot.")