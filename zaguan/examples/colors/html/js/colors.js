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

$(document).ready(load_ready_msg);
