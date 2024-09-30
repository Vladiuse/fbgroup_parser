def confirm_action(message: str | None = None):
    if message is None:
        message = 'Continue? '
    user_answer = input(message)
    if user_answer.lower() in ['yes', 'y']:
        return
    print('End')
    exit()