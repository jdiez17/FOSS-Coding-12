# euskalMap v.0.1 CLI documentation

euskalMap CLI is the reference implementation for the euskalMap API.

## Commands

* ```help``` - Prints the available commands.
* ```show [mode [filter]]``` - Fetches information from the API. (See Appendix. 1 for available filters)
	* ```show messages [location [filter]]```
		* ```show messages AK-91``` - Shows all the messages in location AK-91
		* ```show messages AK-91 timestamp``` - Messages in location AK-91 with a timestamp
	* ```show messages near location [radius=1]``` - Shows the messages whose location is contained in a square with radius ```radius```. See API documentation for more information.

	* ```show abuse``` - shows abuse reports.
* ```send [message [location]]``` - Sends a message whose location can be specified by the optional parameter ```location```.
	* ```send "I am writing the documentation for euskalMap" AK-91```

* ```map``` - Prints a map of the party site, with the count of messages per location.

* ```report id [reason]``` - Generates abuse notice for message id ```id```, with the optional reason ```reason```.
	* ```report 1337 "I find this message very offensive."```

* ```quit``` - Quits the client.

## Example session

	$ python client.py
	euskalMap CLI consumer - v.0.1
	
	eM $ show messages
	eM $ send "I am writing the euskalMap documentation" AA-02
	Sent OK!
	eM $ show messages
	 * [#37] 'I am writing the euskalMap documentation' on AA-2
	eM $ show messages AA-02
	 * [#37] 'I am writing the euskalMap documentation' on AA-2
	eM $ show messages AA-02 timestamp
	eM $ map
	AA-1 (0) AA-2 (1)   AA-3 (0) AA-4 (0)   AA-5 (0) AA-6 (0)   AA-7 (0) AA-8 (0)   AA-9 (0) AA-10 (0)
	AB-1 (0) AB-2 (0)   AB-3 (0) AB-4 (0)   AB-5 (0) AB-6 (0)   AB-7 (0) AB-8 (0)   AB-9 (0) AB-10 (0)
	
	BA-1 (0) BA-2 (0)   BA-3 (0) BA-4 (0)   BA-5 (0) BA-6 (0)   BA-7 (0) BA-8 (0)   BA-9 (0) BA-10 (0)
	BB-1 (0) BB-2 (0)   BB-3 (0) BB-4 (0)   BB-5 (0) BB-6 (0)   BB-7 (0) BB-8 (0)   BB-9 (0) BB-10 (0)
	eM $ show messages near AB-02
	 * [#37] 'I am writing the euskalMap documentation' on AA-2
	eM $ report 37 "I find this message very offensive."
	Abuse report received.
	eM $ quit
