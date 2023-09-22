from collections import defaultdict
from itertools import cycle
from random import shuffle

class Scheduler:
    def __init__(self, areas_list, students_list, area_student_counts):
        self.areas_list = areas_list
        self.students_list = students_list
        self.area_student_counts = area_student_counts
        self.schedule = defaultdict(lambda: defaultdict(list))
        self.create_schedule()

    def create_schedule(self):
        rotations = len(self.areas_list) - 1  # Each student rotates to every other area exactly once
        student_assignments = {student['Name']: [student['Area']] for student in self.students_list}
        
        for rotation in range(rotations):
            area_counts = self.area_student_counts.copy()
            students_cycle = cycle(self.students_list)
            
            # Shuffle students for each rotation for a fair and balanced distribution
            shuffled_students = self.students_list.copy()
            shuffle(shuffled_students)
            
            for student in shuffled_students:
                available_areas = [
                    area for area in self.areas_list 
                    if area not in student_assignments[student['Name']] 
                    and area_counts[area] > 0
                ]
                
                # If no available areas, continue to the next student
                if not available_areas:
                    continue
                
                # Assign student to an available area and update the counts
                assigned_area = available_areas[0]
                self.schedule[assigned_area][rotation + 1].append(student['Name'])
                student_assignments[student['Name']].append(assigned_area)
                area_counts[assigned_area] -= 1
                
                # If all areas are filled for this rotation, break out of the loop
                if all(count == 0 for count in area_counts.values()):
                    break

    def print_schedule(self):
        for area, rotations in self.schedule.items():
            print(f"{area}:")
            for rotation, students in rotations.items():
                print(f"    Rotation {rotation}: {', '.join(students)}")