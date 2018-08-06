$(function () {

    /* 头像的上传 */

    // bindAvatar1();
    // bindAvatar2();
    // bindAvatar3();
    bindAvatar();

    function bindAvatar() {
        // 针对不同版本兼容性的做特殊处理
        if (window.URL.createObjectURL) {
            bindAvatar2();
        } else if (window.FileReader) {
            bindAvatar3();
        } else {
            bindAvatar1();
        }
    }

    function bindAvatar1() {
        $('#imgSelect').change(function () {
            // $(this)[0]把jquery对象变成dom对象
            var file_obj = $(this)[0].files[0];
            // Ajax发送后台，并获取路径，在img的src上一写
            console.log(file_obj)
        })
    }

    function bindAvatar2() {
        // 本地上传预览
        $('#imgSelect').change(function () {
            var file_obj = $(this)[0].files[0];
            // 使用window.URL.createObjectURL可以创建一个对象
            // 相当于已经把文件上传到浏览器了，而不是提交给后台
            var v = window.URL.createObjectURL(file_obj);
            // 对浏览器兼容是有问题的。ie10以下就有问题了。
            $('#previewimg').attr('src', v);
            $('#previewimg').load(function () {
                // 这个方法并不会自动进行图片的释放，需要手动释放
                // 而且释放不能加载完了就直接释放而是
                // 等图片在浏览器加载了再内存中释放v
                window.URL.revokeObjectURL(v);
            });

        })
    }

    function bindAvatar3() {
        // 本地上传预览
        $('#imgSelect').change(function () {
            var file_obj = $(this)[0].files[0];
            // fileReader对象也可以帮助完成预览的效果
            // 相当于已经把文件上传到浏览器了，而不是提交给后台
            var reader = new FileReader();
            // 相当于把读取到的文件放到这个对象（内存）
            reader.readAsDataURL(file_obj);
            // 把内存的数据放到浏览器显示，只要reader有内容
            // 就会进行加载，然后触发执行函数。
            // FileReader会自动帮你释放内存占用
            reader.onload = function () {
                $('#previewimg').attr('src', this.result)
            }
        })

    }

    //
    // $('.avatar').mousemove(function () {
    //     $(this).css('width','150px')
    // })


    $('.authcode image').on('click', function () {
        // 通过加问号实现刷新的效果
        // 个人觉得加时间戳也是可以解决问题的。
        // $(this).attr('src', this.src + '?' )
        // 永远取第0个，也就是永远取原来的src
        // 通过修改让连接后面不是一直叠加问号，而是叠加时间戳。
        var imgsrc = this.src.split('?')[0];
        $(this).attr('src', imgsrc + '?' + Number(new Date()))
    });


    $('button[type=button]').on('click', function () {
        var formdata = new FormData();
        // 获取到用户上传的所有的数据，注意csrftoken不要忘掉
        console.log($('#id_username').val());
        formdata.append('username', $('#id_username').val());
        formdata.append('nickname', $('#id_nickname').val());
        formdata.append('email', $('#id_email').val());
        formdata.append('password', $('#id_password').val());
        formdata.append('re_password', $('#id_re_password').val());
        formdata.append('auth_code', $('#id_auth_code').val());
        formdata.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        formdata.append('avatar', $('#imgSelect')[0].files[0]);
        $.ajax({
            url: '/register/',
            type: 'post',
            data: formdata,
            // 告诉jquery不要处理我的数据
            contentType: false,
            // 告诉jquery不要设置content-type
            processData: false,
            dataType: 'JSON',
            success: function(arg){
                console.log(arg);
                if(arg.status){
                    console.log('证明没有错误')
                }else{
                    // 证明status=0是存在错误的
                    $.each(arg.msg, function (k, v) {
                        if(k === 'auth_code'){
                            $('#id_auth_code').parent().next('span').text(v[0]).parent().addClass('has-error');
                        }else{
                            $('#id_'+k).next('span').text(v[0]).parent().addClass('has-error');
                        }

                    })
                }
            }
        })
    });

    $('form input').focus(function () {
        // $(this)也就是当前点击的标签，也就是当前你点击的这个input框
        if($(this).attr('id')==='id_auth_code'){
           $(this).parent().next('span').text('').parent().removeClass('has-error');
        } else{
           $(this).next('span').text('').parent().removeClass('has-error');
        }

    });

    // 通过失去焦点的方式去判断用户所要注册的用户名是否存在
    $('#id_username').blur(function () {
        var username=$('#id_username').val();
        // 有的时候可能不输入任何内容我也点了其他地方失去焦点，这个时候是没有必要发送ajax请求的，浪费服务器资源！
        if(username){
            $.ajax({
            url: '/check_user/',
            method: 'get',
            data: {'username': username},
            /*
            * 这个地方是异常重要的，一定要制定以什么数据类型去接受服务器返回来的数据，
            * 否则的话服务器就是按照str去接受的，由于不是一个对象，也因此无法调用传递回来的对应的属性
            * 要被坑死了。。。。
            * */
            dataType: 'JSON',
            success: function (arg) {
                if(!arg.status) {
                    $('#id_username').next().text(arg.msg).parent().addClass('has-error');
                }
            }
        })
        }

    })
});