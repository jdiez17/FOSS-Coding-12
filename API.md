# euskalMap API

## Messages

* ```/<format>/messages``` - GET - Returns all the messages, without any filter.
* ```/<format>/messages/<filter>``` - GET - Filters the stream of messages applying the ```filter``` filter. For more information on filters, please see Appendix. 1
* ```/<format>/messages/<letters>-<int:numbers>/``` - GET - Messages whose location is ```letters```-```numbers```.
* ```/<format>/messages/<letters>-<int:numbers>/<filter>``` - GET - Messages filtered by ```filter``` whose location is ```location```
* ```/<format>/messages/bulk``` - POST - ```{'locations': JSON}``` - Returns message whose location is contained in the JSON-encoded list.
* ```/<format>/send``` - POST - ```{'message': message, ['location_letters': letters, ['location_numbers': numbers', ['timestamp': timestamp]]]) - Submits a new message with the specified params.
* ```/<format>/messages/near/<letters>-<int:numbers>``` - GET - Returns messages *near* the location ```letters```-```numbers```. For more information on how this is calculated, see Appendix. 2
* ```/<format>/messages/near/<letters>-<int:numbers>/<int:radius>``` - GET - Returns messages near the location within the specified radius.

## Reports

* ```/<format>/reports/post``` - POST ```{'id': id, ['message': message]}``` - Posts a report abuse regarding message identified by ```id``` with an optional comment.
* ```/<format>/reports/get``` - GET - Gets the abuse reports. 

## Comments
* ```/<format>/comments/post``` - POST ```{'id': id, 'message': message}``` - Posts a comment on message identified by ```id```
* ```/<format>/comments/get/<id>``` - GET - Gets the comments for a given message

# Appendix 1

Available filters:

* ```has_timestamp``` - Returns only messages with a timestamp.
* ```has_location``` - Returns only messages with a location.
* ```trending``` - Order by trendingness.
* ```random``` - Add controlled amounts of entropy to your life.

# Appendix 2

The *near* feature returns messages whose location is contained within a square with a specified radius. 
This works by checking if the possible adjacent locations are within bounds, assigning them letters and numbers which are then fed into the Message filter.

The *near* functionality uses a recursive algorithm and a stack to keep track of the candidate locations.

Consider a map with 2 rows, 1 block per row, 2 rows per block and 2 columns per block, like the following:

	AA1		AA2		AA3
	AB1		AB2		AB3
			
	BA1		BA2		BA3
	BB1		BB2		BB3
	
In this example, the location ```AB2``` is "near" AA1, AA2, AA3, AB1, AB3, BA1, BA2 and BA3.
