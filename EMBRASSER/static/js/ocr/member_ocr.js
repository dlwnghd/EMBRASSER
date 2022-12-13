$(document).ready(function(){
    result = $("#warning").text()
    console.log("result :", result)
    if (result == "False") {
        Swal.fire({
            icon: "error",
            title: "OCR 오류",
            text: "요청한 서류가 아닙니다!"
        });
    }
});

console.log("여기에는 왔음")