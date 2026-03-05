def main():
    user_string=input("Enter a string: ").replace(" ","").lower()
    result=""
    dupes=set()

    for char in user_string:
        if char not in dupes:
            result=result+char
            dupes.add(char)
    print(result)
if __name__ == '__main__':
    main()