/*--------------------------------------------------------------
# select2 customization
--------------------------------------------------------------*/

$(".select2-resumes").select2({
    width: 'resolve'
    }
)

$('select').select2({
    minimumResultsForSearch: 4 
});

$(".select").each(function() {
  $(this).siblings(".select2-resumes").css('border', '5px solid red');
});

