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


});





