# User Event Tracker

This user event tracker is a simple Flask REST API that uses Flask-SQLAlchemy and psycopg2-binary to connect to a PostgreSQL database.  Both the application and the database are running in Docker containers.

This app does not include a login system; one is mocked by manually setting a valid `USER_EID` value in `app/config.py`.  It also uses Flask's builtin server, rather than one suitable for a production deployment.

Each event and user have an external id (eid).  This eid is a UUID generated on save.

The search endpoint makes the assumption that if both title and description search values are provided, both should match, and that if neither are provided, the request is bad.

There is a deactivation endpoint _and_ a deletion endpoint.  Events that are not marked active do not show up in search results and are not returned by a direct request; to an end user, they would be functionally deleted.  The deletion endpoint truly deletes an event from the database.

## Installation instructions

Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running locally.

Clone this repository, and from its root directory run `make run`.

If you see `User Event Tracker` when you visit [localhost](http://localhost), everything is running as expected.

## Sample requests

### Postman collection

You can find a Postman collection [here](/postman/collection.json).

### cURLs

- Get requests:

    - [/](http://localhost)
    - [Get all events for user](http://localhost/events)
    - [Get a specific event](http://localhost/event/83731cc8-b3f3-4962-bcb3-e12f5542eb41)

- Create an event

```
curl --location 'http://localhost/event' \
--header 'Content-Type: application/json' \
--data '{
    "title": "A deactivated event",
    "description": "Not active."
} '
```

- Search title

```
curl --location 'http://localhost/events' \
--header 'Content-Type: application/json' \
--data '{
    "title": "time"
} '
```

- Search description

```
curl --location 'http://localhost/events' \
--header 'Content-Type: application/json' \
--data '{
    "description": "it'\''s"
} '
```

- Search title AND description

```
curl --location 'http://localhost/events' \
--header 'Content-Type: application/json' \
--data '{
    "title": "refreshing",
    "description": "something"
} '
```

- Deactivate event

You might prefer to create a separate event to test this one.  Just swap out the eid!

```
curl --location --request PUT 'http://localhost/event/92be70d5-8811-4520-b7c5-7f3025e7159e'
```

- Delete event

You might prefer to create a separate event to test this one.  Just swap out the eid!

```
curl --location --request DELETE 'http://localhost/event/92be70d5-8811-4520-b7c5-7f3025e7159e'
```

- For further testing: create a different user

    - Visit [Create a user](http://localhost/user)
    - Copy the eid returned.
    - Replace the existing value for `USER_EID` in `app/config.py` with the newly-created user eid.
    - Try some requests.  See how they've changed.