students = {
    "Alice": 85,
    "Bob": 78,
    "Charlie": 92
}

# Print all students and their marks
print("Student Marks:")
for name, marks in students.items():
    print(name, ":", marks)

# Add a new student
students["David"] = 88

# Update marks
students["Bob"] = 82

# Find a student's marks
search_name = "Alice"
if search_name in students:
    print(f"\n{search_name}'s marks:", students[search_name])
else:
    print(f"\n{search_name} not found")

# Calculate average marks
average = sum(students.values()) / len(students)
print("\nAverage Marks:", average)