/* window.onload = function () {
    // 执行代码
			
}
$(document).ready(function(){
	window.alert(1213+"卧槽"+213);
	$('#input_excel').innerHTML = '12321'
});  */
/**
 * Using AJAX post message to server to varify user's identity
 */

function __submit(DOMelement) {
     clickCallback = DOMelement.click ;
     console.log(clickCallback)
     DOMelement.click = '';
     DOMelement.type = 'submit'
     DOMelement.click();
     DOMelement.click = clickCallback;
}

//Django url.py里配置的 route name --> 约定接口
var AJAXServletURL = "/userlogin";
//"http://localhost:8000"
function basePath(){
	var currentAbsPath = window.document.location.href;
	var lastNamespaceIndex = currentAbsPath.lastIndexOf("/");
	var basePath = currentAbsPath.substring( 0, lastNamespaceIndex );
	return basePath;
}
function  logout(){
    var logout = confirm("Are you confirm to log out ReCAST?");
    if (logout == false) {
        //do nothing
    } else {
        window.location='/logout/';
    }
}

function help() {

}

function saveTask() {
    var isSaved = confirm("Do you want to save task?")
    
}

function discardTask() {
    var discard = confirm("Do you want to discard the task?\n(Data will be not be recorded in Database.)")
    if (discard == false) {
        //do nothing
    } else {
        window.location='/index/';
    }
}

function quitTask() {
    alert("Task Quit.(No thing changed.)")
    /*
    var isSaved = confirm("Do you want to quit the task?\n(Nothing changed.)")
    */
    window.location='/index/'
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // 这些HTTP方法不要求CSRF包含
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
/********************AJAX*********************/

$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});




//创建xmlHttprequest
function getXmlhttp() {
    var xmlhttp;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
    	xmlhttp = new XMLHttpRequest();
    } else {// code for IE6, IE5
    	xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttp;
}

/*** Post ***/
function post(url,data,callback){
	//1、获取到xmlhttprequest 对象
    var xhr = getXmlhttp();

    //2、xmlhttprequest的响应事件
    xhr.onreadystatechange = function() {
    	//alert("xhr.readyState"+xhr.readyState +",   xhr.status:"+xhr.status+"      : "+xhr.responseText); //test
        if (xhr.readyState == 4 && xhr.status == 200) {

            //5、操作获取到的信息
            //5.1 ajax返回的数据,转换为JSON对象
            //    使用JSON.parse转换字符串为JSON对象 (利用eval实现转换  不知道行不行) JSON.stringify(obj)->string
            var data = JSON.parse(xhr.responseText);
            //alert(xhr.responseText); //test
            //5.2 获取JSON对象的属性
            //var isValid = data.isValid;

            //6. 执行回调
        	//function && function() 的意思是防止function() 未定义就直接执行从而报错
        	callback && callback(data);
        }
    }
    //对url做参数拼接处理
    data.forEach( function(value, key){
    	url += (url.indexOf("?") == -1 ? "?" : "&");
    	url +=encodeURIComponent(key) + "=" + encodeURIComponent(value);
    });

    //final url
    url = url+'&'+Number(new Date()); //增加url的随机数，防止缓存
    //3、准备获取ajax请求
    //3.1 初始化get请求,POST带参数的方式,第二个参数为目标地址
    xhr.open("POST", url, true);

    //4、发送ajax请求
    //4.1 设置POST HTTP头信息
    xhr.setRequestHeader("Content-type",  "application/x-www-form-urlencoded");
    //4.2 发送AJAX [send(string)的参数仅限用于post方式,username=1234&password=1234...]
    xhr.send();
}