str = "Alpaca"

output = ""
for c in str:
    output += chr(ord(c) ^ 7)

print(output)
