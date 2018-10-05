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

function delete_child(child_id){
    $.ajax({
          url : "/childDelete/", // the endpoint
          type : "POST", // http method
          data : { id : child_id },

          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          },
  
          // handle a successful response
          success : function(json) {
              if(json["status"] == "1"){
                var element_name = "child_" + json["id"];
                var record = document.getElementById(element_name);
                record.style.display = "none";
              }
              
          },
      });
  }

  function activate_child(child_id){
    $.ajax({
          url : "/childActivate/", // the endpoint
          type : "POST", // http method
          data : { id : child_id },

          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          },
  
          // handle a successful response
          success : function(json) {
            if(json["status"] == "1"){
                window.location.href = "/homepage/";
            }
            else{
                window.location.href = "/";
            }
          },
      });
  }

  