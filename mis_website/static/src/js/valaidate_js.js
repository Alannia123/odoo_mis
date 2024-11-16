odoo.define('mis_website.valaidate_js', [], function (require) {
    "use strict";


    var core = require("web.core");
    var time = require("web.time");
    var ajax = require("web.ajax");

    $(document).ready(function() {

	   var exact_age = document.getElementById("exact_age");

	    $( "#exact_age" ).keypress(function(evt) {
            var key = evt.keyCode;
            console.log('dddddddd========',key)

            var ASCIICode = (evt.which) ? evt.which : evt.keyCode
        if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
            return false;
        return true;

        });


        var mobile_whats = document.getElementById("mobile_whats");
        $( "#mobile_whats" ).keypress(function(evt) {
            var key = evt.keyCode;
            console.log('dddddddd========',key)

            var ASCIICode = (evt.which) ? evt.which : evt.keyCode
        if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
            return false;
        return true;

        });

        var alternate_phone = document.getElementById("alternate_phone");
        $( "#alternate_phone" ).keypress(function(evt) {
            var key = evt.keyCode;
            console.log('dddddddd========',key)

            var ASCIICode = (evt.which) ? evt.which : evt.keyCode
        if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
            return false;
        return true;

        });

        var aahar_no = document.getElementById("aahar_no");
        $( "#aahar_no" ).keypress(function(evt) {
            var key = evt.keyCode;
            console.log('dddddddd========',key)

            var ASCIICode = (evt.which) ? evt.which : evt.keyCode
        if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
            return false;
        return true;

        });






    });
});
