from typing import Optional

from app.models import Goal, User


def _create_goal(name: Optional[str] = "SomeGoal") -> Goal:
    user = User.query.first()
    return user.create_goal(name)


def test_it_creates_subaction():
    # arrange
    goal = _create_goal()
    action_1 = goal.create_action("SomeAction")
    # act
    action_2 = action_1.create_subaction("SomeSubAction")
    # assert
    assert action_2.text == "SomeSubAction"
    assert action_2.parent_action == action_1


# TODO - 1
def test_it_marks_as_complete():
    # arrange
    goal = _create_goal()
    action_1 = goal.create_action("SomeAction")

    # act
    action_1.mark_as_complete()

    # assert
    assert action_1.completed is not None


def test_it_marks_sub_actions_as_complete():
    # arrange
    goal = _create_goal()
    action_1 = goal.create_action("SomeAction")
    sub_action_1 = action_1.create_subaction("SomeSubAction1")
    sub_action_2 = action_1.create_subaction("SomeSubAction2")

    # act
    action_1.mark_as_complete()

    # assert
    assert action_1.completed is not None
    assert sub_action_1.completed is not None
    assert sub_action_2.completed is not None


def test_it_marks_parent_action_as_complete_when_all_sub_actions_are_complete():
    # arrange
    goal = _create_goal()
    action_1 = goal.create_action("SomeAction")
    sub_action_1 = action_1.create_subaction("SomeSubAction1")
    sub_action_2 = action_1.create_subaction("SomeSubAction2")

    # act
    sub_action_1.mark_as_complete()
    sub_action_2.mark_as_complete()

    # assert
    assert action_1.completed is not None
    assert sub_action_1.completed is not None
    assert sub_action_2.completed is not None


# TODO - 1
def test_it_marks_as_not_complete():
    pass
