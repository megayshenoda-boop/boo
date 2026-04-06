# Soldiers, Heroes, Chat, and Sync Decoding

Total packets: 3709

============================================================
SOLDIER_INFO (0x06C2) - All Occurrences
============================================================
  Found 14 0x06C2 packets

  Packet 1: len=112, count=4, remaining=108, entry_size=27
    Entry 1 (27B): 010000000200f828000000000000020000000200301c0000000000
      [27B] type=1, f1=2, f2=10488, f3=0, f4=131072, f5=131072, f6=7216, f7=0, f8=0
    Entry 2 (27B): 00040000000100a83f000000000000080000000100ce4100000000
      [27B] type=1024, f1=256, f2=43008, f3=63, f4=134217728, f5=16777216, f6=52736, f7=65, f8=0
    Entry 3 (27B): 000004000000010000007c0e0000020000005317000004000000bc
      [27B] type=262144, f1=0, f2=1, f3=243007488, f4=131072, f5=391315456, f6=0, f7=4, f8=188
    Entry 4 (27B): 0b000008000000580b000000000000000000000000000000000000
      [27B] type=134217739, f1=0, f2=22528, f3=11, f4=0, f5=0, f6=0, f7=0, f8=0

  Packet 2: len=112, count=4, remaining=108, entry_size=27
    Entry 1 (27B): 010000000200001c000000000000020000000200ca0e0000000000
      [27B] type=1, f1=2, f2=7168, f3=0, f4=131072, f5=131072, f6=3786, f7=0, f8=0
    Entry 2 (27B): 00040000000100a83f000000000000080000000100ce4100000000
      [27B] type=1024, f1=256, f2=43008, f3=63, f4=134217728, f5=16777216, f6=52736, f7=65, f8=0
    Entry 3 (27B): 000004000000010000007c0e0000020000005317000004000000bc
      [27B] type=262144, f1=0, f2=1, f3=243007488, f4=131072, f5=391315456, f6=0, f7=4, f8=188
    Entry 4 (27B): 0b000008000000580b000000000000000000000000000000000000
      [27B] type=134217739, f1=0, f2=22528, f3=11, f4=0, f5=0, f6=0, f7=0, f8=0

  Packet 3: len=112, count=4, remaining=108, entry_size=27
    Entry 1 (27B): 010000000200f828000000000000020000000200301c0000000000
      [27B] type=1, f1=2, f2=10488, f3=0, f4=131072, f5=131072, f6=7216, f7=0, f8=0
    Entry 2 (27B): 00040000000100a83f000000000000080000000100ce4100000000
      [27B] type=1024, f1=256, f2=43008, f3=63, f4=134217728, f5=16777216, f6=52736, f7=65, f8=0
    Entry 3 (27B): 000004000000010000007c0e0000020000005317000004000000bc
      [27B] type=262144, f1=0, f2=1, f3=243007488, f4=131072, f5=391315456, f6=0, f7=4, f8=188
    Entry 4 (27B): 0b000008000000580b000000000000000000000000000000000000
      [27B] type=134217739, f1=0, f2=22528, f3=11, f4=0, f5=0, f6=0, f7=0, f8=0

  Packet 4: len=112, count=4, remaining=108, entry_size=27
    Entry 1 (27B): 010000000200f828000000000000020000000200301c0000000000
      [27B] type=1, f1=2, f2=10488, f3=0, f4=131072, f5=131072, f6=7216, f7=0, f8=0
    Entry 2 (27B): 00040000000100a83f000000000000080000000100ce4100000000
      [27B] type=1024, f1=256, f2=43008, f3=63, f4=134217728, f5=16777216, f6=52736, f7=65, f8=0
    Entry 3 (27B): 000004000000010000007c0e0000020000005317000004000000bc
      [27B] type=262144, f1=0, f2=1, f3=243007488, f4=131072, f5=391315456, f6=0, f7=4, f8=188
    Entry 4 (27B): 0b000008000000580b000000000000000000000000000000000000
      [27B] type=134217739, f1=0, f2=22528, f3=11, f4=0, f5=0, f6=0, f7=0, f8=0

  Packet 5: len=112, count=4, remaining=108, entry_size=27
    Entry 1 (27B): 010000000500550b00000000000002000000050093621400000000
      [27B] type=1, f1=5, f2=2901, f3=0, f4=131072, f5=327680, f6=25235, f7=20, f8=0
    Entry 2 (27B): 0004000000050090c313000000000008000000050035b605000000
      [27B] type=1024, f1=1280, f2=36864, f3=5059, f4=134217728, f5=83886080, f6=13568, f7=1462, f8=0
    Entry 3 (27B): 00000400000001000000744301000200000040f300000400000040
      [27B] type=262144, f1=0, f2=1, f3=1131675648, f4=131073, f5=4081057792, f6=0, f7=4, f8=64
    Entry 4 (27B): 6c010008000000c99a010000000000000000000000000000000000
      [27B] type=134218092, f1=0, f2=51456, f3=410, f4=0, f5=0, f6=0, f7=0, f8=0


