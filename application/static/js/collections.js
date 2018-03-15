$("#form-collection").submit(function (event) {
    event.preventDefault();
    var form_data = $(this).serializeArray();
    $.ajax({
        type: 'POST',
        url: '/collections',
        data: form_data,
        success: function(response) {
            window.location.reload(true);
        }
    });
});

$('.collection-card').on('click', function() {
    var card = $(this);
    var id = card.attr('id');
    window.location.replace('/collections?id=' + id);
});

$(".collection-delete").on('click', function () {
    event.cancelBubble = true;
    if(event.stopPropagation) 
        event.stopPropagation();

    var card = $(this);
    var close_id = card.attr('id');
    var parts = close_id.split('-');
    var collection_id = parts[parts.length - 1];
    console.log(collection_id);
    $.ajax({
        type: 'DELETE',
        url: '/collections' + '?' + $.param({"id": collection_id}),
        contentType: "application/text; charset=utf-8",
        success: function(response) {
            window.location.reload(true);
        }
    });
});
