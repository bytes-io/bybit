JSON Parsing would be necessary:

Now if you think about that a bit, you’ll come to realize a fundamental truth of sockets: messages must either be fixed length (yuck), or be delimited (shrug), or indicate how long they are (much better), or end by shutting down the connection. The choice is entirely yours, (but some ways are righter than others).
The easiest enhancement is to make the first character of the message an indicator of message type, and have the type determine the length. Indicating msg type could also ease parsing.
Prefixing the message with its length (say, as 5 numeric characters) gets more complex, because (believe it or not), you may not get all 5 characters in one recv.
Cela veut dire que notre serveur ne pourra dialoguer qu'avec 5 clients maximum ?
Non. Cela veut dire que si 4 clients se connectent et que le serveur n'accepte aucune de ces connexions, aucun autre client ne pourra se connecter. Mais généralement, très peu de temps après que le client ait demandé la connexion, le serveur l'accepte. Vous pouvez donc avoir bien plus de clients connectés, ne vous en faites pas.
