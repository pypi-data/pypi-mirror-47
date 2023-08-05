# strsql
#
# ===> select * from QIWS/QCUSTCDT where LSTNAM='Jones' or LSTNAM='Vine'
#   
#                                  Display Data    
#                                              Data width . . . . . . :     102
# Position to line  . . . . .              Shift to column  . . . . . .        
# ....+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....
#  CUSNUM   LSTNAM    INIT  STREET         CITY    STATE  ZIPCOD   CDTLMT   CHGCO
# 839,283   Jones     B D   21B NW 135 St  Clay     NY    13,041      400      1
# 392,859   Vine      S S   PO Box 79      Broton   VT     5,046      700      1
# ********  End of data  ********
import config
from itoolkit import *

itool = iToolKit()
itool.add(iSqlPrepare('cust2prep', "select * from QIWS/QCUSTCDT where LSTNAM=? or LSTNAM=?"))
itool.add(
 iSqlExecute('cust2exec')
 .addParm(iSqlParm('pm1','Jones'))
 .addParm(iSqlParm('pm2','Vine'))
)
itool.add(iSqlFetch('cust2fetch'))
itool.add(iSqlFree('cust2free'))

# xmlservice
itool.call(config.itransport)

# output
QCUSTCDT = itool.dict_out('cust2fetch')
# print(QCUSTCDT)
if 'error' in QCUSTCDT:
  print (QCUSTCDT['error'])
  exit()
else:
  for row in QCUSTCDT['row']:
    print('row:')
    print(' CDTDUE :' + row['CDTDUE'])
    print(' CDTLMT :' + row['CDTLMT'])
    print(' CUSNUM :' + row['CUSNUM'])
    print(' CHGCOD :' + row['CHGCOD'])
    print(' STREET :' + row['STREET'])
    print(' INIT   :' + row['INIT'])
    print(' BALDUE :' + row['BALDUE'])
    print(' LSTNAM :' + row['LSTNAM'])
    print(' ZIPCOD :' + row['ZIPCOD'])
    print(' CITY   :' + row['CITY'])
    print(' STATE  :' + row['STATE'])

