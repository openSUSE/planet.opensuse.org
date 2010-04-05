// vim: set ts=4 sw=4 noet ai:
var currentPost = 0;
var currentDay = 0;

$(function($) {

	$("#help-trigger").click(function() {
		$("#help").toggle();
		return false;
	});

	$("#help").click(function() {
		$(this).toggle();
	});

	$('.item').each(function(i) {
		$(this).prepend('<a id="post-item-'+(i+1)+'" class="post-item-anchor" name="post-item-'+(i+1)+'"></a>');
	});

	$('.day').each(function(i) {
		$(this).prepend('<a id="day-item-'+(i+1)+'" class="day-item-anchor" name="day-item-'+(i+1)+'"></a>');
	});

    document.onkeydown = function(_e) {
		var element = null;
        var e = _e || window.event;
		if (e.target) {
			element = e.target;
		} else if (e.srcElement) {
			element = e.srcElement;
		}

		if (element.nodeType == 3) {
			element = element.parentNode;
		}

		if (e.ctrlKey == true || e.metaKey == true) {
			return;
		}

		var keyCode = (e.keyCode) ? e.keyCode : e.which;

		if (keyCode && (element.tagName == 'INPUT' || element.tagName == 'TEXTAREA' && element.tagName == 'SELECT')) {
			// don't mess around when in input or textarea
			return;
		}

		switch(keyCode) {
			//  "j" key
			case 74:
				var nextPostId = null;
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
				var nextPostId = null;
				if (currentPost > 1) {
					nextPostId = '#post-item-' + (currentPost - 1);
				} else {
					// no previous post, we're on the first already
					return;
				}

				$.scrollTo(nextPostId, 0);
				currentPost--;
				break;

			// "d" key
			case 68:
				var nextDayId = null;
				if (currentDay > 0) {
					nextDayId = '#day-item-' + (currentDay + 1)
				} else {
					nextDayId = '#day-item-1';
				}
				if ($(nextDayId).length == 0) {
					// no next post on this page
					return;
				}

				$.scrollTo(nextDayId, 0);
				currentDay++;
				break;

			// "u" key
			case 85:
				var nextDayId = null;
				if (currentDay > 1) {
					nextDayId = '#day-item-' + (currentDay - 1);
				} else {
					// no previous day, we're on the first already
					return;
				}

				$.scrollTo(nextDayId, 0);
				currentDay--;
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

