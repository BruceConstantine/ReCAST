var targetScenario = null;


window.onload = function () {
    function getCWsHeader(cw1, cw2){
        var tableHeader = [''];
        for(var i=cw1; i<=cw2; i++){
            tableHeader.push('CW '+i);
        }
        return tableHeader;
    }

    function getHeader_col(cw1,cw2) {
        var tableHeader = [];   
        for(var i=cw1; i<=cw2; i++) {
            tableHeader.push('CW ' + i);
        }
        return tableHeader;
    }

    function getHeader_row() {
        //return ['Plant ATP','Customer1 ','Customer 2', 'Customer 3']
        result = ['Plant ATP']
        customerList_name.forEach(function (item) {
            result.push( item )
        })
        return result;
    }

    //deep copy
    customerList_CMAD_with_PlantATP = customerList_CMAD.concat()
    customerList_CMAD_with_PlantATP.unshift(plantATP);

    var  container0 = document.getElementById('sce-tab-2'), hot0;
    hot0 = new Handsontable(container0, {
        data: customerList_CMAD_with_PlantATP, //JSON.parse(JSON.stringify([1,2,34])),
        licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
        mergeCells:  true,//合并单元格
        contextMenu: false,//使用菜单
        readOnly:    true,
        rowHeaders: getHeader_row(),
        colHeaders: getHeader_col(CW_start,CW_end),
        rowHeaderWidth: 180,
        colWidths: 60,
        width: "100%",
        height:   150,
        rowHeights:23,
        headerTooltips: {
            rows: false,
            columns: true,
            onlyTrimmed: true
          }
    });
    hot0.addHook('afterOnCellMouseDown', function(event, coords){
         hot0.setCellMeta(coords.row, coords.col, 'className', hot1.getCellMeta(coords.row, coords.col).className + ' clk-td');
    });

    var data1 = [
        // [78000,62000,4500,130500,71000,80000,80000,165000,160500,161500,88500,80000],
        [0,0,0,0,801000,0,101500,0,115500,163500,191000],

        [ 1100, 1200, 4100, 1100, 300, 600, 900, 1600,
                400, 520, 1130, 4320],

        [                1800, 300, 500, 820, 500, 1600, 2202, 329,
                300, 2200, 1400, 2291],

        [1600, 2300, 400, 200, 3300, 300, 0, 102,
                1800, 3300, 500, 2800 ]
    ],  container1 = document.getElementById('sce-tab-1'), hot1;
    hot1 = new Handsontable(container1, {
        data:  customerList_CMAD_with_PlantATP, //JSON.parse(JSON.stringify(data1)),
        licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
        mergeCells:true,//合并单元格
        contextMenu: false,//使用菜单
        readOnly: true,
        rowHeaders: getHeader_row(),
        colHeaders: getHeader_col(CW_start,CW_end),
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
    hot1.addHook('afterOnCellMouseDown', function(event, coords){
         hot1.setCellMeta(coords.row, coords.col, 'className', hot1.getCellMeta(coords.row, coords.col).className + ' clk-td');
    });

    var data2 = [
       // [78000,62000,4500,130500,71000,80000,80000,165000,160500,161500,88500,80000],
        [0,0,0,0,801000,0,101500,0,115500,163500,191000],
        [0,0,0,0,170000,0,60000,50000,0,0,0],

        [0,0,0,0,0,0,66000,68000,68000,0,75000],

        [0,0,0,0,1000,0,0,0,0,0,0]
    ],  container2 = document.getElementById('inputData'), hot2;

    hot2 = new Handsontable(container2, {
      data:  customerList_CMAD_with_PlantATP, //JSON.parse(JSON.stringify(data2)),
        licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
        mergeCells:true,//合并单元格
        contextMenu: false,//使用菜单
        readOnly: true,
        rowHeaders: getHeader_row(),
        colHeaders: getHeader_col(CW_start,CW_end),
        rowHeaderWidth: 180,
        headerTooltips: {
            rows: false,
            columns: true,
            onlyTrimmed: true
          }
        //readOnly:true, // column redy only
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
    hot2.addHook('afterOnCellMouseDown', function(event, coords){
        a =  this;
         hot2.setCellMeta(coords.row, coords.col, 'className', hot2.getCellMeta(coords.row, coords.col).className + ' clk-td');
    });

    // 获取到这个DOM节点，然后初始化
    var myChart = echarts.init(document.getElementById("data_vis"));
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
            data: customerList_name
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
                /*
                for (var i = 10; i < 18; i++) {
                    if (i <= 12) {
                        list.push('2016-' + i + '-01');
                    } else {
                        list.push('2017-' + (i - 12) + '-01');
                    }
                }
                */
                //for (var i = 0; i<=52; i++){
                for (var i = CW_start; i<=CW_end; i++){
                  list.push(i)
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
        series: (function (customerList_name,customerList_CMAD){
                result = []
                l=customerList_CMAD.length

                for (var i = 0 ; i < l; i++) {
                    result.push({
                        name: customerList_name[i],
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
                        data: customerList_CMAD[i],
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        }
                    });
                }
                return result
            })(customerList_name,customerList_CMAD)
    };
    // 一定不要忘了这个，具体是干啥的我忘了，官网是这样写的使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

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
}
function checkoutRadio() {

}
