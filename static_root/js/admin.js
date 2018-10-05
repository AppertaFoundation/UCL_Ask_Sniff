function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
var csrftoken = getCookie("csrftoken");

function delete_symptom(symptom_id){
    $.ajax({
          url : "/symptom/delete/", // the endpoint
          type : "POST", // http method
          data : { id : symptom_id },

          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          },
  
          // handle a successful response
          success : function(json) {
              if(json["status"] == "1"){
                var element_name = "symptom_" + json["id"];
                var symptom = document.getElementById(element_name);
                symptom.style.display = "none";
              }
              
          },
      });
  }

  