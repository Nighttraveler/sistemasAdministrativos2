$(document).ready(function(){

   // jQuery methods go here...
   $('#add_more').click(function() {
     console.log("asdasdasdasd");
     var form_idx = $('#id_form-TOTAL_FORMS').val();
     console.log("boton presionado");
     $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
     $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
   });

});
