$(document).ready(function(){

//refreshing events afer ajax call
    $('.dropdown-toggle').dropdown();

//Hide and show list form
	$(".listFormDiv").on("click",".addList", function(e){
	    $(this).parent().css('background-color', '#e8ede6')
		$(this).next("#listForm").toggle();
		$(this).hide();
	});

//    Hie and show card form
	$(".alllistDiv").on("click",".addCard", function(e){
		$(this).next(".cardForm").toggle();
		$(this).hide();
	});

	$(".container-fluid").on("click",".glyphicon-remove", function(e){
		$(this).parent().hide();
		$(this).parent().prev().show();
		$(this).closest(".listFormDiv").css('background-color', '')
	});


//    textarea
    $("textarea").attr("rows", "4");

// Hide carret in dropdown button
    $(".oneList").find(".caret").css("display","none");



// Hide and show form for moving card

    $(".side-menu").on("click", ".cardMove", function(){
        $("#moveCardForm").toggle();
        $(this).hide();
    });

//    Hide and show form in modal     te hide n show mozna przerobic na jedno

    $(".form-content").on("click", ".cardListModal", function(){
        $(".modalFormCard").toggle();
        $(this).hide();
    });

// Exit from modal's form
    $(".modal-content").on("click",".glyphicon-remove", function(e){
		$(this).parent().hide();
		$(this).parent().prev().toggle();
	});


//Creating lists
    $("#listForm").on("submit", function(e){
        $(this).hide();
        $(this).parent().css('background-color','');
        $(this).prev().show();
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/trello/create_list",
            data: {
                name: $(this).find("#id_name").val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(){
                location.reload();
                console.log("dodano");
                $("#listForm").find("#id_name").val("");


            }
        });
    })
//    Creating cards
        $(".cardForm").on("submit", function(e){
        e.preventDefault();
        var listId = $(this).data('id');
        $.ajax({
            type: "POST",
            url: "/trello/create_card",
            data: {
                name:$(this).find("#id_name").val(),
                description:$(this).find("#id_description").val(),
                list:listId,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(){
                location.reload();
                $(".cardForm").find("#id_name").val("");
                $(".cardForm").find("#id_description").val("");
                console.log("dodano karte");



            }
        });
    })

//    Insert data to edit form in modals

        $(".carditem").on("click", function(e){
        var id = $(this).data('id');

        $.ajax({
              dataType: "json",
              url: "detail_card/"+id,
              data: { get_param: 'value' },
              success: function(data){
                console.log(data);
                $(".modal-title").text(data.name);
                $(".modal-card-content").text(data.description);
                $(".modalFormCard").find("#id_name").val(data.name);
                $(".modalFormCard").find("#id_description").val(data.description);
                $(".modalFormCard").attr("data-id", data.id);
                $(".modalFormCard").attr("data-listid", data.list);
                $('[data-listidselect='+data.list+']').prop('selected', true);
              }
            });
        });


//    Editing cards
        $(".modalFormCard").on("submit", function(e){
            e.preventDefault();
            var cardId = $(this).data('id');
            $.ajax({
                type: "POST",
                url: "/trello/edit_card/"+cardId,
                data: {
                    name:$(this).find("#id_name").val(),
                    description:$(this).find("#id_description").val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(){
                    $('#modal').modal('toggle');
                    location.reload();
                    console.log("dodano karte");
                }
            });
        })


// Delete card
        $(".side-menu").on("click", ".cardDelete", function(e){
            e.preventDefault();
            var cardId = $(this).parent().prev().find(".modalFormCard").data('id');
            $.ajax({
                type: "POST",
                url: "/trello/delete_card/"+cardId,
                data: {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},
                success: function(){
                    $('#modal').modal('toggle');
                    location.reload();
                    console.log("usunieto karte");
                }
            })

        })


// Copy card
        $(".side-menu").on("click", ".cardCopy", function(e){
            e.preventDefault();
            var name = $(".modalFormCard").find("#id_name").val();
            var description = $(".modalFormCard").find("#id_description").val();
            var cardId = $(".modalFormCard").data('id')
            var listID = $(".modalFormCard").data('listid');
            $.ajax({
                type: "POST",
                url: "/trello/create_card",
                data: {
                    name: name,
                    description: description,
                    list: listID,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(){
                    $('#modal').modal('toggle');
                    location.reload();
                    console.log("skopiowano karte");
                }
            })

        })

// Moving card from one list to another
        $(".side-menu").on("click", ".moveButton", function(e){
            e.preventDefault();
            var cardId = $(".modalFormCard").data('id')
            $.ajax({
                type: "POST",
                url: "/trello/edit_card/"+cardId,
                data: {
                    list: $('#listOption').find(":selected").data('listidselect'),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(){
                    $('#modal').modal('toggle');
                    location.reload();
                    console.log("przeniesiono karte");
                }
            })

        })
// copy list
        $(".dropdown").on("click", ".copylist", function(e){
            e.preventDefault();
            console.log("jestem tu")
            var listid = $(this).data('id');
            $.ajax({
                type: "POST",
                url: "/trello/copy_list/"+listid,
                data: {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},
                success: function(){
                    location.reload();
                    console.log("skopiowano liste");
                }
            })
        });
//  removing list
        $(".dropdown").on("click", ".dellist", function(e){
            e.preventDefault();
            console.log("tu tex");
            var listid = $(this).data('id');
            $.ajax({
                type: "POST",
                url: "/trello/delete_list/"+listid,
                data: {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},
                success: function(){
                    location.reload();
                    console.log("usunieto liste");
                }
            })
        })

// removing all cards
        $(".dropdown").on("click", ".delallcards", function(e){
            e.preventDefault();
            console.log("tu tex");
            var listid = $(this).data('id');
            $.ajax({
                type: "POST",
                url: "/trello/delete_allcards/"+listid,
                data: {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},
                success: function(){
                    location.reload();
                    console.log("usunieto wszystkie karty");
                }
            })
        })

});





