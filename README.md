# Proposal

## What will (likely) be the title of your project?

Superior Sports Stats

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

A website which has a variety of sports analytics pages including win percentages for sports team using GLICKO instead of ELO and fantasy player projections.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

Our project will be a python based website which will generate various win percentage in sporting games.  The software will look through the past performances of the sports team based on whether they won or lost and the caliber of opponent.  From those performances, the software will generate a rating system based on the GLICKO model.  The website will then use the ratings to generate win probabilities in future games.  For this project, we will use SQL to store the teams’ performances and update based on new results.  A separate SQL database will contain the future matchups and the projected win percentages.  All this information could be obtain by an API which ESPN kindly provides: http://www.espn.com/static/apis/devcenter/docs/scores.html.
In terms of features, the webpage will have three main pages: one which shows the win probabilities of all the upcoming games, another which enables users to search for a team and see that team’s projections and rating, and a final page which lets users see rankings for each league.
If time permits, we may transition into analyzing projections for individual players in every game instead of focusing just on teams.  This would be implemented similarly to the above, but of course, we would use a different model.


## If planning to combine CS50's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to CS50, and which aspect(s) would relate to the other course?

N/A

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

A webpage with the GLICKO win percentage of every college basketball team's next game.

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

A webpage with the GLICKO win percentage of every college and professional basketball team's remaining games.

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

A webpage with the GLICKO win percentage of every game in major sport (MLB, NBA, NFL, NHL, NCAAM, NCAAF) and also have additional pages which model the projected proformance of individual players.

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

I think we know pretty much all that we need to for this project.  In terms of CS, we should probably learn a little more about API so that we can properly store all the necessary data into SQL databases.  Also, we should do a little more research about how precisely the GLICKO model creates rankings in niche circumstances such as after major injuries or major trades.  Our next step should just be to create a more detailed outline of how exactly we want to update our databases in the most efficient manner.  In terms of splitting up work, William will work on loading past results into the database and updating ratings, and Reid will work on creating a database with win probabilities which updates with the new ratings.

