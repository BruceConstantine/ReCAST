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
        result = ['','Plant ATP','']
        customerNameList.forEach(function (item) {
            result.push( item )
        })
        return result;
    }

    var container2 = document.getElementById('sce-tab-1'), hot2;

    //pre-processing for CMAD datalist:
    function CMAD_insert_space_precessing(CMAD_in_table) {
        /*
        var CMAD = CMAD_in_table.slice(0);
        var l = CMAD.length
        for(var i = 0 ; i < l; i++){
            var temp = CMAD[i].join("   ").split(" ");
            console.log(CMAD[i])
            temp.unshift('','')
            console.log(temp)
            console.log("---------------")
            CMAD[i] = temp;
        }
        return CMAD;
        */
        return customerList_All;
    }

    var CMAD_in_table = CMAD_insert_space_precessing(customerList_CMAD)

    l = CW_list.length;
    firstRow  = [];
    //secondRow = [];
    thirdRow  = [];
    for(var i = 0; i < l ; i++) {
        firstRow.push('CW'+(CW_list[i]), '', '');
        //secondRow is plantATP
        thirdRow.push('AATP','A-Stock','Sum');
    }
    CMAD_in_table.unshift( thirdRow );
    CMAD_in_table.unshift( plantATP.join("   ").split(" ") ); //secondRow
    CMAD_in_table.unshift( firstRow  );

    hot2 = new Handsontable(container2, {
        data: CMAD_in_table.slice(0, l*3),//JSON.parse(JSON.stringify(data2)),
        licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
        mergeCells:true,    //合并单元格
        contextMenu: false, //使用菜单
        readOnly: false,
        rowHeaders: getHeader_row(),
        //colHeaders: getHeader_col(12,23),
        rowHeaderWidth: 180,
        headerTooltips: {
            rows: false,
            columns: true,
            onlyTrimmed: true
          },
         // column redy only
        mergeCells:(function mergeCellsLambda(length) {
                var dictList = []
                for (var i = 0; i <= length; i++) {
                    dictList.push({ row: 0, col: i*3, rowspan: 1, colspan:3});
                    dictList.push({ row: 1, col: i*3, rowspan: 1, colspan:3});
                }
                return dictList;
            })(CW_end - CW_start)
        /*
        columns: [
        {
          editor:    Handsontable.editors.TextEditor
          //renderer:  Handsontable.renderers.NumericRenderer,
          //validator: Handsontable.validators.NumericValidator
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
            data: CW_list
                /*function() {
                var list = [];*/
                /*
                for (var i = 10; i < 18; i++) {
                    if (i <= 12) {
                        list.push('2016-' + i + '-01');
                    } else {
                        list.push('2017-' + (i - 12) + '-01');
                    }
                }
                */ /*
                //for (var i = 0; i<=52; i++){
                for (var i = CW_start; i<=CW_end; i++){
                  list.push(i)
                }
                return list;
            }()*/
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
                l=customerList_CMAD.length

                for (var i = 0 ; i < l; i++) {
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
            })(customerNameList,customerList_CMAD)
    };
    // 一定不要忘了这个，具体是干啥的我忘了，官网是这样写的使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

