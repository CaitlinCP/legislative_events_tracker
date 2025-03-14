# legislative_events_tracker
Legislative events tracker allows a user to select a state and see what upcoming events there are for that state legislature.

## To Run:
Run `uv sync`
Run `uv run app.py`

## Future Updates:
Event data from states differs drastically. Right now, the product only includes results from three states: Texas, California, and Colorado.

* Parse time zone returned by the API to show the accurate time for an event
* Create an interface to search for bills associated with a hearing
* Handle state-level differences in returned event data
* Let people search for hearings by subject matter type
