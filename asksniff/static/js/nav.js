window.onload = get_urls;

function get_urls(){
    $(".button-collapse").sideNav();
    $('.modal').modal();
    $.ajax({
            url : "/all_urls/", // the endpoint
            type : "GET", // http method

            // handle a successful response
            success : function(json) {
                $('#results_urls').val('');
                var result = "<table><tr><th>Name</th><th>URL</th></tr>";
                for(var i=0;i<json.length;i++){
                    url_info = json[i];
                    result += "<tr><td>" + url_info["name"] + "</td><td>" + url_info["url"] + "</td></tr>"                    
                }
                result += "</table>"
                $('#results_urls').html(result);                
            },
        });
}

function goBack() {
    window.history.back();
}
