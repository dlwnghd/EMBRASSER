function modify(id) {
    num = document.getElementById(id).value;
    console.log(num);
    Swal.fire({
        icon: "success",
        title: "회원 정보 수정",
        text: "회원 정보가 수정되었습니다.",
    }).then(function(){
        document.getElementById('form').submit();
    })
    ;
}