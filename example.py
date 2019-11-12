#
# username_list = ['la','qw','sf','qe']
# username_list_len= len(username_list)
# print(username_list_len)
# print(username_list[3])
# for i in range(username_list_len):
#     print('\ni:'+str(i))
#     print(username_list[i])

ROOM_SIZE = 10
room_size_reserve = []*ROOM_SIZE

room_size_reserve2 = []*ROOM_SIZE

name = 'phong'

second_name = 'linh'

third_name = 'bon'

room_list = []

room_list.append([name])

room_list.append([second_name])

room_list[0].append(third_name)

#room_list[0].append(second_name)

#room_list[1].append(third_name)

print(room_list)