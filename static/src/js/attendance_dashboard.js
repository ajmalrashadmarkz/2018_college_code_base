/* @odoo-module */
import { Component, useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AttendanceDashboard extends Component {
    setup() {
        this.action = useService('action');
        this.state = useState({ 
            filteredDurationDates: [], 
            employeeData: [] 
        });
        this.orm = useService("orm");
        this.root = useRef('attendance-dashboard');
    }

    onChangeFilter(ev) {
        ev.stopPropagation();
        this.onclick_this_filter(ev.target.value);
    }
    
    _OnClickSearchEmployee(ev) {
        const searchbar = this.root.el.querySelector('#search-bar')?.value?.toLowerCase() || '';
        const attendance_table_rows = this.root.el.querySelector('#attendance_table_nm')?.children[1];
        
        if (attendance_table_rows) {
            for (let tableData of attendance_table_rows.children) {
                const dataName = tableData.children[0].getAttribute("data-name")?.toLowerCase() || '';
                tableData.style.display = (!dataName.includes(searchbar)) ? 'none' : '';
            }
        }
    }
    
    _OnClickPdfReport(ev) {
        const table = this.root.el.querySelector('#attendance_table_nm');
        if (!table) return;
        
        const tHead = table.children[0].innerHTML;
        const tBody = table.children[1].innerHTML;
        
        return this.action.doAction({
            type: 'ir.actions.report',
            report_type: 'qweb-pdf',
            report_name: 'advance_hr_attendance_dashboard.report_hr_attendance',
            report_file: 'advance_hr_attendance_dashboard.report_hr_attendance',
            data: {'tHead': tHead, 'tBody': tBody}
        });
    }
    
    async onclick_this_filter(filterOption) {
        try {
            const result = await this.orm.call("hr.employee", "get_employee_leave_data", [filterOption]);
            this.state.filteredDurationDates = result.filtered_duration_dates;
            this.state.employeeData = result.employee_data;
        } catch (error) {
            console.error("Error fetching employee data:", error);
        }
    }
    
    formatDate(inputDate) {
        if (!inputDate) return '';
        const months = [
            'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
            'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
        ];
        const parts = inputDate.split('-');
        if (parts.length !== 3) return inputDate;
        
        const day = parts[2];
        const month = months[parseInt(parts[1], 10) - 1];
        const year = parts[0];
        return `${day}-${month}-${year}`;
    }
}
AttendanceDashboard.template = 'AttendanceDashboard';
registry.category("actions").add("attendance_dashboard", AttendanceDashboard);
