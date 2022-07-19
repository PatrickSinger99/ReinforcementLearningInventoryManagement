import itertools

action_space = [5, 5, 2]


def create_actions_conversion_list():
    actions_as_lists = []

    for entry in action_space:
        new_list = []
        for pos in range(entry):
            new_list.append(pos)
        actions_as_lists.append(new_list)

    actions_dict = {}
    all_pos_action_comb = list(itertools.product(*actions_as_lists))

    count = 0
    for action_combination in all_pos_action_comb:
        actions_dict[count] = list(action_combination)
        count += 1

    return actions_dict


actions_dict = create_actions_conversion_list()
print(actions_dict)


def convert_discrete_to_multi_discrete(discrete_action):
    return actions_dict[discrete_action]


def convert_nulti_discrete_to_discrete(multi_discrete_action):
    for entry in actions_dict:
        if actions_dict[entry] == multi_discrete_action:
            return entry


a = convert_discrete_to_multi_discrete(0)
b = convert_nulti_discrete_to_discrete([0, 4, 0])
print(a)
print(b)



