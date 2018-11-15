# False Alarm

## Questions

2.1. The problem with the design is that all the options look identical expect for the word DRILL, making the possibility of a misclick much higher.  The UI should have made the buttons with real warnings a different color to ensure a user wouldn't accidentally click the button.

2.2. The UI is at fault here.  Because the buttons look so similar, it is hardly suprising that a user made a careless mistake.  The programmers should have anticipated such error and made it impossible for a human to accidently click the non-drill button.

2.3a. In terms of HTML, I would use two seperate dropdown menus, one for drills and one for emergencies, which would have prvented this problem.

2.3b. For CSS, I would have made styles for the different buttons which would reflect the danger of clicking the emergency buttons by making them red and bold.

2.3c. For JavaScript, I would check if the user clicked an emergency button.  If they did, I would send a popup alert to their page to confirm that they had indeed selected the correct button.

2.4. An SQL database could be useful to create a database of different users with different levels of authority.  The SQL could then be useful to ensure that low level users could not click the emergency buttons and that only senior level employees would have the ability to send emergency alerts.

2.5. Using my proposal, a human could still err by first logging into a high level account, then going to the emergency drop down menu instead of the drill menu, clicking on the red button which said PACOM, and then ignoring the popup alert or disabling JSS which asks them to confirm it is not a drill.

## Debrief

a. None were necessary

b. 15 minutes
