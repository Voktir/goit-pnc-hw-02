from typing import List

def create_matrix(text: str, num_cols: int, fill: str = ' ') -> List[List[str]]:
    """
    Створює матрицю тексту за кількістю стовпчиків.

    :param text: Вхідний текст для обробки.
    :param num_cols: Кількість стовпчиків (довжина ключа).
    :param fill: Символ для доповнення (за замовчуванням пробіл).
    :return: Матриця тексту.
    """
    num_rows = (len(text) + num_cols - 1) // num_cols
    padded_text = text.ljust(num_cols * num_rows, fill)
    return [list(padded_text[i * num_cols:(i + 1) * num_cols]) for i in range(num_rows)]

def transpos_cols_encrypt(text: str, key: str, log: bool = False) -> str:
    """
    Шифрує текст за методом перестановки стовпчиків.

    :param text: Вхідний текст для шифрування.
    :param key: Ключ для шифрування.
    :param log: Якщо True, виводить матрицю.
    :return: Зашифрований текст.
    """
    if not text or not key:
        raise ValueError("Text and key must not be empty.")

    num_cols = len(key)
    matrix = create_matrix(text, num_cols)

    if log:
        print("Матриця для шифрування (ключ: {}):".format(key))
        for row in matrix:
            print(row)

    # Визначаємо порядок стовпчиків на основі ключа
    sorted_key_indices = sorted(range(num_cols), key=lambda k: key[k])

    # Шифруємо, зчитуючи матрицю по колонках у порядку ключа
    encrypted_text = ''.join(''.join(row[col_index] for row in matrix) for col_index in sorted_key_indices)
    return encrypted_text

def transpos_cols_decrypt(encrypted_text: str, key: str, log: bool = False) -> str:
    """
    Розшифровує текст за методом перестановки стовпчиків.

    :param encrypted_text: Зашифрований текст.
    :param key: Ключ для розшифрування.
    :param log: Якщо True, виводить матрицю.
    :return: Розшифрований текст.
    """
    if not encrypted_text or not key:
        raise ValueError("Encrypted text and key must not be empty.")

    num_cols = len(key)
    num_rows = len(encrypted_text) // num_cols

    # Визначаємо порядок стовпчиків на основі ключа
    sorted_key_indices = sorted(range(num_cols), key=lambda k: key[k])

    # Відновлюємо матрицю, зчитуючи по колонках
    matrix = [[''] * num_cols for _ in range(num_rows)]
    index = 0
    for col_index in sorted_key_indices:
        for row in range(num_rows):
            matrix[row][col_index] = encrypted_text[index]
            index += 1

    if log:
        print("Матриця для дешифрування (ключ: {}):".format(key))
        for row in matrix:
            print(row)

    # Зчитуємо текст по рядках
    decrypted_text = ''.join(''.join(row) for row in matrix)
    return decrypted_text.rstrip()


def double_transpos_encrypt(text: str, key_row: str, key_col: str, log: bool = False) -> str:
    """
    Шифрує текст за методом подвійної перестановки.

    :param text: Вхідний текст для шифрування.
    :param key_row: Ключ для перестановки рядків.
    :param key_col: Ключ для перестановки стовпчиків.
    :param log: Якщо True, виводить проміжні матриці.
    :return: Зашифрований текст.
    """
    num_cols = len(key_col)
    matrix = create_matrix(text, num_cols)

    # Перестановка рядків
    row_indices = sorted(range(len(matrix)), key=lambda i: key_row[i % len(key_row)])
    reordered_matrix = [matrix[i] for i in row_indices]

    if log:
        print("Матриця після перестановки рядків (ключ: {}):".format(key_row))
        for row in reordered_matrix:
            print(row)

    # Перестановка стовпчиків
    col_indices = sorted(range(num_cols), key=lambda k: key_col[k])
    encrypted_text = ''.join(
        ''.join(row[col_index] for row in reordered_matrix) for col_index in col_indices
    )

    return encrypted_text


def double_transpos_decrypt(encrypted_text: str, key_row: str, key_col: str, log: bool = False) -> str:
    """
    Розшифровує текст за методом подвійної перестановки.

    :param encrypted_text: Зашифрований текст.
    :param key_row: Ключ для перестановки рядків.
    :param key_col: Ключ для перестановки стовпчиків.
    :param log: Якщо True, виводить проміжні матриці.
    :return: Розшифрований текст.
    """
    num_cols = len(key_col)
    num_rows = len(encrypted_text) // num_cols

    # Відновлення матриці з перестановкою стовпчиків
    col_indices = sorted(range(num_cols), key=lambda k: key_col[k])
    matrix = [[''] * num_cols for _ in range(num_rows)]
    index = 0
    for col_index in col_indices:
        for row in range(num_rows):
            matrix[row][col_index] = encrypted_text[index]
            index += 1

    if log:
        print("Матриця після перестановки стовпчиків (ключ: {}):".format(key_col))
        for row in matrix:
            print(row)

    # Відновлення перестановки рядків
    row_indices = sorted(range(num_rows), key=lambda i: key_row[i % len(key_row)])
    row_order = sorted(range(len(row_indices)), key=lambda i: row_indices[i])
    reordered_matrix = [matrix[i] for i in row_order]

    # Читання тексту по рядках
    decrypted_text = ''.join(''.join(row) for row in reordered_matrix)
    return decrypted_text.rstrip()


def read_file(file_path: str) -> str:
    """
    Зчитує текст із файлу.
    
    :param file_path: Шлях до файлу.
    :return: Вміст файлу.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        return ""
    except Exception as e:
        print(f"Помилка читання файлу {file_path}: {e}")
        return ""


# Тестування
if __name__ == "__main__":
    original_text = read_file("plain_text.txt")
    key = "SECRET"

    # Шифрування тексту
    encrypted = transpos_cols_encrypt(original_text, key)
    print("РІВЕНЬ 1: Алгоритм простої перестановки для шифрування та дешифрування тексту")
    print(f"Зашифрований текст методом перестановки стовпчиків:\n{encrypted}\n")

    # Дешифрування тексту
    decrypted = transpos_cols_decrypt(encrypted, key)
    print(f"Дешифрований текст методом перестановки стовпчиків:\n{decrypted}\n")

    original_text = read_file("plain_text.txt")
    key_row = "SECRET"
    key_col = "CRYPTO"

    # Шифрування тексту
    encrypted = double_transpos_encrypt(original_text, key_row, key_col, log=False)
    print("РІВЕНЬ 2: Алгоритм подвійної перестановки для шифрування та дешифрування тексту")
    print(f"Зашифрований текст методом подвійної перестановки:\n{encrypted}\n")

    # Дешифрування тексту
    decrypted = double_transpos_decrypt(encrypted, key_row, key_col, log=False)
    print(f"Дешифрований текст методом подвійної перестановки:\n{decrypted}\n")