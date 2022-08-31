from routePlotter import plot

kmlPath = "../Records.json"
be = (2.4, 6.6, 49.4, 51.7)
zoombe = 9
ch = (5.4,11.0,45.5,47.8)
zoomch = 9
world = (-179, 79, -89, 89)
zoomworld = 1

leuven = (4.65,4.72,50.85,50.9)
zoomleuven=15

# plot(kmlPath, boundingBox=be, zoom=zoombe, name="be". verbose=True)
plot(kmlPath, boundingBox=ch, zoom=zoomch, name="ch", verbose=True)
# plot(kmlPath, boundingBox=leuven, zoom=zoomleuven, name="leuven_12", verbose=True, minDistThreshold=1e-7, splitDistThreshold=3e-2, minRelativeDistThreshold=0.7)
# plot(kmlPath, boundingBox=world, zoom=zoomworld, verbose=True)
# plot(kmlPath, verbose=True, zoom=12, startDate='2022-04-16 00:00:00', endDate='2022-04-19 12:00:00')
plot(kmlPath, verbose=True)
