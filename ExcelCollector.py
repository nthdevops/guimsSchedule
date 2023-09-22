import warnings
import pandas as pd
from tabulate import tabulate  # Assuming you are using tabulate to print the students list in tabular form

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

class ExcelCollector:
    def __init__(self, file_path):
        self.file_path = file_path
        self.days = 0
        self.areas_list = []
        self.students_list = []
        self.area_student_counts = {}
        self.read_configuration_tab()
        self.read_areas_tab()
        self.read_students_tab()
        self.get_area_student_counts()

    def read_configuration_tab(self):
        config_df = pd.read_excel(self.file_path, sheet_name='Configuration')
        try:
            self.days = int(config_df.loc[0, 'Days'])
        except ValueError:
            raise ValueError('Invalid value for Days in Configuration tab')

    def read_areas_tab(self):
        areas_df = pd.read_excel(self.file_path, sheet_name='Areas', header=None)
        self.areas_list = areas_df.iloc[:, 0].tolist()
        if not self.areas_list or all(not area for area in self.areas_list):
            raise ValueError('No areas found in Areas tab')

    def read_students_tab(self):
        students_df = pd.read_excel(self.file_path, sheet_name='Students')
        for index, row in students_df.iterrows():
            student_name = row.get('Name')
            area_assigned = row.get('Area')
            if not student_name or not area_assigned:
                raise ValueError(f'Invalid data in Students tab at row {index + 2}')
            if area_assigned not in self.areas_list:
                raise ValueError(f'Student {student_name} is assigned to non-existing area {area_assigned}')
            self.students_list.append({'Name': student_name, 'Area': area_assigned})

    def get_area_student_counts(self):
        """
        Method to populate area_student_counts with initial counts of students in each area.
        """
        for area in self.areas_list:
            count = sum(1 for student in self.students_list if student['Area'] == area)
            self.area_student_counts[area] = count

    def print_data(self):
        print('Days:', self.days)
        print('Areas:', self.areas_list)
        print('Area Student Counts:', self.area_student_counts)
        print('Students:')
        print(tabulate(self.students_list, headers='keys', tablefmt='grid'))