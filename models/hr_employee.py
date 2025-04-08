import pandas
from datetime import date, timedelta
from odoo import api, fields, models
from odoo.http import request
from odoo.tools import date_utils

class HrEmployee(models.Model):
    """This module extends the 'hr.employee' model of Odoo Employees Module.
     It adds a new method called 'get_employee_leave_data', which is used to
     retrieve data for the dashboard."""
    _inherit = 'hr.employee'
    _check_company_auto = True 

    @api.model
    def get_employee_leave_data(self, option):
        """Returns filtered attendance data based on user role (Admin/Employee)"""
        employee_data = []
        
        is_admin = self.env.user.has_group('base.group_system')
        res_config = self.env['res.config.settings'].search([], limit=1, order='id desc') if is_admin else None
        
       
        dates = False
        if option == 'this_week':
            dates = pandas.date_range(
                date_utils.start_of(fields.Date.today(), 'week'),
                date_utils.end_of(fields.Date.today(), 'week'),
                freq='d'
            ).strftime("%Y-%m-%d").tolist()
        elif option == 'this_month':
            dates = pandas.date_range(
                date_utils.start_of(fields.Date.today(), 'month'),
                date_utils.end_of(fields.Date.today(), 'month'),
                freq='d'
            ).strftime("%Y-%m-%d").tolist()
        elif option == 'last_15_days':
            dates = [str(date.today() - timedelta(days=day)) for day in range(15)]
        
        
        domain = [('company_id', 'in', self.env.companies.ids)]
        if not is_admin: 
            domain.append(('user_id', '=', self.env.user.id))
        
        employees = self.env['hr.employee'].search(domain)
        
        for employee in employees:
            leave_data = []
            
            present_dates = {str(attendance.check_in.date()) for attendance in employee.attendance_ids}
            
            total_leave_days = 0
            total_present_days = 0
            total_working_days = 0
            sick_leave_used = 0
            casual_leave_used = 0
            max_sick_leave = 7
            max_casual_leave = 12
            wfh_days_count = 0 
            
            
            self._cr.execute("""
                SELECT hl.request_date_from, hl.request_date_to, hlt.leave_code, hlt.color
                FROM hr_leave hl
                INNER JOIN hr_leave_type hlt ON hlt.id = hl.holiday_status_id 
                WHERE hl.state = 'validate' AND hl.employee_id = %s
            """, (employee.id,))
            
            leave_records = self._cr.dictfetchall()
            
            
            leave_date_map = {}
            
            for leave in leave_records:
                leave_range = pandas.date_range(
                    leave['request_date_from'], 
                    leave['request_date_to'], 
                    freq='d'
                ).strftime("%Y-%m-%d").tolist()

                
                if leave['leave_code'] == 'SL':
                    sick_leave_used += len(leave_range)
                elif leave['leave_code'] == 'CL':
                    casual_leave_used += len(leave_range)

                for l_date in leave_range:
                    leave_date_map[l_date] = {
                        'code': leave['leave_code'],
                        'color': leave['color']
                    }

            today = date.today()
            
            for d in dates:
                color = "#ffffff"
                state = "Absent"  
                
                
                if d in present_dates:
                    present_mark = self.env['ir.config_parameter'].sudo().get_param(
                        'advance_hr_attendance_dashboard.present', 'Present')
                    state = present_mark
                    total_present_days += 1
                else:
                    absent_mark = self.env['ir.config_parameter'].sudo().get_param(
                        'advance_hr_attendance_dashboard.absent', 'Absent')
                    state = absent_mark
                
                if d in leave_date_map:
                    state = leave_date_map[d]['code']
                    leave_color = leave_date_map[d]['color']
                    if state == "SL":  
                        color = "#F7CD1F"
                    elif state == "CL":  
                        color = "#ADD8E6"
                    elif state == "WFH":  
                        color = "#D3FFD3"
                    else:
                        color = "#F06050" if leave_color == 1 \
                            else "#F4A460" if leave_color == 2 \
                            else "#F7CD1F" if leave_color == 3 \
                            else "#6CC1ED" if leave_color == 4 \
                            else "#814968" if leave_color == 5 \
                            else "#EB7E7F" if leave_color == 6 \
                            else "#2C8397" if leave_color == 7 \
                            else "#475577" if leave_color == 8 \
                            else "#D6145F" if leave_color == 9 \
                            else "#30C381" if leave_color == 10 \
                            else "#9365B8" if leave_color == 11 \
                            else "#ffffff"
                    
                   
                    if state != "WFH":
                        total_leave_days += 1
                        if d in present_dates:
                            total_present_days -= 1
                    else:
                        # Only count WFH as working day if date is today or in the past
                        if d <= str(today):
                            wfh_days_count += 1


                
                leave_data.append({
                    'leave_date': d, 
                    'state': state, 
                    'color': color
                })
            
            remaining_sick_leave = max(0, max_sick_leave - sick_leave_used)
            remaining_casual_leave = max(0, max_casual_leave - casual_leave_used)

            
            employee_data.append({
                'id': employee.id,
                'name': employee.name,
                'leave_data': leave_data[::-1], 
                'total_leave_days': total_leave_days,
                'total_present_days': total_present_days,
                'total_working_days': total_present_days + wfh_days_count,
                'remaining_sick_leave': remaining_sick_leave,
                'remaining_casual_leave': remaining_casual_leave
            })

        return {
            'employee_data': employee_data, 
            'filtered_duration_dates': dates[::-1]  
        }