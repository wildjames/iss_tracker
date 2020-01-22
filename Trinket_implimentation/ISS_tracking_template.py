import json
import time
import turtle
import urllib.request
import geocoder



while True:
    #people in space
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    print("People in space: {}".format(result["number"]))

    people = result["people"]
    print("\n\nCurrent people in space:")
    for person in people:
        print("{:>20s}, craft: {}".format(person["name"], person["craft"]))

    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    # Request the ISS location.
    location = result["iss_position"]
    lat = float(location["latitude"])
    lon = float(location["longitude"])
    print("ISS lat, lon: {:.4f}, {:.4f}".format(lat, lon))

    # Lay down the background
    earth = "earth.gif"
    screen = turtle.Screen()
    screen.setup(720,360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic(earth)

    #iss turtle
    screen.register_shape("ISS k.gif")
    iss = turtle.Turtle()
    iss.shape("ISS k.gif")
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)


    # Where am I?
    # Get my location and label it
    me = geocoder.ip('me')
    mylat, mylon = me.latlng

    # Label
    location = turtle.Turtle()
    location.speed(999999999999999)
    location.hideturtle()
    location.penup()
    location.goto(mylon, mylat)
    location.color("crimson")
    location.dot(5)

    # When will the ISS pass this location? Label it.
    url = "http://api.open-notify.org/iss-pass.json?lat={}&lon={}".format(mylat, mylon)
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    over = result["response"][1]["risetime"]
    location.write(time.ctime(over), "6pt bold")

    time.sleep(60)

