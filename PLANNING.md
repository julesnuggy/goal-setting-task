1. **The functionality for marking and unmarking actions as complete isn’t finished.
   Thinking carefully about the relationship between parent and child actions, finish
   the `mark_as_complete` and `unmark_as_complete` methods on `GoalAction` model
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
2. **Implement the method `refresh_percentage_complete`. Thinking about the best way
   to represent the weight of completed tasks, write an algorithm for generating the
   percentage of actions completed (app/models.py).**
    1. Each `action` is the "top level" percentage completion
    2. The `sub-ation`s of an action are a percentage of that `action`s percentage
        1. So, if we have 4 `action`s, each is 25% of the total completion
        2. If the first action has no `sub-action`s, then it will just be 25% of the total.
        3. If the second action has 2 `sub-action`s, then each `sub-action` is half of the 25% that the first action
           constitutes, meaning these `sub-action`s are 12.5% each
            1. If these `sub-action`s have further `sub-action`s, then each of these will be `1/n` of the 12.5%,
               where `n` is the number of sub-actions
    3. So, at each level, each (sub-)action is `1/n` of the total percentage of its parent.
    4. The calculation for how much completion a (sub-)action constitutes will
       be: `parent_percentage / number_of_actions_at_this_level`
    5. The percentage should be refreshed whenever a (sub-)action is:
       1. Created
       2. Marked as complete
       3. Marked as incomplete
       4. Deleted
