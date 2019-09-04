$(function () {
    var page = 1;
    var page_end = false;

    $(window).bottom({ proximity: 0.1 });

    $(window).bind('bottom', function () {


        if (!page_end) {
            var obj = $(this);
            if (!obj.data('loading')) {
                obj.data('loading', true);

                $('.loading').html('<i class="fas fa-spinner fa-lg fa-spin"></i>')

                setTimeout(function () {

                    $.ajax({
                        url: '?page=' + String(++page),
                        method: 'GET',
                        dataType: 'html',
                    })

                        .done((response) => {
                            next_contents = $(response).find('.contents').html()
                            if (response != 'end') {
                                $('.contents').append(next_contents);
                            } else {
                                page_end = true;
                            }
                            $('.loading').html('');
                        })

                        .fail((response) => {
                            page_end = true;
                            $('.loading').html('');
                        })

                        .always((response) => {
                            console.log(response);
                        })

                }, 1000);
            }
        }
    });

    $('html, body').animate({ scrollTop: 0 }, '1');

});