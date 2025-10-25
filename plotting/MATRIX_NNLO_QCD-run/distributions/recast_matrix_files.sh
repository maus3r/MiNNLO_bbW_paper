cp ../../raw_data/MATRIX_results/result.runs/mWbb/scale.band/*..NNLO.QCD.dat .
rename_make ..NNLO.QCD.dat __MATRIX_NNLO_QCD.dat
rename_make ..NLO.QCD.dat __MATRIX_NLO_QCD.dat
rename_make ..LO.dat __MATRIX_LO.dat

rename_make plot.m_bb__ m_bb__
rename_make plot.pT_ljet1__ pt_j1__
rename_make plot.y_bb__ y_bb__
rename_make plot.m_W__ m_Z__
rename_make plot.pT_ljet2__ pt_j2__
rename_make plot.y_bx__ y_bx__
rename_make plot.m_Wbb__ m_bbZ__
rename_make plot.pT_lp__ pt_em__
rename_make plot.y_lp__ y_em__
rename_make plot.n_jets__ n_light_jets__
rename_make plot.pT_W__ pt_Z__
rename_make plot.y_W__ y_Z__
rename_make plot.pT_b__ pt_b__
rename_make plot.pT_Wbb__ pt_bbZ__
rename_make plot.y_Wbb__ y_bbZ__
rename_make plot.pT_bb__ pt_bb__
rename_make plot.total_rate__ total_rate__
rename_make plot.pT_bx__ pt_bx__
rename_make plot.y_b__ y_b__

for i in *.dat
do
    echo $i
    awk 'BEGIN{}NF=(NF-2)' $i > sav
    mv sav $i
done
