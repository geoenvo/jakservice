$(document).ready(function() {
    if ($('#filter input.datepicker').length > 0) {
        $('#filter input.datepicker').datepicker({
            format: "yyyy-mm-dd",
            autoclose: true,
            todayBtn: "linked",
            todayHighlight: true,
        });
    }
});