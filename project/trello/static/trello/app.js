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

//    Hide and show form in modal
    $(".form-content").on("click", ".cardListModal", function(){
        $(".modalFormCard").toggle();
        $(this).hide();
    });

    $(".modal-content").on("click",".glyphicon-remove", function(e){
		$(this).parent().hide();
		$(this).parent().prev().show();
		$(this).closest(".listFormDiv").css('background-color', '')
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
                $( "body" ).load( window.location.href );
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
                $("body").load(window.location.href);
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
                ;
                $(".modalFormCard").find("#id_name").val(data.name);
                $(".modalFormCard").find("#id_description").val(data.description);
                $(".modalFormCard").attr("data-id", data.id);
                $(".modalFormCard").attr("data-listid", data.list);
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
                    $("body").load(window.location.href);
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
                    $("body").load(window.location.href);
                    console.log("usunieto karte");
                }
            })

        })


// Copy card
        $(".side-menu").on("click", ".cardCopy", function(e){
            e.preventDefault();
            var form = $(this).parent().prev().find(".modalFormCard")
            var name = form.find("#id_name").val();
            var description = form.find("#id_description").val();
            var cardId = form.data('id');
            var listID = form.data('listid');
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
                    $("body").load(window.location.href);
                    console.log("skopiowano karte");
                }
            })

        })



});





