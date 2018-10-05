$('#search').on('submit', function(event){
    event.preventDefault();
    $('#wait').show();
    $('#results').hide();
    get_results();
});

function get_results(){
    $.ajax({
          url : "/search/", // the endpoint
          type : "POST", // http method
          data : { search : $('#query').val(), csrfmiddlewaretoken:$('[name=csrfmiddlewaretoken]').val() },
  
          // handle a successful response
          success : function(json) {
              $('#results').val(''); // remove the value from the input
              var result = '<br><h3>Results</h2>';
              var status = json['status'];
              if(status == 0){
                  result += '<h4>No results found.</h4>'; 
              }
              else{
                for(var i = 0; i <json['data'].length;i++){
                    var heading = json['data'][i]
                    result += '<h4><a href="/symptom/information/'+ heading['heading_id'] + '#' + heading['sub_heading_id'] + '">' + heading['title'] + '</a></h4>' + heading['text'] + '<div class="divider"></div>'
                }
              }  
              $('#results').html(result);
              $('.truncate ul').addClass('browser-default');
              $('.truncate ol').addClass('browser-default');    
              $('#wait').hide();
              $('#results').show();              
              $("html, body").animate({ scrollTop: $('#results').offset().top }, 1000);              
              
          },
  
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          }
      });
  }