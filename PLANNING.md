1. **The functionality for marking and unmarking actions as complete isn’t finished.
   Thinking carefully about the relationship between parent and child actions, finish
   the mark_as_complete and unmark_as_complete methods on GoalAction model
   (app/models.py).**
    1. mark_as_complete:
        - When an `action` is marked as complete, all `sub-action`s should also be marked as complete
          (recursion).
        - When all `sub-action`s are individually marked as complete, the parent `action` should also be marked as
          complete

    2. unmark_as_complete:
        - If an `action` and its `sub-action`s are marked as complete, if the `action` is unmarked as complete, then
          its `sub-action`s should all be unmarked too.
        - If an `action` and its `sub-action`s are marked as complete, if a `sub-action` is unmarked as complete,
          then the `action` should be unmarked as complete (but any sibling `sub-action`s should not be changed).
