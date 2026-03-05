def main():
    s1= input("Enter first string: ")
    s2= input("Enter second string: ")

    s1=s1.replace(" ","").lower()
    s2 = s2.replace(" ", "").lower()

    sorted_s1=sorted(s1)
    sorted_s2=sorted(s2)

    if sorted_s1==sorted_s2:
        print("The strings are anagrams")
    else:
        print("The strings are not anagrams")



if __name__ == '__main__':
    main()