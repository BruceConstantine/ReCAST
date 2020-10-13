//variable upgrade
//data = [],  container = document.getElementById('BS_table'), hot;
var table_BS, hot_allow;
//var vaild_input_at_configPage = false;

function setBSTableContent(rowname, value) {
    var row;
    if (rowname == 'MBS'){
        row = 0;
    } else if (rowname == 'RBS') {
        row = 1;
    }
    for (var col=0; col<CW_len; col++ ){
        table_BS.setDataAtCell(row,col,value);
    }
}
function cleanBSTable() {
    for (var col=0; col<CW_len; col++ ){
        table_BS.setDataAtCell(0,col,"");
    }
    for (var col=0; col<CW_len; col++ ){
        table_BS.setDataAtCell(1,col,"");
    }
}
function BS_apply_callback(boxid) {
    var value = '-1' ;
    if (boxid == 'MBS'){
        value = $('#MBS').val();
    } else if (boxid == 'RBS') {
        value = $('#RBS').val();
    }
    setBSTableContent(boxid,value);
}


function getCWsHeader(cw1, cw2){
    return CW_list;
}

function getBSHeader_col_by_CWlist(cw_list_in) {
    var l = cw_list_in.length;
    var tableHeader = [];
    for(var i = 0; i < l; i++) {
        tableHeader.push('CW ' + cw_list_in[i]);
    }
    return tableHeader;
}
function getBSHeader_col(cw1,cw2) {
    CW1 = cw1; CW2 = cw2;
    var tableHeader = [];
    for(var i=cw1; i<=cw2; i++) {
        tableHeader.push('CW ' + i);
    }
    return tableHeader;
}

function getBSHeader_row() {
    return ['Min. Buffer Stock','Reserve Buffer Stock']
}

function getRFHeader_row() {
    return['Plant ATP', 'Vulnearable ATP', 'Possible Gain/Loss']
}

function listStringfy(list) {
    var res_str = '';
    for (var i=0; i<list.length-1; i++) {
        res_str += list[i]+',';
    }
    res_str += list[list.length-1]
    return res_str;
}
/*
function isRunnableInput() {
    if ( !vaild_input_at_configPage ){
        alert("Please check the RBS data at table firstly before generating results.")
        return false;
    } else {
        return true;
    }
}*/


function pageSubmit(element) {
    //var btn= document.getElementById('submit')
    var MBS_input= document.getElementById('MBS_input')
    var RBS_input= document.getElementById('RBS_input')
    var templist_BS = table_BS.getData()
    var MBSList = templist_BS[0]
    var RBSList = templist_BS[1]
    MBS_input.value = listStringfy(MBSList)
    RBS_input.value = listStringfy(RBSList)

    var problem_cells = []
    var allow_use_binary_list = [] // only 1 or 0
    var templist_Allow = hot_allow.getData()
    var i_max = templist_Allow.length, j_max = 0;
    if ( i_max > 0 ) {
        j_max = templist_Allow[0].length;
        console.log("i_max=" + i_max);
        console.log("j_max=" + j_max);
    }
    for (var i_ = 0; i_ < i_max; i_++){
        var templist_Allow_aRow = new Array();
        for (var j_ = 0; j_ < j_max; j_++){
           if (undefined == templist_Allow[i_][j_]){
                console.log("i_="+i_+",j_="+j_);
                console.log();
           }
           var cell_value = (templist_Allow[i_][j_]).trim().toLowerCase() ;
           if ( cell_value == 'yes' ) {
                templist_Allow_aRow.push(1);
           } else {
                templist_Allow_aRow.push(0);
                if ( cell_value != 'no'){
                    problem_cells.push([i_,j_]);
                }
           }
        }
        allow_use_binary_list.push(templist_Allow_aRow);
    }
    var isRunGurobi = true;
    var pc_len = problem_cells.length;
    if ( pc_len != 0 ) {
        var problem_cells_index_str = "";
        var index = 0;
        for (var i = 0 ; i < pc_len; i++) {
            var row_i = customerList_name[problem_cells[i][0]];
            var col_j = CW_list[problem_cells[i][1]];
            problem_cells_index_str += "["+row_i+", CW"+col_j+"]";
        }
        isRunGurobi = confirm("Please check the cell value at: " + problem_cells_index_str+"\n" + "any non-'yes' value shall be considered as 'no'."+"\n"+"Continue to run?");
        //alert("isRunGurobi="+isRunGurobi)
    }
    if (isRunGurobi) {
        var allowTable_input= document.getElementById('allowTable_input')
        // Here is to test if a list of int [1,0,0,0,1,1...] can be send to server.

        //JSON.stringify can keep the origin structure of a int list [[1,1],[2,2]],
        //rather than [1,1,2,2].
        allowTable_input.value = JSON.stringify(allow_use_binary_list);
        console.log(allowTable_input.value)
        console.log("Before running")
        /*
        var url_post = ''
        post((url_post, {"maxdelay":10,
                "MBS":"",
                "RBS":"",
                "bin_use_from_stock":""
                } ,function () {
            //empty
        }))
        */
        // window.location.href='/run/';
        // $("#submit_btn").submit();

        /*Error! here!*/
        __submit(element);

        /*Error! here!*/
        //window.location.href='/run/';

        //btn.click = '';
        //btn.type = 'submit'
        //btn.click()
    }
}

