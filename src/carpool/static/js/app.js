requestButtons = document.getElementsByClassName('request')
unrequestButtons = document.getElementsByClassName('unrequest')

for (var i = 0; i < requestButtons.length; i++) {
    requestButtons[i].addEventListener('click', function(){
        console.log("called")
        id = requestButtons[i].value
        $.ajax({
            method : "POST",
            url : "allrides/",
            data : id
        });
    });
}
