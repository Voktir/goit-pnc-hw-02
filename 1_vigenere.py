# ------------------------- РІВЕНЬ 1 -------------------------
def prepare_text_with_positions(text):
    """
    Підготовка тексту із збереженням позицій спеціальних символів
    
    Returns:
        tuple: (підготовлений текст, словник спеціальних символів)
    """
    special_chars = {}
    text_without_spaces = ""
    for i, char in enumerate(text):
        if char.isalpha():
            text_without_spaces += char.upper()
        else:
            special_chars[i] = char
    return text_without_spaces, special_chars

def restore_special_chars(text, special_chars, original_length):
    """Відновлення спеціальних символів у тексті"""
    result = ""
    text_pos = 0
    
    for i in range(original_length):
        if i in special_chars:
            result += special_chars[i]
        else:
            result += text[text_pos]
            text_pos += 1
    return result

def vigenere_encrypt(text, key):
    """
    Шифрування тексту за допомогою шифру Віженера зі збереженням форматування
    
    Args:
        text (str): Вхідний текст для шифрування
        key (str): Ключ шифрування
    
    Returns:
        str: Зашифрований текст з оригінальним форматуванням
    """
    # Підготовка тексту зі збереженням спеціальних символів
    clean_text, special_chars = prepare_text_with_positions(text)
    key = ''.join(char.upper() for char in key if char.isalpha())
    
    # Розширення ключа
    key_repeated = (key * (len(clean_text) // len(key) + 1))[:len(clean_text)]
    
    # Шифрування
    encrypted = ''
    for i in range(len(clean_text)):
        if clean_text[i].isalpha():
            shift = (ord(clean_text[i]) + ord(key_repeated[i]) - 2 * ord('A')) % 26
            encrypted += chr(shift + ord('A'))
    
    # Відновлення форматування
    return restore_special_chars(encrypted, special_chars, len(text))

def vigenere_decrypt(encrypted_text, key):
    """
    Дешифрування тексту, зашифрованого шифром Віженера, зі збереженням форматування
    
    Args:
        encrypted_text (str): Зашифрований текст
        key (str): Ключ шифрування
    
    Returns:
        str: Розшифрований текст з оригінальним форматуванням
    """
    # Підготовка тексту зі збереженням спеціальних символів
    clean_text, special_chars = prepare_text_with_positions(encrypted_text)
    key = ''.join(char.upper() for char in key if char.isalpha())
    
    # Розширення ключа
    key_repeated = (key * (len(clean_text) // len(key) + 1))[:len(clean_text)]
    
    # Дешифрування
    decrypted = ''
    for i in range(len(clean_text)):
        if clean_text[i].isalpha():
            shift = (ord(clean_text[i]) - ord(key_repeated[i])) % 26
            decrypted += chr(shift + ord('A'))
    
    # Відновлення форматування
    return restore_special_chars(decrypted, special_chars, len(encrypted_text))

def level1_demo(text, key):
    """Демонстрація роботи першого рівня"""
    print("\n" + "="*50)
    print("РІВЕНЬ 1: Базове шифрування та дешифрування")
    print("="*50)
    
    print(f"Початковий текст:\n{text}")
    print(f"\nКлюч: {key}")
    
    # Шифрування
    encrypted = vigenere_encrypt(text, key)
    print(f"\nЗашифрований текст:\n{encrypted}")
    
    # Дешифрування
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"\nРозшифрований текст:\n{decrypted}")
    
    return encrypted

# ------------------------- РІВЕНЬ 2 -------------------------
def get_clean_text(text):
    """Отримання чистого тексту для аналізу"""
    return ''.join(char.upper() for char in text if char.isalpha())

def calculate_ic(text):
    """Обчислення індексу відповідності"""
    N = len(text)
    if N <= 1:
        return 0
    
    freqs = {}
    for char in text:
        freqs[char] = freqs.get(char, 0) + 1
    
    total = 0
    for count in freqs.values():
        total += count * (count - 1)
    
    ic = total / (N * (N - 1))
    return ic

def find_repeated_sequences(text, seq_length=3):
    """Знаходить повторювані послідовності в тексті та їх позиції"""
    clean_text = get_clean_text(text)
    sequences = {}
    
    for i in range(len(clean_text) - seq_length + 1):
        seq = clean_text[i:i + seq_length]
        if seq in sequences:
            sequences[seq].append(i)
        else:
            sequences[seq] = [i]
    
    return {seq: positions for seq, positions in sequences.items() if len(positions) > 1}

def calculate_spacings(positions):
    """Обчислює відстані між позиціями повторюваних послідовностей"""
    spacings = []
    for i in range(len(positions) - 1):
        for j in range(i + 1, len(positions)):
            spacing = positions[j] - positions[i]
            if spacing > 0:
                spacings.append(spacing)
    return spacings

def find_factors(number, max_factor):
    """Знаходить всі можливі дільники числа до max_factor"""
    factors = []
    for i in range(1, min(number + 1, max_factor + 1)):
        if number % i == 0:
            factors.append(i)
    return factors

def kasiski_examination(text, seq_length=3, max_key_length=20):
    """Повна реалізація методу Касіскі"""
    clean_text = get_clean_text(text)
    sequences = find_repeated_sequences(clean_text, seq_length)
    factor_counts = {}
    
    for seq, positions in sequences.items():
        spacings = calculate_spacings(positions)
        for spacing in spacings:
            factors = find_factors(spacing, max_key_length)
            for factor in factors:
                if factor > 1:
                    factor_counts[factor] = factor_counts.get(factor, 0) + 1
    
    possible_lengths = [(length, count) for length, count in factor_counts.items()]
    possible_lengths.sort(key=lambda x: x[1], reverse=True)
    
    return possible_lengths

def friedman_test(text, max_key_length=20):
    """Реалізація тесту Фрідмана"""
    clean_text = get_clean_text(text)
    ENGLISH_IC = 0.0667
    
    ic_scores = []
    
    for key_length in range(1, max_key_length + 1):
        subsequences = [''] * key_length
        for i, char in enumerate(clean_text):
            subsequences[i % key_length] += char
        
        avg_ic = sum(calculate_ic(seq) for seq in subsequences) / key_length
        ic_scores.append((key_length, avg_ic))
    
    ic_scores.sort(key=lambda x: abs(x[1] - ENGLISH_IC))
    
    return ic_scores

def find_key_length_combined(text, max_key_length=20):
    """Комбінований метод визначення довжини ключа"""
    clean_text = get_clean_text(text)
    kasiski_lengths = kasiski_examination(clean_text, max_key_length=max_key_length)
    friedman_lengths = friedman_test(clean_text, max_key_length=max_key_length)
    
    length_scores = {}
    
    # Додаємо бали від методу Касіскі
    max_kasiski_count = max(count for _, count in kasiski_lengths) if kasiski_lengths else 1
    for length, count in kasiski_lengths:
        length_scores[length] = count / max_kasiski_count
    
    # Додаємо бали від тесту Фрідмана
    english_ic = 0.0667
    for length, ic in friedman_lengths:
        score = 1 - abs(ic - english_ic) / english_ic
        length_scores[length] = length_scores.get(length, 0) + score
    
    best_length = max(length_scores.items(), key=lambda x: x[1])[0]
    
    return best_length

def get_letter_frequencies():
    """Повертає частоти букв англійської мови"""
    return {
        'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127, 
        'F': 0.022, 'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002, 
        'K': 0.008, 'L': 0.040, 'M': 0.024, 'N': 0.067, 'O': 0.075, 
        'P': 0.019, 'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091, 
        'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001, 'Y': 0.020, 
        'Z': 0.001
    }

def find_key_char(subtext):
    """Знаходження одного символу ключа за допомогою частотного аналізу"""
    expected_freqs = get_letter_frequencies()
    best_shift = 0
    min_chi_square = float('inf')
    
    for shift in range(26):
        shifted_freqs = {}
        
        for char in subtext:
            shifted = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            shifted_freqs[shifted] = shifted_freqs.get(shifted, 0) + 1
        
        # Обчислення хі-квадрат
        chi_square = 0
        total = sum(shifted_freqs.values())
        
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            observed_freq = shifted_freqs.get(char, 0) / total if total else 0
            expected_freq = expected_freqs[char]
            chi_square += (observed_freq - expected_freq) ** 2 / expected_freq if expected_freq else 0
        
        if chi_square < min_chi_square:
            min_chi_square = chi_square
            best_shift = shift
    
    return chr((best_shift) % 26 + ord('A'))

def find_key(encrypted_text, key_length):
    """Знаходження повного ключа"""
    clean_text = get_clean_text(encrypted_text)
    substrings = [''] * key_length
    
    for i, char in enumerate(clean_text):
        substrings[i % key_length] += char
    
    key = ''
    print(substrings)
    for substring in substrings:
        key += find_key_char(substring)
    
    return key

def level2_demo(encrypted_text):
    """Демонстрація роботи другого рівня"""
    print("\n" + "="*50)
    print("РІВЕНЬ 2: Криптоаналіз шифру Віженера")
    print("="*50)
    
    # Метод Касіскі
    print("\nМетод Касіскі:")
    kasiski_results = kasiski_examination(encrypted_text)
    print("Топ 5 можливих довжин ключа за методом Касіскі:")
    for length, count in kasiski_results[:5]:
        print(f"Довжина {length}: {count} співпадінь")
    
    # Тест Фрідмана
    print("\nТест Фрідмана:")
    friedman_results = friedman_test(encrypted_text)
    print("Топ 5 можливих довжин ключа за тестом Фрідмана:")
    for length, ic in friedman_results[:5]:
        print(f"Довжина {length}: IC = {ic:.4f}")
    
    # Комбінований результат
    key_length = find_key_length_combined(encrypted_text)
    print(f"\nФінальна оцінка довжини ключа: {key_length}")
    
    # Знаходимо сам ключ
    found_key = find_key(encrypted_text, key_length)
    print(f"Знайдений ключ: {found_key}")
    
    # Розшифровуємо текст знайденим ключем
    decrypted = vigenere_decrypt(encrypted_text, found_key)
    print(f"\nРозшифрований текст:\n{decrypted}")

if __name__ == "__main__":

    # Текст для шифрування
    with open('plain_text.txt', 'r', encoding='utf-8') as file:
        original_text = file.read()
    # original_text = """The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."""
    key = "KEY"
    
    # Демонстрація Рівня 1
    encrypted_text = level1_demo(original_text, key)
    
    # Демонстрація Рівня 2
    level2_demo(encrypted_text)