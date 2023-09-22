from ExcelCollector import ExcelCollector
from Scheduler import Scheduler

collector = ExcelCollector('dados.xlsx')
collector.print_data()
scheduler = Scheduler(collector.areas_list, collector.students_list, collector.area_student_counts)
scheduler.print_schedule()