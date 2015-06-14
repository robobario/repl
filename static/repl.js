var updater = {
    errorSleepTime: 500,

    poll: function () {
        $.ajax({
            url: "/1", type: "GET", dataType: "text",
            success: updater.onSuccess,
            error: updater.onError
        });
    },

    onSuccess: function (response) {
        try {
            var str = JSON.parse(response);
            var strs = str.split("\n");
            for (var i = 0; i < strs.length; i++) {
                var p = $("<p>");
                p.text(strs[i])
                $("#output").append(p);
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
updater.poll()
$(function () {
    $("#input").keypress(function (event) {
        if (event.which == 13) {
            event.preventDefault();
            $.post("/1", $("#input").val() + "\n")
        }
    })
})
