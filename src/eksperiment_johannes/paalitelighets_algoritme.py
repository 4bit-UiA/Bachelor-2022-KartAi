import datetime
import numpy as np

observasjoner = [
    # 2017
    {"dataset": "foto", "dato": datetime.datetime(2017, 5, 17), "geometri": "2D", "areal": 100},
    {"dataset": "foto", "dato": datetime.datetime(2017, 5, 17), "geometri": "2D", "areal": 100},
    {"dataset": "foto", "dato": datetime.datetime(2017, 5, 17), "geometri": "2D", "areal": 100},
    {"dataset": "foto", "dato": datetime.datetime(2017, 5, 17), "geometri": "2D", "areal": 100},
    {"dataset": "foto", "dato": datetime.datetime(2017, 5, 17), "geometri": "2D", "areal": 100.2},
    {"dataset": "foto", "dato": datetime.datetime(2017, 5, 17), "geometri": "2D", "areal": 99.9},
    {"dataset": "ortofoto", "dato": datetime.datetime(2017, 8, 17), "geometri": "2D", "areal": 100},
    {"dataset": "lidar", "dato": datetime.datetime(2017, 9, 17), "geometri": "3D", "volum": 500},

    # 2018
    {"dataset": "foto", "dato": datetime.datetime(2018, 5, 17), "geometri": "2D", "areal": 100},
    {"dataset": "foto", "dato": datetime.datetime(2018, 5, 17), "geometri": "2D", "areal": 100},
    {"dataset": "foto", "dato": datetime.datetime(2018, 5, 17), "geometri": "2D", "areal": 100},
    {"dataset": "foto", "dato": datetime.datetime(2018, 5, 17), "geometri": "2D", "areal": 99},
    {"dataset": "foto", "dato": datetime.datetime(2018, 5, 17), "geometri": "2D", "areal": 100.1},
    {"dataset": "foto", "dato": datetime.datetime(2018, 5, 17), "geometri": "2D", "areal": 99.9},

    # 2019
    {"dataset": "foto", "dato": datetime.datetime(2019, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2019, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2019, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2019, 5, 17), "geometri": "2D", "areal": 105.2},
    {"dataset": "foto", "dato": datetime.datetime(2019, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2019, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "ortofoto", "dato": datetime.datetime(2019, 8, 17), "geometri": "2D", "areal": 105},

    # 2020
    {"dataset": "foto", "dato": datetime.datetime(2020, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2020, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2020, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2020, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2020, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2020, 5, 17), "geometri": "2D", "areal": 105},

    # 2021
    {"dataset": "foto", "dato": datetime.datetime(2021, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2021, 5, 17), "geometri": "2D", "areal": 105},
    {"dataset": "foto", "dato": datetime.datetime(2021, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2021, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2021, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2021, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "ortofoto", "dato": datetime.datetime(2021, 9, 17), "geometri": "2D", "areal": 110},

    # 2022
    {"dataset": "foto", "dato": datetime.datetime(2022, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2022, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2022, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2022, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2022, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "foto", "dato": datetime.datetime(2022, 5, 17), "geometri": "2D", "areal": 110},
    {"dataset": "lidar", "dato": datetime.datetime(2022, 8, 17), "geometri": "3D", "volum": 550},
]
"""
Alle faktorer og observasjoner i dette scriptet er mocket.    
"""
if __name__ == '__main__':
    ny_observasjon = {"dataset": "foto", "dato": datetime.datetime(2023, 5, 17), "geometri": "2D", "areal": 110}
    nyeste_aar: int = ny_observasjon['dato'].year
    # utgangspunkt
    paalitelighetsmaal: float = 50.0

    observasjoner.reverse()

    # Henter ut 3D observasjoner.
    observasjoner_3D = []
    for observasjon in observasjoner:
        if observasjon["dataset"] == "lidar":
            observasjoner_3D.append(observasjon)

    # Går videre om det er 2 3D objekter
    if observasjoner_3D[1] is not None:
        # Filtrerer ut observasjoner som ikke eksisterer i tidsrommet mellom nyeste observasjon og anst nyeste
        # observasjon som holder på et 3D objekt
        observasjoner_i_tidsrom = list(filter(lambda x: (x['dato'] >= observasjoner_3D[1]['dato']), observasjoner))
        observasjoner_i_tidsrom_2D = list(filter(lambda x: x['geometri'] == "2D", observasjoner_i_tidsrom))

        # Foerste 2D observasjon i utvalgt tidsrom
        observasjon_nr1_2D = observasjoner_i_tidsrom_2D[len(observasjoner_i_tidsrom_2D) - 1]

        # Ser på forskjeller hos "3D objekter" og "2D objekter" fra samme tidsrom samsvarer med hverandre.
        # Om vist så styrkes paaliteligheten basert på tidsrommet mellom den nye observasjonen og sist 3D observasjon.
        ############################################################################
        diff_ny_observasjon_nr1_observasjon_2D = ny_observasjon['areal'] - observasjon_nr1_2D['areal']
        diff_lidar1_lidar2_3D = observasjoner_3D[0]['volum'] - observasjoner_3D[1]['volum']

        # Om begge differ samsvarer, det vil si om begge har økt eller om begge har synket
        if (diff_ny_observasjon_nr1_observasjon_2D > -0.2 and diff_lidar1_lidar2_3D > -0.5) or (
                diff_ny_observasjon_nr1_observasjon_2D < -0.2 and diff_lidar1_lidar2_3D < -0.5):
            # Hvor mye denne samsvaringen teller avgjøres av år mellom ny observasjon og sist 3D observasjon
            # 4 og over ignoreres
            match ny_observasjon['dato'].year - observasjoner_3D[0]['dato'].year:
                case 0:
                    paalitelighetsmaal *= 1.3
                case 1:
                    paalitelighetsmaal *= 1.2
                case 2:
                    paalitelighetsmaal *= 1.1
                case 3:
                    paalitelighetsmaal *= 1.05

            print("Pålitelighetsmål:", paalitelighetsmaal)
        ############################################################################

        # Sammenligner ny observasjoner med 2D observasjoner fra de siste 3 årene.
        ############################################################################
        # Filtrerer ut alle observasjoner som ikke er fra de siste 3 årene.
        observations_last_3_y = list(
            filter(lambda x: x['dato'].year in range(nyeste_aar - 3, nyeste_aar), observasjoner_i_tidsrom_2D))

        # Map som holder på likheter og uliker gjennom årene.
        # 20XX (lik, ulik), 20XX - 1 (lik ulik), 20XX - 2 (lik, ulik)
        likhet_gjennom_aar = [[0, 0], [0, 0], [0, 0]]

        for o in observations_last_3_y:
            if -0.2 <= (ny_observasjon['areal'] - o['areal']) <= 0.2:
                if o['dato'].year == nyeste_aar:
                    likhet_gjennom_aar[0][0] += 1
                elif o['dato'].year == nyeste_aar - 1:
                    likhet_gjennom_aar[1][0] += 1
                elif o['dato'].year == nyeste_aar - 2:
                    likhet_gjennom_aar[2][0] += 1
            else:
                if o['dato'].year == nyeste_aar:
                    likhet_gjennom_aar[0][1] += 1
                elif o['dato'].year == nyeste_aar - 1:
                    likhet_gjennom_aar[1][1] += 1
                elif o['dato'].year == nyeste_aar - 2:
                    likhet_gjennom_aar[2][1] += 1

        scores = likhet_gjennom_aar.copy()

        # Her så sammenlignes antall like observasjoner et år med antall ulike.
        # Om det det finnes både ulike og like så deles like på ulike for å lage en score. Feks 6 / 2 = 3
        # Om det er > 0 like og 0 ulike så settes scoren til antall like. Som feks [6, 0] score = 6
        # Om det er 0 like og > 0 ulike så settes scoren til 0
        # Alt annet settes osm 0.5
        for i in range(len(likhet_gjennom_aar)):
            score = scores[i]
            if score[0] != 0 and score[1] != 0:
                scores[i] = score[0] / score[1]
            elif score[0] != 0 and score[1] == 0:
                scores[i] = score[0]
            elif score[0] == 0 and score[1] != 0:
                scores[i] = 0
            else:
                scores[i] = 0.5

        print("\nObservasjoner som er like og ulike nyeste observasjon de siste 3 årene:")
        print(nyeste_aar, ":", likhet_gjennom_aar[0][0], "like,", likhet_gjennom_aar[0][1], "ulike. Score:",
              scores[0])
        print(nyeste_aar - 1, ":", likhet_gjennom_aar[1][0], "like,", likhet_gjennom_aar[1][1], "ulike. Score:",
              scores[1])
        print(nyeste_aar - 2, ":", likhet_gjennom_aar[2][0], "like,", likhet_gjennom_aar[2][1], "ulike. Score:",
              scores[2])

        ############################################################################
        faktor: float = 0.0
        tillegg: float = 0.0

        # Her regner vi ut faktoren som skal ganges med tidligere paalitelighetsmål.
        # Et tillegg på faktoren blir lagt til basert på hver score.
        # Siste linje i loopen tar også hensyn til år. Om scoren er for et mål 3 år siden så ganges tilegget med 0.7
        for i in range(0, 3):
            if likhet_gjennom_aar[i][0] == 0 and likhet_gjennom_aar[i][1] == 0:
                continue
            elif scores[i] > 2:
                tillegg += scores[i] - 2
            elif 1 <= scores[i] < 2:
                tillegg += 1
            tillegg *= 1 - (i / 10) if i != 0 else 1

        faktor += tillegg
        paalitelighetsmaal *= 1 + (faktor / 10)

        print()
        print("Pålitelighetsmål:", paalitelighetsmaal)
