
function checkSize(input) {  
    if (input.files) {
        let files = input.files;  
        for (let i=0; i < files.length; i++) {    
            if (files.item(i).size > (3*1024*1024)) {
                alert("파일 사이즈가 2mb 를 넘습니다.");
                files.item(i).value = null;
            }
        } 
    }  
}


$(function () {
    var gigigubun_val = $('select.gigigubun').attr('data-gigi');
    $('select.gigigubun option[value=' + gigigubun_val + ']').attr('selected', 'selected');
    $('select.gigigubun').change(function(){
        $('select.gigigubun').attr('data-gigi', $(this).val());
        location.href='/gshs/infogigi/gigi/' + $('select.gigigubun').attr('data-gigi');
    });

/* Functions */
    var loadForm = function () {
        var btn = $(this);
        var number = btn.attr('class').split(' ')[2];
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            data: {'number': number},
            dataType: 'json',
            beforeSend: function () {
            $("#modal-infogigi").modal("show");
            },
            success: function (data) {
            $("#modal-infogigi .modal-content").html(data.html_form);               
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {  
                window.location.reload();
                $("#modal-infogigi").modal("hide");
            }
            else {
                $("#modal-infogigi .modal-content").html(data.html_form);
            }                      
        }       
        });
        return false;
    };

    var loadForm2 = function () {
        var btn = $(this);
        var number = btn.attr('class').split(' ')[2];
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            data: {'number': number},
            dataType: 'json',
            beforeSend: function () {
            $("#modal-place").modal("show");
            },
            success: function (data) {
            $("#modal-place .modal-content").html(data.html_form);               
            }
        });
    };

    var surisaveForm = function () {
        var form = $(this);
        var formData = new FormData($('#suri-form')[0]);
        $.ajax({
        url: form.attr("action"),
        data: formData,
        type: form.attr("method"),
        dataType: 'json',
        contentType : false, //false 로 선언 시 content-type 헤더가 multipart/form-data로 전송되게 함
        processData : false, //false로 선언 시 formData를 string으로 변환하지 않음
        success: function (data) {
            if (data.form_is_valid) {  
                window.location.reload();
                $("#modal-infogigi").modal("hide");
            }
            else {
                $("#modal-infogigi .modal-content").html(data.html_form);
            }                      
        }       
        });
        return false;
    };

    var surisaveForm2 = function () {
        var form = $(this);
        var formData = new FormData($('#place-form')[0]);
        $.ajax({
        url: form.attr("action"),
        data: formData,
        type: form.attr("method"),
        dataType: 'json',
        contentType : false, //false 로 선언 시 content-type 헤더가 multipart/form-data로 전송되게 함
        processData : false, //false로 선언 시 formData를 string으로 변환하지 않음
        success: function (data) {
            if (data.form_is_valid) {  
                window.location.reload();
                $("#modal-place").modal("hide");
            }
            else {
                $("#modal-place .modal-content").html(data.html_form);
            }                      
        }       
        });
        return false;
    };

    var variousjob = function () {
        var btn = $(this);
        var gubun = btn.attr("id");
        if (gubun == "gigirental") {
            content = "반납 하시겠습니까?";
        } else if (gubun == "softwarerental") {
            content = "소프트웨어를 반납 하시겠습니까?";
        } else if (gubun == "rental") {
            content = "대여 하시겠습니까?";
        } else {
            content = "재고 테이블로 이동할까요?";
        }    
        if(confirm(content)) {
            $.ajax({
                url: btn.attr("data-url"),
                type: 'get',            
                dataType: 'json',            
                success: function (data) {
                    window.location.reload();              
                }
            });
        }
    };

    /* Binding */
    // Create infogigi
    $(".js-create-infogigi").click(loadForm);
    $("#modal-infogigi").on("submit", ".js-infogigi-create-form", saveForm);
    // Update infogigi
    $("#infogigi-table").on("click", ".js-update-infogigi", loadForm);
    $("#modal-infogigi").on("submit", ".js-infogigi-update-form", saveForm);
    // Delete infogigi
    $("#infogigi-table").on("click", ".js-delete-infogigi", loadForm);
    $("#modal-infogigi").on("submit", ".js-infogigi-delete-form", saveForm);
    //기기수리
    $(".js-suri-infogigi").click(loadForm);
    $("#modal-infogigi").on("submit", ".js-infogigi-suri-form", surisaveForm);
    //공간내 수리
    $(".js-suri-place").click(loadForm2);
    $("#modal-place").on("submit", ".js-place-suri-form", surisaveForm2);
    // 부품 교환    
    $(".js-bupum-infogigi").click(loadForm);
    $("#modal-infogigi").on("submit", ".js-infogigi-bupum-form", saveForm);    
    //재고 이동
    $(".js-jaego-infogigi").click(variousjob);   
    //기기 반납
    $(".gigirentl-receive").click(variousjob);
    //소프트웨어 반납
    $(".softwarerentl-receive").click(variousjob);
    
    var main_loadForm = function () {
        var btn = $(this);
        var modalgubun = $(".modal").attr("id");
        var number = btn.attr('class').split(' ')[2];
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            data: {'number': number},
            dataType: 'json',
            beforeSend: function () {
            $("#"+modalgubun).modal("show");
            },
            success: function (data) {
            $("#"+modalgubun+" .modal-content").html(data.html_form);               
            }
        });
    };

    var main_saveForm = function () {
        var form = $(this);  
        var modalgubun = $(".modal").attr("id");
        $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',        
        success: function (data) {
            if (data.form_is_valid) {  
                window.location.reload();
                $("#"+modalgubun).modal("hide");
            }
            else {
                $("#"+modalgubun+" .modal-content").html(data.html_form);
            }            
        }
        });
        return false;
    };

    var deleteForm = function () {
        if (confirm("글을 삭제 하시겠습니까?")) {
            var btn = $(this);        
            $.ajax({
                url: btn.attr("data-url"),
                type: 'get',            
                dataType: 'json',            
                success: function (data) {  
                    window.location.reload();                              
                }
            });
        } else {
            return false;
        }        
    };

    //수리 Update
    $("#suri-table").on("click", ".js-suri-update", main_loadForm);
    $("#modal-suri").on("submit", ".js-suri-update-form", main_saveForm);
    $("#suri-table").on("click", ".js-suri-delete", main_loadForm);
    $("#modal-suri").on("submit", ".js-suri-delete-form", main_saveForm);
   //제품구매
    $(".js-create-productbuy").click(main_loadForm);
    $("#modal-productbuy").on("submit", ".js-productbuy-create-form", main_saveForm);
    $("#productbuy-table").on("click", ".js-productbuy-delete", main_loadForm);
    $("#modal-productbuy").on("submit", ".js-productbuy-delete-form", main_saveForm); 
    //부품 업데이트
    $("#bupum-table").on("click", ".js-update-bupum", main_loadForm);
    $("#modal-bupum").on("submit", ".js-bupum-update-form", main_saveForm);
    //렌탈 삭제     
    $(".gigirental-delete").click(deleteForm);
    // 기기대여
    $(".js-rental-infogigi").click(main_loadForm);
    $("#modal-rental").on("submit", ".js-jaego-rental-form", main_saveForm);
    // 소프트웨어 대여
    $(".js-rental-software").click(main_loadForm);
    $("#modal-softwarerental").on("submit", ".js-software-rental-form", main_saveForm);

    $(document).ready(function () {
        $(".place-left ul li").each(function() {
            $(this).click(function() {
                if $(this).attr('class') 
                $(this).addClass("listchected");
                $(this).siblings().removeClass("listchected");
            });  
        });
    })
});


