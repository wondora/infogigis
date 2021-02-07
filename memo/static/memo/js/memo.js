$(document).ready(function () {

    var loadMemo = function () {
        var btn = $(this);  
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',          
            dataType: 'json',
            beforeSend: function () {
            $("#modal-memo").modal("show");
            },
            success: function (data) {
            $("#modal-memo .modal-content").html(data.html_memo);               
            }
        });
    };

    let MemoForm = function () {
         let form = $(this);  
         $.ajax({
         url: form.attr("action"),
         data: form.serialize(),
         type: form.attr("method"),
         dataType: 'json',        
         success: function (data) {
             if (data.form_is_valid) {  
                 let htmlCode = '';
                 let del_id = data.memos[0]['id'];       
                 let url = "{% url 'memo:del_memo' pk=333 %}".replace(333, del_id);                             
                 htmlCode += '<div class="memo'+del_id+'">'
                 htmlCode += "<p>" +  data.memos[0]['title'] + "<button class='del_memo' data-url=" + url + ">del</button></p>"
                 htmlCode += "<p>" +  data.memos[0]['created_date'] + "</p>"
                 htmlCode += "<p>" +  data.memos[0]['content'] + "</p>"
                 htmlCode += '</div>' 
 
             $(".memo_form")[0].reset();
             $('#memo_list').prepend(htmlCode); 
             }                     
         }        
         });
         return false;
     };
 
     var deleteForm = function () {       
             var btn = $(this);        
             $.ajax({
                 url: btn.attr("data-url"),
                 type: 'get',            
                 dataType: 'json',            
                 success: function (data) {                      
                     $('.memo'+data.pk).remove();                               
                 }
             });
     };
     
     $('.headers .js-memo').click(loadMemo);

     $(".memo_form").submit(MemoForm);
     $(document).on('click', '.del_memo', deleteForm);
 
     $(".memo_show").on('click', '.memo_show_sub', function() {   
         $('.memo_form').toggle(350);    
     })
     $(".memo_show").on('click', '.memo_search_sub', function() {     
         $('.searchmemo_form').toggle(350);    
     })
 
     let SearchForm = function () {
         let form = $(this);  
         $.ajax({
         url: form.attr("action"),
         data: form.serialize(),
         type: form.attr("method"),
         dataType: 'json',        
         success: function (data) {
             if (data) {  
                 let htmlCode = '';    
                 let del_id = data.search[0]['id'];       
                 let url = "{% url 'memo:del_memo' pk=333 %}".replace(333, del_id);                           
                 htmlCode += '<h4>검색 결과</h4>'
                 htmlCode += '<div class="search_memo memo'+del_id+'">'
                 htmlCode += "<p>" +  data.search[0]['title'] + "<input type='button' class='del_memo' data-url=" + url + " value='del'></p>"
                 htmlCode += "<p>" +  data.search[0]['created_date'] + "</p>"
                 htmlCode += "<p>" +  data.search[0]['content'] + "</p>"
                 htmlCode += '</div>' 
             
             $('#memo_list').prepend(htmlCode); 
             }                     
         }        
         });
         return false;
     };
 
     $(".searchmemo_form").submit(SearchForm);
 })