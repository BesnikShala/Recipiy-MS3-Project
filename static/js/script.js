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




    validateMaterializeSelect();

    function validateMaterializeSelect() {
        let classValid = {
            "border-bottom": "1px solid #4caf50",
            "box-shadow": "0 1px 0 0 #4caf50"
        };
        let classInvalid = {
            "border-bottom": "1px solid #f44336",
            "box-shadow": "0 1px 0 0 #f44336"
        };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({
                "display": "block",
                "height": "0",
                "padding": "0",
                "width": "0",
                "position": "absolute"
            });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }

});