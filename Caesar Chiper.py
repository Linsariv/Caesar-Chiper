import sys
import string
from datetime import datetime

ALPHABET_LOWER = string.ascii_lowercase
ALPHABET_UPPER = string.ascii_uppercase
ALPH_LEN = 26

def shift_char(c, shift):
    if c in ALPHABET_LOWER:
        idx = ALPHABET_LOWER.index(c)
        return ALPHABET_LOWER[(idx + shift) % ALPH_LEN]
    if c in ALPHABET_UPPER:
        idx = ALPHABET_UPPER.index(c)
        return ALPHABET_UPPER[(idx + shift) % ALPH_LEN]
    return c  # non-letter unchanged

def caesar(text, shift):
    return ''.join(shift_char(c, shift) for c in text)

def save_to_file(mode, plaintext, ciphertext, shift, default_name=None):
    """
    Save result to .txt with the requested formatted layout.
    mode: "ENCRYPT", "DECRYPT", or "AUTO_DECRYPT"
    plaintext: original plain text (or decrypted result for auto)
    ciphertext: original cipher text (or encrypted result)
    shift: integer shift used (or the discovered k for auto)
    """
    # Timestamp without seconds to match example format
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = "==== Caesar Cipher Result ===="
    footer = "=" * 29

    result_text = (
        f"{header}\n"
        f"Date: {timestamp}\n"
        f"Mode: {mode}\n"
        f"Plaintext: {plaintext}\n"
        f"Shift: {shift}\n"
        f"Ciphertext: {ciphertext}\n"
        f"Notes: Shift used = {shift} (classic Caesar)\n"
        f"{footer}\n"
    )

    if default_name is None:
        default_name = f"caesar_{mode.lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

    name = input(f"Simpan hasil ke file (tekan Enter untuk '{default_name}'): ").strip()
    if not name:
        name = default_name

    try:
        with open(name, 'w', encoding='utf-8') as f:
            f.write(result_text)
        print(f"Hasil tersimpan ke '{name}'.\n")
        print("Berikut isi file:")
        print(result_text)
    except Exception as e:
        print("Gagal menyimpan file:", e)

def encrypt_flow():
    plain = input("Masukkan teks yang ingin dienkripsi:\n")
    while True:
        try:
            k = int(input("Masukkan shift (0-25): "))
            k = k % ALPH_LEN
            break
        except ValueError:
            print("Masukkan angka antara 0 sampai 25.")
    cipher = caesar(plain, k)
    print("\nHasil enkripsi:")
    print(cipher)
    
    save_to_file(mode="ENCRYPT", plaintext=plain, ciphertext=cipher, shift=k)
    return

def decrypt_flow():
    cipher = input("Masukkan teks yang ingin didekripsi:\n")
    while True:
        try:
            k = int(input("Masukkan shift (0-25): "))
            k = k % ALPH_LEN
            break
        except ValueError:
            print("Masukkan angka antara 0 sampai 25.")
    plain = caesar(cipher, -k)
    print("\nHasil dekripsi:")
    print("Ciphertext:", cipher)
    print("Plaintext :", plain)

    save_to_file(mode="DECRYPT", plaintext=cipher, ciphertext=plain, shift=k)
    return

def auto_decrypt_flow():
    cipher = input("Masukkan teks terenkripsi (akan dicoba semua shift 0..25):\n")
    candidates = []
    print("\nMencoba semua kemungkinan (0..25):\n")
    for k in range(ALPH_LEN):
        attempt = caesar(cipher, -k)
        candidates.append((k, attempt))
        print(f"[k={k:2}] {attempt}")
    print("\nJika salah satu terlihat benar, masukkan nomor k yang ingin disimpan.")
    while True:
        choice = input("Masukkan k pilihan (atau 'n' untuk batal): ").strip().lower()
        if choice == 'n':
            print("Batal menyimpan.")
            return
        try:
            k_choice = int(choice)
            if 0 <= k_choice < ALPH_LEN:
                selected = dict(candidates)[k_choice] 
                print("\nTeks terpilih:")
                print(selected)
                
                save_to_file(mode=f"AUTO_DECRYPT", plaintext=selected, ciphertext=cipher, shift=k_choice)
                return
        except ValueError:
            pass
        print("Input tidak valid. Masukkan angka antara 0 dan 25 atau 'n'.")

def main():
    print("=== Caesar Cipher Tool ===")
    print("Pilih mode:")
    print("  1. Enkripsi")
    print("  2. Dekripsi (dengan kunci)")
    print("  3. Auto-decrypt (brute force semua kunci)")
    print("  0. Keluar")
    while True:
        choice = input("Masukkan pilihan (0-3): ").strip()
        if choice == '1':
            encrypt_flow()
            break
        elif choice == '2':
            decrypt_flow()
            break
        elif choice == '3':
            auto_decrypt_flow()
            break
        elif choice == '0':
            print("Keluar.")
            return
        else:
            print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    main()

