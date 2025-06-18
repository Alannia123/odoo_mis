from odoo import models
from datetime import date, timedelta

class ReportMonthlyAttendance(models.AbstractModel):
    _name = 'report.mis_education_attendances.monthly_attendance_report_temp'
    _description = 'Monthly Attendance Report'

    def _get_month_dates(self, year, month):
        start = date(year, month, 1)
        print('eeeeeeee44444444',start)
        end = (start.replace(month=month % 12 + 1, day=1) - timedelta(days=1))
        print('AQQQQQQQQQQQQQQQ',start)
        print('AQQQQQQQQQQQQQQQ',end)
        return [(start + timedelta(days=i)) for i in range((end - start).days + 1)]

    @staticmethod
    def _format_attendance(edu_attendances):
        result = {}
        for attendance in edu_attendances:
            for line in attendance.attendance_line_ids:
                student = line.student_id.id
                date_str = line.date.strftime('%Y-%m-%d')
                result.setdefault(student, {})[date_str] = line.present_morning
        return result

    def _get_report_values(self, docids, data=None):
        print('ttttttttttttttt',data)
        division_id = int(data['division_id'][0])
        month = int(data['month'])
        year = int(data['year'])
        students = self.env['education.student'].search([('class_division_id', '=', division_id)])
        print('STUUUUUUUUUUUUUU',students)
        dates = self._get_month_dates(year, month)

        edu_attendances = self.env['education.attendance'].search([
            ('date', '>=', dates[0]),
            ('date', '<=', dates[-1]),
        ])
        print('ATEEEEEEEEEEEEEEEE',edu_attendances)

        attendance_dict = self._format_attendance(edu_attendances)

        print('#######################',docids, students, dates, attendance_dict)

        return {
            'doc_ids': docids,
            'doc_model': 'education.attendance',
            'students': students,
            'dates': dates,
            'attendance_dict': attendance_dict,
            'standard_name': data['standard_name'],
            'month_str': data['month_str'],
            'month_str': data['month_str'],
            'academic_year_id': data['academic_year_id'][1],
        }
