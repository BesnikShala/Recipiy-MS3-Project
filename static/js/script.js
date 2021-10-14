//  initialize javascript
$(document).ready(function () {
    $('.sidenav').sidenav({
        edge: "right"
    });
    $('.modal').modal();
    $('.parallax').parallax();
    $('select').formSelect();
   
    // Add new Ingredient Input
    let ingredient = 1;

    $(".add_ingredient").click(function (e) {
        e.preventDefault();
        ingredient++;
        $(".new_ingredient").append(`
            <div class="input-field col s12 m6">
            <input id ="recipe_ingredients${ingredient}" name="recipe_ingredients"
            type = "text" class = "validate"required><label
            for = "recipe_ingredients${ingredient}">Ingredients</label>
            <button class="btn delete_ingredient" type="button">-</button>`);
    });

    // Remove Ingredient Input

    $("body").on('click', ".delete_ingredient", function (){
        $(this).parent('div').remove();
        ingredient--;
    });
});