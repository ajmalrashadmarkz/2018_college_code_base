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
        
        dates = []
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
            dates = [str(date.today() - timedelta(days=14 - day)) for day in range(15)]
        elif option.startswith('month_'):
            # Format is "month_YYYY_MM" (e.g., "month_2024_01" for January 2024)
            year_month = option.split('_')[1:]
            year = int(year_month[0])
            month = int(year_month[1])
            
            # Get the first and last day of the specified month
            first_day = date(year, month, 1)
            if month == 12:
                last_day = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = date(year, month + 1, 1) - timedelta(days=1)
                
            dates = pandas.date_range(
                first_day,
                last_day,
                freq='d'
            ).strftime("%Y-%m-%d").tolist()
        
        # Sort dates in descending order
        if dates:
            dates.sort()
            print(f"Sorted dates in descending order: {dates}")  # Debug output
        
        # Create a mapping for weekends (Saturday and Sunday)
        weekend_map = {}
        for d in dates:
            date_obj = date.fromisoformat(d)
            # 5 is Saturday, 6 is Sunday in the weekday() method
            weekend_map[d] = date_obj.weekday() >= 5
        
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
            
            # Make sure leave_data matches the order of dates
            for d in dates:
                color = "#ffffff"
                state = "Absent"  
                is_weekend = weekend_map.get(d, False)
                
                if is_weekend:
                    # Set weekend color and state
                    color = "#E8E8E8"  # Light gray for weekends
                    state = ""
                elif d in present_dates:
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
                    'color': color,
                    'is_weekend': is_weekend
                })
            
            remaining_sick_leave = max(0, max_sick_leave - sick_leave_used)
            remaining_casual_leave = max(0, max_casual_leave - casual_leave_used)
            
            employee_data.append({
                'id': employee.id,
                'name': employee.name,
                'leave_data': leave_data,  # Leave data is in the same order as dates (descending)
                'total_leave_days': total_leave_days,
                'total_present_days': total_present_days,
                'total_working_days': total_present_days + wfh_days_count,
                'remaining_sick_leave': remaining_sick_leave,
                'remaining_casual_leave': remaining_casual_leave
            })

        # Add debug logging
        print(f"Returning {len(dates)} dates and {len(employee_data)} employee records")
        
        return {
            'employee_data': employee_data, 
            'filtered_duration_dates': dates  # Already sorted in descending order
        }