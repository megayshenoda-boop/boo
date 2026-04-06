# Items Map - IGG Conquerors (الفاتحون)

## Item Use Opcode: 0x0065 (old-style, unencrypted)
```
[0:2]    u16  length
[2:4]    u16  unknown
[4:8]    u32  item_id
[8:12]   u32  count/unknown
```

## Speedup Items (تسريع)
| Item ID | Duration | الوصف | Qty (test) |
|---------|----------|-------|-----------|
| 201 | 1 minute | تسريع ١ دقيقة | 40 |
| 203 | 5 minutes | تسريع ٥ دقائق | 1 |
| 205 | 10 minutes | تسريع ١٠ دقائق | 3 |
| 206 | 15 minutes | تسريع ١٥ دقيقة | 82 |
| 209 | 30 minutes | تسريع ٣٠ دقيقة | 15 |
| 212 | 60 minutes | تسريع ساعة | 3 |
| 213 | 3 hours | تسريع ٣ ساعات | 21 |
| 216 | 8 hours | تسريع ٨ ساعات | 25 |
| 220 | 15 hours | تسريع ١٥ ساعة | 9 |
| 224 | 24 hours | تسريع ٢٤ ساعة | 4 |
| 226 | 3 days | تسريع ٣ أيام | 4 |

## Training Speedup
| Item ID | Description |
|---------|-------------|
| 381 | Training speedup (تسريع تدريب) |

## Resource Packs (حزم الموارد)

### Food (طعام) - 400 series
| Item ID | Amount | Qty (test) |
|---------|--------|-----------|
| 400 | 10K Food | 2 |
| 401 | 50K Food | 3 |
| 402 | 150K Food | 3 |

### Stone (حجر) - 412 series
| Item ID | Amount | Qty (test) |
|---------|--------|-----------|
| 412 | 10K Stone | 1 |
| 413 | 50K Stone | 39 |
| 414 | 150K Stone | 1 |
| 415 | 500K Stone | 10 |
| 416 | 1500K Stone | 2 |

### Wood (خشب) - 421 series
| Item ID | Amount | Qty (test) |
|---------|--------|-----------|
| 421 | 50K Wood | 4 |
| 424 | 1500K Wood | 18 |

## Hero Materials (مواد الأبطال)
| Item ID | Qty (test) |
|---------|-----------|
| 521 | 46 |
| 522 | 89 |
| 523 | 89 |
| 524 | 36 |

## Equipment Materials (مواد المعدات)
| Item ID | Qty (test) |
|---------|-----------|
| 570 | 53 |
| 571 | 86 |
| 572 | 30 |
| 573 | 97 |
| 574 | 33 |
| 575 | 246 |
| 576 | 17 |
| 577 | 4 |

## Gems/Jewels (أحجار كريمة)
| Item ID | Qty (test) |
|---------|-----------|
| 620 | 24 |
| 621 | 28 |
| 622 | 27 |
| 623 | 116 |
| 624 | 19 |
| 625 | 218 |
| 626 | 8 |

## Special Items
| Item ID | Name | Qty (test) |
|---------|------|-----------|
| 723 | Unknown | 58 |
| 732 | Unknown | 50 |
| 902 | Unknown | 1 |
| 923 | Relocator (نقل) | 6 |
| 924 | Relocator 2 (نقل ٢) | 21 |
| 970 | Unknown | 1 |
| 2000 | Random Relocator | 383 |

## Monster Materials (مواد الوحوش)
| Item ID | Qty (test) | Notes |
|---------|-----------|-------|
| 1100 | 19 | |
| 1101 | 156 | Common drop |
| 1110 | 11 | |
| 1120 | 91 | |
| 1121 | 104 | |
| 1128 | 6 | |
| 1130 | - | From monster drops |
| 1131 | 94 | |
| 1138 | - | From monster drops |
| 1140 | 71 | |
| 1141 | 54 | |
| 1148 | 4 | |
| 1150 | 6 | |

## Holy Stars / Energy (نجوم مقدسة)
| Item ID | Qty (test) | Notes |
|---------|-----------|-------|
| 1200 | 115 | Very common monster drop |
| 1201 | 14 | |
| 1202 | 9 | |
| 1203 | 668 | Most common item! |
| 1287 | 2 | From gather |

## VIP Items
| Item ID | Name | Qty (test) |
|---------|------|-----------|
| 1300 | VIP Points (نقاط VIP) | 38 |
| 1301 | Unknown | 5 |
| 1302 | Unknown | 3 |

## Familiar Items (المألوف)
| Item ID | Qty (test) |
|---------|-----------|
| 6008 | 1 |
| 6200 | 2 |
| 6201 | 1 |
| 6202 | 15 |

## Item Use Response
| Opcode | Description |
|--------|-------------|
| 0x0066 | ITEM_USE_RESULT |
| 0x0069 | ITEM_USE_CHOOSE (选择使用) |
