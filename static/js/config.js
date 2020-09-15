//variable upgrade
//data = [],  container = document.getElementById('BS_table'), hot;
var table_BS, hot_allow;

var CW1, CW2;
function setBSTableContent(rowname, value) {
    var row;
    if (rowname == 'MBS'){
        row = 0;
    } else if (rowname == 'RBS') {
        row = 1;
    }
    for (var col=0; col<=CW2-CW1; col++ ){
        table_BS.setDataAtCell(row,col,value);
    }
}
function cleanBSTable() {
    for (var col=0; col<=CW2-CW1; col++ ){
        table_BS.setDataAtCell(0,col,"");
    }
    for (var col=0; col<=CW2-CW1; col++ ){
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
    CW1 = cw1; CW2 = cw2;
    var tableHeader = [''];
    for(var i=cw1; i<=cw2; i++){
        tableHeader.push('CW '+i);
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

function pageSubmit(btn) {
    //var btn= document.getElementById('submit')
    var MBS_input= document.getElementById('MBS_input')
    var RBS_input= document.getElementById('RBS_input')
    var templist_BS = table_BS.getData()
    var MBSList = templist_BS[0]
    var RBSList = templist_BS[1]
    MBS_input.value = listStringfy(MBSList)
    RBS_input.value = listStringfy(RBSList)

    var allow_use_binary_list = [] // only 1 or 0
    var templist_Allow = hot_allow.getData()
    var i_max = templist_Allow.length, j_max = 0;
    if(i_max>0)
        j_max = templist_Allow[0].length;
        console.log("j_max="+j_max)
        console.log("j_max="+j_max)
    for (var i_ = 0; i_ < i_max; i_++){
        var templist_Allow_aRow = new Array();
        for (var j_ = 0; j_ < j_max; j_++){
            if (undefined == templist_Allow[i_][j_]){
                console.log("i_,j_=")
                console.log(i_,j_)
                console.log();
            }
           if ( (templist_Allow[i_][j_]).trim().toLowerCase() == 'yes'){
                templist_Allow_aRow.push(1);
           } else {
                templist_Allow_aRow.push(0);
           }
        }
        allow_use_binary_list.push(templist_Allow_aRow);
    }
    var allowTable_input= document.getElementById('allowTable_input')
    // Here is to test if a list of int [1,0,0,0,1,1...] can be send to server.

    //JSON.stringify can keep the origin structure of a int list [[1,1],[2,2]],
    //rather than [1,1,2,2].
    allowTable_input.value = JSON.stringify(allow_use_binary_list);
    console.log(allowTable_input.value)

    __submit(btn)
    //btn.click = '';
    //btn.type = 'submit'
    //btn.click()
}

function initBStable_content(cw_start, cw_end) {
    tableRow_MBS = [];
    tableRow_RBS = [];
    for(var i=cw_start; i<=cw_end; i++){
        tableRow_MBS.push('');
        tableRow_RBS.push('');
    }
    return  [tableRow_MBS,tableRow_RBS];
}

function getBStable_all(cw1, cw2){
    CW1 = cw1; CW2 = cw2;
    var tableHeader = getCWsHeader(cw1,cw2);
    var tableRow_MBS = ['Min. Buffer Stock'];
    var tableRow_RBS = ['Reserve Buffer Stock'];
    for(var i=cw1; i<=cw2; i++){
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
                return aRow
            }())
        )
        })
    return tableRows;
}


function getAUStable_content( cw_start, cw_end, customerList) {
    var rows = customerList.length, cols =  cw_end - cw_start, content = [];
    for ( var i = 0; i < rows; i++){
        var content_row = [];
        for (var j = 0; j <= cols ; j++){
            content_row.push('yes');
        }
        content.push(content_row);
    }
    return content;
}

function getRFHeader_col(cw1, cw2,) {
        list = getCWsHeader(cw1, cw2)
        list.shift(1)
        return list;
}

function getRFtable_content(cw1, cw2) {
    //getPlantATP
    var content_row_plantATP = [78000,62000,4500,130500,71000,80000,80000,165000,160500,161500,88500,80000];
    var content_row_VulATP = [];
    var content_row_PLG = [];
    //handle relation between PLG and VulATP
    var columns = [];
    for (var i=cw1; i <=cw2; i++) {
        columns.push({
            plantATP :  content_row_plantATP[i-cw1],
            VulATP : true,
            PLG : 0
        })
    }
    return columns;
}

BStableConfig  = {
    // data: JSON.parse(JSON.stringify(getBStable_content(12,23))),
    data: initBStable_content(CW_start,CW_end),
    licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
    colHeaders: getBSHeader_col(CW_start,CW_end),
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
    data: getAUStable_content(CW_start,CW_end,customerList_name) ,
    licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
    colHeaders: getBSHeader_col(CW_start,CW_end),
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


window.onload = function () {
    //BS_table
	var hot = new Handsontable( document.getElementById('BS_table'), BStableConfig );
    table_BS = hot
    console.log(hot)
    //hot.container.onmousedown = function(){alert('down')}
    //hot.getDataAtRow(0)

    hot_allow = new Handsontable(document.getElementById('allow_table'), AllowTableConfig);

	var hot3 = new Handsontable(container3 = document.getElementById('RFtable'), {
        data: getRFtable_content(CW_start,CW_end), //JSON.parse(JSON.stringify(getRFtable_content(CW_start,CW_end))),
        // multiColumnSorting: "row",
        rowHeaderWidth: 80,
        colWidths:180,
        autoColumnSize:true,
        colHeaders:  getRFHeader_row(),
        rowHeaders:  getRFHeader_col(CW_start,CW_end),
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