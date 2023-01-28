function set_tabs_inactive() {
    var elements = $('.tablinks');
    for (var i in elements) {
        if (elements.hasOwnProperty(i)) {
        elements[i].id = "";
    }
    }
}

function showLogin(tab){
    set_tabs_inactive();
    $('#Login').show();
    $('#Signup').hide();
    tab.id = "tab-active";
}


function showSignup(tab) {
    set_tabs_inactive();
    $('#Signup').show();
    $('#Login').hide();
    tab.id = "tab-active";
}
