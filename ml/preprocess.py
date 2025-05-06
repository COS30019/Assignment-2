import csv

def preview_csv(filepath, output_txt="preview_output.txt", num_rows=5):
    with open(filepath, "r", newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    for row in rows[:num_rows + 1]:
        print(row)
    with open(output_txt, "w") as f:
        for row in rows[:num_rows + 1]:
            f.write(", ".join(row) + "\n")

if __name__ == "__main__":
    preview_csv("Traffic_Count_Locations_with_LONG_LAT.csv")

# X, Y, FID, OBJECTID, TFM_ID, TFM_DESC, TFM_TYP_DE, MOVEMENT_T, SITE_DESC, ROAD_NBR, DECLARED_R, LOCAL_ROAD, DATA_SRC_C, DATA_SOURC, TIME_CATEG, YEAR_SINCE, LAST_YEAR, AADT_ALLVE, AADT_TRUCK, PER_TRUCKS
# 144.250613557206833, -36.779313366338279, 7001, 7301, 7656, CALDER HWY NE OF OAK ST, INTERSECTION, All Moves, CALDER HWY & OAK ST, 2530, CALDER HIGHWAY, HIGH STREET, TMVMT, Manual, Greater than 10 Years, 19, 1997, 7700, 330, 0.04
# 145.356779391056335, -37.835308803164338, 7002, 7302, 29406, MT DANDENONG RD S BD SE OF UPALONG RD, INTERSECTION, All Moves, MT DANDENONG RD SE OF UPALONG RD, 4991, MOUNT DANDENONG ROAD, MOUNT DANDENONG TOURIST ROAD, APARX, Classification, Greater than 10 Years, 16, 2000, 1900, 0, 0
# 144.988843533294272, -37.824628792499844, 7003, 7303, 22676, SWAN ST W BD E OF PUNT RD, INTERSECTION, All Moves, PUNT RD LEFT TURN TO SWAN ST OD:12, 2080, HODDLE HIGHWAY, PUNT ROAD, MOTSV, Manual, Greater than 10 Years, 23, 1993, 15000, 630, 0.04
# 144.932442383513632, -37.803783317565575, 7004, 7304, 27902, DYNON RD W BD E OF RADCLIFFE ST, INTERSECTION, All Moves, DYNON RD & RADCLIFFE ST, 5035, DYNON ROAD, DYNON ROAD, TMVMT, Manual, Greater than 10 Years, 19, 1997, 12000, 1300, 0.1
# 145.030600501489857, -37.660502400829095, 7005, 7305, 10935, DALTON RD N of CHILDS RD, INTERSECTION, All Moves, CHILDS RD & DALTON RD, 5605, DALTON ROAD, DALTON ROAD, TMVMT, Manual, Greater than 10 Years, 19, 1997, 12000, 600, 0.05
