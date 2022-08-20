text = input()
words = text.split()
for word in words:
    if word.lower().startswith("www.") or word.lower().startswith("http"):
        print(word)
