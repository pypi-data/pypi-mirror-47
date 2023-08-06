# DJ StreamIO

Framework for making it easy to post stream updates to (stream.io)[https://getstream.io]

## Installation

[![PyPI version](https://badge.fury.io/py/dj-streamio.svg)](https://badge.fury.io/py/dj-streamio)

```
pip install dj-streamio
```

## Configuration

### 1. Add `streamio` to `INSTALLED_APPS`

### 2. Configure your models for tracking:

e.g.:

```python
class Todo(models.Model, StreamModelMixin):

    collection = 'todos'
    feed_name = 'todo'
    feed_actor_field = 'owner_id'
    feed_once_off_actions = ["create"]
    feed_related_mapping = [
        # feed_slug, model_field
        ('user', 'owner_id'),
        ('todo', 'id'),
    ]
    enrichment_serializer = 'example_app.models.TodoSerializer'

```

**Notes:**

1. We add `StreamModelMixin` to our model
2. Add the various meta fields
3. Profit

now you can now run:

```python
todo = Todo.objects.first()
todo.track_action('create')
todo.track_action('start')
todo.track_action('complete')
```

### TODOS:

* Provide signals
* Provide async celery task
* Provide alternative backends (later)



