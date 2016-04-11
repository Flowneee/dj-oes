import csv

from main.models import Subject, Question, Answer

ERROR = 'Error'
WARNING = 'Warning'
MESSAGE = 'Message'


class CsvParseMessage:

    def __init__(self, level, text, line, position, *args):
        self.lvl = level
        self.text = text
        self.line = line
        self.position = position
        self.args = args

    def __str__(self):
        return self.lvl + ': ' + str(self.text.format(self.line,
                                                      self.position,
                                                      *self.args))

    def get_str(self):
        return self.__str__()


def parse_subjects(subjects, line_number):
    s = subjects.split(r'/')
    subjects = []
    ignorable = ['', ' ']
    not_ignorable = []
    errors = []
    ret_status = 0
    for i in range(0,  len(s)):
        if not ((s[i] in ignorable) or (s[i] in not_ignorable)):
            subjects.append(s[i].strip())
        if s[i] in ignorable:
            errors.append(CsvParseMessage(WARNING, 'in line {0}: '
                                          'unacceptable subject "{2}"; '
                                          'ignored.', line_number, i, s[i]))
            ret_status = 1
        if s[i] in not_ignorable:
            errors.append(CsvParseMessage(ERROR, 'in line {0}: '
                                          'unacceptable subject "{2}"; '
                                          'cannot be ignored, '
                                          'whole line ignored.',
                                          line_number, i, s[i]))
            ret_status = 2
            break
    return subjects, ret_status, errors


def parse_question(question, line_number):
    unacceptable = ['', ' ', ]
    question = question.strip()
    ret_status = 0
    errors = []
    if question in unacceptable:
        errors.append(CsvParseMessage(ERROR, 'in line {0}: '
                                      'unacceptable question "{2}"; '
                                      'cannot be ignored, '
                                      'whole line ignored.',
                                      line_number, '', question))
        ret_status = 2
    return question, ret_status, errors


def parse_answers(answers, line_number):
    a = answers
    answers = []
    errors = []
    unacceptable = ['', ' ']
    ret_status = 0

    if len(a) < 4:
        errors.append(CsvParseMessage(ERROR, 'in line {0}: '
                                      'required at least 4 answers; '
                                      'cannot be ignored, '
                                      'whole line ignored.', line_number, ''))
        ret_status = 2
        return answers, ret_status, errors

    def answer_correct(s, u):
        return not (s in u) and not (s[:-1] in u) and\
            ((s[-1] == '1') or (s[-1] == '0'))

    for i in range(0, len(a)):
        if answer_correct(a[i], unacceptable):
            answers.append(a[i])
        else:
            errors.append(CsvParseMessage(WARNING, 'in line {0}: '
                                          'unacceptable answer "{2}"; '
                                          'ignored.', line_number, i, a[i]))
            ret_status = 1

    if len(answers) < 4:
        errors.append(CsvParseMessage(ERROR, 'in line {0}: '
                                      'required at least 4 correct answers; '
                                      'cannot be ignored, '
                                      'whole line ignored.',
                                      line_number, i))
        ret_status = 2
    return answers, ret_status, errors


def parse_csv_file(file_name, error_level='error'):

    def write_line_to_error(errors, error_level):
        for e in errors:
            if error_level == 'full':
                e.text += '\nLine: {0}'.format(row)
            if error_level == 'errors':
                if e.lvl == ERROR:
                    e.text += '\nLine: {0}'.format(row)

    csv_file = csv.reader(open(file_name, 'rt', newline=''), delimiter='`')
    errors = []
    ret_state = 0
    i = 0
    for row in csv_file:
        i += 1

        subjects, ret, errs = parse_subjects(row[0], i)
        write_line_to_error(errs, error_level)
        errors += errs
        subject = None
        if ret_state < ret:
            ret_state = ret
        if ret == 2:
            continue
        for s in subjects:
            subject, s_created = Subject.objects.get_or_create(
                text=s,
                parent_subject=subject
            )

        question, ret, errs = parse_question(row[1], i)
        write_line_to_error(errs, error_level)
        errors += errs
        if ret_state < ret:
            ret_state = ret
        if ret == 2:
            continue
        question, q_created = Question.objects.get_or_create(
            text=question,
            subject=subject,
        )

        answers, ret, errs = parse_answers(row[2:], i)
        write_line_to_error(errs, error_level)
        errors += errs
        if ret_state < ret:
            ret_state = ret
        if ret == 2:
            continue
        for a in answers:
            answer, a_created = Answer.objects.get_or_create(
                text=a[:-1].strip(),
                question=question,
                is_true=bool(int(a[-1]))
            )

    return ret_state, errors
