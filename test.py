if __name__ == '__main__':

    numbers = [10, 20, 20, 30]
    d = {}
    for num in numbers:
        if num in d:
            d[num] = d[num] + 1
        else:
            d[num] = 1
    print(d)
    # To print maximum number of occurrences from the dictionary
    max = 0
    freq = 0
    for key in d.keys():  # key is actual number 10,20,30
        value = d[key]
        if value > freq:
            max = key
            freq = value
    print(max)
    print(freq)

    # To print maximum number of occurrences from dictionary that contains strings
    line = "hello world hi world hi nepal"
    words = line.split(' ')  # takes the word
    print(words)
    counts = {}
    for word in words:
        if word in counts:
            counts[word] = counts[word] + 1  # checks if word match
        else:
            counts[word] = 1
    print(counts)

    word = 0
    freq = 0
    for key in counts.keys():  # key is actual number 10,20,30
        value = counts[key]
        if value > freq:
            word = key
            freq = value
    print(word)
    print(freq)

    # Set
    num = [3, 1, 2, 2, 5, 3, 4, 4, 5]
    s = set(list)
    print(s)

    # To add into empty list
    output = []
    new_set = set()
    for num in list:
        if num not in output:
            output.append(num)
            new_set.add(num)
    print(output)
    print(new_set)

    # To sort the numbers in set\

    output = []
    for num in list:

        for n in list:
            if n not in output:
                smallest = n
        output.append(smallest)

    print(output)

