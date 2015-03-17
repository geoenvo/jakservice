$(document).ready(function() {
    $('#filter input.datepicker').datepicker({
        format: "yyyy-mm-dd",
        autoclose: true,
        todayBtn: "linked",
        todayHighlight: true,
    });
});