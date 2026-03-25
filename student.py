# List of student names (can have duplicates)
students = ["Raju", "Sam", "Amit", "Raju", "John", "Amit"]

print("Original List:")
print(students)

# Convert list to set to remove duplicates
unique_students = set(students)

print("\nUnique Students (Set):")
print(unique_students)

# Create a dictionary with student names and their marks
student_marks = {
    "Raju": 85,
    "Sam": 90,
    "Amit": 78,
    "John": 88
}

print("\nStudent Marks (Dictionary):")
for name, marks in student_marks.items():
    print(name, ":", marks)

# Add a new student
student_marks["David"] = 92

# Update marks
student_marks["Amit"] = 80

print("\nUpdated Student Marks:")
print(student_marks)

# Find students who scored above 85
top_students = []

for name, marks in student_marks.items():
    if marks > 85:
        top_students.append(name)

print("\nTop Students (Marks > 85):")
print(top_students)

# Convert top students list to set (just for demo)
top_students_set = set(top_students)

print("\nTop Students as Set:")
print(top_students_set)