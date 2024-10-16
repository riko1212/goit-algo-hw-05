import timeit

def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0: 
        return -1
    
    bad_char = {}
    
    for i in range(m):
        bad_char[pattern[i]] = i
    
    s = 0 
    while s <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            return s
        else:
            shift = j - bad_char.get(text[s + j], -1)
            s += max(1, shift)
    
    return -1

def knuth_morris_pratt_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0: return -1
    lps = [0] * m
    j = 0
    
    def compute_lps_array(pattern, m, lps):
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

    compute_lps_array(pattern, m, lps)
    i = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp_search(text, pattern, prime=101):
    m = len(pattern)
    n = len(text)
    if m == 0: return -1
    d = 256
    p_hash = 0
    t_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * d) % prime
    
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % prime
        t_hash = (d * t_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:
                t_hash += prime
    return -1

def measure_time(text, pattern, search_func):
    timer = timeit.Timer(lambda: search_func(text, pattern))
    return timer.timeit(number=10)  # Виконуємо 10 повторень для більш точного вимірювання

def main():
    with open('article1.txt', 'r', encoding='utf-8') as file:
        text1 = file.read()

    with open('article2.txt', 'r', encoding='utf-8') as file:
        text2 = file.read()

    existing_substring = text1[:30]  # Перші 30 символів першого файлу
    non_existing_substring = "ThisSubstringDoesNotExistInTheText"

    bm_time_existing = measure_time(text1, existing_substring, boyer_moore_search)
    bm_time_non_existing = measure_time(text1, non_existing_substring, boyer_moore_search)

    kmp_time_existing = measure_time(text1, existing_substring, knuth_morris_pratt_search)
    kmp_time_non_existing = measure_time(text1, non_existing_substring, knuth_morris_pratt_search)

    rk_time_existing = measure_time(text1, existing_substring, rabin_karp_search)
    rk_time_non_existing = measure_time(text1, non_existing_substring, rabin_karp_search)

    bm_time_existing_2 = measure_time(text2, existing_substring, boyer_moore_search)
    bm_time_non_existing_2 = measure_time(text2, non_existing_substring, boyer_moore_search)

    kmp_time_existing_2 = measure_time(text2, existing_substring, knuth_morris_pratt_search)
    kmp_time_non_existing_2 = measure_time(text2, non_existing_substring, knuth_morris_pratt_search)

    rk_time_existing_2 = measure_time(text2, existing_substring, rabin_karp_search)
    rk_time_non_existing_2 = measure_time(text2, non_existing_substring, rabin_karp_search)

    print("Результати для тексту 1:")
    print(f"Боєр-Мур: Існуючий: {bm_time_existing:.6f}, Неіснуючий: {bm_time_non_existing:.6f}")
    print(f"Кнут-Морріс-Пратт: Існуючий: {kmp_time_existing:.6f}, Неіснуючий: {kmp_time_non_existing:.6f}")
    print(f"Рабін-Карп: Існуючий: {rk_time_existing:.6f}, Неіснуючий: {rk_time_non_existing:.6f}")

    print("\nРезультати для тексту 2:")
    print(f"Боєр-Мур: Існуючий: {bm_time_existing_2:.6f}, Неіснуючий: {bm_time_non_existing_2:.6f}")
    print(f"Кнут-Морріс-Пратт: Існуючий: {kmp_time_existing_2:.6f}, Неіснуючий: {kmp_time_non_existing_2:.6f}")
    print(f"Рабін-Карп: Існуючий: {rk_time_existing_2:.6f}, Неіснуючий: {rk_time_non_existing_2:.6f}")

if __name__ == "__main__":
    main()
