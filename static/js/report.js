get_all_capability_url = "/capability/all"
report_am_url="/am/report"
selected_list = []


$(function () {
    $.ajax({
        url: get_all_capability_url,
        method: 'GET'
    }).done(function (res) {
        var mySelect = $("#capSelect").mySelect({
            mult: true,//true-multi,false-single
            option: res,
            onChange: function (selected) {
                selected_list = selected
            }
        });
    })
})

$('#btn_form_submit').click(function () {
    var fd = new FormData();
    fd.append("name",$('#name').val())
    fd.append("website",$('#website').val())
    fd.append("address",$('#address').val())
    fd.append("interest",$('#interest').val())
    fd.append("product",$('#product').val())
    fd.append("project",$('#project').val())
    fd.append("description",$('#description').val())
    fd.append("capability",selected_list)
    $.ajax({
        type: 'post',
        url: report_am_url, 
        data: fd,
        cache: false,
        processData: false,
        contentType: false,
    }).done(function (res) {
        if (res.success) {
            BootstrapDialog.show({
                message: "Finish! Company ID is "+ res.companyId +". Return to Recommand System",
                buttons: [{
                    label: 'confirm',
                    cssClass: 'btn-primary',
                    action: function () {
                        window.location.href = "/static/page/rs.html"
                    }
                }, {
                    label: 'Close',
                    action: function (dialogItself) {
                        dialogItself.close();
                    }
                }]
            });
        } else {
            BootstrapDialog.alert("Server error!")
        }
    })
})