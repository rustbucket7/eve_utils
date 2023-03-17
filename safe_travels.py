import requests

print("======================================================================")
print("Starting EVE Safe Travels Utility...")
print("======================================================================")
print()

# starting and destination star system names
start_loca = 'Jita'
dest_loca = 'Dodixie'
loca_data = "[\"%s\", \"%s\"]" % (start_loca, dest_loca)

# retrieve star system IDs (will use POST method)
print("Retrieving IDs of start and destination star systems")
get_star_system_ids_url = "https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en"
post_star_systems_ids = requests.post(get_star_system_ids_url, data=loca_data)
returned_star_systems = post_star_systems_ids.json()["systems"]
name_id_dict = {}

# save a dictionary containing {system_name:system_id} for start and dest system
for star_system in returned_star_systems:
    name_id_dict[star_system['name']] = star_system['id']
print("Done")

# retrieve route between locations
print("Retrieve route between start and destination star systems")
get_route_url = "https://esi.evetech.net/latest/route/%s/%s/?datasource=tranquility&flag=shortest"
get_route_url = get_route_url % (name_id_dict[start_loca], name_id_dict[dest_loca])
get_route = requests.get(get_route_url)
get_route_list = get_route.json()
print("Done")

# retrieve # of kills in all systems (no API call available for more granular calls)
print("Retrieve # of kills in all star systems")
get_all_system_kills_url = "https://esi.evetech.net/latest/universe/system_kills/?datasource=tranquility"
get_all_system_kills = requests.get(get_all_system_kills_url)
get_all_system_kills_list = get_all_system_kills.json()  # list of JSON objects
print("Done")

# output # of kills in the systems along the route
print()
print("======================================================================")
print("Route (shortest) from %s to %s" % (start_loca, dest_loca))
print("======================================================================")
print("Format -- Name: Ship Kills, Pod Kills")
print("----------------------------------------------------------------------")

system_id_url = "https://esi.evetech.net/latest/universe/systems/%s/?datasource=tranquility&language=en"

print("Number of jumps (not including %s): %d" % (start_loca, len(get_route_list) - 1))  # -1 accounts for the starting system
print()

for i in range(len(get_route_list)):
    curr_sys_id = get_route_list[i]

    # traverse list of all system kills until desired system is found
    for system_object in get_all_system_kills_list:
        if curr_sys_id == system_object["system_id"]:
            # when found, output name of system and # of ship kills and pod kills
            sys_name_url = system_id_url % str(curr_sys_id)
            get_sys_name = requests.get(sys_name_url)
            sys_name = get_sys_name.json()["name"]
            print(sys_name + ":", str(system_object["ship_kills"]) + ",", system_object["pod_kills"])

print()
input("Press any key to exit...")
