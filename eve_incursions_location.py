import requests

print("======================================================================")
print("Starting EVE Incursions Location Utility...")
print("======================================================================")
print()

# get infested constellation IDs and their star system IDs
print("Getting infested constellation IDs and their star system IDs")
r_constellation = requests.get('https://esi.evetech.net/latest/incursions/?datasource=tranquility')

curr_inc_constellation_ids = []  # hold constellation IDs of incursion systems
curr_inc_constellation_system_ids = []  # hold constellation system of incursion systems

for constellation in r_constellation.json():
    # print(constellation)  # testing only...
    curr_inc_constellation_ids.append(constellation["constellation_id"])
    curr_inc_constellation_system_ids.append(constellation["infested_solar_systems"])
print("Done")

# get the names of each constellation ID
print("Getting names of infested constellation IDs")
constellation_id_url_str = 'https://esi.evetech.net/latest/universe/constellations/%s/?datasource=tranquility&language=en'
constellation_names = []

for constellation_id in curr_inc_constellation_ids:
    constellation_id_request_url = constellation_id_url_str % str(constellation_id)
    r_constellation_id = requests.get(constellation_id_request_url)
    constellation_names.append(r_constellation_id.json()["name"])
print("Done")

# get the names of each star system ID
print("Getting names of infested star system IDs")
system_id_url_str = 'https://esi.evetech.net/latest/universe/systems/%s/?datasource=tranquility&language=en'
system_names = []

for constellation_system_id in curr_inc_constellation_system_ids:
    system_names_temp = {}
    for system_id in constellation_system_id:
        system_id_request_url = system_id_url_str % str(system_id)
        r_system_id = requests.get(system_id_request_url)
        system_names_temp[r_system_id.json()["name"]] = round(r_system_id.json()["security_status"], 1)

    system_names.append(system_names_temp)  # add completed list of system names to system_name[]
print("Done")

print()
print("======================================================================")
print("Current Incursion constellations, their star systems, and security statuses are:")
print("======================================================================")
for i in range(len(constellation_names)):
    print(constellation_names[i], system_names[i])

print()
input("Press any key to exit...")
