function parseClassInfo() {
    $.getJSON('js/class_info.json', function(lessonData) {
        for(var key in lessonData)
        {
            var data = lessonData[key];
            if (key == "Other"){
                for(var item in data){
                    $("ul#Other").append("<li>"+data[item]+"</li>")
                }
            } else {
                if ($("td#"+key).html() != ""){
                    $("td#"+key).html("<i class=\"warning sign icon\"></i>衝突<i class=\"warning sign icon\"></i>");
                    $("td#"+key).addClass("error");
                } else {
                    $("td#"+key).html(data["name"]+"<br>"+data["classroom"]+"<br>"+data["teacher"]);
                    if(data.hasOwnProperty("code")){
                        $("td#"+key).attr("data-content", "選課代碼："+data["code"]);
                        $("td#"+key).attr("data-variation", "inverted");
                        $("td#"+key).addClass("popup inver");
                        $("td.popup").popup();
                    }
                    var status = data["status"];
                    if(status == 0){
                        $("td#"+key).addClass("current");
                    } else if (status == 1) {
                        $("td#"+key).addClass("ta");
                    } else if (status == 2) {
                        $("td#"+key).addClass("club");
                    } else if (status == 3){
                        $("td#"+key).addClass("master");
                    } else {
                        $("td#"+key).addClass("unsure");
                    }
                }
            }
        }
    });

}
