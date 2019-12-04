import numpy as np
from region import Region
import csv

# Metodo per caricare una linked map da file CSV
def load_csv_map(shapes, map_filename):
    # Creo la struttura dati vuota
    linked_map = np.empty((shapes[0],shapes[1]), dtype=object)
    # Inizializzo le coordinate di ogni regione 
    for x in range(0, linked_map.shape[0]):
        for y in range(0, linked_map.shape[1]):
            linked_map[x][y] = Region(coord=(x,y))
    with open(map_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        i = 0
        j = 0
        # Per ogni riga del CSV, aggiunge le simulazioni alla struttura dati
        for row in csv_reader:
            linked_map[i][j].add_list_sim(row)
            j += 1
            if j >= shapes[1]:
                i += 1
                j = 0
            line_count += 1
            if line_count % 1000 == 0:
                print("Line ", line_count, " processed")
    print("Linked Map created")
    return linked_map

# Metodo per salvare una linked map in un file CSV
def write_in_csv(csv_filename, l_map):
    print("Writing csv...")
    line_count = 0
    with open(csv_filename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        for x in range(0, l_map.shape[0]):
            for y in range(0, l_map.shape[1]):
                filewriter.writerow(l_map[x][y].create_csv_row())
                line_count += 1
                if line_count % 10000 == 0:
                    print("Line ", line_count, " processed")
    print("CSV written")

# Conversion coordinate griglia vent in griglia DEM
def vent_in_dem(notN_filename):
    # numero di righe della griglia dei vent
    ROWS_VENT = 73
    # ampiezza in metri quadrati di ogni cella della griglia vent
    STEP_VENT = 500
    # estremi coordinate nord e ovest della griglia dei vent
    EASTING_MIN_VENT = 482490
    NORTHING_MAX_VENT = 4191990

    # estremi coordinate nord e ovest della griglia DEM
    NORTHING_MAX_DEM = 4192500
    EASTING_MIN_DEM = 482500
    # ampiezza in metri quadrati di ogni cella della griglia DEM
    STEP_DEM = 20

    # calcola coordinate della bocca nella griglia vent 
    id_vent = int(notN_filename[10: -6])-1
    x_vent = id_vent % ROWS_VENT
    y_vent = int(id_vent/ROWS_VENT)

    # calcola le coordinate nord e est della bocca
    northing_vent = NORTHING_MAX_VENT - (STEP_VENT * x_vent)
    easting_vent = EASTING_MIN_VENT + (STEP_VENT * y_vent)
    # calcola le coordinate della bocca nella griglia DEM
    x_dem = int((NORTHING_MAX_DEM - northing_vent) / STEP_DEM)
    y_dem =int((easting_vent - EASTING_MIN_DEM) / STEP_DEM)

    return (x_dem, y_dem)
"""
l_map = load_csv_map((455,375), 'scaled_map.csv')
print(l_map[2][122].sim) """