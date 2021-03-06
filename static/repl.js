interp = 0

var updater = {
    errorSleepTime: 500,

    poll: function () {
        $.ajax({
            url: "/" + interp, type: "GET", dataType: "text",
            success: updater.onSuccess,
            error: updater.onError
        });
    },

    onSuccess: function (response) {
        try {
            var str = JSON.parse(response);
            var strs = str.split("\n");
            for (var i = 0; i < strs.length; i++) {
                  if (strs[i] !== ""){
                  var p = $("<p>");
                  p.text(strs[i])
                  $("#output").append(p);
                  var container = $("#container");
                  container.scrollTop(container[0].scrollHeight)
                }
            }
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 0);
    },

    onError: function (response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    }

};
$(function () {
    $("#type").change(function(){
       if(interp !== 0){
            $.get("/kill/" + interp)
       }
       var type = $("#type").val();
       $.ajax({
            url: "/new/" + type, type: "GET", dataType: "text",
            success: function(data){
              interp = JSON.parse(data);
              updater.poll();
           }
       });
    })
    var input = $("#input")
    input.keypress(function (event) {
        if (event.which == 13) {
            event.preventDefault();
            $.post("/" + interp, input.val() + "\n");
            input.val("")
        }
    })
})
