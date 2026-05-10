import base64

# Token enterprise_gold
token = "GdmLYgZZbUqtTgf2NGkd7IupX1ORRmFx_nMHup3cC9MRZHKHdKkyVrUswqRvmr3wsc_RrOPb5xMa2uc" 
tokenPlain = b"item=enterprise_gold&price=004800&buyer=guest&ship=standard" 

# Target Payload
targetPlain = b"item=celestial_waifu&price=000000&buyer=guest&ship=standard"

# Nambah padding "=" supaya decode aman
cipher = base64.urlsafe_b64decode(token + '=' * (-len(token) % 4))

# XOR buat dapetin keystream
# K = C ^ P
keystream = bytes([c ^ p for c, p in zip(cipher, tokenPlain)])

# XOR keystream dengan target payload buat dapetin ciphertext baru
# C_new = P_new ^ K
newCipher = bytes([k ^ p for k, p in zip(keystream, targetPlain)])

# Buat token untuk celestial_waifu
newToken = base64.urlsafe_b64encode(newCipher).decode().rstrip('=')

print(f"Token: {newToken}")