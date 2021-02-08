$(document).ready(function () {
    let MemoForm = function () {
         let form = $(this);  
         $.ajax({
         url: form.attr("action"),
         data: form.serialize(),
         type: form.attr("method"),
         dataType: 'json',        
         success: function (data) {
             if (data) {  
                window.location.reload();
                $(".memo_form")[0].reset();
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
                 let url = ''; 
                 htmlCode += '<h4>검색 결과</h4>'                
                 for (i in data.search) {
                     htmlCode += '<div class="search_memo memo'+data.search[i]['id']+'">'
                     htmlCode += "<p>" + data.search[i]['created_date'] + "<input type='button' class='del_memo' data-url=" + "{% url 'memo:del_memo' pk=333 %}".replace(333, data.search[i]['id'] ) + " value='del'> </p>"
                     htmlCode += "<p>" + data.search[i]['title'] + "</p>"  
                     htmlCode += '</div>' 
                 }
             $('#memo_list').prepend(htmlCode); 
             }                     
         }        
         });
         return false;
     };
 
     $(".searchmemo_form").submit(SearchForm);
})