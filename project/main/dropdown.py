# coding: utf-8


class SubjectNode():
    def __init__(self, string_repr, record_id):
        self.string_repr = string_repr
        self.record_id = record_id


def create_dropdown(data, parent=None, lvl=0, indent=4):
    indentation = ' ' * indent
    nodes = []
    for obj in data.filter(parent_subject=parent):
        nodes.append(SubjectNode(indentation * lvl + str(obj), str(obj.id)))
        nodes += create_dropdown(data, obj, lvl=lvl+1, indent=indent)
    return nodes
