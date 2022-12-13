function modify_confirm(id) {
    num = document
        .getElementById(id)
        .value;
    window.location.href = "http://127.0.0.1:8000/ocr/modify_customer?idx=" + num;
}

function delete_confirm(id) {
    swal.fire({
            title: '정말로 삭제 하시겠습니까?',
            text: "다시 되돌릴 수 없습니다.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#9e9494',
            confirmButtonText: '승인',
            cancelButtonText: '취소'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire(
                    '회원이 삭제되었습니다.',
                    'success'
                ).then(function(){
                    num = document.getElementById(id).value;
                    window.location.href = "delete_customer?idx=" + num;
                })
            }
        })
}
