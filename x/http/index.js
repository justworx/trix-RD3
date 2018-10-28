
// *** UNDER CONSTRUCTION ***

// GLOBALS
gMainStatus = {}
gMainAccount = {}
gMainTabs = []


$(function() {
	
	// old-fashioned (original) command method - this may change
	oldfashionedcommand();
	
	// new mode of operation (under construction)
	startmainloop();
});


function startmainloop() {
	gLoopCt = 0;
	setInterval(mainloop, 1000);
	$('#NavMid').css('color','#eee')
}


function mainloop() {
	$('#NavMid').text(gLoopCt)
	gLoopCt++;
	
	main_account()
	main_status()
	main_tabs()
}

// check root status - update status indicators
function main_status()
{}

// check login, update account pane if necessary
function main_account()
{}

// query for service tab updates
function main_tabs()
{}




// COMMAND HANDLER - This may change.
function oldfashionedcommand() {
	gDisplay = $('#Content');
	$('#Command').submit(function(e) {
		
		// never submit this form
		e.preventDefault();
		
		// get the entered command and clear the text box
		cmd = $('#cmd').val();
		if ($.trim(cmd) == '') {
			gDisplay.append("<br/>");
		}
		else {
			try {
				$('#cmd').val("").focus();
				
				// create a div to show the command and its response
				tm = new Date().getTime();
				id = "c_"+tm;
				dc = "<div class='cmd'>"+cmd+"</div>";
				dr = "<pre class='resp'><i>...</i></pre>"
				dd = "<div id='"+id+"'>"+dc+dr+"</div>";
				
				// add the new entry to display and scroll-top
				gDisplay.append(dd);
				
				// send command to server and insert response
				resp = $("#"+id).find('.resp');
				requestURL='/?c='+cmd; //+'&id='+id
				$.ajax({url:'/', data:{c:cmd}, context:resp})
					.done(function(c,r) {this.text(r+': '+c);})
					.fail(function(a,r,m) {this.text(r+': '+m);})
					.always(function() {
					$("html, body").animate({
						scrollTop: $(document).height()},599);
					})
				;
			}
			finally {
			}
		}
		
		$("html, body").animate({scrollTop: $(document).height()},599);
			
		// handled via javascript
		return false
	});
}
