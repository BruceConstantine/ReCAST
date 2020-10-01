var targetScenario = null;


window.onload = function () {
    function getBSHeader_col_by_CWlist(cw_list_in) {
        var l = cw_list_in.length;
        var tableHeader = [];
        for(var i = 0; i < l; i++) {
            tableHeader.push('CW ' + cw_list_in[i]);
        }
        return tableHeader;
    }

    function getHeader_row() {
        //return ['Plant ATP','Customer1 ','Customer 2', 'Customer 3']
        var result = ['Plant ATP'];
        customerNameList.forEach(function (item) {
            result.push( item );
        });
        return result;
    }


    function fillingTable(scenariosCustomerList_CMAD) {
        var tableID_list = [];
        ////TODO: testing here: check if the sequence of scenariolist at webpage is same as the sequence of this for loop
        ////ASSET:Scenario Number is always bigger 1 than scenario index.
        for(var i=1 ; i <= scenarioNumber; i++){
            tableID_list.push('sce-tab-'+i);
        }

        for(var i=0; i < scenarioNumber; i++){
            /*
            console.log("scenariosCustomerList_CMAD[i]="+ scenariosCustomerList_CMAD[i])
            console.log("i="+i)
            */
            //deep copy
            customerList_CMAD_with_PlantATP = scenariosCustomerList_CMAD[i].concat()
            customerList_CMAD_with_PlantATP.unshift(plantATP);

            var container = document.getElementById(tableID_list[i]), hot;
            hot = new Handsontable(container, {
                data:  customerList_CMAD_with_PlantATP, //JSON.parse(JSON.stringify(data1)),
                licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
                mergeCells:true,//合并单元格
                contextMenu: false,//使用菜单
                readOnly: true,
                rowHeaders: getHeader_row(),
                colHeaders: getBSHeader_col_by_CWlist(CW_list),
                rowHeaderWidth: 180,
                colWidths: 60,
                width:"100%",
                height: 150,
                rowHeights:23,
                headerTooltips: {
                    rows: false,
                    columns: true,
                    onlyTrimmed: true
                  }
            });
            hot.addHook('afterOnCellMouseDown', function(event, coords){
                 hot.setCellMeta(coords.row, coords.col, 'className', hot.getCellMeta(coords.row, coords.col).className + ' clk-td');
            });
        };
    }


    function createDataPanelConfig(xAxis_data, content_series, legend_list) {
        return {
            // Define margin-left (x), margin-top (y), margin-right (x2), margin-button (y2), at grid.
            grid:{
                x:'45px',
                y:'25px',
                x2:'45px',
            },
            //width:900,
            // title: { '' },
            // 定义样式和数据
            backgroundColor: '#FBFBFB',
            tooltip: {
                //trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#6a7985'
                    }
                }
            },
            legend: {
                data: legend_list
            },
            calculable: true,
            xAxis: [{
                axisLabel: {
                    rotate: 0,//30,
                    interval: 0
                },
                axisLine: {
                    lineStyle: {
                        color: '#222'
                    }
                },
                type: 'category',
                boundaryGap: false,
                data: xAxis_data
            }],
            yAxis: [{
                type: 'value',
                axisLine: {
                    lineStyle: {
                        color: '#222'
                    }
                }
            }],
            series: content_series
        };
    }

    function createSeriesContent_dictList(scenario_index,customerNameList,customerList_CMAD){
        var result = []
        var customerNumber = customerNameList.length
        for (var i = 0 ; i < customerNumber; i++) {
            result.push({
                name: customerNameList[i],
                type: 'line',
                symbol: 'none', //--> It means only mouse hover on it, then the data label can be displayed
                smooth: 0.168,
                color: (function(){     //['#66AEDE','#9911E1','#19B1D2'],
                    colorDict=[0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']
                    color='#'
                    for (var i = 0 ; i < 6; i++) {
                        color_bit = parseInt(Math.random()*100%16)
                        color += colorDict[color_bit]
                    }
                    return color;
                })(),
                data: customerList_CMAD[scenario_index][i],
                label: {
                    normal: {
                        show:      true,
                        position: 'top'
                    }
                }
            });
        }
        return result;
    }

    //'scenario_index' always less 1 than its number(No.)
    function updateDataPanel(scenario_index) {
        var xAxis_data = [], content_series = [], legend_list = [];

        var config_seriesContent_dictList = createSeriesContent_dictList(scenario_index,customerNameList,customerList_CMAD)
        var config_xAxis_data = CW_list;

        legend_list    = customerNameList;
        xAxis_data     = config_xAxis_data
        content_series = config_seriesContent_dictList
        var config = createDataPanelConfig(xAxis_data, content_series, legend_list);
        myChart.setOption(config);
    }

    function initateDataPanel(scenario_index , config) {
        updateDataPanel(scenario_index);
    }

    ///** INIT Config **///
    // Initate the content of selected-div
    var selectContent = document.getElementById('dropdownList-content')
    var selectItem = document.getElementById('dropdownList-selectItem')
    selectContent.innerText = 'scenario 1';
    selectItem.style.display = 'none';
    var myChart = echarts.init(document.getElementById("data_vis"));
    fillingTable(customerList_CMAD);
    //default for scenario.1
    var selected_scenario_index = 0 ; //the first scenario shall be displayed when user open the webpage
    initateDataPanel(selected_scenario_index)

    var data_testTableContent = [
       // Original CMAD data should be here
       // [78000,62000,4500,130500,71000,80000,80000,165000,160500,161500,88500,80000],
        [0,0,0,0,801000,0,101500,0,115500,163500,191000],
        [0,0,0,0,170000,0,60000,50000,0,0,0],
        [0,0,0,0,0,0,66000,68000,68000,0,75000],
        [0,0,0,0,1000,0,0,0,0,0,0]
    ];

    origin_CMAD_order.unshift(plantATP);
    var excelData_container = document.getElementById('inputData')
    var excelData_hot = new Handsontable(excelData_container, {
        data:  origin_CMAD_order,
        licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
        mergeCells:true,//合并单元格
        contextMenu: false,//使用菜单
        readOnly: true,
        rowHeaders: getHeader_row(),
        colHeaders: getBSHeader_col_by_CWlist(CW_list),
        rowHeaderWidth: 180,
        headerTooltips: {
            rows: false,
            columns: true,
            onlyTrimmed: true
        },
        readOnly:true  // column redy only
        /* mergeCells: [
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
        ]*/
    });
    var a;
    excelData_hot.addHook('afterOnCellMouseDown', function(event, coords){
        a =  this;
         excelData_hot.setCellMeta(coords.row, coords.col, 'className', excelData_hot.getCellMeta(coords.row, coords.col).className + ' clk-td');
    });

    //TODO: deined JSON data format for post to server here
    function getTargetScenario(btnItem) {
        return btnItem; // type->button
    }

    //Bind event callback to button onclick listener or others listeners....
    var selectableBtnHTMLCollection = document.getElementsByClassName('select-scen-btn')
    var selectableBtnList = [...selectableBtnHTMLCollection]
    var lastSelectedBtn = null;
    //Here the 'scenario_has_selected' is a flag variable showing if one of button is selected.
    //var scenario_has_selected = false;
    //TODO: ASSERT : item here must be button of selectable
    selectableBtnList.forEach(function (item) {
        item.onclick = function () {
            clist = item.classList;
            //If the button has not been selected, user click one button of those all buttons at list.
            if ( lastSelectedBtn != item ){
                item.classList.add("gbtn-selectable");
                if (lastSelectedBtn!=null){
                    lastSelectedBtn.classList.remove("gbtn-selectable")
                }
                targetScenario = getTargetScenario(item);
                lastSelectedBtn = item;
            } else if (lastSelectedBtn == item) {
            //If the button is selected now, then user click again, button remove the added style.
                lastSelectedBtn.classList.remove("gbtn-selectable");
                lastSelectedBtn = null;
            }
        }
    })

    //var selectableBtnHTMLCollection = document.getElementById("")

    //targetScenario


/***********************************/
/****dropdown list defined here****/
 //TODO: ERROR!!!!
  // var scenario_max_length = customerNameList.length

    // data content for #scenario# Number.
  var data = []
  for ( var i = 0 ; i < scenarioNumber; i++) {
      data.push({name:'scenario '+(1+i), value: i});
  }

  var content = document.getElementById('dropdownList-content');
  var selectImg = document.getElementById('dropdownList-selectImg');
  var selectItem = document.getElementById('dropdownList-selectItem');

  var ul = document.createElement('ul');
  selectItem.appendChild(ul);
  for(var i = 0; i < data.length; i++){
    var li = document.createElement('li');
    li.setAttribute('data-value',data[i].value);
    li.innerText = data[i].name;
    ul.appendChild(li);
  }
  /** 点击下拉箭头 */
  selectImg.onclick = function () {
    console.log(selectItem.style.display);
    if(selectItem.style.display == 'none' || selectItem.style.display == ''){
      selectItem.style.display = 'block';
    }else{
      selectItem.style.display = 'none';
    }
  }

  content.onclick = function () {
    if(selectItem.style.display == 'none' || selectItem.style.display == ''){
      selectItem.style.display = 'block';
    }else{
      selectItem.style.display = 'none';
    }
  }

  var lis = selectItem.getElementsByTagName('li');
  for(var i = 0; i < lis.length; i++){
    lis[i].onclick = function () {
      content.innerText = this.innerHTML;
      selectItem.style.display = 'none';
      // update data visualization panel
      updateDataPanel(this.getAttribute('data-value'));
    };
  }

    function checkoutRadio() {

    }

}


