get_newesst_10_am_information_url = "/am/newest10"
get_am_by_company_name_url = "/am"
get_am_recommend_by_company_description_url = "/am/recommend/base_description"
get_am_recommend_by_company_id_url="/am/recommend/base_id"

cols = [{
    align: "center", 
    halign: "center", 
    field: "CompanyID",
    title: "Company ID"
},
{
    align: "center", 
    halign: "center", 
    field: "CompanyName",
    title: "Name"
},
{
    align: "center", 
    halign: "center", 
    field: "CompanyDescription",
    title: "Description"
},
{
    align: "center", 
    halign: "center", 
    field: "DefaultAddress",
    title: "Address"
},
{
    align: "center", 
    halign: "center", 
    field: "Interests",
    title: "Interests"
},
{
    align: "center", 
    halign: "center", 
    field: "Products",
    title: "Products"
},
{
    align: "center", 
    halign: "center", 
    field: "Projects",
    title: "Projects"
}
]

// via company name, search manufacture
$('#company_name_submit').click(function () {
    company_name = $('#company_name').val()
    $.ajax({
        url: get_am_by_company_name_url,
        type: 'GET',
        data: { 'company_name': company_name }
    }).done(function (res) {
        if (res.success) {
            console.log(res.data)
            $("#result_table").bootstrapTable('refreshOptions', {
                data: res.data
            })
        } else {
            BootstrapDialog.show({
                type: BootstrapDialog.TYPE_DANGER,
                message: res.msg + " Hope you can help us supplement the information.",
                buttons: [{
                    label: 'confirm',
                    cssClass: 'btn-primary',
                    action: function () {
                        window.location.href = "/static/page/report.html"
                    }
                }, {
                    label: 'Close',
                    action: function (dialogItself) {
                        dialogItself.close();
                    }
                }]
            });
        }
    })
})

// based on description, search for similar manufacturing
$('#company_description_submit').click(function () {
    company_description = $('#company_description').val()
    $.ajax({
        url: get_am_recommend_by_company_description_url,
        type: 'GET',
        data: { 'company_description': company_description }
    }).done(function (res) {
        if (res.success) {
            console.log(res.data)
            $("#result_table").bootstrapTable('refreshOptions', {
                data: res.data
            })
        } else {
            BootstrapDialog.alert("Server error!")
        }
    })
})

// double click
var rowDBClick = function (row, $element, field) {
    // BootstrapDialog.alert(JSON.stringify(row));
    msg="Should I recommend a similar manufacturer based on a company with id of "+row.CompanyID+" ?"
    BootstrapDialog.show({
        type: BootstrapDialog.TYPE_INFO,
        message: msg,
        buttons: [{
            label: 'Confirm',
            cssClass: 'btn-primary',
            action: function (dialogItself) {
                $.ajax({
                    url: get_am_recommend_by_company_id_url,
                    type: 'GET',
                    data: {'company_id': row.CompanyID}
                }).done(function (res) {
                    if (res.success) {
                        console.log(res.data)
                        $("#result_table").bootstrapTable('refreshOptions', {
                            data: res.data
                        })
                    } else {
                        BootstrapDialog.alert("Server error!")
                    }
                })
                dialogItself.close();
            }
        }, {
            label: 'Cancel',
            action: function (dialogItself) {
                dialogItself.close();
            }
        }]
    });
}

// initialize the table, show latest 10 data
$.ajax({
    url: get_newesst_10_am_information_url,
    type: 'get',
    cache: false,
    processData: false,
    contentType: false
}).done(function (res) {
    $("#result_table").bootstrapTable({
        pagination: true, // tab window (page) function
        pageSize: 10, // default
        pageList: [5, 10, 15, 20], // size options
        striped: true, // striped
        columns: cols,
        data: res,
        onDblClickRow: rowDBClick
    });
}).fail(function (res) {
    BootstrapDialog.alert('fail to get initial data');
});