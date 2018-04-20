import itertools

support = int(input("Please enter support value in %: "))
confidence = int(input("Please enter confidence value in %: "))
try:
    add_value = input("Enter a value. Press enter if no value is to be entered. ")
except:
    add_value = None

def generate_all_asscoiation_rules(C1, D, transactions):

    support_value = support/ 100.0 * transactions
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

    k = 2
    L = []
    main_dict = {}
    while(True):
        Ck = {}
        Lk = []
        comb_list = itertools.combinations(L1, r=k)
        for item in (comb_list):
            item_list = []
            for i in range(len(item)):
                item_list.append(item[i][0])
            item_list = sorted(item_list)
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
        k += 1

    num = 1
    for items in L:
        if add_value_flag:
            if add_value not in items:
                continue
        length = len(items) - 1
        if length > 1:
            temp_dict = {}
            temp_dict = main_dict['C' + str(length)]
            perm_itemsets = list(itertools.combinations(items, r=length))
            for li in perm_itemsets:
                missing_item = list(set(items) - set(list(li)))
                other_item = sorted(list(li))
                missing_percentage = support_value/C1[missing_item[0]]
                CK = temp_dict[tuple(other_item)]
                other_percentage = support_value/CK
                count = len(missing_item)
                m_count = len(missing_item)
                o_count = len(other_item)
                if count == 1:
                    key = missing_item[0]
                    numerator = C1[key]
                else:
                    key = 'C' + str(count)
                    temp = main_dict[key]
                    numerator = temp[tuple(sorted(missing_item))]
                missing_support = numerator / transactions * 100
                print("Rule#  %d : %s ==> %s %d %d" %(num, missing_item, other_item, missing_support, missing_percentage * 100))
                num += 1
                count = len(other_item)
                if count == 1:
                    key = other_item[0]
                    numerator = C1[key]
                else:
                    key = 'C' + str(count)
                    temp = main_dict[key]
                    numerator = temp[tuple(sorted(other_item))]
                other_support = numerator/ transactions * 100
                print("Rule#  %d : %s ==> %s %d %d" %(num, other_item, missing_item, other_support, other_percentage * 100))
                num += 1
        else:
            missing_item = items[0]
            other_item = items[1]
            temp_dict = main_dict['C2']
            missing_percentage = temp_dict[tuple(sorted([other_item, missing_item]))] / C1[other_item]
            other_percentage = temp_dict[tuple(sorted([other_item, missing_item]))] / C1[missing_item]
            print("Rule#  %d : [%s] ==> [%s] %d %d" %(num, missing_item, other_item, C1[missing_item]/transactions * 100, missing_percentage * 100))
            num += 1
            print("Rule#  %d : [%s] ==> [%s] %d %d" %(num, other_item, missing_item, C1[other_item]/transactions * 100, other_percentage * 100))
            num += 1

add_value_flag = False
f = open('testing.csv', 'r')
fc = f.read().strip()
C1 = {}
D = []
transactions = 0        # to be made zero later
if not add_value:
    print('This')
    for line in fc.split('\n'):
        line_split = line.split(',')
        transactions += 1
        D.append(line_split)
        for word in line_split:
            if word in C1:
                count = C1[word]
                C1[word] = count + 1
            else:
                C1[word] = 1
else:
    add_value_flag = True
    for line in fc.split('\n'):
        line_split = line.split(',')
        if add_value in line_split:
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

generate_all_asscoiation_rules(C1, D, transactions)