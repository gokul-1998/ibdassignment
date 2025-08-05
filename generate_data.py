with open('data.txt', 'w') as f:
    for i in range(1, 1001):
        f.write(f"record_{i}\n")

print("Generated data.txt with 1000 records.")