//function initBStable_content(cw_start, cw_end) {}

function initBStable_content(cw_list) {
    tableRow_MBS = [];
    tableRow_RBS = [];
    var l = cw_list.length;
    for(var i=0; i<l; i++){
        tableRow_MBS.push('');
        tableRow_RBS.push('');
    }
    return  [tableRow_MBS,tableRow_RBS];
}

//function getBStable_all(cw1, cw2){}

function getBStable_all(cw_list_in){
    var tableHeader = cw_list_in;
    var tableRow_MBS = ['Min. Buffer Stock'];
    var tableRow_RBS = ['Reserve Buffer Stock'];
    var l = cw_list_in.length;
    for(var i = 0 ; i < l; i++){
        tableRow_MBS.push('');
        tableRow_RBS.push('');
    }
    return table_BS = [
        tableHeader,
        tableRow_MBS,
        tableRow_RBS
    ];
}
//Allowance of Using from Stock (AUS)
function getAUStable(cw1, cw2, customerList){
    var tableHeader = getCWsHeader(cw1,cw2);
    var tableRows = [];
    tableRows.push(tableHeader);
    //Note: customerList must be the type of list, string list.
    customerList.forEach(function (item) {
        //item here is type of string
        tableRows.push(
            //anonynous function
            (function (){
                var aRow = [item]
                //alert("aRow= "+aRow+".")
                for(var i=cw1; i<=cw2; i++){
                    aRow.push('Yes');
                }
                return aRow;
            }())
        );
        })
    return tableRows;
}


function getAUStable_content( CW_list, customerList) {
    var rows = customerList.length, cols =  CW_list.length, content = [];
    for ( var i = 0; i < rows; i++){
        var content_row = [];
        for (var j = 0; j < cols ; j++){
            content_row.push('yes');
        }
        content.push(content_row);
    }
    return content;
}

/* function here standing-by for forture calling
function getRFHeader_col(CW_list_in) {
        var list = CW_list_in
        list.shift(1)
        return list;
}
*/

//@pre-condition: plantATP must represents the time horizon within 'cw_list';
function getRFtable_content(cw_list_in) {
    //getPlantATP
    var content_row_plantATP = plantATP; //test data :[78000,62000,4500,130500,71000,80000,80000,165000,160500,161500,88500,80000];
    var content_row_VulATP = [];
    var content_row_PLG = [];
    //handle relation between PLG and VulATP
    var columns = [];
    var l = cw_list_in.length;

    for (var i = 0; i < l; i++) {
        columns.push({
            plantATP :  content_row_plantATP[i],
            VulATP : true,
            PLG : 0
        });
    }
    return columns;
}
function triggerRFtable(e){
    RFtable = document.getElementById('RFtable');
     /*RFtable.hidden = ! RFtable.hidden ;*/
    var display = RFtable.style.display;
    if (display == 'none'){
         RFtable.style.display = 'block';
    } else {
         RFtable.style.display = 'none';
    }

}

