function load_ready_msg(){
    send('document_ready');
}

function get_url(action, data){
    if(data === undefined) {
        data = "";
    }
    var json_data = JSON.stringify(data);
    if(typeof debug_enabled != 'undefined' && debug_enabled){
        server = debug_server + "/";
    } else{
        server = "";
    }
    var url = "http://" + server + "colors/" + action + "?" + json_data;
    return url;
}

function change_color(color){
    $("body").css("background-color",color);
    $(".news").text("Background color changed to " + color );
}

function select_color(color){
    send('select_color',color);
}

$(document).ready(function(){
    load_ready_msg;
    $(".color1").click(function() { send('select_color','red'); });
    $(".color2").click(function() { send('select_color','green'); });
    $(".color3").click(function() { send('select_color','blue'); });
});
