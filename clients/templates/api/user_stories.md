# EXPRESS

we all know what is express. 
it is nothing but a component that can communicate with porters(bikers) and operators
to just create new trips to assign orders to porters.
solving this unroutine problem bering a few common problems such as:

1. graph maximum matching, tsp
2. routing and traffic forcasting
3. cost per trip calculation
4. restaurant delay prediction
5. data analysis

and solving these problems needs a tool compatible with numerical analysis and graph traversal algorithm and speed
the best tool is python by farr.

[comment]: <> (a reference style link.)

#### to achieve these we need some components:

1. a robust agile server to handle vast amount of requests
    * sanic is a trend fast micro framework that handle requests asyncrounus.
    * it is compatible with motor (async library to communicate with mongodb)
    * it can support all loginext functionality in future.
2. mongodb to save users data i use mongodb for:
    * it is document oriented it reduces maintenance time cost.
    * is more agile for it's schema less.
    * join between collections are few.
    * express is not a critical and it's db does not contain important contents so does'nt matter if mongodb is'nt supportive for acid.
3. temporary sub space that live in memory to speed up intercommunication
    * it acts like a cache (has lru) to hold trend data
    * for now we only keep porters hot orders(un assigned) and G (graph) and auto dispatched trips.
4. a state of art function using kn-tree to predict density of orders in a given coordination. (MU)
5. configured osrm for routing problem.
    * i used [AccuWeather](http://accuweather.com) to get current weather data of tehran and current time to configure car.lua traffic weights of highway types
    * i uses two osrm local server for robustness and switch between them every one hour for every new data
    * i created amortized feature to predict the expected distance and duration for every porter to arrive to new order.
    * it used number 5 (MU)
6. a little lstm using keras with tensorflow backend to predict:
    * traffics in future ensha allah.
    * restaurant delay for every orders. (for a better dispatching. it is good to know how much time can we think to assign the best porter to it)
7. gcm notifier  

# USER STORIES
let me summarize all some points on each stack holder (every stack holder type is a User type):

1. Applicator: # this user is a customer who needs a delivery or pickup or both.
    * /orders/ :POST ): create a new order.
    * /orders/<id>/@delay:<delay> ): set a new delay number for this order.
2. Porter: # this user has a vehicle and moves for our sake
    * /locations/ :POST ): sends his location.
    * /trips/<_id>/@ack:<response> ): accept or reject this trip.
    * /orders/<_id>/@status:<status> ): set status for this order.
3. Operator:
    * ...
4. Company: (ZoodFood | SnappBox)
5. Dev
6. Admin

## now let me explain the most important part.

1. an applicator creates an order using [new Order](/clients/API/#) (and probably set delay (it is optional))
2. simultaneously:
    * probably some porters logged in. [update $me@status: available](/clients/API/#user-status) and are waiting for new orders.
    * they also send their current locations [send-location](/clients/API/#send-location) for every 1 sec so we know where they are now.
3. a cron job every time that gets free run itself get available users and hot orders and make a matching (new Trips) between them.
4. then we (the cron job) send notification with trip data to it's porter. and wait for their ack
[/trips/<_id>/@ack:<response>](/clients/API/#ack) 
5. if they reject they will get a penalty about the difference of the best porter and second best porter and we start to renotify the second and again wait for him to reply and so on.
6. but if they accept they will probably start to follow the order.
7. a cron job has mission to observe their movement. if they don't follow their trip it call's the endpoint [need-call](http:///users/need-call) for them
    * be attention that porters also can call this endpoint if they got problem 
##DONE 
##END