from tqdm.auto import tqdm

from . import *  # noqa


INPUT = """\
13386587
7830282
11151745
15059004
7808482
1317021
16298290
13031370
9052008
1701725
4846114
11148553
1088866
16388296
673726
11365400
9566459
16588541
14428134
3127245
16306885
4063841
4664232
3543298
13704110
16602970
3623930
6872352
4087272
10866793
15440565
721039
12135130
2489350
14981024
11025065
16610469
15458369
4091009
3893108
13959552
16361958
14769537
1164481
13108516
5606233
11128919
9767414
8431521
8446376
7006203
3295582
11417931
7108213
11141056
3126475
11132977
11598973
16167625
711422
15236117
5770277
6795279
4029808
6527544
14901092
16101907
12731385
16505152
778669
956561
12270366
15255354
14777108
3218525
7991281
6668065
11863807
9756346
4994766
3457166
5732307
8773713
5973684
10668541
15281141
11707625
14210666
10255542
16084539
16618203
1642845
1003462
5447287
10048544
5373107
1596757
15712079
16397731
9293824
4842134
4222650
2262103
11533536
9721313
4489166
12171593
16180134
4059073
262213
434856
3036816
9278131
654388
4493938
11623917
9371872
13826018
13738009
2552846
8232834
2038859
4463647
14984474
2618284
15519791
5377853
10902137
15815668
8117953
4445505
15018205
15514888
11823099
4530780
2891999
3638361
411315
4836111
3744157
2030357
15374090
6682485
4069584
1874989
15394438
13546773
7627162
11516330
7815050
14322365
1103990
3465087
9155857
10709884
3366052
1924110
12577736
7242729
2739146
333784
4197235
5731205
4643009
7839318
7655782
1695228
7313372
16050364
13077386
7823792
4929419
3215410
5803182
12395719
10842318
10547048
13320311
16630929
7206277
346778
14422072
2535150
8456328
14493915
6589458
1060554
16767559
10580261
6889106
12179099
586149
5890265
14575043
4442663
16409028
4149111
9710854
12107424
14071744
15508466
10686638
10461534
1647721
15372940
2279486
2010448
4096905
12277300
10797203
7897441
10645888
12008791
2981088
13267381
14542546
3254178
15640153
6485715
5565566
14714745
13361121
238447
11297287
6465289
9801380
11501441
15125415
1692792
7773089
11458812
10770982
15018833
13082231
12422007
1463235
10117460
8413343
8530827
9866177
3027686
15059760
14376091
13654579
4302285
7553480
7899966
12094752
10629209
2321639
6764363
7402551
16397882
5660214
15041005
7907067
3900103
11582347
4172291
6293416
16724568
11387753
12979783
3289321
593974
9709738
11597188
10825471
15924435
11939003
11287671
635916
4595572
12867929
7787115
4607972
11605762
4173366
6294813
2186240
13248158
14222624
8123596
418084
13798304
11629167
14489276
13022114
5655267
5910615
11911608
10103370
2773728
16481442
3611004
676016
1361316
9509347
7122482
11748525
4164036
8247724
8026196
4908765
15354509
1623486
16691861
8934213
11679227
10540058
12334722
2179155
9232832
4017971
7020759
13779976
11575106
8755438
16495460
11915075
553142
2694975
7208889
3504929
984710
15483989
10807956
6615417
9921503
14664960
9228368
198099
9286324
11241195
3307872
693393
13079224
4685721
14505706
5857344
12053140
327103
7673468
14462680
8294237
13798023
14853063
4454140
3244665
10875082
15369222
3274327
7412284
519872
9251759
5135009
14820417
9336056
8671168
9135396
10971653
9763982
14304202
11278646
8742749
9889909
4780176
749436
1531760
12624802
7849928
8806084
14757465
6646128
5372975
14243252
1086460
12754988
2102487
7920582
429750
4866295
10111771
12824975
5143093
14673284
9230158
11795941
313196
13059353
4648103
10175491
9993646
7983159
3435684
6374570
3766781
11988736
2345038
4988405
9254976
8551157
642711
1534349
883048
6834987
5289237
14648326
16017836
12456768
3285014
5189657
791006
11993972
3124015
11559657
2319933
10304597
8587214
11206783
13478813
13274124
15499173
3460960
3745927
12808235
6031352
13429849
9706170
325152
5133622
11461215
15604190
2613248
8713794
4614902
9882952
13046855
9345334
1066858
5504159
1939294
8165991
13826027
2840747
15890039
10944154
13240500
4860651
15373826
12078444
12766276
7186052
2509977
7435518
8882704
758764
3487372
3815155
12658709
14168312
9336950
11441359
11024698
12093766
756080
16742835
14290880
5660104
10748195
5137766
9387917
2786755
10571020
13779838
11795899
9377540
15184791
12107074
9926305
6659561
5561679
608481
4773654
1589190
15402403
8505380
5244664
279176
2479836
16431053
8810142
11178679
14305758
3177034
7302444
7627994
15940380
2367570
5115873
3856345
3140818
9429891
6891442
8315747
7382052
12531160
2091231
11218522
9358588
6910034
3540172
11496982
2263265
8691424
12891824
3892952
8636630
2044653
2747807
4573162
177000
10767560
15324914
3152368
7624596
6441276
3678474
2585466
13622512
2492543
4705614
2573933
3369672
13394091
267844
13529024
11396161
7931065
10054097
9490947
9367688
14300153
8631499
11317659
9127208
15227285
1837684
2049757
9115479
9022163
13841590
6323755
11557046
8540458
8646553
12294126
4124266
10157660
15585261
6664609
16218075
13721612
15878343
7837007
16131714
4387198
12874335
3888555
5135147
16353323
5078135
1575320
14782721
14206755
1363128
12431885
11863115
5486619
11483957
7420033
5997673
1387561
13996708
9386368
6758123
949309
10824686
9873070
427753
771643
16532274
8936579
8657083
1575616
10906790
12300801
362806
5997655
6135643
16081704
9187652
13194996
4702325
5607760
15701315
10103096
6154300
1439364
16348185
12872701
3019014
4903380
11083295
4313953
599063
7993821
6877503
11653702
9103214
4741176
13178759
4817414
9305746
8305446
2922822
10172104
6204839
2116249
4433277
11518345
3104345
8018433
9888754
14872216
3204980
15341659
11111783
3720661
12025758
9014205
186861
15615152
6102784
1971239
12884996
12796991
8472713
15964812
3750755
16761731
3800835
16434173
4713677
14506556
14262821
12821889
3559162
14475071
9372088
273052
16083202
2275740
6350290
16039529
14771725
5343568
16005489
10214720
2092529
6762125
9954508
13535790
2446496
12994831
9372949
1816554
15815626
13917979
7124177
4423631
11664624
13138217
9699406
7762479
4130693
4415342
16335475
16173461
15638533
6175904
13380799
4928985
1512487
9200005
1486622
8397717
11069000
15114761
15150855
12298296
1462523
14705310
9746025
9165354
10323060
6438616
2131928
8820355
6353907
6571032
4307885
6046326
9634513
10309724
2617079
1615140
15925476
14301434
12236412
9612939
3636789
5251913
12936046
14156103
8779706
9559270
4717060
9303640
2046883
11478623
13902268
15344521
1621346
959668
11454681
13645305
628988
10330149
9076297
8073776
4326529
10331239
14666830
11295102
15615665
4227888
2596854
7438508
7500985
6742470
16374730
4355536
9291746
5525490
1393673
12257758
10909850
16750154
12912194
2475456
12974032
7820955
9114189
10654180
8778737
6282911
6260043
7498226
11257101
982765
9868707
10509277
7875996
5202298
1648356
14533037
1340518
7798687
2403039
15404910
520599
7303934
512118
6183471
3968730
12362286
6497587
9210231
13064551
5252446
14353181
5376432
8462243
807850
6128890
1565375
2081424
15504147
15122119
12702365
1251498
11851388
1567527
5502724
6898758
10320457
771884
1942315
5674332
13331595
15986993
16655943
8089348
2882764
8528696
519408
16532810
14370016
6798013
8382887
15944235
11993903
1881324
6186881
12487036
10115872
1340369
14886067
9067881
12737891
7077177
2889928
7192811
445166
12483557
12376970
6692095
10307206
16418040
6092069
5366277
11754678
5553054
8005026
9193886
6057242
5175669
6230258
12374195
13944001
3412078
10736790
10206730
6294630
13422754
4879511
6611382
12628268
13981435
1070550
6143518
7012156
5127806
2960298
4959725
11294386
9202320
6083991
3548278
3932127
16739008
2432864
964927
10334143
11824474
6068440
2016592
10781768
16460613
6730696
14648010
8459472
5757649
13886435
10225384
2806148
8457563
259841
14243089
12466332
8995594
14324249
1968364
3341410
5188975
3569912
1220285
10741246
4725568
8373107
3849779
301367
1720873
5609948
9944517
7282975
13094244
12563336
11277687
14211053
4019588
16401619
9959535
13664473
6168066
14347641
2340637
9614622
4910058
14525461
13033756
5486803
2301248
15114145
12449755
10798188
16043758
15098630
13407046
1138766
9839940
3199333
11757893
4187106
2905750
7703149
8657303
14812451
4122069
5680374
7990033
13099919
14475740
7662177
13033104
4427241
1649272
4648560
15681818
2938903
2045027
13851917
16665253
13029831
7202272
2545960
2247658
12675711
12231920
3077348
13083705
6627297
2497264
971661
10463979
15467236
6450605
16408663
14542699
5780458
3569964
15792486
16287977
16394081
12846289
6649030
15703325
14207185
4517842
6919141
7605526
3331040
13969830
16312736
1423906
10132992
13375605
2192980
869436
6941452
7948171
13030514
7487739
5396277
6760290
10272190
11910979
1059881
7599596
1732075
639507
8659552
14945688
10838392
16145860
15750400
7582158
16256890
11659246
2065049
304547
1466844
4873408
12010160
5665517
12595358
2162208
6226574
6758948
930325
2169664
8781706
10580993
10318470
1233810
16508033
6652499
8599902
200691
14137282
5139245
9207843
293359
9578812
15961667
15857539
16524424
5540395
9471280
7909431
5387696
11565830
11061821
8353810
9508067
15406530
6208344
7466640
3109802
3648778
5369332
3559169
5147105
6914097
12030414
9271555
12962447
16683827
2865635
3692862
10055896
2850083
10744120
15168572
10874964
2685431
1278627
8907508
7637615
10721670
15836243
7029773
13638868
13990159
6059903
14021860
10573078
16300434
7997304
7203408
14718138
8765327
2852633
3144112
4608178
15160251
9481648
554738
5441790
11651946
4248162
10644346
15737519
16023134
14951498
15125331
4462843
14041549
3726272
1194406
416557
14377293
11703195
14195337
1152633
10146139
1117600
980515
10323306
16648213
9879771
11249575
11938980
4139705
11194692
6555929
6604566
11201819
14019254
1362598
3783756
4042613
12336159
3074387
4955077
15130973
1318821
4013061
3875180
7502520
2447237
10108737
11678498
9646104
12911239
3346121
8660823
16243389
5321721
5650421
6464017
10356988
12744600
16422889
8598143
6600093
11163372
7019756
10383471
3888953
5466445
3721680
10590262
15968077
7249716
13141256
13047455
16660258
440858
6439427
15973993
13822569
9271817
16720532
3323775
1259411
9670067
5369497
15396525
8736947
6565845
12931501
5426445
10977255
9198045
8702096
9849236
3126217
1912218
11868655
15112012
4378292
8234057
12330913
9337016
8149519
9862477
5854648
9234086
7213311
9042068
15444918
13672286
8572744
8723676
15933683
283767
14945593
1996524
2400148
10525483
2925532
4231481
12095659
8398301
6113449
8937847
856023
845770
5925182
8253497
656473
9760399
9300373
13517810
13801697
14379507
3544444
12167549
2105658
9474777
5891029
15513254
14558677
8259527
13286254
9671761
1161106
12681579
6502676
2183994
7373369
15484385
7288952
14103988
5927221
11724582
13336960
8271714
7714649
13246991
1973355
3985242
5060658
4405408
4279572
5859088
2143760
9442846
7644021
562688
9290746
8107633
15939917
7046425
8242438
3968672
12000673
551632
8366815
3574545
11784822
12627690
4231949
15610663
11703013
3907879
14726483
13355618
12878672
11980115
697517
11542217
5101099
9287561
2621353
11400339
12775756
2515450
2235262
15964527
16747888
13793295
898772
2926481
7155479
16629361
2461045
9569234
7796816
16232986
11398116
10478504
13249205
3975068
6801844
9140621
1208854
830611
268717
373130
15116259
15969605
16383997
7024188
2543553
4296083
15501173
1380697
15463165
14087067
16369512
16628745
6016511
10830248
3322612
5497843
3949604
1823105
10287219
15432601
11257487
8579737
9853851
12843293
14124520
1801294
11613707
15437507
3659797
13142758
1026151
9148098
4840994
8978179
11294887
8227067
4034259
16744660
6435116
8890087
14807876
1306759
2078230
8753639
5500995
6451547
15233962
11748241
4420580
13091313
7632915
10977273
2461460
11763888
1535055
3248442
12247460
7148392
2808650
834184
13107323
7283652
4237817
16761350
3673169
1655733
3885017
15905874
2010980
9139074
12993446
13088102
3474780
2778112
6077428
12746951
6135148
16758804
890448
7729492
5087104
10804940
13891779
878625
8004913
11395069
14262520
4303825
15059381
8943306
805147
13397911
13649134
15320151
12596242
4932821
9257036
8111983
12685610
4295857
1072085
6584573
12450129
1370717
11348564
9185027
13213105
10660889
3643443
6059244
15636511
2238909
6440214
5091088
6185193
11720158
1742804
8527024
5630614
6286057
4209372
13387220
13234870
2263694
12185500
14886424
14243436
5028832
2665923
4901047
15319351
13497882
8483548
7498260
8318101
7826400
6445772
8449368
1467992
6276838
5580377
9897712
5829131
11386773
7636214
10818609
8457858
14178562
3788411
3879630
5235596
295147
7902092
15408502
12993537
12351199
5176245
6081435
14214574
15947441
15694455
8934936
3295808
11743884
10705797
1806167
13951528
1681846
7610040
10406041
11598702
15289283
9824289
9762030
7295651
3434132
15299806
9151152
14176952
2111698
3232828
10476419
8317180
15377611
6328995
3733050
1668264
13711802
4244462
10662749
2483270
2958682
16668785
16310694
7741124
1957487
10848041
5071200
8122737
275594
1159954
9380164
6680333
10558134
12787147
584516
1570284
11977746
8175927
7221404
650117
3826550
12538036
3143787
11997736
1477686
11428905
7895120
203067
6382328
12426995
1859726
16746821
2468897
5959239
10128018
4508187
14717697
2204012
352032
4066015
15375127
2735516
9512382
12619779
13860135
5724946
9670569
4201274
9651630
15768653
4495911
9993033
557915
12234509
12948703
2688453
15985597
13024266
12404123
8417865
9561097
9333227
6175198
8643899
8109357
13241677
12328113
6620950
12594878
2715195
12515884
7265352
7621969
6327964
4632425
15284199
9539529
764072
8792824
10590478
16760319
3013521
7322669
5439081
10173098
10646262
8682818
2862431
6421763
16056020
12728764
8288637
10013919
3473649
2637385
4465937
12687405
4830683
4769289
2806934
13812692
8869317
7051526
3478340
7243154
11923606
4234666
5429054
4657799
11735984
10758401
7442163
3721019
2106062
16753858
10698474
11502765
10566556
6515786
2410161
13241063
10778735
5021725
2665656
11202265
10266001
10686435
2716394
14569484
9038212
10846814
133163
10759301
10526328
4566892
1965449
9844681
6915592
14001908
13287311
10919537
14789435
9203280
8205657
11791337
425323
14612925
8013328
605502
7730350
16633422
15946498
2065327
762079
1138688
14522161
8349107
13980481
8803493
16348410
13465238
1788752
13057213
12607154
7947676
8410365
3140771
9078598
5179042
9483560
12492762
7973765
6635943
13626310
2982906
4311920
1021318
9029029
6067523
2739189
4181552
12760400
1645204
8053891
16159033
13790970
10690186
5118093
14288491
5177825
8482100
1665636
3935782
10259966
14460681
4066026
4640467
9298487
16482241
7116672
14040755
15802781
15546388
2950406
3572035
1284274
13605229
6988550
16367928
3766729
10508374
13083943
8520383
5033246
4899480
11061668
8271648
4110632
15095501
2386428
11252790
2086452
8880566
15132184
8241492
10072123
2672516
10076695
13693249
7229240
3174910
13355633
8443817
9221183
3681681
9660756
10600779
9896899
4152373
4868706
14449268
13672308
9057119
9973318
12058875
9895716
7583580
10884731
9369326
3908638
8546260
15065430
3382113
14303327
6939797
7153578
7037088
7210721
7814240
14370461
8416200
8992581
11605754
11176412
6388598
6435022
3798400
14117669
2364054
7062173
7644623
12178461
8461229
15389900
6841531
15119775
10119473
7924443
5670069
8752149
10025540
16326553
14325940
7238199
11817545
7080033
4705103
10228275
9283099
13374767
13055304
4288664
5531005
12347339
16225038
11305842
16618359
15817139
580442
1413824
1140411
13357628
7077743
16071942
6903041
8171450
1961285
16048838
3382105
828198
15401617
810458
12239625
7893276
1577617
8187162
4055102
7686291
5528901
14008618
3358490
6304524
9052907
13808762
9561623
11873889
2783123
1801511
8149925
16097721
2201075
3185692
13904384
16525427
8256466
14544885
4126947
11430700
2636515
6036531
5120644
9270093
15637577
447717
10314132
8703144
10473647
16317557
15575665
12604961
7477377
1686339
14097368
16580922
859275
12658602
10089562
7492799
11236660
11503509
12778433
13659081
2314882
9892598
16007999
6927206
14116612
3434413
14388934
9822798
985365
7465697
5588549
10932728
1846762
11784545
8990936
12385150
11372156
5103574
5981925
3512201
2264198
6210373
7734573
16296858
8911749
16057116
6904452
7326398
11478069
12291663
2664060
3659943
13120942
5926130
6453722
9422602
8735793
4058806
7908300
3987906
11630460
3693540
1753630
10256943
10254212
12593637
3938450
463061
5667741
6087935
7288148
13781266
4680473
11552493
2652210
784740
5844194
7250927
4788406
16580177
3072705
1394246
769704
9773743
11358876
2703799
9912737
3471516
9294190
6651190
6951282
8820451
349800
4153357
828141
15131217
3942001
4909263
16143730
16198810
10444280
10919680
6716958
4140879
4321042
6974408
11388910
5385059
13842655
14092807
2903396
4120962
14403895
5732895
16319071
11110287
5314553
11485447
519360
6121503
11200900
4371668
692791
7587070
10725735
1321340
5917269
12085522
12088486
8480674
5424969
13257772
1837506
383830
5125943
5257109
14391586
2865674
5342471
15640627
4653178
15062189
3750846
4890224
9548915
16626832
13351989
14336002
14758660
14173920
5456812
9926618
1170369
9697934
3456079
3385483
14376907
10979142
8755246
14897272
14638587
5392482
4310326
3549460
8537994
8869125
9694992
2885241
9519780
16475505
10365800
12285561
10072319
15973669
16734238
260424
10839582
12994753
3930718
12977553
5433503
7007634
13796109
520658
13279680
11579031
14961226
9805934
9126716
4341515
14498286
11824855
13527930
10636525
14514127
13182406
14188614
16197043
2489732
6714445
10585701
2569245
8656369
9536806
1797524
6066001
14709362
811074
12630774
14792863
7982046
8693320
2810967
8945122
15187885
12229444
3283764
14844467
7428546
5764400
7216193
6710418
7020568
2899403
15799466
10619994
7256399
4671576
9922399
8058056
9747141
11597724
8617843
3670894
4831265
11780523
15052482
1548361
1660586
6924701
10876700
8550720
4621233
2958969
10583409
9772320
10268767
13645349
15603639
3730323
14444550
12645947
5115081
4763497
12851620
2428726
3520218
10978900
2456514
6767429
5610171
13624454
13868101
9305507
2416103
12184285
14818754
13499449
8280069
1819380
16718627
5341084
7022690
3020091
16450045
782451
8548857
16070984
1105393
14348444
2111126
4306866
13636808
2450712
9838784
3722876
5739886
15036474
15344238
2266229
2078001
10783776
8141001
12139815
16070566
9187537
8409524
2161884
2535576
825856
16548696
16497323
16258323
9992833
11181713
6860038
2229049
1479232
4921288
3617560
3291413
1589886
171162
4438575
10988229
11480745
13571217
9681334
9734561
10205751
15121964
1653156
2347467
7962712
8350866
16438775
8334244
9481537
1133421
5875118
5719048
12981604
7733948
5123025
8614644
5630089
2980285
3265871
15693146
1476961
1573782
935474
4789834
14891210
12419031
5937960
2190966
1798758
8147384
11993496
9601314
3527111
5324933
12504943
9939991
9738223
1568703
8797299
12775168
10822454
9048857
10463303
9791176
5590079
15767497
4196974
294131
2311145
8212105
13095772
6279937
826505
13706752
12693302
13012942
667431
12749175
836381
2470585
11458456
14426443
7347417
9817855
3281849
10747621
10031466
3869466
9283129
164520
3774819
13665646
13690775
7812344
15907109
10877576
6921241
9953593
427726
11696985
9328328
16638075
5125988
2524325
5096282
2449051
7671771
15355271
4519772
3607940
13264065
3388286
2568342
1709194
7255040
780248
13791243
7394043
11273863
1222280
9185430
13130334
13325304
6822529
8122987
2180179
12957484
9965985
9423976
8060529
7960602
4211448
3476797
15594048
11326700
3950527
14326818
11699451
12914959
11317998
10383054
16390328
15508706
14759537
14773251
5153638
3992320
7004493
3977963
4625927
4704372
2011371
7054127
1017019
5731043
8225427
13945686
5239878
5866117
13112000
4376263
8710419
8340727
9987991
16512330
14560254
6035747
5938167
7368596
1501119
6112018
8024829
819711
13325382
9560121
258472
16569347
16711953
3188950
9246567
15924143
5911079
14100729
4581332
13962160
14303848
16497528
13541815
13394964
6522510
5009782
12722833
1514806
1082499
11225632
6624351
552152
2430877
6799166
16070224
13156998
2179488
14039951
4098584
13737476
15450023
16125777
14661713
12098433
7480966
14867746
15202312
5595603
6310306
5387598
16656898
14172682
7493360
3378884
16758946
844020
3903571
14377793
8180586
8674902
10314616
11124481
11176517
12418484
12268308
5694164
3701331
10909102
14951547
9236927
3513854
4100102
15548517
12732506
1731929
12237153
6558489
11256773
4125781
6670323
1733681
10983296
3773332
7640869
3100357
3179693
13014932
8146776
7738614
5599487
7543548
13055906
3818373
14948439
2311288
9463689
2234549
5795898
7469372
488283
252509
12736635
1164209
1692348
657386
12345101
10140699
11473348
11682562
9512572
3381282
9886920
1643089
13882820
16457774
10445223
14596946
16041227
10598220
14043691
8910553
3357821
2002425
5727660
16400041
15526086
11846348
14276575
10468730
4649694
9565989
1567540
12041359
11679329
15051618
7293416
9228103
7840384
3446540
12184895
6314983
4693117
5621597
15682086
3585676
15953881
5100331
4825255
2974979
8396488
10500074
12291170
2342450
7527700
4645314
7762525
3125973
2637694
11139622
7393299
9618765
16302503
1242676
6560755
3670180
16399341
6959711
1797072
14870788
7059721
4881510
4767258
8261481
10995731
1253756
"""


if __name__ == "__main__":
    seeds = [int(n.strip()) for n in INPUT.split("\n") if n.strip()]
    print(
        "Sum of 2000th secret for all monkeys:",
        sum(nth_secret(seed, 2000) for seed in tqdm(seeds))
    )
    change_dict = {}
    for seed in tqdm(seeds):
        add_to_change_dict(
            change_dict,
            compile_change_dict(str(seed), seed, limit=2000)
        )
    _, payoff_best = most_profitable_change(change_dict)
    print(
        "Best possible banana payoff:",
        payoff_best
    )

