$(document).ready(function(){  
    $(document).on("click", ".b_action", function(){
        var page = $(this);
        var arr = page.attr('id').split(';');
        console.log(arr);
        $.ajax({
            url: "/guest_action",
            type: "POST",
            data: JSON.stringify({"user": arr[1],
                                  "event": arr[0],
                                  "action": arr[2]}),
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