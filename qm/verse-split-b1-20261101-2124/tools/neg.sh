# QM: exit code of an import-and-build of <variant> for every case, at 390 (NAE_SE=0) and 320 (NAE_SE=1). No pipes on the python call.
v=$1; for c in scratch/cases/*.md; do n=$(basename $c .md); for e in 0 1; do
  if [ $e = 1 ]; then s=320; else s=390; fi
  NAE_PASTE=$PWD/$c NAE_SE=$e python3 -B tools/build.py $v $s scratch/neg-out.json > scratch/neg-stdout.txt 2> scratch/neg-stderr.txt; rc=$?
  echo "$v $n SE=$e exit=$rc :: $(tail -n1 scratch/neg-stderr.txt)"; done; done
