// Submit post on submit
$("#mybow").on("submit", function(event){
    event.preventDefault();
    console.log("you roll the bow!");  // sanity check
    bowling()
});

var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



// AJAX for posting
function bowling() {
    console.log("bowling is working!") // sanity check
    //var amount = $("#id_amount").val();
    var button = $("form").attr("id");
    console.log(button)
    $.ajax({
        url: $("#mybow").attr('action'), // the endpoint
        //type : "GET", // http method
        data: {
            button: button
            //amount: amount
        },

        // data sent with the post request

        // handle a successful response
        success : function(json) {
            //console.log(json); // log the returned json to the console
            //console.log("success"); // another sanity check
            console.log(json);
            console.log(json.game_frame);
            var game_frame = JSON.parse(json.game_frame);
            console.log(game_frame[0]);
            $("#total").replaceWith('<td id="total" colspan="21">Your total score is: '+json.total+'</div>');
            if (json.result_frame_1 == null) {}
            else {
                $("#one").replaceWith('<td id="one" colspan="2">'+json.result_frame_1+'</td>');
            }
            if (json.result_frame_2 == null) {}
            else {
                $("#two").replaceWith('<td id="two" colspan="2">'+json.result_frame_2+'</td>');
            }
            if (json.result_frame_3 == null) {}
            else {
                $("#three").replaceWith('<td id="three" colspan="2">'+json.result_frame_3+'</td>');
            }
            if (json.result_frame_4 == null) {}
            else {
                $("#four").replaceWith('<td id="four" colspan="2">'+json.result_frame_4+'</td>');
            }
            if (json.result_frame_5 == null) {}
            else {
                $("#five").replaceWith('<td id="five" colspan="2">'+json.result_frame_5+'</td>');
            }
            if (json.result_frame_6 == null) {}
            else {
                $("#six").replaceWith('<td id="six" colspan="2">'+json.result_frame_6+'</td>');
            }
            if (json.result_frame_7 == null) {}
            else {
                $("#seven").replaceWith('<td id="seven" colspan="2">'+json.result_frame_7+'</td>');
            }
            if (json.result_frame_8 == null) {}
            else {
                $("#eight").replaceWith('<td id="eight" colspan="2">'+json.result_frame_8+'</td>');
            }
            if (json.result_frame_9 == null) {}
            else {
                $("#nine").replaceWith('<td id="nine" colspan="2">'+json.result_frame_9+'</td>');
            }
            if (json.result_frame_10 == null) {}
            else {
                $("#ten").replaceWith('<td id="ten" colspan="2">'+json.result_frame_10+'</td>');
            }

            for (var i = 0; i < game_frame.length; i++) {
                var res = i+1;
                if(game_frame[i].fields.Result == null){}
                else{
                    $("#Result_"+res).replaceWith('<td id="Result_'+res+'">'+game_frame[i].fields.Result+'</td>');
                }
            }

            for (var i = 0; i < game_frame.length; i++) {
                var incr = i+1;
                if(game_frame[i].fields.StrikeSpareInfo == null){}
                else{
                    $("#StrikeSpareInfo_"+incr).replaceWith('<td id="StrikeSpareInfo_'+incr+'" height="38">'+game_frame[i].fields.StrikeSpareInfo+'</td>');
                }
            }

            for (var i = 0; i < game_frame.length; i++) {
                if(game_frame[i].fields.StateOfGame === 2){
                    $(location).attr('href', '/end/')
                    //window.location('/end/');
                    document.getElementById('mybow').id = 'exit';
                }
            }
     }



   })

}