============================================================
HERO_INFO (0x00AA) - Detailed Field Mapping
============================================================
  Found 15 0x00AA packets

  Packet 1: len=549, heroes=5, entry_size=109

    Hero 1 (id=201):
      Non-zero u32 fields:
        [  0]:        201 (0x000000C9)
        [  4]:         29 (0x0000001D)
        [  8]:     429313 (0x00068D01)
        [ 12]:        256 (0x00000100)
        [ 20]:   78708736 (0x04B10000)
        [ 24]:     131072 (0x00020000)
        [ 32]:      65536 (0x00010000)
        [ 36]:      65536 (0x00010000)
        [ 48]:      65536 (0x00010000)
        [ 56]:          1 (0x00000001)
        [ 84]:        206 (0x000000CE)
        [ 88]:         24 (0x00000018)
        [ 92]:    1906176 (0x001D1600)
        [ 96]:        256 (0x00000100)
        [104]:   79036416 (0x04B60000)
      hero_id=201, level_or_exp=29, star_or_flag=1
      field4=1677, field5=1, field6=0

    Hero 2 (id=512):
      Non-zero u32 fields:
        [  0]:        512 (0x00000200)
        [  8]:        256 (0x00000100)
        [ 12]:        256 (0x00000100)
        [ 24]:        256 (0x00000100)
        [ 28]:   16777216 (0x01000000)
        [ 56]: 3556769792 (0xD4000000)
        [ 60]:  335544320 (0x14000000)
        [ 68]:       4005 (0x00000FA5)
        [ 72]:          1 (0x00000001)
        [ 80]:     310272 (0x0004BC00)
        [ 84]:        512 (0x00000200)
        [ 92]:        256 (0x00000100)
        [ 96]:        256 (0x00000100)
      hero_id=512, level_or_exp=0, star_or_flag=0
      field4=1, field5=1, field6=0

    Hero 3 (id=1):
      Non-zero u32 fields:
        [  0]:          1 (0x00000001)
        [  4]:      65536 (0x00010000)
        [ 32]:   14155776 (0x00D80000)
        [ 36]:    1507328 (0x00170000)
        [ 40]: 2801795072 (0xA7000000)
        [ 44]:   16777245 (0x0100001D)
        [ 56]:       1216 (0x000004C0)
        [ 60]:          1 (0x00000001)
        [ 68]:          1 (0x00000001)
        [ 84]:          1 (0x00000001)
        [ 88]:      65536 (0x00010000)
      hero_id=1, level_or_exp=65536, star_or_flag=0
      field4=0, field5=0, field6=0

    Hero 4 (id=0):
      Non-zero u32 fields:
        [  8]:      57344 (0x0000E000)
        [ 12]:       5632 (0x00001600)
        [ 16]:  491978752 (0x1D530000)
        [ 20]:      65536 (0x00010000)
        [ 28]: 3355443200 (0xC8000000)
        [ 32]:   16777220 (0x01000004)
        [ 40]:   16777216 (0x01000000)
        [ 56]:   16777216 (0x01000000)
        [ 64]:        256 (0x00000100)
      hero_id=0, level_or_exp=0, star_or_flag=0
      field4=224, field5=22, field6=1921792

    Hero 5 (id=0):
      Non-zero u32 fields:
      hero_id=0, level_or_exp=0, star_or_flag=0
      field4=0, field5=0, field6=0

  Packet 2: len=222, heroes=2, entry_size=109

    Hero 1 (id=201):
      Non-zero u32 fields:
        [  0]:        201 (0x000000C9)
        [  4]:         29 (0x0000001D)
        [  8]:     429313 (0x00068D01)
        [ 12]:        256 (0x00000100)
        [ 20]:   78708736 (0x04B10000)
        [ 24]:     131072 (0x00020000)
        [ 28]:  249036800 (0x0ED80000)
        [ 32]:      65536 (0x00010000)
        [ 36]:      65536 (0x00010000)
        [ 48]:      65536 (0x00010000)
        [ 56]:          1 (0x00000001)
        [ 84]:        206 (0x000000CE)
        [ 88]:         24 (0x00000018)
        [ 92]:    1906176 (0x001D1600)
        [ 96]:        256 (0x00000100)
        [104]:   79036416 (0x04B60000)
      hero_id=201, level_or_exp=29, star_or_flag=1
      field4=1677, field5=1, field6=0

    Hero 2 (id=512):
      Non-zero u32 fields:
        [  0]:        512 (0x00000200)
        [  4]:     878080 (0x000D6600)
        [  8]:        256 (0x00000100)
        [ 12]:        256 (0x00000100)
        [ 24]:        256 (0x00000100)
        [ 28]:   16777216 (0x01000000)
      hero_id=512, level_or_exp=878080, star_or_flag=0
      field4=1, field5=1, field6=0

  Packet 3: len=549, heroes=5, entry_size=109

    Hero 1 (id=201):
      Non-zero u32 fields:
        [  0]:        201 (0x000000C9)
        [  4]:         29 (0x0000001D)
        [  8]:     429313 (0x00068D01)
        [ 12]:        256 (0x00000100)
        [ 20]:   78708736 (0x04B10000)
        [ 24]:     131072 (0x00020000)
        [ 32]:      65536 (0x00010000)
        [ 36]:      65536 (0x00010000)
        [ 48]:      65536 (0x00010000)
        [ 56]:          1 (0x00000001)
        [ 84]:        206 (0x000000CE)
        [ 88]:         24 (0x00000018)
        [ 92]:    1906176 (0x001D1600)
        [ 96]:        256 (0x00000100)
        [104]:   79036416 (0x04B60000)
      hero_id=201, level_or_exp=29, star_or_flag=1
      field4=1677, field5=1, field6=0

    Hero 2 (id=512):
      Non-zero u32 fields:
        [  0]:        512 (0x00000200)
        [  8]:        256 (0x00000100)
        [ 12]:        256 (0x00000100)
        [ 24]:        256 (0x00000100)
        [ 28]:   16777216 (0x01000000)
        [ 56]: 3556769792 (0xD4000000)
        [ 60]:  335544320 (0x14000000)
        [ 68]:       4005 (0x00000FA5)
        [ 72]:          1 (0x00000001)
        [ 80]:     310272 (0x0004BC00)
        [ 84]:        512 (0x00000200)
        [ 92]:        256 (0x00000100)
        [ 96]:        256 (0x00000100)
      hero_id=512, level_or_exp=0, star_or_flag=0
      field4=1, field5=1, field6=0

    Hero 3 (id=1):
      Non-zero u32 fields:
        [  0]:          1 (0x00000001)
        [  4]:      65536 (0x00010000)
        [ 32]:   14155776 (0x00D80000)
        [ 36]:    1507328 (0x00170000)
        [ 40]: 2801795072 (0xA7000000)
        [ 44]:   16777245 (0x0100001D)
        [ 56]:       1216 (0x000004C0)
        [ 60]:          1 (0x00000001)
        [ 68]:          1 (0x00000001)
        [ 84]:          1 (0x00000001)
        [ 88]:      65536 (0x00010000)
      hero_id=1, level_or_exp=65536, star_or_flag=0
      field4=0, field5=0, field6=0

    Hero 4 (id=0):
      Non-zero u32 fields:
        [  8]:      57344 (0x0000E000)
        [ 12]:       5632 (0x00001600)
        [ 16]:  491978752 (0x1D530000)
        [ 20]:      65536 (0x00010000)
        [ 28]: 3355443200 (0xC8000000)
        [ 32]:   16777220 (0x01000004)
        [ 40]:   16777216 (0x01000000)
        [ 56]:   16777216 (0x01000000)
        [ 64]:        256 (0x00000100)
      hero_id=0, level_or_exp=0, star_or_flag=0
      field4=224, field5=22, field6=1921792

    Hero 5 (id=0):
      Non-zero u32 fields:
      hero_id=0, level_or_exp=0, star_or_flag=0
      field4=0, field5=0, field6=0


