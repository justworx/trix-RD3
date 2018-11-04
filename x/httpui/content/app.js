/*
Copyright 2014-2018 justworx
This file is part of the trix project, distributed under
the terms of the GNU Affero General Public License.
*/


$(function() {
	app = new App();
	app.start();
})


//
//
// APP
//
//
var App = function(f) {
	this.__freq = f ? f : 2000;
	this.init();
}


//
// INIT
//  - Call this at the creation of the app and
//    any time the app becomes disconnected.
//
App.prototype.init = function() {
	this.__username = '';
	this.__running = false;
	this.__update = null;  // interval object
	this.__state = null;  // object from server
}


//
// START
//  - Hit update every 'freq' milliseconds
//
App.prototype.start = function() {
	
	// get state; update; load panels; start.
	this.getstate().done(function() {
		this.getupdate().done(function() {
			this.getpanel('Home').done(function() {
				this.firstpage();
				
				/*
				// add more default panels here
				this.getpanel('Service').done(function() {
					this.getpanel('Command').done(function() {
						this.getpanel('Data')	
					});
				});
				*/
				
				// Create/start the update interval object
				if (!this.__update) {
					var update = this.update.bind(this);
					this.__update = setInterval(update, this.__freq);
				}	
			})
		})
	});
}

App.prototype.firstpage = function() {
	this.show('#Home');
}


//
// UPDATE
//
App.prototype.update = function(force) {
	if (!this.__state || force)
		this.getstate().done(function() {
			this.getupdate();
			this.xclass()
		});
	else
		this.getupdate();
}


// REQUEST
App.prototype.request = function (req) {
	return $.ajax({url:'/', data:req, context:this})
		.fail(function(x, stat, err) {
			this.on_fail(x, stat, err)
		})
		.done(function(data, stat) {
			this.on_done(data, stat)
		});
}


// COMMAND
App.prototype.command = function (cmd) {
	
	// make sure `cmd` is a string
	if (typeof cmd == 'object')
		cmd = cmd.join(' ')
	
	// send the command as a request to the server
	return this.request({c:cmd})
	
		// handle the response
		.done(function(data) {
			
			// check whether the  response is an error message
			e = app.on_error(data);
			if (e) {
				e = (typeof e == 'object') ? e.join(' ') : e;
				this.notify(e);
			}
			else if (data.Command == 'auth whoami')
				
				// try to keep loss of session up to date
				if (data.Result == null)
					this.setuser(null);
			
			else if (!data.Private)
				this.notify(data.Command, data.Message, data.Result);
			else if (data.Message)
				this.notify(data.Message);
		});
}


// GET state
App.prototype.getstate = function () {
	return this.request({u:'state'})
		.done(function(data, stat) {
			this.__state = data;
			this.on_state(data);
		});
}

// GET UPDATE
App.prototype.getupdate = function () {
	return this.request({u:'update'})
	.done(function(data, stat) {
		this.on_update(data, stat);
	});
}

// GET PANEL
App.prototype.getpanel = function (panelName) {
	var p = panelName;
	return $.ajax({url:'/panels/'+p+'.html', context:this})
		.fail(function(x, stat, err) {
			this.notify('Loading Panel:', p, err);
		})
		.done(function(data, stat) {
			x = $(data);
			x.hide();
			$('#Content').append(x);
			this.on_panel(x);
		})
}


// NOTIFY
// - Sets middle status section text; fades in 9 seconds.
App.prototype.notify = function (msg, prompt, detail) {
	prompt = prompt ? (prompt + ': ') : '';
	detail = detail ? ('; ' + detail) : '';
	sn = $('#status_notice').empty();
	sn.append('<span/>')
	mspan = sn.children().eq(0);
	mspan.text(prompt + msg + detail)
		.delay(9000)
		.fadeOut({
			duration: 3000,
			complete: function() {$(this).remove();}
		});
}




// --- CALLBACKS ---

App.prototype.on_error = function (data) {
	if (data.Error) {
		try {
			err = data.Error[0]
		}
		catch (e) {
			err = data.Error
		}
		if (err == 'invalid-session') {
			// try to keep loss of session up to date
			this.setuser(null);
			this.xclass();
			document.cookie="name=auth;expires=Thu, 01 Jan 1970 00:00:01 GMT";
		}
		
		// return whatever the error code was
		return err
	}
}