BStableConfig  = {
    // data: JSON.parse(JSON.stringify(getBStable_content(12,23))),
    data: initBStable_content(CW_list),
    licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
    colHeaders: getBSHeader_col_by_CWlist(CW_list),
    //The number of 'rowHeaders'here must be consistent with that of 'data' property
    rowHeaders: getBSHeader_row(),
    //stretchH:"none",
    rowHeaderWidth: 180,
    mergeCells: false,//合并单元格
    contextMenu:false,//使用菜单
    headerTooltips: {
        rows: false,
        columns: true,
        onlyTrimmed: true
    }
}
AllowTableConfig={
    data: getAUStable_content(CW_list,customerList_name) ,
    licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
    colHeaders: getBSHeader_col_by_CWlist(CW_list),
    // Refactoring rowHeaders here.
    rowHeaders: customerList_name,//['A_4006047_WF00','B_WF00','C_WF00'],
    //stretchH:"none",
   //@@@@@@@@@@@@@@@@@@@@@ multiline: true,@@@@@@@@@@@@@@@@@
    rowHeaderWidth: 180,
    mergeCells: false,//合并单元格
    contextMenu:false,//使用菜单
    headerTooltips: {
        rows: false,
        columns: true,
        onlyTrimmed: true
  }
}

/**TODO: This is Testing，Two things need to improved:
 * 1. Remove console.log()
 * 2. 出现两个scroll bar，如何清除一个保留内部的一个是要解决的问题：
 *      现在可以解决这个问题但是会出现另一个问题：
*       那就是无法把页面中所有的表格都展现->它只展示了没有overflow掉的
 *       对于overflow掉的那一部分，当拖动scrollbar的时候就没法展示了
 *       猜测： 可能是HandsonTable.js是使用了懒加载的机制，当
 *              overflow的那一部分不出现的时候就不加载，当且仅当用户托动
 *              之前的scroll bar时，被hidden的那一部分才会出现
 * */

/*
/////@@@@@@@@@@这里就是那个删除Handsontable自动生成的css属性的那一块代码@@@@@@@@@@@
$(document).ready( function(){
    //initialize 'handsontable' scrollable table structure:
    // remove 'ht_master' classname so to leave only one sroll-bar under table div
    var ht_master = document.getElementsByClassName( "ht_master")

    if( null != ht_master &&  ht_master.length>0 ){
        [...ht_master].forEach(function(table_div_item){
            console.log(table_div_item.classList)
            table_div_item.classList.remove("ht_master")
            console.log(table_div_item.classList)
        })
     //alert(ht_master.length)
    }
})
 */

function checkRBS() {
    var RBS_list = table_BS.getData()[1]
    var sum_RBS_list = getArrSum(RBS_list)
    var sum_plantATP = getArrSum(plantATP)
    var sum_CMAD = 0;
    customerList_CMAD.forEach( function(item) {
        sum_CMAD += getArrSum(item)
    })
    var sum_threshold_value = sum_plantATP - sum_CMAD;
    if (sum_RBS_list > sum_plantATP) {
        alert("Your input value for RBS is too big.");
    } else {
        if (sum_RBS_list > sum_threshold_value) {
            //vasum_thresholdild_input_at_configPage = false;
            //print text here.
            var printText = '*Note: If the sum of Reserve Buffer Stock is bigger than ' + (sum_threshold_value) + ' possibly ReCAST would not allocate product to all the CMADs.'
            document.getElementById('threshold_text').innerText = printText;
        } else {
            //vaild_input_at_configPage = true;
            //correct input
            //document.getElementById('threshold_text').innerText = "";
            alert("This is a applicable input.");
        }
    }
    var sum_RBS_span = document.getElementById("sum_RBS")
    sum_RBS_span.innerText = sum_RBS_list;
}


