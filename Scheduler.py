from collections import defaultdict
from itertools import cycle

class Scheduler:
    def __init__(self, areas_list, students_list, area_student_counts):
        self.areas_list = areas_list
        self.students_list = students_list
        self.area_student_counts = area_student_counts
        self.schedule = defaultdict(lambda: defaultdict(list))
        self.create_schedule()  # You can keep this call here and remove from main.py

    def create_schedule(self):
        rotations = len(self.areas_list) - 1  # If you want equal number of rotations in each area, you might want to remove '- 1'
        student_assignments = {student['Name']: [student['Area']] for student in self.students_list}
        
        for rotation in range(rotations):
            area_counts = self.area_student_counts.copy()
            for _ in range(len(self.students_list)):  # Limit the cycle
                student = next(cycle(self.students_list))
                if all(area_counts[area] == 0 for area in self.areas_list):
                    break  # break out of the loop once all areas are filled for this rotation
                
                available_areas = [area for area in self.areas_list if area not in student_assignments[student['Name']] and area_counts[area] > 0]
                if available_areas:
                    assigned_area = available_areas[0]
                    self.schedule[assigned_area][rotation + 1].append(student['Name'])
                    student_assignments[student['Name']].append(assigned_area)
                    area_counts[assigned_area] -= 1
        
    def print_schedule(self):
        for area, rotations in self.schedule.items():
            print(f"{area}:")
            for rotation, students in rotations.items():
                print(f"    Rotation {rotation}: {', '.join(students)}")