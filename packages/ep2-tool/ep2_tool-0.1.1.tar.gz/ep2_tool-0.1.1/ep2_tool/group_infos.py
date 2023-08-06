import re
from ep2_tool.group import Group
from collections import namedtuple


Student = namedtuple('Student', 'name matrikelnr email group_name')


class GroupInfos:
    """
    Reads, parses and stores all information about all groups,
    like the names of the groups, the names of the instructors and tutors,
    and the names, register-numbers and emails of all students.
    """

    def __init__(self, repo_path=''):
        """Initializes the instance. Reads and parses all the infos from files in the pk repo."""
        self.repo_path = repo_path
        self.groups = dict()

        self.__read_group_infos()
        self.__read_student_lists()

    def tutor_names(self):
        """Returns a list of the names of all tutors"""
        groups = [[group.tutor1, group.tutor2] for group in self.groups.values()]
        names = set(name for group in groups for name in group)
        names.add('')
        return sorted(names)

    def get_group_info(self, group_name):
        """Returns the info for a specific group"""
        if group_name not in self.groups:
            self.groups[group_name] = Group(group_name)
        return self.groups[group_name]

    def get_involved_groups(self, tutor_name):
        """Returns a list of names of all groups a tutor is involved in"""
        return [name for name, info in self.groups.items() if tutor_name in [info.tutor1, info.tutor2]]

    def get_group_names(self, allowed_types=None):
        """
        Returns a list of group names, which are of a certain type that can be specified the
        parameter allowed_types, which is a list of strings like 'normal' or 'fortgeschritten'.
        If allowed_types is None, a list of all groups is returned.
        """
        if allowed_types is None:
            return [name for name in self.groups]
        else:
            return [name for name, group in self.groups.items() if group.group_type in allowed_types]

    def get_student(self, matrikelnr):
        """Finds the student object for a given matrikelnr"""
        for group in self.groups.values():
            for student in group.students:
                if student.matrikelnr == matrikelnr:
                    return student

        return Student('', matrikelnr, '', '')

    @staticmethod
    def split_file_into_parts(filename, regex):
        """Splits the lines of a file into parts. It starts a new part if the line matches a regex."""
        file_parts = []

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if regex.search(line):
                        file_parts.append([])
                    if file_parts:
                        file_parts[-1].append(line)
        except IOError:
            pass

        return file_parts

    def __read_group_infos(self):
        """
        Parses the file "GRUPPEN.txt" and stores the data for all student groups.
        This includes group, instructor and tutor names.
        """
        path = self.repo_path + '/GRUPPEN.txt'
        name_regex = re.compile(r'\[((mo|di|mi|do|fr)\d{2}\w)\]')
        name_simple_regex = re.compile(r'\[.*\]')

        for part in self.split_file_into_parts(path, name_simple_regex):
            match = name_regex.search(part[0])
            if match:
                group_name = match.group(1)
            else:
                continue

            info = dict()
            for line in part[1:]:
                for title in 'leiter tutor1 tutor2 ersatz'.split():
                    if line.startswith(title) and '=' in line:
                        info[title] = line.split('=')[-1].strip()

            self.groups[group_name] = Group(name=group_name)

    def __read_student_lists(self):
        """
        Reads the files 'groups_fortgeschritten.txt' und 'groups_normal.txt',
        and extracts all groups and student data.
        """
        path_template = self.repo_path + '/Anwesenheiten/Anmeldung/groups_{group_type}.txt'
        group_name_regex = re.compile(r'(mo|di|mi|do|fr)\d{2}\w')
        student_regex = re.compile(r'\s+[+✔]\s+(\D+)\s(\d+)\s(.*)\s?')

        for group_type in ['fortgeschritten', 'normal']:
            path = path_template.format(group_type=group_type)
            for part in self.split_file_into_parts(path, group_name_regex):
                group_name = group_name_regex.search(part[0]).group(0)
                group = self.get_group_info(group_name)
                group.group_type = group_type

                for line in part[1:]:
                    match = student_regex.search(line)
                    if match:
                        group.add_student(Student(*([match.group(i) for i in range(1, 4)] + [group_name])))
