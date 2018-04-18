support = int(input("Please enter support value in %: "))
confidence = int(input("Please enter confidence value in %: "))

f = open('student.csv', 'r')
fc = f.read().strip()
C1 = {}
D = []
transactions = 1        # to be made zero later
for line in fc.split('\n'):
    line_split = line.split()
    if 'Dalc=5' in line_split:
        transactions += 1
        D.append(line_split)
        for word in line_split:
            if word in C1:
                count = C1[word]
                C1[word] = count + 1
            else:
                C1[word] = 1
    else:
        continue

print("--------------------CANDIDATE 1-ITEMSET------------------------- ")
print(C1)
print("-----------------------------------------------------------------")

"""Frequent-1-itemset"""

L1 = []
for key in C1:
    if (100 * C1[key] / transactions) >= support:
        L1.append([key])
        
print("----------------------FREQUENT 1-ITEMSET-------------------------")
print(L1)
print("-----------------------------------------------------------------")
