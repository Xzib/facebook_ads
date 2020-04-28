def campare_values(list_of_tuples):
    page_list = []
    sum_of_amount_list = []
    for i, val in enumerate(list_of_tuples):
        amount = val[2]
        # print(amount)
        for j in range(i+1,len(list_of_tuples)):
            # print(j)
            # print(list_of_tuples[j][1])
            if val[1] == list_of_tuples[j][1]:
                if val[1] not in page_list:
                    page_list.append(val[1])
                amount += list_of_tuples[j][2]
        sum_of_amount_list.append(amount)    
    sum_of_pages = list(zip(page_list,sum_of_amount_list))
    return sum_of_pages    


if __name__ == "__main__":
    val1 = [i for i in range(11)]
    val2 = [1,2,3,1,5,6,2,1,8,3]
    val3 = [i for i in range(11)]
    vals = list(zip(val1,val2,val3))
    print(vals)
    x = campare_values(vals)
    print(x)