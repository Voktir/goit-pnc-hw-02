import os
vigenere = __import__('1_vigenere')

# Константа алфавіту
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def create_matrix(key: str) -> list[list[str]]:
    """
    Створює матрицю для Полібіанського квадрата на основі ключа.
    Літера 'I' і 'J' об'єднуються в одну позицію.
    Аргументи:
        key (str): Ключ для створення матриці.
    Повертає:
        list[list[str]]: Матриця розміром 5x5.
    """
    unique_key = ''.join(sorted(set(key.upper()), key=key.upper().index))
    unique_key = unique_key.replace('J', 'I')
    modified_alphabet = ALPHABET.replace('J', '')
    remaining_chars = ''.join([c for c in modified_alphabet if c not in unique_key])
    matrix_chars = unique_key + remaining_chars
    
    return [matrix_chars[i:i + 5] for i in range(0, len(matrix_chars), 5)]


def print_matrix(matrix: list[list[str]]):
    """
    Виводить квадрат Полібія у зрозумілому форматі.
    Аргументи:
        matrix (list[list[str]]): Матриця розміром 5x5.
    """
    print("квадрат Полібія:")
    for row in matrix:
        print(" ".join(row))
    print()

def table_transform(text: str, key: str, encrypt: bool) -> str:
    """
    Універсальна функція для шифрування або дешифрування тексту 
    за допомогою Полібіанського квадрата.

    Args:
        text (str): Текст для обробки.
        key (str): Ключ для створення матриці.
        encrypt (bool): True для шифрування, False для дешифрування.

    Returns:
        str: Оброблений текст.
    """
    matrix = create_matrix(key)  # Створення матриці
    print_matrix(matrix)  # Виведення матриці для наочності
    direction = 1 if encrypt else -1  # Визначення напрямку зміщення
    transformed_text = []

    for char in text:
        if char.isalpha():  # Обробляємо лише літери
            found = False
            for col in range(len(matrix[0])):
                column_letters = [matrix[row][col] for row in range(len(matrix))]
                if char.upper() in column_letters:
                    row_index = column_letters.index(char.upper())
                    new_row = (row_index + direction) % len(matrix)
                    transformed_char = matrix[new_row][col]
                    transformed_text.append(transformed_char.lower() if char.islower() else transformed_char)
                    found = True
                    break
            if not found:
                transformed_text.append(char)  # Якщо буква не знайдена, додаємо її як є
        else:
            transformed_text.append(char)  # Нешифровані символи залишаються незмінними
    return ''.join(transformed_text)



def read_file(file_path: str) -> str:
    """
    Зчитує текст із файлу.
    Аргументи:
        file_path (str): Шлях до файлу.
    Повертає:
        str: Текст із файлу.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Помилка: файл '{file_path}' не знайдено.")
        return ""

if __name__ == "__main__":
    # Завантаження тексту
    text = read_file('plain_text.txt')
    if not text:
        exit()  # Завершення програми, якщо файл не знайдено
    
    key= "MATRIX"
    key2= "CRYPTO"

    encrypted_text = table_transform(text, key, encrypt=True)
    print(f"Зашифрований текст:\n{encrypted_text}\n")
    
    decrypted_text = table_transform(encrypted_text, key, encrypt=False)
    print(f"Розшифрований текст:\n{decrypted_text}\n")


    # Шифрування тексту спочатку використовуючи шифр Віженера, потім табличний шифр з ключем "CRYPTO"
    encrypted_text = vigenere.vigenere_encrypt(text, key)
    print(f"=== Зашифрований текст Віженером: ===\n{encrypted_text}\n")
     
    encrypted_text_table = table_transform(encrypted_text, key2, encrypt=True)
    print(f"=== Подвійно зашифрований текст Полібіанським квадратом: ===\n{encrypted_text_table}\n")
    
    # Розшифрування двічи зашифрованого тексту 
    decrypted_text_table = table_transform(encrypted_text_table, key2, encrypt=False)
    print(f"=== Розшифрований текст перший рівень ===:\n{decrypted_text_table}\n")
    
    decrypted_text = vigenere.vigenere_decrypt(decrypted_text_table, key)
    print(f"=== Розшифрований текст другий рівень: ===\n{decrypted_text}\n")