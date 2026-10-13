# Complete exact finite bases for the U10 unbounded argument

Curated mathematical proof from **Pro053/A78 accepted dependency**. The corresponding accepted scope
is stated in the module guide; [the source map](../../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Derived SOURCE. These are **twenty full polynomial identities**, not parameter sampling. The arbitrary-index parts of the proof reduce only to these fixed bases. Every coefficient, including every zero, is supplied below. Two newly authored implementations independently reconstruct each identity.

JSON SHA-256: `2a27bb8b3b9b0fc211df76dbffb53397866c26aea0bd94f8fdb7e161d54296b0`.

For each matrix, row i lists ascending powers of the second variable z in the coefficient of x^i, divided by the stated positive common denominator. The full total-degree bound determines the row length, including trailing zeros. For HIGH-E, x=At and z=(H-A)t. For LOW-G, the displayed x is b in original x=b+h and displayed z=h; partial_h was taken at fixed original x **before** this substitution. LOW-E-SCALAR uses the first variable as h and every second-variable exponent is zero.

Definitions: HIGH-E is the complete expression (15) of the main proof minus K, not an auxiliary subtotal. LOW-G-D1/D2 are the first/second derivatives of V-V0-J_low. LOW-E-SCALAR is `a_(n-1)(2h)-1-(4/3)h*a_(n-1)(h)+(4/3)h^n/(n-1)!`.

## HIGH-E-3

Total degree bound: 6. Nonzero coefficients: 17.

```text
x^0: denominator 2; numerators [0, 3, 1, 0, 0, 0, 0]
x^1: denominator 120; numerators [210, 771, 155, 0, 0, 0]
x^2: denominator 240; numerators [1496, 2445, 285, 0, 0]
x^3: denominator 48; numerators [421, 360, 22, 0]
x^4: denominator 48; numerators [289, 123, 3]
x^5: denominator 240; numerators [475, 78]
x^6: denominator 240; numerators [59]
```

## HIGH-E-4

Total degree bound: 8. Nonzero coefficients: 29.

```text
x^0: denominator 3; numerators [0, 7, 6, 2, 0, 0, 0, 0, 0]
x^1: denominator 1260; numerators [3150, 16829, 11718, 2422, 0, 0, 0, 0]
x^2: denominator 360; numerators [4149, 11385, 5932, 750, 0, 0, 0]
x^3: denominator 360; numerators [8222, 14232, 5145, 380, 0, 0]
x^4: denominator 1440; numerators [35673, 40080, 9220, 360, 0]
x^5: denominator 360; numerators [5615, 3936, 507, 8]
x^6: denominator 720; numerators [4047, 1590, 86]
x^7: denominator 2520; numerators [2681, 446]
x^8: denominator 160; numerators [13]
```

## HIGH-E-5

Total degree bound: 10. Nonzero coefficients: 44.

```text
x^0: denominator 24; numerators [0, 70, 85, 50, 11, 0, 0, 0, 0, 0, 0]
x^1: denominator 10080; numerators [30660, 199880, 209515, 93370, 14399, 0, 0, 0, 0, 0]
x^2: denominator 60480; numerators [991842, 3531975, 2997895, 1000104, 104720, 0, 0, 0, 0]
x^3: denominator 120960; numerators [4784970, 11597560, 7624743, 1847090, 125895, 0, 0, 0]
x^4: denominator 725760; numerators [39892190, 69417243, 33934845, 5691420, 237930, 0, 0]
x^5: denominator 34560; numerators [1649415, 2065130, 714690, 77380, 1782, 0]
x^6: denominator 34560; numerators [918457, 805170, 183880, 11412, 110]
x^7: denominator 120960; numerators [1140405, 660160, 88182, 2360]
x^8: denominator 241920; numerators [495020, 168669, 9885]
x^9: denominator 16128; numerators [3967, 598]
x^10: denominator 725760; numerators [9049]
```

## HIGH-E-6

Total degree bound: 12. Nonzero coefficients: 62.

```text
x^0: denominator 60; numerators [0, 202, 300, 235, 90, 13, 0, 0, 0, 0, 0, 0, 0]
x^1: denominator 831600; numerators [2882880, 21437189, 28292550, 17997595, 5380155, 595881, 0, 0, 0, 0, 0, 0]
x^2: denominator 3326400; numerators [69389924, 291814611, 324530910, 165998140, 38395665, 3139136, 0, 0, 0, 0, 0]
x^3: denominator 2721600; numerators [156490191, 466829297, 424220145, 171519235, 30074625, 1742013, 0, 0, 0, 0]
x^4: denominator 10886400; numerators [1023235088, 2308350555, 1674320130, 522426240, 67254705, 2637180, 0, 0, 0]
x^5: denominator 3628800; numerators [362290075, 628958998, 355274535, 82828760, 7485660, 186732, 0, 0]
x^6: denominator 10886400; numerators [781176127, 1039219272, 443084985, 73812060, 4382910, 62244, 0]
x^7: denominator 3628800; numerators [128614479, 128505014, 39591690, 4406920, 153000, 936]
x^8: denominator 3628800; numerators [43530313, 31472205, 6554340, 433020, 6615]
x^9: denominator 2177280; numerators [5924871, 2909726, 363669, 10708]
x^10: denominator 10886400; numerators [4284349, 1270962, 71505]
x^11: denominator 39916800; numerators [1302763, 175170]
x^12: denominator 119750400; numerators [140803]
```

## LOW-G-D1-3

Total degree bound: 5. Nonzero coefficients: 21.

```text
x^0: denominator 240; numerators [100, 502, 815, 600, 205, 26]
x^1: denominator 72; numerators [71, 297, 369, 180, 30]
x^2: denominator 48; numerators [47, 138, 114, 28]
x^3: denominator 36; numerators [17, 30, 12]
x^4: denominator 48; numerators [5, 4]
x^5: denominator 120; numerators [1]
```

## LOW-G-D2-3

Total degree bound: 4. Nonzero coefficients: 15.

```text
x^0: denominator 360; numerators [398, 960, 855, 330, 45]
x^1: denominator 12; numerators [26, 54, 33, 6]
x^2: denominator 24; numerators [35, 54, 18]
x^3: denominator 12; numerators [5, 4]
x^4: denominator 24; numerators [1]
```

## LOW-G-D1-4

Total degree bound: 7. Nonzero coefficients: 36.

```text
x^0: denominator 10080; numerators [2940, 18580, 40782, 44695, 27195, 9289, 1659, 120]
x^1: denominator 1440; numerators [1206, 6372, 11435, 9750, 4305, 948, 82]
x^2: denominator 1440; numerators [1503, 6010, 8235, 5090, 1455, 156]
x^3: denominator 1440; numerators [979, 2820, 2730, 1080, 150]
x^4: denominator 144; numerators [35, 69, 42, 8]
x^5: denominator 480; numerators [23, 28, 8]
x^6: denominator 1440; numerators [7, 4]
x^7: denominator 5040; numerators [1]
```

## LOW-G-D2-4

Total degree bound: 6. Nonzero coefficients: 28.

```text
x^0: denominator 5040; numerators [5069, 18480, 27020, 20265, 8155, 1659, 133]
x^1: denominator 720; numerators [1683, 5425, 6390, 3520, 915, 90]
x^2: denominator 1440; numerators [3073, 8010, 7080, 2580, 330]
x^3: denominator 72; numerators [71, 135, 78, 14]
x^4: denominator 96; numerators [23, 28, 8]
x^5: denominator 240; numerators [7, 4]
x^6: denominator 720; numerators [1]
```

## LOW-G-D1-5

Total degree bound: 9. Nonzero coefficients: 55.

```text
x^0: denominator 725760; numerators [163296, 1186848, 3097476, 4211360, 3392487, 1702890, 537138, 103296, 11043, 502]
x^1: denominator 302400; numerators [221796, 1351530, 2967290, 3321780, 2140705, 826560, 188580, 23400, 1215]
x^2: denominator 120960; numerators [127110, 608688, 1077741, 960064, 475965, 133182, 19656, 1188]
x^3: denominator 181440; numerators [147976, 546966, 755853, 513450, 183855, 33264, 2394]
x^4: denominator 34560; numerators [12873, 36260, 37710, 18360, 4230, 372]
x^5: denominator 28800; numerators [3013, 6300, 4640, 1440, 160]
x^6: denominator 17280; numerators [315, 464, 216, 32]
x^7: denominator 15120; numerators [29, 27, 6]
x^8: denominator 80640; numerators [9, 4]
x^9: denominator 362880; numerators [1]
```

## LOW-G-D2-5

Total degree bound: 8. Nonzero coefficients: 45.

```text
x^0: denominator 604800; numerators [545448, 2459400, 4593820, 4664730, 2813965, 1032570, 225400, 26820, 1335]
x^1: denominator 60480; numerators [143196, 578228, 915327, 752500, 350595, 93114, 13104, 756]
x^2: denominator 60480; numerators [156368, 530775, 684243, 438480, 149100, 25704, 1764]
x^3: denominator 8640; numerators [13173, 35726, 35640, 16660, 3690, 312]
x^4: denominator 17280; numerators [9091, 18810, 13620, 4140, 450]
x^5: denominator 2880; numerators [315, 464, 216, 32]
x^6: denominator 2160; numerators [29, 27, 6]
x^7: denominator 10080; numerators [9, 4]
x^8: denominator 40320; numerators [1]
```

## LOW-G-D1-6

Total degree bound: 11. Nonzero coefficients: 78.

```text
x^0: denominator 79833600; numerators [14636160, 117330864, 344474064, 539816068, 518529770, 325610461, 137704413, 39493806, 7568880, 927245, 65593, 2036]
x^1: denominator 7257600; numerators [4755120, 32030568, 80412096, 106859040, 85867225, 44316888, 15030456, 3331500, 464325, 36900, 1274]
x^2: denominator 7257600; numerators [7514028, 40694612, 84885750, 93755550, 61843845, 25616430, 6724200, 1085700, 98325, 3820]
x^3: denominator 10886400; numerators [9858716, 42762720, 72938100, 65631510, 34630155, 11088630, 2119950, 222480, 9855]
x^4: denominator 1451520; numerators [702305, 2441030, 3354666, 2398886, 974400, 226590, 28098, 1440]
x^5: denominator 7257600; numerators [1214125, 3360588, 3637452, 1989120, 583800, 87696, 5292]
x^6: denominator 1036800; numerators [39963, 86648, 71280, 28000, 5280, 384]
x^7: denominator 1814400; numerators [10831, 17820, 10500, 2640, 240]
x^8: denominator 483840; numerators [297, 350, 132, 16]
x^9: denominator 4354560; numerators [175, 132, 24]
x^10: denominator 7257600; numerators [11, 4]
x^11: denominator 39916800; numerators [1]
```

## LOW-G-D2-6

Total degree bound: 10. Nonzero coefficients: 66.

```text
x^0: denominator 39916800; numerators [32512272, 168305940, 367457574, 449334820, 341756415, 169370355, 55560813, 11952270, 1618815, 125015, 4191]
x^1: denominator 3628800; numerators [8501256, 39717484, 75402810, 77978900, 48948375, 19474938, 4936050, 771600, 67725, 2550]
x^2: denominator 725760; numerators [2097718, 8424606, 13539045, 11611236, 5882184, 1816794, 336000, 34164, 1467]
x^3: denominator 362880; numerators [723119, 2421510, 3208485, 2218468, 873705, 197400, 23814, 1188]
x^4: denominator 1451520; numerators [1226905, 3348744, 3559206, 1908480, 549150, 80892, 4788]
x^5: denominator 172800; numerators [40051, 86564, 70800, 27600, 5160, 372]
x^6: denominator 259200; numerators [10831, 17820, 10500, 2640, 240]
x^7: denominator 60480; numerators [297, 350, 132, 16]
x^8: denominator 483840; numerators [175, 132, 24]
x^9: denominator 725760; numerators [11, 4]
x^10: denominator 3628800; numerators [1]
```

## LOW-G-D1-7

Total degree bound: 13. Nonzero coefficients: 105.

```text
x^0: denominator 6227020800; numerators [963705600, 8321569920, 26666509896, 46342528960, 50418328246, 36867594478, 18833123595, 6854879031, 1787925711, 331569953, 42657329, 3616769, 181623, 4089]
x^1: denominator 3353011200; numerators [1990906560, 14471077824, 40080800088, 60156370736, 56181953674, 34966401162, 15025457447, 4524336432, 952612815, 137365690, 12921293, 713916, 17563]
x^2: denominator 319334400; numerators [322736736, 1915455456, 4492492620, 5748461972, 4560943695, 2388163844, 849710554, 206768980, 33888855, 3576540, 219428, 5944]
x^3: denominator 239500800; numerators [231421836, 1125822082, 2218729755, 2395360275, 1593786645, 690003699, 198290631, 37553670, 4504665, 310090, 9328]
x^4: denominator 87091200; numerators [50308300, 201960768, 332525820, 299309280, 164053155, 57221472, 12774930, 1768260, 138195, 4660]
x^5: denominator 14515200; numerators [3342026, 11091578, 15110894, 11143734, 4901197, 1323966, 215488, 19392, 741]
x^6: denominator 87091200; numerators [5533231, 15115240, 16784964, 9887892, 3354960, 658476, 69468, 3048]
x^7: denominator 76204800; numerators [944311, 2098278, 1855980, 840840, 206640, 26208, 1344]
x^8: denominator 9676800; numerators [16653, 29460, 20020, 6560, 1040, 64]
x^9: denominator 8709120; numerators [1473, 2002, 984, 208, 16]
x^10: denominator 87091200; numerators [1001, 984, 312, 32]
x^11: denominator 79833600; numerators [41, 26, 4]
x^12: denominator 958003200; numerators [13, 4]
x^13: denominator 6227020800; numerators [1]
```

## LOW-G-D2-7

Total degree bound: 12. Nonzero coefficients: 91.

```text
x^0: denominator 10897286400; numerators [8092301040, 46301781708, 113035676754, 157420092830, 140000102242, 84106993971, 35139531427, 10326866550, 2126235111, 300064765, 27628601, 1493856, 35945]
x^1: denominator 479001600; numerators [1099086624, 5705290800, 12303823884, 14858587612, 11293169745, 5714471994, 1975204770, 468393420, 74946465, 7729370, 463584, 12276]
x^2: denominator 39916800; numerators [123721014, 560212114, 1046308362, 1082791710, 695709080, 292281066, 81777542, 15112020, 1771275, 119240, 3509]
x^3: denominator 21772800; numerators [52039162, 201444642, 320754255, 280249500, 149584890, 50937054, 11122860, 1507860, 115515, 3820]
x^4: denominator 14515200; numerators [16949998, 55384050, 74100170, 53650100, 23178575, 6155100, 985530, 87300, 3285]
x^5: denominator 14515200; numerators [5558347, 15106548, 16646238, 9716896, 3264870, 634452, 66276, 2880]
x^6: denominator 21772800; numerators [1890188, 4195926, 3703959, 1673280, 409815, 51786, 2646]
x^7: denominator 1209600; numerators [16653, 29460, 20020, 6560, 1040, 64]
x^8: denominator 967680; numerators [1473, 2002, 984, 208, 16]
x^9: denominator 8709120; numerators [1001, 984, 312, 32]
x^10: denominator 7257600; numerators [41, 26, 4]
x^11: denominator 79833600; numerators [13, 4]
x^12: denominator 479001600; numerators [1]
```

## LOW-G-D1-8

Total degree bound: 15. Nonzero coefficients: 136.

```text
x^0: denominator 2615348736000; numerators [350269920000, 3209162198400, 11016289366560, 20741985998280, 24805208418900, 20304334929970, 11877759278385, 5094901826157, 1625088876840, 387240838985, 68635396830, 8914398311, 823482660, 51194745, 1919025, 32752]
x^1: denominator 1307674368000; numerators [711467517600, 5494937957280, 16429050313164, 27051699167220, 28245538973015, 20110575474990, 10173944000220, 3742324661790, 1011258499680, 200627036610, 28865597761, 2928915990, 198600675, 8071560, 148605]
x^2: denominator 871782912000; numerators [856598641200, 5463069940368, 14015507835420, 20008142843780, 18131002124235, 11160925093318, 4844346507000, 1510754179220, 340152497685, 54818794030, 6165429270, 459428060, 20373990, 406840]
x^3: denominator 2615348736000; numerators [2634839180712, 13996091556720, 30719060184540, 37816200381960, 29534838678345, 15574876857540, 5727336144530, 1487717611380, 272051845065, 34269034800, 2830247420, 137919600, 3004820]
x^4: denominator 2874009600; numerators [1886533020, 8431535778, 15814304550, 16689450426, 11128671675, 4960679097, 1516977000, 319649946, 45644445, 4218775, 227700, 5448]
x^5: denominator 9580032000; numerators [2786155670, 10538155980, 16830482944, 15092862840, 8477826115, 3134466720, 775966730, 127466460, 13336455, 804540, 21296]
x^6: denominator 2612736000; numerators [238706265, 764902910, 1033321860, 777602080, 361137105, 107804424, 20757870, 2493420, 169965, 5020]
x^7: denominator 18289152000; numerators [382086271, 1033288560, 1168234320, 724900680, 271123230, 62800920, 8822940, 689040, 22950]
x^8: denominator 203212800; numerators [717450, 1622545, 1510740, 753788, 218400, 36848, 3360, 128]
x^9: denominator 3657830400; numerators [1622545, 3021480, 2261364, 873600, 184240, 20160, 896]
x^10: denominator 1306368000; numerators [53955, 80763, 46800, 13160, 1800, 96]
x^11: denominator 9580032000; numerators [26921, 31200, 13160, 2400, 160]
x^12: denominator 2874009600; numerators [390, 329, 90, 8]
x^13: denominator 74724249600; numerators [329, 180, 24]
x^14: denominator 174356582400; numerators [15, 4]
x^15: denominator 1307674368000; numerators [1]
```

## LOW-G-D2-8

Total degree bound: 14. Nonzero coefficients: 120.

```text
x^0: denominator 2615348736000; numerators [1786227163200, 11042702818560, 29367857368512, 45117435341160, 45030596703820, 31045404720330, 15316424782659, 5516061691140, 1462650551505, 285099895080, 40327185899, 4023959940, 268330335, 10723230, 194070]
x^1: denominator 1307674368000; numerators [2925142033680, 16468890805224, 39108573995400, 52957727360720, 46159871002245, 27560888721366, 11663233111530, 3557805459780, 785185836435, 124199595520, 13721788080, 1004923920, 43808310, 859950]
x^2: denominator 871782912000; numerators [2828230759656, 14034924114120, 29305368346800, 34707808114980, 26269786788245, 13491202184460, 4847943110010, 1233502370100, 221317301205, 27385257900, 2223461240, 106568280, 2284100]
x^3: denominator 1437004800; numerators [3917094156, 16894137438, 30705787134, 31532832507, 20530779885, 8959969755, 2688036813, 556532394, 78173370, 7113260, 378180, 8916]
x^4: denominator 1916006400; numerators [2834868182, 10547583420, 16548417908, 14583594960, 8057770875, 2933441280, 715733018, 115970580, 11976195, 713460, 18656]
x^5: denominator 435456000; numerators [240300825, 765140994, 1024795800, 763820850, 351241695, 103822866, 19799640, 2356200, 159165, 4660]
x^6: denominator 2612736000; numerators [382816639, 1033355160, 1164571920, 719647740, 267898890, 61746300, 8631000, 670680, 22230]
x^7: denominator 152409600; numerators [4306038, 9735302, 9058077, 4514713, 1306305, 220059, 20034, 762]
x^8: denominator 406425600; numerators [1622545, 3021480, 2261364, 873600, 184240, 20160, 896]
x^9: denominator 130636800; numerators [53955, 80763, 46800, 13160, 1800, 96]
x^10: denominator 870912000; numerators [26921, 31200, 13160, 2400, 160]
x^11: denominator 239500800; numerators [390, 329, 90, 8]
x^12: denominator 5748019200; numerators [329, 180, 24]
x^13: denominator 12454041600; numerators [15, 4]
x^14: denominator 87178291200; numerators [1]
```

## LOW-E-SCALAR-3

Total degree bound: 3. Nonzero coefficients: 1.

```text
x^0: denominator 1; numerators [0, 0, 0, 0]
x^1: denominator 3; numerators [5, 0, 0]
x^2: denominator 1; numerators [0, 0]
x^3: denominator 1; numerators [0]
```

## LOW-E-SCALAR-4

Total degree bound: 4. Nonzero coefficients: 2.

```text
x^0: denominator 1; numerators [0, 0, 0, 0, 0]
x^1: denominator 3; numerators [7, 0, 0, 0]
x^2: denominator 9; numerators [14, 0, 0]
x^3: denominator 1; numerators [0, 0]
x^4: denominator 1; numerators [0]
```

## LOW-E-SCALAR-5

Total degree bound: 5. Nonzero coefficients: 4.

```text
x^0: denominator 1; numerators [0, 0, 0, 0, 0, 0]
x^1: denominator 6; numerators [17, 0, 0, 0, 0]
x^2: denominator 18; numerators [55, 0, 0, 0]
x^3: denominator 18; numerators [25, 0, 0]
x^4: denominator 9; numerators [1, 0]
x^5: denominator 1; numerators [0]
```

## LOW-E-SCALAR-6

Total degree bound: 6. Nonzero coefficients: 5.

```text
x^0: denominator 1; numerators [0, 0, 0, 0, 0, 0, 0]
x^1: denominator 30; numerators [97, 0, 0, 0, 0, 0]
x^2: denominator 90; numerators [401, 0, 0, 0, 0]
x^3: denominator 6; numerators [19, 0, 0, 0]
x^4: denominator 18; numerators [19, 0, 0]
x^5: denominator 10; numerators [1, 0]
x^6: denominator 1; numerators [0]
```
