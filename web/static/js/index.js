$(document).ready(function(){

    $("#cf-all").click(function () {
        if($(this).prop("checked")){
            $(this).prop("checked",true);
            $(this).parent().nextAll().children().prop("checked",false);
            $.post("/", {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,'txt':'全部'},
            function(response) {
                $("#list-container").html(response);
            }).done(function (response) {
            console.log(response);
            }).fail(function (error) {
            console.log(error);
            });
        }else{
            $(this).prop("checked",true);
            $(this).nextAll().children().prop("checked",false);
            $.post("/", {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,'txt':'全部'},
            function(response) {
                $("#list-container").html(response);
            }).done(function (response) {
            console.log(response);
            }).fail(function (error) {
            console.log(error);
            });
        }
    });
    $("#cf-all").parent().nextAll().children().click(function() {
        //if($(this).prop("checked",false)&&$(this).siblings().prop("checked",false)){
            //$("#cf-all").parent().click()
        //}else {
            $("#cf-all").prop("checked", false);
            var ctxt = {};
            $("input[name='classification']:checked").each(function(i){     //把所有被选中的复选框的值存入数组
            ctxt[i] =$(this).val();
            });
            //alert(ctxt);
            $.post("/", {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 'ctxt': ctxt},
                function (response) {
                    $(".more").remove();
                    $("#list-container").html(response);
                }).done(function (response) {
                console.log(response);
            }).fail(function (error) {
                console.log(error);
            });
        //}
    });

    $(window).scroll(function() {
        if ($(document).scrollTop() >= $(document).height() - $(window).height()) {
            scroll_times = $(".more").last().attr('value');
            //alert(scroll_times);
            $.post("/", {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    'txt':"bottom", 'scroll':scroll_times},
            function(response) {
                $(".more").last().html(response);
            })
        }
    });

});