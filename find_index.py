#Write a Python function to find the first non-repeating character in a given string and return its index. Input: "swiss" Output: 1 (for 'w' in "swiss")
s = input("Enter a string: ")

for i in range(len(s)):
    if s.count(s[i]) == 1:
        print(i)
        break
else:
    print(-1)