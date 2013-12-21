"""
API client for Car Share Everywhere.

You must set CSE_API_ENDPOINT in your settings.
"""
import json


def get_fleet():
    # TODO
    json_result = json.loads('{"FleetName":"Okanagan Car Share Co-op","Request":{"NeighbourhoodLimit":null,"LocationLimit":null,"CarLimit":null,"Filter":null},"NeighbourhoodCount":"3","LocationCount":"3","CarCount":"3","Neighbourhoods":{"1":{"ID":"1","SortOrder":"1","Name":"Downtown","City":"Kelowna","LocationCount":"1","CarCount":"1","Locations":{"3":{"ID":"3","Name":"Downtown City Hall Parking Lot","ShortDescription":"City Hall Parking Lot","Latitude":"49.888826","Longitude":"-119.495401","CarCount":"1","Cars":{"3":{"ID":"3","Make":"Mazda","Model":"B2300","Year":"2003","Colour":"White","Category":null,"Plate":"FH5213","Seats":"2","AccessoryCount":"2","Accessories":{"17":"CD Player","16":"Power Door Locks"}}}}}},"4":{"ID":"4","SortOrder":"4","Name":null,"City":null,"LocationCount":"1","CarCount":"1","Locations":{"1":{"ID":"1","Name":"Downtown","ShortDescription":"Kelowna - Ellis Street & Queensway","Latitude":"49.887878","Longitude":"-119.493685","CarCount":"1","Cars":{"1":{"ID":"1","Make":"Toyota","Model":"Prius","Year":"2010","Colour":"White","Category":"Hybrid","Plate":"263RVL","Seats":"5","AccessoryCount":"7","Accessories":{"9":"Air Conditioning","10":"Bluetooth Handsfree","11":"Cruise Control","12":"MP3 CD Player","13":"Power Door Locks","14":"Power Mirrors","15":"Power Windows"}}}}}},"5":{"ID":"5","SortOrder":"5","Name":null,"City":null,"LocationCount":"1","CarCount":"1","Locations":{"2":{"ID":"2","Name":"South Pandosy","ShortDescription":"Osprey Park parking lot","Latitude":"49.866091","Longitude":"-119.490345","CarCount":"1","Cars":{"2":{"ID":"2","Make":"Nissan","Model":"Versa","Year":"2010","Colour":"white","Category":"4 Door Hatchback","Plate":"031RNM","Seats":"5","AccessoryCount":"8","Accessories":{"4":"Air Conditioning","7":"Bluetooth Handsfree","6":"Cruise Control","5":"MP3 CD Player","8":"Navigation System","1":"Power Door Locks","2":"Power Mirrors","3":"Power Windows"}}}}}}}}')
    # Go through the result, selecting which fields we want to expose
    # and fixing the type of various fields encoded as strings.
    locations = {}
    for n in json_result["Neighbourhoods"].itervalues():
        for loc in n["Locations"].itervalues():
            l_id = int(loc['ID'])
            cars = {}
            for c in loc['Cars'].itervalues():
                c_id = int(c["ID"])
                cars[c_id] = {
                    "id": c_id,
                    "year": int(c["Year"]),
                    "make": c["Make"],
                    "model": c["Model"],
                    "category": c["Category"],
                    "colour": c["Colour"],
                    "seats": int(c["Seats"]),
                    #"plate": c["Plate"],
                    "accessories": [a for a in c["Accessories"].itervalues()] if c["Accessories"] else [],
                }
            locations[l_id] = {
                "id": l_id,
                "name": loc['Name'],
                "lat": float(loc["Latitude"]),
                "lng": float(loc["Longitude"]),
                "short_description": loc['ShortDescription'],
                "cars": cars,
            }
    result = {
        "car_count": int(json_result["CarCount"]),
        "locations": locations,
    }
    return result