function getCWsHeader(cw1, cw2){
    var tableHeader = [''];
    for(var i=cw1; i<=cw2; i++){
        tableHeader.push('CW '+i);
    }
    return tableHeader;
}


function createCWList(CW_start,CW_end) {
    var list = [];
    for (var i = CW_start; i<=CW_end; i++){
      list.push(i);
    }
    return list;
}

//NOTE: Not Correct method for get the datelist as Excel!
function createDateList() {
    var list = [];
    for (var i = 10; i < 18; i++) {
        if (i <= 12) {
            list.push('2016-' + i + '-01');
        } else {
            list.push('2017-' + (i - 12) + '-01');
        }
    }
    return list;
}

//*The following for code backup*//
/*
function initateDataPanel(scenario_index , config) {
    /*
    // option 里面的内容基本涵盖你要画的图表的所有内容
    var option = {
        // Define margin-left (x), margin-top (y), margin-right (x2), margin-button (y2), at grid.
        grid:{
            x:'45px',
            y:'25px',
            x2:'45px',
        },

        //width:900,
        // title: { '' },
        // 定义样式和数据
        backgroundColor: '#FBFBFB',
        tooltip: {
            //trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
            data: customerNameList
        },
        calculable: true,
        xAxis: [{
            axisLabel: {
                rotate: 0,//30,
                interval: 0
            },
            axisLine: {
                lineStyle: {
                    color: '#222'
                }
            },
            type: 'category',
            boundaryGap: false,
            data: function() {
                var list = [];
                //for (var i = 0; i<=52; i++){
                for (var i = CW_start; i<=CW_end; i++){
                  list.push(i);
                }
                return list;
            }()
        }],
        yAxis: [{
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#222'
                }
            }
        }],
        series: (function (customerNameList,customerList_CMAD){
                result = []
                var customerNumber = customerNameList.length
                for (var i = 0 ; i < customerNumber; i++) {
                    result.push({
                        name: customerNameList[i],
                        type: 'line',
                        symbol: 'none', //--> It means only mouse hover on it, then the data label can be displayed
                        smooth: 0.168,
                        color: (function(){     //['#66AEDE','#9911E1','#19B1D2'],
                            colorDict=[0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']
                            color='#'
                            for (var i = 0 ; i < 6; i++) {
                                color_bit = parseInt(Math.random()*100%16)
                                color += colorDict[color_bit]
                            }
                            return color
                        })(),
                        data: customerList_CMAD[scenario_index][i],
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        }
                    });
                }
                return result;
            })(customerNameList,customerList_CMAD)
    };

    // update the data panel -- 'myChart' is global variable
    updateDataPanel(scenario_index)
}
*/