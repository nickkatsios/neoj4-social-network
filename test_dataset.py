
# Check to see how many user nodes we will have to create
# in order to assign relationships and avoid creating unecessary nodes
def check_range_in_sorted_list(sorted_list, start, end):
    if not sorted_list:
        return False

    if start > sorted_list[-1] or end < sorted_list[0]:
        return False

    i = 0
    for num in range(start, end+1):
        while i < len(sorted_list) and sorted_list[i] < num:
            i += 1
        if i >= len(sorted_list) or sorted_list[i] != num:
            return False
    return True

def read_tsv_user_ids(filepath):
    user_ids = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            values = line.strip().split('\t')
            user_id = int(values[1])
            user_ids.append(user_id)
    user_ids.sort()
    return user_ids

def read_tsv_target_ids(filepath):
    target_ids = []
    with open("./dataset/mooc_actions.tsv", 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            values = line.strip().split('\t')
            target_id = int(values[2])
            target_ids.append(target_id)
    target_ids.sort()
    return target_ids


user_ids_sorted = read_tsv_user_ids("./dataset/mooc_actions.tsv")
target_ids_sorted = read_tsv_target_ids("./dataset/mooc_actions.tsv")

print(str(user_ids_sorted[-1]))
print(str(target_ids_sorted[-1]))
print(check_range_in_sorted_list(user_ids_sorted , 0 , user_ids_sorted[-1]))
print(check_range_in_sorted_list(target_ids_sorted , 0 , target_ids_sorted[-1]))



