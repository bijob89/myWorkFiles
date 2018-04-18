import itertools

support = int(input("Please enter support value in %: "))
confidence = int(input("Please enter confidence value in %: "))
try:
    add_value = input("Enter a value. Press enter if no value is to be entered. ")
except:
    add_value = None
# if add_value:
#     print(add_value)

f = open('student.csv', 'r')
fc = f.read().strip()
C1 = {}
D = []
transactions = 1        # to be made zero later
for line in fc.split('\n'):
    line_split = line.split()
    # if 'Dalc=5' in line_split:
    transactions += 1
    D.append(line_split)
    for word in line_split:
        if word in C1:
            count = C1[word]
            C1[word] = count + 1
        else:
            C1[word] = 1
    # else:
    #     continue

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

"""Frequent-k-itemset"""

for item in D:
    k = 2
    Ck = {}
j = 0
while(j< 10):
    k = 2
    Ck = {}
    Lk = []
    main_list = []
    for item in D:
        perm_list = list(itertools.permutations(item, r=k))
        for perm_item in perm_list:
            main_list.append(sorted(list(perm_item)))            
    comb_list = list(itertools.combinations(main_list, r=k))
    for list1 in comb_list:
        Ck[list1] = main_list.count(list1)
    for key in Ck:
        if (100 * Ck[key] / transactions) >= support:
            Lk.append([key])

    if Lk != []:
        print("-------------------------CANDIDATE %d-ITEMSET---------------------" % k)
        print("Ck: %s" % Ck)
        print("------------------------------------------------------------------")
    else:
        break
    k += 1
    j += 1