============================================================
CHAT_HISTORY (0x026D) - Message Decoding
============================================================
  Found 144 chat packets

  First 30 bytes of each (looking for header structure):
  [1] len=1592: 0a00d300e0b2dc2b238cee02f271de7d0000000000000000000000000102
  [2] len=1372: 0a00ae0078c9e22b238cee027848da40000000000000000000000000013d
  [3] len=1366: 0a000e00c8dfea2b238cee02ae12da3c0000000000000000000000000133
  [4] len=1864: 0a00740060f0f12b238cee02a643373400000000000000000000000001a5
  [5] len=1884: 0a00d4001092f52b238cee02c5a6263200000000000000000000000001f7
  [6] len= 132: 010054008878f62b238cee02c136fd4a0000000000000000000000000121
  [7] len= 152: 01007600707cf62b238cee02106a5f2e0000000000000000000000000129
  [8] len= 243: 01002a0058fdf62b238cee023585651f0000000000000000000000000183
  [9] len= 158: 01007e005128f72b238cee02070ed376000000000000000000000000012f
  [10] len= 118: 0100d30058f7f72b238cee02f912f0380000000000000000000000000105

  Header analysis:
  [1] channel=10, count/id=0x00D3, v1=0x2BDCB2E0, v2=0x02EE8C23
  [2] channel=10, count/id=0x00AE, v1=0x2BE2C978, v2=0x02EE8C23
  [3] channel=10, count/id=0x000E, v1=0x2BEADFC8, v2=0x02EE8C23
  [4] channel=10, count/id=0x0074, v1=0x2BF1F060, v2=0x02EE8C23
  [5] channel=10, count/id=0x00D4, v1=0x2BF59210, v2=0x02EE8C23
  [6] channel=1, count/id=0x0054, v1=0x2BF67888, v2=0x02EE8C23
  [7] channel=1, count/id=0x0076, v1=0x2BF67C70, v2=0x02EE8C23
  [8] channel=1, count/id=0x002A, v1=0x2BF6FD58, v2=0x02EE8C23
  [9] channel=1, count/id=0x007E, v1=0x2BF72851, v2=0x02EE8C23
  [10] channel=1, count/id=0x00D3, v1=0x2BF7F758, v2=0x02EE8C23

  Searching for readable text in chat payloads:

  Chat 1 (len=1592):
    [  71] "yfy"
    [ 147] " I-"
    [ 380] "054#"
    [ 399] "VW;"
    [ 417] "[chat_face]_46"
    [ 518] "   "
    [ 559] "   "
    [ 650] "snkX"
    [ 899] "*M|"
    [ 917] "toplamda 1 ki"
    [ 932] "i 5 defa ya"
    [ 945] "malasa 50-60 bin inci ya"
    [ 971] "mal"
    [ 976] "yor . ancak serginin yar"
    [1005] " bo"
    [1010] "a gidiyor. nerdeyse 900 bin i"
    [1041] "inden 50-60 bin civar"
    [1064] " inci al"
    [1077] "yorg,"
    [1103] "zagor4155"
    [1114] "cLc"
    [1151] "T7N "
    [1182] "BedirhanY"
    [1197] "BS5"
    [1234] "[chat_face]_61@,"
    [1293] "T7N7"
    [  27] UTF-8:   ٕ\-i                 روان 🎩 yfy    h+#{Z         

  Chat 2 (len=1372):
    [ 115] "Haya"
    [ 127] "F5Wq"
    [ 249] "MAXC"
    [ 351] "ONEb"
    [ 370] "Tbx"
    [ 388] "[chat_face]_46"
    [ 447] "cLc"
    [ 648] "TyMH"
    [ 685] "[chat_face]_46"
    [ 722] "shosho"
    [ 770] "[chat_face]_48"
    [ 829] "300/"
    [ 848] "H)|"
    [ 866] "[chat_face]_02x-"
    [ 920] "Cl2X"
    [1073] "Dmr3"
    [  27] UTF-8:  = مصرية صاحية تجي ندردش بدل لمللل💔K.i                
 Ha

  Chat 3 (len=1366):
    [  31] "o y"
    [  36] "zden a"
    [  44] "ktan me"
    [  53] "kten rabbim bizi korusun "
    [ 105] "IM PALAA"
    [ 123] "H7KL"
    [ 160] "[chat_face]_10P/"
    [ 210] "FZ3d"
    [ 295] "   "
    [ 322] "   "
    [ 379] "snkX"
    [ 416] "sevenin hali harap bo"
    [ 439] "una harap olmay"
    [ 456] "n derim"
    [ 486] "IM PALAA"
    [ 504] "H7KL"
    [ 523] "H)|"
    [ 582] "Cl2X"
    [ 658] "Cl2"
    [ 748] "R5K4"
    [ 876] "TyMH"
    [ 976] "MAXC"
    [ 995] "H)|"
    [1013] "[chat_face]_02U."
    [1067] "Cl2X"
    [1246] "sm>"
    [1309] "NkI"
    [ 193] UTF-8:    حلا 🥰 FZ3d   +#Wm            X معقوله  ماكو  عرا

  Chat 4 (len=1864):
    [  13] "C74"
    [ 130] " G Tshling Wok Kathithk Ksisk Abu Wajh Murba' Bakhil. Bamako, Mali"
    [ 236] "iRl"
    [ 309] "30 "
    [ 332] " 2."
    [ 343] " 30 "
    [ 412] " 3 "
    [ 468] " 3 "
    [ 515] " 360$"
    [ 564] "T7Ng"
    [ 601] "[chat_face]_19Z0"
    [ 659] "saw "
    [ 762] "SHMb"
    [ 942] "queen"
    [ 969] "C74"
    [ 987] "G. Tishling Wook, Kthithk Ksisk, ek wil asseblief 'n Brasiliaanse bankrekening h"
    [1111] "iRl"
    [1148] "[chat_face]_68"
    [1207] "300/"
    [1244] "derleeeerrr yapmasan da yapt"
    [1274] " derleeerrr"
    [1308] "BedirhanY"
    [1323] "BS5"
    [1360] "assuming no normal ppl are still playin this  **** except for those h0rny guys "
    [1482] "SNK"
    [1550] "BedirhanY"
    [1565] "BS5"
    [1744] "8UD"
    [  27] UTF-8:   ممكن طلب اريد فلوس عيديه دزو لي فلوس للزين كاش من فضل

  Chat 5 (len=1884):
    [  67] "30 "
    [  90] " 2."
    [ 101] " 30 "
    [ 170] " 3 "
    [ 226] " 3 "
    [ 273] " 360$:1"
    [ 322] "T7Ng"
    [ 414] "GAG/"
    [ 640] "BRIT"
    [ 783] "SHMb"
    [ 873] "GAG/"
    [1031] " ----- For sale "
    [1070] "Diss"
    [1084] "DMRh"
    [1153] "     "
    [1166] "   "
    [1233] "snkX"
    [1270] "T7N"
    [1279] "TMT"
    [1309] "BedirhanY"
    [1329] "T7N"
    [1347] ",]Q="
    [1579] "H..."
    [1585] "T7NH"
    [1755] "8UD"
    [  29] UTF-8:  3 قلاع للبيـع قلعتين30 و قلعه هيبه 2.قلعه 30 فيها بطلين م 


