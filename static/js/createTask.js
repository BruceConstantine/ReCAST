/*    var add=document.getElementById('add');
    var snr_no=4;
    var tb_snr = document.createElement('tb_snr');
    var row = document.createElement('tr');
    var td_snr = document.createElement('td');
    var td_cusW = document.createElement('td');
    var td_stoW = document.createElement('td');
    var td_minus = document.createElement('td');
    var minus = document.createElement('span');
    // 添加class
    //dialog.className = 'dialog';
    // 属性
    //img.src = 'close.gif';
    // 样式
    //btn.style.paddingRight = '10px';
    // 文本
    td_snr.innerHTML = 'Scenario&nbsp;' + snr_no++;
    td_cusW.innerHTML = 'Scenario&nbsp;' + snr_no++;
    appendChild(btn);
    tb_snr.appendChild(td_snr);

    add.onclick = function (ev) {
        tr_row.append()
    }
*/
function getfilenameSpanElement() {
    return document.getElementById('input_filename');
}
function imgTableSwitch(str) {
    //传进来的str一定是可见的-->display 一定为：inline-block，否则用户无法点击。
    var excel = {
       "content": document.getElementById('excel'),
        "btn" : document.getElementById('excelSwitchBtn')
    }
    var img = {
        "content" : document.getElementById('img_excel'),
        "btn" : document.getElementById('imgSwitchBtn')
    }
    var display = 'img' == str ?  img.btn.style.display : excel.btn.style.display;
    if (undefined==display || null == display || display == "") {
        excel.btn.style.display = 'none'
        img.btn.style.display = 'none'
    }
    if (str == 'img') {         // img.display:   inline-block
        img.btn.style.display = 'none'
        excel.btn.style.display = 'inline-block'
        img.content.style.display = 'none'
        excel.content.style.display = 'inline-block'
    } else if (str == 'excel') {// excel.display: inline-block
        excel.btn.style.display = 'none'
        img.btn.style.display = 'inline-block'
        excel.content.style.display = 'none'
        img.content.style.display = 'inline-block'
    }
}
function login(){
	var un = document.getElementsByClassName('input')[0].value;
	var pd = document.getElementsByClassName('input')[1].value;
	verifyInput(un,pd);
	var url = basePath() + AJAXServletURL;
	var mapAttrs = new Map();
	mapAttrs.set("username",un);
	mapAttrs.set("password",pd);
	//接口：JSON->isValid
	//回调: 根据服务器返回的结果，执行业务
	var callback = function(isValid){
		if (isValid) { // user is a valid user, do redirect to welcome webpage
			//window.navigate(stringURL)这个方法是只针对IE浏览器的
			window.location.href = basePath()+'/welcome.jsp'; // TODO:测试在这里能不能使用Struts的URL配置
		} else {
			alert("username and password is not correct");
		}
	};
	post(url, mapAttrs, callback);
}

function verifyInput(un,pd){
    /*js中有个变量arguments,可以访问所有传入的值
    for(var i=0; i<arguments.length; i++){} */
	/// TODO: 这里写验证用户输入的JS逻辑 if else 用户提示之类
}
function get_csrf_token() {
    var inputbox = document.getElementsByName('csrfmiddlewaretoken')[0]
    return inputbox.value;
}
//AJAX for upload Excel file and get the data back to JS
function upload(csrf_token){
    var data = $('#input_excel').prop('files')[0];
    if (undefined == data || null == data){
        alert("Please upload an Excel file with the format as the image shown.")
    }
    var name = data.name;
    var token = get_csrf_token(); //document.getElementsByName("csrfmiddlewaretoken")[0].value
    //$ajaxFileUpload("/upload/",data);
    $ajax( "/upload/", data, token);
    getfilenameSpanElement().innerText = name;
   document.getElementById('img_excel').style.display='none';
   document.getElementById('imgSwitchBtn').style.display='none';
   document.getElementById('excelSwitchBtn').style.display='inline-block';
   //document.getElementById('excel').style.display='inline-block';
}

