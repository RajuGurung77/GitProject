def main():
    user_string=input("Enter a string: ")
    result=""

    for char in user_string:
        result=char+result
    print (result)

if __name__ == '__main__':
    main()