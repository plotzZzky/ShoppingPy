function showNewItem() {
    $("#modalNew").toggle()
}

function createNewItem() {
    $.post("http://127.0.0.1:8000/list/item/new/", data={data: frm.serialize(),})
}

function getListAll(value) {
    $.get("http://127.0.0.1:8000/list/all/id=" + value + "/", function(data) {
        $("#listAll").html(data);
    })
}


function getYourList(value) {
    $.get("http://127.0.0.1:8000/list/your/id=" + value + "/", function(result) {
        $("#myList").html(result);
    })
}


function getLists() {
    let value = $("#listSelector").val();
    getListAll(value);
    getYourList(value);
}

function changeAmount(item_id, input) {
    $.post('http://127.0.0.1:8000/list/your/'+ item_id + '/amount=' + input.value + '/')
}


$(document).ready(function(){
    let modal_n = $("#modalNew");
    modal_n.click(function(){
        modal_n.hide()
    });
   $("#modalNew *").click(function(e) {
        e.stopPropagation();
   });
});

function removeFromYourList(item, item_id) {
    item.remove()
    $.post("http://127.0.0.1:8000/list/remove/id=" + item_id + "/");
}


function addToYourList(name) {
    $.post("http://127.0.0.1:8000/list/add/" + name + "/", function (){
        let value = $("#listSelector").val();
        getYourList(value);
    });
}


function clearList() {
    let value = $("#listSelector").val();
    $.get("http://127.0.0.1:8000/list/clear/id=" + value + "/", function() {
    getYourList(value);
    })
}


function buyList(){
    let value = $('#listSelector').val();
    $.get("http://127.0.0.1:8000/pantry/add/id=" + value + "/", function() {
    getYourList(value);
    })
}


function filterLists(input) {
    let value = input.value.toLowerCase()
    let item = $(".div-list-item")
     for (i = 0; i < item.length; i++) {
        let word = item[i].children[0].text.toLowerCase()
        if ( word.indexOf(value) > -1 ) {
            item[i].style.display = "";
        } else {
            item[i].style.display = "none";
        }
    }
}
