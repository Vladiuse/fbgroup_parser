def confirm_action(message: str | None = None):
    if message is None:
        message = 'Continue? '
    user_answer = input(message)
    if user_answer.lower() in ['yes', 'y']:
        return
    print('End')
    exit()
    
    
def convert_to_int(string: str) -> int:
    string = string.lower()
    incorrect_letters = [char for char in string if not (char.isdigit() or char in ['.', 'k', 'm'])]
    if incorrect_letters:
        raise ValueError(f'Incorrect chars, only k and m available\nValue: {string}')
    numbers = float(''.join([char for char in string if char.isdigit() or char == '.']))
    if 'k' in string:
        numbers *= 1000
    if 'm' in string:
        numbers *= 1000 * 1000
    return int(numbers)