var Thoughts = {

    loadThoughtsPage: function(button) {
        $(button).live('click', function() {
            var path = $(this).attr('rel');
            $.ajax(path).success(function(response) {
                    var parent = $(button).parent();
                    $(button).remove();
                    $(parent).append($(response).html());
                }
            );
        });
    }

};