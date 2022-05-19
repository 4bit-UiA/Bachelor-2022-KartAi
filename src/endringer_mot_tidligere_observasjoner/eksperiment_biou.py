from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from descartes import PolygonPatch


def measure_biou(geo1: Polygon, geo2: Polygon):
    # Tykkelsen på "inwards stroke":
    d = -3

    G = geo1
    G_d = geo1.buffer(d, cap_style=3, join_style=2, mitre_limit=10)

    P = geo2
    P_d = geo2.buffer(d, cap_style=3, join_style=2, mitre_limit=10)

    G_d_intersect_G = G_d.symmetric_difference(G)
    P_d_intersect_P = P_d.symmetric_difference(P)

    intersect = G_d_intersect_G.intersection(P_d_intersect_P)
    union = G_d_intersect_G.union(P_d_intersect_P)

    biou = intersect.area / union.area

    return biou


## Under her følger eksempel-data og noen metoder brukt for å visualisere dem
geo1 = Polygon([[0,0], [0,10], [10,10], [10,0], [0,0]])
geo5 = Polygon([[0.5,0.5], [0.5,10.5], [10.5,10.5], [10.5,0.5], [0.5,0.5]])

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


def scatter(geo1, geo2):
    fig, ax = plt.subplots()

    ax.scatter(*geo1.exterior.xy, alpha=0.0)
    ax.add_patch(PolygonPatch(geo1, alpha=0.5, fc='orange'))
    if geo2:
        ax.add_patch(PolygonPatch(geo2, alpha=0.5, fc='blue'))

    #ax.scatter(x2,y2)
    #ax.scatter(x_u,y_u)
    #ax.add_patch(PolygonPatch(alpha, alpha=0.2))
    plt.show()


if __name__ == "__main__":
    print(measure_biou(geo1, geo5))
    #fig, ax = plt.subplots()
    #ax.add_patch(PolygonPatch(row1, alpha=0.2))
    #plt.show()

    print()
    # show()


