# fampay_video_app
Youtube video App linked with youtube api, made for fampay interview first round.. please do not copy if you are giving interview for fampay and if you do please make sure at least change the readme file..

BASIC REQUIREMENTS - 
1. Call youtube API every 10 sec with a hard coded query - [x]

2. Create a API to return a paginated response of all stored videos - [x]
    -> 'https://fampayapp.herokuapp.com/view'
3. Create a API able to search the videos in local db based on title and description - [x]
    -> 'https://fampayapp.herokuapp.com/search/<INSERT QUERY HERE>/'

4. Dockerise the application - [x]
    -> 'https://docker_url.com/

5. Make the project Scalable and optimised - [x]
    -> search queries are optimised to do the searching in a single request.
    -> easy to scale the application by increasing the constant for resultThreshold in the code.

BONUS POINTS -
1. Added support for adding multiple api keys in dashboard - [x]
2. Created dashboard with proper css, having sorting and searching functionality - [x]
3. Search API optimised for partial matches - [x]

ASSUMPTIONS - 
1. Query parameter was assumed  to be -> 'cricket'
2. Threshold date was hardcoded as query parameter to be  -> '2020-01-01T18:42:16Z'
3. total results were restricted to 1000

ISSUES - 
1. Server Side rendering was not done dashboard, due to which it will take a lot of time to render if max_results exceeds 10,000
