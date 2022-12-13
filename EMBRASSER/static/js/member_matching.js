
// 페이지 로딩시 select 태그 업데이트 해주는 for문.
for(i=0; i < 10; i++){
    var idx = $('.member_idx')[i].innerText
    var matching = $('#matching_' + idx)
    var m_val = matching.attr('matching');

    matching.val(m_val).prop("selected", true);
}

// select 태그 선택시 DB에 update 해주는 함수
function selectBoxChange(matching, idx){
    $.ajax({
        type:'get',                                     // get
        url: 'matching',                                // 호출 URL
        data: {'matching' : matching, 'idx' : idx},     // 파라미터 정보
        success: (res)=>{                               // 리턴값
            console.log('💚 member_matching update 결과 : ', res.result)
            if(res.result == 'no') alert('DB 통신 오류, 관리자에게 문의하세요.')
        },
    })
}