// arr must be a list of integer or ineteger string, if there is an exception cell at the list, it cannot to work　
function getArrSum(arr){
    var l = arr.length;
    var lastElement = arr[l-1];
    //if not number type and content is not a number, it should return 0 as result
    if ( lastElement == undefined || lastElement == null || lastElement == ""
            || ( typeof (lastElement) != "number" &&  !new RegExp("^[0-9]*$").test(lastElement.trim()) )
    ) {
        return 0;
    } else {
        return eval(arr.join("+"));
    }
}

window.onload = function () {

    //BS_table
	var hot = new Handsontable( document.getElementById('BS_table'), BStableConfig );
    table_BS = hot
    console.log(table_BS)
    //hot.container.onmousedown = function(){alert('down')}
    //hot.getDataAtRow(0)

    hot_allow = new Handsontable(document.getElementById('allow_table'), AllowTableConfig);

	var hot3 = new Handsontable( document.getElementById('RFtable'), {
        data: getRFtable_content(CW_list), //JSON.parse(JSON.stringify(getRFtable_content(CW_start,CW_end))),
        // multiColumnSorting: "row",
        rowHeaderWidth: 100,
        colWidths:180,
        autoColumnSize:true,
        colHeaders:  getRFHeader_row(),
        rowHeaders:  getBSHeader_col_by_CWlist(CW_list),
        licenseKey:  'ab3e4-1bee8-ed01c-4d94b-08cfe',
        contextMenu: false,//使用菜单
        columnSorting: false,
        multiColumnSorting: false,
        columns: [{
              data: 'plantATP'
            }, {
              data: 'VulATP',
              type: 'checkbox',
              label: {
                position: 'after',
                checkedTemplate: 'yes',
                uncheckedTemplate: 'no',
                value: ' apply' // Read value from row object
              },
            }, {
              data: 'PLG',
              type: 'numeric'
            },
        ],
    });

    hot3.addHook('afterOnCellMouseDown', function(event, coords){
        hot3.setCellMeta(coords.row, coords.col, 'className', hot2.getCellMeta(coords.row, coords.col).className + ' clk-td');
    });

    /*********** check input is infeasible or not ************/

    //display data for <span> of checking infeasible case input.
    var sum_RBS_span = document.getElementById("sum_RBS")
    var sum_threshold_span = document.getElementById("sum_threshold")
    var sum_plantATP = getArrSum(plantATP)
    var sum_CMAD = 0;
    customerList_CMAD.forEach( function(item) {
        sum_CMAD += getArrSum(item)
    })
    var sum_threshold_value = sum_plantATP - sum_CMAD;
    var RBS_list = table_BS.getData()[1]
    var sum_RBS_list = getArrSum(RBS_list)

    sum_threshold_span.innerText = sum_threshold_value;
    sum_RBS_span.innerText = sum_RBS_list;


    /*
    ---Testing---

    	var data2 = [1,12,2,3,4],  container2 = document.getElementById('example2'), hot3;

hot2 = new Handsontable(container2, {
  data: JSON.parse(JSON.stringify(data2)),
    licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
    mergeCells:true,//合并单元格
    contextMenu: false,//使用菜单
    rowHeaders: false,
    colHeaders: false,
    //readOnly:true, // column redy only
     mergeCells: [
        {row: 1, col: 1, rowspan: 3, colspan: 3},
        {row: 3, col: 4, rowspan: 2, colspan: 2},
        {row: 5, col: 6, rowspan: 3, colspan: 3}
    ],
    columns: [
    {
      editor: Handsontable.editors.TextEditor,
      renderer: Handsontable.renderers.NumericRenderer,
      validator: Handsontable.validators.NumericValidator
    }
  ]
});
var a;
    hot2.addHook('afterOnCellMouseDown', function(event, coords){
        a =  this;
        hot2.setCellMeta(coords.row, coords.col, 'className', hot2.getCellMeta(coords.row, coords.col).className + ' clk-td');
    });
*/
}