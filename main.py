from telegram_functions.telegram_functions import get_updates, handle_message


def main():
    offset = None
    print("Bot iniciado y escuchando mensajes...")

    while True:
        updates = get_updates(offset)
        if updates and 'result' in updates:
            for update in updates['result']:
                offset = update['update_id'] + 1
                if 'message' in update:
                    handle_message(update['message'])

if __name__ == '__main__':
    main()