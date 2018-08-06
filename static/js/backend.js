$(function () {
    $('.navigate').click(function () {
        var $header = $('#header');
        var $section =$('#section');
        var header_left = $header.position().left;
        if(header_left<0){
            // 小于0证明这个左侧菜单栏已经被隐藏了。此时应该让侧边栏显示出来
            $header.css('left', 0);
            $section.css('left', 200);
        }else{
            // 不小于0证明现在菜单栏正常显示，得让它隐藏起来
            $header.css('left',-200);
            $section.css('left',0);
        }
    })
});