#Compress a String Using the Counts of Repeated Characters. Write a Python function to perform basic string compression using the counts of repeated characters.
#Input: "aabcccccaaa" Output: "a2b1c5a3"
def compress_string(s):
    if not s:
        return ""

    result = ""
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result += s[i - 1] + str(count)
            count = 1

    # add the last character group
    result += s[-1] + str(count)
    return result

# Ask user for input
user_input = input("Enter a string to compress: ")
compressed = compress_string(user_input)
print(f"Input String: {user_input}")
print(f"Compressed Output: {compressed}")