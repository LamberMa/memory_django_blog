$(function () {

    /* 主页点击登录弹出登录框 */
    $('#login-btn').on('click', function () {
        var loginform = $('#loginform');
        if(loginform.hasClass('hide')){
            loginform.removeClass('hide');
        }else{
            loginform.addClass('hide');
        }

    });

    /* 极验验证码登录 */
    var handlerPopup = function (captchaObj) {
        // 成功的回调
        captchaObj.onSuccess(function () {
            var validate = captchaObj.getValidate();
            // 首先获取用户填写的用户名和密码，直接从input框取就行。
            var username = $('#username1').val();
            var password = $('#password1').val();
            $.ajax({
                url: "/login/", // 进行二次验证
                type: "post",
                dataType: "json",
                data: {
                    username: username,
                    password: password,
                    csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                    geetest_challenge: validate.geetest_challenge,
                    geetest_validate: validate.geetest_validate,
                    geetest_seccode: validate.geetest_seccode
                },
                success: function (data) {
                    if (data.status) {
                        // 有错误，需要在页面上显示
                        $('.login-error').text(data.msg);
                    } else {
                        // 没有问题登录成功
                        location.href = data.msg;
                    }
                }
            });
        });

        $("#popup-submit").click(function () {
            captchaObj.show();
        });
        // 将验证码加到id为captcha的元素里
        captchaObj.appendTo("#popup-captcha");
        // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
    };

    $("#username1, #password1").focus(function () {
        $('.login-error').text("");
    });

    // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
    $.ajax({
        url: "/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
        type: "get",
        dataType: "json",
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
            }, handlerPopup);
        }
    });
});