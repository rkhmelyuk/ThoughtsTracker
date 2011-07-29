var Thoughts = {

    editThought: function() {
        $('textarea').autoResize();
        $('textarea').focus();
        $('#text').change(function() {
            var text = $(this).val();
            // TODO - use websocket
            $('#tagsDetectionForm #text').val(text);
            $('#tagsDetectionForm').ajaxSubmit({
                success: function(response) {
                    console.log(response);
                    $('#tags').val(response);
                }
            })
        })
    },

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
    },

    settings: function() {
        
    }

};