App.prototype.on_done = function  (data, stat) {
	if (!this.__running) {
		this.firstpage();
		$('#status_connection').text('Online');
		this.__running = true;
	}
	
	if (this.on_error(data))
		;
	
	// Either way, if something got done, the account 
	// div should be visible. It's only hidden when
	// we're offline.
	$('#status_account').show();
}

App.prototype.on_fail = function  (x, stat, err) {
	if (this.__running) {
		if (!x.readyState) {
			this.show('#Offline')
			$('#status_connection').text('Offline');
			$("#status_version").text('');
			$('#status_account').hide()
			this.init();
			this.setuser(null);
		}
	}
	//$("#status_notice").text(stat+': '+err+'; '+);
	this.notify(err, stat, JSON.stringify(x));
}

App.prototype.on_panel = function($panel) {
	var APP = app;
	var pid = $panel.attr('id')
	$a = $("<a class='click'></a>")
	$a.text(pid).attr('id','Tabs_'+pid)
	$('#Tabs').append($a)
	$('#Tabs a').on('click', function(e) {
		e.preventDefault();
		var id = $(this).text();
		var ID = '#'+id
		APP.show(ID);
		return false;
	});
	
	// execute class-designated commands
	this.xclass();
}

// ON STATE - called only when running *becomes* true
App.prototype.on_state = function (data) {
	s = this.__state;
	$("#status_version").text(s.server+' '+s.revision)
		.attr('title', s.service);
}


//
// ON UPDATE
//  - called each successful app.update()
//
App.prototype.on_update = function (data, stat) {

	// Calculations based on the difference between
	// the current state (this.__state) and new state
	// (data) are done first.
	if (this.__state && (this.__state.session != data.session)) {
		this.setuser(null);
	}
	
	//
	// WHEN DONE EXAMINING the difference between 
	// the prior and current state, update values
	// in state that have changed with this update.
	//
	// DO NOT REPLACE! Update doesn't send all the
	// same variables. Update the values in state
	// with ONLY the values data actually contains.
	//
	for (var x in data) {
		this.__state[x] = data[x];
	}
	
	// If there's a session but no username, query 
	// for the new username
	if (this.__state && this.__state.session && !this.__username) {
		this.command('auth whoami')
		.done(function(data) {
			if ((!data) || (this.on_error(data) == 'invalid-session')) {
				this.init()
				this.setuser(null)
				this.xclass();
				document.cookie="name=auth;expires=Thu, 01 Jan 1970 00:00:01 GMT";
			}
			else
				this.setuser(data.Result);
		});
	}
}


// --- Utility ---

App.prototype.setuser = function (username) {
	this.__username = username ? username : '';
	if (!username)
		if (this.__state)
			this.__state.session = null;
	this.xclass();
}


App.prototype.show = function(selector) {
	// hide everything inside conent
	$('#Content').children().hide();
	
	// show all parents of the div selected
	// (which will usually be a panel, but 
	// not always)
	$(selector).parents().show();
	
	// show the selected object itself
	$(selector).show();
	
	// set focus in the first item within
	// selector that has class x_focus
	$(selector).find('.x_focus').eq(0).focus()
}


App.prototype.xclass = function() {
	
	if (!this.__running)
		return
	
	// session
	if (!(this.__state && this.__state.session)) {
		$('.x_noses,.x_noses_show').show();
		$('.x_onses,.x_noses_hide').hide();
	}
	else {
		$('.x_onses,.x_onses_show').show();
		$('.x_noses,.x_onses_hide').hide();
	}
	
	// auth
	if (!(this.__state && this.__state.hasauth)) {
		$('.x_noauth,.x_noauth_show').show();
		$('.x_onauth,.x_noauth_hide').hide();
	}
	else {
		$('.x_onauth,.x_onauth_show').show();
		$('.x_noauth,.x_onauth_hide').hide();
	}
	
	// username
	$('.x_username').text(this.__username)
}
