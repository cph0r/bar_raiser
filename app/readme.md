The following assignment was created for barraiser interview, Please do not copy paste and if you do please make sure to change the readme file.

Assumptions:
1. one deal only has one product
2. date format = yyyy-mm-dd

Validations:
1. complete data check
2. offer time check( start time > end time)
3. date format check
4. Deal duplicity check ( not 2 deals can have same product)

Payloads:
1. Deal Creation Payload:
{
    "product_id":2,
    "start":"2021-09-10 23:30:00",
    "end":"2021-09-09 23:30:00",
    "max":2
}

2. Deal Deletion Payload:

{
    "deal_id":2,
}


3. Deal claim Payload:
{
    "user_id":2,
    "deal_id":1,
}

4. Deal Update Payload:
{
    "deal_id":1
    "product_id":3,
    "start":"2021-09-10 23:30:00",
    "end":"2021-09-09 23:30:00",
    "max":2
}