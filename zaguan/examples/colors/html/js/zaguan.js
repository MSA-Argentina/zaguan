
function send(action, data) {
    $.get(get_url(action, data));
}

function log(msg){
    send('log', msg);
}

function run_op(operacion, data){
    func = eval(operacion);
    data = JSON.parse(data);
    func(data);
}


