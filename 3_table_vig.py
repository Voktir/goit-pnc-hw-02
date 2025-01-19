def create_matrix_key(keyword):
    """Створює матрицю для табличного шифру на основі ключового слова"""
    size = len(keyword)
    matrix = [['' for _ in range(size)] for _ in range(size)]
    
    top, bottom = 0, size-1
    left, right = 0, size-1
    index = 0
    
    while top <= bottom and left <= right and index < len(keyword):
        for i in range(left, right + 1):
            if index < len(keyword):
                matrix[top][i] = keyword[index]
                index += 1
        top += 1
        
        for i in range(top, bottom + 1):
            if index < len(keyword):
                matrix[i][right] = keyword[index]
                index += 1
        right -= 1
        
        if top <= bottom:
            for i in range(right, left - 1, -1):
                if index < len(keyword):
                    matrix[bottom][i] = keyword[index]
                    index += 1
            bottom -= 1
        
        if left <= right:
            for i in range(bottom, top - 1, -1):
                if index < len(keyword):
                    matrix[i][left] = keyword[index]
                    index += 1
            left += 1
    
    return matrix

def get_matrix_positions(matrix):
    """Отримує позиції символів в матриці в порядку зростання"""
    positions = {}
    size = len(matrix)
    
    chars_with_positions = []
    for i in range(size):
        for j in range(size):
            if matrix[i][j]:
                chars_with_positions.append((matrix[i][j], i, j))
    
    chars_with_positions.sort(key=lambda x: x[0])
    
    for index, (char, i, j) in enumerate(chars_with_positions):
        positions[index] = (i, j)
    
    return positions

def prepare_text_with_positions(text):
    """Підготовка тексту із збереженням спеціальних символів"""
    special_chars = {}
    clean_text = ""
    for i, char in enumerate(text):
        if char.isalpha():
            clean_text += char.upper()
        else:
            special_chars[i] = char
    return clean_text, special_chars

def restore_special_chars(text, special_chars, original_length):
    """Відновлення спеціальних символів у тексті"""
    result = list(text)
    offset = 0
    
    for pos, char in sorted(special_chars.items()):
        result.insert(pos, char)
        offset += 1
    
    return ''.join(result[:original_length])

# ------------------------- РІВЕНЬ 1 -------------------------
def matrix_encrypt(text, keyword):
    """Шифрування тексту табличним шифром зі збереженням форматування"""
    # Зберігаємо спеціальні символи
    original_length = len(text)
    clean_text, special_chars = prepare_text_with_positions(text)
    
    # Створюємо матрицю та отримуємо позиції
    matrix = create_matrix_key(keyword)
    positions = get_matrix_positions(matrix)
    
    # Доповнюємо текст, якщо потрібно
    block_size = len(keyword)
    padding_length = (block_size - (len(clean_text) % block_size)) % block_size
    clean_text += 'X' * padding_length
    
    # Шифруємо текст блоками
    encrypted = ''
    for i in range(0, len(clean_text), block_size):
        block = clean_text[i:i + block_size]
        encrypted_block = [''] * block_size
        
        for j, char in enumerate(block):
            pos = positions[j]
            encrypted_block[pos[0] * len(matrix) + pos[1]] = char
        
        encrypted += ''.join(encrypted_block)
    
    # Відновлюємо спеціальні символи
    return restore_special_chars(encrypted, special_chars, original_length)

def matrix_decrypt(encrypted_text, keyword):
    """Дешифрування тексту табличним шифром зі збереженням форматування"""
    # Зберігаємо спеціальні символи
    original_length = len(encrypted_text)
    clean_text, special_chars = prepare_text_with_positions(encrypted_text)
    
    # Створюємо матрицю та отримуємо позиції
    matrix = create_matrix_key(keyword)
    positions = get_matrix_positions(matrix)
    
    # Створюємо зворотній словник позицій
    reverse_positions = {(i, j): pos for pos, (i, j) in positions.items()}
    
    # Дешифруємо текст блоками
    decrypted = ''
    block_size = len(keyword)
    
    for i in range(0, len(clean_text), block_size):
        block = clean_text[i:i + block_size]
        decrypted_block = [''] * block_size
        
        for j, char in enumerate(block):
            row, col = j // len(matrix), j % len(matrix)
            original_pos = reverse_positions.get((row, col))
            if original_pos is not None:
                decrypted_block[original_pos] = char
        
        decrypted += ''.join(decrypted_block)
    
    # Відновлюємо спеціальні символи
    return restore_special_chars(decrypted, special_chars, original_length)

# ------------------------- РІВЕНЬ 2 -------------------------
def vigenere_encrypt_with_spaces(text, key):
    """Шифрування методом Віженера зі збереженням форматування"""
    original_length = len(text)
    clean_text, special_chars = prepare_text_with_positions(text)
    key = ''.join(c.upper() for c in key if c.isalpha())
    key = (key * (len(clean_text) // len(key) + 1))[:len(clean_text)]
    
    encrypted = ''
    for i in range(len(clean_text)):
        shift = (ord(clean_text[i]) + ord(key[i]) - 2 * ord('A')) % 26
        encrypted += chr(shift + ord('A'))
    
    return restore_special_chars(encrypted, special_chars, original_length)

def combined_encrypt(text, vigenere_key, matrix_key):
    """Комбіноване шифрування зі збереженням форматування"""
    # Спочатку шифруємо методом Віженера
    vigenere_encrypted = vigenere_encrypt_with_spaces(text, vigenere_key)
    
    # Потім застосовуємо табличний шифр
    return matrix_encrypt(vigenere_encrypted, matrix_key)

def visualize_matrix(matrix):
    """Візуалізація матриці шифрування"""
    print("\nМатриця шифрування:")
    for row in matrix:
        print(' '.join(f'{c:2}' for c in row))

def level1_demo(text):
    """Демонстрація роботи першого рівня"""
    print("\n" + "="*50)
    print("РІВЕНЬ 1: Табличний шифр")
    print("="*50)
    
    keyword = "MATRIX"
    print(f"Початковий текст:\n{text}")
    print(f"\nКлюч: {keyword}")
    
    matrix = create_matrix_key(keyword)
    visualize_matrix(matrix)
    
    encrypted = matrix_encrypt(text, keyword)
    print(f"\nЗашифрований текст:\n{encrypted}")
    
    decrypted = matrix_decrypt(encrypted, keyword)
    print(f"\nРозшифрований текст:\n{decrypted}")
    
    return encrypted

def level2_demo(text):
    """Демонстрація роботи другого рівня"""
    print("\n" + "="*50)
    print("РІВЕНЬ 2: Комбінований шифр (Віженер + Табличний)")
    print("="*50)
    
    vigenere_key = "CRYPTOGRAPHY"
    matrix_key = "CRYPTO"
    
    print(f"Початковий текст:\n{text}")
    print(f"\nКлюч Віженера: {vigenere_key}")
    print(f"Ключ матриці: {matrix_key}")
    
    matrix = create_matrix_key(matrix_key)
    visualize_matrix(matrix)
    
    encrypted = combined_encrypt(text, vigenere_key, matrix_key)
    print(f"\nЗашифрований текст:\n{encrypted}")

if __name__ == "__main__":
    # Тестовий текст
    sample_text = "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."
    
    # Демонстрація Рівня 1
    encrypted_text = level1_demo(sample_text)
    
    # Демонстрація Рівня 2
    level2_demo(sample_text)