============================================================
SYN_ATTRIBUTE (0x0033) - Resource Sync Messages
============================================================
  Found 52 SYN_ATTRIBUTE packets
  Size range: 16-16 bytes
  Most common sizes:
      16 bytes:  52x

  First 10 packets:
  [1] len= 16: 03000000530f02000000000000000000
    count(u16)=3
      attr=0x0000, val=134995
  [2] len= 16: 03000000fab202000000000000000000
    count(u16)=3
      attr=0x0000, val=176890
  [3] len= 16: 0300000032b202000000000000000000
    count(u16)=3
      attr=0x0000, val=176690
  [4] len= 16: 040000005e8c02000000000000000000
    count(u16)=4
      attr=0x0000, val=167006
  [5] len= 16: 350000008eff05000000000002000000
    count(u16)=53
      attr=0x0000, val=393102
  [6] len= 16: 33000000720e00000000000000000000
    count(u16)=51
      attr=0x0000, val=3698
  [7] len= 16: 030000006ab102000000000000000000
    count(u16)=3
      attr=0x0000, val=176490
  [8] len= 16: 040000006a8a02000000000000000000
    count(u16)=4
      attr=0x0000, val=166506
  [9] len= 16: 35000000a2ff05000000000002000000
    count(u16)=53
      attr=0x0000, val=393122
  [10] len= 16: 33000000860e00000000000000000000
    count(u16)=51
      attr=0x0000, val=3718


