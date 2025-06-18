/** @odoo-module */
import { registry} from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, onMounted} = owl
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";
import { WebClient } from "@web/webclient/webclient";
import { useRef } from "@odoo/owl";

export class EducationalDashboard extends Component {
    /**
     * Sets up the Education Dashboard component.
     */
    setup() {
        super.setup(...arguments);
        this.action = useService("action");
        this.orm = useService("orm");
         this.dashboard_templates = ['MainSection'];
        onWillStart(async () => {
            var self = this;
            this.props.title = 'Dashboard';
            $('.academic_exam_result').hide();
            $('.exam_result').show();
            $('.class_attendance_today').hide();
            $('.total_attendance_today').show();
        });
            onMounted(async () => {
                await this.render_graphs();
                this.fetch_data()
                await this.render_filters();
            });
        }
//    /* Orm call to fetch the count of applications, students, faculties,
//    amenities and total exams */
        fetch_data() {
            var self = this;
            this.orm.call("erp.dashboard", "erp_data", []
            ).then(function (result) {
                $('#all_applications').append('<span>' + result.applications + '</span>');
                $('#all_students').append('<span>' + result.students + '</span>');
                $('#all_faculties').append('<span>' + result.faculties + '</span>');
                $('#all_amenities').append('<span>' + result.amenities + '</span>');
                $('#all_exams').append('<span>' + result.exams + '</span>');
            });
        }
        change_select_period(e){
            e.preventDefault();
            if(e.target.value == 'select')
            {
                $('.academic_exam_result').hide();
                $('.exam_result').show();
                this.render_exam_result_pie();
            }
            else
            {
                $('.exam_result').hide();
                $('.academic_exam_result').show();
                this.get_academic_exam_result(e.target.value);
            }
          }
        change_select_class(e)
        {
            e.preventDefault();
            if(e.target.value == 'select')
            {
                $('.class_attendance_today').hide();
                $('.total_attendance_today').show();
                this.render_attendance_doughnut();
            }
            else
            {
                 $('.total_attendance_today').hide();
                 $('.class_attendance_today').show();
                 this.get_class_attendance(e.target.value);
            }
          }
//    /* Functions that to show the details on click event */
//    /* Click event function to show the applications */
        async onclick_application_list(e)
        {
            e.preventDefault();
            this.action.doAction({
                type: "ir.actions.act_window",
                name: "Applications",
                res_model: "education.application",
                views: [[false,'list'],[false,'form']],
                target: 'current',
                view_type : 'list',
                view_mode : 'list',
            });
      }
//    /* Click event function to show the students */
      onclick_student_list(e)
      {
        e.preventDefault();
        this.action.doAction({
             type: "ir.actions.act_window",
             name: "Students",
             res_model: "education.student",
             views: [[false,'list'],[false,'form']],
             target: 'current',
             view_type : 'list',
             view_mode : 'list',
         });
      }
//    /* Click event function to show the faculties */
      onclick_faculty_list(e){
         e.preventDefault();
         this.action.doAction({
             type: "ir.actions.act_window",
             name: "Faculties",
             res_model: "education.faculty",
             views: [[false,'list'],[false,'form']],
             target: 'current',
             view_type : 'list',
             view_mode : 'list',
         });
      }
//    /* Click event function to show the amenities */
      onclick_amenity_list(e){
        e.preventDefault();
        this.action.doAction({
             type: "ir.actions.act_window",
             name: "Amenities",
             res_model: "education.amenities",
             views: [[false,'list'],[false,'form']],
             target: 'current',
             view_type : 'list',
             view_mode : 'list',
        });
      }
//    /* Click event function to show the attendance list */
      onclick_attendance_list(e){
        e.preventDefault();
             this.action.doAction({
                 type: "ir.actions.act_window",
                 name: "Attendance",
                 res_model: "education.attendance",
                 views: [[false,'list'],[false,'form']],
                 target: 'current',
                 view_type : 'list',
                 view_mode : 'list',
               });
      }
//    /* Click event function to show the exam results */
      onclick_exam_result(e){
      e.preventDefault();
         this.action.doAction({
             type: "ir.actions.act_window",
             name: "Exam Result",
             res_model: "education.exam",
             views: [[false,'list'],[false,'form']],
             target: 'current',
             view_type : 'list',
             view_mode : 'list',
           });
      }
//    /* Click event function to show the time table */
      onclick_timetable(e){
        e.preventDefault();
             this.action.doAction({
                 type: "ir.actions.act_window",
                 name: "Timetable",
                 res_model: "education.timetable",
                 views: [[false,'list'],[false,'form']],
                 target: 'current',
                 view_type : 'list',
                 view_mode : 'list',
               });
      }
    /* Click event function to show the promotions */
      onclick_promotions(e){
        e.preventDefault();
             this.action.doAction({
                 type: "ir.actions.act_window",
                 name: "Student Promotions",
                 res_model: "education.student.final.result",
                 views: [[false,'list'],[false,'form']],
                 target: 'current',
                 view_type : 'list',
                 view_mode : 'list',
               });
      }
//    /* Calling the functions to creates charts */
      render_graphs(){
          var self = this;
          self.render_total_application_graph();
          self.render_exam_result_pie();
          self.render_attendance_doughnut();
          self.render_rejected_accepted_applications();
          self.render_student_strength();
          self.render_class_wise_average_marks();
      }
//    /* Calling the filter functions */
      render_filters(){
          var self = this;
          self.render_pie_chart_filter();
          self.render_doughnut_chart_filter();
      }
    /* Function to create a bar chart to show application counts in each
    academic year */
    /* Function to create a bar chart that shows the count of accepted and
    rejected applications */
    /* Function to create a pie chart that shows the exam results */
    render_exam_result_pie() {
        var self = this;
        var ctx = $(".exam_result")[0].getContext('2d');
        // Check if chart exists and destroy it
        if(self.chart_total_result){
            self.chart_total_result.destroy()
        }
        this.orm.call("erp.dashboard", "get_exam_result", []).then(function(result) {
            self.chart_total_result = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(result),
                    datasets: [{
                        label: 'Exam Result',
                        data: Object.values(result),
                        backgroundColor: [
                            "#003f5c",
                            "#dc143c"
                        ],
                        borderColor: [
                            "#003f5c",
                            "#dc143c",
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        },
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });
        })
    }
    /* Function to create a doughnut chart that shows attendance details */
      /* Function to create a line chart that shows the class wise student strength */
//    /* Function to create a bar chart that shows the average marks in each class */
    //    /* Function to add the filter option */
    //   /* Function to get academic wise exam result and to create chart accordingly */
    get_academic_exam_result(academic_year){
      var self = this;
      var ctx = $(".academic_exam_result")[0].getContext('2d');
      if(self.chart_academy_result){
                    self.chart_academy_result.destroy()
                }
      this.orm.call("erp.dashboard","get_academic_year_exam_result",[academic_year]
            ).then(function (result) {
            self.chart_academy_result = new Chart(ctx, {
                type: 'pie',
                data: {
                labels: Object.keys(result),
                     datasets: [{
                        label: 'Exam Result',
                        data: Object.values(result),
                        backgroundColor: [
                        "#003f5c",
                            "#dc143c"
                        ],
                          borderColor: [
                            "#003f5c",
                            "#dc143c",
                        ],
                        borderWidth: 1
                        }]
                        },
                        options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        },
                    },
                    responsive: true, // Instruct chart js to respond nicely.
                    maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                }
            });
        });
    }
    //    /* Function to add filter option for doughnut chart */
    /* Function to get class wise attendance and to create chart accordingly */
}
EducationalDashboard.template = "EducationalDashboard"
registry.category("actions").add("erp_dashboard_tag", EducationalDashboard)

