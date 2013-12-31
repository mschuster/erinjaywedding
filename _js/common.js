function showMenu () {

	var selected = $("nav li.selected");

	if(selected.length === 0) {
		return false;
	}

	selected.removeClass("selected");
	$("nav").addClass("drop-menu");

	setTimeout(function() {
		$("body").click(function() {
			$("nav").removeClass("drop-menu");
			selected.addClass("selected");
			$("body").unbind("click");
		});
	}, 500);

}