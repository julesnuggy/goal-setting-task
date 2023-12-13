from app.models import User


def test_it_creates_goal():
    # arrange
    user = User.query.first()
    # act
    goal = user.create_goal("SomeGoal")
    # assert
    assert goal.text == "SomeGoal"


def test_it_creates_action():
    # arrange
    user = User.query.first()
    # act
    goal = user.create_goal("SomeGoal")
    goal_action = goal.create_action("SomeAction")
    # assert
    assert goal_action.text == "SomeAction"
    assert goal_action in goal.base_actions.all()


def test_it_gets_goal_user():
    # arrange
    user = User.query.first()
    # act
    goal = user.create_goal("SomeGoal")
    # assert
    assert goal.user == user


def test_it_marks_as_complete():
    # arrange
    user = User.query.first()
    # act
    goal = user.create_goal("SomeGoal")
    goal.mark_as_complete()
    # assert
    assert goal.completed is not None


# TODO - 2
def test_it_sets_correct_percentage_complete():
    # arrange
    user = User.query.first()
    goal = user.create_goal("SomeGoal")

    action_1 = goal.create_action("SomeAction1")  # 100/2 = 50%
    sub_action_1_1 = action_1.create_subaction("SomeSubAction1_1")  # 50/2 = 25%
    sub_action_1_2 = action_1.create_subaction("SomeSubAction1_2")  # 50/2 = 25%

    action_2 = goal.create_action("SomeAction2")  # 100/2 = 50%
    sub_action_2_1 = action_2.create_subaction("SomeSubAction2_1")  # 50/2 = 25%
    sub_action_2_2 = action_2.create_subaction("SomeSubAction2_2")  # 50/2 = 25%

    sub_action_2_2_1 = sub_action_2_2.create_subaction("SomeSubAction2_2_1")  # 25/3 = 8.33%
    sub_action_2_2_2 = sub_action_2_2.create_subaction("SomeSubAction2_2_2")  # 25/3 = 8.33%
    sub_action_2_2_3 = sub_action_2_2.create_subaction("SomeSubAction2_2_3")  # 25/3 = 8.33%

    # act
    sub_action_2_2_1.mark_as_complete()
    sub_action_2_2_2.mark_as_complete()
    # assert
    assert goal.percentage_complete is 17

    # act
    sub_action_2_2.mark_as_complete()
    # assert
    assert goal.percentage_complete is 25

    # act
    action_2.mark_as_complete()
    # assert
    assert goal.percentage_complete is 50

    # act
    sub_action_1_1.mark_as_complete()
    # assert
    assert goal.percentage_complete is 75

    # act
    action_1.mark_as_complete()
    # assert
    assert goal.percentage_complete is 100

