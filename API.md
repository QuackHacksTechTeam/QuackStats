

# API Documentation

## Endpoint: Get User Commits

### URL
`/api/user-commits`

### Method
`GET`

### Description
Retrieves all user commit history in JSON format.

### Response Format
```json
[
    {
        "username": "string",
        "commits": int
    },
    ...
]
```

### Example Response
```json
[
    {
        "username": "johndoe",
        "commits": 42
    },
    {
        "username": "janedoe",
        "commits": 35
    }
]
```

