# TeamsWebhook
Send a teams message to a channel automatically, (found the solution to add pictures)

Initially I struggled to send a proper teams message to a channel automatically, but after an exhaustive investigation and endless tries I did this code.
The TeamsSenderMain will trigger the webhook by a specified action (when the software finds a new folder in certain path)
Then I did a basic webserver to load the picture I want to share in the teams message and I share this link to the Teams_Sender where all the format of the webhook is structured.
Make sure to configure properly the webhook in Power Automate before using the code and of course add your own webhook url into the parameters.json file

