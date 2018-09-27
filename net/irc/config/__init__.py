#
# DEFAULT PLUGIN CONFIG
#  - Defines the default configuration for plugins. It will be
#    coppied to the config of new bots, where it may be edited
#    to suit the user's tastes.
#  - This is ONLY a template, and is never called in code, but is
#    loaded as default when creating a new bot config file.
#  - This file will be updated when new plugins are added to the
#    irc package, or when changes are made to existing plugins.
#  - Every connection gets its own unique copy of the plugin config 
#    dict so as to allow for fine-tuning by connection.
#

DEF_PLUGIN_CONFIG = {

	# actions to perform automatically on various
	"action" : {
		# the trix.create path to the plugin class
		"plugin"  : "trix.net.irc.plugin.action.IRCAction",
		
		# what to do wehn a connection to an irc server is made.
		# for example: ["JOIN #MyChannel", "NOTICE MyFriend :Hi!"]
		"on_connect" : []
	},
	
	# manage (load, unload, reload) plugins
	"plugin" : {
		"plugin"  : "trix.net.irc.plugin.plugins.Plugins"
	},
	
	# announce titles of videos and web pages when urls are posted
	"announce" : {
		"plugin"  : "trix.net.irc.plugin.announce.Announce",
		"tags" : ["title"]
	},
	
	# server connection information, chanel census 
	"info" : {
		"plugin"  : "trix.net.irc.plugin.info.IRCInfo"
	},
	
	# a very simple log-file feature. (needs improvement!)
	"irclog" : {
		"plugin"  : "trix.net.irc.plugin.irclog.IRCLog",
		"logpath" : "~/.cache/trix/irclog/undernet.log",
		"logendl" : "\n",
		"logtime" : 45
	},
	
	# commands for the bot to execute. Eg, join, part, nick, etc...
	"command" : {
		"plugin": "trix.net.irc.plugin.command.IRCCommand"
	},
	
	# dictionary lookup
	"dict" : {
		"plugin": "trix.net.irc.plugin.dict.IRCDict"
	}
}



#
# CONNECTION TEMPLATE
#  - A dict with 'desc' and 'keys', suitable for passing as config 
#    to `trix.util.xinput.Form()` when entering new bot connections.
#
CONNECTION_TEMPLATE = {

	# DESCRIPTION
	"desc" : {
		
		# Connection id - eg, "undernet" or "undernet2" or "whatever"...
		# This will be the key in the config['connections'] dict.
		"connid"   : "The name of this connection - it must be unique!",
		
		# connection params
		"network" : "Network name   (Eg,'undernet')",
		"host"    : "Server address (Eg, 'eu.undernet.org')",
		"port"    : "Port number    (Eg, 6667)",
		"user"    : "Username for this IRC server",
		"nick"    : "Your bot's nick (Eg, '^^MyBot^^')",
		"realname": "Any sort of text (except your real name).",
		"encoding": "Text encoding expected by `host` server. (Eg, UTF_8)",
		"errors"  : "Encoding error handler. (Eg, strict, replace, etc.)",
		
		# admin params
		"enabled" : "Start bot automatically on creation? ['yes' or 'no']",
		"owner"   : "List of host masks to treat as bot owner.",
		
		# plugin params
		"pi_list" : "Space-separated string of plugins (keys) to load",
		"pi_update" : "Interval (seconds) between plugin updates."
	},
	
	# KEYS (IN ORDER)
	"keys" : [
		"connid", "network", "host", "port", "user", "nick", "realname", 
		"encoding", "errors", "enabled", "owner", "pi_list", "pi_update"
	]

}

