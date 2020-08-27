

function validateForm(){
    var usernameEle=document.getElementById('input1') ;
    var usernameEleVal=entities(usernameEle.value);
    var passwordEle=document.getElementById('input2');
    var passwordEleVal=entities(passwordEle.value);
    var passwordEle2=document.getElementById('input3');
    var passwordEleVal2=entities(passwordEle2.value);
    if (usernameEleVal.length == 0){
        window.alert('用户名为必填项!');
        usernameEle.focus();
        return false;}
    if (usernameEleVal.length < 6){
        window.alert('用户名不能小于6位!');
        usernameEle.focus();
        return false;}
    if (passwordEleVal.length == 0){
        window.alert('密码为必填项!');
        passwordEle.focus();
        return false;}
    if (passwordEleVal.length < 8){
        window.alert('密码不能小于8位!');
        passwordEle.focus();
        return false;}
    if (passwordEleVal != passwordEleVal2){
        window.alert('两次密码不一致！请重新输入!');
        passwordEle2.value='';
        passwordEle2.focus();
        return false;}
    else{
        return true
    }
}
function get_csrf_token() {
    var inputbox = document.getElementsByName('csrfmiddlewaretoken')[0]
    return inputbox.value;
}

function setBtnCountdown60s(btn){
    var oBtn = btn;
    var __callback_ = btn.onclick;
    btn.onclick='';
    var time = 60;
    var timer = null;
    oBtn.innerHTML = 'after '+ time + 's resend';
    oBtn.setAttribute('disabled', 'disabled');  // 禁用按钮
    oBtn.setAttribute('class', 'disabled btnAtList');   // 添加class 按钮样式变灰
    timer = setInterval(function(){
        // 定时器到底了 兄弟们回家啦
        if(time == 1){
          clearInterval(timer);
          oBtn.innerHTML = 'send OTC';
          oBtn.removeAttribute('disabled');
          oBtn.removeAttribute('class');
          oBtn.setAttribute('class', 'greenBtn btnAtList');   // 添加class 按钮样式变灰
          btn.onclick=__callback_ ;
        } else {
          time--;
          oBtn.innerHTML = 'after '+ time + 's resend';
        }
    }, 1000);
}

function sendOTC(sendBtn) {
     try {
         var email   =  entities(document.getElementsByName("email")[0].value)
         if (email.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/) == -1){
             throw "Email address is not valid.";
        } else {
             var email      = document.getElementsByName('email')[0]
             var to_email   = email.value
             setBtnCountdown60s(sendBtn);
             // send email
             $ajax_email('/sendMail/',to_email, get_csrf_token())
         }
     }catch(err) {
         console.log( err );
         return false;
    }
}

function checkUsername(sendBtn) {
     try {
         var account   =  entities(document.getElementsByName("username")[0].value)
         if (account == null || account.replace(/(^\s*)|(\s*$)/g, "") == "") {
            console.log("account:"+account)
            throw "account can not be empty.";
        } else if (!/^[0-9A-Za-z]+/.test(account)) {
            throw "account must be alphanumeric.";
        } else if (account.length < 8 ) {
            throw "account min-length is 8 over 6 digits";
        } else {
             //setBtnCountdown60s(sendBtn);
             // send email
             $ajax_checkUsername('/checkUsername/',account, get_csrf_token())
         }
     }catch(err) {
         console.log( err );
         return false;
    }
}

function $ajax_checkUsername(url, data, csrf_token) {
    var formData = new FormData();
    formData.append("username", data);
    formData.append("csrfmiddlewaretoken", csrf_token);
    succ_callback = function (msg) {
                // Return a Json object
                // No need to parse it, as 'dataType' set to json
                //data=JSON.parse(msg)
                if (msg.valid == false){
                    alert("username cannot be used, try another one.")
                }
            }
    error_callback = function(msg){
                console.log("register.js: error[$ajax]: "+msg)
            }
    execute_ajax_post(url,formData,succ_callback,error_callback)
}

function $ajax_email(url, data, csrf_token) {
    var formData = new FormData();
    formData.append("to_email", data);
    formData.append("csrfmiddlewaretoken", csrf_token);
    succ_callback = function (msg) {
                // Return a Json object
                // No need to parse it, as 'dataType' set to json
                //data=JSON.parse(msg)
                if (msg.success == true){
                    alert("success call ajax")
                }
            }
    error_callback = function(msg){
                console.log("register.js: error[$ajax]: "+msg)
            }
    execute_ajax_post(url,formData,succ_callback,error_callback)
}

function execute_ajax_post(url,formData,succ_callback,error_callback) {
 $.ajax({
            url:url,
            type:'POST',    //  method:"POST",
            dataType:'json',
            data: formData, //发送到服务器的数据
                            // data就是Django传过来的字典对象
            //headers:'',
            //In case of TypeError: 'append' called on an object that does not implement interface FormData.
            processData: false,
            contentType: false,
            success: succ_callback,
            error: error_callback
        });
}


function checkInput(account, password, eNumber, code) {
    try {
        if (account == null || account.replace(/(^\s*)|(\s*$)/g, "") == "") {
            console.log("account:"+account)
            throw "account can not be empty.";
        }  else if ( password == null || password.replace(/(^\s*)|(\s*$)/g, "") == "" ) {
            console.log("password:"+password)
            throw "password can not be empty.";
        } /*else if (isNaN(account)) {
            throw "账号只能是数字！";
        } */else if (!/^[0-9A-Za-z]+/.test(account)) {
            throw "account must be alphanumeric.";
        } else if (account.length < 8 || password.length < 8) {
            throw "account , password min-length is 8 over 6 digits";
        }  else {
           //document.getElementById("p").innerHTML = "登陆成功！";
            return true;
        }
    } catch(err) {
        // 1.弹出警告框。
        /*alert(err);*/
        // 2.写到 HTML 文档中。
        /*document.write(err);*/
        // 3.写入到 HTML 元素。
        //document.getElementById("p").innerHTML = err;
         alert( err );
        // 4.写入到浏览器的控制台。
        /*console.log(err);*/
        return false;
    }
}
//将用户名和密码及确认密码中的特殊符号换位对应的HTML实体，以防止SQL注入产生
//SQL注入问题必须重视
function entities(str){
    console.log(str)
    if(null == str || undefined == str )
        return ""
    str = str.replace(/&/g,'&amp;');
    str = str.replace(/'/g,'&#39;');
    str = str.replace(/"/g,'&quot;');
    str = str.replace(/>/g,'&gt;');
    str = str.replace(/</g,'&lt;');
    str = str.replace(/ /g,'&nbsp;');
    return str;
}


function pageSubmit(element){
    var username = entities(document.getElementsByName("username")[0].value)
    //var password = entities(document.getElementsByName("password")[0].value)
    var empnum  =  entities(document.getElementsByName("empnum")[0].value)
    var otc     =  entities(document.getElementsByName("otc")[0].value)
    if( checkInput( username,password,empnum,otc) ){
        __submit(element)
    }
}