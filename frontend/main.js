console.log("page loaded!");

// Connect buttons
var dorm_name = document.getElementById('dorm');
dorm_name.onmouseup = get_name;

var all_button = document.getElementById('display_all_dorms');
all_button.onclick = function() {
    netcall_api('display_all_dorms');
}

var female_button = document.getElementById('female_dorms');
female_button.onclick = function() {
    netcall_api('female_dorms');
}

var male_button = document.getElementById('male_dorms');
male_button.onclick = function() {
    netcall_api('male_dorms');
}

var clear_button = document.getElementById('clear');
clear_button.onclick = function() {
    let clear_dorms = '';
    let response_item = document.getElementById("dorm-names");
    response_item.innerHTML = clear_dorms;
}

// Get info form
function get_name(){
    console.log('entered get_name.');

    var name = document.getElementById('name').value;
    console.log(name);
    name = name.trim();

    if(name) {
        netcall_api(name);
    }
} 

// Make network calls to api
function netcall_api(name){
    console.log("entered netcall_api...");
    var url = "http://localhost:51023/dorms/";

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);

    xhr.onload = function(e){ 
        console.log("name: " + name);
        if(name == 'display_all_dorms'){ 
            show_all_dorms(xhr.responseText,1);
        } else if (name=='male_dorms'){
            show_all_dorms(xhr.responseText,2);
        }else if (name=='female_dorms'){
            show_all_dorms(xhr.responseText,3);
        }
        else {
            get_id(name, xhr.responseText);
        }
    }

    xhr.onerror = function(e){
        console.log('age api onerror triggered' + xhr.statusText);
    }

    xhr.send();
}

// Show all dorms from api
function show_all_dorms(response_text,choice) {
    console.log("entered show_all_dorms");

    var response_json = JSON.parse(response_text);
    
    let all_dorms = '';
    if(choice==1){
        all_dorms = all_dorms + response_json[1]['name']; // so "," is in the right place

        for(let i = 2; i <= 33; i++) {
            all_dorms = all_dorms + ", " + response_json[i]['name'];
        }
    }else if(choice==2){
        all_dorms = all_dorms + response_json[1]['name']; // so "," is in the right place

        for(let i = 2; i <= 33; i++) {
            if(response_json[i]['gender']=='Male'){
                all_dorms = all_dorms + ", " + response_json[i]['name'];
            }
            
        }
    }else if(choice==3){
        all_dorms = all_dorms + response_json[2]['name']; // so "," is in the right place

        for(let i = 3; i <= 33; i++) {
            if(response_json[i]['gender']=='Female'){
                all_dorms = all_dorms + ", " + response_json[i]['name'];
            }
            
        }
    }
    let response_item = document.getElementById("dorm-names"); 
    response_item.innerHTML = all_dorms;
}

function get_id(name, response_text){
    var response_json = JSON.parse(response_text);

    for (let i = 1; i <= 33; i++) {
        i_lower = response_json[i]['name'].toLowerCase();
        name_lower = name.toLowerCase();
        if (i_lower == name_lower) {
            var d_id = i;
        }
    }

    let response_item = document.getElementById("response");
    response_item.innerHTML = '';

    if(d_id != null) {
        update_button = document.getElementById('dorm');
        
        var year_button = document.getElementById('year');
        var gender_button = document.getElementById('gender');
        var quad_button = document.getElementById('quad');
        var mascot_button = document.getElementById('mascot');
        var all_info_button = document.getElementById('all_info');

        var name = response_json[d_id]['name'];
        var year = response_json[d_id]['year'];
        var gender = response_json[d_id]['gender'];
        var quad = response_json[d_id]['quad'];
        var mascot = response_json[d_id]['mascot'];

        year_button.onmouseup = function() {
            var response_string = name + " Hall was established in " + year;
            response_item.innerHTML = response_string;
        }
        gender_button.onmouseup = function() {
            var response_string = name + " Hall is a " + gender.toLowerCase() + " dorm";
            response_item.innerHTML = response_string;
        }
        quad_button.onmouseup = function() {
            var response_string = name + " Hall is on " + quad + " Quad";
            response_item.innerHTML = response_string;
        }
        mascot_button.onmouseup = function() {
            var response_string = name + " Hall is represented by the " + mascot;
            response_item.innerHTML = response_string;
        }
        all_info_button.onmouseup = function() {
            var response_string = name + " Hall is a " + gender.toLowerCase() + ". It was founded in " + year + ". It is on " + quad + " Quad and is represented by the mascot: " + mascot + ". ";
            response_item.innerHTML = response_string;
        }

    } else {
        var response_string = name + " is not a dorm at Notre Dame.";
        response_item.innerHTML = response_string;
    }
}