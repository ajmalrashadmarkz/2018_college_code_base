/* @odoo-module */
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AttendanceDashboard extends Component {
    setup() {
        this.action = useService('action');
        this.state = useState({ 
            filteredDurationDates: [], 
            employeeData: [],
            monthOptions: []
        });
        this.orm = useService("orm");
        this.root = useRef('attendance-dashboard');
        
        onMounted(() => {
            this.populateMonthOptions();
            // Auto-select "This Month" on load
            const selectElement = this.root.el.querySelector('#filter_duration');
            if (selectElement) {
                selectElement.value = 'this_month';
                this.onclick_this_filter('this_month');
            }
        });
    }
    
    populateMonthOptions() {
        const months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        // Generate month options for current year and previous year
        const currentDate = new Date();
        const currentYear = currentDate.getFullYear();
        const prevYear = currentYear - 1;
        
        const options = [];
        
        // Add months for current year
        for (let i = 0; i < months.length; i++) {
            const monthNum = i + 1;
            const monthValue = `month_${currentYear}_${monthNum.toString().padStart(2, '0')}`;
            options.push({
                value: monthValue,
                label: `${months[i]} ${currentYear}`
            });
        }
        
        // Add months for previous year
        for (let i = 0; i < months.length; i++) {
            const monthNum = i + 1;
            const monthValue = `month_${prevYear}_${monthNum.toString().padStart(2, '0')}`;
            options.push({
                value: monthValue,
                label: `${months[i]} ${prevYear}`
            });
        }
        
        this.state.monthOptions = options;
    }

    async onChangeFilter(ev) {
        ev.stopPropagation();
        await this.onclick_this_filter(ev.target.value);
        console.log("Filtered dates received:", this.state.filteredDurationDates);
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
        let tBody = table.children[1].innerHTML;
        
        // Replace emoji symbols with more print-compatible symbols while preserving color
        tBody = tBody.replace(/❌/g, '<span style="color:red;">✘</span>');
        tBody = tBody.replace(/⭕/g, '<span style="color:red;">⊘</span>');
        tBody = tBody.replace(/✅/g, '<span style="color:green;">✔</span>');
        tBody = tBody.replace(/✔/g, '<span style="color:green;">✓</span>');
        
        return this.action.doAction({
            type: 'ir.actions.report',
            report_type: 'qweb-pdf',
            report_name: 'advance_hr_attendance_dashboard.report_hr_attendance',
            report_file: 'advance_hr_attendance_dashboard.report_hr_attendance',
            data: {'tHead': tHead, 'tBody': tBody}
        });
    }
    
    async onclick_this_filter(filterOption) {
        if (!filterOption) return;
        
        try {
            const result = await this.orm.call("hr.employee", "get_employee_leave_data", [filterOption]);
            
            // Debug log to check received data
            console.log("Received data from backend:", result);
            
            this.state.filteredDurationDates = result.filtered_duration_dates || [];
            this.state.employeeData = result.employee_data || [];
            
            console.log("Dates after assignment:", this.state.filteredDurationDates);
        } catch (error) {
            console.error("Error fetching employee data:", error);
        }
    }
    
    formatDate(inputDate) {
        if (!inputDate) return { display: '', isWeekend: false };
        
        // Parse the date string (in format 'YYYY-MM-DD')
        const parts = inputDate.split('-');
        if (parts.length !== 3) return { display: inputDate, isWeekend: false };
        
        const year = parseInt(parts[0]);
        const month = parseInt(parts[1]) - 1; // JavaScript months are 0-indexed
        const day = parseInt(parts[2]);
        
        const date = new Date(year, month, day);
        const isWeekend = date.getDay() === 0 || date.getDay() === 6; // 0 is Sunday, 6 is Saturday
        
        const dayStr = day.toString().padStart(2, '0');
        const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
        const monthStr = months[month];
        
        return {
            display: `${dayStr}-${monthStr}`,
            isWeekend: isWeekend
        };
    }
}

AttendanceDashboard.template = 'AttendanceDashboard';
registry.category("actions").add("attendance_dashboard", AttendanceDashboard);