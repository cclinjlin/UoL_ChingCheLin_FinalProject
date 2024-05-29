$('#btn_file_submit').click(function () {
    alert('submit')
    var fd = new FormData();
    fd.append('file', $('#upload_file')[0].files[0])
    $.ajax({
        type: 'post',
        url: "/am/upload", //must be absolute route
        data: fd,
        cache: false,
        processData: false,
        contentType: false,
    }).done(function (res) {
        if (res.success) {
            BootstrapDialog.show({
                size: BootstrapDialog.SIZE_LARGE,
                message: 'Upload success!',
                buttons: [{
                    label: 'confirm',
                    cssClass: 'btn-primary',
                    action: function () {
                        window.location.href = "/static/page/rs.html"
                    }
                }]
            });
        } else {
            BootstrapDialog.alert('文件格式或系统故障!,请重新上传');
        }
        // after success, confirm to db
    }).fail(function (res) {
        BootstrapDialog.alert('上传失败!,请重新上传');
    });
})