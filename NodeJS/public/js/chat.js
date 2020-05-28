var app = new Vue({
    http: {
        emulateJSON: true,
        emulateHTTP: true
    },
    el: '#app',
    data: {
        messages : [
            {time: getTimeHM(), message: {name: "Chatbot", message: ''}}
        ]	
    }
});

$("#msg-field").keyup(function(e){
    var key = e.keyCode ? e.keyCode : e.which;
    if (key == 13) sendMessage();
});

$("#messages-field").mouseenter(function(){
    app.autoScrollDown = false;
});
$("#messages-field").mouseleave(function(){
    app.autoScrollDown = true;
});

//Returns current hour and minutes formatted in string
function getTimeHM(){
    let date = new Date();
    let hours = date.getHours();
    if (hours < 10) hours = '0'+hours;
    let minutes = date.getMinutes();
    if (minutes < 10) minutes = '0'+minutes;
    return hours + ':' + minutes;
}

function sendChatMessage(msg){
    app.messages.push({
        time: getTimeHM(), message: {name: "Deg", message: msg}
    });
    $.post("/chat", {tekst: msg}).done(function(data){
        svar = data.res;
        app.messages.push({
            time: getTimeHM(), message: {name: "Chatbot", message: svar}
        });
        Vue.nextTick(function () {
            var objDiv = document.getElementById("messages-field");
            objDiv.scrollTop = objDiv.scrollHeight;
        });
    });
}

function sendMessage(){
    var msg = $("#msg-field").val().trim();
    if (msg == "") {
        $("#msg-field").val("");
        return;
    } else {
        $("#msg-field").val("");
        console.log(msg)
        sendChatMessage(msg);
    }
}