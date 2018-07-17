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


    $('.authcode img').on('click', function () {
        // 通过加问号实现刷新的效果
        // 个人觉得加时间戳也是可以解决问题的。
        // $(this).attr('src', this.src + '?' )
        // 永远取第0个，也就是永远取原来的src
        // 通过修改让连接后面不是一直叠加问号，而是叠加时间戳。
        var imgsrc = this.src.split('?')[0];
        $(this).attr('src', imgsrc + '?' + Number(new Date()))
    });
});