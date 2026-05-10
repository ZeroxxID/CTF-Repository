from pwn import *
from randcrack import RandCrack

# Set log level biar gak spam terminal
context.log_level = 'info'
r = remote('crypto.cbd2026.cloud', 1337)
rc = RandCrack()

def play_roulette(stake, guess):
    """Fungsi pembungkus buat main roulette, bikin kode bersih"""
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'stake: ', str(stake).encode())
    r.sendlineafter(b'number (0-36): ', str(guess).encode())
    
    # Ambil ticket hex
    r.recvuntil(b'ticket id: ')
    ticket = int(r.recvline().strip().decode(), 16)
    return ticket

# --- 1. Data Collection Phase ---
print("[*] Mengumpulkan 624 sampel...")
for i in range(624):
    ticket = play_roulette(1, 0)
    rc.submit(ticket)
    if (i + 1) % 100 == 0:
        print(f"[*] Progress: {i + 1}/624")

print("[+] Status MT19937 sudah di-clone!")

# --- 2. Exploitation Phase ---
while True:
    # Ambil balance tanpa banyak bacot
    r.recvuntil(b'Balance: ')
    balance = int(r.recvuntil(b' credits').replace(b' credits', b'').strip())
    
    if balance >= 50000:
        print("[!] Balance mencukupi, sedang membeli flag...")
        r.sendlineafter(b'> ', b'3')
        print(f"[FLAG] {r.recvall().decode().strip()}")
        break
    
    # Prediksi
    prediction = rc.predict_getrandbits(32) % 37
    
    # Main dengan stake optimal
    stake = min(balance, 5000)
    print(f"[*] Bet: {stake} on {prediction} (Balance: {balance})")
    
    # Kirim taruhan
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'stake: ', str(stake).encode())
    r.sendlineafter(b'number (0-36): ', str(prediction).encode())