// Need {% csrf_token %}

$(function () {
    var good_button = $('#good-button');
    var bad_button = $('#bad-button');
    var good_field = $('#good-count');
    var bad_field = $('#bad-count')
    var good_count = 0;
    var bad_count = 0;

    // GET method
    $.ajax({
        url: '{% url "apis:posteval-list" %}',
        method: 'GET',
        data: {
            'post': '{{ post.pk }}',
            'good': true,
            'bad': false,
        }
    })
        .done((response) => {
            good_count = Object.keys(response).length;
            good_field.html(good_count);
            if ('{{ post_eval.good }}' == 'True') {
                good_button.addClass('btn-primary');
            }
        })
        .fail((response) => {
            console.log('GET method fail!');
            good_count = 0;
        })

    $.ajax({
        url: '{% url "apis:posteval-list" %}',
        method: 'GET',
        data: {
            'post': '{{ post.pk }}',
            'good': false,
            'bad': true
        }
    })
        .done((response) => {
            bad_count = Object.keys(response).length;
            bad_field.html(bad_count);
            if ('{{ post_eval.bad }}' == 'True') {
                bad_button.addClass('btn-danger');
            }
        })
        .fail((response) => {
            console.log('GET method fail!');
            bad_count = 0;
        })

    
    // PUT Method
    var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

    good_button.on('click', function () {
        $.ajax({
            url: '{% url "apis:posteval-detail" post_eval.pk %}',
            method: 'PUT',
            data: {
                'post': '{{ post.pk }}',
                'user': '{{ user.pk }}',
                'good': true,
                'bad': false,
            },
            headers: { "X-CSRFToken": $crf_token }, // csrf_token
        })
            .done((response) => {
                console.log('PUT method success');
                if (good_button.hasClass('btn-primary')) {
                    good_field.html(--good_count)
                    good_button.removeClass('btn-primary');
                } else {
                    if (bad_button.hasClass('btn-danger')) {
                        bad_field.html(--bad_count)
                        bad_button.removeClass('btn-danger');
                    }
                    good_field.html(++good_count);
                    good_button.addClass('btn-primary');
                }

            })
            .fail((response) => {
                console.log('Uncaught');
            })
    });

    bad_button.on('click', function () {

        $.ajax({
            url: '{% url "apis:posteval-detail" post_eval.pk %}',
            method: 'PUT',
            data: {
                'post': '{{ post.pk }}',
                'user': '{{ user.pk }}',
                'good': false,
                'bad': true,
            },
            headers: { "X-CSRFToken": $crf_token }, // csrf_token
        })
            .done((response) => {
                console.log('PUT method success');
                if (bad_button.hasClass('btn-danger')) {
                    bad_field.html(--bad_count)
                    bad_button.removeClass('btn-danger');
                } else {
                    if (good_button.hasClass('btn-primary')) {
                        good_field.html(--good_count)
                        good_button.removeClass('btn-primary');
                    }
                    bad_field.html(++bad_count);
                    bad_button.addClass('btn-danger');
                }
            })
            .fail((response) => {
                console.log('Uncaught')
            })
    });



});