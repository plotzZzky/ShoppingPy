function getPantry() {
    let value = $('#listSelector').val();
    $.get('http://127.0.0.1:8000/pantry/list=' + value + '/', function(result) {
    $('#myList').html(result);
    })
}


function getProperties(itemId) {
    $.get('http://127.0.0.1:8000/pantry/item=' + itemId + '/', function(result) {
    $('#pantryProps').html(result);
    })
}


function setProperties(itemId) {
    let input = $('#inputDate').val();
    $.get('http://127.0.0.1:8000/pantry/item=' + itemId + '/date=' + input + '/' , function() {
        getProperties(itemId)
    })
}


function removeItem(itemId) {
    $.get('http://127.0.0.1:8000/pantry/remove=' + itemId + '/', function(){
    getPantry()
    })

}


function clearList() {
    let value = $("#listSelector").val();
    $.get("http://127.0.0.1:8000/pantry/clear/id=" + value + "/", function() {
    getPantry();
    })
}


function showAlert() {
    let item = $(".div-list-item")
     for (i = 0; i < item.length; i++) {
        if (item[i].children.length < 3){
            if (item[i].style.display == "") {
                item[i].style.display = "none";
            } else { item[i].style.display = ""; }
        }
     }
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
