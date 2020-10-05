from ReCAST.util.Algo import selectChunkAtArr

def test_selectChunkAtArr():
    arr = [9, 10, 11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # r=selectChunkAtArr(10,3,arr)#Correct
    # r=selectChunkAtArr(1,8,arr)#Correct
    # r=selectChunkAtArr(10,9,arr) #Correct
    # r=selectChunkAtArr(11,11,arr) #Correct
    r = selectChunkAtArr(1, 11, arr)  # Correct
    print(r.__str__())
    print(r.firstElement())
    print(r.lastElement())
    print(r.getSelectedArr())
    print(r.get_originArrIndex_startElement())
    print(r.get_originArrIndex_endElement())


def test_sortAffiliateLists():
    CW = ['CW11', 'CW1', 'CW3', 'CW4', 'CW15', 'CW5', 'CW2', 'CW35']  # 8

    plantATP = [
        1, 2, 3, 4, 5, 6, 7, 8
    ]
    NAT_ATP = [
        11, 22, 33, 44, 55, 66, 77, 88
    ]
    # CW.sort() #-> sorted by ascending order

    # sorted({8: 'D', 2: 'B', 3: 'B', 4: 'E', 5: 'A'}) #-> sort dict by its key (asc order).

    # define an lambda function as map callback:
    #  return a tuple with key of CW and value of a pair value of tuple/list
    map_callback_func = lambda x, y, z: (x, (y, z))

    # execute the lambda function as defined:
    # then get an Iterator(also is Iterable) object as result:
    #  parameters:   callback,     x,     y,    z
    r = map(map_callback_func, CW, plantATP, NAT_ATP)

    # get the list value of this iterator
    resultList = list(r);

    # then sort these tuple list by our lambda key:
    #  sorted by the integer at the first tuple element(key) string：
    #  e.g.: 'CW12' -> 12  /  "CW1" -> 1
    resultList.sort(key=lambda cw: int(cw[0][2:]))

    # then the list is sorted, and we can extract the affiliate array list
    # at the second element on these tuple(value):
    CW_list = []
    plantATP_list = []
    NAT_ATP_list = []
    for sorted_CW_tuple in resultList:
        CW_list.append(sorted_CW_tuple[0])  # ('CW1', (2, 22)) -> 'CW1'
        plantATP_list.append(sorted_CW_tuple[1][0])  # ('CW1', (2, 22)) -> (2,22)-> 2
        NAT_ATP_list.append(sorted_CW_tuple[1][1])  # ('CW1', (2, 22)) -> (2,22)-> 22

    print("CW_list=" + str(CW_list))
    print("plantATP_list=" + str(plantATP_list))
    print("NAT_ATP_list=" + str(NAT_ATP_list))
    print("Origin CW=" + str(CW))


    # In python 2.7: It's possible to define a customered comparable/sorting function
    # as one input parameter of sort() function:
    def comp(a1, a2):
        a1 = int(a1[2:]);
        a2 = int(a2[2:]),
        if a1 < a2:
            return 1;
        elif a1 > a2:
            return -1;
        else:  # a1==a2
            return 0;


    # The following are equivalent
    # 1. define a key function as the sorting rule
    def key_callback_getCWNum(arr_ele):
        return int(arr_ele[2:])

    CW.sort(key=key_callback_getCWNum)

    # 2. define lambda function as key
    CW.sort(key=lambda cw: int(cw[2:]))

test_selectChunkAtArr()