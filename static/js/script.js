//  initialize javascript
$(document).ready(function () {
    $('.sidenav').sidenav({
        edge: "right"
    });
    $('.modal').modal();
    $('.parallax').parallax();
    $('select').formSelect();
    $('.chips-initial').chips({
        autocompleteOptions: {
            //  data: [{
            //      tag: 'e.g carrots'
            //  }],
        },
        onChipAdd: function (autocomplete, tag) {
            $(tag).find('.material-icons').removeClass('material-icons').addClass('fas fa-times right').text('');
            $(".chip").attr("name", "recipe_ingredients");
        }
    });

});