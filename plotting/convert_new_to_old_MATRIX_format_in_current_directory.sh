for i in *.dat; do awk '{print $1, $3, $4, $5, $6, $7, $8}'  $i > $i.tmp && mv $i.tmp $i; done