var e;
function $ajax(url, data, csrf_token) {
    var formData = new FormData();
    formData.append("excel_in", data);
    formData.append("csrfmiddlewaretoken", csrf_token);
     $.ajax({
            url:url,
            type:'POST',    // method:"POST",
            dataType:'json',
            data: formData, // 发送到服务器的数据
                            // data就是Django传过来的字典对象
            //headers:'',
            //In case of TypeError: 'append' called on an object that does not implement interface FormData.
            processData: false,
            contentType: false,
            success: function (msg) {
                // Return a Json object
                // No need to parse it, as 'dataType' set to json
                //data=JSON.parse(msg)
                e = msg;
                var img = $('#img_excel');
                var h = img.height();
                //console.log(h);
                renderExcelTable(msg.excelTable, h);
                img.hide();
            },
            error: function(msg){
                e = msg;
                alert(e);
            }
        });
}

    function renderExcelTable(data, tableHeight) {
        var container1 = document.getElementById('excel');
        var hot1 = new Handsontable(container1, {
            data:data,
            licenseKey: 'ab3e4-1bee8-ed01c-4d94b-08cfe',
            mergeCells:  [
                {row: 0, col: 0, rowspan: 1, colspan: 10},
                {row: 1, col: 0, rowspan: 1, colspan: 10},
            ],//合并单元格
            contextMenu: false,//使用菜单
            readOnly: true,
            rowHeaders:false,
            colHeaders:false,
            //rowHeaderWidth: 180,
            //colWidths: 60,
            //the whole table width
            width:"100%",
            height: tableHeight,
            colWidths: 180,
            rowHeights:23,
            headerTooltips: {
                rows: false,
                columns: true,
                onlyTrimmed: true
            }
        });
    }

/*********************  Useless functions  ********************/
function $ajaxFileUpload(url,data) {
    // var name = $("#upfile").val();
    // formData.append("name", name);
    $.ajaxFileUpload({
        url: url,
        secureuri: false,
        //name:'inputFile',
        fileElementId: 'inputFile',//file标签的id
        dataType: 'json',           //返回数据的类型
        global:true,
        data:{headCode:'SumAmount'},
        complete:function(){
            $.messager.progress('close');
            $("#inputFile").val("");
        },
        success: function (data) {
            if (data =="0") {
               // HdUtil.messager.info("表格数据导入成功");
               alert("上传成功");
               // queryCodShipData();
            } else {
                alert("上传失败")
            }
        },
    });
}

//Bug here
function basic_ajax() {
    var data = [];
   	var callback = function(data){
		if (data) {
			alert("Success");
			// window.location.href = basePath()+'/welcome.jsp'; // TODO:测试在这里能不能使用Struts的URL配置
		} else {
			alert("username and password is not correct");
		}
	};
   	var url = "/upload/";
    var mapAttrs = new Map();
   	var excel_file = $('#input_excel').prop('files')[0];
	//Here should be same as the backend constrain
    mapAttrs.set("excel_in" , excel_file);
    mapAttrs.set("X_CSRFTOKEN" , get_csrf_token());
	post(url,mapAttrs, callback);
    renderExcel(data)
}

function pageSubmit(element){
    function constrain() {
        taskName = document.getElementsByName('taskName')[0]
        taskDescription = document.getElementsByName('taskDescription')[0]
        CW_start = document.getElementsByName('CW_start')[0]
        CW_end = document.getElementsByName('CW_end')[0]
        packagingUnit = document.getElementsByName('packagingUnit')[0]
        CW_input_list = document.getElementsByName('CW_input')
        SW_input_list = document.getElementsByName('SW_input')
        /*alert(
            "taskName= "+taskName.value +"\n"+
            "taskDescription= "+taskDescription.value +"\n"+
            "CW_start= "+CW_start.value +"\n"+
            "CW_end= "+CW_end.value +"\n"+
            "packagingUnit= "+packagingUnit.value +"\n"+
            "CW_input_list= "+CW_input_list +"\n"+
            "SW_input_list= "+SW_input_list +"\n"+
            "CW_input_ = "+CW_input_list[0].value +"\n"+
            "CW_input_ = "+CW_input_list[1].value +"\n"+
            "SW_input_ = "+SW_input_list[0].value +"\n"+
            "SW_input_ = "+SW_input_list[1].value +"\n"
        );*/


    }

    constrain()
    __submit(element)
}