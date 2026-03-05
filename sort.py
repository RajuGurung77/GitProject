list=[1,2,3,4,5,3]
#output=[1,2,4,5]
output=[]
value=3
for num in list:
    if num !=value:
        output.append(num)
print(output)
