tinymce.init({
    selector: 'textarea',  // change this value according to your HTML
    images_upload_url: '/media/upload_image/', // Django路由中图片上传地址
    height: 500,
    plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount'
    ],
    menubar: 'favs file edit view insert format tools table help',
    toolbar: 'undo redo | formatselect | ' +
        'bold italic backcolor | alignleft aligncenter ' +
        'alignright alignjustify | bullist numlist outdent indent | ' +
        'code image | ' +
        'removeformat | help',
    language: 'zh_CN',
});