============================================================
SERVER_TIME (0x0043)
============================================================
  Found 30 packets
  [1] len=16: 022b0000000000000000000000000000
    timestamp_u64: 11010
    timestamp_u32: 11010
    as unix time: 1970-01-01 03:03:30
  [2] len=16: 333e0000000000000000000000000000
    timestamp_u64: 15923
    timestamp_u32: 15923
    as unix time: 1970-01-01 04:25:23
  [3] len=16: dc880200000000000000000000000000
    timestamp_u64: 166108
    timestamp_u32: 166108
    as unix time: 1970-01-02 22:08:28
  [4] len=16: 022b0000000000004c31b76900000000
    timestamp_u64: 11010
    timestamp_u32: 11010
    as unix time: 1970-01-01 03:03:30
  [5] len=16: 333e0000000000005131b76900000000
    timestamp_u64: 15923
    timestamp_u32: 15923
    as unix time: 1970-01-01 04:25:23


============================================================
0x0037 UNKNOWN - Error/Status?
============================================================
  Found 7 0x0037 packets
  [1] len=12: 2b000000e96a170000000000
    u32[0]: 43 (0x0000002B)
    u32[4]: 1534697 (0x00176AE9)
  [2] len=12: 2b000000900e180000000000
    u32[0]: 43 (0x0000002B)
    u32[4]: 1576592 (0x00180E90)
  [3] len=12: 0d000000d320000000000000
    u32[0]: 13 (0x0000000D)
    u32[4]: 8403 (0x000020D3)
  [4] len=12: 160000007319c36900000000
    u32[0]: 22 (0x00000016)
    u32[4]: 1774393715 (0x69C31973)
  [5] len=12: 160000004b1fc36900000000
    u32[0]: 22 (0x00000016)
    u32[4]: 1774395211 (0x69C31F4B)
  [6] len=12: 160000008440c76900000000
    u32[0]: 22 (0x00000016)
    u32[4]: 1774665860 (0x69C74084)
  [7] len=12: 160000001a95c86900000000
    u32[0]: 22 (0x00000016)
    u32[4]: 1774753050 (0x69C8951A)


