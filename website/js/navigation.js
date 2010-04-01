// vim: set ts=4 sw=4 noet ai:
var currentPost = 0;

$(function($) {

	$("#help-trigger").click(function() {
		$("#help").toggle();
		return false;
	});

	$("#help").click(function() {
		$(this).toggle();
	});

	$('.item').each(function(i) {
		$(this).prepend('<a id="post-item-'+(i+1)+'" name="post-item-'+(i+1)+'"></a>');
	});

    document.onkeydown = function(e) {
        e = e || window.event;
		if (e.target) {
			element = e.target;
		} else if (e.srcElement) {
			element = e.srcElement;
		}

		if (element.nodeType == 3) {
			element = element.parentNode;
		}

		if (e.ctrlKey == true || e.altKey == true || e.metaKey == true) {
			return;
		}

		var keyCode = (e.keyCode) ? e.keyCode : e.which;

		if (keyCode && (element.tagName == 'INPUT' || element.tagName == 'TEXTAREA')) {
			// don't mess around when in input or textarea
			return;
		}

		switch(keyCode) {
			//  "j" key
			case 74:
				if (currentPost > 0) {
					nextPostId = '#post-item-' + (currentPost + 1)
				} else {
					nextPostId = '#post-item-1';
				}
				if ($(nextPostId).length == 0) {
					// no next post on this page
					return;
				}

				$.scrollTo(nextPostId, 0);
				currentPost++;
				break;
                            
			// "k" key
			case 75:
				if (currentPost > 1) {
					nextPostId = '#post-item-' + (currentPost - 1);
				} else {
					// no previous post, we're on the first already
					return;
				}

				$.scrollTo(nextPostId, 0);
				currentPost--;
				break;

			// "t" key
			case 84:
				$.scrollTo('#header', 0);
				currentPost = 0;
				break;

			// "esc" key
			case 27:
				if ($("#help:visible").length > 0) {
					$('#help').toggle();
				}
				break;
		}
	}
});

