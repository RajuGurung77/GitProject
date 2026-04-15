# Simple Python program using list and set

# List (allows duplicates)
fruits_list = ["apple", "banana", "orange", "apple", "mango"]

print("List:")
print(fruits_list)

# Set (removes duplicates automatically)
fruits_set = set(fruits_list)

print("\nSet (duplicates removed):")
print(fruits_set)

# Adding elements
fruits_list.append("grape")
fruits_set.add("grape")

print("\nAfter adding 'grape':")
print("List:", fruits_list)
print("Set:", fruits_set)

# Checking membership
print("\nIs 'banana' in list?", "banana" in fruits_list)
print("Is 'banana' in set?", "banana" in fruits_set)