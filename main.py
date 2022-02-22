from routePlotter import plot

kmlPath = "../LocationHistory.json"
be = (2.4, 6.6, 49.4, 51.7)
zoombe = 9
world = (-179, 79, -89, 89)
zoomworld = 1

plot(kmlPath, boundingBox=be, zoom=zoombe, verbose=True)
# plot(kmlPath, boundingBox=world, zoom=zoomworld, verbose=True)
# plot(kmlPath, verbose=True)
