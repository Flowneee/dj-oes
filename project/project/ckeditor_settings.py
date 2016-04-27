CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_myToolbar': [
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font',
                                         'FontSize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                       'Superscript', '-', 'RemoveFormat']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            '/',
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                       '-', 'Blockquote', 'CodeSnippet', 'Mathjax', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                       'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'insert',
             'items': ['Table', 'HorizontalRule', 'Smiley', 'SpecialChar']},
            {'name': 'other', 'items': [
                'Preview',
                'Source',
            ]},

        ],
        'toolbar': 'myToolbar',
        'mathJaxLib': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'codeSnippet_theme': 'monokai_sublime',
        'extraPlugins': ','.join(
            [
                'autolink',
                'autogrow',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'mathjax',
                'codesnippet',
            ]),
    }
}
