import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from extrator import ExtratorEstatistico
from dotenv import load_dotenv

load_dotenv()

def gerar_menu_inicial():
    keyboard = [[InlineKeyboardButton("Ver os jogos de hoje", callback_data='listar')]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Escolha uma opção para acompanhar os jogos:", reply_markup=gerar_menu_inicial())

async def monitor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ex = ExtratorEstatistico()

    if query.data == 'listar':
        jogos = ex.listar_jogos_hoje()
        if not jogos:
            await query.message.edit_text("Não encontrei jogos para hoje.", reply_markup=gerar_menu_inicial())
            return

        keyboard = [[InlineKeyboardButton(j['nome'], callback_data=f"get_{j['id']}")] for j in jogos]
        keyboard.append([InlineKeyboardButton("Voltar ao início", callback_data='inicio')])
        await query.message.edit_text("Selecione um jogo para ver os detalhes:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('get_'):
        id_jogo = query.data.split('_')[1]
        informacoes = ex.buscar_dossie_real(id_jogo)
        
        keyboard = [
            [InlineKeyboardButton("Atualizar dados", callback_data=f"get_{id_jogo}")],
            [InlineKeyboardButton("Voltar para a lista", callback_data='listar')],
            [InlineKeyboardButton("Ir para o início", callback_data='inicio')]
        ]
        await query.message.edit_text(f"Aqui estão as informações do jogo:\n\n{informacoes}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'inicio':
        await query.message.edit_text("O que você gostaria de fazer agora?", reply_markup=gerar_menu_inicial())

if __name__ == "__main__":
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(monitor_callback))
    app.run_polling()