from app import db
import datetime


class User(db.Model):
    """User model for authentication and identification"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.Unicode(32))
    surname = db.Column(db.Unicode(32))
    username = db.Column(db.String(128), unique=True)

    @property
    def name(self):
        # display full name of user
        return self.forename + " " + self.surname

    def create_goal(self, text):
        # check some text has been entered
        if not text.strip():
            raise ValueError("Goals must have some text")

        goal = Goal(text=text)
        self.goals.append(goal)
        return goal


class Goal(db.Model):
    """Big overall goals for individual users, comprising of actions"""

    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    completed = db.Column(db.DateTime)
    percentage_complete = db.Column(db.SmallInteger, default=0)
    text = db.Column(db.Unicode(512), nullable=False)

    user = db.relationship(
        "User",
        backref=db.backref(
            "goals",
            order_by="Goal.created",
            cascade="all,delete-orphan",
            lazy="dynamic",
        ),
    )

    def create_action(self, text):
        # check some text has been entered
        if not text.strip():
            raise ValueError("Actions must have some text")

        action = GoalAction(text=text)
        self.actions.append(action)
        db.session.flush()  # in case refresh_percentage_complete uses further queries

        self.refresh_percentage_complete()

        return action

    def mark_as_complete(self):
        self.completed = datetime.datetime.utcnow()

    @property
    def base_actions(self):
        # fetch non-nested actions
        return self.actions.filter(GoalAction.parent_action_id == None)

    # TODO - 2
    def calculate_completion(self, action, proportion):
        if action.completed:
            self.percentage_complete += proportion
        elif action.child_actions:
            action_proportion = proportion/len(action.child_actions)
            for child in action.child_actions:
                self.calculate_completion(child, action_proportion)

    def refresh_percentage_complete(self):
        self.percentage_complete = 0
        base_actions = self.base_actions.all()
        proportion = 100/len(base_actions)

        for base_action in base_actions:
            self.calculate_completion(base_action, proportion)

        return self.percentage_complete

    def delete_goal(self):
        db.session.delete(self)


class GoalAction(db.Model):
    """Actions & nested sub-actions for goals"""

    __tablename__ = "goalaction"

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=False)
    parent_action_id = db.Column(db.Integer, db.ForeignKey("goalaction.id"))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    completed = db.Column(db.DateTime)
    text = db.Column(db.Unicode(512), nullable=False)

    goal = db.relationship(
        "Goal",
        backref=db.backref(
            "actions",
            order_by="GoalAction.created",
            cascade="all,delete-orphan",
            lazy="dynamic",
        ),
    )
    parent_action = db.relationship(
        "GoalAction",
        remote_side="GoalAction.id",
        foreign_keys="GoalAction.parent_action_id",
        backref=db.backref(
            "child_actions",
            remote_side="GoalAction.parent_action_id",
            cascade="all,delete-orphan",
            order_by="GoalAction.created",
        ),
    )

    def create_subaction(self, text):
        # check some text has been entered
        if not text.strip():
            raise ValueError("Actions must have some text")

        action = GoalAction(text=text, goal=self.goal)
        db.session.add(action)

        self.child_actions.append(action)
        db.session.flush()  # in case refresh_percentage_complete uses further queries

        self.goal.refresh_percentage_complete()
        return action

    # TODO - 1
    def mark_as_complete(self):
        self.completed = datetime.datetime.utcnow()

        if self.child_actions:
            for action in self.child_actions:
                action.mark_as_complete()

        if self.parent_action:
            child_completions = [child.completed is not None for child in self.parent_action.child_actions]
            if not self.parent_action.completed and all(child_completions):
                self.parent_action.mark_as_complete()

        self.goal.refresh_percentage_complete()

    # TODO - 1
    def unmark_as_complete(self):
        self.completed = None

        if self.child_actions:
            for action in self.child_actions:
                action.unmark_as_complete()

        if self.parent_action and self.parent_action.completed:
            self.parent_action.completed = None

        self.goal.refresh_percentage_complete()

    def delete_action(self):
        goal = self.goal
        self.goal.actions.remove(self)
        db.session.flush()  # in case refresh_percentage_complete uses further queries

        goal.refresh_percentage_complete()
