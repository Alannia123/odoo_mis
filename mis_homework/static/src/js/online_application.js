/** @odoo-module **/
// This file is used for adding filtration for online application form fields
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
publicWidget.registry.OnlineApplication = publicWidget.Widget.extend({
    selector: '#online_appl_form',
    events: {
        'change select[name="course"]': '_onCourseChange',
        'change select[name="semester"]': '_onSemesterChange',
        'submit form': '_onFormSubmit',
    },
     init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },
    async _onCourseChange(ev) {
        ev.preventDefault();
        var self = this
        var course = ev.currentTarget.value;
        self.$el.find('select[name="semester"]').find('option').remove()
        self.$el.find('select[name="semester"]').append("<option value=0></option>");
         self.$el.find('select[name="department"]').append("<option value=0></option>");
          const result = await this.orm.searchRead(
            'university.semester',
            [['department_id.course_id', '=', parseInt(course)]],['name']
        )
         result.forEach(function(item){
                    self.$el.find('select[name="semester"]').append("<option value=" + item['id'] + ">" +item['name'] + "</option>");
                })
        },
    async _onSemesterChange(ev){
        var self = this
        var semester = ev.currentTarget.value;
        self.$el.find('select[name="department"]').find('option').remove()
        self.$el.find('select[name="department"]').append("<option value=0></option>");
         const result = await this.orm.searchRead(
            'university.department',
            [['semester_ids', 'in', [parseInt(semester)]]],['name']
        )
        result.forEach(function(item){
                    self.$el.find('select[name="department"]').append("<option value=" + item['id'] + ">" +item['name'] + "</option>");
                })
      },
    _onFormSubmit(ev) {
        ev.preventDefault();
        // Validate fields
        const course = this.$('select[name="course"]').val();
        const semester = this.$('select[name="semester"]').val();
        const department = this.$('select[name="department"]').val();
        if (!course || !semester || department==0) {
            // If any required field is empty, show validation error
            this._displayErrorMessage('Some Fields are Empty!');
            return;
        }
        ev.currentTarget.submit();
    },
    _displayErrorMessage(message) {
        // Display error message near the submit button or form
        const errorMessage = `<div class="alert alert-danger" role="alert">${message}</div>`;
        this.$('.form-error-message').html(errorMessage);
    },
})



<input type="file" id="imageInput" accept="image/*">
<script>
document.getElementById("imageInput").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Set desired max width and height and quality
    const MAX_WIDTH = 800;
    const MAX_HEIGHT = 800;
    const QUALITY = 0.7;

    // Read the file as a data URL
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function(event) {
        const img = new Image();
        img.src = event.target.result;
        img.onload = function() {
            // Create a canvas element
            const canvas = document.createElement("canvas");
            let width = img.width;
            let height = img.height;

            // Resize if larger than max dimensions
            if (width > height) {
                if (width > MAX_WIDTH) {
                    height *= MAX_WIDTH / width;
                    width = MAX_WIDTH;
                }
            } else {
                if (height > MAX_HEIGHT) {
                    width *= MAX_HEIGHT / height;
                    height = MAX_HEIGHT;
                }
            }

            // Set canvas dimensions
            canvas.width = width;
            canvas.height = height;

            // Draw the image on the canvas
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);

            // Convert canvas to blob
            canvas.toBlob(
                function(blob) {
                    // Upload or handle the compressed blob
                    uploadCompressedImage(blob);
                },
                "image/jpeg",  // Image type
                QUALITY        // Compression quality
            );
        };
    };
});

function uploadCompressedImage(blob) {
    // You can use FormData to append the blob for upload
    const formData = new FormData();
    formData.append("image", blob, "compressed_image.jpg");

    // Replace with your server upload logic
    fetch("your-upload-endpoint", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error("Error:", error));
}
</script>

