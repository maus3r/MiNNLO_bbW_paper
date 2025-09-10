
reset
set terminal pdfcairo enhanced dashed dl 1.5 lw 3 font "Helvetica,30" size 7.6, 8
set encoding utf8

## default key features
#set key at graph 1.03,0.97
set key reverse  # put text on right side
set key Left     # left bounded text
set key spacing 1.1
set key samplen 2
## to have a assisting grid of dashed lines
set grid front
## set margins
set lmargin 5
set rmargin 2

## general settings
set key at graph 0.99, 0.95
set xtics 
set xtics add 
set mxtics 
set mytics 10
set logscale y
#set logscale x
set ytic offset 0, 0.1
set format y "10^{\%T}"

set label "d{/Symbol s}/dp_{{/Times-New-Roman=18 T},ℓ^+{/Menlo=30 ν}} [fb]" at graph 0, 1.06
set label "pp{/Symbol �} b~{b}{.75−} ℓ^+{/Menlo=30 ν}\\@LHC 13 TeV" right at graph 1, graph 1.07

set output "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/pt_Z-mbbZ150.pdf"

##############
# main frame #
##############

# origin, size of main frame
set origin 0, 0.48
set size 1, 0.47
set bmargin 0 # set marging to remove space
set tmargin 0 # set margin to remove space
set format x ""

## define line styles
## define line styles
set style line 2 dt (3,3) lc rgb "black" lw 1
set style line 3 dt (7,4) lc rgb "red" lw 1
set style line 1 lt 4 lc rgb "blue" lw 1
set style line 4 dt (10,3,3,3) lc rgb "magenta" lw 1
set style line 5 dt (15,2) lc rgb "forest-green" lw 1
set style line 6 dt (8,4,8,4,3,4) lc rgb "forest-green" lw 1
set style line 7 dt (10,3,3,3,3,3) lc rgb "#B8860B" lw 1
set style line 8 lt 1 lc rgb "violet" lw 1
set style line 9 dt (10,3,3,3) lc rgb "brown" lw 1

## for the uncertainty band borders (less thick)
set style line 12 dt (3,3) lc rgb "black" lw 0.1
set style line 13 dt (9,6) lc rgb "red" lw 0.1
set style line 11 dt (15,2) lc rgb "blue" lw 0.1
set style line 14 lt 4 lc rgb "magenta" lw 0.1
set style line 15 dt (20,3,10,3) lc rgb "forest-green" lw 0.1
set style line 16 dt (7,4) lc rgb "forest-green" lw 0.1
set style line 17 dt (10,3,3,3,3,3) lc rgb "#B8860B" lw 0.11
set style line 18 lt 1 lc rgb "violet" lw 0.1
set style line 19 dt (10,3,3,3,3,3) lc rgb "brown" lw 0.1

# set style line 2 dt (3,3) lc rgb "black" lw 1
# set style line 3 dt (7,4) lc rgb "red" lw 1.25
# set style line 1 lt 1 lc rgb "blue" lw 0.75
# set style line 4 dt (10,3,3,3) lc rgb "forest-green" lw 0.75
# set style line 5 lt 5 lc rgb "orange" lw 0.75
# set style line 6 lt 6 lc rgb "magenta" lw 0.75
# ## for the uncertainty band borders (less thick)
# set style line 12 dt (3,3) lc rgb "black" lw 0.1
# set style line 13 dt (9,6) lc rgb "red" lw 0.1
# set style line 11 lt 1 lc rgb "blue" lw 0.1
# set style line 14 dt (10,3,3,3) lc rgb "forest-green" lw 0.1
# set style line 15 lt 5 lc rgb "orange" lw 0.1
# set style line 16 lt 6 lc rgb "magenta" lw 0.1

## define ranges
set xrange [0.0:1000.0]
set yrange [:]

set multiplot
plot "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:2 with lines ls 1 title "MiNNLO (LHE)", "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:4:6 with filledcurves ls 1 fs transparent solid 0.15 notitle, "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:4 with lines ls 11 notitle, "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:6 with lines ls 11 notitle,\
"/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist" using 1:2 with lines ls 2 title "MiNLO (LHE)", "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist" using 1:4:6 with filledcurves ls 2 fs transparent solid 0.15 notitle, "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist" using 1:4 with lines ls 12 notitle, "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist" using 1:6 with lines ls 12 notitle,\
"/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist" using 1:2 with lines ls 5 title "NLO+PS", "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist" using 1:4:6 with filledcurves ls 5 fs transparent solid 0.15 notitle, "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist" using 1:4 with lines ls 15 notitle, "/Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist" using 1:6 with lines ls 15 notitle
###############
# ratio inset #
###############

## remove previous settings
unset label  
#unset key
unset logscale y
unset format

## set ratio inset size
set size 1, 0.32
set origin 0, 0.11

## can be changed
#set logscale y
#set logscale x
set format y 
set key at graph 0.93, 0.95
#set label "ratio to MiNNLO (LHE)" at graph 0, 1.01
set label "d{/Symbol s}/d{/Symbol s}_{MiNNLO (LHE)}" at graph 0, 1.1
set label "m_{b~{b}{.75−} ℓ^+{/Menlo=30 ν}} < 150 GeV" at graph 0.03, 2.5
set label "" at graph 0.65, 2.5
set yrange [0.2:1.6]
set ytics 0.3
set mytics 
set ytic offset 0.4, 0
set xtic offset -0.21,0.4
set xtics 
set xtics add 
set mxtics 
set xlabel offset 0,0.7
set xlabel  "p_{{/Times-New-Roman=18 T},ℓ^+{/Menlo=30 ν}} "
plot "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($2/$9) with lines ls 1 notitle\
, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($4/$9):($6/$9) with filledcurves ls 1 fs transparent solid 0.15 notitle, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($4/$9) with lines ls 11 notitle, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($6/$9) with lines ls 11 notitle,\
"<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($2/$9) with lines ls 2 notitle\
, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($4/$9):($6/$9) with filledcurves ls 2 fs transparent solid 0.15 notitle, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($4/$9) with lines ls 12 notitle, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNLO_Wp_kQ05_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($6/$9) with lines ls 12 notitle,\
"<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($2/$9) with lines ls 5 notitle\
, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($4/$9):($6/$9) with filledcurves ls 5 fs transparent solid 0.15 notitle, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($4/$9) with lines ls 15 notitle, "<paste /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__NLO+PS_NLOPDF_lhef.hist /Users/mars/Uni/Own_Papers/MiNNLO_bbW_paper/plotting/gnuplot_LHEF/histograms/pt_Z-mbbZ150__MiNNLO_Wp_kQ05_lhef.hist" using 1:($6/$9) with lines ls 15 notitle