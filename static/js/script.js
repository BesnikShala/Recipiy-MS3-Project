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
            <input id="recipe_ingredients${ingredient}" name="recipe_ingredients" type="text" class="validate"required>
            <label for="recipe_ingredients${ingredient}">Ingredients</label>
            <button class="btn red delete_ingredient" type="button"> - </button>
            </div>`
        );

    });

    // Remove Ingredient Input

    $("body").on('click', ".delete_ingredient", function (){
        $(this).parent('div').remove();
        ingredient--;
    });

    // Add New Utensil

    let utensil = 1;

    $(".add_utensil").click(function (e) {
        e.preventDefault();
        utensil++;
        $(".new_utensil").append(`
                <div class="input-field col s12 m6">
                <input id="recipe_tools${utensil} "name="recipe_tools"
                type="text" class="validate" required><label
                for="recipe_tools${utensil}">Utensils</label> 
                <button class="btn red delete_utensil"
                type="button">-</button>`);
        });

    // Remove Utensil

    $("body").on('click', ".delete_utensil", function () {
        $(this).parent('div').remove();
        utensil--;
    });

    // add instruction input field

    let instruction = 1;
    
    $(".add_instruction").click(function (e) {
        e.preventDefault();
        instruction++;
        $(".new_instruction").append(`
             <div class="input-field col s12 m6">
             <input id="recipe_instructions${instruction}"
             name = "recipe_instructions"
             type="text" class="validate" required><label
             for=recipe_instructions${instruction}"> instruction </label> 
             <button class="btn red delete_instruction"
             type="button ">-</button>`);
    });

    // remove instruction input field
    $("body").on('click', ".delete_instruction", function () {
        $(this).parent('div').remove();
        instruction--;
    });

});