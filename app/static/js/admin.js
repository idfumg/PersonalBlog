function display_wysiwyg(element, air_mode, focus) {
    air_mode = typeof air_mode !== 'undefined' ? air_mode : true;
    focus = typeof focus !== 'undefined' ? focus : true;

    var air_data = [
        //[groupname, [button list]]

        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['font', ['strikethrough', 'superscript', 'subscript']],
        ['fontsize', ['fontsize', 'fontname', 'style']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
    ]

    var font_names =  [
        'Serif', 'Sans', 'Arial', 'Arial Black', 'Courier',
        'Courier New', 'Comic Sans MS', 'Helvetica', 'Impact',
        'Lucida Grande', 'Clearly', 'Redressed'
    ];

    var font_names_ignore_check = [
        'Clearly', 'Redressed'
    ];

    var summernote_dict = {
        focus: focus,
        airMode: air_mode,
        airPopover: air_data,
        fontNames: font_names,
        fontNamesIgnoreCheck: font_names_ignore_check
    };

    element.summernote(summernote_dict);
}

function hide_wysiwyg(element) {
    element.destroy();
}

function setup_toolbar(toolbar, header_elem, text_elem, intro_elem) {
    var toggle = false;
    toolbar.bind('click', function() {
        hide_wysiwyg(header_elem);
        hide_wysiwyg(text_elem);
        hide_wysiwyg(intro_elem);
        display_wysiwyg(header_elem, toggle);
        display_wysiwyg(text_elem, toggle);
        display_wysiwyg(intro_elem, toggle);
        toggle = !toggle;
    });
}

function setup_post_save_action(element, id, tip_elem, header, text, domain, intro) {
    id = typeof id !== 'undefined' ? id : null;
    element.bind('click', function() {
        function on_complete(data) {
            tip_elem.fadeIn(500).fadeOut(1000);
        }

        var query = '/post/save';

        if (id)
            query += '/' + id;

        var data = {
            header: header.code(),
            intro: intro.code(),
            text: text.code(),
            domain: domain.val()
        };

        $.post(query,
               data,
               on_complete,
               'json');

        return false;
    });
}

function setup_delete_restore_button(id,
                                     post_elem,
                                     del_button,
                                     res_button) {
    function on_complete_delete(data) {
        post_elem.fadeTo(700, 0.4, function() {
            del_button.hide();
            res_button.show();
        });
    }

    function on_complete_restore(data) {
        post_elem.fadeTo(700, 1, function() {
            del_button.show();
            res_button.hide();
        });
    }

    if (!id || !post_elem)
        return;

    res_button.bind('click', function() {
        $.post('/post/restore/' + id, {}, on_complete_restore);
    });

    del_button.bind('click', function() {
        $.post('/post/del/' + id, {}, on_complete_delete);
    });
}

function setup_erase_button(id, post_elem, erase_button) {
    function on_complete(data) {
        post_elem.hide();
    }

    if (!id)
        return;

    erase_button.bind('click', function() {
        $.post('/post/erase/' + id, {}, on_complete);
    });
}