============================================================
0x00B8 - March ACK?
============================================================
  Found 16 0x00B8 packets
  [1] len=1 src=7000: 00
  [2] len=14 src=7000: 010100000002c9000000ce000000
  [3] len=1 src=7000: 00
  [4] len=1 src=7000: 00
  [5] len=1 src=7001: 00
  [6] len=10 src=7001: 010100000001ff000000
  [7] len=1 src=7001: 00
  [8] len=10 src=7001: 010100000001ff000000
  [9] len=1 src=7001: 00
  [10] len=10 src=7001: 010100000001ff000000


============================================================
March-Related Opcodes Search
============================================================

  0x0071: 7 packets
    [1] len=70 src=7000: 48ae0d00d30000000100c9aa1e7c0000000001700100002f015101320153
    [2] len=70 src=7001: e1620900b60000000100ed0273220000000001b003000043023e03260253
    [3] len=70 src=7001: 34630900b60000000100ed0273220000000001b003000043023e03530255

  0x0070: 13 packets
    [1] len=9 src=7000: 48ae0d00d300000000
    [2] len=9 src=7001: e1620900b600000000
    [3] len=9 src=7001: e1620900b600000000

  0x00B8: 16 packets
    [1] len=1 src=7000: 00
    [2] len=14 src=7000: 010100000002c9000000ce000000
    [3] len=1 src=7000: 00

  0x00B9: 1 packets
    [1] len=4 src=7001: 01000000

  0x0CE8: 6 packets
    [1] len=54 src=59224: 4c55e2b23630a2a2aaca8b580daf727b4533f760cecf3e2b8282d9a37856
    [2] len=50 src=53956: cf41f64ac3493e68dfe16e07f8789604b6cfd83f3b345b747779e5fc8dad
    [3] len=50 src=54894: 11f84fba472ee82e2b7791017e23692036992939bd62a472f12f1afa0bfb


