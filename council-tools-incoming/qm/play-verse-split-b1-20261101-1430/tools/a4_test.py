# QM: A4 check. Import <variant> on a PASTE copy where verses.weekly[0] duplicates the rest ref, then call verse(rest ref) under whatever -O level runs this.
import sys, os; sys.dont_write_bytecode = True; sys.argv = ['x']; sys.path.insert(0, os.path.abspath(sys.argv_v if False else os.environ['V']))
import play_v608 as PV
r = PV.verse(PV.PJ['verses']['rest']['ref']); print('verse() returned', type(r).__name__, 'assert active' if __debug__ else 'assert stripped (-O)')
