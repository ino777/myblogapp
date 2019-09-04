$(function(){
    $('.search-form-text').on('change input', function(){
        if ($(this).val().length <= 0){
            // No input
            $('.search-form-button').get(0).type = 'button';

        } else if (!(/[\S]+/).test($(this).val())) {
            // only blank
            $('.search-form-button').get(0).type = 'button';
        }else {
            $('.search-form-button').get(0).type = 'submit';
        }
    }).change();
});