============================================================
Full Opcode Coverage in PCAPs
============================================================

  Top 60 opcodes by frequency:
    0x026D (CMSG_CHAT_HISTORY                            ):  144x
    0x0042 (UNKNOWN                                      ):  136x <-- UNMAPPED
    0x0003 (UNKNOWN                                      ):   90x <-- UNMAPPED
    0x0001 (UNKNOWN                                      ):   82x <-- UNMAPPED
    0x099D (CMSG_COMMON_EXCHAGE_COUNT_REQUEST            ):   58x
    0x099E (CMSG_COMMON_EXCHAGE_COUNT_RETURN             ):   58x
    0x0033 (CMSG_SYN_ATTRIBUTE_CHANGE                    ):   52x
    0x036C (UNKNOWN                                      ):   41x <-- UNMAPPED
    0x0403 (UNKNOWN                                      ):   35x <-- UNMAPPED
    0x0078 (UNKNOWN                                      ):   32x <-- UNMAPPED
    0x0043 (CMSG_SYN_SERVER_TIME                         ):   30x
    0x1B16 (CMSG_CLANPK_QUERY_DEFEND_INFO                ):   26x
    0x0601 (UNKNOWN                                      ):   26x <-- UNMAPPED
    0x0077 (UNKNOWN                                      ):   25x <-- UNMAPPED
    0x007A (UNKNOWN                                      ):   25x <-- UNMAPPED
    0x2B08 (UNKNOWN                                      ):   24x <-- UNMAPPED
    0x11F8 (UNKNOWN                                      ):   23x <-- UNMAPPED
    0x007B (CMSG_NOTIFY_OWNER_CASTLE                     ):   20x
    0x0085 (UNKNOWN                                      ):   20x <-- UNMAPPED
    0x06EB (UNKNOWN                                      ):   20x <-- UNMAPPED
    0x0076 (UNKNOWN                                      ):   20x <-- UNMAPPED
    0x0064 (CMSG_ITEM_INFO                               ):   18x
    0x020D (UNKNOWN                                      ):   17x <-- UNMAPPED
    0x01E7 (UNKNOWN                                      ):   17x <-- UNMAPPED
    0x006E (UNKNOWN                                      ):   16x <-- UNMAPPED
    0x00B8 (UNKNOWN                                      ):   16x <-- UNMAPPED
    0x0098 (UNKNOWN                                      ):   16x <-- UNMAPPED
    0x00AA (CMSG_HERO_INFO                               ):   15x
    0x009E (CMSG_BUILDING_OPERAT_RETURN                  ):   15x
    0x06C2 (UNKNOWN                                      ):   14x <-- UNMAPPED
    0x076C (UNKNOWN                                      ):   14x <-- UNMAPPED
    0x0091 (UNKNOWN                                      ):   14x <-- UNMAPPED
    0x0AF3 (CMSG_REWARD_POINT_SHOP_ITEM_INFO_RETURN      ):   13x
    0x0070 (UNKNOWN                                      ):   13x <-- UNMAPPED
    0x009D (UNKNOWN                                      ):   12x <-- UNMAPPED
    0x0211 (UNKNOWN                                      ):   12x <-- UNMAPPED
    0x07C8 (CMSG_SYNC_MOBILIZATION_TASK_REFRESH          ):   12x
    0x0701 (UNKNOWN                                      ):   11x <-- UNMAPPED
    0x0640 (UNKNOWN                                      ):   11x <-- UNMAPPED
    0x0080 (UNKNOWN                                      ):   11x <-- UNMAPPED
    0x0082 (UNKNOWN                                      ):   11x <-- UNMAPPED
    0x0840 (CMSG_WORLD_BATTLE_ACTION_REQUEST             ):   10x
    0x0709 (UNKNOWN                                      ):   10x <-- UNMAPPED
    0x0767 (UNKNOWN                                      ):   10x <-- UNMAPPED
    0x0769 (UNKNOWN                                      ):   10x <-- UNMAPPED
    0x0CEB (CMSG_ENABLE_VIEW_NEW                         ):   10x
    0x039B (CMSG_SYNC_LUCKY_TURNTABLE_INFO               ):   10x
    0x0654 (CMSG_AF_INFO                                 ):   10x
    0x004A (CMSG_SYN_VERSION_CONTROL                     ):   10x
    0x0034 (UNKNOWN                                      ):   10x <-- UNMAPPED
    0x01D4 (CMSG_SYN_CITYDEFENSE_FIRE                    ):   10x
    0x0A00 (CMSG_SYNC_CHAMPIONSHIP_CONFIG                ):   10x
    0x0A0A (CMSG_SYNC_CHAMPIONSHIP_BOX_ID                ):   10x
    0x0A0B (CMSG_SYNC_CHAMPIONSHIP_BANNER_ID             ):   10x
    0x0A02 (CMSG_SYN_ALL_QUEST_CHAMPIONSHIP              ):   10x
    0x07E4 (CMSG_SYS_LEAGUE_BATTLEFIELD_INFO             ):   10x
    0x0C4E (CMSG_SYNC_LEAGUE_BATTLEFIELD_CONFIG          ):   10x
    0x084E (CMSG_WORLD_BATTLEFIELD_SYS_INFO              ):   10x
    0x083F (CMSG_SYNC_WORLD_BATTLE_ACTION_CONFIG         ):   10x
    0x0F0A (CMSG_SYS_FORTRESS_INFO                       ):   10x

  Named: 27, Unnamed: 33 (out of top 60)
  Total unique opcodes in PCAPs: 339