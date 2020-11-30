//ajax get请求封装
function ajax_jquery(path,get_data,method,type) {
    var return_data;
    $.ajax({
        type: method,
        dataType: type,
        url: '/' + path + '/',
        data: get_data,
        async:false,
        success: function (data,status){
            if(status=='success'){
                return_data = data;
            }
        }
    });
    return return_data;
}

//获取地址栏参数
function GetQueryString(name){
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  decodeURIComponent(r[2]); return null;
}

//layer提示弹窗
function tishi(msg,status=1,flush=1,timeout=1000){
    if (flush==1){
        setTimeout(function(){
            //刷新当前页面
            location.reload();
        },timeout);
    }
    //提示层
    if (status==1){
        layer.msg(msg,{icon:1});
    }else if (status==0){
        layer.msg(msg,{icon:2});
    }
}

//正整数验证
function isPInt(str) {
    var g = /^[1-9]*[1-9][0-9]*$/;
    return g.test(str);
}