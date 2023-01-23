# Actions
Actions are classes that inherit from `BaseAction` and implement the `pre_create`, `post_create`, `pre_update`, `post_update`, `pre_delete`, `post_delete` methods.
You can use them to implement business logic that is not related to the model itself.

For example, you can use them to implement a `pre_create` method that sends an email to the user when a new user is created.

## Example

```python
...  # imports
from canvass_fastapi.actions import BaseAction
from {{ cookiecutter.project_module }}.models import User

class WelcomeEmailAction(BaseAction):
    async def pre_create(self, user: User, context: dict = None) -> None:
        # Send an email to the user
        await send_email(user.email, "Welcome to {{ cookiecutter.project_name }}!")
```

## Usage

To use an action, you need to register it in the repositories that you want to use it. For example, if you want to use the `WelcomeEmailAction` in the `UserRepository`, you need to register it in the `UserRepository`:

```python
...  # imports
from {{ cookiecutter.project_module }}.actions import WelcomeEmailAction


class UserRepository(AsyncModelRepository[User]):
    class Meta:
        model = User
        actions = [WelcomeEmailAction]
```

