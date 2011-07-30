var Thoughts = {

    createThought: function() {
        $('textarea').autoResize();
        $('textarea').focus();

        var changeTimeout = null;
        $('#text').keyup(function() {
            if (changeTimeout) {
                clearTimeout(changeTimeout);
            }
            changeTimeout = setTimeout(function() {
                var text = $("#text").val();
                $('#tagsDetectionForm #text').val(text);
                $('#tagsDetectionForm').ajaxSubmit({
                    success: function(response) {
                        console.log(response);
                        $('#tags').val(response);
                    }
                })
            }, 500)
        })
    },

    editThought: function() {
        $('textarea').autoResize();
        $('textarea').focus();
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