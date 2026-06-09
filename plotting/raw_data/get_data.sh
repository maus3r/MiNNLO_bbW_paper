source ~/.bash_functions

double_scp wieseman@tha310.mpp.mpg.de mwiese@mppui4.t2.rzg.mpg.de /ptmp/mpp/mwiese/NEW-POWHEG-BOX-RES/MiNNLO_res_ptj/bblnu/run_LO+PS_nf6_Q/combined-pwgLHEF_analysis-LO-*.top run_LO_Wp_nf6/

#double_scp wieseman@tha310.mpp.mpg.de mwiese@mppui4.t2.rzg.mpg.de /ptmp/mpp/mwiese/NEW-POWHEG-BOX-RES/MiNNLO_res_ptj/bblnu/run_NLO+PS_nf6_Q/combined-pwgLHEF_analysis-NLO-*.top run_NLO_Wp_nf6/

exit 1

mkdir tmp

double_scp wieseman@tha310.mpp.mpg.de mwiese@mppui4.t2.rzg.mpg.de /ptmp/mpp/mwiese/NEW-POWHEG-BOX-RES/MiNNLO_res_ptj/bblnuJ/run_ptj_Wp_first_MiNNLO_reweight_2loop/combined-*MiN*LO-kQ*-???.top ./tmp/

mv tmp/combined-*MiN*LO-kQ05*-???.top   run_MiNNLOptj_Wp_nf6_kQ05_2loop_soft/

mv tmp/combined-*MiN*LO-kQ025*-???.top  run_MiNNLOptj_Wp_nf6_kQ025_2loop_soft/

mv tmp/combined-*MiN*LO-kQ1*-???.top    run_MiNNLOptj_Wp_nf6_kQ1_2loop_soft/

rm -rf tmp


exit 1

double_scp wieseman@tha310.mpp.mpg.de mwiese@mppui4.t2.rzg.mpg.de /ptmp/mpp/mwiese/NEW-POWHEG-BOX-RES/MiNNLO_res_ptj/bblnuJ/run_Wp_first_MiNNLO_reweight_2loopLC/combined-*MiN*LO-kQ*-???.top ./tmp/

mv tmp/combined-*MiN*LO-kQ05*-???.top run_Wp_nf6_kQ05_LC/

mv tmp/combined-*MiN*LO-kQ025*-???.top run_Wp_nf6_kQ025_LC/

mv tmp/combined-*MiN*LO-kQ1*-???.top run_Wp_nf6_kQ1_LC/

rm -rf tmp

exit


double_scp wieseman@tha310.mpp.mpg.de mwiese@mppui4.t2.rzg.mpg.de /ptmp/mpp/mwiese/NEW-POWHEG-BOX-RES/MiNNLO_res_ptj/bblnu/run_NLO+PS_nf6_Q/combined-pwgLHEF_analysis-NLO-*.top run_NLO_Wp_nf6/

mkdir tmp

double_scp wieseman@tha310.mpp.mpg.de mwiese@mppui4.t2.rzg.mpg.de /ptmp/mpp/mwiese/NEW-POWHEG-BOX-RES/MiNNLO_res_ptj/bblnuJ/run_ptj_Wp_first_MiNLO/combined-*MiN*LO-kQ*-???.top ./tmp/

mv tmp/combined-*MiN*LO-kQ05*-???.top   run_MiNNLOptj_Wp_nf6_kQ05/

mv tmp/combined-*MiN*LO-kQ025*-???.top  run_MiNNLOptj_Wp_nf6_kQ025/

mv tmp/combined-*MiN*LO-kQ1*-???.top    run_MiNNLOptj_Wp_nf6_kQ1/

rm -rf tmp

