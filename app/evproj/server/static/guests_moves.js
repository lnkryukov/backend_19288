$(document).ready(function(){  
    $(document).on("click", ".b_confirm", function(){
        var page = $(this);
        $.ajax({
            url: "/api/confirm_guest",
            type: "POST",
            data: JSON.stringify({"login": page.attr('id')}),
            contentType: "application/json",
            dataType: "json",
            success: function(data){
                if(data['status'] == 'ok') {
                    page.parents("tr").remove();
                }
            }
        });
    });
});

$(document).ready(function(){  
    $(document).on("click", ".b_decline", function(){
        var page = $(this);
        $.ajax({
            url: "/api/decline_guest",
            type: "POST",
            data: JSON.stringify({"login": page.attr('id')}),
            contentType: "application/json",
            dataType: "json",
            success: function(data){
                if(data['status'] == 'ok') {
                    page.parents("tr").remove();
                }
            }
        });
    });
});