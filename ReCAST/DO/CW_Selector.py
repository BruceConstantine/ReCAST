def get_index_atSelectedCWList(cw_list, cw_value):
    # must every one element at the list is unique.
    # if not found the element at the, then return None as error.
    index = 0;
    for item in cw_list:
        if cw_value == item:
            return index;
        index += 1;
    return None;

def generateCWList(cw_list_origin, cw_start, cw_end):
    # if return None, it means user's inpout CW is not at the list.
    # else return the selected segment of user's input.

    result = [];
    index = 0;
    start_index = None;
    end_index   = None;
    for i in cw_list_origin:
        if start_index == None and  i == cw_start:
            start_index = index;
            print("start_index="+str(index))
        #it must get cw_start firstly
        elif (cw_start!= None) and (end_index == None) and (i == cw_end):
            end_index = index;
            print("end_index=" + str(index))
        index+=1;
    # if index has be founded
    #if end_index != None and start_index != None :
        #return cw_list_origin[start_index: end_index+1];
    result = cw_list_origin[start_index: end_index+1];
    if [] == result :
        return None;
    else:
        return result;

 # get the CW length of a unselected list array/list.



def get_slelectedCW_len(cw_list):
    return  cw_list.__len__();

#def getATP_NAT(ATP):


def get_cw_len(cw_list_origin, cw_start, cw_end):
    count = 0;
    start = False ;
    for i in cw_list_origin:
        if start:
            count+=1;
            if i == cw_end:
                start = False;
                break;
        else:
            if i == cw_start:
                start = True;
                count+=1;
    return count;


#k考虑是否允许出现end 比 start大的情况
#NOTE: cw_list here must be original CW list.
#def getRealValuelistBySelectedCW(cw_start, cw_end, cw_list, valuelist):

def getRealValuelistBySelectedCW(cw_start, cw_end, cw_list, valuelist):
    #print("Start of getRealValuelistByCW")
    #print("cw_start=" + str(cw_start) + "cw_end=" + str(cw_end))
    #print("valuelist= " + str(valuelist)  )
    l = cw_list.__len__()
    #print("l =  " + str(l)  )
    index_start = -1
    index_end = -1
    print("--------------")
    for index in range(l):
        print(cw_list[index])
        if cw_list[index] == cw_start :
            index_start = index;
        if cw_list[index] == cw_end :
            index_end = index;
    #print("end of getRealValuelistByCW")
    return valuelist[index_start: index_end +1]


#k考虑是否允许出现end 比 start大的情况
#NOTE: cw_list here must be original CW list.
def getRealValuelistByCW(cw_start, cw_end, cw_list_origin, valuelist):
    #print("Start of getRealValuelistByCW")
    #print("cw_start=" + str(cw_start) + "cw_end=" + str(cw_end))
    #print("valuelist= " + str(valuelist)  )
    l = cw_list_origin.__len__()
    #print("l =  " + str(l)  )
    index_start = -1
    index_end = -1
    print("--------------")
    cw_start_found = False
    cw_end_found = False
    for index in range(l):
        print(cw_list_origin[index])
        if not cw_start_found and cw_list_origin[index] == cw_start :
            index_start = index;
            cw_start_found = True;
        if not cw_end_found and cw_list_origin[index] == cw_end :
            index_end = index;
            cw_end_found = True;
        if cw_end_found and cw_start_found:
            break;
    #print("end of getRealValuelistByCW")
    #print([cw_start, cw_end])
    #print([index_start, index_end +1])
    #print(valuelist[index_start: index_end +1])
    return valuelist[index_start: index_end +1]