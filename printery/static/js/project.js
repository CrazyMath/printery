/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

jQuery(document).ready(function ($) {

    $('.form-group').removeClass('row');

    var messagesBlock = $('#messages'),
        messages = messagesBlock.find('li');
    if (messages.length !== 0) {
        $.each(messages, function (i, e) {
            var message_type = $(e).attr('data-message-type'),
                message = $(e).text();
            if (message_type === 'success') {
                toastr.success(message)
            } else if (message_type === 'error') {
                toastr.error(message)
            } else if (message_type === 'info') {
                toastr.info(message);
            } else {
                console.log('Message isn\'t determined for type: ' + message_type);
                console.log('Message: ' + message)
            }
        })
    }
    var myModal = $('#myModal');
    $(document).on('click', '.assign_writer, .edit_article', function (e) {
        e.preventDefault();
        var _this = $(this);
        myModal.modal('show');
        myModal.find('#modal-form').find('.input').attr('name', _this.attr('data-input-name'))
            .attr('type', _this.attr('data-input-type'))
            .val(_this.attr('data-input-value'));
        myModal.find('#modal-form').attr('action', _this.attr('data-url'));
        myModal.find('#exampleModalLabel').html(_this.attr('data-modal-title'));
        // myModal.find('.message').html('Are you sure that you want to assign "' + _this.attr('data-title') + '" to yourself?')
        myModal.find('.message').html(_this.attr('data-message'));
        myModal.find('.submit').html(_this.attr('data-button-title'));
    });
    $(document).on('submit', '#modal-form', function (e) {
        e.preventDefault();
        var _this = $(this);
        var actionUrl = _this.attr('action');
        var method = _this.attr('method');
        var data = _this.serialize();
        var ajaxError = $('.ajax-error');
        console.log(data)

        ajaxError.parents('.has-error').removeClass('has-error');
        ajaxError.remove();
        $.ajax({
            url: actionUrl,
            method: method,
            beforeSend: function () {
                $("#loader").show();
            },
            complete: function () {
                $('#loader').hide();
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            data: data,
            success: function (data) {
                // toastr.success(gettext('Article was assigned successfully!'));
                myModal.modal('hide');
                location.reload();
            },
            error: function (data) {
                var message = '';
                if (data.hasOwnProperty('status') && data['status'] === 400) {
                    message = 'An error occurred. Please check form.';
                    var errorMessages = data['responseJSON'];
                    $.each(Object.keys(errorMessages), function (i, key) {
                        var error = '';
                        if (key === 'non_field_errors') {
                            error = '<div class="form-group ajax-error">' +
                                '<ul class="errorlist">' +
                                '<li>' + errorMessages[key][0] + '</li>' +
                                '</ul>' +
                                '</div>';
                            _this.prepend(error);
                        } else {
                            error = '<span class="help-block ajax-error">' + errorMessages[key][0] + '</span>';
                            _this.find('label[for="' + key + '"]').after(error).parents('.form-group').addClass('has-error');
                        }
                    });


                } else {
                    message = gettext('An error occurred. Try again later.');
                }
                // toastr.error(message)
            }
        })

    });


});
