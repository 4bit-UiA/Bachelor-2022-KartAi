from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import alphashape
from descartes import PolygonPatch


geo1 = Polygon([[0,0], [0,10], [30,10], [30,0], [0,0]])
geo2 = Polygon([[0,0], [0,10], [30,10], [30,0], [20,0], [20,-10], [10, -10], [10, 0], [0,0]])
geo3 = Polygon([[0,0], [0,20], [ 5,20], [5, 5], [20,5], [20, 0], [15, 0], [15, -5], [5,-5], [5, 0], [0, 0]])
geo4 = Polygon([[1,1], [1,21], [ 6,21], [6, 6], [16,6], [16, -4], [6,-4], [6, 1], [1, 1]])


def show(ob1, ob2):
    x1, y1 = ob1.exterior.xy
    x2, y2 = ob2.exterior.xy
    plt.plot(x1,y1)
    plt.plot(x2,y2)

    # plt.plot(*geo2.exterior.xy)
    plt.show()


if __name__ == "__main__":
    x1, y1 = geo3.exterior.coords.xy
    x2, y2 = geo4.exterior.coords.xy
    
    corners_geo1 = len(x1)-1
    corners_geo2 = len(x2)-1

    show(geo3, geo4)

    print(min(corners_geo1, corners_geo2))

    union = geo3.union(geo4)

    x_u, y_u = union.exterior.coords.xy

    x_a = x1+x2
    y_a = y1+y2
    xy = []

    for i in range(0, len(x_a)):
        xy.append( [x_a[i], y_a[i]])


    #print(xy)

    #alpha = alphashape.alphashape(xy, 0.1)
    #print(alpha)

    #x3, y3 = alpha.xy
    
    fig, ax = plt.subplots()
    
    #ax.scatter(x1,y1)
    #ax.scatter(x2,y2)
    #ax.scatter(x_u,y_u)
    #ax.add_patch(PolygonPatch(alpha, alpha=0.2))

    area_c_x, area_c_y = union.exterior.coords.xy


    # Loop least corners
    for i in range(0, len(x_u)):
        print(i, x_u[i], y_u[i])
        if i > 0 and i < len(x_u) - 1:
            prev_xy = x_u[i-1], y_u[i-1]
            this_xy =   x_u[i], y_u[i]
            next_xy = x_u[i+1], y_u[i+1]

            # angle = shapely.angle()
            


    area_c_x.pop(1)
    area_c_y.pop(1)
    
    area_c_x.pop(3)
    area_c_y.pop(3)

    area_c_x.pop(4)
    area_c_y.pop(4)

    area_c_x.pop(6)
    area_c_y.pop(6)

    area_c_x.pop(7)
    area_c_y.pop(7)

    area_c_x.pop(9)
    area_c_y.pop(9)
    
    

    plt.plot(x_u,y_u)
    plt.plot(area_c_x, area_c_y)
    plt.show()


    print()
    # show()
