def select_cw_arr(cw_start, cw_end, origin_cw_list):
    return selectChunkAtArr(cw_start, cw_end, origin_cw_list);

# Here the algorithm created for selecting CWs.
def selectChunkAtArr(start_element, end_element, arr):
    #The start element must the first element matching to the value for start_elment.
    #And the end element must the next following element behind of the start_element matching to end_elment.
    start_element_found = False;
    end_element_found = False;
    start_index = None;
    end_index = None;

    #create a inner class here for better OOD.
    class SelectedArr(object):
        def __init__(self,start_index_in, end_index_in, arr_in):
            self.__start_index = start_index_in;
            self.__end_index = end_index_in;
            self.__arr = arr_in;
        def firstElement(self):
            return self.__arr[0];
        def lastElement(self):
            l = len(self.__arr)
            return self.__arr[l-1];
        def get_originArrIndex_startElement(self):
            return self.__start_index;
        def get_originArrIndex_endElement(self):
            return self.__end_index;
        def getSelectedArr(self):
            return self.__arr;
        def __str__(self):
            return  "start_index = "+ str(self.__start_index) \
                    + ", end_index = "+ str(self.__end_index)\
                    + ", arr = " + str(self.__arr);

    index_count = 0;
    for item in arr:
        if not start_element_found :
            if item == start_element:
                start_index = index_count;
                start_element_found = True;
        else: # start_element_found == True
            if item == end_element and not end_element_found:
                end_index = index_count;
                end_element_found = True; #end_element_found can be ommit
                break;
        index_count += 1;
    #User's input value are out of range.
    # after one pass traverse of the list, if CW_end > max(cw_list), or
    # CW_start < the fist_beginning min(cw_list), then throw an error.
    #cw_end > cw_list_origin[max_index] or cw_start < cw_list_origin[0]:
    return SelectedArr(start_index, end_index,arr[start_index : end_index+1])


# 三个数组排序，需要将第一个数组作为主键进行排序，其余的俩数组是affiliate数组（从属数组），必须与第一个数组保持对应关系
def sortAffiliateLists(sortingRule, key_list, value_list1, value_list2,value_list3):
    map_callback_func = lambda x, y, z: (x, (y, z))
    r = map(map_callback_func, key_list, value_list1, value_list2)
    resultList = list(r);
    resultList.sort(key=sortingRule)
