import csv
from itertools import zip_longest

def make_combined_csv(file_name = './results/res.csv'):

    with open('./results/fusion_results.csv', mode='r') as f_file:
        with open('./results/bl_res.csv', mode='r') as bl_file:
            with open('./results/sprase_bl_summary.csv', mode='r') as sparse_bl_file:
                bl_reader = csv.reader(bl_file)
                sparse_bl_reader = csv.reader(sparse_bl_file)
                f_reader = csv.reader(f_file)
                with open(file_name, 'w', newline='') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

                    bl_pw1_e = 0.0
                    bl_pw2_e = 0.0
                    bl_dw_e = 0.0

                    bl_pw1_c = 0
                    bl_pw2_c = 0
                    bl_dw_c = 0

                    sp_bl_pw1_e = 0
                    sp_bl_pw2_e = 0
                    sp_bl_dw_e = 0

                    sp_bl_pw1_c = 0
                    sp_bl_pw2_c = 0
                    sp_bl_dw_c = 0

                    f_pred1_e = 0.0
                    f_pred2_e = 0.0
                    f_main_e = 0.0
                    f_overhead_e = 0.0

                    f_pred1_c = 0.0
                    f_pred2_c = 0.0
                    f_main_c = 0.0

                    i = 0

                    for f_row, bl_row, sparse_bl_row in zip_longest(f_reader, bl_reader, sparse_bl_reader, fillvalue=['0']*7):
                        if i == 0:
                            wr.writerow(["block"] + bl_row + sparse_bl_row+ f_row)
                        else:
                            wr.writerow([str(i)] + bl_row + sparse_bl_row + f_row)

                            bl_pw1_e += float(bl_row[0])
                            bl_dw_e += float(bl_row[1])
                            bl_pw2_e  += float(bl_row[2])

                            bl_pw1_c += int(bl_row[3])
                            bl_dw_c += int(bl_row[4])
                            bl_pw2_c  += int(bl_row[5])

                            sp_bl_pw1_e += float(sparse_bl_row[0])
                            sp_bl_pw2_e += float(sparse_bl_row[2])
                            sp_bl_dw_e  += float(sparse_bl_row[1])

                            sp_bl_pw1_c += int(sparse_bl_row[3])
                            sp_bl_pw2_c += int(sparse_bl_row[4])
                            sp_bl_dw_c += int(sparse_bl_row[5])

                            f_pred1_e += float(f_row[0])
                            f_pred2_e += float(f_row[1])
                            f_main_e += float(f_row[2])
                            f_overhead_e += float(f_row[3])

                            f_pred1_c += int(f_row[4])
                            f_pred2_c += int(f_row[5])
                            f_main_c += int(f_row[6])
                        i += 1
                    wr.writerow(["total", str(bl_pw1_e), str(bl_dw_e), str(bl_pw2_e), str(bl_pw1_c), str(bl_dw_c), str(bl_pw2_c),\
                                 str(sp_bl_pw1_e), str(sp_bl_dw_e), str(sp_bl_pw2_e), str(sp_bl_pw1_c), str(sp_bl_dw_c), str(sp_bl_pw2_c), str(f_pred1_e),\
                                 str(f_pred2_e), str(f_main_e), str(f_overhead_e), str(f_pred1_c), str(f_pred2_c), str(f_main_c)])

                    bl_c = bl_pw1_c + bl_pw2_c + bl_dw_c
                    bl_e = bl_pw1_e + bl_pw2_e + bl_dw_e

                    sp_bl_c = sp_bl_pw1_c + sp_bl_pw2_c + sp_bl_dw_c
                    sp_bl_e = sp_bl_pw1_e + sp_bl_pw2_e + sp_bl_dw_e

                    f_c = f_pred1_c + f_pred2_c + f_main_c
                    f_e = f_pred1_e + f_pred2_e +f_main_e +f_overhead_e

                    wr.writerow([""]*20)
                    wr.writerow([""]*20)
                    wr.writerow(["", "cycles", "speedup", "", "energy", "speedup"])
                    wr.writerow(["fusion", str(f_c), str(f_c/f_c), "", str(f_e), str(f_e/f_e)])
                    wr.writerow(["sparse", str(sp_bl_c), str(sp_bl_c/f_c), "", str(sp_bl_e), str(sp_bl_e/f_e)])
                    wr.writerow(["dense", str(bl_c), str(bl_c/f_c), "", str(bl_e), str(bl_e/f_e)])

