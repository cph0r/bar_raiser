# fampay_video_app
Youtube video App linked with youtube api, made for fampay interview first round.. please do not copy if you are giving interview for fampay and if you do please make sure at least change the readme file..

I have created to dashboard for viewing of all the availale videos in local db also I have added the functionality to add new api keys from the dashboard.

I hope the project was upto the expectations of the reviewer , Let me know if there is anything else that I can add..

I did all the basic requirements along with bonus points, the deployed  app on heroku has the update disabled to save requests in quota.

HEROKU LINK -> https://fampayapp.herokuapp.com/

BASIC REQUIREMENTS - 
1. Call youtube API every 10 sec with a hard coded query - [x]

2. Create a API to return a paginated response of all stored videos - [x]
    -> 'https://fampayapp.herokuapp.com/view'
3. Create a API able to search the videos in local db based on title and description - [x]
    -> 'https://fampayapp.herokuapp.com/search?search=INSERT SEARCH QUERY HERE'

4. Dockerise the application - [x]
    -> 'docker pull ph0rgasm/fampay-app:latest'

5. Make the project Scalable and optimised - [x]
    -> search queries are optimised to do the searching in a single request.
    -> easy to scale the application by increasing the constant for resultThreshold in the code.
    -> Elastic search was used to optimise the projects search api using sharding.
    -> Redis was used to do caching in view api.

BONUS POINTS -
1. Added support for adding multiple api keys in dashboard - [x]
2. Created dashboard with proper css, having sorting and searching functionality - [x]
3. Search API optimised for partial matches - [x]

ASSUMPTIONS - 
1. Query parameter was assumed  to be -> 'cricket'
2. Threshold date was hardcoded as query parameter to be  -> '2020-01-01T18:42:16Z'
3. total results were restricted to 100 to prevent quota exhaustion

ISSUES - 
1. Server Side rendering was not done dashboard, due to which it will take a lot of time to render if max_results exceeds 10,000
2. Null checks and string format checks are not performed for api Keys creation from the frontend
3. Redis Caching was used so consistency was compromised for availability
