from geopy.geocoders import Yandex
from geopy.distance import vincenty
import time

t0 = time.time()
geolocator = Yandex()
location1 = geolocator.geocode("Московская обл, г Клин", timeout=10)
print(location1.address)
print(location1.point)
print((location1.latitude, location1.longitude))
print(location1.raw)


center = geolocator.geocode('Москва', timeout=10)

loc_coord = (location1.latitude, location1.longitude)
center_coord = (center.latitude, center.longitude)
print(vincenty(loc_coord, center_coord).km)
print(time.time()-t0)