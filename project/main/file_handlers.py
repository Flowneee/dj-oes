import tempfile

from main import parser


def parse_csv(f, user):
    with tempfile.NamedTemporaryFile('w+b', delete=False) as temp:
        for chunk in f.chunks():
            temp.write(chunk)
    name = temp.name
    temp.close()
    return parser.parse_csv_file(name, user, 'errors')
