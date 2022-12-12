$(document).ready(function(){
    result = $("#warning").text()
    console.log("result :", result)
    if (result == "False") {
        alert("양식에 맞지 않는 이미지입니다.\n확인 후 다시 넣어주세요!")
    }
});