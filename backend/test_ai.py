from ai import ask_gemini


question = input("You: ")

answer = ask_gemini(question)

print()
print("ZENO:")
print(answer)