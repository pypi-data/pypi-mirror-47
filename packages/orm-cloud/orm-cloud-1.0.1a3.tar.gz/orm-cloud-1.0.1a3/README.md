# ORM.Cloud
ORM.Cloud takes an opinionated approach to implementing REST APIs using serverless cloud services such as AWS API Gateway and Lambda to front SQL data stores using Python. It defines a standardized way to map common query string parameters, such as sort_by, limit, and offset to provide sorting and pagination out of the box. It supports Lucene-style filter expressions to get only the data you're interested in. Using ORM.Cloud and a few lines of code, you can have a full featured REST API implementation for all CRUD operations on your entity. 

# Features
## Sorting and Pagination
ORM.Cloud implements sorting and pagination via standardized query string parameters. 

### Sorting
ORM.Cloud supports sorting by multiple fields in both ascending and descending order with the **sort_by** query string parameter. To sort ascending, prefix the field name with '+'; to sort descending, prefix the field name with '-'. To sort by multiple fields, separate them with a comma.

    # Sort by 'thing_id' ascending
    GET /things?sort_by=+thing_id

    # Sort by color descending, then thing_id ascending
    GET /things?sort_by=-color,+thing_id
    
### Pagination
Fetching entire result sets from a database is wasteful. ORM.Cloud has built in support for fetching paged result sets using the **limit** and **offset** query string parameters.

    # Get the first 20 results
    GET /things?limit=20

    # Get the second set of 20 results
    GET /things?limit=20,offset=20

## Filtering
Filtering is handled by the **filter** query string parameter. It takes in a Lucene formatted filter expression to generate the SQL WHERE clause. 

    # Filter results where color = 'orange'
    GET /things/?filter='color: "orange"'

    # Filter results where color = 'red' and age = 1
    GET /things?filter='color: "red" and age: 1'

# Examples
The examples below utilize the **Thing** class:

    @entity('table_name'='things')
    class Thing(Entity)
        @property
        @field(key=True, column_name='thing_id')
        def thing_id(self)
            return self._thing_id
        
        @property
        @field(column_name='color')
        def color(self)
            return self._color
        
        @property
        @field(column_name='size')
        def size(self)
            return self._size

## Get a Thing

> GET /things/123

      {
          "statusCode": 200,
          "headers": {},
          "body": {
            "thing_id": 1,
            "color": "red",
            "size": "large"
          }
      }

## Search for Things
> GET /things?filter=color: 'orange'&limit=20&offset=0&sort_by=+thing_id

    {
      "statusCode": 200,
      "headers": {},
      "body": [
        {
        "thing_id": 1,
        "color": "red",
        "size": "large"
        },
        {
        "thing_id": 2,
        "color": "blue",
        "size": "medium"
        },
        {
        "thing_id": 3,
        "color": "yellow",
        "size": "small"
        }
      ]
    }
        
## Search for 'blue' Things
> GET /things?filter=color: 'blue'

    {
          "statusCode": 200,
          "headers": {},
          "body": [
          {
            "thing_id": 2,
            "color": "blue",
            "size": "medium"
            }
          ]
        }

 
