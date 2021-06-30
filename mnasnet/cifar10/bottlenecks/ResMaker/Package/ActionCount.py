class action_count:

    def __init__(self, arguments=None, name=""):
        self.arguments = arguments
        self.counts=0
        self.name=name

    def get_dict(self):
        new_dict = {}
        if self.arguments:
            new_dict['arguments'] = self.arguments
        new_dict['counts'] = self.counts
        new_dict['name'] = self.name
        return new_dict


class action_counts:

    def __init__(self, name):
        self.dict = {}
        self.actions = []
        self.name = name

    def add_action(self, arguments=None, name=""):
        new_action = action_count(arguments, name)
        self.actions.append(new_action)

    def get_dict(self):
        actions_list  =[]
        for action in self.actions:
            tmp_dict = action.get_dict()
            actions_list.append(tmp_dict)
        new_dict = {"action_counts":actions_list ,'name':self.name}
        return new_dict

    def inc_action(self, action, count):
        self.actions[action].counts += count
