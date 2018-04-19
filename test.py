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
transactions = 0        # to be made zero later
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
support_value = support/ 100.0 * transactions
print(len(D) == transactions)
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

'''
k = 2
L = []
main_dict = {}
while(True):
    Ck = {}
    Lk = []
    main_list = []
    for item in D:
        perm_list = list(itertools.combinations(item, r=k))
        
        for perm_item in perm_list:
            main_list.append('\t'.join(sorted(list(perm_item))))
    
    comb_list = list(set(main_list))
    for item1 in comb_list:
        Ck[item1] = main_list.count(item1)
    
    for key in Ck:
        if (100 * Ck[key] / transactions) >= support:
            Lk.append(key.split('\t'))
    if Lk != []:
        L += Lk
        print("----------------------FREQUENT %d-ITEMSET-------------------------" % k)
        print(Lk)
        print("-----------------------------------------------------------------")
    else:
        break
    main_dict['C' + str(k)] = Ck
    k += 1

print(L)
'''
#############################################################################

# '''
k = 2
L = []
main_dict = {}
while(True):
    Ck = {}
    Lk = []
    main_list = []
    
    comb_list = itertools.combinations(L1, r=k)
    
    for item in (comb_list):
        print('item:', item)
        item_list = []
        for i in range(len(item)):
            item_list.append(item[i][0])
        item_list = sorted(item_list)
        print(item_list)
        count = 0
        for line in D:
            if set(item_list).issubset(set(line)):
                count += 1
            else:
                continue
        Ck[tuple(item_list)] = count
        if count >= support_value:
            Lk.append(item_list)
    if Lk != []:
        L += Lk
        print("----------------------FREQUENT %d-ITEMSET-------------------------" % k)
        print(Lk)
        print("-----------------------------------------------------------------")
    else:
        break
    main_dict['C' + str(k)] = Ck
    print('Reached here')
    k += 1
# '''

#############################################################################

num = 1
for items in L:
    length = len(items) - 1
    if length > 1:
            
        temp_dict = {}
        temp_dict = main_dict['C' + str(length)]

        perm_itemsets = list(itertools.combinations(items, r=length))
        for li in perm_itemsets:
            missing_item = list(set(items) - set(list(li)))
            other_item = sorted(list(li))
            missing_percentage = support_value/C1[missing_item[0]]   #((support/100) * transactions)
            CK = temp_dict[tuple(other_item)]
            other_percentage = support_value/CK  #((support/100) * transactions)
            print("Rule#  %d : %s ==> %s %d %d" %(num, missing_item, other_item, support, missing_percentage * 100))
            num += 1
            print("Rule#  %d : %s ==> %s %d %d" %(num, other_item, missing_item, support, other_percentage * 100))
            num += 1
    else:
        missing_item = items[0]
        other_item = items[1]
        missing_percentage = support_value/C1[missing_item]  #((support/100) * transactions)
        other_percentage = support_value/C1[other_item]  #((support/100) * transactions)
        print("Rule#  %d : %s ==> %s %d %d" %(num, missing_item, other_item, support, missing_percentage * 100))
        num += 1
        print("Rule#  %d : %s ==> %s %d %d" %(num, other_item, missing_item, support, other_percentage * 100))
        num += 1