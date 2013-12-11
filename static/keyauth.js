var keystrokes = new Array();
var pwd = "";
var regdata = new Array();
var regcount = 0;
var offset = 0;
var pwfield;
var validKeyCodeRanges = [  //ranges are inclusive, based on http://www.cambiaresearch.com/articles/15/javascript-char-codes-key-codes
    [16, 16],  //shift
    [48, 90],  //0-9, a-z
    [32, 32],  //space (at least for chrome)
    [186, 192], //special characters
    [219, 222] //more special characters
];

function show_pwd(){
    visible_field = document.getElementById("pwd_visible")
    pwd_field = document.getElementById("password");
    if (visible_field.checked) {
        pwd_field.type = "text";
    } else {
        pwd_field.type = "password";
    }
}

function checkKeyCode(code){
    for (i=0; i<validKeyCodeRanges.length; i++) {
        if ((code >= validKeyCodeRanges[i][0]) && (code <= validKeyCodeRanges[i][1])) {
            return true;
        }
    }
    return false;
}

function reset() {
    keystrokes = [];
    offset = 0;
    pwfield.value = "";
}

function pwFocus() {
    pwfield = document.getElementById("password");
    reset();
}

function pwKeyDown(evt) {
    evt = evt || window.event
    if (evt.keyCode == 9 || evt.keyCode == 13){ //enter or tab blurs the field
        return;
    }
    if (!checkKeyCode(evt.keyCode)) {
        reset();
        return;
    }

    var keystroke = new Object();
    keystroke.code = evt.keyCode;
    if (keystrokes.length==0){
        offset = evt.timeStamp;
    }
    keystroke.down = evt.timeStamp - offset;
    keystrokes.push(keystroke);
}

function pwKeyUp(evt) {
    evt = evt || window.event
    if (evt.keyCode == 9 || evt.keyCode == 13){ //enter or tab blurs the field
        return;
    }
    if (!checkKeyCode(evt.keyCode)) {
        reset();
    }
    for (i=0; i<keystrokes.length; i++) {
        if ((keystrokes[i].code == evt.keyCode) && (keystrokes[i].up == undefined)) {
            keystrokes[i].up = evt.timeStamp - offset;
        }
    }
}

function loginSubmit() {
    var json = JSON.stringify(keystrokes);
    document.getElementById("keystrokes").value = json;
    document.getElementById("output").innerHTML += json;
    return true;
}

function registerReset() {
    regcount = 0;
    document.getElementById("count").innerHTML = regcount;
}

function registerSubmit() {
    if (regcount == 0) {
        pwd = document.getElementById("password").value;       
    }
    if (regcount == 1) {
        if (document.getElementById("password").value != pwd) {
            registerReset();
            alert("Password changed. Start over");
        }
    }
    if (document.getElementById("password").value == pwd) {
        regcount += 1;
        document.getElementById("count").innerHTML = regcount;
        regdata.push(keystrokes);
        if (regcount == 10) {
            var json = JSON.stringify(regdata);
            document.getElementById("keystrokes").value = json;
            document.getElementById("output").innerHTML += json;
            return true; 
        }
        reset();
        return false;
    }
    else {
        reset();
        return false;
    }
}
