def nextLevel(reborn, lev):
    if reborn == 0:
        if lev < 6:
            return (0, lev + 1)
        else:
            return 1, 1
    elif reborn == 1:
        if lev < 11:
            return (1, lev + 1)
        else:
            return (2, 1)
    elif reborn == 2:
        if lev < 16:
            return (2, lev + 1)
        else:
            return (3, 1)
    elif reborn == 3:
        if lev < 21:
            return (3, lev + 1)
        else:
            return (4, 1)
    elif reborn == 4:
        if lev < 26:
            return (4, lev + 1)
        else:
            return (5, 1)
    elif reborn == 5:
        if lev < 31:
            return (5, lev + 1)
        else:
            return (5, 31)

# df = r0_tab
#
# #Reborn 0
# tmp = df[df["Level"]<=6]
# tmp = tmp.copy(deep=True)
# tmp["Reborn"]=0
# tmp["Iter"]=tmp["Level"]
# lvl_table = tmp.copy(deep=True)
#
# #Reborn 1
# tmp = df[df["Level"]<=11]
# tmp = tmp.copy(deep=True)
# tmp["Reborn"]=1
# tmp["Iter"]=tmp["Level"]+6
# tmp["Might"] += 200
# tmp["Troops"] += 102
# lvl_table = lvl_table.append(tmp)
#
# #Reborn 2
# tmp = df[df["Level"]<=16]
# tmp = tmp.copy(deep=True)
# tmp["Reborn"]=2
# tmp["Iter"]=tmp["Level"]+11+6
# tmp["Might"] += (200+350)
# tmp["Troops"] += (102 + 268)
# lvl_table = lvl_table.append(tmp)
#
# #Reborn 3
# tmp = df[df["Level"]<=21]
# tmp = tmp.copy(deep=True)
# tmp["Reborn"]=3
# tmp["Iter"]=tmp["Level"]+16+11+6
# tmp["Might"] += (200+350+600)
# tmp["Troops"] += (102 + 268 + 751)
# lvl_table = lvl_table.append(tmp)
#
# #Reborn 4
# tmp = df[df["Level"]<=26]
# tmp = tmp.copy(deep=True)
# tmp["Reborn"]=4
# tmp["Iter"]=tmp["Level"]+21+16+11+6
# tmp["Might"] += (200+350+600+1200)
# tmp["Troops"] += (102 + 268 + 751 + 1583)
# lvl_table = lvl_table.append(tmp)
#
# #Reborn 5
# tmp = df #[df["Level"]<=26]
# tmp = tmp.copy(deep=True)
# tmp["Reborn"]=5
# tmp["Iter"]=tmp["Level"]+26+21+16+11+6
# tmp["Might"] += (102 + 268 + 751 + 1583 + 1700)
# tmp["Troops"] += (102 + 268 + 751 + 1583 + 2957)
# lvl_table = lvl_table.append(tmp)
#
# lvl_table = lvl_table[ ["Iter", "Reborn", "Level", "Might","Troops","Gold","Souls"]]
# pd.set_option('max_rows', 99999)
# lvl_table
