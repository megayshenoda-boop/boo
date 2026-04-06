# Deep Server Response Format Analysis

```
================================================================================
DEEP SERVER RESPONSE FORMAT ANALYSIS
================================================================================

================================================================================
PART A: BINARY ANALYSIS OF libgame.so
================================================================================

Loaded libgame.so: 104,080,728 bytes
DYNSTR offset: 0x682A10
DYNSYM offset: 0x2F8, size: 0x682758

--- Step 1: Finding all getData symbols ---
Total dynsym entries parsed: 222599
Symbols containing 'getData': 5143

Unique classes with getData: 4068

Class Name                                                   Address     Size
--------------------------------------------------------------------------------
  10getDataArrEv                                        0x104D700027C78 633099654266880B
  11CMailDBUtil11getDataInfoERNSt6__ndk113unordered_mapImP8MailInfoNS0_4hashImEENS0_8equal_toImEENS0_9allocatorINS0_4pairIKmS3_EEEEEE 0x00008F0F  63607B
  2getDataCountEv                                       0x00021893      0B
  31Activity_chess_land_positionXml10getDataMapEv       0x3000400410200000 4611722302379010384B
  7CMSG_BUILDING_OPERAT_RETURN7getDataEPKc              0x52F600000000 245783798480896B
  7getDataEPKc                                          0x0000EB4C  56751B
  ARD7getDataEPKc                                       0x200500028008808 9241568954294472768B
  ATTLEFIELD_RANK_VIEW_REQUEST7getDataEPKc              0xBC072810606050AA 576698247368679808B
  AchievementXml                                        0x04C1FFD0      8B
  AchievementXml                                        0x04C1FFD8      8B
  AchievementXml                                        0x04C20754      8B
  AchievementXml                                        0x04C2075C      8B
  Achievement_score_rewardXml                           0x04C21D30      8B
  Achievement_score_rewardXml                           0x04C21D38      8B
  Active_freepickXml                                    0x04C231B8      8B
  Active_freepickXml                                    0x04C231C0      8B
  Active_freepick_rewardXml                             0x04C24664      8B
  Active_freepick_rewardXml                             0x04C2466C      8B
  Active_freepick_rewardXml                             0x04C24DD0      8B
  Active_freepick_rewardXml                             0x04C24DD8      8B
  Active_freepick_setXml                                0x04C25F58      8B
  Active_freepick_setXml                                0x04C25F60      8B
  Active_giftsXml                                       0x04C27D20      8B
  Active_giftsXml                                       0x04C27D28      8B
  Active_gifts_skinXml                                  0x04C28EB0      8B
  Active_gifts_skinXml                                  0x04C28EB8      8B
  Active_gifts_taskXml                                  0x04C2A7EC      8B
  Active_gifts_taskXml                                  0x04C2A7F4      8B
  Active_gifts_taskXml                                  0x04C2AE3C      8B
  Active_gifts_taskXml                                  0x04C2AE44      8B
  Active_recharge_bonusXml                              0x04C2CBC8      8B
  Active_recharge_bonusXml                              0x04C2CBD0      8B
  Active_recharge_bonusXml                              0x04C2D344      8B
  Active_recharge_bonusXml                              0x04C2D34C      8B
  Activity_CollectionsXml                               0x04C2E79C      8B
  Activity_CollectionsXml                               0x04C2E7A4      8B
  Activity_chessXml                                     0x04C2FE78      8B
  Activity_chessXml                                     0x04C2FE80      8B
  Activity_chess_bossXml                                0x04C31778      8B
  Activity_chess_bossXml                                0x04C31780      8B
  Activity_chess_buffXml                                0x04C32784      8B
  Activity_chess_buffXml                                0x04C3278C      8B
  Activity_chess_guild_rewardXml                        0x04C33AD8      8B
  Activity_chess_guild_rewardXml                        0x04C33AE0      8B
  Activity_chess_land_colourXml                         0x04C348DC      8B
  Activity_chess_land_colourXml                         0x04C348E4      8B
  Activity_chess_land_positionXml                       0x04C35860      8B
  Activity_chess_land_positionXml                       0x04C35868      8B
  Activity_chess_markXml                                0x04C3691C      8B
  Activity_chess_markXml                                0x04C36924      8B
  Activity_chess_markXml                                0x04C36F6C      8B
  Activity_chess_markXml                                0x04C36F74      8B
  Activity_chess_mark_rewardXml                         0x04C3853C      8B
  Activity_chess_mark_rewardXml                         0x04C38544      8B
  Activity_chess_npcXml                                 0x04C39C68      8B
  Activity_chess_npcXml                                 0x04C39C70      8B
  Activity_chess_pointXml                               0x04C3A9BC      8B
  Activity_chess_pointXml                               0x04C3A9C4      8B
  Activity_gift_packXml                                 0x04C3C394      8B
  Activity_gift_packXml                                 0x04C3C39C      8B
  Activity_gift_packXml                                 0x04C3C9DC      8B
  Activity_gift_packXml                                 0x04C3C9E4      8B
  Activity_knightXml                                    0x04C3DE7C      8B
  Activity_knightXml                                    0x04C3DE84      8B
  Activity_knight_guild_rewardXml                       0x04C3F1BC      8B
  Activity_knight_guild_rewardXml                       0x04C3F1C4      8B
  Activity_knight_markXml                               0x04C40208      8B
  Activity_knight_markXml                               0x04C40210      8B
  Activity_knight_markXml                               0x04C40858      8B
  Activity_knight_markXml                               0x04C40860      8B
  Activity_knight_monsterXml                            0x04C45D34      8B
  Activity_knight_monsterXml                            0x04C45D3C      8B
  Activity_knight_monster_nameXml                       0x04C46B00      8B
  Activity_knight_monster_nameXml                       0x04C46B08      8B
  Activity_knight_number_rewardXml                      0x04C47E3C      8B
  Activity_knight_number_rewardXml                      0x04C47E44      8B
  Activity_knight_point_rewardXml                       0x04C49190      8B
  Activity_knight_point_rewardXml                       0x04C49198      8B
  Activity_knight_rewardXml                             0x04C49FE4      8B
  Activity_knight_rewardXml                             0x04C49FEC      8B
  Activity_rank_rewardXml                               0x04C4B740      8B
  Activity_rank_rewardXml                               0x04C4B748      8B
  Activity_rank_rewardXml                               0x04C4BE18      8B
  Activity_rank_rewardXml                               0x04C4BE20      8B
  Activity_roud_awardXml                                0x04C4D74C      8B
  Activity_roud_awardXml                                0x04C4D754      8B
  Activity_roud_awardXml                                0x04C4DE54      8B
  Activity_roud_awardXml                                0x04C4DE5C      8B
  Activity_rush_eventXml                                0x04C4F838      8B
  Activity_rush_eventXml                                0x04C4F840      8B
  Activity_sourceXml                                    0x04C50DB4      8B
  Activity_sourceXml                                    0x04C50DBC      8B
  Activity_sourceXml                                    0x04C514C8      8B
  Activity_sourceXml                                    0x04C514D0      8B
  Activity_source_buyXml                                0x04C529BC      8B
  Activity_source_buyXml                                0x04C529C4      8B
  Activity_switchXml                                    0x04C53874      8B
  Activity_switchXml                                    0x04C5387C      8B
  Activity_target_typeXml                               0x04C54DF4      8B
  Activity_target_typeXml                               0x04C54DFC      8B
  Activity_target_typeXml                               0x04C555A8      8B
  Activity_target_typeXml                               0x04C555B0      8B
  Activity_timeXml                                      0x04C56ACC      8B
  Activity_timeXml                                      0x04C56AD4      8B
  Ad_eventXml                                           0x04C57D80      8B
  Ad_eventXml                                           0x04C57D88      8B
  Ad_idXml                                              0x04C58D04      8B
  Ad_idXml                                              0x04C58D0C      8B
  Ad_idXml                                              0x04C59260      8B
  Ad_idXml                                              0x04C59268      8B
  Ad_itemXml                                            0x04C5AC50      8B
  Ad_itemXml                                            0x04C5AC58      8B
  Ad_popXml                                             0x04C5D054      8B
  Ad_popXml                                             0x04C5D05C      8B
  Ad_popXml                                             0x04C5D83C      8B
  Ad_popXml                                             0x04C5D844      8B
  Adventure_baseXml                                     0x04C604D8      8B
  Adventure_baseXml                                     0x04C604E0      8B
  Adventure_chapterXml                                  0x04C6239C      8B
  Adventure_chapterXml                                  0x04C623A4      8B
  Adventure_chapterXml                                  0x04C62B24      8B
  Adventure_chapterXml                                  0x04C62B2C      8B
  Adventure_coordinateXml                               0x04C6490C      8B
  Adventure_coordinateXml                               0x04C64914      8B
  Adventure_coordinateXml                               0x04C64FA0      8B
  Adventure_coordinateXml                               0x04C64FA8      8B
  Af_event_packXml                                      0x04C66208      8B
  Af_event_packXml                                      0x04C66210      8B
  AlarmItemXml                                          0x04C672B4      8B
  AlarmItemXml                                          0x04C672BC      8B
  AlarmItemXml                                          0x04C679B4      8B
  AlarmItemXml                                          0x04C679BC      8B
  All_for_oneXml                                        0x04C691FC      8B
  All_for_oneXml                                        0x04C69204      8B
  All_for_one_rewardXml                                 0x04C6A95C      8B
  All_for_one_rewardXml                                 0x04C6A964      8B
  All_for_one_rewardXml                                 0x04C6AFE4      8B
  All_for_one_rewardXml                                 0x04C6AFEC      8B
  Anniversary_donateXml                                 0x04C6D1C8      8B
  Anniversary_donateXml                                 0x04C6D1D0      8B
  Anniversary_donateXml                                 0x04C6DA20      8B
  Anniversary_donateXml                                 0x04C6DA28      8B
  Anniversary_donate_dialogueXml                        0x04C6F00C      8B
  Anniversary_donate_dialogueXml                        0x04C6F014      8B
  Anniversary_donate_dialogueXml                        0x04C6F664      8B
  Anniversary_donate_dialogueXml                        0x04C6F66C      8B
  ArenaEffectXml                                        0x04C7082C      8B
  ArenaEffectXml                                        0x04C70834      8B
  ArenaSoundXml                                         0x04C718F4      8B
  ArenaSoundXml                                         0x04C718FC      8B
  ArenaXml                                              0x04C72C6C      8B
  ArenaXml                                              0x04C72C74      8B
  Arena_rewardXml                                       0x04C74160      8B
  Arena_rewardXml                                       0x04C74168      8B
  Arena_robotXml                                        0x04C755A8      8B
  Arena_robotXml                                        0x04C755B0      8B
  Arena_robot_nameXml                                   0x04C763AC      8B
  Arena_robot_nameXml                                   0x04C763B4      8B
  Arena_skillTipXml                                     0x04C770FC      8B
  Arena_skillTipXml                                     0x04C77104      8B
  Army_lossXml                                          0x04C78298      8B
  Army_lossXml                                          0x04C782A0      8B
  Army_lossrewardXml                                    0x04C79704      8B
  Army_lossrewardXml                                    0x04C7970C      8B
  Army_skinXml                                          0x04C7AEE0      8B
  Army_skinXml                                          0x04C7AEE8      8B
  Army_skinXml                                          0x04C7B658      8B
  Army_skinXml                                          0x04C7B660      8B
  Auto_hangupXml                                        0x04C7CBB8      8B
  Auto_hangupXml                                        0x04C7CBC0      8B
  Battle_animationXml                                   0x04C7E9B4      8B
  Battle_animationXml                                   0x04C7E9BC      8B
  Battle_testXml                                        0x04C7FECC      8B
  Battle_testXml                                        0x04C7FED4      8B
  Battle_testXml                                        0x04C805AC      8B
  Battle_testXml                                        0x04C805B4      8B
  Black_current_comingXml                               0x04C8237C      8B
  Black_current_comingXml                               0x04C82384      8B
  Black_current_comingXml                               0x04C82BB8      8B
  Black_current_comingXml                               0x04C82BC0      8B
  Black_current_rewardXml                               0x04C843BC      8B
  Black_current_rewardXml                               0x04C843C4      8B
  Black_current_rewardXml                               0x04C84AC4      8B
  Black_current_rewardXml                               0x04C84ACC      8B
  Bloody_war_eventXml                                   0x04C877DC      8B
  Bloody_war_eventXml                                   0x04C877E4      8B
  Bloody_war_event_bet_rewardXml                        0x04C88998      8B
  Bloody_war_event_bet_rewardXml                        0x04C889A0      8B
  Bloody_war_event_cityXml                              0x04C89F1C      8B
  Bloody_war_event_cityXml                              0x04C89F24      8B
  Bloody_war_event_city_descXml                         0x04C8AFAC      8B
  Bloody_war_event_city_descXml                         0x04C8AFB4      8B
  Bloody_war_event_mapXml                               0x04C8BE84      8B
  Bloody_war_event_mapXml                               0x04C8BE8C      8B
  Bloody_war_event_scoreXml                             0x04C8CF2C      8B
  Bloody_war_event_scoreXml                             0x04C8CF34      8B
  Bloody_war_event_scoreXml                             0x04C8D57C      8B
  Bloody_war_event_scoreXml                             0x04C8D584      8B
  Bloody_war_event_season_rewardXml                     0x04C8ECD0      8B
  Bloody_war_event_season_rewardXml                     0x04C8ECD8      8B
  Bloody_war_event_season_skinXml                       0x04C901C8      8B
  Bloody_war_event_season_skinXml                       0x04C901D0      8B
  Bloody_war_event_season_skinXml                       0x04C9084C      8B
  Bloody_war_event_season_skinXml                       0x04C90854      8B
  Bloody_war_event_talentXml                            0x04C91BFC      8B
  Bloody_war_event_talentXml                            0x04C91C04      8B
  Bloody_war_prematch_reward_lXml                       0x04C92FE8      8B
  Bloody_war_prematch_reward_lXml                       0x04C92FF0      8B
  Bloody_war_prematch_reward_lXml                       0x04C9366C      8B
  Bloody_war_prematch_reward_lXml                       0x04C93674      8B
  Bloody_war_prematch_reward_pXml                       0x04C94C54      8B
  Bloody_war_prematch_reward_pXml                       0x04C94C5C      8B
  Bloody_war_prematch_reward_tXml                       0x04C96054      8B
  Bloody_war_prematch_reward_tXml                       0x04C9605C      8B
  Bloody_war_prematch_reward_tXml                       0x04C966D8      8B
  Bloody_war_prematch_reward_tXml                       0x04C966E0      8B
  Boss_artXml                                           0x04C97C74      8B
  Boss_artXml                                           0x04C97C7C      8B
  Boss_artXml                                           0x04C98338      8B
  Boss_artXml                                           0x04C98340      8B
  Boss_baseXml                                          0x04C9A058      8B
  Boss_baseXml                                          0x04C9A060      8B
  Boss_lvXml                                            0x04C9AE20      8B
  Boss_lvXml                                            0x04C9AE28      8B
  Build_removecdXml                                     0x04C9BBC0      8B
  Build_removecdXml                                     0x04C9BBC8      8B
  Building_baseXml                                      0x04C9D0B8      8B
  Building_baseXml                                      0x04C9D0C0      8B
  Building_weightXml                                    0x04C9E518      8B
  Building_weightXml                                    0x04C9E520      8B
  Bulk_rewardsXml                                       0x04C9FC44      8B
  Bulk_rewardsXml                                       0x04C9FC4C      8B
  Bulk_rewardsXml                                       0x04CA02F4      8B
  Bulk_rewardsXml                                       0x04CA02FC      8B
  ByzantineXml                                          0x04CA1C8C      8B
  ByzantineXml                                          0x04CA1C94      8B
  ByzantineXml                                          0x04CA2418      8B
  ByzantineXml                                          0x04CA2420      8B
  CCityPlusManager                                      0x036CC2B8     80B
  CCityPlusManager                                      0x036CCCB8    256B
  CCityPlusManager                                      0x036CCDB8    472B
  CCityPlusManager                                      0x036CBEBC    792B
  CCityPlusManager                                      0x036CC1D4    228B
  CMGS_SYNC_CONTINUOUS_TASK_PROGRESS                    0x05011D14    104B
  CMSG_ABANDON_KING_CHESS_REQUEST                       0x050C8CD8     88B
  CMSG_ACCUMULATION_INFO                                0x04F9C5A4   1408B
  CMSG_ACCUMULATION_RANK_REQUEST                        0x04F9D3BC     72B
  CMSG_ACCUMULATION_RANK_RETURN                         0x04F9D5C8    136B
  CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST               0x052862D8     72B
  CMSG_ACHIEVEMENT_RECEIVE_REWARD_RETURN                0x05286474    104B
  CMSG_ACHIEVEMENT_SCORE_RECEIVE_REWARD_REQUEST         0x0528659C     56B
  CMSG_ACHIEVEMENT_SCORE_RECEIVE_REWARD_RETURN          0x052866BC     72B
  CMSG_ACHIEVEMENT_WEAR_REQUEST                         0x052867EC     72B
  CMSG_ACHIEVEMENT_WEAR_RETURN                          0x0528691C     72B
  CMSG_ACTION_EXCHAGE_COUNT_REQUEST                     0x04F9E85C    168B
  CMSG_ACTION_EXCHAGE_COUNT_RETURN                      0x04F9EC54    880B
  CMSG_ACTION_EXCHAGE_GET_REWARD_REQUEST                0x04F9F2D4    200B
  CMSG_ACTION_EXCHAGE_GET_REWARD_RETURN                 0x04F9F4F0    104B
  CMSG_ACTION_EXCHAGE_GIFT_BUY_TIMES_REQUEST            0x04F9FD10    168B
  CMSG_ACTION_EXCHAGE_GIFT_BUY_TIMES_RETURN             0x04F9FFC8    484B
  CMSG_ACTION_EXCHAGE_GIFT_REWARD_REQUEST               0x04F9F830    184B
  CMSG_ACTION_EXCHAGE_GIFT_REWARD_RETURN                0x04F9FA04     88B
  CMSG_ACTION_EXCHANGE_ITEM_REQUEST                     0x053206EC    184B
  CMSG_ACTION_EXCHANGE_ITEM_RETURN                      0x053208C4     88B
  CMSG_ACTIVEGIFTS_ACTION_REQUEST                       0x04FA0A2C     72B
  CMSG_ACTIVEGIFTS_ACTION_RETURN                        0x04FA0DAC    624B
  CMSG_ACTIVEGIFTS_CHANGEGRANDPRIZE_REQUEST             0x04FA1784     88B
  CMSG_ACTIVEGIFTS_CHANGEGRANDPRIZE_RETURN              0x04FA1964    120B
  CMSG_ACTIVEGIFTS_REWARD_REQUEST                       0x04FA06E0    104B
  CMSG_ACTIVEGIFTS_REWARD_RETURN                        0x04FA08CC    120B
  CMSG_ACTIVEGIFTS_SHOWACTION_REQUEST                   0x04FA1104     72B
  CMSG_ACTIVEGIFTS_SHOWACTION_RETURN                    0x04FA1414    592B
  CMSG_ACTIVITY_BUILDING_BUILDING                       0x051864FC    168B
  CMSG_ACTIVITY_BUILDING_BUILDING_RETURN                0x05186C30   1652B
  CMSG_ACTIVITY_BUILDING_INFO                           0x051854F0    152B
  CMSG_ACTIVITY_BUILDING_INFO_RETURN                    0x05185C3C   1548B
  CMSG_ACTIVITY_BUILDING_LOGIN_INFO                     0x051851EC    152B
  CMSG_ACTIVITY_GAIN_REQUEST                            0x051831A4    184B
  CMSG_ACTIVITY_GAIN_RETURN                             0x0518337C     88B
  CMSG_ACTIVITY_GAIN_ROUND_REQUEST                      0x05183BB4    184B
  CMSG_ACTIVITY_GAIN_ROUND_RETURN                       0x05183D88     88B
  CMSG_ACTIVITY_GAIN_SERVER_REQUEST                     0x051836AC    184B
  CMSG_ACTIVITY_GAIN_SERVER_RETURN                      0x05183884     88B
  CMSG_ACTIVITY_GIFT_REWARD_REQUEST                     0x051840B8    184B
  CMSG_ACTIVITY_GIFT_REWARD_RETURN                      0x0518428C     88B
  CMSG_ACTIVITY_LOOP_BOSS_ATTACK                        0x05181CC4    184B
  CMSG_ACTIVITY_LOOP_BOSS_ATTACK_RETURN                 0x051820AC    628B
  CMSG_ACTIVITY_LOOP_BOSS_INFO                          0x05181448    152B
  CMSG_ACTIVITY_LOOP_BOSS_INFO_RETURN                   0x051817D0    540B
  CMSG_ACTIVITY_LOOP_BOSS_LOGIN_INFO                    0x05181154    136B
  CMSG_ACTIVITY_LOOP_SEARCH                             0x0518A414    168B
  CMSG_ACTIVITY_LOOP_SEARCH_INFO                        0x05189C48    152B
  CMSG_ACTIVITY_LOOP_SEARCH_INFO_RETURN                 0x05189F64    508B
  CMSG_ACTIVITY_LOOP_SEARCH_LOGIN_INFO                  0x05189954    136B
  CMSG_ACTIVITY_LOOP_SEARCH_RETURN                      0x0518A748    580B
  CMSG_ACTIVITY_LUCKY_GIFT_START                        0x051D1CA8    780B
  CMSG_ACTIVITY_REWARD_INFO_REQUEST                     0x051825D4    168B
  CMSG_ACTIVITY_REWARD_INFO_RETURN                      0x05182ADC   1008B
  CMSG_ACTIVITY_RUSH_EVENT_RANK_REQUEST                 0x04FA34E0    168B
  CMSG_ACTIVITY_RUSH_EVENT_RANK_RETURN                  0x04FA3AB0   1320B
  CMSG_ACTIVITY_RUSH_EVENT_REWARD_REQUEST               0x04FA3000    184B
  CMSG_ACTIVITY_RUSH_EVENT_REWARD_RETURN                0x04FA31D8     88B
  CMSG_ADD_ACCUMULATION_GIFT                            0x04F9CC0C     72B
  CMSG_ADD_ACCUMULATION_GIFT_NEW_SERVER                 0x04F9CD3C     72B
  CMSG_ADD_AF_OPERATE                                   0x04F9BF00     88B
  CMSG_ADD_CHARGE_DAILY_GIFT                            0x04FD6B24     72B
  CMSG_ADD_CITYDEFENSE_REQUEST                          0x0505BE10     56B
  CMSG_ADD_CUMULATIVE_RECHARGE_GIFT                     0x050130FC     88B
  CMSG_ADD_HONOR_SOUL                                   0x050B9994    548B
  CMSG_ADD_LEAGUEBUILD                                  0x0515ADC0    584B
  CMSG_ADD_LEAGUE_GIFT                                  0x05165928    464B
  CMSG_ADD_LEAGUE_INVITE                                0x050FB500   1432B
  CMSG_ADD_NOVICE_RECHARG_REWARD_GIFT                   0x05260408     88B
  CMSG_ADD_TRIGGER_GIFT_INFO                            0x052E5DC8    104B
  CMSG_AD_SYNC_TIMES                                    0x04FA982C    848B
  CMSG_AD_USE_TIMES_REWARD_REQUEST                      0x04FAA164     88B
  CMSG_AD_USE_TIMES_REWARD_RETURN                       0x04FAA310    104B
  CMSG_AD_WATCHREWARD_REQUEST                           0x04FA9DE0    168B
  CMSG_AD_WATCHREWARD_RETURN                            0x04FA9FDC    104B
  CMSG_AF_INFO                                          0x04F9BBBC    548B
  CMSG_ALIEN_SYNC                                       0x051ED7F8    996B
  CMSG_ALLFORONE_POINT_REQUEST                          0x04FAB890    168B
  CMSG_ALLFORONE_POINT_RETURN                           0x04FABA54     88B
  CMSG_ALLFORONE_REWARD_REQUEST                         0x04FAB3AC    184B
  CMSG_ALLFORONE_REWARD_RETURN                          0x04FAB584     88B
  CMSG_ALL_CAMELS_REQUEST                               0x050547C8     56B
  CMSG_ALL_CAMELS_RETURN                                0x05054A4C    740B
  CMSG_ALL_DOMINION_BUILD_INFO_REQUEST                  0x05047A54     56B
  CMSG_ALL_DOMINION_BUILD_INFO_RETURN                   0x05047D7C   1180B
  CMSG_ANNIVERSARY_DONATE_INFO_REQUEST                  0x0527AB48     56B
  CMSG_ANNIVERSARY_DONATE_REQUEST                       0x0527AF40     72B
  CMSG_ANNIVERSARY_DONATE_RETURN                        0x0527B110    120B
  CMSG_ANNIVERSARY_DONATE_REWARD_REQUEST                0x0527B270     72B
  CMSG_ANNIVERSARY_DONATE_REWARD_RETURN                 0x0527B3D8     88B
  CMSG_ANNIVERSARY_SHARE_REWARD_REQUEST                 0x0527B518     72B
  CMSG_ANNIVERSARY_SHARE_REWARD_RETURN                  0x0527B680     88B
  CMSG_ANSWER_USE_SPECIAL_ITEM                          0x050C1D68    548B
  CMSG_APPEND_SIGN_REQUEST                              0x052C39D8     56B
  CMSG_APPLY_ENTER_LEAGUE                               0x050F83B8    324B
  CMSG_APPLY_ENTER_LEAGUE_EX                            0x050F7F38    324B
  CMSG_APPLY_ENTER_LEAGUE_FAST                          0x050F86F0     56B
  CMSG_APPLY_ENTER_LEAGUE_FAST_RETURN                   0x050F8848     88B
  CMSG_ARENA_BATTLE_RECORD_INFO                         0x04FB0AF8    772B
  CMSG_ARENA_BUY_TIMES_REQUEST                          0x04FAD6DC     56B
  CMSG_ARENA_CHALLENGE_MATCH_REQUEST                    0x04FAE790     72B
  CMSG_ARENA_CHALLENGE_MATCH_RETURN                     0x04FAE8C0     72B
  CMSG_ARENA_CHANGE_MATCH_REQUEST                       0x04FAD7D4     56B
  CMSG_ARENA_CHANGE_MATCH_REQUEST_NEW                   0x04FB1F50    136B
  CMSG_ARENA_CHANGE_MATCH_RETURN                        0x04FADF3C   1816B
  CMSG_ARENA_DELETE_BATTLE_RECORD_REQUEST               0x04FB0F94    420B
  CMSG_ARENA_DELETE_BATTLE_RECORD_RETURN                0x04FB12D0    404B
  CMSG_ARENA_MATCH_INFO_REQUEST                         0x04FAEC1C     56B
  CMSG_ARENA_MATCH_INFO_REQUEST_NEW                     0x04FB1CCC    136B
  CMSG_ARENA_MATCH_INFO_RETURN                          0x04FAF350   1800B
  CMSG_ARENA_RANK_INFO_REQUEST                          0x04FAFB18     56B
  CMSG_ARENA_RANK_INFO_RETURN                           0x04FB00F8   1804B
  CMSG_ARENA_SET_BATTLE_RECORD_FLAG_REQUEST             0x04FB1600    420B
  CMSG_ARENA_SET_BATTLE_RECORD_FLAG_RETURN              0x04FB193C    404B
  CMSG_ARENA_SYS_SETTLEMENT                             0x04FAE9F0    116B
  CMSG_ARENA_TIMES_RESTORE_REQUEST                      0x04FAEB24     56B
  CMSG_AREN_HERO_QUEUE_CHANGE_REQUEST                   0x04FACDC8    504B
  CMSG_AREN_HERO_QUEUE_CHANGE_RETURN                    0x04FAD17C    504B
  CMSG_AREN_HERO_QUEUE_INFO                             0x04FACA14    504B
  CMSG_ARMY_LOSS_REWARD_REQUEST                         0x0505B180     56B
  CMSG_ARMY_LOSS_REWARD_RETURN                          0x0505B370    484B
  CMSG_ATTACK_SECRET_BOSS_REQUEST                       0x052D29A8     72B
  CMSG_ATTACK_SECRET_BOSS_RETURN                        0x052D2C48    544B
  CMSG_ATTACK_SECRET_BOSS_TEN_REQUEST                   0x052D2F50     72B
  CMSG_ATTACK_SECRET_BOSS_TEN_RETURN                    0x052D31F0    544B
  CMSG_ATTRIBUTE_INFO                                   0x04FB9DD8   2436B
  CMSG_AUCTION_BID_REQUEST                              0x04FBDCDC    184B
  CMSG_AUCTION_BID_RETURN                               0x04FBDEEC    104B
  CMSG_AUCTION_INFO_REQUEST                             0x04FBE1C0    152B
  CMSG_AUCTION_INFO_RETURN                              0x04FBE4FC    592B
  CMSG_AUTO_HANDUP_CHANGE_REQUEST                       0x04FC1498    908B
  CMSG_AUTO_HANDUP_CHANGE_RETURN                        0x04FC190C     72B
  CMSG_AUTO_JOIN_BUILDUP_CLOSE_REQUEST                  0x04FC30D4    152B
  CMSG_AUTO_JOIN_BUILDUP_CLOSE_RETURN                   0x04FC322C     56B
  CMSG_AUTO_JOIN_BUILDUP_OPEN_REQUEST                   0x04FC245C   1036B
  CMSG_AUTO_JOIN_BUILDUP_OPEN_RETURN                    0x04FC2B1C    844B
  CMSG_BACK_DEFEND                                      0x05215B34    316B
  CMSG_BACK_DEFEND_KING_CHESS                           0x050C94C0    316B
  CMSG_BACK_DEFEND_NEW                                  0x051399E4    468B
  CMSG_BACK_TRADE_MARCH_REQUEST                         0x0504BCD4    316B
  CMSG_BATTLE_DETAIL_REPORT                             0x051E4B98    552B
  CMSG_BATTLE_DETAIL_REPORT_REQUEST                     0x051E47B0    308B
  CMSG_BATTLE_LEADERID_REQUEST                          0x0510B520     88B
  CMSG_BATTLE_LEADERID_RESPONSE                         0x0510B698     88B
  CMSG_BESTOW_FORTRESS_REWARD_REQUEST                   0x0506F7CC     88B
  CMSG_BESTOW_FORTRESS_REWARD_RETURN                    0x0506FA6C    376B
  CMSG_BESTOW_KING_REWARD_REQUEST                       0x0503F32C     88B
  CMSG_BESTOW_KING_REWARD_RETURN                        0x0503F5CC    376B
  CMSG_BESTOW_LORD_WAR_REWARD_REQUEST                   0x0511C514    104B
  CMSG_BESTOW_LORD_WAR_REWARD_RETURN                    0x0511C808    392B
  CMSG_BOSS_INFO_REQUEST                                0x04FC941C     56B
  CMSG_BOSS_INFO_RETURN                                 0x04FC9570     88B
  CMSG_BOSS_POS_RETURN                                  0x04FC9304     88B
  CMSG_BOSS_SYNC                                        0x051EEA30    816B
  CMSG_BUILDING_BASE_INF                                0x04FCA874     72B
  CMSG_BUILDING_HELP_REQUEST                            0x04FCD1F4     72B
  CMSG_BUILDING_INFO                                    0x04FCABBC    800B
  CMSG_BUILDING_OPERAT_ONEKEY_REQUEST                   0x04FCC0E0    628B
  CMSG_BUILDING_OPERAT_REQUEST                          0x04FCBCAC    136B
  CMSG_BUILDING_OPERAT_REQUEST_FIX_NEW                  0x04FCCCEC    200B
  CMSG_BUILDING_OPERAT_REQUEST_NEW                      0x04FCC768    688B
  CMSG_BUILDING_OPERAT_RETURN                           0x04FCD040    200B
  CMSG_BUILDING_SKIN_REWARD_REQUEST                     0x04FCF198    168B
  CMSG_BUILDING_SKIN_REWARD_RETURN                      0x04FCF328     72B
  CMSG_BUILDING_SKIN_SUIT_REWARD_REQUEST                0x04FCECB4    184B
  CMSG_BUILDING_SKIN_SUIT_REWARD_RETURN                 0x04FCEE8C     88B
  CMSG_BUILDING_SKIN_UPGRADE_LV_REQUEST                 0x04FCE7F4    184B
  CMSG_BUILDING_SKIN_UPGRADE_LV_RETURN                  0x04FCE994     72B
  CMSG_BUYONESHOP_SET_FLAG_REQUEST                      0x04FD1384     72B
  CMSG_BUYONESHOP_SET_FLAG_RETURN                       0x04FD14F0     88B
  CMSG_BUYONESHOP_SET_GIFTID                            0x04FD1254     72B
  CMSG_BUYONESHOP_SYNC_ACTION                           0x04FD04CC    544B
  CMSG_BUYONESHOP_SYNC_GIFTID                           0x04FD1124     72B
  CMSG_BUYONESHOP_SYNC_NEW_ACTION                       0x04FD09F8    544B
  CMSG_BUYONESHOP_SYNC_TIMES                            0x04FD0D38     88B
  CMSG_BUYONESHOP_USE_ITEM_REQUEST                      0x04FD163C     72B
  CMSG_BUYONESHOP_USE_ITEM_RETURN                       0x04FD17A8     88B
  CMSG_BUYONESHOP_USE_TIMES_REQUEST                     0x04FD0E78     72B
  CMSG_BUYONESHOP_USE_TIMES_RETURN                      0x04FD0FE4     88B
  CMSG_BUY_ALIEN_REWARD_TIMES_REQUEST                   0x0505B614     56B
  CMSG_BUY_ALIEN_REWARD_TIMES_RETURN                    0x0505B738     72B
  CMSG_BUY_GIFT_FAIL_TRIGGER_GIFT                       0x05095480    152B
  CMSG_BUY_MOBILIZATION_TASK_TIMES_REQUEST              0x0505B840     56B
  CMSG_BUY_MOBILIZATION_TASK_TIMES_RETURN               0x0505B964     72B
  CMSG_BUY_REWARD_POINT_SHOP_ITEM_REQUEST               0x052B0138    104B
  CMSG_BUY_REWARD_POINT_SHOP_ITEM_RETURN                0x052B0328    120B
  CMSG_BUY_ROYAL_SHOP_ITEM_REQUEST                      0x050B83DC    104B
  CMSG_BUY_ROYAL_SHOP_ITEM_RETURN                       0x050B85CC    120B
  CMSG_CAMEL_SHOP_BUY_REQUEST                           0x04FD22A8    104B
  CMSG_CAMEL_SHOP_BUY_RETURN                            0x04FD2464    104B
  CMSG_CAMEL_SHOP_INFO_REQUEST                          0x04FD19FC     56B
  CMSG_CAMEL_SHOP_REFRESH_REQUEST                       0x04FD258C     56B
  CMSG_CAMEL_SYNC                                       0x051ED104    860B
  CMSG_CANCEL_MARCH                                     0x051EB060     72B
  CMSG_CANCEL_MARCH_NEW                                 0x051F5374    136B
  CMSG_CANNON_BATTLE_DAMAGE                             0x04FD2F64    480B
  CMSG_CANNON_BATTLE_DELETE_RECORD_REQUEST              0x04FD2C80     56B
  CMSG_CANNON_BATTLE_RECORD_INFO                        0x04FD28B8    776B
  CMSG_CANNON_BATTLE_RECORD_SET_FLAG_REQUEST            0x04FD2D78     56B
  CMSG_CASTLE_DUEL                                      0x051F0840    168B
  CMSG_CASTLE_PET_SKILL_BE_USED                         0x051F0574    152B
  CMSG_CASTLE_PET_SKILL_CHANGE_POS                      0x051F00B4    136B
  CMSG_CASTLE_PET_SKILL_SLOW_MARCH                      0x051F02F8    136B
  CMSG_CASTLE_SYNC                                      0x051EBE50   2060B
  CMSG_CASTLE_THUNDER                                   0x051EFE60    152B
  CMSG_CHANGE_AMRY_SKIN_REQUEST                         0x04FAC190     72B
  CMSG_CHANGE_AMRY_SKIN_RETURN                          0x04FAC2F4     88B
  CMSG_CHANGE_AVATAR_REQUEST                            0x0505AF70     88B
  CMSG_CHANGE_BUILDING_SKIN_REQUEST                     0x04FCE2A4    184B
  CMSG_CHANGE_BUILDING_SKIN_RETURN                      0x04FCE4B0    104B
  CMSG_CHANGE_CHAT_BOX                                  0x04FBB658     72B
  CMSG_CHANGE_CHAT_BUBBLE                               0x04FBB788     72B
  CMSG_CHANGE_HONOR_FLAG_REQUEST                        0x04FBC5B4     72B
  CMSG_CHANGE_HONOR_FLAG_RETURN                         0x04FBC6E4     72B
  CMSG_CHANGE_LEADERFLAG_REQUEST                        0x04FBC354     72B
  CMSG_CHANGE_LEADERFLAG_RETURN                         0x04FBC484     72B
  CMSG_CHANGE_LEAGUE_LEADER                             0x050FFFAC     72B
  CMSG_CHANGE_LEAGUE_MEMBER_LEVEL_NAME                  0x050F9128    324B
  CMSG_CHANGE_LEAGUE_POSTION                            0x0510037C     88B
  CMSG_CHANGE_LEGION_CHANGE_NAME_REQUEST                0x05119A40    324B
  CMSG_CHANGE_LEGION_CHANGE_NAME_RETURN                 0x05119D74    340B
  CMSG_CHANGE_LEGION_POSTION                            0x051192B4    120B
  CMSG_CHANGE_LORD_HEAD                                 0x04FBB528     72B
  CMSG_CHANGE_MEMBER_POWER                              0x050FFE68     88B
  CMSG_CHANGE_NAMEPLATE_REQUEST                         0x05279BB8     72B
  CMSG_CHANGE_NAMEPLATE_RETURN                          0x05279D1C     88B
  CMSG_CHANGE_NAME_REQUEST                              0x04FBA94C    340B
  CMSG_CHANGE_NAME_RETURN                               0x04FBAC60    344B
  CMSG_CHANGE_PUSH_REQUEST                              0x05284768     88B
  CMSG_CHANGE_SERVER_FLAG_REQUEST                       0x0527CA00     72B
  CMSG_CHANGE_SERVER_NAME_REQUEST                       0x0527C7E4    308B
  CMSG_CHANGE_SIGNATURE_REQUEST                         0x04FBBAC4    324B
  CMSG_CHANGE_SIGNATURE_RETURN                          0x04FBBE00    360B
  CMSG_CHANGE_SKIN_REQUEST                              0x052C5260     72B
  CMSG_CHANGE_SKIN_RETURN                               0x052C53C4     88B
  CMSG_CHARGE_DAILY_INFO                                0x04FD6238    948B
  CMSG_CHARGE_DAILY_REWARD_REQUEST                      0x04FD690C     56B
  CMSG_CHARGE_DAILY_REWARD_RETURN                       0x04FD6A04     56B
  CMSG_CHARGE_DAILY_SING_REQUEST                        0x04FD66D4     72B
  CMSG_CHARGE_DAILY_SING_RETURN                         0x04FD6804     72B
  CMSG_CHARGE_INFO                                      0x05092614    752B
  CMSG_CHAT_ADD_BOX_RETURN                              0x04FDBD04     72B
  CMSG_CHAT_ADD_BUBBLE_RETURN                           0x04FDBE68     88B
  CMSG_CHAT_BLOCK                                       0x04FD6F6C   1048B
  CMSG_CHAT_CONTACT_OPERATION                           0x04FDB13C    336B
  CMSG_CHAT_DEL_INVALID_MSG                             0x04FDD448     88B
  CMSG_CHAT_ERROR                                       0x04FDD158     88B
  CMSG_CHAT_HISTORY                                     0x04FD7EBC   2672B
  CMSG_CHAT_NAME_ERROR_RETURN                           0x04FDC7C8     56B
  CMSG_CHAT_READ_SHARE_MAIL                             0x04FDC9F4    160B
  CMSG_CHAT_READ_SHARE_MAIL_RESULT                      0x04FDCDBC    636B
  CMSG_CHAT_SEND                                        0x04FDB794    856B
  CMSG_CHAT_SEND_RETURN                                 0x04FDC690    120B
  CMSG_CHAT_SET_BLOCK_CONDITION_REQUEST                 0x04FE3570    120B
  CMSG_CHAT_SET_BLOCK_CONDITION_RETURN                  0x04FE3774    120B
  CMSG_CHAT_SHARE_CD                                    0x04FDD2D0     88B
  CMSG_CHAT_SYNC_BLOCK_CONDITION                        0x04FE3A08    672B
  CMSG_CHAT_SYNC_BOX_BUBBLE                             0x04FDC184    900B
  CMSG_CHAT_UPDATE_WORLD_BATTLE_FLAG                    0x04FDBBD4     72B
  CMSG_CHAT_USEITEM_ADDBOX_REQUEST                      0x04FE3D90     72B
  CMSG_CITY_BUFF_GET_USE                                0x0527C4C0    104B
  CMSG_CITY_BUFF_GET_USE_RETURN                         0x0527C610     72B
  CMSG_CITY_BUFF_USE                                    0x0527C2FC    104B
  CMSG_CLANPK_ACTIVITY_INFO_REQUEST                     0x04FF4674    152B
  CMSG_CLANPK_ACTIVITY_INFO_RETURN                      0x04FF48B4    120B
  CMSG_CLANPK_ACTIVITY_VIEW_RETURN                      0x04FED5A4    204B
  CMSG_CLANPK_ADD_KILL_VALUE                            0x04FF28B4     72B
  CMSG_CLANPK_ASSIST_HERO_REQUEST                       0x04FEEF44    152B
  CMSG_CLANPK_ASSIST_HERO_RETURN                        0x04FEF918   3924B
  CMSG_CLANPK_ATTACK_BUILDING_BEGIN                     0x05004350     72B
  CMSG_CLANPK_ATTACK_BUILDING_END                       0x05004634    200B
  CMSG_CLANPK_BATTLE_RECORD_REQUEST                     0x04FED8DC    152B
  CMSG_CLANPK_BATTLE_RECORD_RETURN                      0x04FEE324   2132B
  CMSG_CLANPK_BUILDING_DETAIL_REQUEST                   0x04FFAF20    184B
  CMSG_CLANPK_BUILDING_DETAIL_RETURN                    0x04FFB0F8     88B
  CMSG_CLANPK_BUILDING_REQUEST                          0x04FF4B98    152B
  CMSG_CLANPK_BUILDING_RETURN                           0x04FF50C4   1364B
  CMSG_CLANPK_BUILD_UPGRADE_REQUEST                     0x04FF860C    200B
  CMSG_CLANPK_BUILD_UPGRADE_RETURN                      0x04FF8888    136B
  CMSG_CLANPK_CHAT_HISTORY                              0x04FDA6A0   2252B
  CMSG_CLANPK_CHECK_SET_DEF_REQUEST                     0x04FE5F24    152B
  CMSG_CLANPK_CHECK_SET_DEF_RETURN                      0x04FE60A4     72B
  CMSG_CLANPK_DEFEND_AMRY_REQUEST                       0x04FEBCB8    168B
  CMSG_CLANPK_DEFEND_AMRY_RETURN                        0x04FEC5AC   2764B
  CMSG_CLANPK_DEFEND_BUILDING_REQUEST                   0x04FEAB6C    184B
  CMSG_CLANPK_DEFEND_BUILDING_RETURN                    0x04FEB3C0   1604B
  CMSG_CLANPK_DONATE_REQUEST                            0x04FF8C24    200B
  CMSG_CLANPK_DONATE_RETURN                             0x04FF8E78    120B
  CMSG_CLANPK_FIRST_LEVEL_REWARD_REQUEST                0x05005118    168B
  CMSG_CLANPK_FIRST_LEVEL_REWARD_RETURN                 0x050052A8     72B
  CMSG_CLANPK_GIVE_ASSIST_HERO_REQUEST                  0x04FF22A4    168B
  CMSG_CLANPK_GIVE_ASSIST_HERO_RETURN                   0x04FF2468     88B
  CMSG_CLANPK_LEVEL_RANK_VIEW_REQUEST                   0x04FF2BB0    168B
  CMSG_CLANPK_LEVEL_RANK_VIEW_RETURN                    0x04FF3134   1300B
  CMSG_CLANPK_MAILBOX_MAIL                              0x05003CDC   1416B
  CMSG_CLANPK_MAILBOX_MAIL_REQUEST                      0x05003628    184B
  CMSG_CLANPK_QUERY_ATTACK_INFO                         0x04FFCF88    152B
  CMSG_CLANPK_QUERY_DEFEND_INFO                         0x04FFB42C    184B
  CMSG_CLANPK_SET_ASSIST_HERO_REQUEST                   0x04FF0B48    184B
  CMSG_CLANPK_SET_ASSIST_HERO_RETURN                    0x04FF15FC   2548B
  CMSG_CLANPK_SET_ATTACK_HERO_REQUEST                   0x04FFA1FC    980B
  CMSG_CLANPK_SET_ATTACK_HERO_RETURN                    0x04FFA8B0    916B
  CMSG_CLANPK_SET_DEFEND_HERO_REQUEST                   0x04FF9350    980B
  CMSG_CLANPK_SET_DEFEND_HERO_RETURN                    0x04FF9A08    916B
  CMSG_CLANPK_SIGNUP_REQUEST                            0x04FEA6B4    168B
  CMSG_CLANPK_SIGNUP_RETURN                             0x04FEA844     72B
  CMSG_CLANPK_START_ATTACK                              0x05002A64    168B
  CMSG_CLANPK_START_ATTACK_RETURN                       0x05002C2C     88B
  CMSG_CLANPK_START_DEFEND                              0x05002F38    168B
  CMSG_CLANPK_START_DEFEND_RETURN                       0x05003278    212B
  CMSG_CLANPK_THUNDER_ATTACK_BEGIN                      0x050049B0    168B
  CMSG_CLANPK_THUNDER_ATTACK_END                        0x05004B78     88B
  CMSG_CLANPK_UPDATE_ASSIST_HERO                        0x04FF2684    324B
  CMSG_CLANPK_UPDATE_BUILDING_INFO                      0x05004DCC    152B
  CMSG_CLANPK_USER_RANK_VIEW_REQUEST                    0x04FF38F4    168B
  CMSG_CLANPK_USER_RANK_VIEW_RETURN                     0x04FF3EBC   1356B
  CMSG_CLIENT_LOG                                       0x0527D06C    308B
  CMSG_CLIENT_OFFLINE_PLAYER                            0x0527CEA8     56B
  CMSG_CLIENT_TRIGGER_GIFT                              0x052E5F18     72B
  CMSG_COLLECTION_DELETE_RECORD_REQUEST                 0x0500DDD4     56B
  CMSG_COLLECTION_RECORD_INFO                           0x0500DA0C    776B
  CMSG_COLLECTION_RECORD_SET_FLAG_REQUEST               0x0500DECC     56B
  CMSG_COMMON_ACTION_PLAYER_RANK_REQUEST                0x052F3034    168B
  CMSG_COMMON_ACTION_PLAYER_RANK_RETURN                 0x052F3510   1192B
  CMSG_COMMON_ACTION_SELF_RANK_REQUEST                  0x052F3C6C    168B
  CMSG_COMMON_ACTION_SELF_RANK_RETURN                   0x052F3E34     88B
  CMSG_COMMON_EXCHAGE_COUNT_REQUEST                     0x0500E984     72B
  CMSG_COMMON_EXCHAGE_COUNT_RETURN                      0x0500ECB4   1000B
  CMSG_COMMON_EXCHAGE_GET_REWARD_REQUEST                0x0500F1F0    104B
  CMSG_COMMON_EXCHAGE_GET_REWARD_RETURN                 0x0500F3AC    104B
  CMSG_COMPLETE_GUIDE_REQUEST                           0x0505F4D8     88B
  CMSG_CONTINUITY_GIFTPACK_ACTION_REQUEST               0x0500F8F0     72B
  CMSG_CONTINUITY_GIFTPACK_ACTION_RETURN                0x0500FB00    136B
  CMSG_CONTINUITY_GIFTPACK_DISCOUNT_REQUEST             0x050105F4     88B
  CMSG_CONTINUITY_GIFTPACK_DISCOUNT_RETURN              0x050107A4    104B
  CMSG_CONTINUITY_GIFTPACK_GOLDBUY_REQUEST              0x0500FEAC     88B
  CMSG_CONTINUITY_GIFTPACK_GOLDBUY_RETURN               0x050100CC    136B
  CMSG_CONTINUITY_GIFTPACK_POINT_REQUEST                0x05010274     88B
  CMSG_CONTINUITY_GIFTPACK_POINT_RETURN                 0x0501045C    120B
  CMSG_CONTINUOUS_TASK_ACTION_REQUEST                   0x0501100C    168B
  CMSG_CONTINUOUS_TASK_ACTION_RETURN                    0x0501133C    512B
  CMSG_CONTINUOUS_TASK_REWARD_REQUEST                   0x0501198C    184B
  CMSG_CONTINUOUS_TASK_REWARD_RETURN                    0x05011B64     88B
  CMSG_CREATE_LEAGUE                                    0x050F2A78    500B
  CMSG_CUMULATIVE_RECHARGE_RECEIVE_REWARD_REQUEST       0x05012858    184B
  CMSG_CUMULATIVE_RECHARGE_RECEIVE_REWARD_RETURN        0x05012A60    104B
  CMSG_CUSTOMGIFTS_ACTION_REQUEST                       0x050137E8     72B
  CMSG_CUSTOMGIFTS_ACTION_RETURN                        0x05013D28   1992B
  CMSG_CUSTOMGIFTS_CHANGEREWARD_REQUEST                 0x0501467C    120B
  CMSG_CUSTOMGIFTS_CHANGEREWARD_RETURN                  0x050148E8    152B
  CMSG_CUSTOM_HEAD_CHANGE_HEAD_REQUEST                  0x05015670    596B
  CMSG_CUSTOM_HEAD_CHANGE_HEAD_RETURN                   0x05015B28    516B
  CMSG_CUSTOM_HEAD_REQUEST                              0x0501684C    912B
  CMSG_CUSTOM_HEAD_RETURN                               0x05016EF0   1016B
  CMSG_CUSTOM_HEAD_UPLOAD_HEAD_REQUEST                  0x050160D4    596B
  CMSG_CUSTOM_HEAD_UPLOAD_HEAD_RETURN                   0x050163E8     56B
  CMSG_CUSTOM_HEAD_VIOLATION                            0x050174B8    308B
  CMSG_CYCLE_ACTION_RANK_RECORD_REQUEST                 0x0501B680     72B
  CMSG_CYCLE_ACTION_RANK_RECORD_RETURN                  0x0501BB24   1396B
  CMSG_DAILYCONSUME_ACTION_REQUEST                      0x050232C0     72B
  CMSG_DAILYCONSUME_ACTION_RETURN                       0x0502353C    476B
  CMSG_DAILYCONSUME_REWARD_REQUEST                      0x05022FC4     88B
  CMSG_DAILYCONSUME_REWARD_RETURN                       0x05023170    104B
  CMSG_DAILY_RECHARGE_GET_REWARD_REQUEST                0x0505D2D0    152B
  CMSG_DAILY_RECHARGE_GET_REWARD_RETURN                 0x0505D454     72B
  CMSG_DAILY_RECHARGE_POINT                             0x050251CC     72B
  CMSG_DAILY_RECHARGE_REWARD_REQUEST                    0x05024C60     88B
  CMSG_DAILY_RECHARGE_REWARD_RETURN                     0x05024ED8    524B
  CMSG_DAILY_TASKS_FACEBOOK_SHARE                       0x05025BC4     56B
  CMSG_DAILY_TASKS_REWARD_REQUEST                       0x05025944     72B
  CMSG_DAILY_TASKS_REWARD_RETURN                        0x05025AAC     88B
  CMSG_DAILY_VIP_REWARD_REQUEST                         0x0506016C     56B
  CMSG_DAMAGE_BUY                                       0x0502969C    168B
  CMSG_DAMAGE_BUY_ITEM                                  0x05029BCC    200B
  CMSG_DAMAGE_BUY_ITEM_RETURN                           0x05029DB4     88B
  CMSG_DAMAGE_BUY_RETURN                                0x05029864     88B
  CMSG_DAMAGE_GIFT_INFO                                 0x050282E4    216B
  CMSG_DAMAGE_GIFT_INFO_RETURN                          0x05028860   1176B
  CMSG_DAMAGE_HELP                                      0x05029070    232B
  CMSG_DAMAGE_HELP_NOTIFY                               0x0502A434    104B
  CMSG_DAMAGE_HELP_RETURN                               0x05029350    152B
  CMSG_DAMAGE_SHARE                                     0x0502A0C0    168B
  CMSG_DAMAGE_SHARE_RETURN                              0x0502A288     88B
  CMSG_DAY_REFRESH_REQUEST                              0x052C2ED8     56B
  CMSG_DELETE_GENERAL_ACTIBITIES_ACTION_DATA            0x050898F4    308B
  CMSG_DELETE_GENERAL_ACTIBITIES_INFO                   0x05089640    308B
  CMSG_DELETE_LEAGUEBUILD                               0x0515BD1C    456B
  CMSG_DELETE_QUEST                                     0x05285AD8     72B
  CMSG_DELETE_REWARD_TASK_HERO_REQUEST                  0x0517685C     72B
  CMSG_DELETE_REWARD_TASK_HERO_RETURN                   0x05176A78    424B
  CMSG_DELETE_REWARD_TASK_REQUEST                       0x051765FC     72B
  CMSG_DELETE_REWARD_TASK_RETURN                        0x0517672C     72B
  CMSG_DEL_FAVORITE_REQUEST                             0x05064F60    104B
  CMSG_DEL_FAVORITE_RETURN                              0x0506511C    104B
  CMSG_DEL_LEAGUE_HELP                                  0x0516797C    120B
  CMSG_DEL_LEAGUE_HELP_FLAG                             0x051689D0    104B
  CMSG_DESERT_TRADE_QUERY_BATTLE_RECORD_REQUEST         0x05032280    184B
  CMSG_DESERT_TRADE_QUERY_BATTLE_RECORD_RETURN          0x05032598    624B
  CMSG_DESERT_TRADE_QUERY_HELP_RECORD_REQUEST           0x05034C18    168B
  CMSG_DESERT_TRADE_QUERY_HELP_RECORD_RETURN            0x05035078   1076B
  CMSG_DESERT_TRADE_QUERY_LEAGUE_HELP_REQUEST           0x05032ABC    168B
  CMSG_DESERT_TRADE_QUERY_LEAGUE_HELP_RETURN            0x05032F8C   1728B
  CMSG_DESERT_TRADE_QUERY_TRUCK_INFO_REQUEST            0x050305CC    216B
  CMSG_DESERT_TRADE_QUERY_TRUCK_INFO_RETURN             0x050311B8   3560B
  CMSG_DESERT_TRADE_RECEIVE_TRUCK_REWARD_REQUEST        0x05033928    184B
  CMSG_DESERT_TRADE_RECEIVE_TRUCK_REWARD_RETURN         0x05033C48    568B
  CMSG_DESERT_TRADE_REFRESH_TRUCK_REQUEST               0x0502D960    200B
  CMSG_DESERT_TRADE_REFRESH_TRUCK_RETURN                0x0502DE30   1304B
  CMSG_DESERT_TRADE_ROBBERY_REQUEST                     0x0502F004    564B
  CMSG_DESERT_TRADE_ROBBERY_RETURN                      0x0502F4A0    568B
  CMSG_DESERT_TRADE_SEARCH_TRUCK_REQUEST                0x0502F98C    168B
  CMSG_DESERT_TRADE_SEARCH_TRUCK_RETURN                 0x0502FEA0    992B
  CMSG_DESERT_TRADE_SET_HELP_HERO_REQUEST               0x0502D04C    508B
  CMSG_DESERT_TRADE_SET_HELP_HERO_RETURN                0x0502D47C    476B
  CMSG_DESERT_TRADE_START_MARCH_REQUEST                 0x0502E724    548B
  CMSG_DESERT_TRADE_START_MARCH_RETURN                  0x0502EB3C    152B
  CMSG_DESERT_TRADE_SYNC_INFO                           0x0502BA54   4740B
  CMSG_DESERT_TRADE_TRUCK_ROBBERY_TIMES_REQUEST         0x05034230    608B
  CMSG_DESERT_TRADE_TRUCK_ROBBERY_TIMES_RETURN          0x050346F4    624B
  CMSG_DESERT_TRADE_UPDATE_ROBBED_TIMES                 0x05035600    104B
  CMSG_DESSERT_ACTION_COOKING_REQUEST                   0x0503B5DC     56B
  CMSG_DESSERT_ACTION_COOKING_RETURN                    0x0503B6D4     56B
  CMSG_DESSERT_ACTION_GET_REWARD_REQUEST                0x0503B7CC     56B
  CMSG_DESSERT_ACTION_GET_REWARD_RETURN                 0x0503B924     88B
  CMSG_DESSERT_ACTION_RESET_ALL_REWARD_REQUEST          0x0503BA3C     56B
  CMSG_DESSERT_ACTION_RESET_ALL_REWARD_RETURN           0x0503BB5C     72B
  CMSG_DESSERT_ACTION_RESET_REWARD_REQUEST              0x0503B3A4     72B
  CMSG_DESSERT_ACTION_RESET_REWARD_RETURN               0x0503B4D4     72B
  CMSG_DESSERT_ACTION_REWARD_INFO_REQUEST               0x0503A400     56B
  CMSG_DESSERT_ACTION_REWARD_INFO_RETURN                0x0503A81C   1276B
  CMSG_DESSERT_ACTION_SET_REWARD_REQUEST                0x0503AF28    668B
  CMSG_DESSERT_ACTION_SET_REWARD_RETURN                 0x0503B284     56B
  CMSG_DINAR_BACK_INFO                                  0x0503BD98    556B
  CMSG_DOMINION_ACTION_END                              0x0503DD34    500B
  CMSG_DOMINION_ACTION_SET_SLAVE_REQUEST                0x0503E044     88B
  CMSG_DOMINION_ACTION_SET_SLAVE_RETURN                 0x0503E364    432B
  CMSG_DOMINION_BUILD_ACCELERATE                        0x050492F4     88B
  CMSG_DOMINION_BUILD_ACCELERATE_NEW                    0x05049438     72B
  CMSG_DOMINION_BUILD_INFO                              0x05048474    564B
  CMSG_DOMINION_BUILD_PLAYER_INFO                       0x05048790     72B
  CMSG_DOMINION_BUILD_UPGRADE                           0x05049048     88B
  CMSG_DOMINION_CHANGE_HAND                             0x05044550    308B
  CMSG_DOMINION_DISCARD                                 0x0504918C     72B
  CMSG_DOMINION_LATEST_REQUEST                          0x05043D5C     72B
  CMSG_DOMINION_LATEST_RETURN                           0x050440AC    792B
  CMSG_DOMINION_SYNC                                    0x051F1CB0   1504B
  CMSG_DOMINION_TRADE_DEL                               0x05052024     72B
  CMSG_DOMINION_TRADE_KICK_DEL                          0x05052188     88B
  CMSG_DOMINION_TRADE_NEW                               0x05051E00    312B
  CMSG_DOMINION_TRADE_SYNC                              0x05052338    104B
  CMSG_DOUBLE_LOTTERY_CONFIG_INFO                       0x05052E30    508B
  CMSG_DOUBLE_LOTTERY_PLAY_REQUEST                      0x05053370    216B
  CMSG_DOUBLE_LOTTERY_PLAY_RETURN                       0x05053640    152B
  CMSG_DOUBLE_LOTTERY_REWARD_HISTORY_REQUEST            0x05053E90    152B
  CMSG_DOUBLE_LOTTERY_REWARD_HISTORY_RETURN             0x050541D4    760B
  CMSG_DOUBLE_LOTTERY_SHOP_BUY_REQUEST                  0x050539E4    200B
  CMSG_DOUBLE_LOTTERY_SHOP_BUY_RETURN                   0x05053BCC     88B
  CMSG_DOWN_LOAD_REWARD_REQUEST                         0x05060074     56B
  CMSG_DO_LEAGUE_DONATE_CRIT                            0x05048EE0     72B
  CMSG_DO_LEAGUE_DONATE_CRIT_NEW_REQUEST                0x051787BC     88B
  CMSG_DO_LEAGUE_DONATE_CRIT_NEW_REQUEST_NEW            0x05178A7C    168B
  CMSG_DO_LEAGUE_DONATE_CRIT_NEW_RETURN                 0x05178C7C    104B
  CMSG_DRIVE_CAMEL_REQUEST                              0x05054FD0    536B
  CMSG_DRIVE_CAMEL_RETURN                               0x0505530C     88B
  CMSG_EFFECT_INFO                                      0x052DA640    480B
  CMSG_EMPLOY_WORKER_REQUEST                            0x04FCB7D0     88B
  CMSG_ENABLE_DOMINION_DEFEND                           0x0510411C     72B
  CMSG_ENABLE_VIEW                                      0x051EB3D4     72B
  CMSG_ENABLE_VIEW_NEW                                  0x051F5660    168B
  CMSG_ENERGY_CD_END                                    0x0505C2A8     56B
  CMSG_ENTER_CLANPK_REQUEST                             0x04FF5884    152B
  CMSG_ENTER_CLANPK_RETURN                              0x04FF6444   2512B
  CMSG_ENTER_CLANPK_VIEW                                0x04FED2E4    152B
  CMSG_ENTER_FORTRESS_REQUEST                           0x0506BB74     56B
  CMSG_ENTER_FORTRESS_VIEW                              0x05068790     56B
  CMSG_ENTER_GAME_REQUEST                               0x0517BF4C    448B
  CMSG_ENTER_GAME_RETURN                                0x0517C1F4     72B
  CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST                 0x051117F4     56B
  CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW                    0x0511017C     56B
  CMSG_ENTER_LOSTLAND_ERROR_RETURN                      0x051ABBD0    104B
  CMSG_ENTER_LOSTLAND_REQUEST                           0x051ABA44     56B
  CMSG_ENTER_LOSTLAND_VIEW                              0x051A88C8     56B
  CMSG_EVERY_DAY_GIFTPACK_INFO                          0x050906F4     88B
  CMSG_EVERY_DAY_GIFTPACK_INFO_NEW                      0x05095638     88B
  CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST                0x0509080C     56B
  CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST_NEW            0x05095750     56B
  CMSG_EVERY_DAY_GIFTPACK_REWARD_RETURN                 0x05090904     56B
  CMSG_EVERY_DAY_GIFTPACK_REWARD_RETURN_NEW             0x05095848     56B
  CMSG_EXCHANGE_BUILDING_REQUEST                        0x04FCD3F8    584B
  CMSG_EXCHANGE_BUILDING_RETURN                         0x04FCD700     56B
  CMSG_EXIT_BUILDUP                                     0x051092EC     72B
  CMSG_EXIT_CLANPK_REQUEST                              0x04FF7080    152B
  CMSG_EXIT_FORTRESS_REQUEST                            0x0506BC6C     56B
  CMSG_EXIT_LEAGUE                                      0x05102EB8     56B
  CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST                  0x051118EC     56B
  CMSG_EXIT_LOSTLAND_REQUEST                            0x051ABCF8     56B
  CMSG_EXPEDITION_BATTLE_REQUEST                        0x0523EA8C    504B
  CMSG_EXPEDITION_BUILDUP_REQUEST                       0x0523EE9C    552B
  CMSG_EXPEDITION_INFO_REQUEST                          0x0523DA0C     56B
  CMSG_EXPEDITION_INFO_RETURN                           0x0523E1B0   1272B
  CMSG_EXTRA_ATTRIBUTE_INFO                             0x0505DA18    484B
  CMSG_EXTRA_GIFTPACK_ACTION_REQUEST                    0x050615B0     72B
  CMSG_EXTRA_GIFTPACK_ACTION_REQUEST_NEW                0x05062A08     72B
  CMSG_EXTRA_GIFTPACK_ACTION_RETURN                     0x050619D0    964B
  CMSG_EXTRA_GIFTPACK_ACTION_RETURN_NEW                 0x05062F28   2140B
  CMSG_EXTRA_GIFTPACK_REWARD_REQUEST                    0x05061264    104B
  CMSG_EXTRA_GIFTPACK_REWARD_REQUEST_NEW                0x05062668    120B
  CMSG_EXTRA_GIFTPACK_REWARD_RETURN                     0x05061450    120B
  CMSG_EXTRA_GIFTPACK_REWARD_RETURN_NEW                 0x05062898    136B
  CMSG_FAVORITE_INFO_REQUEST                            0x05063F54     56B
  CMSG_FAVORITE_INFO_RETURN                             0x050642D4    816B
  CMSG_FB_INVITE_REWARD_REQUEST                         0x050BBF1C     72B
  CMSG_FB_INVITE_REWARD_RESP                            0x050BC084     88B
  CMSG_FIGHT_RECORD_REQUEST                             0x05065244     56B
  CMSG_FIREWORKS_SYNC                                   0x051EFC04    104B
  CMSG_FIXED_TIME_REQUEST                               0x0505F964     72B
  CMSG_FIXED_TIME_RETURN                                0x0505FAC4     88B
  CMSG_FOG_MINE_STORAGE_INFO                            0x04FCD94C    480B
  CMSG_FORTRESS_ACTIVITY_VIEW_RETURN                    0x05068CCC   1188B
  CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_REQUEST          0x0506E634     56B
  CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_RETURN           0x0506EBF4   2748B
  CMSG_FORTRESS_DOMINION_OCCUPY                         0x0506DFF4     72B
  CMSG_FORTRESS_FORCE_REQUEST                           0x0506BD64     56B
  CMSG_FORTRESS_FORCE_RETURN                            0x0506C168   1108B
  CMSG_FORTRESS_LEVEL_RANK_VIEW_REQUEST                 0x0506A6C4     72B
  CMSG_FORTRESS_LEVEL_RANK_VIEW_RETURN                  0x0506AB6C   1244B
  CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_REQUEST            0x0506B130     72B
  CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_RETURN             0x0506B5D8   1244B
  CMSG_FORTRESS_MAPINFO_REQUEST                         0x0506CCD0     56B
  CMSG_FORTRESS_MAPINFO_RESPONSE                        0x0506D4B4   2512B
  CMSG_FORTRESS_RANK_VIEW_REQUEST                       0x050694D8     56B
  CMSG_FORTRESS_RANK_VIEW_RETURN                        0x05069904   1180B
  CMSG_FORTRESS_RESOURCE_REQUEST                        0x0506E0FC     56B
  CMSG_FORTRESS_RESOURCE_RETURN                         0x0506E330    580B
  CMSG_FORTRESS_SIGNUP_REQUEST                          0x05069290     88B
  CMSG_FORTRESS_SIGNUP_RETURN                           0x050693D0     72B
  CMSG_FORTRESS_USER_VALUE_REQUEST                      0x05069E60     56B
  CMSG_FORTRESS_USER_VALUE_RETURN                       0x0506A22C    944B
  CMSG_FREE_WISHES                                      0x052F5C10     88B
  CMSG_FREE_WISHES_RETURN                               0x052F5D88     88B
  CMSG_FRIEND_ACCEPT_REQUEST                            0x0507E8F8     88B
  CMSG_FRIEND_ACCEPT_RESULT                             0x05080BA8    368B
  CMSG_FRIEND_ACCEPT_RETURN                             0x0507EF78   1700B
  CMSG_FRIEND_APPLY_ADD_REQUEST                         0x0507E3E0    324B
  CMSG_FRIEND_APPLY_VIEW_REQUEST                        0x0507C7CC     56B
  CMSG_FRIEND_APPLY_VIEW_RETURN                         0x0507CCC8   1432B
  CMSG_FRIEND_DELETE_REQUEST                            0x0507E610     72B
  CMSG_FRIEND_DELETE_RETURN                             0x0507E77C     88B
  CMSG_FRIEND_RECV_GIFT_COUNT_REQUEST                   0x0508084C     56B
  CMSG_FRIEND_RECV_GIFT_COUNT_RETURN                    0x0508096C     72B
  CMSG_FRIEND_REJECTED_RETURN                           0x0507FA48     72B
  CMSG_FRIEND_REJECT_REQUEST                            0x0507F740     88B
  CMSG_FRIEND_REJECT_RETURN                             0x0507F8F4    104B
  CMSG_FRIEND_SEARCH_REQUEST                            0x0507D634    376B
  CMSG_FRIEND_SEARCH_RETURN                             0x0507DC94   1416B
  CMSG_FRIEND_SEND_GIFT_REQUEST                         0x0507FB7C     72B
  CMSG_FRIEND_SEND_GIFT_RETURN                          0x0507FCE8     88B
  CMSG_FRIEND_VIEW_REQUEST                              0x0507BC28     56B
  CMSG_FRIEND_VIEW_RETURN                               0x0507C15C   1456B
  CMSG_FTRIEND_GIFT_PRESEND_HISTORY_REQUEST             0x0509471C     56B
  CMSG_FTRIEND_GIFT_PRESEND_HISTORY_RETURN              0x05094B5C   1616B
  CMSG_FTRIEND_GIFT_PRESEND_REQUEST                     0x050940CC   1120B
  CMSG_FTRIEND_GIFT_PRESEND_RETURN                      0x05094614     72B
  CMSG_GAIN_EXP_REWARD_REQUEST                          0x04FD4DDC     72B
  CMSG_GAIN_EXP_REWARD_RETURN                           0x04FD4F48     88B
  CMSG_GAIN_REWARD_REQUEST                              0x05285C08     72B
  CMSG_GAIN_REWARD_REQUEST_CHAMPIONSHIP                 0x04FD465C    536B
  CMSG_GAIN_REWARD_RSP                                  0x05285DA4    104B
  CMSG_GAIN_REWARD_RSP_CHAMPIONSHIP                     0x04FD4ACC    552B
  CMSG_GENERAL_ACTIBITIES_DISPRITY_RANK_REQUEST         0x0508A0D4    168B
  CMSG_GENERAL_ACTIBITIES_DISPRITY_RANK_RETURN          0x0508A30C    120B
  CMSG_GENERAL_ACTIBITIES_PLAYER_RANK_REQUEST           0x05088270    168B
  CMSG_GENERAL_ACTIBITIES_PLAYER_RANK_RETURN            0x0508874C   1192B
  CMSG_GENERAL_ACTIBITIES_SELF_RANK_REQUEST             0x05088EA8    168B
  CMSG_GENERAL_ACTIBITIES_SELF_RANK_RETURN              0x05089070     88B
  CMSG_GET_DOMINION_MARCH_REQUEST                       0x0504C19C     72B
  CMSG_GET_DOMINION_MARCH_RETURN                        0x0504C610    468B
  CMSG_GET_DOMINION_TRADE_BASE_REQUEST                  0x05050BA0     56B
  CMSG_GET_DOMINION_TRADE_BASE_RETURN                   0x05050D9C    136B
  CMSG_GET_DOMINION_TRADE_NEW_REQUEST                   0x0504AB64    316B
  CMSG_GET_DOMINION_TRADE_NEW_RETURN                    0x0504AEF0    712B
  CMSG_GET_DOMINION_TRADE_REQUEST                       0x0504A778     72B
  CMSG_GET_DOMINION_TRADE_RETURN                        0x0504A950    120B
  CMSG_GET_HALF_MONTHCARD_ITEM_REQUEST                  0x0505FE4C     56B
  CMSG_GET_HALF_MONTHCARD_ITEM_RETURN                   0x0505FF6C     72B
  CMSG_GET_LEAGUE_TRADE_INFO_REQUEST                    0x0504F4C0     56B
  CMSG_GET_LEAGUE_TRADE_INFO_RETURN                     0x0504FA6C   1092B
  CMSG_GET_LORD_GROW_AWARD_REQUEST                      0x0519B674    104B
  CMSG_GET_LORD_GROW_AWARD_RETURN                       0x0519B92C    544B
  CMSG_GET_MAP_TRADE_REQUEST                            0x0504B2A0     72B
  CMSG_GET_MAP_TRADE_RETURN                             0x0504B610    564B
  CMSG_GET_MYSELF_EXTRA_ATTRIBUTE                       0x05056FD0     56B
  CMSG_GET_OTHER_EXTRA_ATTRIBUTE                        0x050584CC     88B
  CMSG_GET_OTHER_EXTRA_ATTRIBUTE_ERROR_RETURN           0x0505FD54     56B
  CMSG_GET_OTHER_EXTRA_ATTRIBUTE_NEW                    0x0505ACAC    420B
  CMSG_GET_OTHER_NAME                                   0x0505A638     88B
  CMSG_GET_TRADE_MARCH_INFO_REQUEST                     0x0504DFA4     88B
  CMSG_GET_TRADE_MARCH_INFO_RETURN                      0x0504EB34   2252B
  CMSG_GET_WORLD_TRADE_INFO_REQUEST                     0x0504FF70     56B
  CMSG_GET_WORLD_TRADE_INFO_RETURN                      0x0505061C   1220B
  CMSG_GIANT_INVASION_ATTACK_MONSTER_REQUEST            0x0508E130    152B
  CMSG_GIANT_INVASION_ATTACK_MONSTER_RETURN             0x0508E46C    664B
  CMSG_GIANT_INVASION_DAILY_REWARD_REQUEST              0x0508DA78    152B
  CMSG_GIANT_INVASION_DAILY_REWARD_RETURN               0x0508DCE0    484B
  CMSG_GIANT_INVASION_START_REQUEST                     0x0508E970    152B
  CMSG_GIANT_INVASION_START_RETURN                      0x0508EAF0     72B
  CMSG_GIANT_INVASION_TREASURE_POINT_REQUEST            0x0508CBA0    152B
  CMSG_GIANT_INVASION_TREASURE_POINT_RETURN             0x0508CD20     72B
  CMSG_GIANT_INVASION_TREASURE_REWARD_RECORD_REQUEST    0x0508CFD4    152B
  CMSG_GIANT_INVASION_TREASURE_REWARD_RECORD_RETURN     0x0508D428    996B
  CMSG_GIANT_INVASION_WIN_BIG_REWARD                    0x0508EC20     72B
  CMSG_GIFTPACK_EMOTICON                                0x0509045C    376B
  CMSG_GIFTPACK_FREE_INFO                               0x0509373C     72B
  CMSG_GIFTPACK_INFO                                    0x0509141C   3484B
  CMSG_GIFTPACK_RECEIVE_FREE_REQUEST                    0x05093844     56B
  CMSG_GLOBAL_CYCLE_ACTION_RANK_RECORD_REQUEST          0x0501C180     72B
  CMSG_GOLD_OPEN_AREA_REQUEST                           0x04FCB540     72B
  CMSG_GOODLUCK_ACTION_REQUEST                          0x05099308     72B
  CMSG_GOODLUCK_ACTION_RETURN                           0x05099A40   2364B
  CMSG_GOODLUCK_CARD_REQUEST                            0x0509B4AC     88B
  CMSG_GOODLUCK_CARD_RETURN                             0x0509BA18    932B
  CMSG_GOODLUCK_GOLD_BUY_REQUEST                        0x0509BF14    104B
  CMSG_GOODLUCK_GOLD_BUY_RETURN                         0x0509C104    120B
  CMSG_GOODLUCK_LIST_REQUEST                            0x0509C264     72B
  CMSG_GOODLUCK_LIST_RETURN                             0x0509C604    880B
  CMSG_GOODLUCK_SCRATCH_NUM_REQUEST                     0x0509CA94     88B
  CMSG_GOODLUCK_SCRATCH_NUM_RETURN                      0x0509CC40    104B
  CMSG_GOODLUCK_SCRATCH_REQUEST                         0x0509AE00    104B
  CMSG_GOODLUCK_SCRATCH_RETURN                          0x0509B168    548B
  CMSG_GOODLUCK_TARGET_REWARD_REQUEST                   0x0509CF80    184B
  CMSG_GOODLUCK_TARGET_REWARD_RETURN                    0x0509D154     88B
  CMSG_GROUP_CHAT_ADD_MEMBER_REQUEST                    0x050A022C    408B
  CMSG_GROUP_CHAT_ADD_MEMBER_RETURN                     0x050A0910   1680B
  CMSG_GROUP_CHAT_CREATE_REQUEST                        0x0509E530    604B
  CMSG_GROUP_CHAT_CREATE_RETURN                         0x0509ED9C   1748B
  CMSG_GROUP_CHAT_DELETE_REQUEST                        0x0509F55C     72B
  CMSG_GROUP_CHAT_DELETE_RETURN                         0x0509F740    428B
  CMSG_GROUP_CHAT_DEL_MEMBER_REQUEST                    0x050A116C    408B
  CMSG_GROUP_CHAT_EXIT_REQUEST                          0x050A13F0     72B
  CMSG_GROUP_CHAT_MEMBER_LIST_REQUEST                   0x050A1524     72B
  CMSG_GROUP_CHAT_MEMBER_LIST_RETURN                    0x050A1864    736B
  CMSG_GROUP_CHAT_RENAME_REQUEST                        0x0509FAB0    324B
  CMSG_GROUP_CHAT_RENAME_RETURN                         0x0509FE5C    516B
  CMSG_GUIDE_TASKS_RECEIVE_REWARD_REQUEST               0x05286088     56B
  CMSG_GUIDE_TASKS_RECEIVE_REWARD_RETURN                0x052861A8     72B
  CMSG_GUILD_STANDOFF_DATA_REQUEST                      0x050A570C    152B
  CMSG_GUILD_STANDOFF_DATA_RETURN                       0x050A58BC     88B
  CMSG_GUILD_STANDOFF_DUEL_POINT_REQUEST                0x050A5FB4    152B
  CMSG_GUILD_STANDOFF_DUEL_POINT_RETURN                 0x050A6594   1924B
  CMSG_GUILD_STANDOFF_RANK_REQUEST                      0x050A7458    152B
  CMSG_GUILD_STANDOFF_RANK_RETURN                       0x050A7838    904B
  CMSG_GUILD_STANDOFF_REWARD_DAILY_DUEL_REQUEST         0x050A7014    168B
  CMSG_GUILD_STANDOFF_REWARD_DAILY_DUEL_RETURN          0x050A71A4     72B
  CMSG_GUILD_STANDOFF_SIGN_UP_REQUEST                   0x050A5B80    152B
  CMSG_GUILD_STANDOFF_SIGN_UP_RETURN                    0x050A5D00     72B
  CMSG_HANDLE_APPLY_ENTER_LEAGUE                        0x0510251C     88B
  CMSG_HANDLE_APPLY_ENTER_LEAGUE_EX                     0x05102778    616B
  CMSG_HANDLE_APPLY_ENTER_LEAGUE_REPLY_EX               0x05102AC8     72B
  CMSG_HANDLE_INVITE_ENTER_LEAGUE                       0x05102C30     88B
  CMSG_HAND_LEAGUE_HELP                                 0x051682C4    120B
  CMSG_HARBOR_SYNC                                      0x051F3CD0    752B
  CMSG_HERO_AUTO_RECRUIT_AT_DEFEND_FLAG                 0x050AF610    484B
  CMSG_HERO_CANDIDATE_QUEUE_INFO                        0x050ACB00   1236B
  CMSG_HERO_COLLECTION_ACTION_REQUEST                   0x050B0CA4     72B
  CMSG_HERO_COLLECTION_ACTION_RETURN                    0x050B1168   1040B
  CMSG_HERO_COLLECTION_PVE_REQUEST                      0x050B1A84    488B
  CMSG_HERO_COLLECTION_PVE_RETURN                       0x050B1E2C    136B
  CMSG_HERO_COLLECTION_REWARD_REQUEST                   0x050B2008    104B
  CMSG_HERO_COLLECTION_REWARD_RETURN                    0x050B21F8    120B
  CMSG_HERO_COLLECTION_SYNC_ACTION                      0x050B0B04    184B
  CMSG_HERO_COLLECTION_SYNC_RECHARGE                    0x050B23C8    104B
  CMSG_HERO_COLLECTION_SYNC_TASK                        0x050B1774    152B
  CMSG_HERO_DRAW_CD_END                                 0x050B4B6C     56B
  CMSG_HERO_DRAW_EXTRA_INFO                             0x050B4CC4     88B
  CMSG_HERO_DRAW_INFO                                   0x050B3078   4644B
  CMSG_HERO_DRAW_REQUEST                                0x050B4424    104B
  CMSG_HERO_DRAW_RETURN                                 0x050B4820    652B
  CMSG_HERO_DRAW_SET_HERO_REQUEST                       0x050B4E70    104B
  CMSG_HERO_DRAW_SET_HERO_RETURN                        0x050B5060    120B
  CMSG_HERO_HONOR_SOUL_EMBED                            0x050BB3AC    104B
  CMSG_HERO_HONOR_SOUL_EMBED_RESULT                     0x050BB5D0    136B
  CMSG_HERO_INFO                                        0x050AB4C8   3756B
  CMSG_HERO_INFO                                        0x217EC00000000  40061B
  CMSG_HERO_KILL_MONSTER_AWARD                          0x050AF404     88B
  CMSG_HERO_LEGEND_CHANGE_HERO_SKIN_REQUEST             0x050B5F9C     88B
  CMSG_HERO_LEGEND_CHANGE_HERO_SKIN_RETURN              0x050B6148    104B
  CMSG_HERO_LEGEND_EXCHANGE_EXP                         0x050B69B0    120B
  CMSG_HERO_LEGEND_INFO_REQUEST                         0x050B536C     72B
  CMSG_HERO_LEGEND_INFO_RETURN                          0x050B568C    692B
  CMSG_HERO_LEGEND_PVE_CHALLENGE_REQUEST                0x050B6424    512B
  CMSG_HERO_LEGEND_PVE_CHALLENGE_RETURN                 0x050B67AC    120B
  CMSG_HERO_LEGEND_TASK_GET_REWARD_REQUEST              0x050B5C68     88B
  CMSG_HERO_LEGEND_TASK_GET_REWARD_RETURN               0x050B5E14    104B
  CMSG_HERO_MAX_LEVEL_BREAK_REQUEST                     0x050B03A0    184B
  CMSG_HERO_MAX_LEVEL_BREAK_RETURN                      0x050B0578     88B
  CMSG_HERO_QUEUE_ARMY_RETURN                           0x050AD6C0     72B
  CMSG_HERO_QUEUE_EXPEDITION_INFO                       0x050AD220    952B
  CMSG_HERO_RECRUIT_ARMIES                              0x050AC5AC    612B
  CMSG_HERO_RECRUIT_HERO                                0x050ADD40     72B
  CMSG_HERO_SET_EQUIP                                   0x050AF158     88B
  CMSG_HERO_SKILL_CD                                    0x050AE6E4    492B
  CMSG_HERO_SOLDIER_RECRUIT_REQUEST                     0x050AF9C0    408B
  CMSG_HERO_SOLDIER_RECRUIT_RETURN                      0x050AFC40     72B
  CMSG_HERO_SOUL_BATCH_STRENGTHEN                       0x050AFE10    120B
  CMSG_HERO_SOUL_BATCH_STRENGTHEN_RESULT                0x050B0040    136B
  CMSG_HERO_SOUL_EMBED                                  0x050AEA24    104B
  CMSG_HERO_SOUL_EMBED_RESULT                           0x050AEC10    120B
  CMSG_HERO_SOUL_STRENGTHEN                             0x050AEDD4    104B
  CMSG_HERO_SOUL_STRENGTHEN_RESULT                      0x050AEFC0    120B
  CMSG_HERO_UPGRADE_ARMY_LEVEL                          0x050ADEA4    144B
  CMSG_HERO_UPGRADE_ARMY_SKILL                          0x050AE190    592B
  CMSG_HERO_UPGRADE_QUALITY                             0x050AF298     72B
  CMSG_HERO_UPGRADE_SKILL_LEVEL                         0x050ADC10     72B
  CMSG_HERO_USE_EXP_BALL                                0x050AD918    528B
  CMSG_HERO_USE_SKILL                                   0x050AE4C8     72B
  CMSG_HONOR_SOUL_INFO_REQUEST                          0x050B8CE0     56B
  CMSG_HONOR_SOUL_INFO_RETURN                           0x050B914C   1536B
  CMSG_HONOR_SOUL_UPGRADE_REQUEST                       0x050B9D44    120B
  CMSG_HONOR_SOUL_UPGRADE_RETURN                        0x050BA0DC    612B
  CMSG_HONOR_SOUL_WASH_REPLACE_REQUEST                  0x050BAD98    144B
  CMSG_HONOR_SOUL_WASH_REPLACE_RETURN                   0x050BB034    548B
  CMSG_HONOR_SOUL_WASH_REQUEST                          0x050BA4C4    160B
  CMSG_HONOR_SOUL_WASH_RETURN                           0x050BA89C    992B
  CMSG_INVESTIGATION_TRADE_MARCH_REQUEST                0x0504BF2C     88B
  CMSG_INVESTIGATION_TRADE_MARCH_RETURN                 0x0504C06C     72B
  CMSG_INVEST_CANCEL_REQUEST                            0x04FC3654     56B
  CMSG_INVEST_CANCEL_RETURN                             0x04FC3774     72B
  CMSG_INVEST_EARN_REQUEST                              0x04FC387C     56B
  CMSG_INVEST_EARN_RETURN                               0x04FC399C     72B
  CMSG_INVEST_INFO                                      0x04FC3B70    120B
  CMSG_INVEST_REQUEST                                   0x04FC3380     88B
  CMSG_INVEST_RETURN                                    0x04FC352C    104B
  CMSG_INVITE_ADD_LIKE_REQUEST                          0x050BED3C     88B
  CMSG_INVITE_ADD_LIKE_RESP                             0x050BEF84    508B
  CMSG_INVITE_DRAW_LOTTERY_REQUEST                      0x050BD544     56B
  CMSG_INVITE_DRAW_LOTTERY_RETURN                       0x050BD770    684B
  CMSG_INVITE_ENTER_LEAGUE                              0x050F9990     72B
  CMSG_INVITE_ENTER_LEAGUE_NOTICE                       0x05104ABC     72B
  CMSG_INVITE_FRIEND_MILEPOST_REWARD_REQUEST            0x050BE83C     72B
  CMSG_INVITE_FRIEND_MILEPOST_REWARD_RESP               0x050BE970     72B
  CMSG_INVITE_GOLD_LIST_REQUEST                         0x050BCA20     56B
  CMSG_INVITE_GOLD_LIST_RESP                            0x050BCE18    964B
  CMSG_INVITE_INFO_REQUEST                              0x050BC19C     56B
  CMSG_INVITE_INFO_RESP                                 0x050BC66C    756B
  CMSG_INVITE_MARK_REWARD_REQUEST                       0x050BEAA0     72B
  CMSG_INVITE_MARK_REWARD_RESP                          0x050BEBD0     72B
  CMSG_INVITE_MILEPOST_REWARD_REQUEST                   0x050BE620     56B
  CMSG_INVITE_MILEPOST_REWARD_RESP                      0x050BE718     56B
  CMSG_INVITE_PLAYER_LIST_REQUEST                       0x050BDADC     56B
  CMSG_INVITE_PLAYER_LIST_RESP                          0x050BDF20    992B
  CMSG_INVITE_SCORE_REWARD_REQUEST                      0x050BD2C4     72B
  CMSG_INVITE_SCORE_REWARD_RESP                         0x050BD42C     88B
  CMSG_INVITE_TASK_REWARD_REQUEST                       0x050BE3E8     72B
  CMSG_INVITE_TASK_REWARD_RESP                          0x050BE518     72B
  CMSG_ITEM_ADD_SOLDIER                                 0x050C0F54    104B
  CMSG_ITEM_ADD_SOLDIER_SUC                             0x050C114C    120B
  CMSG_ITEM_EQUIP_COMPLEX                               0x050C1AF0     88B
  CMSG_ITEM_INFO                                        0x050C0530    480B
  CMSG_ITEM_SELL                                        0x050C17E4    492B
  CMSG_ITEM_SHOP_BUY_REQUEST                            0x050C3048    104B
  CMSG_ITEM_SHOP_BUY_REQUEST_NEW                        0x050C3640    184B
  CMSG_ITEM_SHOP_BUY_RETURN                             0x050C31D0     88B
  CMSG_ITEM_SHOP_INFO_REQUEST                           0x050C27EC     72B
  CMSG_ITEM_USE                                         0x050C0830     88B
  CMSG_ITEM_USE_CHOOSE                                  0x050C0A10    120B
  CMSG_ITEM_USE_COMMON_HERO_CHIP                        0x050C0BDC    104B
  CMSG_ITEM_USE_COMMON_HERO_CHIP_SUC                    0x050C0D98    104B
  CMSG_ITEM_USE_RESULT                                  0x050C13EC    580B
  CMSG_JOIN_BUILDUP                                     0x05108A20    520B
  CMSG_JOIN_BUILDUP_NEW                                 0x05108F98    616B
  CMSG_KEEPLIVE                                         0x052D9740     56B
  CMSG_KEEP_LIVE_TEST                                   0x0527CB30     72B
  CMSG_KICK_BUILDUP_HERO                                0x05055F14     88B
  CMSG_KICK_DEFEND_HERO                                 0x05055DA0     88B
  CMSG_KICK_DOMINION_DEFEND_HERO                        0x050560BC    104B
  CMSG_KICK_KING_CHESS_DEFEND_HERO                      0x050CCE50    104B
  CMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY                    0x0515D468    184B
  CMSG_KICK_LEGION_MEMBER                               0x05118350     88B
  CMSG_KICK_MEMBER                                      0x051000E0     72B
  CMSG_KINGDOM_ACTION_RANK_RECORD_REQUEST               0x050DD1CC     72B
  CMSG_KINGDOM_ACTION_RANK_RECORD_RETURN                0x050DD670   1396B
  CMSG_KINGDOM_GIFT_ACTION_REQUEST                      0x050E3948     72B
  CMSG_KINGDOM_GIFT_ACTION_RETURN                       0x050E3BBC    168B
  CMSG_KINGDOM_GIFT_LEVEL_GIFT_REQUEST                  0x050E49B8     88B
  CMSG_KINGDOM_GIFT_LEVEL_GIFT_RETURN                   0x050E4B64    104B
  CMSG_KINGDOM_GIFT_LEVEL_REWARD_REQUEST                0x050E4638     88B
  CMSG_KINGDOM_GIFT_LEVEL_REWARD_RETURN                 0x050E4820    120B
  CMSG_KINGDOM_GIFT_TIME_REWARD_REQUEST                 0x050E4CEC     88B
  CMSG_KINGDOM_GIFT_TIME_REWARD_RETURN                  0x050E4ED4    120B
  CMSG_KINGDOM_SERVER_ACTION_VALUE_REQUEST              0x050DDCA4     56B
  CMSG_KINGDOM_SERVER_ACTION_VALUE_RETURN               0x050DDE34    104B
  CMSG_KINGDOM_STRATEGY_NEW_SET_REQUEST                 0x050E5E88    340B
  CMSG_KINGDOM_STRATEGY_NEW_SET_RETURN                  0x050E6280    200B
  CMSG_KINGDOM_STRATEGY_SET_REQUEST                     0x050E5A40     72B
  CMSG_KINGDOM_STRATEGY_SET_RETURN                      0x050E5C1C    120B
  CMSG_KING_CHESS_ACTION_DETAIL_INFO_REQUEST            0x050C4608     56B
  CMSG_KING_CHESS_ACTION_DETAIL_INFO_RETURN             0x050C4B00   1168B
  CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST               0x050CD848     56B
  CMSG_KING_CHESS_BATTLE                                0x050C97DC    460B
  CMSG_KING_CHESS_ENABLE_VIEW                           0x050C5A00     72B
  CMSG_KING_CHESS_LEAGUE_SYNC                           0x050C6BD4   1440B
  CMSG_KING_CHESS_OCCUPY_INFO_REQUEST                   0x050C7298     56B
  CMSG_KING_CHESS_OCCUPY_INFO_RETURN                    0x050C755C    764B
  CMSG_KING_CHESS_RANK_REQUEST                          0x050C5050     56B
  CMSG_KING_CHESS_RANK_RETURN                           0x050C547C   1180B
  CMSG_KING_CHESS_SELF_INFO_REQUEST                     0x050C7940     72B
  CMSG_KING_CHESS_SET_LOOK_CHAT                         0x050C8064     56B
  CMSG_KING_CHESS_SIGNUP_REQUEST                        0x050C3F30     72B
  CMSG_KING_CHESS_SIGNUP_RETURN                         0x050C4060     72B
  CMSG_KING_CHESS_SYNC                                  0x050C60A4   1580B
  CMSG_KING_CHESS_SYNC_ALL_LEAGUE_INFO                  0x050C8238    432B
  CMSG_KING_CHESS_SYNC_SELF_INFO                        0x050C7C94    784B
  CMSG_KING_CHESS_USER_VALUE_REQUEST                    0x050CCF78     56B
  CMSG_KING_CHESS_USER_VALUE_RETURN                     0x050CD32C   1116B
  CMSG_KING_REWARD_INFO_REQUEST                         0x0503E708     56B
  CMSG_KING_REWARD_INFO_RETURN                          0x0503EB04   1668B
  CMSG_KING_ROAD_REWARD_REQUEST                         0x050DC3A4     72B
  CMSG_KING_ROAD_REWARD_RETURN                          0x050DC4D4     72B
  CMSG_KNIGHT_ACTION_DETAIL_REQUEST                     0x050E6EA0     56B
  CMSG_KNIGHT_ACTION_DETAIL_RETURN                      0x050E730C   1064B
  CMSG_KNIGHT_ACTION_LEAGUE_RANK_REQUEST                0x050E85BC     56B
  CMSG_KNIGHT_ACTION_LEAGUE_RANK_RETURN                 0x050E8B00   1308B
  CMSG_KNIGHT_ACTION_PLAYER_RANK_REQUEST                0x050E7A9C     56B
  CMSG_KNIGHT_ACTION_PLAYER_RANK_RETURN                 0x050E7FE0   1308B
  CMSG_KNIGHT_ACTION_REQUEST                            0x050E6BE8     56B
  CMSG_KNIGHT_ACTION_RETURN                             0x050E6D78    104B
  CMSG_KNIGHT_ACTION_SET_BEGIN_TIME_REQUEST             0x050E781C     72B
  CMSG_KNIGHT_ACTION_SET_BEGIN_TIME_RETURN              0x050E7984     88B
  CMSG_KNIGHT_ACTION_UPDATE_BEGIN_TIME                  0x050E9108     72B
  CMSG_KNIGHT_GLORY_CHALLENGE_REQUEST                   0x050EB720    168B
  CMSG_KNIGHT_GLORY_CHALLENGE_RETURN                    0x050EB9B4    152B
  CMSG_KNIGHT_GLORY_HELP_LIST_REQUEST                   0x050EC0B4    152B
  CMSG_KNIGHT_GLORY_HELP_LIST_RETURN                    0x050EC4E4   1108B
  CMSG_KNIGHT_GLORY_HELP_REQUEST                        0x050EBCB8    152B
  CMSG_KNIGHT_GLORY_HELP_RETURN                         0x050EBE10     56B
  CMSG_KNIGHT_GLORY_IS_HELP_REQUEST                     0x050ECBE8    168B
  CMSG_KNIGHT_GLORY_IS_HELP_RETURN                      0x050ECE50    324B
  CMSG_KNIGHT_GLORY_LEAGUE_SYNC                         0x051EF780    820B
  CMSG_KNIGHT_GLORY_SET_LV_REQUEST                      0x050EB16C    168B
  CMSG_KNIGHT_GLORY_SET_LV_RETURN                       0x050EB2FC     72B
  CMSG_KNIGHT_GLORY_SYNC                                0x051EF0D4    816B
  CMSG_KNIGHT_GLORY_UPDATE_HELP_OTHER_END_TIME          0x050EA8E4     72B
  CMSG_KNIGHT_GLORY_UPDATE_INDEX                        0x050EB42C     72B
  CMSG_LATCH_GOLD_PASS_REQUEST                          0x050F1974     72B
  CMSG_LATCH_GOLD_PASS_RETURN                           0x050F1BB4    516B
  CMSG_LATCH_RESULT_REQUEST                             0x050F0DC0    168B
  CMSG_LATCH_RESULT_RETURN                              0x050F118C    972B
  CMSG_LATCH_REWARD_REQUEST                             0x050F1678     88B
  CMSG_LATCH_REWARD_RETURN                              0x050F1824    104B
  CMSG_LATCH_SPECIAL_RESULT_REQUEST                     0x050F214C    168B
  CMSG_LATCH_SPECIAL_RESULT_RETURN                      0x050F23EC    516B
  CMSG_LATCH_UP_LEVEL_UNLOCK                            0x050F1EA0     72B
  CMSG_LEAGUEBUILD_SYNC                                 0x05158590   1624B
  CMSG_LEAGUEPASS_ACTION_STATUS_REQUEST                 0x0516B21C     56B
  CMSG_LEAGUEPASS_ACTION_STATUS_RETURN                  0x0516B340     72B
  CMSG_LEAGUEPASS_ACTION_TASK_INFO_REQUEST              0x0516B448     56B
  CMSG_LEAGUEPASS_ACTION_TASK_INFO_RETURN               0x0516BBC0   1800B
  CMSG_LEAGUEPASS_CONTRIBUTE_INFO_REQUEST               0x0516D210     72B
  CMSG_LEAGUEPASS_CONTRIBUTE_INFO_RETURN                0x0516D708   1720B
  CMSG_LEAGUEPASS_FINISH_TASK_REQUEST                   0x0516E788     72B
  CMSG_LEAGUEPASS_FINISH_TASK_RETURN                    0x0516E990    136B
  CMSG_LEAGUEPASS_FRESH_TASK_REQUEST                    0x0516E1A4     56B
  CMSG_LEAGUEPASS_FRESH_TASK_RETURN                     0x0516E424    636B
  CMSG_LEAGUEPASS_GET_REWARD_REQUEST                    0x0516DED8     88B
  CMSG_LEAGUEPASS_GET_REWARD_RETURN                     0x0516E07C    104B
  CMSG_LEAGUEPASS_GROUP_RANK_INFO_REQUEST               0x0516C3B0     72B
  CMSG_LEAGUEPASS_GROUP_RANK_INFO_RETURN                0x0516C9A0   1848B
  CMSG_LEAGUE_BATTLEFIELD_ACTIVITY_VIEW_RETURN          0x05110674   1168B
  CMSG_LEAGUE_BATTLEFIELD_DOMINION_BATTLE               0x0510B8D0    476B
  CMSG_LEAGUE_BATTLEFIELD_FORCE_REQUEST                 0x051119E4     56B
  CMSG_LEAGUE_BATTLEFIELD_FORCE_RETURN                  0x05111EB0   1216B
  CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST            0x05113298    392B
  CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_RETURN             0x05113504     72B
  CMSG_LEAGUE_BATTLEFIELD_MAPINFO_REQUEST               0x05137AE0     56B
  CMSG_LEAGUE_BATTLEFIELD_MAPINFO_RESPONSE              0x051383C8   2652B
  CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_REQUEST            0x0511360C     56B
  CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_RETURN             0x05113AC0   1244B
  CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_REQUEST             0x05110E6C     56B
  CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_RETURN              0x05111298   1180B
  CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_REQUEST         0x05112A04     56B
  CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_RETURN          0x05112CC4   1096B
  CMSG_LEAGUE_BATTLEFIELD_SIGNUP_REQUEST                0x05110C24     88B
  CMSG_LEAGUE_BATTLEFIELD_SIGNUP_RETURN                 0x05110D64     72B
  CMSG_LEAGUE_BIG_BOSS_CALL_REQUEST                     0x05153A7C    184B
  CMSG_LEAGUE_BIG_BOSS_CALL_RETURN                      0x05153C84    104B
  CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST             0x05152A9C    152B
  CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_RETURN              0x05152C1C     72B
  CMSG_LEAGUE_BIG_BOSS_DONATE_REQUEST                   0x05152F18    168B
  CMSG_LEAGUE_BIG_BOSS_DONATE_RETURN                    0x051530A8     72B
  CMSG_LEAGUE_BIG_BOSS_EMPTYPOS_REQUEST                 0x05154864    152B
  CMSG_LEAGUE_BIG_BOSS_EMPTYPOS_RETURN                  0x05154A50    104B
  CMSG_LEAGUE_BIG_BOSS_POINT_REQUEST                    0x0515335C    152B
  CMSG_LEAGUE_BIG_BOSS_POINT_RETURN                     0x051535D4    460B
  CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_REQUEST          0x05153FC0    184B
  CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_RETURN           0x05154198     88B
  CMSG_LEAGUE_BOARD_LEAVE_WORD                          0x04FC808C    400B
  CMSG_LEAGUE_BOARD_LEAVE_WORD_RETURN                   0x04FC8374    104B
  CMSG_LEAGUE_BOARD_REQUEST                             0x04FC6D34    164B
  CMSG_LEAGUE_BOARD_RETURN                              0x04FC765C   1952B
  CMSG_LEAGUE_BOSS_ITEM_USE_REQUEST                     0x05155590    200B
  CMSG_LEAGUE_BOSS_ITEM_USE_RETURN                      0x05155818    136B
  CMSG_LEAGUE_BUILDING_DETAIL_REQUEST                   0x05158E50    168B
  CMSG_LEAGUE_BUILDING_DETAIL_RETURN                    0x05159A5C   3292B
  CMSG_LEAGUE_BUILDING_OPERAT_REQUEST                   0x05156E2C    136B
  CMSG_LEAGUE_BUILDING_OPERAT_RETURN                    0x0515716C    220B
  CMSG_LEAGUE_BUILD_COLLECT_TIME_REQUEST                0x0515DA04     88B
  CMSG_LEAGUE_BUILD_COLLECT_TIME_RETURN                 0x0515DBE8    120B
  CMSG_LEAGUE_CARD_CANCEL_EXCHANGE_REQUEST              0x05169B24     56B
  CMSG_LEAGUE_CARD_CANCEL_EXCHANGE_RETURN               0x05169DD0    572B
  CMSG_LEAGUE_CARD_HANDLE_EXCHANGE_REQUEST              0x051697F4    104B
  CMSG_LEAGUE_CARD_HANDLE_EXCHANGE_RETURN               0x051699EC    120B
  CMSG_LEAGUE_CARD_LIST_REQUEST                         0x0516A0CC     56B
  CMSG_LEAGUE_CARD_LIST_RETURN                          0x0516A52C   1316B
  CMSG_LEAGUE_CARD_POST_EXCHANGE_REQUEST                0x05168EE8    684B
  CMSG_LEAGUE_CARD_POST_EXCHANGE_RETURN                 0x051693D4    712B
  CMSG_LEAGUE_CONTRIBUTE_INFO_REQUEST                   0x05011FBC     56B
  CMSG_LEAGUE_CONTRIBUTE_INFO_RETURN                    0x05012280    744B
  CMSG_LEAGUE_DONATE_REWARD_REQUEST                     0x05179040     72B
  CMSG_LEAGUE_DONATE_REWARD_RETURN                      0x051791A8     88B
  CMSG_LEAGUE_ERROR                                     0x05103204     72B
  CMSG_LEAGUE_FORCE_LEVEL_UP                            0x050679E8     72B
  CMSG_LEAGUE_FORCE_REQUEST                             0x05066B18     56B
  CMSG_LEAGUE_LATEST_REQUEST                            0x05043668     72B
  CMSG_LEAGUE_LATEST_RETURN                             0x0504397C    756B
  CMSG_LEAGUE_LEADER_EMPTYPOS_REQUEST                   0x051047DC     56B
  CMSG_LEAGUE_LEADER_EMPTYPOS_RETURN                    0x05104968    104B
  CMSG_LEAGUE_MEMBER_INFO_REQUEST                       0x0511245C     72B
  CMSG_LEAGUE_NEW_BOARD_LEAVE_WORD                      0x04FC849C     56B
  CMSG_LEAGUE_PANEL_CLOSE                               0x05103404     56B
  CMSG_LEAGUE_RANK_REQUEST                              0x05067AF0     56B
  CMSG_LEAGUE_RANK_RESPONSE                             0x05067D7C    536B
  CMSG_LEAGUE_RANK_RETURN                               0x05067174   1608B
  CMSG_LEAGUE_RECHARGE_END_MAIL                         0x05178274    168B
  CMSG_LEAGUE_RECHARGE_POINT_REQUEST                    0x05177DB4    152B
  CMSG_LEAGUE_RECHARGE_REWARD_REQUEST                   0x051775FC    200B
  CMSG_LEAGUE_RECHARGE_REWARD_RETURN                    0x05177914    564B
  CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_COMPLETE        0x0517A3A8     88B
  CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_START           0x0517A108    384B
  CMSG_LEAGUE_SCIENCE_CD_END                            0x05179D5C     56B
  CMSG_LEAGUE_SCIENCE_CD_END_NEW                        0x05178DA4     56B
  CMSG_LEAGUE_SCIENCE_CLEAR_CD                          0x05179C64     56B
  CMSG_LEAGUE_SCIENCE_DONATE                            0x05179B4C     88B
  CMSG_LEAGUE_SCIENCE_DONATE_NEW_REQUEST                0x05178474    104B
  CMSG_LEAGUE_SCIENCE_DONATE_NEW_RETURN                 0x05178634    104B
  CMSG_LEAGUE_SCIENCE_ERROR                             0x05179EB4     88B
  CMSG_LEAGUE_SCIENCE_INFO                              0x051795A4    548B
  CMSG_LEAGUE_SCIENCE_PLAYER_INFO                       0x051798B0     72B
  CMSG_LEAGUE_SCIENCE_UPGRADE                           0x051799E4     72B
  CMSG_LEAGUE_SET_COLOR_REQUEST                         0x0506807C     72B
  CMSG_LEAGUE_SET_COLOR_RETURN                          0x050681AC     72B
  CMSG_LEAGUE_SHOP_BUY                                  0x0504781C     72B
  CMSG_LEAGUE_SHOP_BUY_RETURN                           0x0504794C     72B
  CMSG_LEAGUE_STATUS_REQUEST                            0x0517A4CC     56B
  CMSG_LEAGUE_STATUS_RETURN                             0x0517A718    836B
  CMSG_LEAGUE_UPDATE_STATUS_RETURN                      0x0517AC30    136B
  CMSG_LEGION_ACTION_REQUEST                            0x05114824     56B
  CMSG_LEGION_ACTION_RETURN                             0x05114EDC   1520B
  CMSG_LEGION_ADD_MEMBER_LIST_REQUEST                   0x05118B00     72B
  CMSG_LEGION_ADD_MEMBER_LIST_RETURN                    0x05118E48    736B
  CMSG_LEGION_BATTLE_MAP_INFO_REQUEST                   0x0511DF24     56B
  CMSG_LEGION_BATTLE_MAP_INFO_RETURN                    0x0511E188    584B
  CMSG_LEGION_CHANGE_POS_TIMES_REQUEST                  0x0511AF0C     56B
  CMSG_LEGION_CHANGE_POS_TIMES_RETURN                   0x0511B02C     72B
  CMSG_LEGION_CREATE_REQUEST                            0x051157AC    308B
  CMSG_LEGION_CREATE_RETURN                             0x05115E10    892B
  CMSG_LEGION_ENEMY_POS_REQUEST                         0x0511F7A4     56B
  CMSG_LEGION_ENEMY_POS_RETURN                          0x0511F998    492B
  CMSG_LEGION_FINAL_POINT                               0x0513A3C8   2028B
  CMSG_LEGION_INFO_REQUEST                              0x051169E8     72B
  CMSG_LEGION_INFO_RETURN                               0x05116FC4   1220B
  CMSG_LEGION_JOIN_REQUEST                              0x0511765C    468B
  CMSG_LEGION_JOIN_RETURN                               0x05117D8C   1188B
  CMSG_LEGION_LATEST_REQUEST                            0x0511CA7C     72B
  CMSG_LEGION_LATEST_RETURN                             0x0511CD90    756B
  CMSG_LEGION_LIST_REQUEST                              0x0511624C     56B
  CMSG_LEGION_LIST_RETURN                               0x051165BC    832B
  CMSG_LEGION_MEMBER_HIS_INFO_REQUEST                   0x05128FB0     56B
  CMSG_LEGION_MEMBER_HIS_INFO_RETURN                    0x05129428   1316B
  CMSG_LEGION_MEMBER_INFO_REQUEST                       0x0511EB94     56B
  CMSG_LEGION_MEMBER_INFO_RETURN                        0x0511F1D0   1300B
  CMSG_LEGION_RANK_REQUEST                              0x0511A2B8     72B
  CMSG_LEGION_RANK_RETURN                               0x0511A730   1144B
  CMSG_LEGION_RESOURCE_REQUEST                          0x0511E490     56B
  CMSG_LEGION_RESOURCE_RETURN                           0x0511E7D8    764B
  CMSG_LEGION_SEASON_ACTION_GROUP_INFO_REQUEST          0x051282F0     72B
  CMSG_LEGION_SEASON_ACTION_GROUP_INFO_RETURN           0x051288F0   1344B
  CMSG_LEGION_SEASON_ACTION_GUESS_BET_REQUEST           0x05124748    104B
  CMSG_LEGION_SEASON_ACTION_GUESS_BET_RETURN            0x05124EB4   1720B
  CMSG_LEGION_SEASON_ACTION_GUESS_INFO_REQUEST          0x05123024     56B
  CMSG_LEGION_SEASON_ACTION_GUESS_INFO_RETURN           0x0512382C   3520B
  CMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_REQUEST     0x051275E4     72B
  CMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_RETURN      0x05127A5C   1140B
  CMSG_LEGION_SEASON_ACTION_HIS_MVP_REQUEST             0x05126C10     72B
  CMSG_LEGION_SEASON_ACTION_HIS_MVP_RETURN              0x05127088   1140B
  CMSG_LEGION_SEASON_ACTION_HIS_PLAYER_REQUEST          0x05126158    104B
  CMSG_LEGION_SEASON_ACTION_HIS_PLAYER_RETURN           0x05126660   1156B
  CMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_REQUEST         0x05127FEC     88B
  CMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_RETURN          0x0512819C    104B
  CMSG_LEGION_SEASON_ACTION_PLAYOFF_REQUEST             0x0512568C     88B
  CMSG_LEGION_SEASON_ACTION_PLAYOFF_RETURN              0x05125B54   1128B
  CMSG_LEGION_SEASON_ACTION_REQUEST                     0x051200E8     56B
  CMSG_LEGION_SEASON_ACTION_RETURN                      0x05120B28   2144B
  CMSG_LEGION_SEASON_ACTION_SCHEDULE_REQUEST            0x051214A8     88B
  CMSG_LEGION_SEASON_ACTION_SCHEDULE_RETURN             0x05121A20   1664B
  CMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_REQUEST       0x05122160     56B
  CMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_RETURN        0x0512274C   2072B
  CMSG_LEGION_SELF_JOIN_REQUEST                         0x0511D170     72B
  CMSG_LEGION_SELF_JOIN_RETURN                          0x0511D714   1188B
  CMSG_LEGION_SELF_LEAVE_REQUEST                        0x0511DCA4     72B
  CMSG_LEGION_SELF_LEAVE_RETURN                         0x0511DE0C     88B
  CMSG_LEGION_SET_TALENT_REQUEST                        0x0511AC90     72B
  CMSG_LEGION_SET_TALENT_RETURN                         0x0511ADF4     88B
  CMSG_LEGION_VALUE_DETAIL_REQUEST                      0x0511FC44     56B
  CMSG_LEGION_VALUE_DETAIL_RETURN                       0x0511FE5C    460B
  CMSG_LOGIN                                            0x0517B084    552B
  CMSG_LOGIN_DISTRIBUTUON_REQUEST                       0x0517B944     72B
  CMSG_LOGIN_DISTRIBUTUON_RETURN                        0x0517BB18    308B
  CMSG_LOGIN_RETURN                                     0x0517B5F4    612B
  CMSG_LORD_BACK_LORD_REQUEST                           0x0518DBF8     56B
  CMSG_LORD_BACK_LORD_RETURN                            0x0518DD18     72B
  CMSG_LORD_BEREWARD_INFO_REQUEST                       0x0518C024     72B
  CMSG_LORD_BEREWARD_INFO_RETURN                        0x0518C460   1108B
  CMSG_LORD_BE_CATCH                                    0x0518E9E4    656B
  CMSG_LORD_BE_DEFEAT                                   0x0518FAEC     56B
  CMSG_LORD_BE_EXECUTE                                  0x0518F9F4     56B
  CMSG_LORD_BE_PAY_RANSOM                               0x0518FC10     72B
  CMSG_LORD_BE_PUNISH_RECORD_INFO                       0x05191B08    800B
  CMSG_LORD_BE_RELEASE                                  0x0518F8DC     88B
  CMSG_LORD_BE_REWARD                                   0x0518F58C    564B
  CMSG_LORD_CATCHER_INFO_REQUEST                        0x0518DE20     56B
  CMSG_LORD_CATCHER_INFO_RETURN                         0x0518E188    564B
  CMSG_LORD_CATCH_BASE_SYN                              0x0518B15C    232B
  CMSG_LORD_CATCH_INFO_REQUEST                          0x0518B304     56B
  CMSG_LORD_CATCH_INFO_RETURN                           0x0518B8E0   1264B
  CMSG_LORD_CATCH_LORD                                  0x0518F010    596B
  CMSG_LORD_CATCH_USER_TIME_OVER                        0x0518E47C     56B
  CMSG_LORD_CATCH_USE_KEY_ITEM                          0x0518FED8     56B
  CMSG_LORD_CATCH_USE_KEY_ITEM_RETURN                   0x05190064    104B
  CMSG_LORD_DEL_BE_PUNISH_MAIL                          0x05190B40    416B
  CMSG_LORD_EQUIP_CANCEL_MERGE                          0x05195AC0     56B
  CMSG_LORD_EQUIP_COMPLETE_MERGE                        0x05195BB8     56B
  CMSG_LORD_EQUIP_DECOMPOSE                             0x05196514     72B
  CMSG_LORD_EQUIP_DECOMPOSE_RETURN                      0x05196648     72B
  CMSG_LORD_EQUIP_GOLD_MERGE                            0x05195404   1532B
  CMSG_LORD_EQUIP_GOLD_SPEED_MERGE                      0x05195CB0     56B
  CMSG_LORD_EQUIP_ITEM_SPEED_MERGE                      0x05195E08     88B
  CMSG_LORD_EQUIP_ITEM_SPEED_MERGE_ONEKEY               0x051961C8    612B
  CMSG_LORD_EQUIP_MERGE_SYN                             0x051925B0    120B
  CMSG_LORD_EQUIP_NORMAL_MERGE                          0x05194998   1532B
  CMSG_LORD_EQUIP_PUT                                   0x051967AC     88B
  CMSG_LORD_EQUIP_PUT_RETURN                            0x05196920     88B
  CMSG_LORD_EQUIP_SYN                                   0x05193140   2920B
  CMSG_LORD_ESCAPE                                      0x05190334    516B
  CMSG_LORD_EXECUTE_LORD_REQUEST                        0x0518D978     72B
  CMSG_LORD_EXECUTE_LORD_RETURN                         0x0518DAE0     88B
  CMSG_LORD_GEM_DECOMPOSE                               0x05198C14     88B
  CMSG_LORD_GEM_DECOMPOSE_RETURN                        0x05198D8C     88B
  CMSG_LORD_GEM_HOLE_LV_UP_REQUEST                      0x05199FD4    628B
  CMSG_LORD_GEM_HOLE_LV_UP_RETURN                       0x0519A3D4    120B
  CMSG_LORD_GEM_HOLE_UNLOCK_REQUEST                     0x0519996C    184B
  CMSG_LORD_GEM_HOLE_UNLOCK_RETURN                      0x05199B44     88B
  CMSG_LORD_GEM_MERGE                                   0x05198634     88B
  CMSG_LORD_GEM_MERGE_RETURN                            0x051987AC     88B
  CMSG_LORD_GEM_PUT                                     0x05196B00    120B
  CMSG_LORD_GEM_PUT_RETURN                              0x05196CCC    104B
  CMSG_LORD_LIKE_REQUEST                                0x0528B530    104B
  CMSG_LORD_LIKE_RETURN                                 0x0528B7C0    528B
  CMSG_LORD_MATERIAL_DECOMPOSE                          0x05198924     88B
  CMSG_LORD_MATERIAL_DECOMPOSE_RETURN                   0x05198A9C     88B
  CMSG_LORD_MATERIAL_MERGE                              0x05198344     88B
  CMSG_LORD_MATERIAL_MERGE_RETURN                       0x051984BC     88B
  CMSG_LORD_NEW_EQUIP_SYN                               0x051940A0   1160B
  CMSG_LORD_PACKAGE_ADD                                 0x05196EF4    324B
  CMSG_LORD_PACKAGE_ADD_RETURN                          0x051971F8    324B
  CMSG_LORD_PACKAGE_SET                                 0x05197700    592B
  CMSG_LORD_PACKAGE_SET_RETURN                          0x05197D14    688B
  CMSG_LORD_PACKAGE_USE                                 0x051980AC     72B
  CMSG_LORD_PACKAGE_USE_RETURN                          0x051981DC     72B
  CMSG_LORD_PAY_RANSOM_REQUEST                          0x0518CF58     56B
  CMSG_LORD_PAY_RANSOM_RETURN                           0x0518D078     72B
  CMSG_LORD_PUNISH_INFO                                 0x0519137C   1088B
  CMSG_LORD_PUNISH_REQUEST                              0x05190624     72B
  CMSG_LORD_PUNISH_RETURN                               0x05190E9C    136B
  CMSG_LORD_RELEASE_LORD_REQUEST                        0x0518D6CC     72B
  CMSG_LORD_RELEASE_LORD_RETURN                         0x0518D834     88B
  CMSG_LORD_REWARD_LORD_REQUEST                         0x0518D2B4    152B
  CMSG_LORD_REWARD_LORD_RETURN                          0x0518D548    152B
  CMSG_LORD_SELF_STATUS_TIME_OVER                       0x0518E59C     72B
  CMSG_LORD_SET_BE_PUNISH_FLAG                          0x05190804    420B
  CMSG_LORD_SET_RANSOM_REQUEST                          0x0518CBD4    120B
  CMSG_LORD_SET_RANSOM_RETURN                           0x0518CE10    136B
  CMSG_LORD_SKILL_SYN                                   0x0519BFA0   1568B
  CMSG_LORD_SKILL_TRIGGER_110_REQUEST                   0x0519D198     72B
  CMSG_LORD_SKILL_TRIGGER_110_RETURN                    0x0519D3D8    152B
  CMSG_LORD_SKILL_TRIGGER_130_REQUEST                   0x0519D640    456B
  CMSG_LORD_SKILL_TRIGGER_130_RETURN                    0x0519DA38    168B
  CMSG_LORD_SKILL_TRIGGER_202_REQUEST                   0x0519DBCC     72B
  CMSG_LORD_SKILL_TRIGGER_202_RETURN                    0x0519DDD4    136B
  CMSG_LORD_SKILL_TRIGGER_REQUEST                       0x0519DF80     88B
  CMSG_LORD_SKILL_TRIGGER_RETURN                        0x0519E1D0    152B
  CMSG_LORD_SKILL_UPGRADE_BATCH_REQUEST                 0x0519E4DC    768B
  CMSG_LORD_SKILL_UPGRADE_BATCH_RETURN                  0x0519EA50    768B
  CMSG_LORD_SKILL_UPGRADE_REQUEST                       0x0519C6DC     88B
  CMSG_LORD_SKILL_UPGRADE_RETURN                        0x0519C850     88B
  CMSG_LORD_SKILL_USE_ACTIVE_REQUEST                    0x0519C990     72B
  CMSG_LORD_SKILL_USE_ACTIVE_RETURN                     0x0519CC50    508B
  CMSG_LORD_SKILL_USE_FORMATION_REQUEST                 0x0519CF34     72B
  CMSG_LORD_SKILL_USE_FORMATION_RETURN                  0x0519D064     72B
  CMSG_LORD_UPDATE_RANSOM                               0x0518FDB0    104B
  CMSG_LORD_WAR_DISTRIBUTE_REWARD_INFO_REQUEST          0x0511B2B0     56B
  CMSG_LORD_WAR_DISTRIBUTE_REWARD_INFO_RETURN           0x0511B808   2992B
  CMSG_LOSTLAND_ACHIEVEMENT_COMPLETE                    0x051B3D50    736B
  CMSG_LOSTLAND_ACHIEVEMENT_LIST_REQUEST                0x051B3488     56B
  CMSG_LOSTLAND_ACHIEVEMENT_LIST_RETURN                 0x051B3798    736B
  CMSG_LOSTLAND_ACHIEVEMENT_REQUEST                     0x051B4118     72B
  CMSG_LOSTLAND_ACHIEVEMENT_RETURN                      0x051B45B0   1504B
  CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST              0x051B4C78     72B
  CMSG_LOSTLAND_ACHIEVEMENT_REWARD_RETURN               0x051B4DA8     72B
  CMSG_LOSTLAND_ACTIVITY_VIEW_RETURN                    0x051A90A0   1824B
  CMSG_LOSTLAND_BAN_HERO_REQUEST                        0x051AFFE0    432B
  CMSG_LOSTLAND_BAN_HERO_RETURN                         0x051B032C    432B
  CMSG_LOSTLAND_BUILDING_INDEX_OPEN_REQUEST             0x051B6784    392B
  CMSG_LOSTLAND_BUILDING_INDEX_OPEN_RETURN              0x051B6AD8    392B
  CMSG_LOSTLAND_CAMP_RANK_REQUEST                       0x051B0B80     56B
  CMSG_LOSTLAND_CAMP_RANK_RETURN                        0x051B0EA4   1388B
  CMSG_LOSTLAND_DAILY_TASK_COMPLETE                     0x051B6434    388B
  CMSG_LOSTLAND_DAILY_TASK_CONFIG                       0x051B57A8    664B
  CMSG_LOSTLAND_DAILY_TASK_REQUEST                      0x051B5B00     56B
  CMSG_LOSTLAND_DAILY_TASK_RETURN                       0x051B5D7C    512B
  CMSG_LOSTLAND_DAILY_TASK_REWARD_REQUEST               0x051B609C     88B
  CMSG_LOSTLAND_DAILY_TASK_REWARD_RETURN                0x051B6214     88B
  CMSG_LOSTLAND_DONATE_CD_END                           0x051B2C3C     72B
  CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST                 0x051AF308     88B
  CMSG_LOSTLAND_DONATE_HEROCHIP_RETURN                  0x051AF588    548B
  CMSG_LOSTLAND_DONATE_INFO                             0x051B2E9C    540B
  CMSG_LOSTLAND_DONATE_RESOURCE_REQUEST                 0x051AED44     88B
  CMSG_LOSTLAND_DONATE_RESOURCE_RETURN                  0x051AEFC4    548B
  CMSG_LOSTLAND_HERO_VOTE_COUNT_REQUEST                 0x051B05C4     72B
  CMSG_LOSTLAND_HERO_VOTE_COUNT_RETURN                  0x051B0814    684B
  CMSG_LOSTLAND_HISTORY_REQUEST                         0x051AD1AC     56B
  CMSG_LOSTLAND_HISTORY_RETURN                          0x051AD5D4    996B
  CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST                    0x051AAFBC    168B
  CMSG_LOSTLAND_LEAGUE_BUILD_RESPONSE                   0x051AB474   1296B
  CMSG_LOSTLAND_LEAGUE_HISTORY_REQUEST                  0x051ADA78     56B
  CMSG_LOSTLAND_LEAGUE_HISTORY_RETURN                   0x051ADE44   1120B
  CMSG_LOSTLAND_LEAGUE_LATEST_REQUEST                   0x051B4EDC     72B
  CMSG_LOSTLAND_LEAGUE_LATEST_RETURN                    0x051B51F0    756B
  CMSG_LOSTLAND_LEAGUE_RANK_REQUEST                     0x051B161C     56B
  CMSG_LOSTLAND_LEAGUE_RANK_RETURN                      0x051B1AF0   1208B
  CMSG_LOSTLAND_MAPINFO_REQUEST                         0x051A9880     56B
  CMSG_LOSTLAND_MAPINFO_RESPONSE                        0x051A9D90   1316B
  CMSG_LOSTLAND_MARK_REWARD_REQUEST                     0x051ABE18     72B
  CMSG_LOSTLAND_MARK_REWARD_RETURN                      0x051AC058    516B
  CMSG_LOSTLAND_MONTH_CARD_REWARD_REQUEST               0x051A6D44    152B
  CMSG_LOSTLAND_MONTH_CARD_REWARD_RETURN                0x051A6E9C     56B
  CMSG_LOSTLAND_PLAYER_HISTORY_REQUEST                  0x051AE364     56B
  CMSG_LOSTLAND_PLAYER_HISTORY_RETURN                   0x051AE76C   1140B
  CMSG_LOSTLAND_PLAYER_RANK_REQUEST                     0x051B21C8     56B
  CMSG_LOSTLAND_PLAYER_RANK_RETURN                      0x051B269C   1208B
  CMSG_LOSTLAND_RUSH_EVENT_RANK_REQUEST                 0x04FA4ED8    168B
  CMSG_LOSTLAND_RUSH_EVENT_RANK_RETURN                  0x04FA54B0   1320B
  CMSG_LOSTLAND_RUSH_EVENT_REWARD_REQUEST               0x04FA49F8    184B
  CMSG_LOSTLAND_RUSH_EVENT_REWARD_RETURN                0x04FA4BD0     88B
  CMSG_LOSTLAND_SELF_CAMP_AREA                          0x051B3250    376B
  CMSG_LOSTLAND_SELF_DOMINION_REQUEST                   0x051AA49C     56B
  CMSG_LOSTLAND_SELF_DOMINION_RESPONSE                  0x051AA830    940B
  CMSG_LOSTLAND_SHOP_BUY_REQUEST                        0x051AF8CC     88B
  CMSG_LOSTLAND_SHOP_BUY_RETURN                         0x051AFA44     88B
  CMSG_LOSTLAND_TOP_LEAGUE_REQUEST                      0x051AC31C     56B
  CMSG_LOSTLAND_TOP_LEAGUE_RETURN                       0x051AC8E4   2056B
  CMSG_LOST_ERA_TASK_INFO                               0x0519FD44   1180B
  CMSG_LOST_ERA_TASK_INFO_REQUEST                       0x051A04F0     56B
  CMSG_LOST_ERA_TASK_RECEIVE_REQUEST                    0x051A0610     72B
  CMSG_LOST_ERA_TASK_RECEIVE_RETURN                     0x051A07AC    104B
  CMSG_LOST_ERA_TASK_UPDATE                             0x051A03A8    136B
  CMSG_LOST_ERA_TASK_VIEW_REQUEST                       0x051A08FC     72B
  CMSG_LOST_ERA_TASK_VIEW_RETURN                        0x051A0DE4   1284B
  CMSG_LOST_KING_ROAD_REWARD_REQUEST                    0x051A661C     72B
  CMSG_LOST_KING_ROAD_REWARD_RETURN                     0x051A674C     72B
  CMSG_LOTTERY_BETTING                                  0x051C8474    200B
  CMSG_LOTTERY_BETTING_RETURN                           0x051C87A8    484B
  CMSG_LOTTERY_CUR_STAGE_INFO                           0x051C8C20    168B
  CMSG_LOTTERY_CUR_STAGE_INFO_RETURN                    0x051C8F18    684B
  CMSG_LOTTERY_INFO                                     0x051C7C64   1300B
  CMSG_LOTTERY_OPEN_AWARD                               0x051C9458    168B
  CMSG_LOTTERY_OPEN_AWARD_HISTORY                       0x051C9F84    168B
  CMSG_LOTTERY_OPEN_AWARD_HISTORY_RETURN                0x051CA488    916B
  CMSG_LOTTERY_OPEN_AWARD_RETURN                        0x051C995C    916B
  CMSG_LUCKYPOT_ACTION_REQUEST                          0x051D33F0     72B
  CMSG_LUCKYPOT_ACTION_RETURN                           0x051D3824    892B
  CMSG_LUCKYPOT_CHOOSEGIFT_REQUEST                      0x051D3D2C    120B
  CMSG_LUCKYPOT_CHOOSEGIFT_RETURN                       0x051D3F64    136B
  CMSG_LUCKYPOT_DIG_REQUEST                             0x051D4140    104B
  CMSG_LUCKYPOT_DIG_RETURN                              0x051D4368    136B
  CMSG_LUCKYPOT_NEXTLAYER                               0x051D4650    532B
  CMSG_LUCKY_GIFT_DETAILED_INFO_REQUEST                 0x051D034C     88B
  CMSG_LUCKY_GIFT_END_TIME_REQUEST                      0x051D1448    436B
  CMSG_LUCKY_GIFT_INFO_RETURN                           0x051CF3A8   1264B
  CMSG_LUCKY_GIFT_NOTICE_RECEIVE                        0x051D1174    340B
  CMSG_LUCKY_GIFT_TIMEOUT                               0x051D0F38     72B
  CMSG_LUCKY_LINE_OPEN_REQUEST                          0x051D25C4     72B
  CMSG_LUCKY_LINE_OPEN_RETURN                           0x051D2920    884B
  CMSG_LUCKY_LINE_SET_PRIZE_REQUEST                     0x051D2D7C     72B
  CMSG_LUCKY_LINE_SET_PRIZE_RETURN                      0x051D2EE4     88B
  CMSG_LUCKY_RED_PACK_DETAILED_INFO_REQUEST             0x051D74E0    184B
  CMSG_LUCKY_RED_PACK_INFO_RETURN                       0x051D51F4   2404B
  CMSG_LUCKY_RED_PACK_THANK_REQUEST                     0x051D8AE8    436B
  CMSG_LUCKY_RED_PACK_THANK_RETURN                      0x051D8DBC     88B
  CMSG_LUCKY_SHOP_SCRATCH_CARD                          0x051DE620     56B
  CMSG_LUCKY_TURNTABLE_SET_PRIZE_REQUEST                0x051DF8D8     72B
  CMSG_LUCKY_TURNTABLE_SET_PRIZE_RETURN                 0x051DFA40     88B
  CMSG_LUCKY_TURNTABLE_TURN_NEW_SERVER_REQUEST          0x051DF238     72B
  CMSG_LUCKY_TURNTABLE_TURN_NEW_SERVER_RETURN           0x051DF518    728B
  CMSG_LUCKY_TURNTABLE_TURN_REQUEST                     0x051DEB98     72B
  CMSG_LUCKY_TURNTABLE_TURN_RETURN                      0x051DEE78    728B
  CMSG_LUNA_SHOP_BUY_REQUEST                            0x051E0498    184B
  CMSG_LUNA_SHOP_BUY_RETURN                             0x051E0714    136B
  CMSG_LUNA_SHOP_FREE_REWARD_REQUEST                    0x051E0E04    152B
  CMSG_LUNA_SHOP_FREE_REWARD_RETURN                     0x051E0F5C     56B
  CMSG_LUNA_SHOP_REFRESH_REQUEST                        0x051E1240    168B
  CMSG_LUNA_SHOP_REFRESH_RETURN                         0x051E1580    684B
  CMSG_LUNA_SHOP_REWARD_REQUEST                         0x051E0A08    152B
  CMSG_LUNA_SHOP_REWARD_RETURN                          0x051E0B60     56B
  CMSG_LUNA_SHOP_SYNC_LUCKY_VALUE                       0x051E1980    104B
  CMSG_LUXURY_REWARD_INFO                               0x051E1B18     88B
  CMSG_MAGIC_LAMP_INFO                                  0x051E1EE8    580B
  CMSG_MAGIC_LAMP_INFO_REQUEST                          0x051E25A8    152B
  CMSG_MAILBOX_MAIL                                     0x051E3928   1916B
  CMSG_MAILBOX_MAIL_IDS                                 0x051E2D88    500B
  CMSG_MAILBOX_MAIL_OPERATION                           0x051E433C    744B
  CMSG_MAILBOX_MAIL_OPERATION_NEW                       0x051E566C    884B
  CMSG_MAILBOX_MAIL_REQUEST                             0x051E3118    444B
  CMSG_MAILBOX_MAIL_REQUEST_NEW                         0x051E5094    552B
  CMSG_MARCH_USE_ITEM                                   0x0521302C    120B
  CMSG_MARCH_USE_ITEM_NEW                               0x05213378    200B
  CMSG_MARCH_USE_ITEM_ONEKEY                            0x0521384C    644B
  CMSG_MARKET_INFO                                      0x0523D114    356B
  CMSG_MARKET_SUPPORT                                   0x0523D4A4    432B
  CMSG_MATCH_SERVER_INFO_REQUEST                        0x050DDF84     72B
  CMSG_MATCH_SERVER_INFO_RETURN                         0x050E1930    100B
  CMSG_MERGE_EVNET_REWARD_REQUEST                       0x05243500     72B
  CMSG_MERGE_EVNET_REWARD_RETURN                        0x05243664     88B
  CMSG_MERGE_GAME_ADD_ENERGY_REQUEST                    0x05246C94    168B
  CMSG_MERGE_GAME_ADD_ENERGY_RETURN                     0x05246E74     72B
  CMSG_MERGE_GAME_ENERGY_CD_END                         0x05246948    152B
  CMSG_MERGE_GAME_GIFT_DETAILED_INFO_REQUEST            0x05247EB8    184B
  CMSG_MERGE_GAME_GIFT_END_TIME_REQUEST                 0x05249060    552B
  CMSG_MERGE_GAME_GIFT_INFO_RETURN                      0x0524732C    716B
  CMSG_MERGE_GAME_GIFT_NOTICE_RECEIVE                   0x05248BDC    340B
  CMSG_MERGE_GAME_GIFT_RECEIVE_NUM                      0x05249374     72B
  CMSG_MERGE_GAME_GIFT_TIMEOUT                          0x052489A0     72B
  CMSG_MERGE_GAME_MOVE_REQUEST                          0x05245288    168B
  CMSG_MERGE_GAME_MOVE_RETURN                           0x05245488    104B
  CMSG_MERGE_GAME_RECEIVE_ACHIEVEMENT_REQUEST           0x05245E54    168B
  CMSG_MERGE_GAME_RECEIVE_ACHIEVEMENT_RETURN            0x05245FE4     72B
  CMSG_MERGE_GAME_RECEIVE_PASS_REQUEST                  0x05246298    152B
  CMSG_MERGE_GAME_RECEIVE_PASS_RETURN                   0x05246510    460B
  CMSG_MERGE_GAME_START_REQUEST                         0x05244E4C    152B
  CMSG_MERGE_GAME_START_RETURN                          0x05244FA4     56B
  CMSG_MERGE_GAME_USE_ITEM_REQUEST                      0x0524586C    232B
  CMSG_MERGE_GAME_USE_ITEM_RETURN                       0x05245B18    136B
  CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST                0x0505CEFC     56B
  CMSG_MICROPAYMENT_DAILY_REWARD_RETURN                 0x0505D01C     72B
  CMSG_MIGRATE_COST_REQUEST                             0x0505C5F0     72B
  CMSG_MIGRATE_COST_RETURN                              0x0505C7FC    136B
  CMSG_MINI_GAME_PLAYER_REQUEST                         0x0524C90C     56B
  CMSG_MINI_GAME_PLAYER_RETURN                          0x0524CBFC    660B
  CMSG_MINI_GAME_RANK_REQUEST                           0x0524B488     88B
  CMSG_MINI_GAME_RANK_RETURN                            0x0524B7B4    644B
  CMSG_MINI_GAME_SHOP_BUY_REQUEST                       0x0524BEA0     88B
  CMSG_MINI_GAME_SHOP_BUY_RETURN                        0x0524C018     88B
  CMSG_MOBILIZATION_ACTION_RANK_INFO_REQUEST            0x05250844     72B
  CMSG_MOBILIZATION_ACTION_RANK_INFO_RETURN             0x05250C90   1076B
  CMSG_MOBILIZATION_ACTION_STATUS_REQUEST               0x0524FF38     56B
  CMSG_MOBILIZATION_ACTION_STATUS_RETURN                0x0525005C     72B
  CMSG_MOBILIZATION_ACTION_TASK_INFO_REQUEST            0x05250164     56B
  CMSG_MOBILIZATION_ACTION_TASK_INFO_RETURN             0x052504C4    664B
  CMSG_MOBILIZATION_CONTRIBUTE_INFO_REQUEST             0x052511AC     72B
  CMSG_MOBILIZATION_CONTRIBUTE_INFO_RETURN              0x05251444    636B
  CMSG_MOBILIZATION_DELETE_TASK_REQUEST                 0x05252948     72B
  CMSG_MOBILIZATION_FINISH_TASK_REQUEST                 0x05252A78     72B
  CMSG_MOBILIZATION_FINISH_TASK_RETURN                  0x05252C4C    120B
  CMSG_MOBILIZATION_GET_REWARD_REQUEST                  0x05252014    392B
  CMSG_MOBILIZATION_GET_REWARD_RETURN                   0x05252280     72B
  CMSG_MOBILIZATION_GET_TASK_REQUEST                    0x052523B0     72B
  CMSG_MOBILIZATION_GET_TASK_RETURN                     0x05252550    104B
  CMSG_MOBILIZATION_GIVE_UP_TASK_REQUEST                0x052526A0     72B
  CMSG_MOBILIZATION_GIVE_UP_TASK_RETURN                 0x05252808     88B
  CMSG_MOBILIZATION_REWARD_CONFIG_REQUEST               0x05251780     56B
  CMSG_MOBILIZATION_REWARD_CONFIG_RETURN                0x05251A40   1096B
  CMSG_MODIFY_LEAGUE_NUMBER_VALUE                       0x050FCE10     88B
  CMSG_MODIFY_LEAGUE_STRING_VALUE                       0x050FD028    324B
  CMSG_MONSTER_DELETE_RECORD_REQUEST                    0x0525753C     56B
  CMSG_MONSTER_DIE                                      0x052149F8     88B
  CMSG_MONSTER_RECORD_INFO                              0x05257174    776B
  CMSG_MONSTER_RECORD_SET_FLAG_REQUEST                  0x05257634     56B
  CMSG_MONSTER_SYNC                                     0x051EC9F4    828B
  CMSG_MONTH_REFRESH_REQUEST                            0x052C2DE0     56B
  CMSG_MOVE_CASTLE                                      0x051EB264    136B
  CMSG_MOVE_CASTLE_NEW                                  0x05215F74    216B
  CMSG_NEWSERVER_LIMITSHOP_BUY_REQUEST                  0x0525B3E4    120B
  CMSG_NEWSERVER_LIMITSHOP_BUY_RETURN                   0x0525B620    136B
  CMSG_NEWSERVER_LIMITSHOP_GIFT_REQUEST                 0x0525B834    120B
  CMSG_NEWSERVER_LIMITSHOP_GIFT_RETURN                  0x0525BA00    104B
  CMSG_NEWSERVER_RECORDCOST_REWARD_REQUEST              0x0525A754    104B
  CMSG_NEWSERVER_RECORDCOST_REWARD_RETURN               0x0525A944    120B
  CMSG_NEWSERVER_SIGNFUND_UNLOCK_REQUEST                0x0525C568     72B
  CMSG_NEWSERVER_SIGNFUND_UNLOCK_RETURN                 0x0525C6FC    104B
  CMSG_NEWSERVER_SIGNINFUND_REWARD_REQUEST              0x0525C140    104B
  CMSG_NEWSERVER_SIGNINFUND_REWARD_RETURN               0x0525C3D8    168B
  CMSG_NEWS_INFO_REQUEST                                0x0525D378     56B
  CMSG_NEWS_INFO_RETURN                                 0x0525D630    792B
  CMSG_NEW_LUCKY_RED_PACK_NOTICE                        0x051D86F4    136B
  CMSG_NEW_ONLINE_REWARD_REQUEST                        0x052C3C00     56B
  CMSG_NEW_ONLINE_REWARD_SUCCESS                        0x052C4278    508B
  CMSG_NEW_SYN_ONLINE_INFO                              0x052C3E60    548B
  CMSG_NOTIFY_APPLY_ENTER_LEAGUE_RESULT                 0x050F819C     88B
  CMSG_NOTIFY_BE_LEAGUE_HELP                            0x05167F40    504B
  CMSG_NOTIFY_CANCEL_COLLECT                            0x051F5130     72B
  CMSG_NOTIFY_CASTLE_REBUILD                            0x05214B38     72B
  CMSG_NOTIFY_COLLECT_INFO                              0x051F4C28    168B
  CMSG_NOTIFY_DOMINION_OCCUPY                           0x05045F94    532B
  CMSG_NOTIFY_LEAGUE_MEMBER_LEAVE                       0x05102FDC     72B
  CMSG_NOTIFY_LEAGUE_MEMBER_LEVEL_NAME                  0x050F94F8    692B
  CMSG_NOTIFY_LEAVE_LEAGUE                              0x051030E4     56B
  CMSG_NOTIFY_LEGION_CHANGE_POS_TIMES                   0x0511B198     88B
  CMSG_NOTIFY_LEGION_MEMBER_CHANGE                      0x0511967C    512B
  CMSG_NOTIFY_LEGION_MEMBER_JOIN                        0x051186BC    480B
  CMSG_NOTIFY_LEGION_MEMBER_LEAVE                       0x051189BC     88B
  CMSG_NOTIFY_LEGION_NAME_CHANGE                        0x0511A08C    324B
  CMSG_NOTIFY_MARCH_END                                 0x051F4FBC    136B
  CMSG_NOTIFY_MODIFY_LEAGUE_VALUE_RESULT                0x050FCC98     88B
  CMSG_NOTIFY_OWNER_CASTLE                              0x051F4984    120B
  CMSG_NOTIFY_OWNER_LEAGUE_INFO                         0x050F5B60   3528B
  CMSG_NOTIFY_OWNER_LEAGUE_INFO_NEW                     0x050F3C10   4036B
  CMSG_NOTIFY_OWNER_MARCH                               0x051E87E4    608B
  CMSG_NOTIFY_REFUSE_INVITE                             0x05102DA0     88B
  CMSG_NOTIFY_STOP_COLLECT                              0x051F4DBC     72B
  CMSG_NOVICE_FREE_PURCHASE_BUY_GIFT_REQUEST            0x0525F424     72B
  CMSG_NOVICE_FREE_PURCHASE_BUY_GIFT_RETURN             0x0525F658    508B
  CMSG_NOVICE_FREE_PURCHASE_GET_AWARD_REQUEST           0x0525F93C     72B
  CMSG_NOVICE_FREE_PURCHASE_GET_AWARD_RETURN            0x0525FB70    508B
  CMSG_NOVICE_RECHARG_REWARD_INFO                       0x05260080    620B
  CMSG_NPC_HELP_REQUEST                                 0x0527D288     72B
  CMSG_NPC_HELP_RETURN                                  0x0527D3B8     72B
  CMSG_NPC_REWARD_REQUEST                               0x0505D67C     72B
  CMSG_OBJECT_LEAVE_SCENE                               0x051F47A0     88B
  CMSG_OPEN_AREA_REQUEST                                0x04FCB410     72B
  CMSG_OPEN_AREA_RETURN                                 0x04FCB670     72B
  CMSG_OPEN_LEAGUE_GIFT_INTEGRAL_REWARD_REQUEST         0x05166038     72B
  CMSG_OPEN_SESAME_ATTACK_MONSTER_REQUEST               0x05264660    888B
  CMSG_OPEN_SESAME_ATTACK_MONSTER_RETURN                0x0526525C   2556B
  CMSG_OPEN_SESAME_CHOOSE_DIC_REQUEST                   0x052636D8     88B
  CMSG_OPEN_SESAME_CHOOSE_DIC_RETURN                    0x05263BD4   1844B
  CMSG_OPEN_SESAME_CHOOSE_REWARD_REQUEST                0x05265DE4    120B
  CMSG_OPEN_SESAME_CHOOSE_REWARD_RETURN                 0x05266198   1148B
  CMSG_OPEN_SESAME_CONFIG                               0x05260D1C   1800B
  CMSG_OPEN_SESAME_INFO_REQUEST                         0x0526150C     72B
  CMSG_OPEN_SESAME_INFO_RETURN                          0x05262324   4756B
  CMSG_OPEN_SESAME_LAYER_REWARD_REQUEST                 0x052673F8     88B
  CMSG_OPEN_SESAME_LAYER_REWARD_RETURN                  0x05267570     88B
  CMSG_OPEN_SESAME_MOVE_NEXT_LAYER_REQUEST              0x052666FC     72B
  CMSG_OPEN_SESAME_MOVE_NEXT_LAYER_RETURN               0x05266BAC   1836B
  CMSG_OPEN_SESAME_NPC_REWARD_REQUEST                   0x05268CE4    120B
  CMSG_OPEN_SESAME_NPC_REWARD_RETURN                    0x05269298   1712B
  CMSG_OPEN_SESAME_RANK_REQUEST                         0x05269A68     88B
  CMSG_OPEN_SESAME_RANK_RETURN                          0x05269FAC   1260B
  CMSG_OPEN_SESAME_STATUS_INFO                          0x05267764    604B
  CMSG_OPEN_VIP_BOX                                     0x052C4CA4     72B
  CMSG_OPEN_VIP_BOX_RETURN                              0x052C4F44    544B
  CMSG_OPERATION_ACTION_RANK_RECORD_REQUEST             0x0526D3F4     72B
  CMSG_OPERATION_ACTION_RANK_RECORD_RETURN              0x0526D898   1396B
  CMSG_OUTFIRE_REQUEST                                  0x0505BF08     56B
  CMSG_PASSWORD_CHECK_REQUEST                           0x0527392C    168B
  CMSG_PASSWORD_CHECK_RETURN                            0x05273AC0     72B
  CMSG_PASSWORD_INFO                                    0x052735F4    136B
  CMSG_PASSWORD_RESET_CD_END                            0x05274708    152B
  CMSG_PASSWORD_RESET_REQUEST                           0x0527427C    168B
  CMSG_PASSWORD_RESET_RETURN                            0x05274444     88B
  CMSG_PASSWORD_SET_REQUEST                             0x05273DE4    184B
  CMSG_PASSWORD_SET_RETURN                              0x05273F88     72B
  CMSG_PC_VERSION_CONTROL                               0x0517C35C     88B
  CMSG_PET_CHNAGE_SHOW_REQUEST                          0x05278F20     72B
  CMSG_PET_CHNAGE_SHOW_RETURN                           0x05279050     72B
  CMSG_PET_EXCHNGE_FOOD_REQUEST                         0x05278644     72B
  CMSG_PET_EXCHNGE_FOOD_RETURN                          0x05278880    508B
  CMSG_PET_FEED_FREE_REQUEST                            0x05276568     72B
  CMSG_PET_FEED_FREE_RETURN                             0x052768B8    456B
  CMSG_PET_FEED_GOLD_REQUEST                            0x05276BA0     88B
  CMSG_PET_FEED_GOLD_RETURN                             0x05276F00    456B
  CMSG_PET_GET_NAMEPLATE_INFO_REQUEST                   0x052793E4     72B
  CMSG_PET_GET_NAMEPLATE_INFO_RETURN                    0x052797F4    732B
  CMSG_PET_HUNT_QUICK_REQUEST                           0x05278044     88B
  CMSG_PET_HUNT_QUICK_RETURN                            0x0527832C    560B
  CMSG_PET_HUNT_REQUEST                                 0x052771B0     72B
  CMSG_PET_HUNT_RESULT_REQUEST                          0x05277610    184B
  CMSG_PET_HUNT_RESULT_REQUEST_NEW                      0x052779D0    216B
  CMSG_PET_HUNT_RESULT_RETURN                           0x05277D04    544B
  CMSG_PET_HUNT_RETURN                                  0x05277318     88B
  CMSG_PET_RENAME_REQUEST                               0x05275FDC    324B
  CMSG_PET_RENAME_RETURN                                0x05276318    360B
  CMSG_PET_SET_NAMEPLATE_REQUEST                        0x05279180     72B
  CMSG_PET_SET_NAMEPLATE_RETURN                         0x052792B0     72B
  CMSG_PET_UNLOCK_REQUEST                               0x05275508    324B
  CMSG_PET_UNLOCK_RETURN                                0x05275ADC    824B
  CMSG_PET_UPGRADE_SKILL_REQUEST                        0x05278BD0    104B
  CMSG_PET_UPGRADE_SKILL_RETURN                         0x05278DC0    120B
  CMSG_PLACEMENT_LIMIT_COUNT                            0x051F3968     72B
  CMSG_PLACEMENT_SYNC                                   0x051F33D8   1192B
  CMSG_PLAYER_MIGRATE_RESULT                            0x0524A034     72B
  CMSG_PLOT_QUEST_CHANGE_FLAG                           0x0527EB04     72B
  CMSG_PLOT_QUEST_CHANGE_FLAG_NEW                       0x0527F36C     72B
  CMSG_PLOT_QUEST_COMPLETED                             0x0527E7AC     72B
  CMSG_PLOT_QUEST_COMPLETED_NEW                         0x0527F10C     72B
  CMSG_PLOT_QUEST_RECEIVE_AWARD                         0x0527E8DC     72B
  CMSG_PLOT_QUEST_RECEIVE_AWARD_NEW                     0x0527F23C     72B
  CMSG_PLOT_QUEST_RESIST_NPC_REQUEST                    0x0527EC0C     56B
  CMSG_PLOT_QUEST_RESIST_NPC_REQUEST_NEW                0x0527F474     56B
  CMSG_PLOT_QUEST_UNLOCK                                0x0527F648    444B
  CMSG_PLOT_VERSION_REQUEST                             0x0527E9E4     56B
  CMSG_PM_COMMAND                                       0x052701DC    308B
  CMSG_PM_EFFECT_RETURN                                 0x05270430     88B
  CMSG_POST_TASK_CD_RESET                               0x05281098    152B
  CMSG_POST_TASK_CD_RESET_RETURN                        0x05281428    744B
  CMSG_POST_TASK_FINISH                                 0x05282134    168B
  CMSG_POST_TASK_FINISH_RETURN                          0x052822FC     88B
  CMSG_POST_TASK_FORCE_FINISH                           0x0528269C    540B
  CMSG_POST_TASK_FORCE_FINISH_RETURN                    0x05282A54    444B
  CMSG_POST_TASK_LEVEL_REWARD                           0x052836B4    168B
  CMSG_POST_TASK_LEVEL_REWARD_RETURN                    0x05283844     72B
  CMSG_POST_TASK_NOTIFY                                 0x0528394C     56B
  CMSG_POST_TASK_RESET                                  0x05280790    188B
  CMSG_POST_TASK_RESET_RETURN                           0x05280B44    744B
  CMSG_POST_TASK_REWARD                                 0x05282EC4    168B
  CMSG_POST_TASK_REWARD_RETURN                          0x052831CC    564B
  CMSG_POST_TASK_START                                  0x05281AC8    524B
  CMSG_POST_TASK_START_RETURN                           0x05281DF0    144B
  CMSG_POWER_TASKS_REQUEST                              0x052871E0     56B
  CMSG_POWER_TASKS_RETURN                               0x05287528   1052B
  CMSG_POWER_TASK_REWARD_REQUEST                        0x05286B54    500B
  CMSG_POWER_TASK_REWARD_RETURN                         0x05286F3C    484B
  CMSG_PRODUCT_SHOW_EVENT_INFO                          0x05283BBC    708B
  CMSG_PRODUCT_SHOW_REWARD_REQUEST                      0x05284134    168B
  CMSG_PRODUCT_SHOW_REWARD_RETURN                       0x052842C4     72B
  CMSG_PVE_CHALLENGE_REQUEST                            0x05270DA8    488B
  CMSG_PVE_CHALLENGE_RETURN                             0x0527111C    120B
  CMSG_PVE_FAST_FIGHT_REQUEST                           0x0527158C    104B
  CMSG_PVE_FAST_FIGHT_RETURN                            0x05271A64   1380B
  CMSG_PVE_FIGHT_ONE_KEY_REQUEST                        0x0527230C    216B
  CMSG_PVE_FIGHT_ONE_KEY_RETURN                         0x052726AC    596B
  CMSG_PVE_POINT_CD_END                                 0x0505C3A0     56B
  CMSG_PVE_RECEIVE_AWARD_REQUEST                        0x0527127C     72B
  CMSG_PVE_RECEIVE_AWARD_RETURN                         0x052713E0     88B
  CMSG_PVE_SYNC_INFO                                    0x052707EC    812B
  CMSG_QUERY_ACTIVITY_LUCKY_GIFT_INFO_REQUEST           0x051D16BC     56B
  CMSG_QUERY_ACTIVITY_RUSH_EVENT                        0x04FA205C    168B
  CMSG_QUERY_ALL_DOMINION_BATTLE                        0x05049540     56B
  CMSG_QUERY_ALL_DOMINION_OCCUPY                        0x05049B44     56B
  CMSG_QUERY_BUILDUP_BATTLE_ATK_TIME                    0x05213DAC     88B
  CMSG_QUERY_CYCLE_ACTION                               0x05018564     72B
  CMSG_QUERY_DEFEND_HERO_INFO                           0x0510BB98     72B
  CMSG_QUERY_DOMINION_ACTION_HISTORY_REQUEST            0x0503CB30     56B
  CMSG_QUERY_DOMINION_ACTION_HISTORY_RETURN             0x0503CF30   1064B
  CMSG_QUERY_DOMINION_ACTION_INTEGRAL_REQUEST           0x0503C254     56B
  CMSG_QUERY_DOMINION_ACTION_INTEGRAL_RETURN            0x0503C648   1064B
  CMSG_QUERY_DOMINION_DEFEND_INFO                       0x05045CA8     72B
  CMSG_QUERY_DOMINION_DEFEND_NUM_REQUEST                0x05044820    440B
  CMSG_QUERY_DOMINION_DEFEND_NUM_RETURN                 0x05044B8C    480B
  CMSG_QUERY_DOMINION_DETAIL_INFO                       0x05045918     72B
  CMSG_QUERY_DOMINION_INFO                              0x050457F8     56B
  CMSG_QUERY_DOMINION_OFFICIAL_INFO                     0x05045B78     72B
  CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO                0x05045A48     72B
  CMSG_QUERY_FORTRESS_ACTION                            0x0506C7EC     56B
  CMSG_QUERY_KINGDOM_ACTION                             0x050DCAB0     72B
  CMSG_QUERY_KINGDOM_STRATEGY_COIN                      0x050E6408     56B
  CMSG_QUERY_KING_CHESS_ACTION                          0x050C4168     56B
  CMSG_QUERY_KING_CHESS_DEFEND_INFO                     0x050C9E44     72B
  CMSG_QUERY_KING_CHESS_DETAIL_INFO                     0x050CB210     72B
  CMSG_QUERY_KING_CHESS_SIMPLE_BATTLE_INFO              0x050CCA24     72B
  CMSG_QUERY_KING_INFO_REQUEST                          0x0503D418     56B
  CMSG_QUERY_KING_INFO_RETURN                           0x0503D808    764B
  CMSG_QUERY_LAND_BATTLE                                0x0510BCC8     72B
  CMSG_QUERY_LEAGUE                                     0x050F6C78    344B
  CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO                    0x0515C14C    168B
  CMSG_QUERY_LEAGUEPASS_ACTION                          0x0516AE90     56B
  CMSG_QUERY_LEAGUE_BATTLE                              0x0510C368    468B
  CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION                  0x05112564     56B
  CMSG_QUERY_LEAGUE_BATTLE_KING_CHESS                   0x050C85BC    468B
  CMSG_QUERY_LEAGUE_BATTLE_RECORD                       0x0510C628     72B
  CMSG_QUERY_LEAGUE_HELP                                0x051677B8     56B
  CMSG_QUERY_LEAGUE_INVITE                              0x050F6F90    344B
  CMSG_QUERY_LEAGUE_INVITE_PAGE                         0x050F7414    376B
  CMSG_QUERY_LEAGUE_MEMBER_INFO                         0x0510330C     56B
  CMSG_QUERY_LEAGUE_MONEY_REQUEST                       0x05103524     72B
  CMSG_QUERY_LEAGUE_MONEY_RETURN                        0x0510368C     88B
  CMSG_QUERY_LEAGUE_PAGE                                0x050F71D4     72B
  CMSG_QUERY_LEAGUE_TSAK_INFO                           0x050F8E00     56B
  CMSG_QUERY_LOSTLAND_ACTION_CONFIG                     0x051A6F94     56B
  CMSG_QUERY_LOSTLAND_RUSH_EVENT                        0x04FA4288    168B
  CMSG_QUERY_MAP                                        0x051E8224    104B
  CMSG_QUERY_MAP_KING_CHESS                             0x050C88B0     88B
  CMSG_QUERY_MAP_RESULT                                 0x05211C50     56B
  CMSG_QUERY_MARCH_ARMY_INFO                            0x05214650     72B
  CMSG_QUERY_MOBILIZATION_ACTION                        0x0524FBAC     56B
  CMSG_QUERY_NAME_INFO                                  0x052140A0     88B
  CMSG_QUERY_OPERATION_ACTION                           0x0526C554     72B
  CMSG_QUERY_OTHER_LEAGUE_INFO                          0x05100214     72B
  CMSG_QUERY_OTHER_LEAGUE_MEMBER                        0x0510177C     72B
  CMSG_QUERY_OTHER_SERVER_ALL_DOMINION_INFO             0x05049C64     72B
  CMSG_QUERY_RECOMMEND_LEAGUE_REQUEST                   0x05104224     56B
  CMSG_QUERY_RECOMMEND_LEAGUE_RETURN                    0x05104508    532B
  CMSG_QUERY_RUSH_ACTION                                0x052B1DB0     72B
  CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_REQUEST     0x050409C0     72B
  CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_RETURN      0x05040DD0   1064B
  CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_REQUEST    0x0503FF38     72B
  CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_RETURN     0x0504033C   1064B
  CMSG_QUERY_SERVER_KING_INFO_REQUEST                   0x050412E0     72B
  CMSG_QUERY_SERVER_KING_INFO_RETURN                    0x0504168C    724B
  CMSG_QUERY_SPECIAL_EVENT_RETURN                       0x052D141C    604B
  CMSG_QUERY_WAR_LORD_ACTION                            0x052E6EAC     72B
  CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG                 0x052F6398     56B
  CMSG_QUERY_lEAGUE_BUILD_DESTORY_INFO                  0x0515D640     88B
  CMSG_QUEST_CHAMPIONSHIP_REQUEST                       0x04FD34E4     56B
  CMSG_QUICK_LOGIN_REQUEST                              0x0517CB60    400B
  CMSG_QUICK_LOGIN_RETURN                               0x0517CDD8     72B
  CMSG_RAID_PLAYER_ERROR_RETURN                         0x0523E888     72B
  CMSG_RAID_PLAYER_REQUEST                              0x0523E768     56B
  CMSG_RAID_PLAYER_REQUEST_NEW                          0x0523F2C0    136B
  CMSG_RANDOM_ONLINE_REWARD_REQUEST                     0x052C4534     56B
  CMSG_RANDOM_ONLINE_REWARD_RETURN                      0x052C4724    484B
  CMSG_RANK_INFO_REQUEST                                0x05288084     88B
  CMSG_RANK_INFO_RETURN                                 0x05289034   6168B
  CMSG_RANK_SIMPLE_INFO_REQUEST                         0x0528AA48    512B
  CMSG_RANK_SIMPLE_INFO_RETURN                          0x0528AE5C    480B
  CMSG_READ_LEAGUE_INVITE                               0x050FAD6C     72B
  CMSG_REBUILDING_OASISE_TASKS_RECIEVE_REQUEST          0x05295200    168B
  CMSG_REBUILDING_OASISE_TASKS_RECIEVE_RETURN           0x05295390     72B
  CMSG_REBUILDING_OASISE_TASKS_REWARD_REQUEST           0x0529568C    168B
  CMSG_REBUILDING_OASISE_TASKS_REWARD_RETURN            0x05295854     88B
  CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST              0x04F9D104     88B
  CMSG_RECEIVE_ACCUMULATION_REWARD_RETURN               0x04F9D27C     88B
  CMSG_RECEIVE_ACTIVITY_LUCKY_GIFT_REQUEST              0x051D17B4     56B
  CMSG_RECEIVE_ALL_LEAGUE_GIFT_REQUEST                  0x05165E20     56B
  CMSG_RECEIVE_ALL_LEAGUE_GIFT_RETURN                   0x05165F18     56B
  CMSG_RECEIVE_CITY_FUND_REWARD                         0x0505CBCC     72B
  CMSG_RECEIVE_CITY_LV_GOLD_REWARD                      0x0505CA9C     72B
  CMSG_RECEIVE_CITY_LV_REWARD                           0x0505C96C     72B
  CMSG_RECEIVE_FANS_REWARD                              0x0505CDF4     72B
  CMSG_RECEIVE_FIRST_BIND_REWARD                        0x052DA428     56B
  CMSG_RECEIVE_INDEX_NOVICE_RECHARG_REWARD              0x05260640     72B
  CMSG_RECEIVE_LEAGUE_GIFT_REQUEST                      0x05165BE4     72B
  CMSG_RECEIVE_LEAGUE_GIFT_RETURN                       0x05165D18     72B
  CMSG_RECEIVE_LEAGUE_TSAK                              0x050F8F20     72B
  CMSG_RECEIVE_LUCKY_RED_PACK_NOTICE                    0x051D70D4    324B
  CMSG_RECEIVE_LUCKY_RED_PACK_REQUEST                   0x051D6C5C    184B
  CMSG_RECEIVE_LUCKY_RED_PACK_RETURN                    0x051D6E9C    120B
  CMSG_RECEIVE_LUXURY_REWARD                            0x051E1C58     72B
  CMSG_RECEIVE_MERGE_GAME_GIFT_REQUEST                  0x05247B24    184B
  CMSG_RECEIVE_NOVICE_RECHARG_REWARD                    0x05260520     56B
  CMSG_RECEIVE_OLD_PLAYER_REWARD                        0x052DA320     72B
  CMSG_RECEIVE_ORDINARY_LUCKY_GIFT_REQUEST              0x051D01D4     88B
  CMSG_RECEIVE_RECHARG_REWARD                           0x05260748     56B
  CMSG_RECEIVE_RED_PACK_SYSTEM_REQUEST                  0x051D5DE8    168B
  CMSG_RECEIVE_RED_PACK_SYSTEM_RETURN                   0x051D5FE4    104B
  CMSG_RECEIVE_REWARD_BATCH_REQUEST                     0x0505ED9C     72B
  CMSG_RECEIVE_REWARD_BATCH_RETURN                      0x0505EF94    136B
  CMSG_RECEIVE_REWARD_REQUEST                           0x0505EA74     72B
  CMSG_RECEIVE_REWARD_RETURN                            0x0505EC3C    120B
  CMSG_RECEIVE_SIGN_ACTIVITY                            0x0505CCD4     56B
  CMSG_RECHARGEBONUS_ACTION_REQUEST                     0x05295D60     72B
  CMSG_RECHARGEBONUS_ACTION_RETURN                      0x05295F34    120B
  CMSG_RECHARGEBONUS_REWARD_REQUEST                     0x05296288     88B
  CMSG_RECHARGEBONUS_REWARD_RETURN                      0x05296434    104B
  CMSG_RED_PAPER_CHANGE_VIEW                            0x052A17E8    184B
  CMSG_RED_PAPER_CHAT_HISTORY                           0x04FD9380   2252B
  CMSG_RED_PAPER_CREATE_ROOM_REQUEST                    0x05297E84    200B
  CMSG_RED_PAPER_CREATE_ROOM_RETURN                     0x052983AC    952B
  CMSG_RED_PAPER_GAME_END                               0x052A06CC    120B
  CMSG_RED_PAPER_GAME_START                             0x052A04B8    136B
  CMSG_RED_PAPER_INVITE_PLAYER                          0x052A106C    372B
  CMSG_RED_PAPER_INVITE_PLAYER_REQUEST                  0x052A0B48    660B
  CMSG_RED_PAPER_JOIN_GAME_REQUEST                      0x0529B14C    232B
  CMSG_RED_PAPER_JOIN_GAME_RETURN                       0x0529B9F4   1744B
  CMSG_RED_PAPER_OEPN_INFO                              0x0529F730    908B
  CMSG_RED_PAPER_OPEN_REQUEST                           0x0529E5BC    168B
  CMSG_RED_PAPER_OPEN_RETURN                            0x0529E828    136B
  CMSG_RED_PAPER_PLAYER_COUNT_REQUEST                   0x052976EC    168B
  CMSG_RED_PAPER_PLAYER_COUNT_RETURN                    0x052979A8    480B
  CMSG_RED_PAPER_QUICK_GAME_REQUEST                     0x05299E90    200B
  CMSG_RED_PAPER_QUICK_GAME_RETURN                      0x0529A718   1744B
  CMSG_RED_PAPER_QUIT_GAME_REQUEST                      0x0529C990    200B
  CMSG_RED_PAPER_QUIT_GAME_RETURN                       0x0529CBE4    120B
  CMSG_RED_PAPER_QUIT_VIEW                              0x052A1474    168B
  CMSG_RED_PAPER_RECORD_REQUEST                         0x0529EB74    184B
  CMSG_RED_PAPER_RECORD_RETURN                          0x0529EFE8    908B
  CMSG_RED_PAPER_REPLACE_TO_GAME_REQUEST                0x0529C3C4    200B
  CMSG_RED_PAPER_REPLACE_TO_GAME_RETURN                 0x0529C618    120B
  CMSG_RED_PAPER_ROOM_DETAIL_REQUEST                    0x0529CEF0    168B
  CMSG_RED_PAPER_ROOM_DETAIL_RETURN                     0x0529D724   1716B
  CMSG_RED_PAPER_ROOM_INFO_REQUEST                      0x05298A2C    184B
  CMSG_RED_PAPER_ROOM_INFO_RETURN                       0x05299124   2672B
  CMSG_RED_PAPER_SHOP_BUY_REQUEST                       0x052A1F10    184B
  CMSG_RED_PAPER_SHOP_BUY_RETURN                        0x052A20E8     88B
  CMSG_RED_PAPER_SIMP_RECORD_REQUEST                    0x0529FD50    168B
  CMSG_RED_PAPER_SIMP_RECORD_RETURN                     0x052A007C    636B
  CMSG_RED_PAPER_UPDATE_GAME                            0x0529E160    456B
  CMSG_REQUEST_BATTLE_TARGET                            0x05215358     56B
  CMSG_REQUEST_BROADCAST_INVITE                         0x05103FFC     56B
  CMSG_REQUEST_BUILDUP_BATTLE_MOVE_TIME                 0x0505620C     72B
  CMSG_REQUEST_MONSTER_POS                              0x052156E4    104B
  CMSG_REQUEST_PLAYER_INFO                              0x05214CD4    104B
  CMSG_REQUEST_TRIBUTE_INFO                             0x052E5788     56B
  CMSG_RESOURCE_SYNC                                    0x051F0FEC   1568B
  CMSG_RESPONSE_BATTLE_TARGET                           0x05215514    120B
  CMSG_RESPONSE_BUILDUP_BATTLE_MOVE_TIME                0x0505660C   1228B
  CMSG_RESPONSE_MONSTER_POS                             0x05215910    136B
  CMSG_RESPONSE_PLAYER_INFO                             0x052150A8    496B
  CMSG_RESP_LEAGUE_INFO_LIST                            0x050FF0C0   3208B
  CMSG_RESP_LEAGUE_INVITE_LIST                          0x050F7900    844B
  CMSG_RETURN_EVENT_ACTION_REQUEST                      0x052AF00C     72B
  CMSG_RETURN_EVENT_ACTION_REQUEST_NEW                  0x052AF988     72B
  CMSG_RETURN_EVENT_ACTION_RETURN                       0x052AF218    136B
  CMSG_RETURN_EVENT_ACTION_RETURN_NEW                   0x052AFC00    168B
  CMSG_RETURN_EVENT_REWARD_REQUEST                      0x052AF3BC     88B
  CMSG_RETURN_EVENT_REWARD_REQUEST_NEW                  0x052AFDC4     88B
  CMSG_RETURN_EVENT_REWARD_RETURN                       0x052AF560    104B
  CMSG_RETURN_EVENT_REWARD_RETURN_NEW                   0x052AFF68    104B
  CMSG_REWARD_BOX                                       0x050C2144    484B
  CMSG_REWARD_INFO                                      0x0505F1D4    492B
  CMSG_REWARD_POINT_SHOP_ITEM_INFO_REQUEST              0x052B0460     56B
  CMSG_REWARD_POINT_SHOP_ITEM_INFO_RETURN               0x052B06E4    664B
  CMSG_REWARD_TASKS_HERO_REQUEST                        0x05173F78     72B
  CMSG_REWARD_TASKS_HERO_RETURN                         0x051743B8    908B
  CMSG_REWARD_TASKS_INFO_REQUEST                        0x051738F8     56B
  CMSG_REWARD_TASKS_INFO_RETURN                         0x05173BD8    696B
  CMSG_REWARD_TASK_JOIN_REQUEST                         0x05174918    436B
  CMSG_REWARD_TASK_JOIN_RETURN                          0x05174CC0    484B
  CMSG_REWARD_TASK_MY_HEROS_REQUEST                     0x051764DC     56B
  CMSG_ROYAL_SHOP_ITEM_CONFIG_REQUEST                   0x050B7D0C     56B
  CMSG_ROYAL_SHOP_ITEM_CONFIG_RETURN                    0x050B7FAC    732B
  CMSG_ROYAL_SHOP_ITEM_INFO_REQUEST                     0x050B8704     56B
  CMSG_ROYAL_SHOP_ITEM_INFO_RETURN                      0x050B8950    680B
  CMSG_SCIENCE_CANCEL_STUDY_REQUEST                     0x052B412C     72B
  CMSG_SCIENCE_GOLD_SPEED                               0x052B4394     72B
  CMSG_SCIENCE_GOLD_STUDY_REQUEST                       0x052B3FF8     72B
  CMSG_SCIENCE_HELP_REQUEST                             0x052B4EC0     56B
  CMSG_SCIENCE_INFO                                     0x052B3964   1072B
  CMSG_SCIENCE_ITEM_SPEED                               0x052B4534    104B
  CMSG_SCIENCE_ITEM_SPEED_ONEKEY                        0x052B4944    628B
  CMSG_SCIENCE_NORMAL_STUDY_REQUEST                     0x052B3EB4     88B
  CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW                 0x052B5268    640B
  CMSG_SCIENCE_OPERAT_RETURN                            0x052B4D78    136B
  CMSG_SCIENCE_UPGRADE_OVER                             0x052B4260     72B
  CMSG_SECRET_ADD_RANGE_INFO                            0x052B5720    604B
  CMSG_SECRET_BATTLE_REQUEST                            0x052B704C    388B
  CMSG_SECRET_BATTLE_REQUEST_NEW                        0x052B7368    388B
  CMSG_SECRET_BATTLE_RETURN                             0x052B7744    544B
  CMSG_SECRET_BOSS_LEAVE                                0x052D3E3C     72B
  CMSG_SECRET_BOSS_REQUEST                              0x052D262C     72B
  CMSG_SECRET_BOSS_RETURN                               0x052D2838    136B
  CMSG_SECRET_BUY_SP_REQUEST                            0x052B7A24     56B
  CMSG_SECRET_BUY_SP_RETURN                             0x052B7B1C     56B
  CMSG_SECRET_GOLD_MINING                               0x052B7EE4     72B
  CMSG_SECRET_MINING_END                                0x052B7FEC     56B
  CMSG_SECRET_MINING_GOLD_SPEED                         0x052B80E4     56B
  CMSG_SECRET_MINING_ITEM_SPEED                         0x052B823C     88B
  CMSG_SECRET_MINING_ITEM_SPEED_ONEKEY                  0x052B85FC    612B
  CMSG_SECRET_MINING_REWARD                             0x052B8B70    968B
  CMSG_SECRET_MOVE_REQUEST                              0x052B6600    420B
  CMSG_SECRET_MOVE_RETURN                               0x052B688C     72B
  CMSG_SECRET_NORMAL_MINING                             0x052B7DB4     72B
  CMSG_SECRET_OPEN_BOX_REQUEST                          0x052B6994     56B
  CMSG_SECRET_OPEN_BOX_REQUEST_NEW                      0x052B6A8C     56B
  CMSG_SECRET_OPEN_BOX_RETURN                           0x052B6CB8    508B
  CMSG_SECRET_REWARD_INFO_REQUEST                       0x052D34F8     72B
  CMSG_SECRET_REWARD_INFO_RETURN                        0x052D38C0    796B
  CMSG_SECRET_SP_CD_END                                 0x052B6430     56B
  CMSG_SECRET_SURPRISE_INFO                             0x052B5A94     88B
  CMSG_SECRET_TASKS_BEGIN_REQUEST                       0x052BB280    592B
  CMSG_SECRET_TASKS_BEGIN_RETURN                        0x052BB708    536B
  CMSG_SECRET_TASKS_DELETE_LEAGUE_TASK                  0x052BF780    456B
  CMSG_SECRET_TASKS_FINISH                              0x052BFBFC    168B
  CMSG_SECRET_TASKS_HELP_REQUEST                        0x052BE0D0    184B
  CMSG_SECRET_TASKS_HELP_RETURN                         0x052BE318    120B
  CMSG_SECRET_TASKS_LEAUE_INFO_REQUEST                  0x052BD45C    152B
  CMSG_SECRET_TASKS_LEAUE_INFO_RETURN                   0x052BD95C   1172B
  CMSG_SECRET_TASKS_RECIEVE_REQUEST                     0x052BCBF4    660B
  CMSG_SECRET_TASKS_RECIEVE_RETURN                      0x052BD01C    468B
  CMSG_SECRET_TASKS_REFRESH_REQUEST                     0x052BBBCC    168B
  CMSG_SECRET_TASKS_REFRESH_RETURN                      0x052BC140   1904B
  CMSG_SECRET_TASKS_REPORT_REQUEST                      0x052BEB9C    152B
  CMSG_SECRET_TASKS_REPORT_RETURN                       0x052BF050   1244B
  CMSG_SECRET_TASKS_ROB_REQUEST                         0x052BE670    184B
  CMSG_SECRET_TASKS_ROB_RETURN                          0x052BE8B8    120B
  CMSG_SECRET_TASKS_SET_POS_REQUEST                     0x052BAC2C    200B
  CMSG_SECRET_TASKS_SET_POS_RETURN                      0x052BAE7C    120B
  CMSG_SECRET_TASK_SYNC                                 0x051EE1F8   1340B
  CMSG_SECRET_UPDATE_END_TIME                           0x052B905C     88B
  CMSG_SECRET_UPDATE_EXP                                0x052B7C74     88B
  CMSG_SECRET_WIN_BIG_REWARD                            0x052D3CFC     88B
  CMSG_SELF_LEAGUEBUILD_SYNC                            0x05157854   1220B
  CMSG_SELF_MARCH_QUEUE_REQUEST                         0x052113E8     72B
  CMSG_SELF_MARCH_QUEUE_RETURN                          0x05211858    824B
  CMSG_SEND_LUCKY_GIFT_REQUEST                          0x051CFAD8    356B
  CMSG_SEND_LUCKY_GIFT_RETURN                           0x051CFF14    416B
  CMSG_SEND_LUCKY_RED_PACK_REQUEST                      0x051D63C0    436B
  CMSG_SEND_LUCKY_RED_PACK_RETURN                       0x051D6804    400B
  CMSG_SEND_LUCKY_RED_PACK_SET_FLAG                     0x051D8F04     72B
  CMSG_SEND_MERGE_GAME_GIFT_RETURN                      0x052477C0    136B
  CMSG_SERVER_MAINTAIN                                  0x0527CDB0     56B
  CMSG_SERVER_MISSION_INFO                              0x0524E3D4   1156B
  CMSG_SERVER_MISSION_INFO_REQUEST                      0x0524EB68     56B
  CMSG_SERVER_MISSION_RECEIVE_REQUEST                   0x0524EC88     72B
  CMSG_SERVER_MISSION_RECEIVE_RETURN                    0x0524EE24    104B
  CMSG_SERVER_MISSION_UPDATE                            0x0524EA20    136B
  CMSG_SERVER_MISSION_VIEW_REQUEST                      0x0524EF74     72B
  CMSG_SERVER_MISSION_VIEW_RETURN                       0x0524F520   1484B
  CMSG_SERVER_PLAYER_COUNT_REQUEST                      0x0528BC3C    152B
  CMSG_SERVER_PLAYER_COUNT_RETURN                       0x0528BDBC     72B
  CMSG_SESAME_BUSINESS_BUY_REQUEST                      0x05268884    136B
  CMSG_SESAME_BUSINESS_BUY_RETURN                       0x05268AD0    136B
  CMSG_SESAME_SHOP_BUY_REQUEST                          0x05267AE0     88B
  CMSG_SESAME_SHOP_BUY_RETURN                           0x05267C58     88B
  CMSG_SET_CHAT_HONOR_REQUEST                           0x050B7ABC     72B
  CMSG_SET_CHAT_HONOR_RETURN                            0x050B7BEC     72B
  CMSG_SET_CLANPK_ATTACK_AMRY_INFO                      0x050025C4    492B
  CMSG_SET_CLANPK_DEFEND_AMRY_INFO                      0x04FFEC04    836B
  CMSG_SET_CLANPK_DEFEND_AMRY_INFO_RESULT               0x04FFFB00   3200B
  CMSG_SET_DOMINION_OFFICIAL                            0x05046300    104B
  CMSG_SET_DOMINION_OFFICIAL_RESULT                     0x0504652C    136B
  CMSG_SET_EQUIP_SHOW                                   0x052DA1F0     72B
  CMSG_SET_RECRUIT_ARMY_FLAG                            0x0505C4C0     72B
  CMSG_SIGNATURE_UPDATE                                 0x04FBC128    324B
  CMSG_SIGN_REQUEST                                     0x052C38E0     56B
  CMSG_SIGN_REWARD_SUCCESS                              0x052C3AF8     72B
  CMSG_SOLDIER_CHANGE_LEVEL                             0x052CA724    216B
  CMSG_SOLDIER_CURE_OVER_REQUEST                        0x052C9DC8     56B
  CMSG_SOLDIER_CURE_OVER_RETURN                         0x052CA120    824B
  CMSG_SOLDIER_GOLD_CURE_REQUEST                        0x052C909C    456B
  CMSG_SOLDIER_GOLD_PRODUCE_REQUEST                     0x052C7054     88B
  CMSG_SOLDIER_GOLD_SPEED_CURE_REQUEST                  0x052C9324     56B
  CMSG_SOLDIER_GOLD_SPEED_PRODUCE_REQUEST               0x052C7194     72B
  CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_REQUEST           0x052C9970    612B
  CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURN            0x052C9CC0     72B
  CMSG_SOLDIER_ITEM_SPEED_CURE_REQUEST                  0x052C947C     88B
  CMSG_SOLDIER_ITEM_SPEED_CURE_RETURN                   0x052C95C0     72B
  CMSG_SOLDIER_ITEM_SPEED_PRODUCE_ONEKEY_REQUEST        0x052C78B8    628B
  CMSG_SOLDIER_ITEM_SPEED_PRODUCE_ONEKEY_RETURN         0x052C7C48     88B
  CMSG_SOLDIER_ITEM_SPEED_PRODUCE_REQUEST               0x052C7330    104B
  CMSG_SOLDIER_ITEM_SPEED_PRODUCE_RETURN                0x052C74B4     88B
  CMSG_SOLDIER_NORMAL_CURE_REQUEST                      0x052C8464    916B
  CMSG_SOLDIER_NORMAL_CURE_RETURN                       0x052C8B58    868B
  CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST                   0x052C66D4    104B
  CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW               0x052C6AE4    656B
  CMSG_SOLDIER_NORMAL_PRODUCE_RETURN                    0x052C6ECC    104B
  CMSG_SOLDIER_PRODUCE_OVER_REQUEST                     0x052C7E38    388B
  CMSG_SOLDIER_PRODUCE_OVER_RETURN                      0x052C80D8     88B
  CMSG_SOLDIER_UP_BREAK_LEVEL_REQUEST                   0x052CD258    168B
  CMSG_SOLDIER_UP_BREAK_LEVEL_RETURN                    0x052CD48C    120B
  CMSG_SOLDIER_UP_GET_LEVEL_REWARD_REQUEST              0x052CD7DC    184B
  CMSG_SOLDIER_UP_GET_LEVEL_REWARD_RETURN               0x052CD9B4     88B
  CMSG_SOLDIER_UP_REQUEST                               0x052CCA28    184B
  CMSG_SOLDIER_UP_RETURN                                0x052CCD98    524B
  CMSG_SOLDIER_UP_SET_TALENT_REQUEST                    0x052CE2E4    572B
  CMSG_SOLDIER_UP_SET_TALENT_RETURN                     0x052CE72C    480B
  CMSG_SOLDIER_UP_UNLOCK_TALENT_REQUEST                 0x052CDCE4    184B
  CMSG_SOLDIER_UP_UNLOCK_TALENT_RETURN                  0x052CDEBC     88B
  CMSG_SOLOMON_ANWSER_QUESTIONS_REQUEST                 0x052CFE68     72B
  CMSG_SOLOMON_ANWSER_QUESTIONS_RETURN                  0x052D00D8    548B
  CMSG_SOLOMON_CHOOSE_REWARD_REQUEST                    0x052CFB6C     88B
  CMSG_SOLOMON_CHOOSE_REWARD_RETURN                     0x052CFD18    104B
  CMSG_SOLOMON_INFO_REQUEST                             0x052D03E4     72B
  CMSG_SOLOMON_NS_ANWSER_QUESTIONS_REQUEST              0x052D0D74     72B
  CMSG_SOLOMON_NS_ANWSER_QUESTIONS_RETURN               0x052D0FE4    548B
  CMSG_SOLOMON_NS_CHOOSE_REWARD_REQUEST                 0x052D0A78     88B
  CMSG_SOLOMON_NS_CHOOSE_REWARD_RETURN                  0x052D0C24    104B
  CMSG_SOLOMON_NS_ROLL_DICE_REQUEST                     0x052D0514     72B
  CMSG_SOLOMON_NS_ROLL_DICE_RETURN                      0x052D0754    516B
  CMSG_SOLOMON_ROLL_DICE_REQUEST                        0x052CF608     72B
  CMSG_SOLOMON_ROLL_DICE_RETURN                         0x052CF848    516B
  CMSG_SOUL_SMELT_REQUEST                               0x0505E794    504B
  CMSG_SOUL_SMELT_SET_DROP_REQUEST                      0x0505E590     72B
  CMSG_SPECIAL_EVENT_DROP                               0x052D1864    504B
  CMSG_SPECIAL_EVENT_DROP_LIMIT_REQUEST                 0x052D7CF8    168B
  CMSG_SPECIAL_EVENT_DROP_LIMIT_RETURN                  0x052D82A0   2376B
  CMSG_START_BUILDUP                                    0x0510734C    652B
  CMSG_START_BUILDUP_NEW                                0x05107AB8    824B
  CMSG_START_DEFEND                                     0x05108018    520B
  CMSG_START_DEFEND_NEW                                 0x05108590    616B
  CMSG_START_LOOK_OTHER_SERVER                          0x05213C24    104B
  CMSG_START_MARCH                                      0x05211FE4    644B
  CMSG_START_MARCH_EX                                   0x05212CC4    476B
  CMSG_START_MARCH_NEW                                  0x05212778    848B
  CMSG_START_TRADE_MARCH_REQUEST                        0x0504B964     88B
  CMSG_START_TRADE_MARCH_RETURN                         0x0504BAE0     88B
  CMSG_STATION_SYNC                                     0x051F28B0   1604B
  CMSG_STATUS_EXTRA_INFO                                0x052D5D88    688B
  CMSG_STATUS_INFO                                      0x052D5798    772B
  CMSG_STATUS_TIP                                       0x052D5B84     72B
  CMSG_SUPERCHAMPIONSHIP_ACTION_REQUEST                 0x052D717C     72B
  CMSG_SUPERCHAMPIONSHIP_ACTION_RETURN                  0x052D74B0    540B
  CMSG_SUPERCHAMPIONSHIP_DONATE_REQUEST                 0x052D693C    104B
  CMSG_SUPERCHAMPIONSHIP_DONATE_RETURN                  0x052D6B98    152B
  CMSG_SUPERCHAMPIONSHIP_GOLD_UNLOCK_REQUEST            0x052D6E90     72B
  CMSG_SUPERCHAMPIONSHIP_GOLD_UNLOCK_RETURN             0x052D702C    104B
  CMSG_SUPERCHAMPIONSHIP_REWARD_REQUEST                 0x052D6580    104B
  CMSG_SUPERCHAMPIONSHIP_REWARD_RETURN                  0x052D6770    120B
  CMSG_SUPERCHAMPIONSHIP_SHOWACTION_REQUEST             0x052D77B4     72B
  CMSG_SUPERCHAMPIONSHIP_SHOWACTION_RETURN              0x052D79BC    136B
  CMSG_SUPERCHOOSEONE_GIFT_BUY_TIME                     0x052D9634     56B
  CMSG_SYNC_ACTION_EXCHAGE_INFO                         0x04F9E330    632B
  CMSG_SYNC_ACTIVEGIFTS_CONFIG                          0x04FA03D4    440B
  CMSG_SYNC_ACTIVEGIFTS_TASK                            0x04FA1BA4    136B
  CMSG_SYNC_ACTIVITY_RUSH_EVENT                         0x04FA2340    444B
  CMSG_SYNC_ACTIVITY_RUSH_EVENT_CONFIG                  0x04FA2800   1320B
  CMSG_SYNC_ALLFORONE_INFO                              0x04FAA90C   1992B
  CMSG_SYNC_ALL_DOMINION_BATTLE                         0x051FFFD8   1608B
  CMSG_SYNC_ALL_DOMINION_BATTLE_COUNT                   0x05049698     88B
  CMSG_SYNC_ALL_DOMINION_BUILD                          0x050489D0    760B
  CMSG_SYNC_ALL_DOMINION_OCCUPY                         0x05200AAC    952B
  CMSG_SYNC_ALL_KING_CHESS_BATTLE_COUNT                 0x050C8B70     72B
  CMSG_SYNC_ALL_LEAGUEBUILD_BATTLE_COUNT                0x0515A878     72B
  CMSG_SYNC_AMRY_SKIN_INFO                              0x04FAC54C    416B
  CMSG_SYNC_ANNIVERSARY_DONATE_INFO                     0x0527ADB0    168B
  CMSG_SYNC_ARENA_INFO                                  0x04FAD538    228B
  CMSG_SYNC_AUCTION_INFO                                0x04FBD784    636B
  CMSG_SYNC_AUCTION_RECORD                              0x04FBEAC0    476B
  CMSG_SYNC_AUCTION_TOTAL_VALUE                         0x04FBE838     72B
  CMSG_SYNC_AUTO_HANDUP                                 0x04FC0D28    928B
  CMSG_SYNC_AUTO_JOIN_BUILDUP_INFO                      0x04FC1C54    920B
  CMSG_SYNC_BATTLE_INFO                                 0x05214854    136B
  CMSG_SYNC_BUILDING_SKIN_INFO                          0x04FCF864   1376B
  CMSG_SYNC_BUILDUP_BATTLE_ATK_TIME                     0x05213F28     88B
  CMSG_SYNC_BUYONESHOP_GIFTID                           0x04FD0090    304B
  CMSG_SYNC_CHAMPIONSHIP_BANNER_ID                      0x04FD557C    380B
  CMSG_SYNC_CHAMPIONSHIP_BOX_ID                         0x04FD5268    380B
  CMSG_SYNC_CHAMPIONSHIP_CONFIG                         0x04FD337C    168B
  CMSG_SYNC_CHAMPIONSHIP_GIFT_ID                        0x04FD5088     72B
  CMSG_SYNC_CLANPK_ATTACK_INFO                          0x04FFDB6C   3152B
  CMSG_SYNC_CLANPK_CONFIG                               0x04FE5A5C    604B
  CMSG_SYNC_CLANPK_DEFEND_INFO                          0x04FFC09C   3200B
  CMSG_SYNC_CLANPK_FINAL_DETAIL_INFO                    0x04FF7B04   2040B
  CMSG_SYNC_CLANPK_INFO                                 0x04FE789C   7740B
  CMSG_SYNC_COMMON_ACTION_TIME_CONFIG                   0x0500E0C0    492B
  CMSG_SYNC_COMMON_EXCHAGE_ACTIVITY_INFO                0x0500E580    796B
  CMSG_SYNC_CONTINUITY_GIFTPACK_ACTION                  0x0500F650    440B
  CMSG_SYNC_CONTINUITY_GIFTPACK_BUY                     0x0500FD14    120B
  CMSG_SYNC_CONTINUOUS_TASK_ACTION                      0x05010BA0    440B
  CMSG_SYNC_CONTINUOUS_TASK_BUY                         0x0501165C     88B
  CMSG_SYNC_CUMULATIVE_RECHARGE_INFO                    0x05012D74    616B
  CMSG_SYNC_CUSTOMGIFTS_CONFIG                          0x05013548    440B
  CMSG_SYNC_CUSTOMGIFTS_GIFT                            0x05014AA0     88B
  CMSG_SYNC_CUSTOM_HEAD_INFO                            0x05014FE4    740B
  CMSG_SYNC_CYCLE_ACTION                                0x05018F4C   3384B
  CMSG_SYNC_CYCLE_ACTION_ID                             0x0501A3C8   4512B
  CMSG_SYNC_DAILYCONSUME_CONFIG                         0x05022CEC    440B
  CMSG_SYNC_DAILYCONSUME_GOLD_CONSUME                   0x05023834     88B
  CMSG_SYNC_DAILY_GET_ITEM_TIMES                        0x05320AFC    460B
  CMSG_SYNC_DAILY_MARKET_SUPPROT                        0x0523D73C     72B
  CMSG_SYNC_DAILY_RECHARGE_INFO                         0x05024028   2840B
  CMSG_SYNC_DAMAGE_INFO                                 0x050269B8   5604B
  CMSG_SYNC_DEFEND_HERO_INFO                            0x051F5FF8   2288B
  CMSG_SYNC_DEFEND_HERO_INFO_NEW                        0x05204650   2736B
  CMSG_SYNC_DEFEND_HERO_NUM                             0x051396C8     72B
  CMSG_SYNC_DEFEND_INFO                                 0x05109B60   3096B
  CMSG_SYNC_DEFEND_INFO_KING_CHESS                      0x050C9B64    500B
  CMSG_SYNC_DEFEND_VERSION                              0x05056BC0     72B
  CMSG_SYNC_DESSERT_ACTION_QUEST_INFO                   0x0503A2B8    136B
  CMSG_SYNC_DOMINION_DEFEND_INFO                        0x051FF09C   2272B
  CMSG_SYNC_DOMINION_DEFEND_INFO_NEW                    0x052102AC   2368B
  CMSG_SYNC_DOMINION_DEFEND_VERSION                     0x05056D24     88B
  CMSG_SYNC_DOMINION_DETAIL_INFO                        0x051FDA60   3464B
  CMSG_SYNC_DOMINION_DETAIL_INFO_NEW                    0x0520EBA0   3592B
  CMSG_SYNC_DOMINION_INFO                               0x050451CC   1388B
  CMSG_SYNC_DOMINION_OCCUPY_VERSION                     0x05056E64     72B
  CMSG_SYNC_DOMINION_OFFICIAL_INFO                      0x05046C8C   2076B
  CMSG_SYNC_DOMINION_SIMPLE_BATTLE_INFO                 0x0504769C    152B
  CMSG_SYNC_EXTRA_GIFTPACK                              0x05061E7C     72B
  CMSG_SYNC_EXTRA_GIFTPACK_ACTION                       0x05060F58    440B
  CMSG_SYNC_EXTRA_GIFTPACK_ACTION_NEW                   0x05062328    440B
  CMSG_SYNC_EXTRA_GIFTPACK_NEW                          0x050638A4     88B
  CMSG_SYNC_EXTRA_GIFTPACK_TASK                         0x0506208C    136B
  CMSG_SYNC_EXTRA_GIFTPACK_TASK_NEW                     0x05063AFC    152B
  CMSG_SYNC_FIXED_TIME                                  0x0505FC3C     88B
  CMSG_SYNC_FORCE_INFO_REQUEST                          0x052FDDF0     72B
  CMSG_SYNC_FORCE_INFO_RETURN                           0x052FDF58     88B
  CMSG_SYNC_FORCE_POWER_INFO_REQUEST                    0x052FE0D4     88B
  CMSG_SYNC_FORCE_POWER_INFO_RETURN                     0x052FE5EC   1016B
  CMSG_SYNC_FORTRESS_ACTION                             0x0506CB28    232B
  CMSG_SYNC_FRIEND                                      0x0507FEFC    504B
  CMSG_SYNC_FRIEND_ADD                                  0x05080290    432B
  CMSG_SYNC_FRIEND_APPLY_COUNT                          0x0507D3AC     72B
  CMSG_SYNC_FRIEND_DEL                                  0x050805DC    432B
  CMSG_SYNC_FTRIEND_GIFT_CONFIG                         0x05093B00    508B
  CMSG_SYNC_FULL_RECHARGE_INFO                          0x05087F44    120B
  CMSG_SYNC_GENERAL_ACTIBITIES_INFO                     0x050892D8    488B
  CMSG_SYNC_GIANT_INVASION_INFO                         0x0508C62C    776B
  CMSG_SYNC_GOLD_GIFT_ACTION_INFO                       0x0509337C    480B
  CMSG_SYNC_GOODLUCK_CARD                               0x0509A88C   1056B
  CMSG_SYNC_GOODLUCK_CONFIG                             0x05099024    508B
  CMSG_SYNC_GROUP_CHAT_ADD_MEMBER                       0x050A1ED4   1084B
  CMSG_SYNC_GROUP_CHAT_DEL_MEMBER                       0x050A26A0   1084B
  CMSG_SYNC_GROUP_CHAT_EXIT_GROUP                       0x050A2D9C    764B
  CMSG_SYNC_GROUP_CHAT_INFO                             0x050A3A64   1404B
  CMSG_SYNC_GROUP_CHAT_LEAVE_SERVER                     0x050A3358    764B
  CMSG_SYNC_GROUP_CHAT_MEMBER_BE_ADD                    0x050A432C    844B
  CMSG_SYNC_GROUP_CHAT_MEMBER_BE_DEL                    0x050A4948    724B
  CMSG_SYNC_GUILD_STANDOFF_INFO                         0x050A53E8    184B
  CMSG_SYNC_HERO_LEGEND_INFO                            0x050B6DE8   1472B
  CMSG_SYNC_HONOR                                       0x050B7848    396B
  CMSG_SYNC_ITEM_RECOVERY_TIME                          0x050C2508    464B
  CMSG_SYNC_KINGDOM_ACTION                              0x050DCE50    660B
  CMSG_SYNC_KINGDOM_ACTION_CONFIG                       0x050DC920    168B
  CMSG_SYNC_KINGDOM_GIFT_CONFIG                         0x050E2C8C   1660B
  CMSG_SYNC_KINGDOM_GIFT_DATA                           0x050E35F4    620B
  CMSG_SYNC_KINGDOM_GIFT_LEVEL                          0x050E3FD4    624B
  CMSG_SYNC_KINGDOM_GIFT_REWARD                         0x050E4470    168B
  CMSG_SYNC_KINGDOM_STRATEGY_COIN                       0x050E652C     72B
  CMSG_SYNC_KINGDOM_STRATEGY_INFO                       0x050E54C0    104B
  CMSG_SYNC_KINGDOM_STRATEGY_NEW_INFO                   0x050E5740    536B
  CMSG_SYNC_KING_CHESS_ACTION                           0x050C4470    216B
  CMSG_SYNC_KING_CHESS_DEFEND_INFO                      0x050CA7DC   2376B
  CMSG_SYNC_KING_CHESS_DEFEND_VERSION                   0x050C8A2C     88B
  CMSG_SYNC_KING_CHESS_DETAIL_INFO                      0x050CBDF4   2884B
  CMSG_SYNC_KING_CHESS_SIMPLE_BATTLE_INFO               0x050CCC60    152B
  CMSG_SYNC_KING_INFO                                   0x0503E600     72B
  CMSG_SYNC_KING_ROAD_ONE_QUEST_INFO                    0x050DC674    104B
  CMSG_SYNC_KING_ROAD_QUEST_INFO                        0x050DBEA8   1044B
  CMSG_SYNC_KNIGHT_ACTION_CONFIG                        0x050E934C    152B
  CMSG_SYNC_KNIGHT_GLORY_INFO                           0x050EA6A0    344B
  CMSG_SYNC_KNIGHT_GLORY_LEAGUE_REQUEST                 0x050EAB98    152B
  CMSG_SYNC_KNIGHT_GLORY_LEAGUE_RETURN                  0x050EAE28    152B
  CMSG_SYNC_LAND_BATTLE                                 0x0510BF3C    600B
  CMSG_SYNC_LATCH_INFO                                  0x050F08D4    648B
  CMSG_SYNC_LEAGUEBUILD_DEFEND_INFO                     0x0515C988   2112B
  CMSG_SYNC_LEAGUEPASS_ACTION                           0x0516B0C4    152B
  CMSG_SYNC_LEAGUEPASS_ADVANCEDGIFT                     0x0516F188     72B
  CMSG_SYNC_LEAGUEPASS_TASK_REFRESH                     0x0516EC2C    608B
  CMSG_SYNC_LEAGUEPASS_UPDATE_MY_TASK                   0x0516F1D0    608B
  CMSG_SYNC_LEAGUE_BATTLEFIELD_ACTION                   0x0511286C    216B
  CMSG_SYNC_LEAGUE_BATTLEFIELD_CONFIG                   0x05114428    828B
  CMSG_SYNC_LEAGUE_BATTLE_COUNT                         0x051391B8   1064B
  CMSG_SYNC_LEAGUE_BATTLE_INFO                          0x051F7EC8   5728B
  CMSG_SYNC_LEAGUE_BATTLE_INFO_NEW                      0x052077DC  10804B
  CMSG_SYNC_LEAGUE_BATTLE_RECORD                        0x05103AD8   1056B
  CMSG_SYNC_LEAGUE_BIG_BOSS_CONFIG                      0x05152748    232B
  CMSG_SYNC_LEAGUE_BIG_BOSS_INFO                        0x05154420    168B
  CMSG_SYNC_LEAGUE_BIG_BOSS_REWARD_TIMES                0x051545B0     72B
  CMSG_SYNC_LEAGUE_BOSS_ACTION_CONFIG                   0x0515522C     88B
  CMSG_SYNC_LEAGUE_CARD                                 0x05168B58     88B
  CMSG_SYNC_LEAGUE_CARD_EXCHANGE_COUNT                  0x05168C98     72B
  CMSG_SYNC_LEAGUE_DONATE_CRIT                          0x05048DB0     72B
  CMSG_SYNC_LEAGUE_DONATE_INFO_NEW                      0x05178F00     88B
  CMSG_SYNC_LEAGUE_HALF_BATTLE_INFO                     0x051FB174   7252B
  CMSG_SYNC_LEAGUE_HALF_BATTLE_INFO_NEW                 0x0520C010   7820B
  CMSG_SYNC_LEAGUE_HELP                                 0x05166A34    956B
  CMSG_SYNC_LEAGUE_HELP_COUNT                           0x05167BB8    136B
  CMSG_SYNC_LEAGUE_HELP_COUNT_EX                        0x051665C8     72B
  CMSG_SYNC_LEAGUE_HELP_FLAG                            0x0516854C    824B
  CMSG_SYNC_LEAGUE_HELP_REWARD_COUNT                    0x05114084     72B
  CMSG_SYNC_LEAGUE_INVITE                               0x050FC300   2176B
  CMSG_SYNC_LEAGUE_KING_CHESS_ADD                       0x050C92AC    120B
  CMSG_SYNC_LEAGUE_KING_CHESS_DEL                       0x050C8F24    512B
  CMSG_SYNC_LEAGUE_MEMBER                               0x050FA8EC    916B
  CMSG_SYNC_LEAGUE_MEMBER_NEW                           0x050F9FC0    940B
  CMSG_SYNC_LEAGUE_NUMBER_VALUE                         0x050FD28C     88B
  CMSG_SYNC_LEAGUE_RECHARGE_CONFIG                      0x05177004    748B
  CMSG_SYNC_LEAGUE_RECHARGE_POINT                       0x05177F68     88B
  CMSG_SYNC_LEAGUE_STRING_VALUE                         0x050FD4A4    324B
  CMSG_SYNC_LEAGUE_TSAK_INFO                            0x050F8AA8    664B
  CMSG_SYNC_LORD_EQUIP_GEM_LEVEL_INFO                   0x05199168   1324B
  CMSG_SYNC_LORD_GROW_GIFT_INFO                         0x0519B4D8     72B
  CMSG_SYNC_LORD_GROW_INFO                              0x0519B0F8    760B
  CMSG_SYNC_LORD_LIKE_INFO                              0x0528B23C    416B
  CMSG_SYNC_LOSTLAND_ACTION_CONFIG                      0x051A72D0    232B
  CMSG_SYNC_LOSTLAND_MONTH_CARD_INFO                    0x051A6A80     88B
  CMSG_SYNC_LOSTLAND_RUSH_EVENT                         0x04FA4564    444B
  CMSG_SYNC_LOSTLAND_SHOP_BUY_TIMES                     0x051AFC7C    460B
  CMSG_SYNC_LOST_KING_ROAD_ONE_QUEST_INFO               0x051A68E4    104B
  CMSG_SYNC_LOST_KING_ROAD_QUEST_INFO                   0x051A61C4    880B
  CMSG_SYNC_LUCKYPOT_CONFIG                             0x051D3150    440B
  CMSG_SYNC_LUCKYPOT_ITEMCOUNT                          0x051D4984     88B
  CMSG_SYNC_LUCKY_LINE_INFO                             0x051D2278    612B
  CMSG_SYNC_LUCKY_SHOP_FLAG                             0x051DE740     72B
  CMSG_SYNC_LUCKY_SHOP_INFO                             0x051DE4C8    152B
  CMSG_SYNC_LUCKY_TURNTABLE_INFO                        0x051DE9F8    184B
  CMSG_SYNC_LUNA_SHOP_CONFIG                            0x051DFEA8    792B
  CMSG_SYNC_MARBLES_CURRENT_VALUE                       0x0523CF04     72B
  CMSG_SYNC_MARBLES_EMISSION_REQUEST                    0x0523C13C    184B
  CMSG_SYNC_MARBLES_EMISSION_RETURN                     0x0523C34C    104B
  CMSG_SYNC_MARBLES_GENERATE_TRACK_MULTIPLE_REQUEST     0x0523CA54    152B
  CMSG_SYNC_MARBLES_GENERATE_TRACK_MULTIPLE_RETURN      0x0523CC84    404B
  CMSG_SYNC_MARBLES_INFO                                0x0523BB00    876B
  CMSG_SYNC_MARBLES_RECEIVE_REWARD_REQUEST              0x0523C620    152B
  CMSG_SYNC_MARBLES_RECEIVE_REWARD_RETURN               0x0523C7A0     72B
  CMSG_SYNC_MARCH                                       0x051E9CA8   4436B
  CMSG_SYNC_MARCH_ARMY_INFO                             0x052011D8    644B
  CMSG_SYNC_MARCH_ARMY_INFO_NEW                         0x05211010    748B
  CMSG_SYNC_MARCH_NEW                                   0x052028BC   4948B
  CMSG_SYNC_MERGE_EVNET_ACTION                          0x052431F8    544B
  CMSG_SYNC_MERGE_EVNET_ACTION_CONFIG                   0x05242F6C    120B
  CMSG_SYNC_MERGE_GAME_CHARGE_TYPE                      0x05244B98     72B
  CMSG_SYNC_MERGE_GAME_ENERGY_INFO                      0x05246FD8     88B
  CMSG_SYNC_MERGE_GAME_INFO                             0x0524404C   2660B
  CMSG_SYNC_MERGE_SERVER_ACTION_CONFIG                  0x052D1E84   1684B
  CMSG_SYNC_MINI_GAME_CONFIG                            0x0524BC2C    340B
  CMSG_SYNC_MINI_GAME_INFO                              0x0524C390    836B
  CMSG_SYNC_MINI_GAME_REWARD_TIMES                      0x0524C7F4     88B
  CMSG_SYNC_MOBILIZATION_ACTION                         0x0524FDE0    152B
  CMSG_SYNC_MOBILIZATION_MY_TASK                        0x052530F4    136B
  CMSG_SYNC_MOBILIZATION_TASK_DELETE                    0x05252DE0     88B
  CMSG_SYNC_MOBILIZATION_TASK_REFRESH                   0x05252F20     72B
  CMSG_SYNC_MOBILIZATION_UPDATE_MY_TASK                 0x05253298     88B
  CMSG_SYNC_NAMEPLATE_INFO                              0x05279F0C    376B
  CMSG_SYNC_NAME_INFO                                   0x05214360    516B
  CMSG_SYNC_NEWSERVER_ACTION                            0x05258418   5344B
  CMSG_SYNC_NEWSERVER_LIMITSHOP                         0x0525ACD8   1408B
  CMSG_SYNC_NEWSERVER_RECORDCOST                        0x05259D3C   2244B
  CMSG_SYNC_NEWSERVER_SIGNINFUND                        0x0525BD54    664B
  CMSG_SYNC_NOVICE_FREE_PURCHASE_INFO                   0x0525F0F0    588B
  CMSG_SYNC_OPEN_SESAME_HP                              0x0526837C    836B
  CMSG_SYNC_OPERATION_ACTION                            0x0526C99C   1048B
  CMSG_SYNC_OPERATION_ACTION_CONFIG                     0x0526D054    696B
  CMSG_SYNC_OTHER_LEAGUE_INFO                           0x05100E08   2184B
  CMSG_SYNC_OTHER_LEAGUE_MEMBER                         0x05101D40   1420B
  CMSG_SYNC_OWNER_BUILDUP                               0x0510AC50   1520B
  CMSG_SYNC_OWNER_DOMINION_ID                           0x050498C0    452B
  CMSG_SYNC_OWNER_LEAGUE_HELP                           0x0516733C    956B
  CMSG_SYNC_OWNER_LEAGUE_INFO                           0x050FDEA0   1836B
  CMSG_SYNC_PET_INFO                                    0x05274D54   1516B
  CMSG_SYNC_PLOT_QUEST_INFO                             0x0527E510    436B
  CMSG_SYNC_PLOT_QUEST_INFO_NEW                         0x0527EE70    436B
  CMSG_SYNC_POST_TASK_INFO                              0x0527FE58   1676B
  CMSG_SYNC_RECHARGEBONUS_CONFIG                        0x05295AC0    440B
  CMSG_SYNC_RECHARGEBONUS_TIMES                         0x05296100    104B
  CMSG_SYNC_RED_PAPER_DEL_ROOM                          0x052A23A0     72B
  CMSG_SYNC_RED_PAPER_INFO                              0x05296DA8   1716B
  CMSG_SYNC_RED_PAPER_SHOP_BUY_TIMES                    0x052A1A80    460B
  CMSG_SYNC_RED_PAPER_VIEW_NUM                          0x052A2260     88B
  CMSG_SYNC_REMOVE_MARCH                                0x051EAF1C     88B
  CMSG_SYNC_RETURN_EVNET_ACTION                         0x052AEE9C    136B
  CMSG_SYNC_RETURN_EVNET_ACTION_NEW                     0x052AF7F8    168B
  CMSG_SYNC_REWARD_TASK_BEGIN                           0x051753AC     88B
  CMSG_SYNC_REWARD_TASK_DELETE                          0x05175890     88B
  CMSG_SYNC_REWARD_TASK_DELETE_HERO                     0x05176254    456B
  CMSG_SYNC_REWARD_TASK_END                             0x051754EC     72B
  CMSG_SYNC_REWARD_TASK_HEROS                           0x051750C0    464B
  CMSG_SYNC_REWARD_TASK_JOIN                            0x05175CD4    888B
  CMSG_SYNC_REWARD_TASK_REFRESH                         0x051756EC    136B
  CMSG_SYNC_RUSH_ACTION                                 0x052B2328   1320B
  CMSG_SYNC_RUSH_ACTION_CONFIG                          0x052B2B54   1320B
  CMSG_SYNC_SECRET_TASKS                                0x052B978C   2488B
  CMSG_SYNC_SERVER_INFO_LIST                            0x052D9CB0   1112B
  CMSG_SYNC_SESAME_SHOP_BUY_TIMES                       0x05267E90    460B
  CMSG_SYNC_SKIN_INFO                                   0x052C55B4    376B
  CMSG_SYNC_SOLDIER_UP_INFO                             0x052CB96C   3556B
  CMSG_SYNC_SOLOMON_INFO                                0x052CF468    184B
  CMSG_SYNC_SUBSCRIPTION_INFO                           0x05092B58    548B
  CMSG_SYNC_SUPERCHAMPIONSHIP_CONFIG                    0x052D6274    440B
  CMSG_SYNC_SUPERCHAMPIONSHIP_GIFT_ID                   0x052D6D50     88B
  CMSG_SYNC_SUPERCHOOSEONE_INFO                         0x052D914C   1064B
  CMSG_SYNC_TEAM_RECHARGE_INFO                          0x052DB8EC   1188B
  CMSG_SYNC_THREEDAYS_CONFIG                            0x052E0A28    440B
  CMSG_SYNC_THREEDAYS_DATA                              0x052E0F3C    704B
  CMSG_SYNC_THREEDAYS_REWARD                            0x052E191C    200B
  CMSG_SYNC_TRADE_MARCH                                 0x05051434   1460B
  CMSG_SYNC_TREASURE_CARD_QUEST_INFO                    0x052E4158    716B
  CMSG_SYNC_TRIGGER_GIFT_INFO                           0x052E59E0    668B
  CMSG_SYNC_VEC_EXTRAATTR                               0x0505BB64    492B
  CMSG_SYNC_WAR_CARD_INFO                               0x05092F5C    468B
  CMSG_SYNC_WAR_LORD_ACTION                             0x052E7230    636B
  CMSG_SYNC_WAR_LORD_ACTION_ID                          0x052E6A98    812B
  CMSG_SYNC_WEEKLY_SPECIAL_GIFT_INFO                    0x05090A58     88B
  CMSG_SYNC_WHEEL_INFO                                  0x052F1E98   1376B
  CMSG_SYNC_WORLD_BATTLE_ACTION_CONFIG                  0x052F670C    248B
  CMSG_SYNC_YAHTZEE_GAME_CONFIG                         0x0531E16C    940B
  CMSG_SYNC_lEAGUE_BUILD_DESTORY_INFO                   0x0515D85C    136B
  CMSG_SYN_ALL_COMPLETE_GUIDE                           0x0505F6CC    432B
  CMSG_SYN_ALL_QUEST                                    0x05285380   1132B
  CMSG_SYN_ALL_QUEST_CHAMPIONSHIP                       0x04FD3A54   1512B
  CMSG_SYN_ATTRIBUTE_CHANGE                             0x04FB8C10    104B
  CMSG_SYN_CITYDEFENSE_FIRE                             0x0505C028     72B
  CMSG_SYN_CLOSE_PUSH                                   0x052844B8    408B
  CMSG_SYN_DAILY_TASKS                                  0x05025488    540B
  CMSG_SYN_EXTRA_ATTRIBUTE_CHANGE                       0x0505D7E0     88B
  CMSG_SYN_EXTRA_ATTRIBUTE_CHANGE7getDataEPKc           0x1B00000023A8 221130686201856B
  CMSG_SYN_FIGHT_RECORD                                 0x050657D8   1284B
  CMSG_SYN_ITEM_SHOP_BUY_INFO                           0x050C38B4    492B
  CMSG_SYN_ITEM_SHOP_INFO                               0x050C2B80    884B
  CMSG_SYN_ITEM_SHOP_WEEK_BUY_INFO                      0x050C3C5C    492B
  CMSG_SYN_LEAGUE_DONATE_REWARD_INFO                    0x05179320     88B
  CMSG_SYN_MONTH_CARD_INFO                              0x050C3348     88B
  CMSG_SYN_MYSELF_EXTRA_ATTRIBUTE                       0x05057F1C   1164B
  CMSG_SYN_OTHER_EXTRA_ATTRIBUTE                        0x050595AC   3944B
  CMSG_SYN_OTHER_NAME                                   0x0505A854    324B
  CMSG_SYN_REBUILDING_OASISE_TASKS                      0x05294AC0    720B
  CMSG_SYN_SERVER_TIME                                  0x0527CC98     88B
  CMSG_SYN_SIGN_CONFIG                                  0x052C3234    788B
  CMSG_SYN_SIGN_INFO                                    0x052C3778    168B
  CMSG_SYN_UPGRADE_REWARD                               0x0505C190     88B
  CMSG_SYN_VERSION_CONTROL                              0x04FBB258    488B
  CMSG_SYSTEM_MESSAGE                                   0x052DA9E8    324B
  CMSG_SYS_ACCUMULATION_GOLD_CONSUMPTION                0x04F9CE70     72B
  CMSG_SYS_ACCUMULATION_NEW_GOLD_CONSUMPTION            0x04F9CFA4     72B
  CMSG_SYS_CAMEL_SHOP_INFO                              0x04FD1D20   1076B
  CMSG_SYS_FORTRESS_INFO                                0x05068688     72B
  CMSG_SYS_LEAGUE_BATTLEFIELD_INFO                      0x0510FADC   1504B
  CMSG_SYS_LEAGUE_GIFT_BINARY                           0x05166274    508B
  CMSG_SYS_LEAGUE_GIFT_INFO                             0x05165318    856B
  CMSG_SYS_LOSTLAND_INFO                                0x051A7BA0   2392B
  CMSG_SYS_LOSTLAND_WEEK_BAN_HERO                       0x051A8690    376B
  CMSG_SYS_LUCKY_GIFT_DETAILED_INFO                     0x051D0950   1276B
  CMSG_SYS_LUCKY_RED_PACK_DETAILED_INFO                 0x051D7DB0   1940B
  CMSG_SYS_MERGE_GAME_GIFT_DETAILED_INFO                0x05248444   1068B
  CMSG_SYS_SECRET_INFO                                  0x052B5F24   1100B
  CMSG_SYS_SOLDIER_INFO                                 0x052C5DFC   1924B
  CMSG_SYS_TRIBUTE_INFO                                 0x052E50B4    120B
  CMSG_TEAM_RECHARGE_ADD_INVITE_ID                      0x052DE524     72B
  CMSG_TEAM_RECHARGE_BUY_ITEM_REQUEST                   0x052DF800    152B
  CMSG_TEAM_RECHARGE_BUY_ITEM_RETURN                    0x052DF980     72B
  CMSG_TEAM_RECHARGE_CREATE_REQUEST                     0x052DC03C    168B
  CMSG_TEAM_RECHARGE_CREATE_RETURN                      0x052DC1D0     72B
  CMSG_TEAM_RECHARGE_EXIT_TEAM_REQUEST                  0x052DFDAC    152B
  CMSG_TEAM_RECHARGE_EXIT_TEAM_RETURN                   0x052DFF30     72B
  CMSG_TEAM_RECHARGE_INVITE_LIST_REQUEST                0x052DE81C    168B
  CMSG_TEAM_RECHARGE_INVITE_LIST_RETURN                 0x052DEC8C   1100B
  CMSG_TEAM_RECHARGE_INVITE_REQUEST                     0x052DDA20    496B
  CMSG_TEAM_RECHARGE_INVITE_RETURN                      0x052DDDE8    452B
  CMSG_TEAM_RECHARGE_JOIN_LIST_REQUEST                  0x052DCE2C    152B
  CMSG_TEAM_RECHARGE_JOIN_LIST_RETURN                   0x052DD28C   1100B
  CMSG_TEAM_RECHARGE_JOIN_REQUEST                       0x052DC4C8    168B
  CMSG_TEAM_RECHARGE_JOIN_RETURN                        0x052DC898    808B
  CMSG_TEAM_RECHARGE_QUICK_REWARD_REQUEST               0x052DF344    152B
  CMSG_TEAM_RECHARGE_QUICK_REWARD_RETURN                0x052DF52C    104B
  CMSG_TEAM_RECHARGE_REJECT_INVITE_REQUEST              0x052DE25C    168B
  CMSG_TEAM_RECHARGE_REJECT_INVITE_RETURN               0x052DE3F0     72B
  CMSG_TEAM_RECHARGE_UPDATE_INTEGRAL                    0x052DFAE8     88B
  CMSG_TEAM_RECHARGE_UPDATE_PLAYER_HEAD                 0x052E0098     88B
  CMSG_TEAM_RECHARGE_UPDATE_PLAYER_NAME                 0x052E02B4    324B
  CMSG_THIRDFORCE_SYNC                                  0x051F4350    812B
  CMSG_THREEDAYS_ACTION_REQUEST                         0x052E12E4     72B
  CMSG_THREEDAYS_ACTION_RETURN                          0x052E15C0    200B
  CMSG_THREEDAYS_REWARD_REQUEST                         0x052E1ACC     72B
  CMSG_THREEDAYS_REWARD_RETURN                          0x052E1E14    232B
  CMSG_TIME_REFRESH                                     0x052D9860     72B
  CMSG_TOWER_LEADER_RETURN                              0x0517EAFC    584B
  CMSG_TOWER_MILITARY_SITUATION                         0x0517E780    356B
  CMSG_TRAP_BUILD                                       0x052E2930    592B
  CMSG_TRAP_BUILD_CANCEL                                0x052E2F30     56B
  CMSG_TRAP_BUILD_CANCEL_RETURN                         0x052E3028     56B
  CMSG_TRAP_BUILD_END                                   0x052E3120     56B
  CMSG_TRAP_BUILD_END_RETURN                            0x052E3218     56B
  CMSG_TRAP_BUILD_END_TIP                               0x052E3370     88B
  CMSG_TRAP_CONSTRUCTOR_INFO                            0x052E2474    556B
  CMSG_TRAP_DESTROY                                     0x052E2CA0     88B
  CMSG_TRAP_DESTROY_RETURN                              0x052E2E18     88B
  CMSG_TRAP_GOLD_ACCELERATE                             0x052E3488     56B
  CMSG_TRAP_ITEM_ACCELERATE                             0x052E35E0     88B
  CMSG_TRAP_ITEM_ACCELERATE_ONEKEY                      0x052E3A98    612B
  CMSG_TRAP_ITEM_ACCELERATE_ONEKEY_RETURN               0x052E3DBC     56B
  CMSG_TRAP_ITEM_ACCELERATE_RETURN                      0x052E36F8     56B
  CMSG_TREASURE_CARD_GET_REWARD_REQUEST                 0x052E4B48     88B
  CMSG_TREASURE_CARD_GET_REWARD_RETURN                  0x052E4D78    136B
  CMSG_TREASURE_CARD_REFRESH_REQUEST                    0x052E4EE8     72B
  CMSG_TREASURE_CARD_REWARD_INFO_REQUEST                0x052E450C     72B
  CMSG_TREASURE_CARD_REWARD_INFO_RETURN                 0x052E479C    652B
  CMSG_TRIBUTE_REQUEST                                  0x052E5244     88B
  CMSG_TRIBUTE_RETURN                                   0x052E54B8    528B
  CMSG_TRIGGER_QUEST_REQUEST                            0x05287ADC    420B
  CMSG_TURN_SOUL_RECAST_TURNTABLE_REQUEST               0x0505E064     72B
  CMSG_TURN_SOUL_RECAST_TURNTABLE_RETURN                0x0505E2A4    516B
  CMSG_UNAPPLY_ENTER_LEAGUE                             0x050F85E8     72B
  CMSG_UNLOCK_BUILDING_SKIN_REQUEST                     0x04FCDDF4    168B
  CMSG_UNLOCK_BUILDING_SKIN_RETURN                      0x04FCDF84     72B
  CMSG_UPDATA_DINAR_BACK_INFO                           0x0503C118    104B
  CMSG_UPDATA_MAGIC_LAMP_INFO                           0x051E22C4    120B
  CMSG_UPDATE_BUILDING                                  0x04FCBA44    168B
  CMSG_UPDATE_CLANPK_AMRY_INFO                          0x04FE9DB4   1620B
  CMSG_UPDATE_CLANPK_ATTACK_AMRY_INFO                   0x05002108    376B
  CMSG_UPDATE_CLANPK_DEFEND_AMRY_INFO                   0x05001304   3184B
  CMSG_UPDATE_FAVORITE_REQUEST                          0x05064894    372B
  CMSG_UPDATE_FAVORITE_RETURN                           0x05064C98    372B
  CMSG_UPDATE_FULL_RECHARGE_GOLD                        0x05087D70     72B
  CMSG_UPDATE_GENERAL_ACTIBITIES_INFO                   0x05089C38    488B
  CMSG_UPDATE_HERO_LEGEND_TASK_PROGRESS                 0x050B5AD0    120B
  CMSG_UPDATE_KNIGHT_GLORY_HELP_TIMES                   0x050ED080     72B
  CMSG_UPDATE_KNIGHT_GLORY_JOIN_TIMES                   0x050ED1B4     72B
  CMSG_UPDATE_LEAGUEBUILD                               0x0515B508    584B
  CMSG_UPDATE_LEAGUEBUILD_CONNECT_STATUS                0x0515B984    452B
  CMSG_UPDATE_ONE_DAILY_TASKS                           0x050257F4    104B
  CMSG_UPDATE_OWNER_BUILDUP                             0x0510B398    104B
  CMSG_UPDATE_PLAYER_NAME                               0x04FBAF44    308B
  CMSG_UPDATE_QUEST                                     0x05285978    120B
  CMSG_UPDATE_QUEST_CHAMPIONSHIP                        0x04FD41F4    136B
  CMSG_UPDATE_QUEST_CHAMPIONSHIP_REQUEST                0x04FD43D0    104B
  CMSG_UPDATE_QUEST_REQUEST                             0x05285F60    104B
  CMSG_UPDATE_REBUILDING_OASISE_TASKS                   0x05294EE4    104B
  CMSG_UPDATE_SECRET_TASKS                              0x052BA560    960B
  CMSG_USERINFO_REQUEST                                 0x0517C544    120B
  CMSG_USERINFO_RETURN                                  0x0517C77C    344B
  CMSG_USE_AMRY_SKIN_SUCESS                             0x04FAC7D4     72B
  CMSG_USE_BUILDING_SKIN_SUCESS                         0x04FCFEAC     72B
  CMSG_USE_ITEM_AND_CHANGE_CHAT_BUBBLE                  0x04FBB8B8     72B
  CMSG_USE_NAMEPLATE_SUCESS                             0x0527A16C     72B
  CMSG_USE_SKIN_SUCESS                                  0x052C5814     72B
  CMSG_USE_VIP_ITEM_RETURN                              0x0505DF24     88B
  CMSG_VIP_BOX_INFO_REQUEST                             0x052C49C8     56B
  CMSG_VIP_BOX_INFO_RETURN                              0x052C4B54    104B
  CMSG_VIP_ITEM_END_REQUEST                             0x0505B088     56B
  CMSG_VIP_LOGIN_INFO                                   0x0505DD8C    120B
  CMSG_VIP_SHOP_BUY_REQUEST                             0x052E6094     88B
  CMSG_VIP_SHOP_BUY_RETURN                              0x052E620C     88B
  CMSG_VIP_SHOP_ITEM_INFO_REQUEST                       0x052E6324     56B
  CMSG_VIP_SHOP_ITEM_INFO_RETURN                        0x052E657C    516B
  CMSG_WAR_LORD_ACTION_MATCH_INFO_REQUEST               0x052E8234     56B
  CMSG_WAR_LORD_ACTION_MATCH_INFO_RETURN                0x052E838C     88B
  CMSG_WAR_LORD_ACTION_RANK_REQUEST                     0x052E75C8     88B
  CMSG_WAR_LORD_ACTION_RANK_RETURN                      0x052E7B6C   1444B
  CMSG_WEB_PLACARD                                      0x052EA9DC    324B
  CMSG_WEEKLY_SPECIAL_GIFT_REQUEST                      0x0509361C     56B
  CMSG_WEEK_CARD_INFO                                   0x052F1424    720B
  CMSG_WEEK_CARD_REWARD_REQUEST                         0x052F17DC     72B
  CMSG_WEEK_CARD_REWARD_RETURN                          0x052F190C     72B
  CMSG_WEEK_SHARE_REWARD_REQUEST                        0x0505D55C     56B
  CMSG_WHEEL_REWARD_REQUEST                             0x052F2B68     88B
  CMSG_WHEEL_REWARD_RETURN                              0x052F2D18    104B
  CMSG_WHEEL_TURN_REQUEST                               0x052F254C    104B
  CMSG_WHEEL_TURN_RETURN                                0x052F2814    564B
  CMSG_WISHING                                          0x052F5A94     88B
  CMSG_WISHINGPOOL_INFO                                 0x052F6200    216B
  CMSG_WISHING_RETURN                                   0x052F5EC8     72B
  CMSG_WORKER_INFO                                      0x04FCB0D0    600B
  CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST             0x052F9658     56B
  CMSG_WORLD_BATTLEFIELD_SELF_GROUP_RETURN              0x052F9B08    780B
  CMSG_WORLD_BATTLEFIELD_SELF_RANK_REQUEST              0x052F7C34     56B
  CMSG_WORLD_BATTLEFIELD_SELF_RANK_RETURN               0x052F7DC8    104B
  CMSG_WORLD_BATTLEFIELD_SYS_INFO                       0x052FEFE0    388B
  CMSG_WORLD_BATTLE_ACTION_DETAIL_REQUEST               0x052F7334     56B
  CMSG_WORLD_BATTLE_ACTION_DETAIL_RETURN                0x052F7764   1040B
  CMSG_WORLD_BATTLE_ACTION_REQUEST                      0x052F68C4     56B
  CMSG_WORLD_BATTLE_ACTION_RETURN                       0x052F6EA8    972B
  CMSG_WORLD_BATTLE_CENTER_FORCE_ID_REQUEST             0x05301460     56B
  CMSG_WORLD_BATTLE_CENTER_FORCE_ID_RETURN              0x0530165C    324B
  CMSG_WORLD_BATTLE_DOMINION_RECORD_REQUEST             0x05301888     72B
  CMSG_WORLD_BATTLE_DOMINION_RECORD_RETURN              0x05301B54    616B
  CMSG_WORLD_BATTLE_ENTER_REQUEST                       0x052FEBE0     56B
  CMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST                  0x052FF224     56B
  CMSG_WORLD_BATTLE_ENTER_VIEW_RETURN                   0x052FF344     72B
  CMSG_WORLD_BATTLE_EXIT_REQUEST                        0x052FECD8     56B
  CMSG_WORLD_BATTLE_GROUP_INFO_REQUEST                  0x052F89EC     56B
  CMSG_WORLD_BATTLE_GROUP_INFO_RETURN                   0x052F8FA0   1324B
  CMSG_WORLD_BATTLE_GROUP_MEMBER_REQUEST                0x052F7F1C     72B
  CMSG_WORLD_BATTLE_GROUP_MEMBER_RETURN                 0x052F8438   1268B
  CMSG_WORLD_BATTLE_GROUP_RANK_REQUEST                  0x052FCA74     56B
  CMSG_WORLD_BATTLE_GROUP_RANK_RETURN                   0x052FCEB0   1156B
  CMSG_WORLD_BATTLE_JOIN_GROUP_REQUEST                  0x052FACFC     72B
  CMSG_WORLD_BATTLE_JOIN_GROUP_RETURN                   0x052FB1FC    796B
  CMSG_WORLD_BATTLE_KICK_MEMBER_REQUEST                 0x052FBA04     88B
  CMSG_WORLD_BATTLE_KICK_MEMBER_RETURN                  0x052FBBB4    104B
  CMSG_WORLD_BATTLE_LEAVE_GROUP_REQUEST                 0x052F9F00     72B
  CMSG_WORLD_BATTLE_LEAVE_GROUP_RETURN                  0x052FA06C     88B
  CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST                 0x052FA184     56B
  CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW             0x052FA3B4    136B
  CMSG_WORLD_BATTLE_NEW_SIGN_UP_RETURN                  0x052FA8F4    796B
  CMSG_WORLD_BATTLE_OVERLORD_RECORD_REQUEST             0x052FD3F4     56B
  CMSG_WORLD_BATTLE_OVERLORD_RECORD_RETURN              0x052FD858   1128B
  CMSG_WORLD_BATTLE_PLAYER_OFFICIAL_REQUEST             0x052FFBA0     56B
  CMSG_WORLD_BATTLE_PLAYER_OFFICIAL_RETURN              0x052FFF68    928B
  CMSG_WORLD_BATTLE_PLAYER_RANK_REQUEST                 0x052FC0B0     56B
  CMSG_WORLD_BATTLE_PLAYER_RANK_RETURN                  0x052FC4EC   1156B
  CMSG_WORLD_BATTLE_SERVER_OFFICIAL_REQUEST             0x052FF44C     56B
  CMSG_WORLD_BATTLE_SERVER_OFFICIAL_RETURN              0x052FF790    848B
  CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_REQUEST         0x05300DC8    388B
  CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_RETURN          0x0530121C    388B
  CMSG_WORLD_BATTLE_SET_POWER_REQUEST                   0x052FB670    104B
  CMSG_WORLD_BATTLE_SET_POWER_RETURN                    0x052FB86C    120B
  CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_REQUEST         0x05300544    356B
  CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_RETURN          0x05300978    388B
  CMSG_WORLD_BATTLE_SIGNUP_REQUEST                      0x052FBE38     72B
  CMSG_WORLD_BATTLE_SIGNUP_RETURN                       0x052FBF98     88B
  CMSG_WORLD_BATTLE_SYNC_BE_KICKED                      0x052FBD08     72B
  CMSG_YAHTZEE_GAME_BEGIN_REQUEST                       0x0531E784    152B
  CMSG_YAHTZEE_GAME_BEGIN_RETURN                        0x0531E8DC     56B
  CMSG_YAHTZEE_GAME_END_REQUEST                         0x05320284    152B
  CMSG_YAHTZEE_GAME_END_RETURN                          0x053203DC     56B
  CMSG_YAHTZEE_GAME_REROLL_REQUEST                      0x0531F2F0    556B
  CMSG_YAHTZEE_GAME_REROLL_RETURN                       0x0531F7D0    816B
  CMSG_YAHTZEE_GAME_ROLL_REQUEST                        0x0531EB80    152B
  CMSG_YAHTZEE_GAME_ROLL_RETURN                         0x0531EDB4    432B
  CMSG_YAHTZEE_GAME_SET_POINT_REQUEST                   0x0531FDB4    168B
  CMSG_YAHTZEE_GAME_SET_POINT_RETURN                    0x0531FFB0    104B
  CMail                                                 0x038DC560      4B
  CMailConfig                                           0x033D7E48      8B
  CMailDBUtil                                           0x0335A7E4    268B
  CMailDBUtil                                           0x0335A358    280B
  CMailDBUtil12getDataCountEv                           0x217CE0000F991 396614459981824B
  CMailTxtTitleCell                                     0x0479D100      8B
  CamelXml                                              0x04CA3B10      8B
  CamelXml                                              0x04CA3B18      8B
  CamelXml                                              0x04CA4350      8B
  CamelXml                                              0x04CA4358      8B
  Camel_shop_showXml                                    0x04CA54D4      8B
  Camel_shop_showXml                                    0x04CA54DC      8B
  Castle_fundXml                                        0x04CA6BBC      8B
  Castle_fundXml                                        0x04CA6BC4      8B
  Castle_fundXml                                        0x04CA7284      8B
  Castle_fundXml                                        0x04CA728C      8B
  Castle_gloryXml                                       0x04CA8A70      8B
  Castle_gloryXml                                       0x04CA8A78      8B
  Castle_gloryXml                                       0x04CA9178      8B
  Castle_gloryXml                                       0x04CA9180      8B
  Castle_up_arrowXml                                    0x04CAA590      8B
  Castle_up_arrowXml                                    0x04CAA598      8B
  Castle_up_arrowXml                                    0x04CAAC68      8B
  Castle_up_arrowXml                                    0x04CAAC70      8B
  Castle_up_rewardXml                                   0x04CAC5D0      8B
  Castle_up_rewardXml                                   0x04CAC5D8      8B
  Castle_up_rewardXml10getDataArrEv                     0x105F30000D36C 222822903476052B
  Championship_baseXml                                  0x04CAE4B8      8B
  Championship_baseXml                                  0x04CAE4C0      8B
  Championship_baseXml                                  0x04CAEC40      8B
  Championship_baseXml                                  0x04CAEC48      8B
  Championship_lvXml                                    0x04CB070C      8B
  Championship_lvXml                                    0x04CB0714      8B
  Championship_lvXml                                    0x04CB0E0C      8B
  Championship_lvXml                                    0x04CB0E14      8B
  Championship_packageXml                               0x04CB23B8      8B
  Championship_packageXml                               0x04CB23C0      8B
  Championship_taskXml                                  0x04CB3910      8B
  Championship_taskXml                                  0x04CB3918      8B
  ChatDBUtil                                            0x036806B8    268B
  ChatDBUtil                                            0x0367F6E0    340B
  Chat_boxXml                                           0x04CB46FC      8B
  Chat_boxXml                                           0x04CB4704      8B
  Chat_bubbleXml                                        0x04CB58E8      8B
  Chat_bubbleXml                                        0x04CB58F0      8B
  Chat_bubbleXml                                        0x04CB6068      8B
  Chat_bubbleXml                                        0x04CB6070      8B
  Chat_bubble_sourceXml                                 0x04CB7124      8B
  Chat_bubble_sourceXml                                 0x04CB712C      8B
  Chat_faceXml                                          0x04CB7F9C      8B
  Chat_faceXml                                          0x04CB7FA4      8B
  City_signatureXml                                     0x04CB8D94      8B
  City_signatureXml                                     0x04CB8D9C      8B
  City_skinXml                                          0x04CBA548      8B
  City_skinXml                                          0x04CBA550      8B
  City_skinXml                                          0x04CBACC0      8B
  City_skinXml                                          0x04CBACC8      8B
  City_skin_sourceXml                                   0x04CBC1CC      8B
  City_skin_sourceXml                                   0x04CBC1D4      8B
  CivilizationXml                                       0x04CBD2AC      8B
  CivilizationXml                                       0x04CBD2B4      8B
  Clanpk_barrageXml                                     0x04CBE084      8B
  Clanpk_barrageXml                                     0x04CBE08C      8B
  Clanpk_baseXml                                        0x04CBF8F4      8B
  Clanpk_baseXml                                        0x04CBF8FC      8B
  Clanpk_build_defXml                                   0x04CC1320      8B
  Clanpk_build_defXml                                   0x04CC1328      8B
  Clanpk_build_defXml                                   0x04CC19D4      8B
  Clanpk_build_defXml                                   0x04CC19DC      8B
  Clanpk_build_itemXml                                  0x04CC2AEC      8B
  Clanpk_build_itemXml                                  0x04CC2AF4      8B
  Clanpk_build_posXml                                   0x04CC3A48      8B
  Clanpk_build_posXml                                   0x04CC3A50      8B
  Clanpk_build_spaceXml                                 0x04CC4F58      8B
  Clanpk_build_spaceXml                                 0x04CC4F60      8B
  Clanpk_build_specialXml                               0x04CC6190      8B
  Clanpk_build_specialXml                               0x04CC6198      8B
  Clanpk_build_specialXml                               0x04CC684C      8B
  Clanpk_build_specialXml                               0x04CC6854      8B
  Clanpk_donateXml                                      0x04CC7DCC      8B
  Clanpk_donateXml                                      0x04CC7DD4      8B
  Clanpk_donateXml                                      0x04CC8494      8B
  Clanpk_donateXml                                      0x04CC849C      8B
  Clanpk_helpXml                                        0x04CC985C      8B
  Clanpk_helpXml                                        0x04CC9864      8B
  Clanpk_helpXml                                        0x04CC9E60      8B
  Clanpk_helpXml                                        0x04CC9E68      8B
  Clanpk_player_rewardXml                               0x04CCB814      8B
  Clanpk_player_rewardXml                               0x04CCB81C      8B
  Clanpk_rankXml                                        0x04CCD930      8B
  Clanpk_rankXml                                        0x04CCD938      8B
  Clanpk_rank_rewardXml                                 0x04CCEEEC      8B
  Clanpk_rank_rewardXml                                 0x04CCEEF4      8B
  Clanpk_rank_rewardXml                                 0x04CCF5F4      8B
  Clanpk_rank_rewardXml                                 0x04CCF5FC      8B
  Clanpk_shopXml                                        0x04CD07EC      8B
  Clanpk_shopXml                                        0x04CD07F4      8B
  Clear_castleXml                                       0x04CD17D8      8B
  Clear_castleXml                                       0x04CD17E0      8B
  Clear_heroXml                                         0x04CD2628      8B
  Clear_heroXml                                         0x04CD2630      8B
  Clear_itemXml                                         0x04CD3788      8B
  Clear_itemXml                                         0x04CD3790      8B
  Clear_league_scienceXml                               0x04CD45C4      8B
  Clear_league_scienceXml                               0x04CD45CC      8B
  Clear_petXml                                          0x04CD5410      8B
  Clear_petXml                                          0x04CD5418      8B
  Clear_scienceXml                                      0x04CD623C      8B
  Clear_scienceXml                                      0x04CD6244      8B
  Clear_solderXml                                       0x04CD7440      8B
  Clear_solderXml                                       0x04CD7448      8B
  Clear_vipXml                                          0x04CD828C      8B
  Clear_vipXml                                          0x04CD8294      8B
  Client_building_skinXml                               0x04CD92C4      8B
  Client_building_skinXml                               0x04CD92CC      8B
  Client_building_skinXml                               0x04CD9988      8B
  Client_building_skinXml                               0x04CD9990      8B
  Collect_energyXml                                     0x04CDB0E0      8B
  Collect_energyXml                                     0x04CDB0E8      8B
  Collect_energyXml                                     0x04CDB814      8B
  Collect_energyXml                                     0x04CDB81C      8B
  ComboXml                                              0x04CDCD68      8B
  ComboXml                                              0x04CDCD70      8B
  ConsumptionXml                                        0x04CDDBB8      8B
  ConsumptionXml                                        0x04CDDBC0      8B
  Continuity_gift_packXml                               0x04CDEF1C      8B
  Continuity_gift_packXml                               0x04CDEF24      8B
  Continuity_gift_rewardXml                             0x04CE0424      8B
  Continuity_gift_rewardXml                             0x04CE042C      8B
  Continuity_gift_rewardXml                             0x04CE0B2C      8B
  Continuity_gift_rewardXml                             0x04CE0B34      8B
  Continuity_gift_tokenXml                              0x04CE23C4      8B
  Continuity_gift_tokenXml                              0x04CE23CC      8B
  Continuity_gift_tokenXml                              0x04CE2A48      8B
  Continuity_gift_tokenXml                              0x04CE2A50      8B
  Crest_drawXml                                         0x04CE3BB8      8B
  Crest_drawXml                                         0x04CE3BC0      8B
  Crest_prestige_attributesXml                          0x04CE4D1C      8B
  Crest_prestige_attributesXml                          0x04CE4D24      8B
  Crest_prestige_attributesXml                          0x04CE53F0      8B
  Crest_prestige_attributesXml                          0x04CE53F8      8B
  Crest_prestige_baseXml                                0x04CE6CFC      8B
  Crest_prestige_baseXml                                0x04CE6D04      8B
  Crest_prestige_evolutionXml                           0x04CE85E0      8B
  Crest_prestige_evolutionXml                           0x04CE85E8      8B
  Crest_prestige_evolutionXml                           0x04CE8D14      8B
  Crest_prestige_evolutionXml                           0x04CE8D1C      8B
  Crest_prestige_groupXml                               0x04CEA214      8B
  Crest_prestige_groupXml                               0x04CEA21C      8B
  Crest_prestige_groupXml                               0x04CEA870      8B
  Crest_prestige_groupXml                               0x04CEA878      8B
  Daily_consumeXml                                      0x04CEC284      8B
  Daily_consumeXml                                      0x04CEC28C      8B
  Daily_consumeXml                                      0x04CEC9F8      8B
  Daily_consumeXml                                      0x04CECA00      8B
  Daily_guild_rewardXml                                 0x04CEE2A4      8B
  Daily_guild_rewardXml                                 0x04CEE2AC      8B
  Daily_rechargeXml                                     0x04CEF378      8B
  Daily_rechargeXml                                     0x04CEF380      8B
  Daily_recharge_rewardXml                              0x04CF0740      8B
  Daily_recharge_rewardXml                              0x04CF0748      8B
  Daily_recharge_rewardXml                              0x04CF0DEC      8B
  Daily_recharge_rewardXml                              0x04CF0DF4      8B
  Daily_shop_rewardXml                                  0x04CF2324      8B
  Daily_shop_rewardXml                                  0x04CF232C      8B
  Daily_tasksXml                                        0x04CF39A0      8B
  Daily_tasksXml                                        0x04CF39A8      8B
  Daily_tasks_rewardXml                                 0x04CF4870      8B
  Daily_tasks_rewardXml                                 0x04CF4878      8B
  DatabaseRequest                                       0x0502AA28    580B
  DatabaseResponse                                      0x0502AF98    564B
  Desert_tradeXml                                       0x04CF6D08      8B
  Desert_tradeXml                                       0x04CF6D10      8B
  Desert_tradeXml                                       0x04CF7508      8B
  Desert_tradeXml                                       0x04CF7510      8B
  Desert_trade_truckXml                                 0x04CF9C30      8B
  Desert_trade_truckXml                                 0x04CF9C38      8B
  Desert_trade_truckXml                                 0x04CFA328      8B
  Desert_trade_truckXml                                 0x04CFA330      8B
  Dessert_makeXml                                       0x04CFB728      8B
  Dessert_makeXml                                       0x04CFB730      8B
  Dessert_make_dropXml                                  0x04CFC7D4      8B
  Dessert_make_dropXml                                  0x04CFC7DC      8B
  Dessert_make_dropXml                                  0x04CFCEB4      8B
  Dessert_make_dropXml                                  0x04CFCEBC      8B
  Dessert_make_refreshXml                               0x04CFE084      8B
  Dessert_make_refreshXml                               0x04CFE08C      8B
  Dessert_make_skinXml                                  0x04CFF1D0      8B
  Dessert_make_skinXml                                  0x04CFF1D8      8B
  Dessert_make_tasteXml                                 0x04D003F8      8B
  Dessert_make_tasteXml                                 0x04D00400      8B
  Dessert_make_tasteXml                                 0x04D00AD8      8B
  Dessert_make_tasteXml                                 0x04D00AE0      8B
  Dinar_backXml                                         0x04D01D74      8B
  Dinar_backXml                                         0x04D01D7C      8B
  Doublelottery_baseXml                                 0x04D03B04      8B
  Doublelottery_baseXml                                 0x04D03B0C      8B
  Doublelottery_dropXml                                 0x04D04B68      8B
  Doublelottery_dropXml                                 0x04D04B70      8B
  Doublelottery_dropXml                                 0x04D0516C      8B
  Doublelottery_dropXml                                 0x04D05174      8B
  Doublelottery_groupXml                                0x04D065C0      8B
  Doublelottery_groupXml                                0x04D065C8      8B
  Doublelottery_groupXml                                0x04D06C1C      8B
  Doublelottery_groupXml                                0x04D06C24      8B
  DownloadXml                                           0x04D084A8      8B
  DownloadXml                                           0x04D084B0      8B
  DownloadXml                                           0x04D08BAC      8B
  DownloadXml                                           0x04D08BB4      8B
  Drop_showXml                                          0x04D0A014      8B
  Drop_showXml                                          0x04D0A01C      8B
  E7getDataEPKc                                         0x3C6900003C66  15471B
  Elemental_war_descXml                                 0x04D0AD18      8B
  Elemental_war_descXml                                 0x04D0AD20      8B
  Elemental_war_eventXml                                0x04D0CDAC      8B
  Elemental_war_eventXml                                0x04D0CDB4      8B
  Elemental_war_eventXml                                0x04D0D510      8B
  Elemental_war_eventXml                                0x04D0D518      8B
  Elemental_war_event_buffXml                           0x04D0E89C      8B
  Elemental_war_event_buffXml                           0x04D0E8A4      8B
  Elemental_war_event_cityXml                           0x04D0FE10      8B
  Elemental_war_event_cityXml                           0x04D0FE18      8B
  Elemental_war_event_cityXml                           0x04D104EC      8B
  Elemental_war_event_cityXml                           0x04D104F4      8B
  Elemental_war_event_lord_rewardXml                    0x04D11E5C      8B
  Elemental_war_event_lord_rewardXml                    0x04D11E64      8B
  Elemental_war_event_lord_rewardXml                    0x04D12564      8B
  Elemental_war_event_lord_rewardXml                    0x04D1256C      8B
  Elemental_war_event_mapXml                            0x04D138EC      8B
  Elemental_war_event_mapXml                            0x04D138F4      8B
  Elemental_war_event_rewardXml                         0x04D14D20      8B
  Elemental_war_event_rewardXml                         0x04D14D28      8B
  Elemental_war_event_rewardXml                         0x04D15428      8B
  Elemental_war_event_rewardXml                         0x04D15430      8B
  Elemental_war_event_scoreXml                          0x04D168F8      8B
  Elemental_war_event_scoreXml                          0x04D16900      8B
  Elemental_war_event_scoreXml                          0x04D16F48      8B
  Elemental_war_event_scoreXml                          0x04D16F50      8B
  Elemental_war_league_rewardXml                        0x04D188F4      8B
  Elemental_war_league_rewardXml                        0x04D188FC      8B
  Elemental_war_league_rewardXml                        0x04D18FF4      8B
  Elemental_war_league_rewardXml                        0x04D18FFC      8B
  Elemental_war_targetXml                               0x04D1A148      8B
  Elemental_war_targetXml                               0x04D1A150      8B
  Elemental_war_warzoneXml                              0x04D1AE4C      8B
  Elemental_war_warzoneXml                              0x04D1AE54      8B
  EquipXml                                              0x04D1C620      8B
  EquipXml                                              0x04D1C628      8B
  EraXml                                                0x04D1D6C4      8B
  EraXml                                                0x04D1D6CC      8B
  EraXml                                                0x04D1DCFC      8B
  EraXml                                                0x04D1DD04      8B
  Era_globalXml                                         0x04D1F558      8B
  Era_globalXml                                         0x04D1F560      8B
  Era_globalXml                                         0x04D1FBE8      8B
  Era_globalXml                                         0x04D1FBF0      8B
  Era_taskXml                                           0x04D215A8      8B
  Era_taskXml                                           0x04D215B0      8B
  Era_task_unlockXml                                    0x04D224A4      8B
  Era_task_unlockXml                                    0x04D224AC      8B
  Event_packXml                                         0x04D231FC      8B
  Event_packXml                                         0x04D23204      8B
  Everyday_giftXml                                      0x04D24508      8B
  Everyday_giftXml                                      0x04D24510      8B
  Everyday_gift_newXml                                  0x04D25C00      8B
  Everyday_gift_newXml                                  0x04D25C08      8B
  Everyday_gift_newXml                                  0x04D26204      8B
  Everyday_gift_newXml                                  0x04D2620C      8B
  Everyday_gift_new_correctXml                          0x04D27A0C      8B
  Everyday_gift_new_correctXml                          0x04D27A14      8B
  Everyday_gift_new_correctXml                          0x04D28094      8B
  Everyday_gift_new_correctXml                          0x04D2809C      8B
  Extra_gift_packXml                                    0x04D29C88      8B
  Extra_gift_packXml                                    0x04D29C90      8B
  Extra_gift_pack_questXml                              0x04D2B248      8B
  Extra_gift_pack_questXml                              0x04D2B250      8B
  Extra_gift_pack_questXml                              0x04D2B8D0      8B
  Extra_gift_pack_questXml                              0x04D2B8D8      8B
  Extra_gift_pack_rewardXml                             0x04D2CF3C      8B
  Extra_gift_pack_rewardXml                             0x04D2CF44      8B
  Extra_gift_pack_rewardXml                             0x04D2D61C      8B
  Extra_gift_pack_rewardXml                             0x04D2D624      8B
  Fans_rewardXml                                        0x04D2ED98      8B
  Fans_rewardXml                                        0x04D2EDA0      8B
  Financial_expert_packXml                              0x04D2FD24      8B
  Financial_expert_packXml                              0x04D2FD2C      8B
  Financial_expert_rewardXml                            0x04D31184      8B
  Financial_expert_rewardXml                            0x04D3118C      8B
  Financial_expert_rewardXml                            0x04D3188C      8B
  Financial_expert_rewardXml                            0x04D31894      8B
  Financial_expert_taskXml                              0x04D32C74      8B
  Financial_expert_taskXml                              0x04D32C7C      8B
  Fixed_accumulation_rankXml                            0x04D34094      8B
  Fixed_accumulation_rankXml                            0x04D3409C      8B
  Fixed_accumulation_rankXml                            0x04D34794      8B
  Fixed_accumulation_rankXml                            0x04D3479C      8B
  Fixed_accumulation_rewardXml                          0x04D364EC      8B
  Fixed_accumulation_rewardXml                          0x04D364F4      8B
  Fixed_accumulation_rewardXml                          0x04D36C30      8B
  Fixed_accumulation_rewardXml                          0x04D36C38      8B
  Fixed_team_rankXml                                    0x04D38F10      8B
  Fixed_team_rankXml                                    0x04D38F18      8B
  Fixed_team_rankXml                                    0x04D39698      8B
  Fixed_team_rankXml                                    0x04D396A0      8B
  Friend_giftXml                                        0x04D3B63C      8B
  Friend_giftXml                                        0x04D3B644      8B
  Friend_giftXml                                        0x04D3BD1C      8B
  Friend_giftXml                                        0x04D3BD24      8B
  Friend_invited_basicXml                               0x04D3D588      8B
  Friend_invited_basicXml                               0x04D3D590      8B
  Friend_invited_taskXml                                0x04D3EB08      8B
  Friend_invited_taskXml                                0x04D3EB10      8B
  Friend_invited_taskXml                                0x04D3F33C      8B
  Friend_invited_taskXml                                0x04D3F344      8B
  Friend_invited_tokenXml                               0x04D408F8      8B
  Friend_invited_tokenXml                               0x04D40900      8B
  Full_rechargeXml                                      0x04D41DF8      8B
  Full_rechargeXml                                      0x04D41E00      8B
  Full_rechargeXml                                      0x04D42464      8B
  Full_rechargeXml                                      0x04D4246C      8B
  GUE_BATTLE7getDataEPKc                                0x4108202042020040 565735307084420B
  GUE_BATTLE7getDataEPKc                                0x800800681101011 6915928138711046B
  G_AF_INFO7getDataEPKc                                 0x387100003869 62088047245428B
  General_shopXml                                       0x04D445A4      8B
  General_shopXml                                       0x04D445AC      8B
  General_shopXml                                       0x04D44C90      8B
  General_shopXml                                       0x04D44C98      8B
  General_shop_gift_packXml                             0x04D466AC      8B
  General_shop_gift_packXml                             0x04D466B4      8B
  General_shop_gift_packXml                             0x04D46CF4      8B
  General_shop_gift_packXml                             0x04D46CFC      8B
  Giant_invasionXml                                     0x04D48AB8      8B
  Giant_invasionXml                                     0x04D48AC0      8B
  Giant_invasion_monsterXml                             0x04D499F4      8B
  Giant_invasion_monsterXml                             0x04D499FC      8B
  Giant_invasion_treasureXml                            0x04D4AB88      8B
  Giant_invasion_treasureXml                            0x04D4AB90      8B
  GifXml                                                0x04D4B9AC      8B
  GifXml                                                0x04D4B9B4      8B
  Gift_invaluableXml                                    0x04D4C768      8B
  Gift_invaluableXml                                    0x04D4C770      8B
  Goodluck_baseXml                                      0x04D4E0B4      8B
  Goodluck_baseXml                                      0x04D4E0BC      8B
  Goodluck_baseXml                                      0x04D4E87C      8B
  Goodluck_baseXml                                      0x04D4E884      8B
  Goodluck_dropXml                                      0x04D4FD84      8B
  Goodluck_dropXml                                      0x04D4FD8C      8B
  Goodluck_dropXml                                      0x04D503E0      8B
  Goodluck_dropXml                                      0x04D503E8      8B
  Goodluck_groupXml                                     0x04D533E4      8B
  Goodluck_groupXml                                     0x04D533EC      8B
  Greedygame_chatXml                                    0x04D541A0      8B
  Greedygame_chatXml                                    0x04D541A8      8B
  Greedygame_groupXml                                   0x04D55724      8B
  Greedygame_groupXml                                   0x04D5572C      8B
  Greedygame_groupXml                                   0x04D55E24      8B
  Greedygame_groupXml                                   0x04D55E2C      8B
  Greedygame_resourceXml                                0x04D57050      8B
  Greedygame_resourceXml                                0x04D57058      8B
  GroupChatDBUtil                                       0x036B58A4    268B
  GroupChatDBUtil                                       0x036B4FE8    340B
  Guild_standoffXml                                     0x04D592B4      8B
  Guild_standoffXml                                     0x04D592BC      8B
  Guild_standoffXml                                     0x04D59AE0      8B
  Guild_standoffXml                                     0x04D59AE8      8B
  Guild_standoff_reward_duelXml                         0x04D5B2E0      8B
  Guild_standoff_reward_duelXml                         0x04D5B2E8      8B
  Guild_standoff_reward_duelXml                         0x04D5B9E8      8B
  Guild_standoff_reward_duelXml                         0x04D5B9F0      8B
  Guild_standoff_reward_rankXml                         0x04D5D85C      8B
  Guild_standoff_reward_rankXml                         0x04D5D864      8B
  Guild_standoff_reward_rankXml                         0x04D5DED8      8B
  Guild_standoff_reward_rankXml                         0x04D5DEE0      8B
  Guild_standoff_reward_starXml                         0x04D5F830      8B
  Guild_standoff_reward_starXml                         0x04D5F838      8B
  Guild_standoff_taskXml                                0x04D60CB4      8B
  Guild_standoff_taskXml                                0x04D60CBC      8B
  Happy_marblesXml                                      0x04D62A8C      8B
  Happy_marblesXml                                      0x04D62A94      8B
  Happy_marblesXml                                      0x04D632A0      8B
  Happy_marblesXml                                      0x04D632A8      8B
  Happy_marbles_probXml                                 0x04D646E0      8B
  Happy_marbles_probXml                                 0x04D646E8      8B
  Happy_marbles_probXml                                 0x04D64DC0      8B
  Happy_marbles_probXml                                 0x04D64DC8      8B
  Happy_marbles_trackXml                                0x04D663E4      8B
  Happy_marbles_trackXml                                0x04D663EC      8B
  Happy_marbles_trackXml                                0x04D66AC4      8B
  Happy_marbles_trackXml                                0x04D66ACC      8B
  Head10getDataMapEv                                    0x40000000200 5792017251624288416B
  Hero_equipXml                                         0x04D68078      8B
  Hero_equipXml                                         0x04D68080      8B
  Hero_legend_baseXml                                   0x04D69650      8B
  Hero_legend_baseXml                                   0x04D69658      8B
  Hero_legend_baseXml                                   0x04D69E24      8B
  Hero_legend_baseXml                                   0x04D69E2C      8B
  Hero_legend_comicXml                                  0x04D6BC68      8B
  Hero_legend_comicXml                                  0x04D6BC70      8B
  Hero_legend_comicXml                                  0x04D6C37C      8B
  Hero_legend_comicXml                                  0x04D6C384      8B
  Hero_legend_lvXml                                     0x04D6D548      8B
  Hero_legend_lvXml                                     0x04D6D550      8B
  Hero_legend_skill_typeXml                             0x04D6E6B8      8B
  Hero_legend_skill_typeXml                             0x04D6E6C0      8B
  Hero_legend_skill_typeXml                             0x04D6EE38      8B
  Hero_legend_skill_typeXml                             0x04D6EE40      8B
  Hero_legend_taskXml                                   0x04D708E0      8B
  Hero_legend_taskXml                                   0x04D708E8      8B
  Hero_legend_taskXml                                   0x04D70F78      8B
  Hero_legend_taskXml                                   0x04D70F80      8B
  Herocollection_eventXml                               0x04D729C0      8B
  Herocollection_eventXml                               0x04D729C8      8B
  Herocollection_operation_eventXml                     0x04D73B90      8B
  Herocollection_operation_eventXml                     0x04D73B98      8B
  Herocollection_packageXml                             0x04D75014      8B
  Herocollection_packageXml                             0x04D7501C      8B
  Herocollection_packageXml                             0x04D7571C      8B
  Herocollection_packageXml                             0x04D75724      8B
  Herocollection_pveXml                                 0x04D77484      8B
  Herocollection_pveXml                                 0x04D7748C      8B
  Herocollection_pveXml                                 0x04D77B04      8B
  Herocollection_pveXml                                 0x04D77B0C      8B
  Herocollection_rechargeXml                            0x04D79618      8B
  Herocollection_rechargeXml                            0x04D79620      8B
  Herocollection_rechargeXml                            0x04D79C98      8B
  Herocollection_rechargeXml                            0x04D79CA0      8B
  Herocollection_storyXml                               0x04D7B25C      8B
  Herocollection_storyXml                               0x04D7B264      8B
  Herocollection_storyXml                               0x04D7B89C      8B
  Herocollection_storyXml                               0x04D7B8A4      8B
  Herocollection_taskXml                                0x04D7D4A0      8B
  Herocollection_taskXml                                0x04D7D4A8      8B
  Herocollection_taskXml                                0x04D7DC44      8B
  Herocollection_taskXml                                0x04D7DC4C      8B
  Herolottery_baseXml                                   0x04D7EF6C      8B
  Herolottery_baseXml                                   0x04D7EF74      8B
  Herolottery_dropXml                                   0x04D80148      8B
  Herolottery_dropXml                                   0x04D80150      8B
  Herolottery_dropXml                                   0x04D80820      8B
  Herolottery_dropXml                                   0x04D80828      8B
  Herolottery_groupXml                                  0x04D8350C      8B
  Herolottery_groupXml                                  0x04D83514      8B
  Huawei_packXml                                        0x04D84560      8B
  Huawei_packXml                                        0x04D84568      8B
  Illegality_newXml                                     0x04D8533C      8B
  Illegality_newXml                                     0x04D85344      8B
  Illegality_new_exactXml                               0x04D86134      8B
  Illegality_new_exactXml                               0x04D8613C      8B
  Imperial_baseXml                                      0x04D86F34      8B
  Imperial_baseXml                                      0x04D86F3C      8B
  Imperial_shopXml                                      0x04D889E4      8B
  Imperial_shopXml                                      0x04D889EC      8B
  Imperial_shopXml                                      0x04D8909C      8B
  Imperial_shopXml                                      0x04D890A4      8B
  Imperial_taskXml                                      0x04D8A868      8B
  Imperial_taskXml                                      0x04D8A870      8B
  InnerDefinedCityXml                                   0x04D8B9BC      8B
  InnerDefinedCityXml                                   0x04D8B9C4      8B
  Innercity_skinXml                                     0x04D8D5D0      8B
  Innercity_skinXml                                     0x04D8D5D8      8B
  Innercity_skinXml                                     0x04D8DD58      8B
  Innercity_skinXml                                     0x04D8DD60      8B
  Innercity_skin_effecttypeXml                          0x04D8F17C      8B
  Innercity_skin_effecttypeXml                          0x04D8F184      8B
  Innercity_skin_effecttypeXml                          0x04D8F89C      8B
  Innercity_skin_effecttypeXml                          0x04D8F8A4      8B
  Innercity_skin_qualityXml                             0x04D90A20      8B
  Innercity_skin_qualityXml                             0x04D90A28      8B
  Innercity_skin_sourceXml                              0x04D91A90      8B
  Innercity_skin_sourceXml                              0x04D91A98      8B
  Innercity_upgrade_rewardXml                           0x04D92F38      8B
  Innercity_upgrade_rewardXml                           0x04D92F40      8B
  Innercity_upgrade_rewardXml                           0x04D93688      8B
  Innercity_upgrade_rewardXml                           0x04D93690      8B
  InvasionXml                                           0x04D9670C      8B
  InvasionXml                                           0x04D96714      8B
  Invasion_timeXml                                      0x04D97674      8B
  Invasion_timeXml                                      0x04D9767C      8B
  Invite_rewardXml                                      0x04D99B60      8B
  Invite_rewardXml                                      0x04D99B68      8B
  Invite_rewardXml                                      0x04D9A2DC      8B
  Invite_rewardXml                                      0x04D9A2E4      8B
  Item_refiningXml                                      0x04D9B694      8B
  Item_refiningXml                                      0x04D9B69C      8B
  K19Castle_up_rewardXml10getDataArrEv                  0x1F56B0001F567 551340656948591B
  K25Active_freepick_rewardXml10getDataArrEv            0x808000180080C8 5334654504698659617B
  K25Active_freepick_rewardXml4Head10getDataMapEv       0x4080080408C0A400 4398113686016B
  Kingdom_giftXml                                       0x04D9C64C      8B
  Kingdom_giftXml                                       0x04D9C654      8B
  Kingdom_gift_reward_levelXml                          0x04D9E350      8B
  Kingdom_gift_reward_levelXml                          0x04D9E358      8B
  Kingdom_gift_reward_levelXml                          0x04D9EAF0      8B
  Kingdom_gift_reward_levelXml                          0x04D9EAF8      8B
  Kingdom_gift_reward_timeXml                           0x04DA034C      8B
  Kingdom_gift_reward_timeXml                           0x04DA0354      8B
  Kingdom_gift_reward_timeXml                           0x04DA09D4      8B
  Kingdom_gift_reward_timeXml                           0x04DA09DC      8B
  Kingdom_gift_reward_tokenXml                          0x04DA2458      8B
  Kingdom_gift_reward_tokenXml                          0x04DA2460      8B
  Kingdom_gift_reward_tokenXml                          0x04DA2AB0      8B
  Kingdom_gift_reward_tokenXml                          0x04DA2AB8      8B
  Kingdom_strategyXml                                   0x04DA4414      8B
  Kingdom_strategyXml                                   0x04DA441C      8B
  Kingdomreward_baseXml                                 0x04DA5A2C      8B
  Kingdomreward_baseXml                                 0x04DA5A34      8B
  Kingdomreward_dialogXml                               0x04DA6D5C      8B
  Kingdomreward_dialogXml                               0x04DA6D64      8B
  Kingdomreward_dialogXml                               0x04DA7384      8B
  Kingdomreward_dialogXml                               0x04DA738C      8B
  Kingdomreward_lvXml                                   0x04DA8C10      8B
  Kingdomreward_lvXml                                   0x04DA8C18      8B
  Kingdomreward_taskXml                                 0x04DAA914      8B
  Kingdomreward_taskXml                                 0x04DAA91C      8B
  Knight_gloryXml                                       0x04DAC810      8B
  Knight_gloryXml                                       0x04DAC818      8B
  Knight_gloryXml                                       0x04DAD0BC      8B
  Knight_gloryXml                                       0x04DAD0C4      8B
  Knight_glory_monsterXml                               0x04DAFF04      8B
  Knight_glory_monsterXml                               0x04DAFF0C      8B
  Knight_glory_monsterXml                               0x04DB06A4      8B
  Knight_glory_monsterXml                               0x04DB06AC      8B
  Kvk_eventXml                                          0x04DB2934      8B
  Kvk_eventXml                                          0x04DB293C      8B
  Kvk_pointXml                                          0x04DB3A0C      8B
  Kvk_pointXml                                          0x04DB3A14      8B
  Kvk_pointXml                                          0x04DB40EC      8B
  Kvk_pointXml                                          0x04DB40F4      8B
  Kvk_rankXml                                           0x04DB5AC0      8B
  Kvk_rankXml                                           0x04DB5AC8      8B
  Kvk_rankXml                                           0x04DB61C8      8B
  Kvk_rankXml                                           0x04DB61D0      8B
  Kvk_rewardXml                                         0x04DB7A48      8B
  Kvk_rewardXml                                         0x04DB7A50      8B
  Kvk_rewardXml                                         0x04DB8150      8B
  Kvk_rewardXml                                         0x04DB8158      8B
  Latch_behaviorXml                                     0x04DB9634      8B
  Latch_behaviorXml                                     0x04DB963C      8B
  Latch_behaviorXml                                     0x04DB9D3C      8B
  Latch_behaviorXml                                     0x04DB9D44      8B
  Latch_collideXml                                      0x04DBAFD0      8B
  Latch_collideXml                                      0x04DBAFD8      8B
  Latch_collider_propertyXml                            0x04DBC294      8B
  Latch_collider_propertyXml                            0x04DBC29C      8B
  Latch_conditionXml                                    0x04DBD084      8B
  Latch_conditionXml                                    0x04DBD08C      8B
  Latch_eventXml                                        0x04DBDE60      8B
  Latch_eventXml                                        0x04DBDE68      8B
  Latch_fall_collideXml                                 0x04DBEC58      8B
  Latch_fall_collideXml                                 0x04DBEC60      8B
  Latch_gem_iconXml                                     0x04DBFED4      8B
  Latch_gem_iconXml                                     0x04DBFEDC      8B
  Latch_gem_iconXml                                     0x04DC058C      8B
  Latch_gem_iconXml                                     0x04DC0594      8B
  Latch_levelXml                                        0x04DC2428      8B
  Latch_levelXml                                        0x04DC2430      8B
  Latch_levelXml                                        0x04DC2B98      8B
  Latch_levelXml                                        0x04DC2BA0      8B
  Latch_object_propertyXml                              0x04DC41A8      8B
  Latch_object_propertyXml                              0x04DC41B0      8B
  Latch_object_stateXml                                 0x04DC4F98      8B
  Latch_object_stateXml                                 0x04DC4FA0      8B
  Latch_objectsXml                                      0x04DC6964      8B
  Latch_objectsXml                                      0x04DC696C      8B
  Latch_objectsXml                                      0x04DC6F78      8B
  Latch_objectsXml                                      0x04DC6F80      8B
  Latch_physicsXml                                      0x04DC8874      8B
  Latch_physicsXml                                      0x04DC887C      8B
  Latch_physics_materialsXml                            0x04DC96DC      8B
  Latch_physics_materialsXml                            0x04DC96E4      8B
  League_eventXml                                       0x04DCB44C      8B
  League_eventXml                                       0x04DCB454      8B
  League_eventXml                                       0x04DCBB98      8B
  League_eventXml                                       0x04DCBBA0      8B
  League_event_rank_rewardXml                           0x04DCD138      8B
  League_event_rank_rewardXml                           0x04DCD140      8B
  League_event_rewardXml                                0x04DCE34C      8B
  League_event_rewardXml                                0x04DCE354      8B
  League_event_taskXml                                  0x04DCF518      8B
  League_event_taskXml                                  0x04DCF520      8B
  League_exchangeXml                                    0x04DD07E8      8B
  League_exchangeXml                                    0x04DD07F0      8B
  League_exchangeXml                                    0x04DD0E44      8B
  League_exchangeXml                                    0x04DD0E4C      8B
  League_giftXml                                        0x04DD227C      8B
  League_giftXml                                        0x04DD2284      8B
  League_giftXml                                        0x04DD2904      8B
  League_giftXml                                        0x04DD290C      8B
  League_medal_systemXml                                0x04DD3FF8      8B
  League_medal_systemXml                                0x04DD4000      8B
  League_medal_systemXml                                0x04DD466C      8B
  League_medal_systemXml                                0x04DD4674      8B
  League_rank_mailXml                                   0x04DD6084      8B
  League_rank_mailXml                                   0x04DD608C      8B
  League_rank_mailXml                                   0x04DD66F0      8B
  League_rank_mailXml                                   0x04DD66F8      8B
  League_rechargeXml                                    0x04DD8448      8B
  League_rechargeXml                                    0x04DD8450      8B
  League_rechargeXml                                    0x04DD8AC0      8B
  League_rechargeXml                                    0x04DD8AC8      8B
  League_recommendXml                                   0x04DD9CB8      8B
  League_recommendXml                                   0x04DD9CC0      8B
  League_short_nameXml                                  0x04DDAD08      8B
  League_short_nameXml                                  0x04DDAD10      8B
  League_short_nameXml                                  0x04DDB3C0      8B
  League_short_nameXml                                  0x04DDB3C8      8B
  League_taskXml                                        0x04DDC4E8      8B
  League_taskXml                                        0x04DDC4F0      8B
  Limit_shop_baseXml                                    0x04DDD4A4      8B
  Limit_shop_baseXml                                    0x04DDD4AC      8B
  Limit_shop_configXml                                  0x04DDE7D8      8B
  Limit_shop_configXml                                  0x04DDE7E0      8B
  Limit_shop_configXml                                  0x04DDEEB8      8B
  Limit_shop_configXml                                  0x04DDEEC0      8B
  LoadingimageXml                                       0x04DE0194      8B
  LoadingimageXml                                       0x04DE019C      8B
  Loop_boss_baseXml                                     0x04DE1D7C      8B
  Loop_boss_baseXml                                     0x04DE1D84      8B
  Loop_boss_monsterXml                                  0x04DE343C      8B
  Loop_boss_monsterXml                                  0x04DE3444      8B
  Loop_boss_target_typeXml                              0x04DE48B0      8B
  Loop_boss_target_typeXml                              0x04DE48B8      8B
  Loop_boss_target_typeXml                              0x04DE4F38      8B
  Loop_boss_target_typeXml                              0x04DE4F40      8B
  Lord_Att_FilterXml                                    0x04DE64DC      8B
  Lord_Att_FilterXml                                    0x04DE64E4      8B
  Lord_DressupXml                                       0x04DE7280      8B
  Lord_DressupXml                                       0x04DE7288      8B
  Lord_catchXml                                         0x04DE7F90      8B
  Lord_catchXml                                         0x04DE7F98      8B
  Lord_effectXml                                        0x04DE8D34      8B
  Lord_effectXml                                        0x04DE8D3C      8B
  Lord_equipXml                                         0x04DEA4D0      8B
  Lord_equipXml                                         0x04DEA4D8      8B
  Lord_equip_ment_suitXml                               0x04DEB880      8B
  Lord_equip_ment_suitXml                               0x04DEB888      8B
  Lord_equip_ment_suitXml                               0x04DEBF38      8B
  Lord_equip_ment_suitXml                               0x04DEBF40      8B
  Lord_gemXml                                           0x04DED6C4      8B
  Lord_gemXml                                           0x04DED6CC      8B
  Lord_gem_unlockXml                                    0x04DEE734      8B
  Lord_gem_unlockXml                                    0x04DEE73C      8B
  Lord_gem_unlockXml                                    0x04DEED90      8B
  Lord_gem_unlockXml                                    0x04DEED98      8B
  Lord_gem_upgradeXml                                   0x04DF0218      8B
  Lord_gem_upgradeXml                                   0x04DF0220      8B
  Lord_gem_upgradeXml                                   0x04DF08F8      8B
  Lord_gem_upgradeXml                                   0x04DF0900      8B
  Lord_grow_lvXml                                       0x04DF22D4      8B
  Lord_grow_lvXml                                       0x04DF22DC      8B
  Lord_grow_lvXml                                       0x04DF29DC      8B
  Lord_grow_lvXml                                       0x04DF29E4      8B
  Lord_grow_typeXml                                     0x04DF4104      8B
  Lord_grow_typeXml                                     0x04DF410C      8B
  Lord_level_growXml                                    0x04DF4EF8      8B
  Lord_level_growXml                                    0x04DF4F00      8B
  Lord_materialXml                                      0x04DF5EDC      8B
  Lord_materialXml                                      0x04DF5EE4      8B
  Lord_material_typeXml                                 0x04DF6CCC      8B
  Lord_material_typeXml                                 0x04DF6CD4      8B
  Lord_orderXml                                         0x033D6B68      8B
  Lord_orderXml                                         0x033D6B70      8B
  Lord_partsXml                                         0x04DF7A24      8B
  Lord_partsXml                                         0x04DF7A2C      8B
  Lord_skillXml                                         0x04DF9390      8B
  Lord_skillXml                                         0x04DF9398      8B
  Lord_skillXml                                         0x04DF9ACC      8B
  Lord_skillXml                                         0x04DF9AD4      8B
  Lord_war_eventXml                                     0x04DFB624      8B
  Lord_war_eventXml                                     0x04DFB62C      8B
  Lord_war_event_buffXml                                0x04DFC43C      8B
  Lord_war_event_buffXml                                0x04DFC444      8B
  Lord_war_event_cityXml                                0x04DFD710      8B
  Lord_war_event_cityXml                                0x04DFD718      8B
  Lord_war_event_league_rewardXml                       0x04DFEAFC      8B
  Lord_war_event_league_rewardXml                       0x04DFEB04      8B
  Lord_war_event_league_rewardXml                       0x04DFF204      8B
  Lord_war_event_league_rewardXml                       0x04DFF20C      8B
  Lord_war_event_lord_rewardXml                         0x04E00894      8B
  Lord_war_event_lord_rewardXml                         0x04E0089C      8B
  Lord_war_event_rewardXml                              0x04E01B18      8B
  Lord_war_event_rewardXml                              0x04E01B20      8B
  Lord_war_event_scoreXml                               0x04E02C24      8B
  Lord_war_event_scoreXml                               0x04E02C2C      8B
  Lord_war_event_scoreXml                               0x04E032FC      8B
  Lord_war_event_scoreXml                               0x04E03304      8B
  Lord_war_targetXml                                    0x04E0443C      8B
  Lord_war_targetXml                                    0x04E04444      8B
  Lost_achievementXml                                   0x04E05C0C      8B
  Lost_achievementXml                                   0x04E05C14      8B
  Lost_achievementXml                                   0x04E06350      8B
  Lost_achievementXml                                   0x04E06358      8B
  Lost_activity_switchXml                               0x04E07840      8B
  Lost_activity_switchXml                               0x04E07848      8B
  Lost_alliance_buffXml                                 0x04E0893C      8B
  Lost_alliance_buffXml                                 0x04E08944      8B
  Lost_alliance_buildXml                                0x04E098B8      8B
  Lost_alliance_buildXml                                0x04E098C0      8B
  Lost_alliance_iconXml                                 0x04E0A974      8B
  Lost_alliance_iconXml                                 0x04E0A97C      8B
  Lost_alliance_iconXml                                 0x04E0B06C      8B
  Lost_alliance_iconXml                                 0x04E0B074      8B
  Lost_alliance_territoryXml                            0x04E0C374      8B
  Lost_alliance_territoryXml                            0x04E0C37C      8B
  Lost_altar_baseXml                                    0x04E0D420      8B
  Lost_altar_baseXml                                    0x04E0D428      8B
  Lost_altar_baseXml                                    0x04E0DB00      8B
  Lost_altar_baseXml                                    0x04E0DB08      8B
  Lost_areaXml                                          0x04E0F818      8B
  Lost_areaXml                                          0x04E0F820      8B
  Lost_areaXml                                          0x04E0FF5C      8B
  Lost_areaXml                                          0x04E0FF64      8B
  Lost_ban_heroXml                                      0x04E1113C      8B
  Lost_ban_heroXml                                      0x04E11144      8B
  Lost_campXml                                          0x04E11EA8      8B
  Lost_campXml                                          0x04E11EB0      8B
  Lost_crystal_genXml                                   0x04E1304C      8B
  Lost_crystal_genXml                                   0x04E13054      8B
  Lost_crystal_genXml                                   0x04E1372C      8B
  Lost_crystal_genXml                                   0x04E13734      8B
  Lost_daily_baseXml                                    0x04E14A1C      8B
  Lost_daily_baseXml                                    0x04E14A24      8B
  Lost_daily_taskXml                                    0x04E160F0      8B
  Lost_daily_taskXml                                    0x04E160F8      8B
  Lost_daily_taskXml                                    0x04E16824      8B
  Lost_daily_taskXml                                    0x04E1682C      8B
  Lost_dominionXml                                      0x04E18950      8B
  Lost_dominionXml                                      0x04E18958      8B
  Lost_dominion_npcXml                                  0x04E1A008      8B
  Lost_dominion_npcXml                                  0x04E1A010      8B
  Lost_dominion_stateXml                                0x04E1B0C4      8B
  Lost_dominion_stateXml                                0x04E1B0CC      8B
  Lost_dominion_stateXml                                0x04E1B708      8B
  Lost_dominion_stateXml                                0x04E1B710      8B
  Lost_dominion_terrainXml                              0x04E1CE00      8B
  Lost_dominion_terrainXml                              0x04E1CE08      8B
  Lost_era_taskXml                                      0x04E1E3E8      8B
  Lost_era_taskXml                                      0x04E1E3F0      8B
  Lost_era_task_unlockXml                               0x04E1F2B4      8B
  Lost_era_task_unlockXml                               0x04E1F2BC      8B
  Lost_event_descXml                                    0x04E202B4      8B
  Lost_event_descXml                                    0x04E202BC      8B
  Lost_event_descXml                                    0x04E208DC      8B
  Lost_event_descXml                                    0x04E208E4      8B
  Lost_event_pre_phase2Xml                              0x04E21AD4      8B
  Lost_event_pre_phase2Xml                              0x04E21ADC      8B
  Lost_event_pre_phase3Xml                              0x04E2288C      8B
  Lost_event_pre_phase3Xml                              0x04E22894      8B
  Lost_event_pre_rewardXml                              0x04E23EE0      8B
  Lost_event_pre_rewardXml                              0x04E23EE8      8B
  Lost_event_pre_reward_soloXml                         0x04E251C0      8B
  Lost_event_pre_reward_soloXml                         0x04E251C8      8B
  Lost_event_rewardXml                                  0x04E26668      8B
  Lost_event_rewardXml                                  0x04E26670      8B
  Lost_event_rewardXml                                  0x04E26CEC      8B
  Lost_event_rewardXml                                  0x04E26CF4      8B
  Lost_event_scoreXml                                   0x04E28248      8B
  Lost_event_scoreXml                                   0x04E28250      8B
  Lost_event_scoreXml                                   0x04E28928      8B
  Lost_event_scoreXml                                   0x04E28930      8B
  Lost_globalXml                                        0x04E2BF10      8B
  Lost_globalXml                                        0x04E2BF18      8B
  Lost_imperial_baseXml                                 0x04E2CE30      8B
  Lost_imperial_baseXml                                 0x04E2CE38      8B
  Lost_imperial_taskXml                                 0x04E2E178      8B
  Lost_imperial_taskXml                                 0x04E2E180      8B
  Lost_month_cardXml                                    0x04E2F6B8      8B
  Lost_month_cardXml                                    0x04E2F6C0      8B
  Lost_refreshXml                                       0x04E3078C      8B
  Lost_refreshXml                                       0x04E30794      8B
  Lost_refreshXml                                       0x04E30E6C      8B
  Lost_refreshXml                                       0x04E30E74      8B
  Lost_rush_eventXml                                    0x04E32778      8B
  Lost_rush_eventXml                                    0x04E32780      8B
  Lost_rush_event_rankXml                               0x04E33D54      8B
  Lost_rush_event_rankXml                               0x04E33D5C      8B
  Lost_rush_event_rankXml                               0x04E343D8      8B
  Lost_rush_event_rankXml                               0x04E343E0      8B
  Lost_rush_event_rewardXml                             0x04E35C70      8B
  Lost_rush_event_rewardXml                             0x04E35C78      8B
  Lost_rush_event_rewardXml                             0x04E36378      8B
  Lost_rush_event_rewardXml                             0x04E36380      8B
  Lost_rush_event_scoreXml                              0x04E379E8      8B
  Lost_rush_event_scoreXml                              0x04E379F0      8B
  Lucky_giftXml                                         0x04E38904      8B
  Lucky_giftXml                                         0x04E3890C      8B
  Lucky_lineXml                                         0x04E3A744      8B
  Lucky_lineXml                                         0x04E3A74C      8B
  Lucky_lineXml                                         0x04E3AF30      8B
  Lucky_lineXml                                         0x04E3AF38      8B
  Lucky_shopXml                                         0x04E3C4D4      8B
  Lucky_shopXml                                         0x04E3C4DC      8B
  Lucky_shop_baseXml                                    0x04E3D63C      8B
  Lucky_shop_baseXml                                    0x04E3D644      8B
  Lucky_shop_baseXml                                    0x04E3DD10      8B
  Lucky_shop_baseXml                                    0x04E3DD18      8B
  Lucky_shop_newXml                                     0x04E3F540      8B
  Lucky_shop_newXml                                     0x04E3F548      8B
  Lucky_shop_newXml                                     0x04E3FC48      8B
  Lucky_shop_newXml                                     0x04E3FC50      8B
  LuckypotXml                                           0x04E41320      8B
  LuckypotXml                                           0x04E41328      8B
  Luckypot_latticeXml                                   0x04E424C4      8B
  Luckypot_latticeXml                                   0x04E424CC      8B
  Luckypot_latticeXml                                   0x04E42BA4      8B
  Luckypot_latticeXml                                   0x04E42BAC      8B
  Luckystar_groupXml                                    0x04E43F4C      8B
  Luckystar_groupXml                                    0x04E43F54      8B
  Luna_shopXml                                          0x04E45320      8B
  Luna_shopXml                                          0x04E45328      8B
  Luna_shop_configXml                                   0x04E468AC      8B
  Luna_shop_configXml                                   0x04E468B4      8B
  Luna_shop_configXml                                   0x04E46FB4      8B
  Luna_shop_configXml                                   0x04E46FBC      8B
  Luna_shop_lucky_giftXml                               0x04E488E4      8B
  Luna_shop_lucky_giftXml                               0x04E488EC      8B
  Luna_shop_lucky_giftXml                               0x04E48F68      8B
  Luna_shop_lucky_giftXml                               0x04E48F70      8B
  Luxury_rewardXml                                      0x04E4A50C      8B
  Luxury_rewardXml                                      0x04E4A514      8B
  MagicLamp_treasure_baseXml                            0x04E4B778      8B
  MagicLamp_treasure_baseXml                            0x04E4B780      8B
  MagicLamp_treasure_rewardXml                          0x04E4CAA0      8B
  MagicLamp_treasure_rewardXml                          0x04E4CAA8      8B
  MagicLamp_treasure_scoreXml                           0x04E4D8F8      8B
  MagicLamp_treasure_scoreXml                           0x04E4D900      8B
  Mail_monitorXml                                       0x04E4E8AC      8B
  Mail_monitorXml                                       0x04E4E8B4      8B
  Mail_monitorXml                                       0x04E4EF90      8B
  Mail_monitorXml                                       0x04E4EF98      8B
  Map_blockXml                                          0x04E5010C      8B
  Map_blockXml                                          0x04E50114      8B
  Map_chat_channelXml                                   0x04E511E4      8B
  Map_chat_channelXml                                   0x04E511EC      8B
  Map_hide_blockXml                                     0x04E52AFC      8B
  Map_hide_blockXml                                     0x04E52B04      8B
  Map_hide_blockXml                                     0x04E52FE0      8B
  Map_hide_blockXml                                     0x04E52FE8      8B
  Match_rulesXml                                        0x04E545A0      8B
  Match_rulesXml                                        0x04E545A8      8B
  Medal_systemXml                                       0x04E55898      8B
  Medal_systemXml                                       0x04E558A0      8B
  Medal_systemXml                                       0x04E55F20      8B
  Medal_systemXml                                       0x04E55F28      8B
  Merge_baseXml                                         0x04E57B10      8B
  Merge_baseXml                                         0x04E57B18      8B
  Merge_eventXml                                        0x04E593F0      8B
  Merge_eventXml                                        0x04E593F8      8B
  Merge_itemXml                                         0x04E5A214      8B
  Merge_itemXml                                         0x04E5A21C      8B
  Merge_newXml                                          0x04E5B388      8B
  Merge_newXml                                          0x04E5B390      8B
  Merge_psXml                                           0x04E5CB68      8B
  Merge_psXml                                           0x04E5CB70      8B
  Merge_rankXml                                         0x04E5DEC0      8B
  Merge_rankXml                                         0x04E5DEC8      8B
  Merge_rewardXml                                       0x04E5F0C0      8B
  Merge_rewardXml                                       0x04E5F0C8      8B
  Merge_scroeXml                                        0x04E5FEE0      8B
  Merge_scroeXml                                        0x04E5FEE8      8B
  Mini_game_sheepXml                                    0x04E6158C      8B
  Mini_game_sheepXml                                    0x04E61594      8B
  Mini_game_sheepXml                                    0x04E61D2C      8B
  Mini_game_sheepXml                                    0x04E61D34      8B
  Move_server_timeXml                                   0x04E62E78      8B
  Move_server_timeXml                                   0x04E62E80      8B
  Name_randomXml                                        0x04E63F04      8B
  Name_randomXml                                        0x04E63F0C      8B
  Name_randomXml                                        0x04E6460C      8B
  Name_randomXml                                        0x04E64614      8B
  Nameplate_skinXml                                     0x04E661DC      8B
  Nameplate_skinXml                                     0x04E661E4      8B
  Nameplate_skinXml                                     0x04E66954      8B
  Nameplate_skinXml                                     0x04E6695C      8B
  NavigationXml                                         0x04E67A9C      8B
  NavigationXml                                         0x04E67AA4      8B
  Navigation_baseXml                                    0x04E6A3CC      8B
  Navigation_baseXml                                    0x04E6A3D4      8B
  Navigation_baseXml                                    0x04E6AAFC      8B
  Navigation_baseXml                                    0x04E6AB04      8B
  Navigation_event_taskXml                              0x04E6C474      8B
  Navigation_event_taskXml                              0x04E6C47C      8B
  Navigation_lvXml                                      0x04E6DE04      8B
  Navigation_lvXml                                      0x04E6DE0C      8B
  Navigation_rank_rewardXml                             0x04E6EFBC      8B
  Navigation_rank_rewardXml                             0x04E6EFC4      8B
  NewsXml                                               0x04E701B0      8B
  NewsXml                                               0x04E701B8      8B
  NewsXml                                               0x04E708E4      8B
  NewsXml                                               0x04E708EC      8B
  Noble_lvXml                                           0x04E72070      8B
  Noble_lvXml                                           0x04E72078      8B
  Noble_shopXml                                         0x04E73130      8B
  Noble_shopXml                                         0x04E73138      8B
  Noble_stateXml                                        0x04E74094      8B
  Noble_stateXml                                        0x04E7409C      8B
  Novice_free_purchaseXml                               0x04E75940      8B
  Novice_free_purchaseXml                               0x04E75948      8B
  Novice_free_purchaseXml                               0x04E75F68      8B
  Novice_free_purchaseXml                               0x04E75F70      8B
  Novice_map_buildingsXml                               0x04E77554      8B
  Novice_map_buildingsXml                               0x04E7755C      8B
  Novice_map_marchXml                                   0x04E784C4      8B
  Novice_map_marchXml                                   0x04E784CC      8B
  Novice_map_monsterXml                                 0x04E794AC      8B
  Novice_map_monsterXml                                 0x04E794B4      8B
  Novice_map_sceneXml                                   0x04E7A220      8B
  Novice_map_sceneXml                                   0x04E7A228      8B
  Novice_rewardXml                                      0x04E7B598      8B
  Novice_rewardXml                                      0x04E7B5A0      8B
  Novice_rewardXml                                      0x04E7BBD0      8B
  Novice_rewardXml                                      0x04E7BBD8      8B
  Novice_world_trendXml                                 0x04E7CE84      8B
  Novice_world_trendXml                                 0x04E7CE8C      8B
  Npc_askXml                                            0x04E7DC38      8B
  Npc_askXml                                            0x04E7DC40      8B
  Npc_diaXml                                            0x04E7EA10      8B
  Npc_diaXml                                            0x04E7EA18      8B
  OnlineXml                                             0x04E80240      8B
  OnlineXml                                             0x04E80248      8B
  OnlineXml                                             0x04E80938      8B
  OnlineXml                                             0x04E80940      8B
  Open_sesameXml                                        0x04E827C4      8B
  Open_sesameXml                                        0x04E827CC      8B
  Open_sesameXml                                        0x04E82EF8      8B
  Open_sesameXml                                        0x04E82F00      8B
  Open_sesame_buffXml                                   0x04E8434C      8B
  Open_sesame_buffXml                                   0x04E84354      8B
  Open_sesame_buffXml                                   0x04E84A2C      8B
  Open_sesame_buffXml                                   0x04E84A34      8B
  Open_sesame_buff_clientXml                            0x04E85CB4      8B
  Open_sesame_buff_clientXml                            0x04E85CBC      8B
  Open_sesame_enemyXml                                  0x04E87368      8B
  Open_sesame_enemyXml                                  0x04E87370      8B
  Open_sesame_eventXml                                  0x04E89678      8B
  Open_sesame_eventXml                                  0x04E89680      8B
  Open_sesame_goodsXml                                  0x04E8A4D0      8B
  Open_sesame_goodsXml                                  0x04E8A4D8      8B
  Open_sesame_heroXml                                   0x04E8BC44      8B
  Open_sesame_heroXml                                   0x04E8BC4C      8B
  Open_sesame_heroXml                                   0x04E8C34C      8B
  Open_sesame_heroXml                                   0x04E8C354      8B
  Open_sesame_layerXml                                  0x04E8DBA8      8B
  Open_sesame_layerXml                                  0x04E8DBB0      8B
  Open_sesame_layerXml                                  0x04E8E2B0      8B
  Open_sesame_layerXml                                  0x04E8E2B8      8B
  Open_sesame_npcXml                                    0x04E8FCA4      8B
  Open_sesame_npcXml                                    0x04E8FCAC      8B
  Open_sesame_npcXml                                    0x04E90404      8B
  Open_sesame_npcXml                                    0x04E9040C      8B
  Open_sesame_random_enemyXml                           0x04E91898      8B
  Open_sesame_random_enemyXml                           0x04E918A0      8B
  Open_sesame_random_enemyXml                           0x04E91F78      8B
  Open_sesame_random_enemyXml                           0x04E91F80      8B
  Open_sesame_random_eventXml                           0x04E93448      8B
  Open_sesame_random_eventXml                           0x04E93450      8B
  Open_sesame_random_eventXml                           0x04E93AA4      8B
  Open_sesame_random_eventXml                           0x04E93AAC      8B
  Open_sesame_random_goodsXml                           0x04E94F38      8B
  Open_sesame_random_goodsXml                           0x04E94F40      8B
  Open_sesame_random_goodsXml                           0x04E95594      8B
  Open_sesame_random_goodsXml                           0x04E9559C      8B
  Open_sesame_random_heroXml                            0x04E96A30      8B
  Open_sesame_random_heroXml                            0x04E96A38      8B
  Open_sesame_random_heroXml                            0x04E97110      8B
  Open_sesame_random_heroXml                            0x04E97118      8B
  Open_sesame_random_npcXml                             0x04E985AC      8B
  Open_sesame_random_npcXml                             0x04E985B4      8B
  Open_sesame_random_npcXml                             0x04E98C8C      8B
  Open_sesame_random_npcXml                             0x04E98C94      8B
  Open_sesame_reward_modelXml                           0x04E9A4BC      8B
  Open_sesame_reward_modelXml                           0x04E9A4C4      8B
  Open_sesame_reward_modelXml                           0x04E9AB34      8B
  Open_sesame_reward_modelXml                           0x04E9AB3C      8B
  Open_sesame_wheelXml                                  0x04E9C234      8B
  Open_sesame_wheelXml                                  0x04E9C23C      8B
  Open_sesame_wheelXml                                  0x04E9C914      8B
  Open_sesame_wheelXml                                  0x04E9C91C      8B
  Operation_actionXml                                   0x04E9DED0      8B
  Operation_actionXml                                   0x04E9DED8      8B
  Operation_markXml                                     0x04E9F2A0      8B
  Operation_markXml                                     0x04E9F2A8      8B
  Operation_markXml                                     0x04E9F9A8      8B
  Operation_markXml                                     0x04E9F9B0      8B
  Operation_pointXml                                    0x04EA0E90      8B
  Operation_pointXml                                    0x04EA0E98      8B
  Operation_pointXml                                    0x04EA14E0      8B
  Operation_pointXml                                    0x04EA14E8      8B
  Operation_rankXml                                     0x04EA2E38      8B
  Operation_rankXml                                     0x04EA2E40      8B
  Operation_rankXml                                     0x04EA3540      8B
  Operation_rankXml                                     0x04EA3548      8B
  Other_activityXml                                     0x04EA4C5C      8B
  Other_activityXml                                     0x04EA4C64      8B
  Pet_baseXml                                           0x04EA5CE4      8B
  Pet_baseXml                                           0x04EA5CEC      8B
  Pet_feed_goldXml                                      0x04EA6A84      8B
  Pet_feed_goldXml                                      0x04EA6A8C      8B
  Pet_libraryXml                                        0x04EA80C0      8B
  Pet_libraryXml                                        0x04EA80C8      8B
  Pet_lvXml                                             0x04EA90CC      8B
  Pet_lvXml                                             0x04EA90D4      8B
  Pet_shoot_baseXml                                     0x04EAC4F4      8B
  Pet_shoot_baseXml                                     0x04EAC4FC      8B
  Pet_shoot_baseXml                                     0x04EACDE0      8B
  Pet_shoot_baseXml                                     0x04EACDE8      8B
  Pet_shoot_rankXml                                     0x04EAE550      8B
  Pet_shoot_rankXml                                     0x04EAE558      8B
  Pet_skill_upgradeXml                                  0x04EB0134      8B
  Pet_skill_upgradeXml                                  0x04EB013C      8B
  Pet_skill_upgradeXml                                  0x04EB0960      8B
  Pet_skill_upgradeXml                                  0x04EB0968      8B
  Pet_sourceXml                                         0x04EB1E68      8B
  Pet_sourceXml                                         0x04EB1E70      8B
  PinBallMaterialXml                                    0x04EB2C0C      8B
  PinBallMaterialXml                                    0x04EB2C14      8B
  PinBallRecordXml                                      0x04EB4108      8B
  PinBallRecordXml                                      0x04EB4110      8B
  Place_itemXml                                         0x04EB4FDC      8B
  Place_itemXml                                         0x04EB4FE4      8B
  PlacementXml                                          0x04EB5ED0      8B
  PlacementXml                                          0x04EB5ED8      8B
  Play_previewXml                                       0x04EB7390      8B
  Play_previewXml                                       0x04EB7398      8B
  Play_previewXml                                       0x04EB7A54      8B
  Play_previewXml                                       0x04EB7A5C      8B
  PlayerDefault                                         0x0373F00C    332B
  Player_limitXml                                       0x04EB8BD8      8B
  Player_limitXml                                       0x04EB8BE0      8B
  Plot_quest_correspondXml                              0x04EB990C      8B
  Plot_quest_correspondXml                              0x04EB9914      8B
  Plot_quest_newXml                                     0x04EBB5B4      8B
  Plot_quest_newXml                                     0x04EBB5BC      8B
  Plot_quest_newXml                                     0x04EBBDA0      8B
  Plot_quest_newXml                                     0x04EBBDA8      8B
  PlotsXml                                              0x04EBD244      8B
  PlotsXml                                              0x04EBD24C      8B
  Point_baseXml                                         0x04EBDF44      8B
  Point_baseXml                                         0x04EBDF4C      8B
  Point_shopXml                                         0x04EBED54      8B
  Point_shopXml                                         0x04EBED5C      8B
  Points_biddingXml                                     0x04EBFE0C      8B
  Points_biddingXml                                     0x04EBFE14      8B
  Points_bidding_itemXml                                0x04EC105C      8B
  Points_bidding_itemXml                                0x04EC1064      8B
  Points_bidding_itemXml                                0x04EC173C      8B
  Points_bidding_itemXml                                0x04EC1744      8B
  Power_tasksXml                                        0x04EC3D24      8B
  Power_tasksXml                                        0x04EC3D2C      8B
  Power_tasksXml                                        0x04EC456C      8B
  Power_tasksXml                                        0x04EC4574      8B
  Power_upXml                                           0x04EC58F8      8B
  Power_upXml                                           0x04EC5900      8B
  Power_up_partXml                                      0x04EC6750      8B
  Power_up_partXml                                      0x04EC6758      8B
  PrevImageXml                                          0x04EC7564      8B
  PrevImageXml                                          0x04EC756C      8B
  PrivilegeXml                                          0x04EC8608      8B
  PrivilegeXml                                          0x04EC8610      8B
  Product_showcase_eventXml                             0x04EC9898      8B
  Product_showcase_eventXml                             0x04EC98A0      8B
  Product_showcase_loginXml                             0x04ECAFC0      8B
  Product_showcase_loginXml                             0x04ECAFC8      8B
  Product_showcase_loginXml                             0x04ECB7A0      8B
  Product_showcase_loginXml                             0x04ECB7A8      8B
  PveXml                                                0x04ECECA4      8B
  PveXml                                                0x04ECECAC      8B
  PveXml                                                0x04ECF508      8B
  PveXml                                                0x04ECF510      8B
  Pve_power_upXml                                       0x04ED06A8      8B
  Pve_power_upXml                                       0x04ED06B0      8B
  Quantity_taskXml                                      0x04ED17D4      8B
  Quantity_taskXml                                      0x04ED17DC      8B
  Quantity_taskXml                                      0x04ED1E4C      8B
  Quantity_taskXml                                      0x04ED1E54      8B
  RD7getDataEPKc                                        0xA0500000C0004000 3098476544201326604B
  RETURN7getDataEPKc                                    0x440A00004407 74826920248332B
  RIBUTE_CHANGE7getDataEPKc                             0xD90E000072EF      0B
  RN7getDataEPKc                                        0x240DE00006C31 377712309054240B
  Rank_worshipXml                                       0x04ED30A4      8B
  Rank_worshipXml                                       0x04ED30AC      8B
  RebelsXml                                             0x04ED3F88      8B
  RebelsXml                                             0x04ED3F90      8B
  Rebuilding_oasiseXml                                  0x04ED5874      8B
  Rebuilding_oasiseXml                                  0x04ED587C      8B
  Rebuilding_oasiseXml                                  0x04ED5FE0      8B
  Rebuilding_oasiseXml                                  0x04ED5FE8      8B
  Rebuilding_oasise_taskXml                             0x04ED7770      8B
  Rebuilding_oasise_taskXml                             0x04ED7778      8B
  Recharge_accumulation_rewardXml                       0x04ED9654      8B
  Recharge_accumulation_rewardXml                       0x04ED965C      8B
  Recharge_accumulation_rewardXml                       0x04ED9DE8      8B
  Recharge_accumulation_rewardXml                       0x04ED9DF0      8B
  Recharge_pointXml                                     0x04EDABA8      8B
  Recharge_pointXml                                     0x04EDABB0      8B
  Recharge_rewardXml                                    0x04EDC10C      8B
  Recharge_rewardXml                                    0x04EDC114      8B
  Record_cost_group_baseXml                             0x04EDD2A4      8B
  Record_cost_group_baseXml                             0x04EDD2AC      8B
  Record_cost_group_configXml                           0x04EDE774      8B
  Record_cost_group_configXml                           0x04EDE77C      8B
  Record_cost_group_configXml                           0x04EDEEC4      8B
  Record_cost_group_configXml                           0x04EDEECC      8B
  Recycle_itemXml                                       0x04EE02BC      8B
  Recycle_itemXml                                       0x04EE02C4      8B
  Red_envelopes_autoXml                                 0x04EE1ED0      8B
  Red_envelopes_autoXml                                 0x04EE1ED8      8B
  Red_envelopes_autoXml                                 0x04EE2744      8B
  Red_envelopes_autoXml                                 0x04EE274C      8B
  Red_envelopes_itemXml                                 0x04EE4754      8B
  Red_envelopes_itemXml                                 0x04EE475C      8B
  Red_envelopes_itemXml                                 0x04EE4F40      8B
  Red_envelopes_itemXml                                 0x04EE4F48      8B
  Red_envelopes_limitXml                                0x04EE6124      8B
  Red_envelopes_limitXml                                0x04EE612C      8B
  Red_envelopes_mergeXml                                0x04EE7734      8B
  Red_envelopes_mergeXml                                0x04EE773C      8B
  Red_envelopes_personalXml                             0x04EE8CB4      8B
  Red_envelopes_personalXml                             0x04EE8CBC      8B
  Red_envelopes_personalXml                             0x04EE9494      8B
  Red_envelopes_personalXml                             0x04EE949C      8B
  Red_envelopes_rewardXml                               0x04EEA9A0      8B
  Red_envelopes_rewardXml                               0x04EEA9A8      8B
  Red_envelopes_rewardXml                               0x04EEAFFC      8B
  Red_envelopes_rewardXml                               0x04EEB004      8B
  Red_envelopes_weekactivityXml                         0x04EED060      8B
  Red_envelopes_weekactivityXml                         0x04EED068      8B
  Red_envelopes_weekactivityXml                         0x04EED860      8B
  Red_envelopes_weekactivityXml                         0x04EED868      8B
  Reduce_price_baseXml                                  0x04EEEF60      8B
  Reduce_price_baseXml                                  0x04EEEF68      8B
  Reduce_price_giftXml                                  0x04EF0690      8B
  Reduce_price_giftXml                                  0x04EF0698      8B
  Reduce_price_giftXml                                  0x04EF0D38      8B
  Reduce_price_giftXml                                  0x04EF0D40      8B
  Reduce_price_help_planXml                             0x04EF27E8      8B
  Reduce_price_help_planXml                             0x04EF27F0      8B
  Reduce_price_help_planXml                             0x04EF2E44      8B
  Reduce_price_help_planXml                             0x04EF2E4C      8B
  Reduce_price_help_rewardXml                           0x04EF407C      8B
  Reduce_price_help_rewardXml                           0x04EF4084      8B
  Reduce_price_shopXml                                  0x04EF51AC      8B
  Reduce_price_shopXml                                  0x04EF51B4      8B
  Reduce_price_shopXml                                  0x04EF588C      8B
  Reduce_price_shopXml                                  0x04EF5894      8B
  Retrieve_baseXml                                      0x04EF6ACC      8B
  Retrieve_baseXml                                      0x04EF6AD4      8B
  Return_eventXml                                       0x04EF8268      8B
  Return_eventXml                                       0x04EF8270      8B
  Return_event_baseXml                                  0x04EF9FAC      8B
  Return_event_baseXml                                  0x04EF9FB4      8B
  Return_event_baseXml                                  0x04EFA7D4      8B
  Return_event_baseXml                                  0x04EFA7DC      8B
  Return_event_packXml                                  0x04EFBDA4      8B
  Return_event_packXml                                  0x04EFBDAC      8B
  Return_event_payXml                                   0x04EFD808      8B
  Return_event_payXml                                   0x04EFD810      8B
  Return_event_payXml                                   0x04EFDE74      8B
  Return_event_payXml                                   0x04EFDE7C      8B
  Return_event_pay_groupXml                             0x04EFF574      8B
  Return_event_pay_groupXml                             0x04EFF57C      8B
  Return_event_pay_groupXml                             0x04EFFAC8      8B
  Return_event_pay_groupXml                             0x04EFFAD0      8B
  Return_event_sign_inXml                               0x04F0175C      8B
  Return_event_sign_inXml                               0x04F01764      8B
  Return_event_sign_inXml                               0x04F01E64      8B
  Return_event_sign_inXml                               0x04F01E6C      8B
  Ruins_search_baseXml                                  0x04F03E5C      8B
  Ruins_search_baseXml                                  0x04F03E64      8B
  Ruins_search_groupXml                                 0x04F053A8      8B
  Ruins_search_groupXml                                 0x04F053B0      8B
  Ruins_search_groupXml                                 0x04F05C2C      8B
  Ruins_search_groupXml                                 0x04F05C34      8B
  Rush_eventXml                                         0x04F07004      8B
  Rush_eventXml                                         0x04F0700C      8B
  Rush_event_rewardXml                                  0x04F0855C      8B
  Rush_event_rewardXml                                  0x04F08564      8B
  Rush_event_rewardXml                                  0x04F08BE0      8B
  Rush_event_rewardXml                                  0x04F08BE8      8B
  Rush_event_scoreXml                                   0x04F0A0B0      8B
  Rush_event_scoreXml                                   0x04F0A0B8      8B
  SG_CHARGE_INFO7getDataEPKc                            0x00024935 50092203601213B
  SG_HERO_INFO7getDataEPKc                              0x0000AD0E      0B
  SMG_SYNC_AS_HEARTBEAT                                 0x05253410     88B
  SMSG_ABANDON_KING_CHESS_REQUEST                       0x050D7CE8    104B
  SMSG_ACCELERATE_MARCH_CHECK_REQUEST                   0x0522EF74    812B
  SMSG_ACCELERATE_MARCH_CHECK_RETURN                    0x0522F5D4    812B
  SMSG_ACC_INVESTIGATION                                0x05229314    104B
  SMSG_ACTIVITY_BUILDING_BUILDING                       0x05188498   1524B
  SMSG_ACTIVITY_BUILDING_BUILDING_RETURN                0x0518911C   1652B
  SMSG_ACTIVITY_BUILDING_INFO                           0x05187410     88B
  SMSG_ACTIVITY_BUILDING_INFO_RETURN                    0x051878F8   1140B
  SMSG_ACTIVITY_GAIN_SERVER_REQUEST                     0x05184A8C     72B
  SMSG_ACTIVITY_GAIN_SERVER_RETURN                      0x05184BBC     72B
  SMSG_ACTIVITY_LOOP_BOSS_INFO                          0x0518465C     88B
  SMSG_ACTIVITY_LOOP_BOSS_INFO_RETURN                   0x051847D4     88B
  SMSG_ACTIVITY_LOOP_BOSS_KILL                          0x0518494C     88B
  SMSG_ACTIVITY_LOOP_SEARCH_INFO                        0x0518AAA8     88B
  SMSG_ACTIVITY_LOOP_SEARCH_INFO_RETURN                 0x0518AC20     88B
  SMSG_ACTIVITY_LOOP_SEARCH_UPDATE                      0x0518AD98     88B
  SMSG_ACTIVITY_REWARD_INFO_REQUEST                     0x05184D5C    104B
  SMSG_ACTIVITY_REWARD_INFO_RETURN                      0x05184F7C    120B
  SMSG_ACTIVITY_RUSH_EVENT_RANK_REQUEST                 0x04FA5EAC    104B
  SMSG_ACTIVITY_RUSH_EVENT_RANK_RETURN                  0x04FA63B8   1256B
  SMSG_ACTIVITY_RUSH_EVENT_REQUEST                      0x04FA5B30    104B
  SMSG_ACTIVITY_RUSH_EVENT_RETURN                       0x04FA5CEC    104B
  SMSG_ACTIVITY_RUSH_EVENT_SYNC_MARK                    0x04FA6BD8    564B
  SMSG_ACTIVITY_STAGE_CHANGE                            0x05141DBC   1980B
  SMSG_ADD_AllFORONE_ACTION_TIMES                       0x04FAC070     56B
  SMSG_ADD_BUILDUP_BATTLE                               0x05221808    312B
  SMSG_ADD_BUILDUP_BATTLE_KING_CHESS                    0x050D39FC    312B
  SMSG_ADD_CAMEL                                        0x05055704    168B
  SMSG_ADD_COLLECT_PLAYER                               0x05160FC8    168B
  SMSG_ADD_COLLECT_RESOURCE                             0x0510D290    248B
  SMSG_ADD_DEFEND                                       0x0510C838    136B
  SMSG_ADD_KINGDOM_ACTION_SERVER_VALUE                  0x050DFA64     88B
  SMSG_ADD_LEAGUEBUILD                                  0x0515EFBC   1176B
  SMSG_ADD_LEAGUE_BIG_BOSS                              0x051564D4    136B
  SMSG_ADD_LEAGUE_BOSS                                  0x051560D4    556B
  SMSG_ADD_NEWS_INFO                                    0x0525DBD4    392B
  SMSG_ADD_NORMAL_BATTLE                                0x05221CA8    264B
  SMSG_ADD_PENDING_DEFEND                               0x0510CC70    168B
  SMSG_ADD_PLACEMENT                                    0x0522521C    136B
  SMSG_ADD_SECRET_TASK                                  0x052C048C    216B
  SMSG_ADD_STATION                                      0x0510D740    152B
  SMSG_AGENT_VIEW_HEARTBEAT                             0x052348C0     88B
  SMSG_AGENT_VIEW_HEARTBEAT_RESULT                      0x05234A38     88B
  SMSG_ALERT_MAIL                                       0x051E6B94    500B
  SMSG_ALLFORONE_POINT_REQUEST                          0x04FABDE0     88B
  SMSG_ALLFORONE_POINT_RETURN                           0x04FABF58     88B
  SMSG_ALL_MARCH_ACCELERATE                             0x052213A8     88B
  SMSG_ANABASIS_RETURN                                  0x05234BE8    104B
  SMSG_ANNIVERSARY_DONATE_INFO_REQUEST                  0x0527B7FC     88B
  SMSG_ANNIVERSARY_DONATE_REQUEST                       0x0527BB6C    104B
  SMSG_ANNIVERSARY_DONATE_RETURN                        0x0527BD98    136B
  SMSG_ANNIVERSARY_SHARE_REWARD_REQUEST                 0x0527BF74    104B
  SMSG_ANNIVERSARY_SHARE_REWARD_RETURN                  0x0527C138    104B
  SMSG_ARENA_BATTLE_RECORD                              0x04FB82F4    324B
  SMSG_ARENA_CHALLENGE_MATCH_REQUEST                    0x04FB41B8    120B
  SMSG_ARENA_CHALLENGE_MATCH_RETURN                     0x04FB43F0    136B
  SMSG_ARENA_CHANGE_CUP                                 0x04FB4B80     88B
  SMSG_ARENA_CHANGE_MATCH_REQUEST                       0x04FB3130    472B
  SMSG_ARENA_CHANGE_MATCH_RETURN                        0x04FB39A8   1664B
  SMSG_ARENA_CREATE_INFO                                0x04FB24E8   1168B
  SMSG_ARENA_MATCH_INFO_REQUEST                         0x04FB5FE4   1664B
  SMSG_ARENA_MATCH_INFO_RETURN                          0x04FB6CCC   1676B
  SMSG_ARENA_PLAYER_ONLINE                              0x04FB7A48   1760B
  SMSG_ARENA_RANK_INFO_REQUEST                          0x04FB4CFC     88B
  SMSG_ARENA_RANK_INFO_RETURN                           0x04FB52AC   1688B
  SMSG_ARENA_UPDATE_DEFEND_INFO                         0x04FB2C28    716B
  SMSG_ARMY_RETURN                                      0x0521AF50    120B
  SMSG_ATTACK_ALIEN                                     0x0522A320    808B
  SMSG_ATTACK_ALIEN_RESULT                              0x0522A8C0    432B
  SMSG_ATTACK_BATTLE_MAP_OBJECT_RESULT                  0x0522E234   1392B
  SMSG_ATTACK_BOSS                                      0x04FC982C    184B
  SMSG_ATTACK_BOSS_RESULT                               0x04FC9A40    104B
  SMSG_ATTACK_BY_KING_CHESS_REQUEST                     0x050D4998   1736B
  SMSG_ATTACK_BY_KING_CHESS_RESULT                      0x050D5604   1408B
  SMSG_ATTACK_BY_SAME_MAP_REQUEST                       0x05231588   1772B
  SMSG_ATTACK_BY_SAME_MAP_RESULT                        0x05231D94     88B
  SMSG_ATTACK_CASTLE                                    0x0521CE74    472B
  SMSG_ATTACK_CASTLE_BY_HARBOR                          0x0521D33C    532B
  SMSG_ATTACK_CASTLE_RESULT                             0x0521E8CC     88B
  SMSG_ATTACK_CROSS_CASTLE_BY_HARBOR                    0x0522B714    532B
  SMSG_ATTACK_CROSS_CASTLE_BY_HARBOR_RESULT             0x0522BA80    104B
  SMSG_ATTACK_CROSS_DOMINION_BY_HARBOR                  0x0522CD78    532B
  SMSG_ATTACK_CROSS_DOMINION_BY_HARBOR_RESULT           0x0522D22C    504B
  SMSG_ATTACK_CROSS_RESOURCE_BY_HARBOR                  0x0522C62C    612B
  SMSG_ATTACK_CROSS_RESOURCE_BY_HARBOR_RESULT           0x0522CA1C    120B
  SMSG_ATTACK_CROSS_STATION_BY_HARBOR                   0x0522BE54    612B
  SMSG_ATTACK_CROSS_STATION_BY_HARBOR_RESULT            0x0522C248    120B
  SMSG_ATTACK_DOMINION                                  0x0521D84C    564B
  SMSG_ATTACK_DOMINION_RESULT                           0x0521EB8C    488B
  SMSG_ATTACK_DOMINION_TRADE_RESULT                     0x0521F818    472B
  SMSG_ATTACK_LEAGUEBUILD                               0x05161974   1820B
  SMSG_ATTACK_LEAGUEBUILD_RESULT                        0x051628A0   1744B
  SMSG_ATTACK_MONSTER                                   0x0521CB4C    168B
  SMSG_ATTACK_MONSTER_RESULT                            0x0521E744    104B
  SMSG_ATTACK_OBJECT_BY_HARBOR_RESULT                   0x0521F57C    104B
  SMSG_ATTACK_RESOURCE                                  0x0521DCE8    184B
  SMSG_ATTACK_RESOURCE_RESULT                           0x0521F040    104B
  SMSG_ATTACK_STATION                                   0x0521E008    184B
  SMSG_ATTACK_STATION_RESULT                            0x0521F200    104B
  SMSG_ATTACK_TRADE                                     0x0521E3BC    564B
  SMSG_AUCTION_BID_REQUEST                              0x04FBEE60    136B
  SMSG_AUCTION_BID_RETURN                               0x04FBF110    168B
  SMSG_AUCTION_CHECK                                    0x04FBFF3C    844B
  SMSG_AUCTION_INFO_REQUEST                             0x04FBF2DC     88B
  SMSG_AUCTION_INFO_RETURN                              0x04FBF610    624B
  SMSG_AUCTION_MIGRATE                                  0x04FC03AC     88B
  SMSG_AUCTION_RETREAT                                  0x04FBF9A4     88B
  SMSG_AUCTION_SET_PLAYER                               0x04FBFB54    104B
  SMSG_BACK_DEFEND                                      0x05225B84   1060B
  SMSG_BACK_MARCH                                       0x0521B0E8     88B
  SMSG_BACK_MARCH_BY_QUEUE_ID                           0x05241B38    104B
  SMSG_BACK_MARCH_RETURN                                0x05236364     72B
  SMSG_BATTLE_DETAIL_REPORT                             0x051E5C10    500B
  SMSG_BATTLE_DETAIL_REPORT_REQUEST                     0x051E63B4    308B
  SMSG_BATTLE_DETAIL_REPORT_RETURN                      0x051E674C    536B
  SMSG_BATTLE_FIELD_SYNC_BATTLE_INFO                    0x05149820   4540B
  SMSG_CANCEL_ALL_BUILDUP                               0x05223D8C     72B
  SMSG_CANCEL_ATTACK_DOMINION                           0x0521EE90     88B
  SMSG_CANCEL_ATTACK_DOMINION_TRADE                     0x0521FB0C     88B
  SMSG_CANCEL_ATTACK_LEAGUEBUILD                        0x051621B0     88B
  SMSG_CANNON_BATTLE_DAMAGE                             0x0522ADD4    504B
  SMSG_CASTLE_DUEL                                      0x0522D8E4    168B
  SMSG_CASTLE_PET_SKILL_BE_USED                         0x05235BB0    152B
  SMSG_CASTLE_PET_SKILL_CHANGE_POS                      0x052356F0    136B
  SMSG_CASTLE_PET_SKILL_SLOW_MARCH                      0x05235934    136B
  SMSG_CASTLE_POS_REPAIR                                0x0521C8A4    120B
  SMSG_CASTLE_THUNDER                                   0x0522D618    152B
  SMSG_CHANGE_CASTLE_EFFECT                             0x0521F3BC    104B
  SMSG_CHAT_HISTORY                                     0x04FE491C   2788B
  SMSG_CHAT_NAME_ERROR_RETURN                           0x04FE277C     88B
  SMSG_CHECK_MARCH_BACK_REQUEST                         0x05236BF8     88B
  SMSG_CHECK_MARCH_INFO                                 0x0522619C    716B
  SMSG_CHECK_MARCH_INFO_FIX_REQUEST                     0x05236498     72B
  SMSG_CHECK_MARCH_INFO_FIX_RETURN                      0x052366D4    716B
  SMSG_CHECK_MARCH_INFO_KING_CHESS_END                  0x050DA018    716B
  SMSG_CHECK_MARCH_INFO_REQUEST                         0x05236A8C     72B
  SMSG_CHECK_RAID_PLAYER_REQUEST                        0x05241074    592B
  SMSG_CHECK_RAID_PLAYER_RETURN                         0x05241578    572B
  SMSG_CHECK_RANK_FLAG                                  0x0528EB0C    152B
  SMSG_CITY_POS_CHANGE                                  0x052377F0    104B
  SMSG_CLANPK_BUILDING_REQUEST                          0x05008E3C     72B
  SMSG_CLANPK_BUILDING_RETURN                           0x05009114    716B
  SMSG_CLANPK_END_COLLECT_REQUEST                       0x0500B578    376B
  SMSG_CLANPK_END_COLLECT_RETURN                        0x0500B9B8    812B
  SMSG_CLANPK_LEVEL_RANK_REQUEST                        0x050061A4    120B
  SMSG_CLANPK_LEVEL_RANK_RESPONSE                       0x05006748   1332B
  SMSG_CLANPK_MATCH_INFO_RESPONSE                       0x05007ABC   1640B
  SMSG_CLANPK_POINT_REQUEST                             0x05005D0C    104B
  SMSG_CLANPK_POINT_RESPONSE                            0x05005F34    228B
  SMSG_CLANPK_QUERY_DEFEND_INFO                         0x05009DCC    120B
  SMSG_CLANPK_SIGNUP_REQUEST                            0x05005730    712B
  SMSG_CLANPK_SIGNUP_RESPONSE                           0x05005B50    104B
  SMSG_CLANPK_SIGN_INFO_UPDATE_REQUEST                  0x05006E18    432B
  SMSG_CLANPK_SIGN_INFO_UPDATE_RESPONSE                 0x05007184    492B
  SMSG_CLANPK_START_ATTACK                              0x050096E0    556B
  SMSG_CLANPK_START_ATTACK_RETURN                       0x05009B70    200B
  SMSG_CLANPK_USER_RANK_VIEW_REQUEST                    0x05008288     88B
  SMSG_CLANPK_USER_RANK_VIEW_RETURN                     0x05008804   1356B
  SMSG_CLEAR_VALIDATED_REQUEST                          0x052EEC48     72B
  SMSG_CLIENT_ROUTE_MAP                                 0x052181C4     72B
  SMSG_COMMAND_CHANGE_NAME_REQUEST                      0x04FBC8F0    324B
  SMSG_COMMAND_CHANGE_NAME_RETURN                       0x04FBCB1C     72B
  SMSG_COMMON_PLAYER_RANK_REQUEST                       0x052F4550    104B
  SMSG_COMMON_PLAYER_RANK_RESPONSE                      0x052F4A20   1224B
  SMSG_COMMON_SELF_RANK_REQUEST                         0x052F5040    104B
  SMSG_COMMON_SELF_RANK_RESPONSE                        0x052F5200    104B
  SMSG_CREATE_BOSS                                      0x04FCA088    760B
  SMSG_CROSS_BATTLE_LOSS                                0x04FC5B00   1788B
  SMSG_CROSS_BATTLE_MATCH_SERVER_ID_REQUEST             0x050E1AEC    104B
  SMSG_CROSS_BATTLE_MATCH_SERVER_ID_RESPONSE            0x050E1CA4    116B
  SMSG_CROSS_CHECK_MARCH_INFO                           0x05232190   1500B
  SMSG_CROSS_DOMINIONBUILD_SUCCESS_SYNC                 0x05233660    104B
  SMSG_CROSS_DOMINION_SIMPLE_INFO_QUERY                 0x05232890     88B
  SMSG_CROSS_KING_CHESS_SIMPLE_INFO_QUERY               0x050D7B38     88B
  SMSG_CROSS_LOSTLAND_BUILDUP_SUCCESS_SYNC              0x052338C0    152B
  SMSG_CS2GS_HEAD                                       0x0528D754     72B
  SMSG_CS_USER_INFO_REQUEST                             0x0524208C    388B
  SMSG_CS_USER_INFO_RETURN                              0x052425AC   1048B
  SMSG_CUSTOM_HEAD_REQUEST                              0x05017808    548B
  SMSG_CUSTOM_HEAD_RETURN                               0x05017D74   1036B
  SMSG_DAMAGE_HELP                                      0x0502A638    120B
  SMSG_DEFAULT_RESPONSE_RPC                             0x052B0C64     88B
  SMSG_DEFENSE_TIME_CHANGE                              0x05240D28     88B
  SMSG_DELETE_CAMEL                                     0x05055BE8    136B
  SMSG_DELETE_INVALID_DATA_REQUEST                      0x052DAEF0     88B
  SMSG_DELETE_INVALID_DATA_RETURN                       0x052DB09C    104B
  SMSG_DELETE_LEAGUEBUILD                               0x051601C4    136B
  SMSG_DELETE_LEAGUE_BIG_BOSS                           0x05156BF8    120B
  SMSG_DELETE_LEAGUE_BOSS                               0x051569D0    136B
  SMSG_DELETE_SECRET_TASK                               0x052C07C0     72B
  SMSG_DELETE_STATION                                   0x05237AE0    104B
  SMSG_DEL_AUTO_JOIN_BATTLE                             0x0515060C     72B
  SMSG_DEL_BATTLE                                       0x05221ED0     88B
  SMSG_DEL_BATTLE_KING_CHESS                            0x050D3C54     88B
  SMSG_DEL_COLLECT_PLAYER                               0x051611C8    104B
  SMSG_DEL_DEFEND                                       0x0510C9E4     88B
  SMSG_DEL_MARCH_INFO                                   0x052283BC     72B
  SMSG_DEL_PENDING_DEFEND                               0x0510CED4    136B
  SMSG_DEL_PLACEMENT                                    0x0522542C    120B
  SMSG_DESERT_TRADE_ADD_BATTLE_RECORD                   0x05038C60    340B
  SMSG_DESERT_TRADE_ADD_TRUCK                           0x05037518    524B
  SMSG_DESERT_TRADE_DELETE_PLAYER_TURCK                 0x0503A038    152B
  SMSG_DESERT_TRADE_QUERY_TRUCK_INFO_REQUEST            0x050357B8    104B
  SMSG_DESERT_TRADE_QUERY_TRUCK_INFO_RESPONSE           0x05036300   3520B
  SMSG_DESERT_TRADE_ROBBERY_REQUEST                     0x0503841C    504B
  SMSG_DESERT_TRADE_ROBBERY_RESPONSE                    0x05038848    548B
  SMSG_DESERT_TRADE_SEARCH_TRUCK_REQUEST                0x050378B4    120B
  SMSG_DESERT_TRADE_SEARCH_TRUCK_RESPONSE               0x05037D98    992B
  SMSG_DESERT_TRADE_TRUCK_ROBBERY_TIMES_REQUEST         0x050392B4    528B
  SMSG_DESERT_TRADE_TRUCK_ROBBERY_TIMES_RETURN          0x05039728    624B
  SMSG_DESERT_TRADE_UPDATE_LEAGUE_DATA                  0x05039CAC    404B
  SMSG_DESERT_TRADE_UPDATE_TUCK_ROBBERY_TIMES           0x05038FE4    168B
  SMSG_DESTROY_CASTLE                                   0x05228DEC     72B
  SMSG_DETELE_BOSS                                      0x04FCA540    500B
  SMSG_DISPATCH_REQUEST_USER_INFO                       0x0517D94C    136B
  SMSG_DISPATCH_RETURN_USER_INFO                        0x0517DB94    136B
  SMSG_DNS_UPDATE_IP                                    0x0517E150    308B
  SMSG_DNS_UPDATE_TOKEN_IP                              0x0517E410    308B
  SMSG_DOMINION_BEATTACK_SYNC                           0x05233AAC    104B
  SMSG_DOMINION_TRADE_FESTIVAL_SYNC                     0x0504D5BC     72B
  SMSG_DOMINION_TRADE_MARCH_INSERT                      0x0504CC98    360B
  SMSG_DOMINION_TRADE_MARCH_RESUME                      0x0504D320    436B
  SMSG_DOMINION_TRADE_MARCH_SUCCESS                     0x0504CF1C     88B
  SMSG_ENABLE_VIEW                                      0x0521832C     88B
  SMSG_ENABLE_VIEW_AND_LOOKAT                           0x05234734    104B
  SMSG_ENABLE_VIEW_KING_CHESS                           0x050D4258    104B
  SMSG_END_INVESTIGATION                                0x05229160     88B
  SMSG_END_LOOK_OTHER_SERVER                            0x05237650     72B
  SMSG_EPD_ATTACKER_REQUEST                             0x0517F5DC    120B
  SMSG_EPD_ATTACKER_RETURN                              0x0517F8DC    392B
  SMSG_EXPEDITION_BATTLE_LOSS                           0x04FC4E40   1684B
  SMSG_EXPEDITION_DEFENDER_MOVED                        0x052351C4    880B
  SMSG_FB_INVITE_REQUEST                                0x050BF44C    388B
  SMSG_FB_INVITE_RESP                                   0x050BF724    104B
  SMSG_FIGHT_RECORD_REQUEST                             0x050662A4    952B
  SMSG_FORTRESS_ACTION_VALUE_REQUEST                    0x050799E8    104B
  SMSG_FORTRESS_ACTION_VALUE_RETURN                     0x05079C9C    484B
  SMSG_FORTRESS_ACTIVITY_STAGE_CHANGE                   0x05074BD4   1956B
  SMSG_FORTRESS_CANNON_ATTACK                           0x05078964   1216B
  SMSG_FORTRESS_CANNON_ATTACK_RETURN                    0x05079340   1360B
  SMSG_FORTRESS_DOMINION_OCCUPY                         0x05077B98     88B
  SMSG_FORTRESS_ENTER_CHECK_REQUEST                     0x05075750    104B
  SMSG_FORTRESS_ENTER_CHECK_RETURN                      0x050758A4     72B
  SMSG_FORTRESS_EXIT_REQUEST                            0x050744A0     88B
  SMSG_FORTRESS_EXIT_RESPONSE                           0x050745E4     72B
  SMSG_FORTRESS_LEAGUE_LEVEL                            0x0507A058    456B
  SMSG_FORTRESS_LEAGUE_POINT_REQUEST                    0x050739D4    104B
  SMSG_FORTRESS_LEAGUE_POINT_RESPONSE                   0x05073EA0   1248B
  SMSG_FORTRESS_LEVEL_RANK_REQUEST                      0x05071BB8    120B
  SMSG_FORTRESS_LEVEL_RANK_RESPONSE                     0x050720D4   1276B
  SMSG_FORTRESS_LEVEL_USER_RANK_REQUEST                 0x05072724    104B
  SMSG_FORTRESS_LEVEL_USER_RANK_RESPONSE                0x05072C30   1276B
  SMSG_FORTRESS_MAPINFO_REQUEST                         0x050755AC     72B
  SMSG_FORTRESS_MATCH_INFO_REQUEST                      0x05076294     72B
  SMSG_FORTRESS_MATCH_INFO_RESPONSE                     0x050764F8    616B
  SMSG_FORTRESS_POINT_REQUEST                           0x0506FD38    104B
  SMSG_FORTRESS_POINT_RESPONSE                          0x050702D4   1192B
  SMSG_FORTRESS_POWER_REQUEST                           0x050732C8    432B
  SMSG_FORTRESS_POWER_RESPONSE                          0x05073670    524B
  SMSG_FORTRESS_RANK_REQUEST                            0x050710DC    104B
  SMSG_FORTRESS_RANK_RESPONSE                           0x05071570   1212B
  SMSG_FORTRESS_RESOURCE_REQUEST                        0x05077D14     88B
  SMSG_FORTRESS_SIGNUP_REQUEST                          0x05070B40    644B
  SMSG_FORTRESS_SIGNUP_RESPONSE                         0x05070F1C    104B
  SMSG_FORTRESS_SIGN_INFO_UPDATE_REQUEST                0x05075A88    432B
  SMSG_FORTRESS_SIGN_INFO_UPDATE_RESPONSE               0x05075DF4    492B
  SMSG_FRIEND_ACCEPT_REQUEST                            0x05083F54    120B
  SMSG_FRIEND_ACCEPT_RESPONSE                           0x0508451C   1476B
  SMSG_FRIEND_APPLY_ADD_REQUEST                         0x050838B4    400B
  SMSG_FRIEND_APPLY_COUNT_RESPONSE                      0x050826B8     88B
  SMSG_FRIEND_APPLY_VIEW_REQUEST                        0x05081A78     88B
  SMSG_FRIEND_APPLY_VIEW_RESPONSE                       0x05081FE8   1456B
  SMSG_FRIEND_DELETE_REQUEST                            0x05083B9C    104B
  SMSG_FRIEND_DELETE_RESPONSE                           0x05083D5C    104B
  SMSG_FRIEND_GET_COUNT_REQUEST                         0x05086B50    104B
  SMSG_FRIEND_GET_COUNT_RESPONSE                        0x05086D0C    104B
  SMSG_FRIEND_GIFT_PRESENT_REQUEST                      0x05097934    388B
  SMSG_FRIEND_GIFT_PRESENT_RESP                         0x05097C4C    120B
  SMSG_FRIEND_REJECT_REQUEST                            0x05084C74    120B
  SMSG_FRIEND_REJECT_RESPONSE                           0x05084E80    120B
  SMSG_FRIEND_SEARCH_REQUEST                            0x050829D0    440B
  SMSG_FRIEND_SEARCH_RESPONSE                           0x050830C4   1440B
  SMSG_FRIEND_SEND_GIFT_CROSS_SERVER                    0x050868A8    340B
  SMSG_FRIEND_SEND_GIFT_REQUEST                         0x05085054    104B
  SMSG_FRIEND_SEND_GIFT_RESPONSE                        0x0508524C    120B
  SMSG_FRIEND_VIEW_REQUEST                              0x05080E3C     88B
  SMSG_FRIEND_VIEW_RESPONSE                             0x050813AC   1448B
  SMSG_GAMESERVER_INFO_REQUEST                          0x0517CFE4    136B
  SMSG_GAMESERVER_INFO_RETURN                           0x0517D3C0    596B
  SMSG_GAMESERVER_INRO_REQUEST_ERROR                    0x0517D734     88B
  SMSG_GAMESERVER_REQUEST_CHANGE_NAME                   0x052ED3C4    408B
  SMSG_GAMESERVER_REQUEST_CHANGE_SERVER_ID              0x052EDDE0    104B
  SMSG_GAMESERVER_RETURN_CHANGE_NAME                    0x052EDAEC    416B
  SMSG_GAMESERVER_RETURN_CHANGE_SERVER_ID               0x052EE004    136B
  SMSG_GAME_EVENT_PUSH                                  0x051E7DB4    340B
  SMSG_GAME_SERVER_READY                                0x0522006C     88B
  SMSG_GENERAL_ACTIBITIES_DISPRITY_RANK_REQUEST         0x0508BDC0    120B
  SMSG_GENERAL_ACTIBITIES_DISPRITY_RANK_RESPONSE        0x0508BFFC    136B
  SMSG_GENERAL_ACTIBITIES_PLAYER_RANK_REQUEST           0x0508AA48    104B
  SMSG_GENERAL_ACTIBITIES_PLAYER_RANK_RESPONSE          0x0508AF18   1224B
  SMSG_GENERAL_ACTIBITIES_SELF_RANK_REQUEST             0x0508B538    104B
  SMSG_GENERAL_ACTIBITIES_SELF_RANK_RESPONSE            0x0508B6F8    104B
  SMSG_GET_ALINE_NUM                                    0x0522B184     56B
  SMSG_GET_DEFEND_INFO_BY_PLAYERID                      0x05143F84    104B
  SMSG_GET_DEFEND_INFO_BY_PLAYERID_RESPONSE             0x05144554   1192B
  SMSG_GET_ONLINE_PLAYER_REQUEST                        0x052ECCF4     56B
  SMSG_GET_OTHER_EXTRA_ATTRIBUTE                        0x05060300    104B
  SMSG_GET_OTHER_NAME                                   0x050604C4    104B
  SMSG_GET_PART_NEWS_INFO_REQUEST                       0x0525DEE4    120B
  SMSG_GET_PART_NEWS_INFO_RETURN                        0x0525E1EC    372B
  SMSG_GET_PLAYERINFO_BY_NAME                           0x052F0BF4    400B
  SMSG_GET_PLAYER_BY_NAME_REQUEST                       0x050E67C8    416B
  SMSG_GET_PLAYER_BY_NAME_RETURN                        0x050E6AC0    104B
  SMSG_GET_QUEUE_BY_PLAYERID                            0x050D8430     72B
  SMSG_GET_QUEUE_BY_PLAYERID_RESPONSE                   0x050D866C    724B
  SMSG_GIANT_INVASION_ADD_TREASURE_POINT                0x0508F9B0     72B
  SMSG_GIANT_INVASION_KILL_MONSTER_REQUEST              0x0508FCEC    548B
  SMSG_GIANT_INVASION_KILL_MONSTER_RETURN               0x05090068    104B
  SMSG_GIANT_INVASION_TREASURE_POINT_REQUEST            0x0508ED8C     88B
  SMSG_GIANT_INVASION_TREASURE_POINT_RETURN             0x0508EF08     88B
  SMSG_GIANT_INVASION_TREASURE_REWARD_RECORD_REQUEST    0x0508F084     88B
  SMSG_GIANT_INVASION_TREASURE_REWARD_RECORD_RETURN     0x0508F4D0   1016B
  SMSG_GIFTPACK_INFO                                    0x050965E8   4004B
  SMSG_GIFTPACK_INFO_REQUEST                            0x05095968     72B
  SMSG_GLOBAL_CYCLE_ACTION_END                          0x05020694     88B
  SMSG_GLOBAL_CYCLE_ACTION_RANK_RECORD_REQUEST          0x050204FC    120B
  SMSG_GLOBAL_CYCLE_ACTION_RANK_RECORD_RETURN           0x05020AAC   1056B
  SMSG_GOLD_CHARGE_GET_GIFT_ID_REQUEST                  0x05097DAC     72B
  SMSG_GOLD_CHARGE_GET_GIFT_ID_RESP                     0x05097F14     88B
  SMSG_GOLD_CHARGE_RETURN                               0x052EBAE8    920B
  SMSG_GOLD_CHARGE_SUCCESS                              0x052EC044    324B
  SMSG_GOODLUCK_ADD_LIST_REQUEST                        0x0509DDA4    464B
  SMSG_GOODLUCK_LIST_REQUEST                            0x0509D304    104B
  SMSG_GOODLUCK_LIST_RETURN                             0x0509D72C    944B
  SMSG_GS_LEAGUE_LEAGUEPASS_REQUEST                     0x051710A4     56B
  SMSG_GS_LEAGUE_LEAGUEPASS_RESPONSE                    0x05171618   1772B
  SMSG_GS_LEAGUE_MOBILIZATION_REQUEST                   0x05254928     56B
  SMSG_GS_LEAGUE_MOBILIZATION_RESPONSE                  0x05254D60   1088B
  SMSG_GS_LEAGUE_TOP10_POWER_REQUEST                    0x050E1DD8     56B
  SMSG_GS_LEAGUE_TOP10_POWER_RESPONSE                   0x050E1F2C     88B
  SMSG_GUILD_STANDOFF_DUEL_POINT_REQUEST                0x050A84BC    104B
  SMSG_GUILD_STANDOFF_DUEL_POINT_RETURN                 0x050A8A6C   1924B
  SMSG_GUILD_STANDOFF_SIGN_UP_REQUEST                   0x050A7F44    608B
  SMSG_GUILD_STANDOFF_SIGN_UP_RETURN                    0x050A82F8    104B
  SMSG_GUILD_STANDOFF_UPDATE_GUILD_BANNER_ID            0x050AA41C     88B
  SMSG_GUILD_STANDOFF_UPDATE_GUILD_NAME                 0x050A9EAC    324B
  SMSG_GUILD_STANDOFF_UPDATE_GUILD_SHORT_NAME           0x050AA1B4    324B
  SMSG_GUILD_STANDOFF_UPDATE_POINT                      0x050A9C80    104B
  SMSG_HARBOR_MARCH_HEARTBEAT                           0x05234D9C    104B
  SMSG_HERO_HEAD_CHANGE                                 0x05292BC4     88B
  SMSG_HERO_POWER_CHANGE                                0x05290468   3016B
  SMSG_HONOR_CHANGE                                     0x05292914    396B
  SMSG_HONOR_SOUL_POWER_CHANGE                          0x052939D8   2136B
  SMSG_HONOR_SOUL_UPDATE                                0x050BB8D4    564B
  SMSG_IMM_BACK_MARCH                                   0x052203E8   1244B
  SMSG_IMM_HARBOR_ARMY_BACK                             0x05237940     72B
  SMSG_INIT_STATION_ERROR                               0x05227728    120B
  SMSG_INIT_USERNAME                                    0x052ED720    324B
  SMSG_INVESTIGATION_RESULT                             0x052244C4   1296B
  SMSG_INVESTIGATION_START                              0x052278F8    104B
  SMSG_INVITER_ADD_PROGRESS                             0x050BFB1C    120B
  SMSG_INVITER_CHANGE_NAME                              0x050BFF8C    356B
  SMSG_INVITER_CHARGE_GOLD                              0x050BF918    120B
  SMSG_INVITER_CITY_LEVELUPGRADE                        0x050BFCE8    104B
  SMSG_ITEM_CHARGE_REQUEST                              0x052EC348    136B
  SMSG_ITEM_CHARGE_RETURN                               0x052EC728    464B
  SMSG_JOIN_BUILDUP                                     0x0521A06C    996B
  SMSG_KICK_BUILDUP_HERO                                0x0531273C    104B
  SMSG_KICK_DEFEND_HERO                                 0x0531257C    104B
  SMSG_KICK_DOMINION_DEFEND_HERO                        0x053123AC    120B
  SMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY                    0x0516423C    136B
  SMSG_KINGDOM_ACTION_GEN_RESOURCE                      0x050DE0B4     72B
  SMSG_KINGDOM_ACTION_RANK_RECORD_REQUEST               0x050DE6E4    104B
  SMSG_KINGDOM_ACTION_RANK_RECORD_RETURN                0x050DEB0C   1056B
  SMSG_KINGDOM_ACTION_VALUE_REQUEST                     0x050DF618     88B
  SMSG_KING_CHESS_ACTION_DETAIL_REQUEST                 0x050CE134    104B
  SMSG_KING_CHESS_ACTION_DETAIL_RESPONSE                0x050CE668   1152B
  SMSG_KING_CHESS_ACTION_END                            0x050D9DDC     72B
  SMSG_KING_CHESS_ACTION_ENDUPDATE_POWER                0x050D9360    776B
  SMSG_KING_CHESS_ACTIVITY_STAGE_CHANGE                 0x050D150C   1984B
  SMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST               0x050DA8A8     88B
  SMSG_KING_CHESS_BATTLE                                0x050D5F54    492B
  SMSG_KING_CHESS_BIND_LEAGUE_ID                        0x050DAA20     88B
  SMSG_KING_CHESS_INIT_RANK_REQUEST                     0x050DA400     88B
  SMSG_KING_CHESS_INIT_RANK_RETURN                      0x050DA57C     88B
  SMSG_KING_CHESS_MARCH_REQUEST                         0x050D27B0   2400B
  SMSG_KING_CHESS_MARCH_RETURN                          0x050D33A4    588B
  SMSG_KING_CHESS_MATCH_INFO_REQUEST                    0x050D0074     72B
  SMSG_KING_CHESS_MATCH_INFO_RESPONSE                   0x050D0310    676B
  SMSG_KING_CHESS_OCCUPY_INFO_REQUEST                   0x050D8A60     88B
  SMSG_KING_CHESS_OCCUPY_INFO_RETURN                    0x050D8DB4    808B
  SMSG_KING_CHESS_PLAYER_INFO_REQUEST                   0x050D6FAC     88B
  SMSG_KING_CHESS_QUIT_LEAGUE                           0x050DAB98     88B
  SMSG_KING_CHESS_RANK_REQUEST                          0x050CEC40    104B
  SMSG_KING_CHESS_RANK_RESPONSE                         0x050CF3D0   2172B
  SMSG_KING_CHESS_SELF_INFO_REQUEST                     0x050DA724    104B
  SMSG_KING_CHESS_SIGNUP_REQUEST                        0x050CDC04    612B
  SMSG_KING_CHESS_SIGNUP_RESPONSE                       0x050CDF88     88B
  SMSG_KING_CHESS_SIGN_INFO_UPDATE_RESPONSE             0x050CFF34     88B
  SMSG_KING_CHESS_SYNC_DEFEND_INFO                      0x050D6AF0    924B
  SMSG_KING_CHESS_UPDATE_BATTLE_VERSION                 0x050DAD10     88B
  SMSG_KING_CHESS_USER_VALUE_REQUEST                    0x050D97C0    104B
  SMSG_KING_CHESS_USER_VALUE_RETURN                     0x050D9A38    696B
  SMSG_KNIGHT_ACTION_DETAIL_INFO_REQUEST                0x050DFDE4    104B
  SMSG_KNIGHT_ACTION_DETAIL_INFO_RESPONSE               0x050DFFDC    120B
  SMSG_KNIGHT_ATTACK_CASTLE                             0x050E9E6C    136B
  SMSG_KNIGHT_ATTACK_CASTLE_RESULT                      0x050EA1B8    104B
  SMSG_KNIGHT_CANCEL_ATTACK_CASTLE                      0x050EA010     88B
  SMSG_KNIGHT_GLORY_ATTACK_REQUEST                      0x050EDD1C    740B
  SMSG_KNIGHT_GLORY_ATTACK_RETURN                       0x050EE26C    184B
  SMSG_KNIGHT_GLORY_DELETE                              0x050EED0C    408B
  SMSG_KNIGHT_GLORY_DEL_LOSTLAND_REQUEST                0x050EF644   1204B
  SMSG_KNIGHT_GLORY_DEL_LOSTLAND_RETURN                 0x050EFF98   1228B
  SMSG_KNIGHT_GLORY_LEAGUE_ATTACK_REQUEST               0x050EE6D8    280B
  SMSG_KNIGHT_GLORY_LEAGUE_ATTACK_RETURN                0x050EEA5C    184B
  SMSG_KNIGHT_GLORY_LEAGUE_DELETE                       0x050EF068    376B
  SMSG_KNIGHT_GLORY_SUMMO_MONSTER_REQUEST               0x050ED430    168B
  SMSG_KNIGHT_GLORY_SUMMO_MONSTER_RETURN                0x050ED7E0    232B
  SMSG_KNIGHT_PLAYER_RANK_REQUEST                       0x050E0178     88B
  SMSG_KNIGHT_PLAYER_RANK_RESPONSE                      0x050E0714   1320B
  SMSG_LEAGUEPASS_GROUP_RANK_REQUEST                    0x051701AC    136B
  SMSG_LEAGUEPASS_GROUP_RANK_RETURN                     0x0517086C   1912B
  SMSG_LEAGUEPASS_MATCH_INFO_REQUEST                    0x05171E3C     72B
  SMSG_LEAGUEPASS_MATCH_INFO_RESPONSE                   0x05172080    556B
  SMSG_LEAGUE_BATTLEFIELD_DOMINION_BATTLE               0x0514D3CC    552B
  SMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST            0x0513C6FC    472B
  SMSG_LEAGUE_BATTLEFIELD_GET_REWARD_RETURN             0x0513CAF4    548B
  SMSG_LEAGUE_BATTLEFIELD_MAPINFO_REQUEST               0x0514D6E0     72B
  SMSG_LEAGUE_BATTLE_ENTER_CHECK_REQUEST                0x0514D9B8    104B
  SMSG_LEAGUE_BATTLE_ENTER_CHECK_RETURN                 0x0514DB0C     72B
  SMSG_LEAGUE_BATTLE_FIELD_ALL_DOMINION_BATTLE_REQUEST  0x0514C9A0     72B
  SMSG_LEAGUE_BATTLE_FIELD_EXIT_REQUEST                 0x0514169C     88B
  SMSG_LEAGUE_BATTLE_FIELD_EXIT_RESPONSE                0x051417E0     72B
  SMSG_LEAGUE_BATTLE_FIELD_FORCE_REQUEST                0x0514C86C     72B
  SMSG_LEAGUE_BATTLE_FIELD_GET_BATTLE_INFO_REQUEST      0x051460CC    500B
  SMSG_LEAGUE_BATTLE_FIELD_GET_BATTLE_INFO_RESPONSE     0x05147450   5028B
  SMSG_LEAGUE_BATTLE_FIELD_GET_DEF_BATTLEINFO_REQUEST   0x0514AAC8     72B
  SMSG_LEAGUE_BATTLE_FIELD_GET_DEF_BATTLEINFO_RESPONSE  0x0514B80C   3484B
  SMSG_LEAGUE_BATTLE_FIELD_LEAGUE_POINT_REQUEST         0x05140B64    104B
  SMSG_LEAGUE_BATTLE_FIELD_LEAGUE_POINT_RESPONSE        0x05141080   1276B
  SMSG_LEAGUE_BATTLE_FIELD_MATCH_INFO_REQUEST           0x0513BF8C     72B
  SMSG_LEAGUE_BATTLE_FIELD_MATCH_INFO_RESPONSE          0x0513C228    684B
  SMSG_LEAGUE_BATTLE_FIELD_POINT_REQUEST                0x0513E0C0    104B
  SMSG_LEAGUE_BATTLE_FIELD_POINT_RESPONSE               0x0513E5F4   1152B
  SMSG_LEAGUE_BATTLE_FIELD_POWER_REQUEST                0x05140458    432B
  SMSG_LEAGUE_BATTLE_FIELD_POWER_RESPONSE               0x05140800    524B
  SMSG_LEAGUE_BATTLE_FIELD_RANK_REQUEST                 0x0513F2B0    104B
  SMSG_LEAGUE_BATTLE_FIELD_RANK_RESPONSE                0x0513FA40   2172B
  SMSG_LEAGUE_BATTLE_FIELD_SEND_DOMINION_BATTLE_COUNT   0x0514CB40    104B
  SMSG_LEAGUE_BATTLE_FIELD_SIGNUP_REQUEST               0x0513ED74    548B
  SMSG_LEAGUE_BATTLE_FIELD_SIGNUP_RESPONSE              0x0513F0F0    104B
  SMSG_LEAGUE_BATTLE_FIELD_SIGN_INFO_UPDATE_REQUEST     0x0513AD50    432B
  SMSG_LEAGUE_BATTLE_FIELD_SIGN_INFO_UPDATE_RESPONSE    0x0513B0BC    500B
  SMSG_LEAGUE_BATTLE_FIELD_SYNC_BUILDUP_INFO            0x05143584   1740B
  SMSG_LEAGUE_BATTLE_FIELD_SYNC_DEFEND_INFO             0x05142980   1272B
  SMSG_LEAGUE_BATTLE_FIELD_SYNC_DETECT_INFO             0x0514D814     72B
  SMSG_LEAGUE_BATTLE_FIELD_SYNC_LEAGUE_BATTLE_COUNT     0x051458E0   1076B
  SMSG_LEAGUE_BATTLE_FIELD_TOWER_BEATTACK               0x0514525C    648B
  SMSG_LEAGUE_BATTLE_FIELD_UPDATE_EMBASSY_VERSION       0x05143DD4     88B
  SMSG_LEAGUE_BATTLE_FIELD_UPDATE_LEADERFLAG            0x0514C728     88B
  SMSG_LEAGUE_BATTLE_NOTIFICATION                       0x0514CFF8    384B
  SMSG_LEAGUE_BATTLE_SYNC_DOMINION_DEFEND_VERSION       0x0514CD30    120B
  SMSG_LEAGUE_BIG_BOSS_CREATE_REQUEST                   0x05154C78    136B
  SMSG_LEAGUE_BIG_BOSS_CREATE_RETURN                    0x05154EC4    136B
  SMSG_LEAGUE_BIG_BOSS_EMPTYPOS_REQUEST                 0x051550A4    104B
  SMSG_LEAGUE_BOSS_CREATE_REQUEST                       0x05155A94    152B
  SMSG_LEAGUE_BOSS_CREATE_RETURN                        0x05155D20    152B
  SMSG_LEAGUE_BUILDING_DEL_REQUEST                      0x0515E734    432B
  SMSG_LEAGUE_BUILDING_DETAIL_REQUEST                   0x051603A4    104B
  SMSG_LEAGUE_BUILDING_DETAIL_RETURN                    0x051608F8    736B
  SMSG_LEAGUE_BUILDING_OPERAT_REQUEST                   0x0515DFF8    464B
  SMSG_LEAGUE_BUILDING_OPERAT_RETURN                    0x0515E4C0    216B
  SMSG_LEAGUE_DESTORY_DEL_LEGION                        0x0512CF54    428B
  SMSG_LEAGUE_ID_CHANGE                                 0x05292EFC     88B
  SMSG_LEAGUE_LEADER_EMPTYPOS_REQUEST                   0x05105EB0    104B
  SMSG_LEAGUE_NAME_CHANGE                               0x05291B5C    836B
  SMSG_LEAGUE_SHORT_NAME_CHANGE                         0x05292110    836B
  SMSG_LEGION_ACTION_REQUEST                            0x0512A57C    120B
  SMSG_LEGION_ACTION_RETURN                             0x0512AB14   1216B
  SMSG_LEGION_ACTION_VALUE_REQUEST                      0x0512B628    104B
  SMSG_LEGION_ACTION_VALUE_RETURN                       0x0512B954    576B
  SMSG_LEGION_BATTLE_MAP_INFO_REQUEST                   0x0512BCF0    104B
  SMSG_LEGION_BATTLE_MAP_INFO_RETURN                    0x0512BFB8    604B
  SMSG_LEGION_BROADCAST_MSG                             0x0512C91C    340B
  SMSG_LEGION_CHANGE_POS_TIMES_REQUEST                  0x0512B12C    104B
  SMSG_LEGION_CHANGE_POS_TIMES_RETURN                   0x0512B2EC    104B
  SMSG_LEGION_ENEMY_POS_REQUEST                         0x0512D418    104B
  SMSG_LEGION_FINAL_POINT                               0x0514EAE0   2004B
  SMSG_LEGION_PLAYER_FINAL_POINT                        0x0514F5EC   1340B
  SMSG_LEGION_RANK_REQUEST                              0x05129A9C    104B
  SMSG_LEGION_RANK_RETURN                               0x05129F68   1160B
  SMSG_LEGION_RESOURCE_REQUEST                          0x0512C6D0     88B
  SMSG_LEGION_SEASON_ACTION_GROUP_INFO_REQUEST          0x05136F34    104B
  SMSG_LEGION_SEASON_ACTION_GROUP_INFO_RETURN           0x05137590   1360B
  SMSG_LEGION_SEASON_ACTION_GUESS_BET_REQUEST           0x05131A68    136B
  SMSG_LEGION_SEASON_ACTION_GUESS_BET_RETURN            0x0513213C   1212B
  SMSG_LEGION_SEASON_ACTION_GUESS_INFO_REQUEST          0x05130B0C    104B
  SMSG_LEGION_SEASON_ACTION_GUESS_INFO_RETURN           0x05131104   1944B
  SMSG_LEGION_SEASON_ACTION_GUESS_RESULT                0x051354AC    744B
  SMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_REQUEST     0x051348E0    104B
  SMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_RETURN      0x05134DAC   1140B
  SMSG_LEGION_SEASON_ACTION_HIS_MVP_REQUEST             0x05133E4C    104B
  SMSG_LEGION_SEASON_ACTION_HIS_MVP_RETURN              0x05134318   1140B
  SMSG_LEGION_SEASON_ACTION_HIS_PLAYER_REQUEST          0x051332EC    136B
  SMSG_LEGION_SEASON_ACTION_HIS_PLAYER_RETURN           0x05133864   1172B
  SMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_REQUEST         0x05136B58    120B
  SMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_RETURN          0x05136D60    120B
  SMSG_LEGION_SEASON_ACTION_MEMBER_INFO_REQUEST         0x0513592C    368B
  SMSG_LEGION_SEASON_ACTION_MEMBER_INFO_RETURN          0x05135D8C    836B
  SMSG_LEGION_SEASON_ACTION_PLAYER_NAME_REQUEST         0x05136268    368B
  SMSG_LEGION_SEASON_ACTION_PLAYER_NAME_RETURN          0x05136694    820B
  SMSG_LEGION_SEASON_ACTION_PLAYOFF_REQUEST             0x05132784    120B
  SMSG_LEGION_SEASON_ACTION_PLAYOFF_RETURN              0x05132CB0   1144B
  SMSG_LEGION_SEASON_ACTION_REQUEST                     0x0512DB8C    104B
  SMSG_LEGION_SEASON_ACTION_RETURN                      0x0512E4B0   1812B
  SMSG_LEGION_SEASON_ACTION_SCHEDULE_REQUEST            0x0512ED50    120B
  SMSG_LEGION_SEASON_ACTION_SCHEDULE_RETURN             0x0512F334   1692B
  SMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_REQUEST       0x0512FB28    104B
  SMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_RETURN        0x05130178   2108B
  SMSG_LEGION_UPDATE_ACTION_VALUE                       0x0512D258    104B
  SMSG_LEGION_VALUE_DETAIL_REQUEST                      0x0512D5D8    104B
  SMSG_LEGION_VALUE_DETAIL_RETURN                       0x0512D854    480B
  SMSG_LOAD_BATTLE_PLAYER_REQUEST                       0x04FC402C   1140B
  SMSG_LOAD_BATTLE_PLAYER_RESPONSE                      0x04FC4770    432B
  SMSG_LOAD_DELETE_SECRET_TASK                          0x052C0924     88B
  SMSG_LOAD_MAIL_REQUEST                                0x04FE2604     88B
  SMSG_LOAD_MAIL_RESPONSE                               0x04FE2D70   1652B
  SMSG_LORD_CHAT_BOX_CHANGE                             0x052926F0     88B
  SMSG_LORD_HEAD_CHANGE                                 0x05292574     88B
  SMSG_LORD_LIKE_CHANGE                                 0x05291400    484B
  SMSG_LORD_LIKE_PLAYER                                 0x05293450     72B
  SMSG_LORD_LIKE_REQUEST                                0x05293118    136B
  SMSG_LORD_LIKE_RETURN                                 0x052932FC    104B
  SMSG_LORD_POWER_CHANGE                                0x05291188    104B
  SMSG_LORD_SKILL_TRIGGER_110_REQUEST                   0x05230058    120B
  SMSG_LORD_SKILL_TRIGGER_110_RETURN                    0x052302C8    152B
  SMSG_LORD_SKILL_TRIGGER_130_REQUEST                   0x05230598    492B
  SMSG_LORD_SKILL_TRIGGER_130_RETURN                    0x052309B4    168B
  SMSG_LORD_SKILL_TRIGGER_REQUEST                       0x0519F270    388B
  SMSG_LORD_SKILL_TRIGGER_RETURN                        0x0519F744    420B
  SMSG_LOSTLAND_ACHIEVEMENT_COMPLETE                    0x051C48B0   1320B
  SMSG_LOSTLAND_ACHIEVEMENT_LIST_REQUEST                0x051C3D40    104B
  SMSG_LOSTLAND_ACHIEVEMENT_LIST_RETURN                 0x051C40B4    740B
  SMSG_LOSTLAND_ACHIEVEMENT_REQUEST                     0x051C4F6C    120B
  SMSG_LOSTLAND_ACHIEVEMENT_RETURN                      0x051C5464   1484B
  SMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST              0x051C5BBC    120B
  SMSG_LOSTLAND_ACHIEVEMENT_REWARD_RETURN               0x051C5D58     88B
  SMSG_LOSTLAND_ACTIVITY_STAGE_CHANGE                   0x051B8264   1564B
  SMSG_LOSTLAND_ADD_LEAGUE_CRYSTAL                      0x051C5FC4    484B
  SMSG_LOSTLAND_ATTACK_ALIEN                            0x051C303C    904B
  SMSG_LOSTLAND_ATTACK_ALIEN_RESULT                     0x051C3674    464B
  SMSG_LOSTLAND_ATTACK_MONSTER                          0x051C3B10    216B
  SMSG_LOSTLAND_BAN_HERO_REQUEST                        0x051BB7D0    476B
  SMSG_LOSTLAND_BAN_HERO_RETURN                         0x051BBB7C    456B
  SMSG_LOSTLAND_BROADCAST_CLIENT                        0x051C26B0     56B
  SMSG_LOSTLAND_CAMP_RANK_REQUEST                       0x051BDBC0     88B
  SMSG_LOSTLAND_CAMP_RANK_RETURN                        0x051BDF3C   1372B
  SMSG_LOSTLAND_ENTER_CHECK_REQUEST                     0x051B9ED4    104B
  SMSG_LOSTLAND_ENTER_CHECK_RETURN                      0x051BA028     72B
  SMSG_LOSTLAND_EXIT_REQUEST                            0x051BB438     88B
  SMSG_LOSTLAND_EXIT_RESPONSE                           0x051BB57C     72B
  SMSG_LOSTLAND_HERO_VOTE_COUNT_REQUEST                 0x051BFC10    104B
  SMSG_LOSTLAND_HERO_VOTE_COUNT_RETURN                  0x051BFEB8    744B
  SMSG_LOSTLAND_HISTORY_REQUEST                         0x051BBE68     88B
  SMSG_LOSTLAND_HISTORY_RETURN                          0x051BC2E4   1008B
  SMSG_LOSTLAND_LEAGUE_BUILD_REQUEST                    0x051B9D10    104B
  SMSG_LOSTLAND_LEAGUE_HISTORY_REQUEST                  0x051BC7F8     88B
  SMSG_LOSTLAND_LEAGUE_HISTORY_RETURN                   0x051BCC1C   1140B
  SMSG_LOSTLAND_LEAGUE_RANK_REQUEST                     0x051BE5B8     88B
  SMSG_LOSTLAND_LEAGUE_RANK_RETURN                      0x051BEAE4   1220B
  SMSG_LOSTLAND_MAPINFO_REQUEST                         0x051B9A3C     72B
  SMSG_LOSTLAND_MARK_REWARD_REQUEST                     0x051BA1FC    120B
  SMSG_LOSTLAND_MARK_REWARD_RETURN                      0x051BA398     88B
  SMSG_LOSTLAND_MATCH_INFO_REQUEST                      0x051B76E8     72B
  SMSG_LOSTLAND_MATCH_INFO_RESPONSE                     0x051B79C0    704B
  SMSG_LOSTLAND_OCC_CENTER_DOMIINON                     0x051C0794    340B
  SMSG_LOSTLAND_OCC_CEN_CITY_LEAGUE                     0x051C02BC     88B
  SMSG_LOSTLAND_OCC_DOMIINON_LEAGUE                     0x051C0508    152B
  SMSG_LOSTLAND_PLAYER_HISTORY_REQUEST                  0x051BD1B4     88B
  SMSG_LOSTLAND_PLAYER_HISTORY_RETURN                   0x051BD614   1160B
  SMSG_LOSTLAND_PLAYER_RANK_REQUEST                     0x051BF0C8     88B
  SMSG_LOSTLAND_PLAYER_RANK_RETURN                      0x051BF5F4   1220B
  SMSG_LOSTLAND_POINT_REQUEST                           0x051BA544    104B
  SMSG_LOSTLAND_POINT_RESPONSE                          0x051BACA0   1656B
  SMSG_LOSTLAND_RUSH_EVENT_RANK_REQUEST                 0x04FA72E0    104B
  SMSG_LOSTLAND_RUSH_EVENT_RANK_RETURN                  0x04FA77EC   1256B
  SMSG_LOSTLAND_RUSH_EVENT_REQUEST                      0x04FA6F64    104B
  SMSG_LOSTLAND_RUSH_EVENT_RETURN                       0x04FA7120    104B
  SMSG_LOSTLAND_RUSH_EVENT_SYNC_MARK                    0x04FA800C    564B
  SMSG_LOSTLAND_SELF_DOMINION_REQUEST                   0x051B9B70     72B
  SMSG_LOSTLAND_SIGN_INFO_UPDATE_REQUEST                0x051B7D40     56B
  SMSG_LOSTLAND_SIGN_INFO_UPDATE_RESPONSE               0x051B7E94     88B
  SMSG_LOST_ERA_TASK_DATA_REQUEST                       0x051A2748    104B
  SMSG_LOST_ERA_TASK_DATA_RETURN                        0x051A2B18    856B
  SMSG_LOST_ERA_TASK_LEAGUE_UPDATE                      0x051A4D88   1416B
  SMSG_LOST_ERA_TASK_LEAGUE_UPDATE_REQUEST              0x051A4224    120B
  SMSG_LOST_ERA_TASK_LEAGUE_UPDATE_RETURN               0x051A4550    528B
  SMSG_LOST_ERA_TASK_RECEIVE_REQUEST                    0x051A3000    120B
  SMSG_LOST_ERA_TASK_RECEIVE_RETURN                     0x051A3274    152B
  SMSG_LOST_ERA_TASK_UPDATE                             0x051A21E8   1028B
  SMSG_LOST_ERA_TASK_UPDATE_REQUEST                     0x051A1828    816B
  SMSG_LOST_ERA_TASK_VIEW_REQUEST                       0x051A349C    120B
  SMSG_LOST_ERA_TASK_VIEW_RETURN                        0x051A3AA0   1408B
  SMSG_LOST_LADN_ADD_VALUE                              0x051C64D4     88B
  SMSG_LOTTERY_BETTING                                  0x051CB68C    544B
  SMSG_LOTTERY_BETTING_LOCK_CODE                        0x051CE0F0    136B
  SMSG_LOTTERY_BETTING_LOCK_CODE_RETURN                 0x051CE370    152B
  SMSG_LOTTERY_BETTING_RETURN                           0x051CBB8C    516B
  SMSG_LOTTERY_BETTING_SYN                              0x051CDA50    136B
  SMSG_LOTTERY_BETTING_SYN_RETURN                       0x051CDD4C    484B
  SMSG_LOTTERY_BETTING_UNLOCK                           0x051CE55C    104B
  SMSG_LOTTERY_CUR_STAGE_INFO                           0x051CBEE4    104B
  SMSG_LOTTERY_CUR_STAGE_INFO_RETURN                    0x051CC1D4    712B
  SMSG_LOTTERY_INFO                                     0x051CAADC    732B
  SMSG_LOTTERY_INFO_RETURN                              0x051CB040    712B
  SMSG_LOTTERY_OPEN_AWARD                               0x051CC5F0    104B
  SMSG_LOTTERY_OPEN_AWARD_HISTORY                       0x051CCFE8    104B
  SMSG_LOTTERY_OPEN_AWARD_HISTORY_RETURN                0x051CD4E4    936B
  SMSG_LOTTERY_OPEN_AWARD_RETURN                        0x051CCAEC    936B
  SMSG_LOTTERY_SEND_AWARD                               0x051CE7BC    152B
  SMSG_LUCKY_RED_PACK_DETAILED_INFO_REQUEST             0x051DB7C0    120B
  SMSG_LUCKY_RED_PACK_INFO                              0x051DC958     88B
  SMSG_LUCKY_RED_PACK_INFO_RETURN                       0x051DCC20    772B
  SMSG_LUCKY_RED_PACK_THANK_REQUEST                     0x051DD744   1316B
  SMSG_LUCKY_RED_PACK_THANK_RETURN                      0x051DDDBC    104B
  SMSG_MAILBOX_MAIL                                     0x051E7410   1968B
  SMSG_MAP_ROUTE_CLIENT                                 0x05218090     72B
  SMSG_MARCH_ACCELERATE                                 0x0522121C    104B
  SMSG_MARCH_INFORMATION_REQUEST                        0x05180794   1164B
  SMSG_MARCH_INFORMATION_RESPONSE                       0x05180E20    368B
  SMSG_MARCH_INFO_REQUEST                               0x0517EF44    152B
  SMSG_MARCH_INFO_RETURN                                0x0517F2B0    416B
  SMSG_MARCH_LEADER_CHANGE                              0x0517FCB0    616B
  SMSG_MARKET_SUPPORT_RESOURCE                          0x0531B660    516B
  SMSG_MATCH_INFO_REQUEST                               0x05240678     72B
  SMSG_MATCH_INFO_RETURN                                0x05240A00    520B
  SMSG_MERGE_GAME_GIFT_DETAILED_INFO_REQUEST            0x05249D0C    120B
  SMSG_MINI_GAME_ADD_VALUE                              0x0524D1EC    104B
  SMSG_MINI_GAME_PLAYER_REQUEST                         0x0524D4EC    372B
  SMSG_MINI_GAME_RANK_REQUEST                           0x0524D7F0    120B
  SMSG_MINI_GAME_RANK_RETURN                            0x0524DB70    660B
  SMSG_MINI_GAME_STATISTICS                             0x0524DF58    104B
  SMSG_MINI_GAME_WIN                                    0x0524D020    120B
  SMSG_MOBILIZATION_ACTION_RANK_REQUEST                 0x05253F2C    120B
  SMSG_MOBILIZATION_ACTION_RANK_RETURN                  0x0525441C   1100B
  SMSG_MOBILIZATION_MATCH_INFO_REQUEST                  0x052552CC     72B
  SMSG_MOBILIZATION_MATCH_INFO_RESPONSE                 0x05255510    556B
  SMSG_MODIFY_LOSTLAND_ACTION_VALUE                     0x051B9620    816B
  SMSG_MODIFY_MARCH_RESOURCE                            0x05216568   1340B
  SMSG_MOVE_CASTLE                                      0x0521B2CC    120B
  SMSG_NAME_CHANGE                                      0x052917A8    324B
  SMSG_NEWS_RANK_INFO_REQUEST                           0x0525E6E8    580B
  SMSG_NEWS_RANK_INFO_RETURN                            0x0525ECB4    580B
  SMSG_NOTIFY_ATTACK_CASTLE_MOVE                        0x05229AAC    340B
  SMSG_NOTIFY_DEFEND_BY_ATTACK                          0x0527DD6C    912B
  SMSG_NOTIFY_EXIT_BUILDUP                              0x05226A50     88B
  SMSG_NOTIFY_HARBOR_MARCH_TIME                         0x0522395C    104B
  SMSG_NOTIFY_INC_BATTLE_VERSION                        0x0510F2B8     72B
  SMSG_NOTIFY_LEGION_CHANGE_POS_TIMES                   0x0512B478     88B
  SMSG_NOTIFY_REFLUSH_CASTLE                            0x052237BC     72B
  SMSG_NOTIFY_SERVER_ID_CHANGE                          0x052EE1B0     88B
  SMSG_OPEN_LOGIN_REQUEST                               0x052EED78     72B
  SMSG_OPEN_SESAME_RANK_REQUEST                         0x0526A778    120B
  SMSG_OPEN_SESAME_RANK_RETURN                          0x0526AD10   1208B
  SMSG_OPERATION_ACTION_BEGIN                           0x0526FFD0     88B
  SMSG_OPERATION_ACTION_END                             0x0526FE6C     72B
  SMSG_OPERATION_ACTION_RANK_RECORD_REQUEST             0x0526EC4C    104B
  SMSG_OPERATION_ACTION_RANK_RECORD_RETURN              0x0526F074   1056B
  SMSG_OTHER_MAP_LEAGUE_CHAT_MSG_SYNC                   0x05234478    356B
  SMSG_OTHER_MAP_LEAGUE_SIMPLE_INFO_REQUEST             0x05233C9C    120B
  SMSG_OTHER_MAP_LEAGUE_SIMPLE_INFO_RESPONSE            0x05234014    548B
  SMSG_OTHER_MAP_SYNC_DOMINION_DEFEND_INFO_REQUEST      0x05232A0C     88B
  SMSG_OTHER_MAP_SYNC_DOMINION_DEFEND_INFO_RESPONSE     0x05232E3C   1224B
  SMSG_OTHER_MAP_SYNC_KING_CHESS_DEFEND_INFO_REQUEST    0x050D7124     88B
  SMSG_OTHER_MAP_SYNC_KING_CHESS_DEFEND_INFO_RESPONSE   0x050D7550   1224B
  SMSG_PET_GET_NAMEPLATE_INFO_REQUEST                   0x0527A310    104B
  SMSG_PET_GET_NAMEPLATE_INFO_RESPONSE                  0x0527A794    756B
  SMSG_PLACEMENT_COMPENSATE                             0x05230E18    104B
  SMSG_PLAYER_BE_KICK_MARCH                             0x05220BE8   1244B
  SMSG_PLAYER_CASTLE_REGIST_INFO                        0x052EAC74    104B
  SMSG_PLAYER_INVALID                                   0x0524A914     88B
  SMSG_PLAYER_INVALID_RESULT                            0x0524AA58     72B
  SMSG_PLAYER_LOGIN                                     0x0521BE5C   1728B
  SMSG_PLAYER_LOGOUT                                    0x0521B430     72B
  SMSG_PLAYER_MIGRATE                                   0x0524A3D4    744B
  SMSG_PLAYER_MIGRATE_CHECK                             0x0524ABFC    104B
  SMSG_PLAYER_MIGRATE_CHECK_RESULT                      0x0524ADC0    104B
  SMSG_PLAYER_MIGRATE_GET_RANK                          0x0524AF10     72B
  SMSG_PLAYER_MIGRATE_GET_RANK_RESULT                   0x0524B078     88B
  SMSG_PLAYER_MIGRATE_RESULT                            0x0524A7A8     72B
  SMSG_PLAYER_OFFLINE                                   0x04FBD3C8    104B
  SMSG_PLAYER_ONLINE                                    0x04FBD1FC    120B
  SMSG_POWER_CHANGE                                     0x05241CC4     88B
  SMSG_PROTECT_TIME_CHANGE                              0x05241E3C     88B
  SMSG_PUSH_MESSAGE_REQUEST                             0x05284A50    372B
  SMSG_PUSH_MESSAGE_RESPONSE                            0x05284E04    356B
  SMSG_PUSH_MSG                                         0x05233490    120B
  SMSG_QUERY_HARBOR_MARCH                               0x05236FA8    104B
  SMSG_QUERY_LEAGUEBUILD_DEFEND_INFO                    0x0516375C    104B
  SMSG_QUERY_LEAGUE_BATTLE_FIELD_COUNT_REQUEST          0x05145E08     72B
  SMSG_QUERY_MAP                                        0x05227534    104B
  SMSG_QUERY_MARCH_ARMY_INFO                            0x05227AB4    104B
  SMSG_QUERY_NAME_INFO                                  0x0531114C    104B
  SMSG_QUERY_OTHER_SERVER_ALL_DOMINION_INFO             0x05223500     88B
  SMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_REQUEST     0x050424A0     88B
  SMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_RETURN      0x05042950   1120B
  SMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_REQUEST    0x05041A7C     88B
  SMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_RETURN     0x05041F20   1124B
  SMSG_QUERY_SERVER_KING_INFO_REQUEST                   0x05040880     88B
  SMSG_QUERY_SERVER_KING_INFO_RETURN                    0x0503FC1C    796B
  SMSG_QUERY_lEAGUE_BUILD_DESTORY_INFO                  0x0516441C    104B
  SMSG_RAID_PLAYER_INFO_REQUEST                         0x0523F924    120B
  SMSG_RAID_PLAYER_INFO_RETURN                          0x052400BC   1232B
  SMSG_RAID_PLAYER_REQUEST                              0x0523F4D0    120B
  SMSG_RAID_PLAYER_RETURN                               0x0523F708    136B
  SMSG_RANKINGS_FLAG                                    0x0528DCB4    104B
  SMSG_RANKINGS_MIN_VALUE                               0x0528DB04     88B
  SMSG_RANK_INFO_REQUEST                                0x0528D960    136B
  SMSG_RANK_OTHER_SERVER_SIMPLE_INFO_REQUEST            0x0528CC8C    840B
  SMSG_RANK_OTHER_SERVER_SIMPLE_INFO_RETURN             0x0528D324    840B
  SMSG_RANK_SIMPLE_INFO_REQUEST                         0x0528C068    524B
  SMSG_RANK_SIMPLE_INFO_RETURN                          0x0528C5EC    868B
  SMSG_RECEIVE_LUCKY_RED_PACK_NOTICE                    0x051DE014    340B
  SMSG_RECEIVE_LUCKY_RED_PACK_REQUEST                   0x051DB1D0    404B
  SMSG_RECEIVE_LUCKY_RED_PACK_RETURN                    0x051DB58C    168B
  SMSG_RECEIVE_MERGE_GAME_GIFT_REQUEST                  0x05249740    632B
  SMSG_RECEIVE_MERGE_GAME_GIFT_RETURN                   0x05249B10    104B
  SMSG_RED_PAPER_ADD_COIN_REQUEST                       0x052AB58C    200B
  SMSG_RED_PAPER_ADD_COIN_RETURN                        0x052AB8B0    184B
  SMSG_RED_PAPER_CHANGE_VIEW                            0x052AD590    104B
  SMSG_RED_PAPER_CHECK_ROOM_INFO_REQUEST                0x052ABB30    136B
  SMSG_RED_PAPER_CHECK_ROOM_INFO_RETURN                 0x052AC3E8   1772B
  SMSG_RED_PAPER_CREATE_ROOM_REQUEST                    0x052A2CEC    404B
  SMSG_RED_PAPER_CREATE_ROOM_RETURN                     0x052A331C    960B
  SMSG_RED_PAPER_GAME_END                               0x052AADDC    136B
  SMSG_RED_PAPER_GAME_START                             0x052AAB7C    152B
  SMSG_RED_PAPER_INVITE_PLAYER                          0x052ACF8C    820B
  SMSG_RED_PAPER_JOIN_GAME_REQUEST                      0x052A5FCC    420B
  SMSG_RED_PAPER_JOIN_GAME_RETURN                       0x052A696C   1768B
  SMSG_RED_PAPER_OEPN_INFO                              0x052A9BA0   1348B
  SMSG_RED_PAPER_OFF_LINE                               0x052ACBF8     88B
  SMSG_RED_PAPER_OPEN_REQUEST                           0x052A8A40    120B
  SMSG_RED_PAPER_OPEN_RETURN                            0x052A8CB0    152B
  SMSG_RED_PAPER_PLAYER_COUNT_REQUEST                   0x052A2540    104B
  SMSG_RED_PAPER_PLAYER_COUNT_RETURN                    0x052A27F4    480B
  SMSG_RED_PAPER_QUICK_GAME_REQUEST                     0x052A4C08    404B
  SMSG_RED_PAPER_QUICK_GAME_RETURN                      0x052A5598   1768B
  SMSG_RED_PAPER_QUIT_GAME_REQUEST                      0x052AA6AC    136B
  SMSG_RED_PAPER_QUIT_GAME_RETURN                       0x052AA8F8    136B
  SMSG_RED_PAPER_QUIT_VIEW                              0x052AD3DC     88B
  SMSG_RED_PAPER_RECORD_REQUEST                         0x052A8ED4    120B
  SMSG_RED_PAPER_RECORD_RETURN                          0x052A9354    948B
  SMSG_RED_PAPER_REPLACE_TO_GAME_REQUEST                0x052AB024    136B
  SMSG_RED_PAPER_REPLACE_TO_GAME_RETURN                 0x052AB270    136B
  SMSG_RED_PAPER_ROOM_DETAIL_REQUEST                    0x052A71A8    104B
  SMSG_RED_PAPER_ROOM_DETAIL_RETURN                     0x052A79D8   1744B
  SMSG_RED_PAPER_ROOM_INFO_REQUEST                      0x052A386C    120B
  SMSG_RED_PAPER_ROOM_INFO_RETURN                       0x052A3F1C   2516B
  SMSG_RED_PAPER_ROOM_TYPE_REQUEST                      0x052AA238    104B
  SMSG_RED_PAPER_ROOM_TYPE_RETURN                       0x052AA464    136B
  SMSG_RED_PAPER_SIMP_RECORD_REQUEST                    0x052AD750    104B
  SMSG_RED_PAPER_SIMP_RECORD_RETURN                     0x052ADA70    636B
  SMSG_RED_PAPER_UPDATE_GAME                            0x052A84D8    988B
  SMSG_REFRESH_BOSS                                     0x04FC9C30    440B
  SMSG_RELOAD_AS_XML_REQUEST                            0x052EF074    428B
  SMSG_RELOAD_AS_XML_RETURN                             0x052EF3DC    452B
  SMSG_RELOAD_LLS_XML_REQUEST                           0x052EFDCC    428B
  SMSG_RELOAD_LLS_XML_RETURN                            0x052F0134    452B
  SMSG_RELOAD_LS_XML_REQUEST                            0x052F0478    428B
  SMSG_RELOAD_LS_XML_RETURN                             0x052F07E0    452B
  SMSG_RELOAD_MS_XML_REQUEST                            0x052EF720    428B
  SMSG_RELOAD_MS_XML_RETURN                             0x052EFA88    452B
  SMSG_RELOAD_XML_REQUEST                               0x052EE388    428B
  SMSG_RELOAD_XML_RETURN                                0x052EE6F0    452B
  SMSG_REMOTE_HARBOR_MARCH_BACK                         0x05236DD8    120B
  SMSG_REQUEST_ACCUMLATION_ACTION_RANK                  0x04F9DBE0    120B
  SMSG_REQUEST_BUILDUP_BATTLE_MOVE_TIME                 0x05229860     88B
  SMSG_REQUEST_CASTLE_COUNT                             0x05241874     56B
  SMSG_REQUEST_CYCLE_ACTION_INFO                        0x0501D350     72B
  SMSG_REQUEST_CYCLE_ACTION_RANK                        0x0501C384    136B
  SMSG_REQUEST_KINGDOM_ACTION_RANK                      0x050DE2B8    136B
  SMSG_REQUEST_LEAGUEPASS_ACTION_INFO                   0x0516F6E4     72B
  SMSG_REQUEST_MARCH_ID                                 0x05228998     72B
  SMSG_REQUEST_MARCH_INFO                               0x0522873C    368B
  SMSG_REQUEST_MOBILIZATION_ACTION_INFO                 0x0525371C     72B
  SMSG_REQUEST_MONSTER_POS                              0x051C6338    120B
  SMSG_REQUEST_MOVE_CASTLE_CHECK                        0x052294D4    104B
  SMSG_REQUEST_OPERATION_ACTION_RANK                    0x0526E218    136B
  SMSG_REQUEST_OTHER_SERVER_LEAGUE_INFO                 0x05104C60    104B
  SMSG_REQUEST_OTHER_SERVER_LEAGUE_MEMBER               0x05104E24    104B
  SMSG_REQUEST_PLACEMENT_TYPE_ID                        0x05230B48     72B
  SMSG_REQUEST_RESOURCE_TYPE                            0x0522244C     88B
  SMSG_REQUEST_RPC                                      0x052B0AE0    104B
  SMSG_REQUEST_RPC_EXTRA                                0x052B0FA4    136B
  SMSG_REQUEST_SERVER_ID                                0x052ECA50    104B
  SMSG_REQUEST_WORLD_DOMINION_PLAYER_INFO               0x051051DC    672B
  SMSG_REQUEST_WORLD_PLAYER_INFO                        0x05105920   1080B
  SMSG_RESOURCE_COLLECT                                 0x0521FE64    232B
  SMSG_RESPONSE_ACCUMLATION_ACTION_RANK                 0x04F9DE1C    136B
  SMSG_RESPONSE_CASTLE_COUNT                            0x05241994     72B
  SMSG_RESPONSE_CYCLE_ACTION_RANK                       0x0501D1E0    136B
  SMSG_RESPONSE_KINGDOM_ACTION_RANK                     0x050DE504    136B
  SMSG_RESPONSE_MARCH_ID                                0x05228BB4    336B
  SMSG_RESPONSE_MARCH_INFO                              0x0527D714    608B
  SMSG_RESPONSE_MOVE_CASTLE_CHECK                       0x052296C8    120B
  SMSG_RESPONSE_OPERATION_ACTION_RANK                   0x0526E464    136B
  SMSG_RESPONSE_PLACEMENT_TYPE_ID                       0x05230C78     72B
  SMSG_RESPONSE_RESOURCE_TYPE                           0x0522258C     72B
  SMSG_RESPONSE_RPC                                     0x052B0DA4     72B
  SMSG_RESPONSE_RPC_EXTRA                               0x052B12E0    120B
  SMSG_RESPONSE_WORLD_DOMINION_PLAYER_INFO              0x0510E008   1620B
  SMSG_RESPONSE_WORLD_PLAYER_INFO                       0x0510ECA0   1324B
  SMSG_RESP_SERVER_ONLINE_NUM                           0x052F0F44    548B
  SMSG_RETURN_ONLINE_PLAYER                             0x052ECF24    532B
  SMSG_RETURN_SERVER_ID                                 0x052ECBDC     88B
  SMSG_ROUTE_CHAT_All_SERVER_MSG                        0x04FDF87C   1456B
  SMSG_ROUTE_CHAT_BLOCK_UPDATE                          0x04FDE7E0    104B
  SMSG_ROUTE_CHAT_BLOCK_UPDATE_RETURN                   0x04FDEBFC    644B
  SMSG_ROUTE_CHAT_HISTORY_REQUEST                       0x04FE2358    396B
  SMSG_ROUTE_CHAT_LEAGUE_BROADCAST                      0x04FE17E0   1796B
  SMSG_ROUTE_CHAT_MSG                                   0x04FDDDCC   1508B
  SMSG_ROUTE_CHAT_MSG_RETURN                            0x04FDE5DC    168B
  SMSG_ROUTE_CHAT_READ_SHARE_MAIL_CHECK                 0x04FE2004     88B
  SMSG_ROUTE_CHAT_READ_SHARE_MAIL_CHECK_RETURN          0x04FE2144     72B
  SMSG_ROUTE_CHAT_WORLD_BATTLE_BROADCAST                0x04FE0784   1796B
  SMSG_ROUTE_LEAVE_WORD_MSG                             0x04FC8984    840B
  SMSG_ROUTE_LEAVE_WORD_MSG_RETURN                      0x04FC8E5C    120B
  SMSG_ROUTE_OTHER_SERVER_CLIENT                        0x052370FC     72B
  SMSG_ROUTING_BATTLE_DETAIL_REPORT                     0x051E6034    500B
  SMSG_SECRET_TASKS_BEGIN_REQUEST                       0x052C0C24    568B
  SMSG_SECRET_TASKS_BEGIN_RETURN                        0x052C1100    568B
  SMSG_SECRET_TASKS_SET_POS_REQUEST                     0x052BFED0    168B
  SMSG_SECRET_TASKS_SET_POS_RETURN                      0x052C0134    136B
  SMSG_SEND_GAMEPM_REQUEST                              0x052EE99C     72B
  SMSG_SEND_GAMEPM_RETURN                               0x052EEB04     88B
  SMSG_SEND_KING_CHESS_BATTLE_COUNT                     0x050D6264     88B
  SMSG_SEND_LUCKY_RED_PACK_REQUEST                      0x051D9DF8   3140B
  SMSG_SEND_LUCKY_RED_PACK_RETURN                       0x051DAD08    432B
  SMSG_SERVER_CONNECTION_STATUS_REQUEST                 0x052DB1EC     72B
  SMSG_SERVER_CONNECTION_STATUS_RETURN                  0x052DB31C     72B
  SMSG_SERVER_EXIT                                      0x052C244C     72B
  SMSG_SERVER_ID_CHANGE                                 0x05292D74    104B
  SMSG_SERVER_ID_REQUEST                                0x052B1444     72B
  SMSG_SERVER_ID_RESPONSE                               0x052B15B0     88B
  SMSG_SERVER_ID_SET_REQUEST                            0x052B17A0    376B
  SMSG_SERVER_ID_SET_RESPONSE                           0x052B1AF8    464B
  SMSG_SET_ACTIVITY_MONSTER                             0x05229E64     72B
  SMSG_SET_NEXT_ALINE_MONSTER                           0x0522B08C     56B
  SMSG_SET_PLAYER_JOIN_KING_CHESS                       0x050D67D4    120B
  SMSG_SET_USER_INFO_VALIDITY_REQUEST                   0x05060650     88B
  SMSG_SET_USER_INFO_VALIDITY_RETURN                    0x05060794     72B
  SMSG_SET_WARTIMESTAMP                                 0x0522B3DC     72B
  SMSG_SKILL_ATTACK_BY_SAME_MAP_REQUEST                 0x0522FC80    592B
  SMSG_SMSG_GET_OTHER_BYNAME_REQUEST                    0x05060A2C    416B
  SMSG_SMSG_GET_OTHER_BYNAME_RETURN                     0x05060CEC     88B
  SMSG_SOLDIER_UP_LEVEL_UPDATE                          0x052CEFF8    524B
  SMSG_SOLDIER_UP_TALENT_UPDATE                         0x052CEB58    480B
  SMSG_STAKE_ADD_GOLD                                   0x052D51F4    120B
  SMSG_STAKE_DELETE_GOLD_PER_REQUEST                    0x052D4A54    448B
  SMSG_STAKE_DELETE_GOLD_PER_RETURN                     0x052D4EE4    388B
  SMSG_STAKE_INFO_REQUEST                               0x052D3FDC    104B
  SMSG_STAKE_INFO_RETURN                                0x052D4408    812B
  SMSG_START_BUILDUP                                    0x0521964C   1252B
  SMSG_START_DEFEND                                     0x0521A9C4   1028B
  SMSG_START_DOMINION_TRADE_MARCH                       0x0504DADC    940B
  SMSG_START_INVESTIGATION                              0x05228FC4    120B
  SMSG_START_KNIGHT_MARCH                               0x050E98E8    964B
  SMSG_START_LOOK_OTHER_SERVER                          0x052373B4    432B
  SMSG_START_MARCH                                      0x05218A74   1280B
  SMSG_START_THIRDFORCE_MARCH                           0x05222A88    916B
  SMSG_SUPPORT_ADD_RESOURCE                             0x0531BA58    388B
  SMSG_SUPPORT_RESOURCE_RESULT                          0x05224B64    120B
  SMSG_SYNC_ACCUMLATION_MARK                            0x04F9E06C    136B
  SMSG_SYNC_ACCUMULATION_ACTION_RANK                    0x04F9D840    532B
  SMSG_SYNC_ACTIVITY_RUSH_EVENT_RANK                    0x04FA859C    916B
  SMSG_SYNC_ALLFORONE_ACTION_INFO                       0x04FABC34    136B
  SMSG_SYNC_ANNIVERSARY_DONATE_INFO                     0x0527B9B0    104B
  SMSG_SYNC_ARENA_CUP                                   0x04FB47B8    676B
  SMSG_SYNC_AUTO_JOIN_LEAGUE_BATTLE                     0x0515049C    136B
  SMSG_SYNC_CASTLE_FIRE_TIME                            0x05227384     88B
  SMSG_SYNC_CASTLE_PET_SKILL_END_TIME                   0x05235F1C    104B
  SMSG_SYNC_CASTLE_SLOW_MARCH_TIME                      0x05235D6C     88B
  SMSG_SYNC_CHAMPIONSHIP_ACTION_INFO                    0x04FD5A04   1204B
  SMSG_SYNC_CLANPK_ACTION_INFO                          0x050074C4    120B
  SMSG_SYNC_CLANPK_DEFEND_INFO                          0x0500A8AC   2868B
  SMSG_SYNC_CLANPK_FINAL_DETAIL_INFO                    0x0500C190   1396B
  SMSG_SYNC_COMMON_ACTION_MARK                          0x052F41C4    564B
  SMSG_SYNC_COMMON_ACTION_RANK                          0x052F55C4    916B
  SMSG_SYNC_CROSS_ADD_INIT_SCORE                        0x050E2044     56B
  SMSG_SYNC_CROSS_BATTLE_MATCH_SERVERINFO               0x050E225C    460B
  SMSG_SYNC_CROSS_CYCLE_ACTION_MARK                     0x0501C7C0    596B
  SMSG_SYNC_CYCLE_ACTION_INFO                           0x0501E630   3236B
  SMSG_SYNC_CYCLE_ACTION_MARK                           0x0501CDC8    596B
  SMSG_SYNC_CYCLE_ACTION_RANK                           0x0501D7D4   1580B
  SMSG_SYNC_DRIVE_ENTER_DOMINION                        0x05055488     88B
  SMSG_SYNC_EXIT_BATTLE                                 0x05226C30    120B
  SMSG_SYNC_EXIT_BATTLE_KING_CHESS                      0x050D4088    120B
  SMSG_SYNC_FORCE_POWER_INFO_REQUEST                    0x0531209C     72B
  SMSG_SYNC_FORTRESS_ACTION_INFO                        0x05076134    120B
  SMSG_SYNC_FORTRESS_ACTION_MARK                        0x05076B24    596B
  SMSG_SYNC_FORTRESS_ACTION_MRAK_REWARD                 0x05077F78    468B
  SMSG_SYNC_FORTRESS_ACTION_RANK                        0x050770C4   1392B
  SMSG_SYNC_FORTRESS_ACTION_USER_RANK                   0x05077848    556B
  SMSG_SYNC_FORTRESS_DISTRIBUTE_REWARD_TIME_OUT         0x050782E8    428B
  SMSG_SYNC_FRIEND                                      0x05085B20    484B
  SMSG_SYNC_FRIEND_ADD                                  0x05086004    780B
  SMSG_SYNC_FRIEND_DEL                                  0x050864D0    484B
  SMSG_SYNC_FRIEND_USER_INFO                            0x050856B4    684B
  SMSG_SYNC_GENERAL_ACTIBITIES_MARK                     0x0508A6BC    564B
  SMSG_SYNC_GENERAL_ACTIBITIES_RANK                     0x0508B9B0    644B
  SMSG_SYNC_GUILD_STANDOFF_DUEL_RESULT                  0x050A9654   1240B
  SMSG_SYNC_HEARTBEAT                                   0x05020FE4     88B
  SMSG_SYNC_JOIN_BATTLE                                 0x052220E4    136B
  SMSG_SYNC_JOIN_BATTLE_KING_CHESS                      0x050D3E70    136B
  SMSG_SYNC_KINGDOM_ACTION_INFO                         0x050DF080    120B
  SMSG_SYNC_KINGDOM_ACTION_RANK                         0x050DF2E8    532B
  SMSG_SYNC_KINGDOM_ACTION_VALUE                        0x050DF8A0    168B
  SMSG_SYNC_KING_CHESS_ACTION_INFO                      0x050CFDA0    120B
  SMSG_SYNC_KING_CHESS_ACTION_MARK                      0x050D0978    596B
  SMSG_SYNC_KING_CHESS_ACTION_PLAYER_REWARD             0x050D648C    456B
  SMSG_SYNC_KING_CHESS_ACTION_RANK                      0x050D0D88    500B
  SMSG_SYNC_KING_CHESS_DEFEND_VERSION                   0x050D5CD8    104B
  SMSG_SYNC_KNIGHT_ACTION_INFO                          0x050DFC10    120B
  SMSG_SYNC_KNIGHT_ACTION_MARK                          0x050E1508    780B
  SMSG_SYNC_KNIGHT_ACTION_RANK                          0x050E0F28    500B
  SMSG_SYNC_LEAGUEBUILD_DEFEND_INFO                     0x05163B74   1280B
  SMSG_SYNC_LEAGUEPASS_ACTION_INFO                      0x0516F584    120B
  SMSG_SYNC_LEAGUEPASS_ACTION_MARK                      0x0516FC20    964B
  SMSG_SYNC_LEAGUEPASS_ACTION_RANK                      0x05172768   1328B
  SMSG_SYNC_LEAGUE_BATTLE_FIELD_ACTION_INFO             0x0513B600    464B
  SMSG_SYNC_LEAGUE_BATTLE_FIELD_ACTION_MARK             0x0513D1D0    900B
  SMSG_SYNC_LEAGUE_BATTLE_FIELD_ACTION_RANK             0x0513D938   1588B
  SMSG_SYNC_LEAGUE_BATTLE_FIELD_REWARD_CONFIG           0x0513BA50   1108B
  SMSG_SYNC_LEAGUE_KING_CHESS_ADD                       0x050D82CC    120B
  SMSG_SYNC_LEAGUE_KING_CHESS_DEL                       0x050D7F44    512B
  SMSG_SYNC_LEGION_ACTION_MRAK_REWARD                   0x0512C3E8    452B
  SMSG_SYNC_LEGION_DISTRIBUTE_REWARD_TIME_OUT           0x0512CC0C    428B
  SMSG_SYNC_LEGION_SEASON_ACTION_RANK_REWARD            0x0514E0FC    532B
  SMSG_SYNC_LEGION_SEASON_ACTION_SCORE                  0x0514DD10    500B
  SMSG_SYNC_LEGION_SEASON_RANK_INFO                     0x05150120    436B
  SMSG_SYNC_LEGION_SEASON_RANK_MEMBER_INFO              0x0514FD6C    476B
  SMSG_SYNC_LOOP_ACTIVITY_ACTION_INFO                   0x051844A8    152B
  SMSG_SYNC_LOSTLAND_ACTION_CITY_REWARD                 0x051C1974    376B
  SMSG_SYNC_LOSTLAND_ACTION_INFO                        0x051B6FD4    796B
  SMSG_SYNC_LOSTLAND_ACTION_LEAGUE_RANK                 0x051C11F4    492B
  SMSG_SYNC_LOSTLAND_ACTION_MARK                        0x051B8DB8    816B
  SMSG_SYNC_LOSTLAND_ACTION_PLAYER_RANK                 0x051C15D0    524B
  SMSG_SYNC_LOSTLAND_ACTION_PRE_RANK                    0x051C0AA4    492B
  SMSG_SYNC_LOSTLAND_ACTION_RANK                        0x051C0E4C    492B
  SMSG_SYNC_LOSTLAND_BAN_HERO_INFO                      0x051B7488    376B
  SMSG_SYNC_LOSTLAND_DOMINION_NOTIFY                    0x051C2450    416B
  SMSG_SYNC_LOSTLAND_DOMINION_REWARD                    0x051C1D80   1228B
  SMSG_SYNC_LOSTLAND_OCC_LEAGUE_NAME                    0x051C29E0    324B
  SMSG_SYNC_LOSTLAND_PRE_RANK_BUFF                      0x051C27D0     72B
  SMSG_SYNC_LOSTLAND_RUSH_EVENT_RANK                    0x04FA8C8C    916B
  SMSG_SYNC_MOBILIZATION_ACTION_INFO                    0x052535BC    120B
  SMSG_SYNC_MOBILIZATION_ACTION_MARK                    0x05253B2C    624B
  SMSG_SYNC_MOBILIZATION_ACTION_RANK                    0x052562C8   1328B
  SMSG_SYNC_MOBILIZATION_REWARD_CONFIG                  0x052559C4   1096B
  SMSG_SYNC_OPENSESAME_ACTION_RANK                      0x0526BB48   1556B
  SMSG_SYNC_OPEN_SESAME_ACTION_MARK                     0x0526B58C    596B
  SMSG_SYNC_OPERATION_ACTION_INFO                       0x0526F6E0    672B
  SMSG_SYNC_OPERATION_ACTION_MARK                       0x0526E8A0    596B
  SMSG_SYNC_OPERATION_ACTION_RANK                       0x0526FB70    532B
  SMSG_SYNC_RED_PAPER_DEL_ROOM                          0x052AE2AC    484B
  SMSG_SYNC_RED_PAPER_VIEW_NUM                          0x052ADEE4    516B
  SMSG_SYNC_SERVER_INFO                                 0x052C1D94   1104B
  SMSG_SYNC_SINGLE_CYCLE_ACTION_INFO                    0x0501FA18   2388B
  SMSG_SYNC_SINGLE_OPERATION_ACTION_INFO                0x0526DFCC    136B
  SMSG_SYNC_THIRDFORCE_LEVEL                            0x05223678     88B
  SMSG_SYNC_WAR_LORD_ACTION_INFO                        0x052E8570    136B
  SMSG_SYNC_WAR_LORD_ACTION_MARK                        0x052E96A0    756B
  SMSG_SYNC_WAR_LORD_MATCH_INFO                         0x052EA244    492B
  SMSG_SYNC_WAR_LORD_RANK_REWARD                        0x052E9E9C    492B
  SMSG_SYNC_WAR_LORD_STAGE_REWARD                       0x052E9B30    432B
  SMSG_SYNC_WORLD_BATTLE_ACTION_INFO                    0x053029B8    136B
  SMSG_SYNC_WORLD_BATTLE_ACTION_MARK                    0x0530DDF8    612B
  SMSG_SYNC_WORLD_BATTLE_ACTION_PLAYER_REWARD           0x05309EAC    424B
  SMSG_SYNC_WORLD_BATTLE_ACTION_RANK                    0x0530D514   1252B
  SMSG_SYNC_WORLD_BATTLE_MATCH_INFO                     0x05302C30    608B
  SMSG_SYNC_WORLD_BATTLE_REWARD_MEMBER_INFO             0x0531BE20    476B
  SMSG_SYNC_lEAGUE_BUILD_DESTORY_INFO                   0x0516467C    152B
  SMSG_SYN_CASTLE_FLAG                                  0x05242AE4     88B
  SMSG_SYN_PLACEMENT_COUNT                              0x0522558C     72B
  SMSG_SYS_LUCKY_RED_PACK_DETAILED_INFO                 0x051DC088   1964B
  SMSG_TEST_POS_EMPTY_REQUEST                           0x052DAC4C     88B
  SMSG_TEST_POS_EMPTY_RETURN                            0x052DAD8C     72B
  SMSG_TEST_RPC_EXTRA                                   0x052B1114     72B
  SMSG_THIRDFORCE_ATTACK_DOMINION                       0x05222FAC    120B
  SMSG_THIRDFORCE_ATTACK_DOMINION_RESULT                0x052231E0    136B
  SMSG_THIRDFORCE_CANCEL_ATTACK_DOMINION                0x05223384     88B
  SMSG_TRANSFER_BY_HARBOR                               0x052175F8   2476B
  SMSG_UPDATE_BATTLE_ATK_TIME                           0x052222C4    104B
  SMSG_UPDATE_BATTLE_DST_POS                            0x05223F5C    120B
  SMSG_UPDATE_BATTLE_VERSION                            0x05236070     72B
  SMSG_UPDATE_BUILD_SPEED                               0x05160D30    104B
  SMSG_UPDATE_CAMEL                                     0x05055998    152B
  SMSG_UPDATE_CASTLE_FLAG                               0x0522DC74     88B
  SMSG_UPDATE_CASTLE_NAMEPLATE                          0x05236214    104B
  SMSG_UPDATE_CASTLE_POS                                0x0521C6A4    120B
  SMSG_UPDATE_CASTLE_SIGNATURE                          0x0522E99C    360B
  SMSG_UPDATE_CASTLE_SKIN                               0x0522DAE8    104B
  SMSG_UPDATE_CASTLE_WAR_TIMESTAMP                      0x0522EC24     88B
  SMSG_UPDATE_COLLECT_EFFECT                            0x0522705C    516B
  SMSG_UPDATE_COLLECT_RESOURCE                          0x0510D4E4    104B
  SMSG_UPDATE_DOMINION_BUILD_INFO                       0x05226E00    104B
  SMSG_UPDATE_DOMINION_INFO                             0x05226780    432B
  SMSG_UPDATE_LEAGUEBUILD                               0x0515FAF8   1236B
  SMSG_UPDATE_LEAGUEBUILD_OCCUPY_LEAGUE_ID              0x05163090     88B
  SMSG_UPDATE_LEAGUE_BOSS                               0x05156764    152B
  SMSG_UPDATE_LEAGUE_BUILDING_LEAGUE_INFO               0x05163354    688B
  SMSG_UPDATE_LEAGUE_SIMPLE_INFO                        0x05224EA4    440B
  SMSG_UPDATE_LORD_CATCH_STATE                          0x0522AB90     88B
  SMSG_UPDATE_MARCH_INFO                                0x05228108    456B
  SMSG_UPDATE_MONSTER_GROUP_ID                          0x052284EC     72B
  SMSG_UPDATE_PENDING_DEFEND_TIME                       0x05223BF8    168B
  SMSG_UPDATE_PLAYER_NUMBER_ATTR                        0x04FBCCBC    104B
  SMSG_UPDATE_PLAYER_STRING_ATTR                        0x04FBCF14    340B
  SMSG_UPDATE_SECRET_TASK                               0x052C0680     88B
  SMSG_UPDATE_SERVER_INFO                               0x052C27B4    592B
  SMSG_UPDATE_SLAVE_OFFICIAL_ID                         0x05229D24     88B
  SMSG_USE_FIRE_WORDKS                                  0x0522B2A8     72B
  SMSG_WAR_LORD_ACTION_RANK_REQUEST                     0x052E8750    104B
  SMSG_WAR_LORD_ACTION_RANK_RETURN                      0x052E8D08   1444B
  SMSG_WEB_COMMAND                                      0x052EAECC    340B
  SMSG_WEB_COMMAND_REQUEST                              0x052EB1E4    324B
  SMSG_WEB_COMMAND_RETURN                               0x052EB4EC    324B
  SMSG_WEB_LOGIN_LOG                                    0x0517DE60    356B
  SMSG_WORD_LEAGUE_RANK_DELETE                          0x0528FBB8     72B
  SMSG_WORD_LEAGUE_RANK_INFO_REQUEST                    0x0528EC64     56B
  SMSG_WORD_LEAGUE_RANK_INFO_RETURN                     0x0528F26C   2032B
  SMSG_WORD_RANK_USERINFO_REQUEST                       0x0528DE38     88B
  SMSG_WORD_RANK_USERINFO_RETURN                        0x0528E46C   1212B
  SMSG_WORLDBATTLEFIELD_ADD_EQUIP                       0x0519A968    104B
  SMSG_WORLDBATTLEFIELD_ADD_HERO_QUEUE                  0x0530C328    508B
  SMSG_WORLDBATTLEFIELD_ADD_PET                         0x053187C8    340B
  SMSG_WORLDBATTLEFIELD_BUILDING_BUILD                  0x0530A1AC    104B
  SMSG_WORLDBATTLEFIELD_BUILDING_REMOVE                 0x0530A4B4     88B
  SMSG_WORLDBATTLEFIELD_BUILDING_UPGRADE                0x0530A338     88B
  SMSG_WORLDBATTLEFIELD_CHANGE_ATTRBUTE                 0x053098FC    556B
  SMSG_WORLDBATTLEFIELD_CHANGE_EFFECT_INFO              0x0530CB70   1528B
  SMSG_WORLDBATTLEFIELD_CHANGE_EQUIP_GEM                0x0519A79C    120B
  SMSG_WORLDBATTLEFIELD_CHANGE_EQUIP_INDEX              0x0519A5A4    104B
  SMSG_WORLDBATTLEFIELD_CHANGE_EXTRA_ATTRBUTE           0x05309C84    104B
  SMSG_WORLDBATTLEFIELD_CHANGE_HERO_AMOUNT              0x05307AA4    548B
  SMSG_WORLDBATTLEFIELD_CHANGE_LORD_SKILL               0x0519EF14    136B
  SMSG_WORLDBATTLEFIELD_CHANGE_SOLDIER                  0x052CAFF4    460B
  SMSG_WORLDBATTLEFIELD_CHANGE_TRAP                     0x0530A660    104B
  SMSG_WORLDBATTLEFIELD_DELETE_HERO_QUEUE               0x0530C648     88B
  SMSG_WORLDBATTLEFIELD_ENTER_CHECK_REQUEST             0x0530E178     88B
  SMSG_WORLDBATTLEFIELD_ENTER_CHECK_RETURN              0x0530E2BC     72B
  SMSG_WORLDBATTLEFIELD_EXIT_REQUEST                    0x0530E420     88B
  SMSG_WORLDBATTLEFIELD_EXIT_RETURN                     0x0530E564     72B
  SMSG_WORLDBATTLEFIELD_HERO_AUTO_RECRUIT_FLAG          0x0530A8B4    508B
  SMSG_WORLDBATTLEFIELD_HERO_RECRUIT_DEDUCT_GLOD_REQUEST 0x05308570    912B
  SMSG_WORLDBATTLEFIELD_HERO_RECRUIT_DEDUCT_GLOD_RETURN 0x053089E8     72B
  SMSG_WORLDBATTLEFIELD_HERO_RECRUIT_REQUEST            0x05307ECC    416B
  SMSG_WORLDBATTLEFIELD_HERO_RECRUIT_RETURN             0x0530818C     88B
  SMSG_WORLDBATTLEFIELD_LOAD_PLAYER                     0x05301EA8     72B
  SMSG_WORLDBATTLEFIELD_MAIN_DEFENSE_LOSS               0x05309064   1644B
  SMSG_WORLDBATTLEFIELD_MIGRATE                         0x053022BC   1084B
  SMSG_WORLDBATTLEFIELD_PACKAGE_SET                     0x0519ACA4    340B
  SMSG_WORLDBATTLEFIELD_RESULT                          0x053027E4     72B
  SMSG_WORLDBATTLEFIELD_SOLDIER_RECRUIT                 0x052CAB60    640B
  SMSG_WORLDBATTLEFIELD_SYN_HERO_INFO                   0x0530B098   4120B
  SMSG_WORLDBATTLEFIELD_SYN_SOLDIER_INFO                0x052CA8E8     72B
  SMSG_WORLDBATTLEFIELD_UPGRADE_PET_SKILL               0x05318AD8    136B
  SMSG_WORLDBATTLE_BROADCAST_CLIENT                     0x05311350    432B
  SMSG_WORLD_ACTIVITY_STAGE_END                         0x0531A0C8     88B
  SMSG_WORLD_ACTIVITY_STAGE_START                       0x05319370   2856B
  SMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST             0x05312A88     88B
  SMSG_WORLD_BATTLEFIELD_SELF_GROUP_RETURN              0x05312FE0    820B
  SMSG_WORLD_BATTLEFIELD_SELF_RANK_REQUEST              0x05313438     88B
  SMSG_WORLD_BATTLEFIELD_SELF_RANK_RETURN               0x05313654    136B
  SMSG_WORLD_BATTLEFIELD_SYNC_BE_KICKED                 0x05318164     88B
  SMSG_WORLD_BATTLE_ACTION_DETAIL_INFO_REQUEST          0x053042EC     88B
  SMSG_WORLD_BATTLE_ACTION_DETAIL_INFO_RESPONSE         0x05304778   1064B
  SMSG_WORLD_BATTLE_ACTION_INFO_REQUEST                 0x05303884    104B
  SMSG_WORLD_BATTLE_ACTION_INFO_RESPONSE                0x05303E60    876B
  SMSG_WORLD_BATTLE_ACTION_REQUEST                      0x052EEEAC     72B
  SMSG_WORLD_BATTLE_ADD_CITY_FIRE_CD                    0x053115EC     72B
  SMSG_WORLD_BATTLE_CENTER_FORCE_ID_REQUEST             0x05311758     88B
  SMSG_WORLD_BATTLE_CENTER_FORCE_ID_RESPONSE            0x053119A4    340B
  SMSG_WORLD_BATTLE_DEL_INVALID_DATA                    0x05317FDC    104B
  SMSG_WORLD_BATTLE_DOMINION_RECORD_REQUEST             0x053128FC    104B
  SMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST                  0x05311D98     88B
  SMSG_WORLD_BATTLE_ENTER_VIEW_RETURN                   0x05311F48    104B
  SMSG_WORLD_BATTLE_FIELD_ALL_DOMINION_BATTLE_REQUEST   0x053121D0     72B
  SMSG_WORLD_BATTLE_FIELD_GET_BATTLE_INFO_REQUEST       0x0531A2EC    136B
  SMSG_WORLD_BATTLE_FIELD_GET_BATTLE_INFO_RESPONSE      0x0531AA20   1136B
  SMSG_WORLD_BATTLE_FIELD_OCCUPY_DOMINION               0x0531B084    340B
  SMSG_WORLD_BATTLE_GROUP_INFO_REQUEST                  0x05314444     88B
  SMSG_WORLD_BATTLE_GROUP_INFO_RETURN                   0x05314A78   1352B
  SMSG_WORLD_BATTLE_GROUP_MEMBER_REQUEST                0x05313838    104B
  SMSG_WORLD_BATTLE_GROUP_MEMBER_RETURN                 0x05313DEC   1332B
  SMSG_WORLD_BATTLE_GROUP_RANK_REQUEST                  0x05305724     88B
  SMSG_WORLD_BATTLE_GROUP_RANK_RESPONSE                 0x05305BB8   1192B
  SMSG_WORLD_BATTLE_JOIN_GROUP_REQUEST                  0x053165A4    860B
  SMSG_WORLD_BATTLE_JOIN_GROUP_RETURN                   0x05316E44    816B
  SMSG_WORLD_BATTLE_KICK_MEMBER_REQUEST                 0x053177F0    120B
  SMSG_WORLD_BATTLE_KICK_MEMBER_RETURN                  0x05317A30    136B
  SMSG_WORLD_BATTLE_LEAVE_GROUP_REQUEST                 0x05317C14    104B
  SMSG_WORLD_BATTLE_LEAVE_GROUP_RETURN                  0x05317E10    120B
  SMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST                 0x053154CC    876B
  SMSG_WORLD_BATTLE_NEW_SIGN_UP_RETURN                  0x05315D78    816B
  SMSG_WORLD_BATTLE_OVERLORD_RECORD_REQUEST             0x05306F58     88B
  SMSG_WORLD_BATTLE_OVERLORD_RECORD_RESPONSE            0x05307414   1128B
  SMSG_WORLD_BATTLE_PLAYER_RANK_REQUEST                 0x05304CC4     88B
  SMSG_WORLD_BATTLE_PLAYER_RANK_RESPONSE                0x05305158   1192B
  SMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_REQUEST         0x0530FD9C    420B
  SMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_RESPONSE        0x05310290    420B
  SMSG_WORLD_BATTLE_SET_POWER_REQUEST                   0x0531733C    136B
  SMSG_WORLD_BATTLE_SET_POWER_RETURN                    0x053175C8    152B
  SMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_REQUEST         0x0530F428    388B
  SMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_RESPONSE        0x0530F8BC    404B
  SMSG_WORLD_BATTLE_SIGNUP_REQUEST                      0x053032F0    648B
  SMSG_WORLD_BATTLE_SIGNUP_RESPONSE                     0x053036C8    104B
  SMSG_WORLD_BATTLE_SIGN_INFO_UPDATE_REQUEST            0x053061FC    432B
  SMSG_WORLD_BATTLE_SIGN_INFO_UPDATE_RESPONSE           0x053067E8   1088B
  SMSG_WORLD_BATTLE_SYNC_DOMINION_DEFEND_VERSION        0x0531B32C    104B
  SMSG_WORLD_BATTLE_SYNC_OFFICIAL_INFO                  0x0530EB48   1556B
  SMSG_WORLD_BATTLE_UPDATE_LEAGUE_ID                    0x05306DDC     88B
  SMSG_WORLD_BATTLE_UPDATE_OFFICIAL_SERVER_ID           0x05311C1C     88B
  SMSG_WORLD_BATTLE_UPDATE_PLAYER_OFFICIAL              0x05310AA8    388B
  SMSG_WORLD_BATTLE_UPDATE_POWER_PLAYER                 0x053183D0    516B
  SMSG_WORLD_BATTLE_UPDATE_SERVER_OFFICIAL              0x05310674    356B
  SMSG_WORLD_BATTLE_UPDATE_SIGNUP_POWER                 0x05310D84    104B
  SMSG_WORLD_GET_DEFEND_INFO_BY_PLAYERID                0x05310F7C    120B
  Second_keyXml                                         0x04F0B1C8      8B
  Second_keyXml                                         0x04F0B1D0      8B
  SecrectmonsterXml                                     0x04F0CAA0      8B
  SecrectmonsterXml                                     0x04F0CAA8      8B
  Secret_baseXml                                        0x04F0DDE8      8B
  Secret_baseXml                                        0x04F0DDF0      8B
  Secret_bossXml                                        0x04F0EEB8      8B
  Secret_bossXml                                        0x04F0EEC0      8B
  Secret_itemXml                                        0x04F0FC14      8B
  Secret_itemXml                                        0x04F0FC1C      8B
  Secret_levelXml                                       0x04F111D4      8B
  Secret_levelXml                                       0x04F111DC      8B
  Secret_taskXml                                        0x04F12AC4      8B
  Secret_taskXml                                        0x04F12ACC      8B
  Server_merge_resXml                                   0x04F13C90      8B
  Server_merge_resXml                                   0x04F13C98      8B
  Server_merge_rewardXml                                0x04F14DB0      8B
  Server_merge_rewardXml                                0x04F14DB8      8B
  Server_merge_timeXml                                  0x04F160CC      8B
  Server_merge_timeXml                                  0x04F160D4      8B
  Server_versionXml                                     0x04F16DE8      8B
  Server_versionXml                                     0x04F16DF0      8B
  Server_whitelistXml                                   0x04F17B74      8B
  Server_whitelistXml                                   0x04F17B7C      8B
  Set_buildskinXml                                      0x04F188C8      8B
  Set_buildskinXml                                      0x04F188D0      8B
  Shop_buy_oneXml                                       0x04F199B8      8B
  Shop_buy_oneXml                                       0x04F199C0      8B
  Shop_giftXml                                          0x04F1AB98      8B
  Shop_giftXml                                          0x04F1ABA0      8B
  Shop_goldXml                                          0x04F1BD08      8B
  Shop_goldXml                                          0x04F1BD10      8B
  Shop_goldXml                                          0x04F1C3EC      8B
  Shop_goldXml                                          0x04F1C3F4      8B
  Sign_in_fund_baseXml                                  0x04F1DC54      8B
  Sign_in_fund_baseXml                                  0x04F1DC5C      8B
  Sign_in_fund_configXml                                0x04F1F730      8B
  Sign_in_fund_configXml                                0x04F1F738      8B
  Sign_in_fund_configXml                                0x04F1FDC8      8B
  Sign_in_fund_configXml                                0x04F1FDD0      8B
  Sign_packageXml                                       0x04F20FFC      8B
  Sign_packageXml                                       0x04F21004      8B
  SoldierActXml                                         0x04F22F00      8B
  SoldierActXml                                         0x04F22F08      8B
  SoldierActXml                                         0x04F23558      8B
  SoldierActXml                                         0x04F23560      8B
  Soldiers_effectXml                                    0x04F24C88      8B
  Soldiers_effectXml                                    0x04F24C90      8B
  Soldiers_hero_talentXml                               0x04F26348      8B
  Soldiers_hero_talentXml                               0x04F26350      8B
  Soldiers_hero_talentXml                               0x04F269D0      8B
  Soldiers_hero_talentXml                               0x04F269D8      8B
  Soldiers_random_groupXml                              0x04F27E80      8B
  Soldiers_random_groupXml                              0x04F27E88      8B
  Soldiers_random_groupXml                              0x04F28560      8B
  Soldiers_random_groupXml                              0x04F28568      8B
  Soldiers_recruitXml                                   0x04F2A554      8B
  Soldiers_recruitXml                                   0x04F2A55C      8B
  Soldiers_recruitXml                                   0x04F2AC34      8B
  Soldiers_recruitXml                                   0x04F2AC3C      8B
  Soldiers_talent_typeXml                               0x04F2BC68      8B
  Soldiers_talent_typeXml                               0x04F2BC70      8B
  Soldiers_upXml                                        0x04F2DB80      8B
  Soldiers_upXml                                        0x04F2DB88      8B
  Soldiers_upXml                                        0x04F2E26C      8B
  Soldiers_upXml                                        0x04F2E274      8B
  Soldiers_up_globalXml                                 0x04F30034      8B
  Soldiers_up_globalXml                                 0x04F3003C      8B
  Soldiers_up_typeXml                                   0x04F31A98      8B
  Soldiers_up_typeXml                                   0x04F31AA0      8B
  Soldiers_up_typeXml                                   0x04F3221C      8B
  Soldiers_up_typeXml                                   0x04F32224      8B
  SolomonXml                                            0x04F33B3C      8B
  SolomonXml                                            0x04F33B44      8B
  Solomon_positionXml                                   0x04F34E38      8B
  Solomon_positionXml                                   0x04F34E40      8B
  Solomon_positionXml                                   0x04F35538      8B
  Solomon_positionXml                                   0x04F35540      8B
  Solomon_randomXml                                     0x04F368B4      8B
  Solomon_randomXml                                     0x04F368BC      8B
  SoulSmeltingXml                                       0x04F37658      8B
  SoulSmeltingXml                                       0x04F37660      8B
  Soul_costXml                                          0x04F383F4      8B
  Soul_costXml                                          0x04F383FC      8B
  SoultestXml                                           0x04F395AC      8B
  SoultestXml                                           0x04F395B4      8B
  Special_eventXml                                      0x04F3A594      8B
  Special_eventXml                                      0x04F3A59C      8B
  Special_event_limitXml                                0x04F3B34C      8B
  Special_event_limitXml                                0x04F3B354      8B
  Special_globalXml                                     0x04F3CC4C      8B
  Special_globalXml                                     0x04F3CC54      8B
  Special_loginXml                                      0x04F3E2C8      8B
  Special_loginXml                                      0x04F3E2D0      8B
  Special_loginXml                                      0x04F3EA9C      8B
  Special_loginXml                                      0x04F3EAA4      8B
  SpecialmailXml                                        0x04F3FF38      8B
  SpecialmailXml                                        0x04F3FF40      8B
  Subscribe_rewardXml                                   0x04F410F0      8B
  Subscribe_rewardXml                                   0x04F410F8      8B
  Super4choose1_packXml                                 0x04F4235C      8B
  Super4choose1_packXml                                 0x04F42364      8B
  Super4choose1_rewardXml                               0x04F43850      8B
  Super4choose1_rewardXml                               0x04F43858      8B
  Super4choose1_rewardXml                               0x04F43ED4      8B
  Super4choose1_rewardXml                               0x04F43EDC      8B
  SurpriseXml                                           0x04F4537C      8B
  SurpriseXml                                           0x04F45384      8B
  TURN7getDataEPKc                                      0x1A04040830300891 3874522862834493184B
  T_RETURN7getDataEPKc                                  0x412000200950000 14416094983570868240B
  T_RETURN7getDataEPKc                                  0x110900012C002482 2308239944831238656B
  T_RETURN7getDataEPKc                                  0x40310242520 9232379240404487234B
  Task_rewardXml                                        0x04F46F44      8B
  Task_rewardXml                                        0x04F46F4C      8B
  Task_settingXml                                       0x04F48070      8B
  Task_settingXml                                       0x04F48078      8B
  Task_settingXml                                       0x04F4877C      8B
  Task_settingXml                                       0x04F48784      8B
  Threedays_baseXml                                     0x04F4A45C      8B
  Threedays_baseXml                                     0x04F4A464      8B
  Threedays_baseXml                                     0x04F4AB88      8B
  Threedays_baseXml                                     0x04F4AB90      8B
  Total_recharge_rewardXml                              0x04F4C434      8B
  Total_recharge_rewardXml                              0x04F4C43C      8B
  Total_recharge_rewardXml                              0x04F4CB3C      8B
  Total_recharge_rewardXml                              0x04F4CB44      8B
  TradepricesXml                                        0x04F4DD6C      8B
  TradepricesXml                                        0x04F4DD74      8B
  TradingXml                                            0x04F4EB8C      8B
  TradingXml                                            0x04F4EB94      8B
  TreasureXml                                           0x04F4FBF0      8B
  TreasureXml                                           0x04F4FBF8      8B
  Treasure_boxXml                                       0x04F50EC4      8B
  Treasure_boxXml                                       0x04F50ECC      8B
  Treasure_boxXml                                       0x04F515C4      8B
  Treasure_boxXml                                       0x04F515CC      8B
  Treasure_cardXml                                      0x04F52924      8B
  Treasure_cardXml                                      0x04F5292C      8B
  Treasure_card_ShuffleXml                              0x04F53B4C      8B
  Treasure_card_ShuffleXml                              0x04F53B54      8B
  Treasure_card_ShuffleXml                              0x04F5422C      8B
  Treasure_card_ShuffleXml                              0x04F54234      8B
  Treasure_card_dropXml                                 0x04F5583C      8B
  Treasure_card_dropXml                                 0x04F55844      8B
  Treasure_card_dropXml                                 0x04F55EC0      8B
  Treasure_card_dropXml                                 0x04F55EC8      8B
  Treasure_card_refreshXml                              0x04F57090      8B
  Treasure_card_refreshXml                              0x04F57098      8B
  Treasure_card_skinXml                                 0x04F581DC      8B
  Treasure_card_skinXml                                 0x04F581E4      8B
  Treasure_configXml                                    0x04F58F10      8B
  Treasure_configXml                                    0x04F58F18      8B
  TributeXml                                            0x04F5A908      8B
  TributeXml                                            0x04F5A910      8B
  TributeXml                                            0x04F5AF90      8B
  TributeXml                                            0x04F5AF98      8B
  Trigger_giftXml                                       0x04F5C608      8B
  Trigger_giftXml                                       0x04F5C610      8B
  UEST7getDataEPKc                                      0x2433BAF0AA00AAEF 14604055321508378352B
  Unlock_lvXml                                          0x04F5D4D0      8B
  Unlock_lvXml                                          0x04F5D4D8      8B
  Upgrade_rewardXml                                     0x04F5E8CC      8B
  Upgrade_rewardXml                                     0x04F5E8D4      8B
  Upgrade_rewardXml                                     0x04F5EE84      8B
  Upgrade_rewardXml                                     0x04F5EE8C      8B
  UserDefinedCityXml                                    0x04F605AC      8B
  UserDefinedCityXml                                    0x04F605B4      8B
  Util11getDataInfoERNSt6__ndk113unordered_mapImP8MailInfoNS0_4hashImEENS0_8equal_toImEENS0_9allocatorINS0_4pairIKmS3_EEEEEE 0x31EC00023F83 536608918994944B
  Vip_rewardXml                                         0x04F61610      8B
  Vip_rewardXml                                         0x04F61618      8B
  WARD7getDataEPKc                                      0x8050100005000 597214034445504832B
  Warlord_eventXml                                      0x04F63B60      8B
  Warlord_eventXml                                      0x04F63B68      8B
  Warlord_phase_rank_rewardXml                          0x04F65138      8B
  Warlord_phase_rank_rewardXml                          0x04F65140      8B
  Warlord_phase_rank_rewardXml                          0x04F65840      8B
  Warlord_phase_rank_rewardXml                          0x04F65848      8B
  Warlord_phase_rewardXml                               0x04F670D8      8B
  Warlord_phase_rewardXml                               0x04F670E0      8B
  Warlord_phase_rewardXml                               0x04F677E0      8B
  Warlord_phase_rewardXml                               0x04F677E8      8B
  Warlord_pointXml                                      0x04F68CE8      8B
  Warlord_pointXml                                      0x04F68CF0      8B
  Warlord_pointXml                                      0x04F693C8      8B
  Warlord_pointXml                                      0x04F693D0      8B
  Warlord_rank_reward_singleXml                         0x04F6AB1C      8B
  Warlord_rank_reward_singleXml                         0x04F6AB24      8B
  Warlord_rank_reward_totalXml                          0x04F6C108      8B
  Warlord_rank_reward_totalXml                          0x04F6C110      8B
  Warlord_rank_reward_totalXml                          0x04F6C810      8B
  Warlord_rank_reward_totalXml                          0x04F6C818      8B
  Week_activity_typeXml                                 0x04F6DD70      8B
  Week_activity_typeXml                                 0x04F6DD78      8B
  Week_cardXml                                          0x04F6F690      8B
  Week_cardXml                                          0x04F6F698      8B
  Weekly_baseXml                                        0x04F706A0      8B
  Weekly_baseXml                                        0x04F706A8      8B
  Weekly_baseXml                                        0x04F70D30      8B
  Weekly_baseXml                                        0x04F70D38      8B
  Weekly_calendarXml                                    0x04F724E0      8B
  Weekly_calendarXml                                    0x04F724E8      8B
  Weekly_calendarXml                                    0x04F72AE8      8B
  Weekly_calendarXml                                    0x04F72AF0      8B
  Weekly_passXml                                        0x04F74C9C      8B
  Weekly_passXml                                        0x04F74CA4      8B
  Weekly_pass_getXml                                    0x04F75E18      8B
  Weekly_pass_getXml                                    0x04F75E20      8B
  Weekly_pass_lvXml                                     0x04F76E84      8B
  Weekly_pass_lvXml                                     0x04F76E8C      8B
  Weekly_pass_lvXml                                     0x04F77564      8B
  Weekly_pass_lvXml                                     0x04F7756C      8B
  Weekly_pass_rewardXml                                 0x04F79444      8B
  Weekly_pass_rewardXml                                 0x04F7944C      8B
  Weekly_pass_rewardXml                                 0x04F79ADC      8B
  Weekly_pass_rewardXml                                 0x04F79AE4      8B
  Wheel_of_giftXml                                      0x04F7B7CC      8B
  Wheel_of_giftXml                                      0x04F7B7D4      8B
  Wheel_of_gift_cycleXml                                0x04F7D4C8      8B
  Wheel_of_gift_cycleXml                                0x04F7D4D0      8B
  Wheel_of_gift_cycleXml                                0x04F7DCE4      8B
  Wheel_of_gift_cycleXml                                0x04F7DCEC      8B
  World_champion_eventXml                               0x04F7F95C      8B
  World_champion_eventXml                               0x04F7F964      8B
  World_champion_event_cityXml                          0x04F809DC      8B
  World_champion_event_cityXml                          0x04F809E4      8B
  World_champion_event_forceXml                         0x04F816E0      8B
  World_champion_event_forceXml                         0x04F816E8      8B
  World_champion_event_l_rewardXml                      0x04F82C78      8B
  World_champion_event_l_rewardXml                      0x04F82C80      8B
  World_champion_event_l_rewardXml                      0x04F83300      8B
  World_champion_event_l_rewardXml                      0x04F83308      8B
  World_champion_event_leaderXml                        0x04F844CC      8B
  World_champion_event_leaderXml                        0x04F844D4      8B
  World_champion_event_ruleXml                          0x04F85450      8B
  World_champion_event_ruleXml                          0x04F85458      8B
  World_champion_event_s_rewardXml                      0x04F86608      8B
  World_champion_event_s_rewardXml                      0x04F86610      8B
  World_champion_event_scoreXml                         0x04F87748      8B
  World_champion_event_scoreXml                         0x04F87750      8B
  World_champion_event_scoreXml                         0x04F87E1C      8B
  World_champion_event_scoreXml                         0x04F87E24      8B
  World_champion_event_t_rewardXml                      0x04F892E0      8B
  World_champion_event_t_rewardXml                      0x04F892E8      8B
  World_champion_p_titleXml                             0x04F8A2D0      8B
  World_champion_p_titleXml                             0x04F8A2D8      8B
  World_champion_powerXml                               0x04F8AFD4      8B
  World_champion_powerXml                               0x04F8AFDC      8B
  World_champion_s_titleXml                             0x04F8BFB0      8B
  World_champion_s_titleXml                             0x04F8BFB8      8B
  World_champion_titleXml                               0x04F8D0B0      8B
  World_champion_titleXml                               0x04F8D0B8      8B
  YN_UPGRADE_REWARD7getDataEPKc                         0x2200405000100 288230393332645888B
  Yahtzee_gameXml                                       0x04F8E7BC      8B
  Yahtzee_gameXml                                       0x04F8E7C4      8B
  Yahtzee_gameXml                                       0x04F8F024      8B
  Yahtzee_gameXml                                       0x04F8F02C      8B
  Yahtzee_game_pointXml                                 0x04F90240      8B
  Yahtzee_game_pointXml                                 0x04F90248      8B
  Yahtzee_game_rankXml                                  0x04F91440      8B
  Yahtzee_game_rankXml                                  0x04F91448      8B
  Yahtzee_game_rewardXml                                0x04F9260C      8B
  Yahtzee_game_rewardXml                                0x04F92614      8B
  ZN11CMailDBUtil12getDataCountEv                       0x22C8200000000 486718578942246B
  ZN16CMSG_CHARGE_INFO7getDataEPKc                      0x0000BF8E  67071B
  ZN27CMSG_BUILDING_OPERAT_RETURN7getDataEPKc           0xD02C00001320 206922934396841B
  ZN28CMSG_SYNC_FULL_RECHARGE_INFO7getDataEPKc          0x4401104000011086 3477383103264079913B
  ZNK25Active_freepick_rewardXml4Head10getDataMapEv     0x4280240100410028 10458625850470400272B
  _ATTRIBUTE_CHANGE7getDataEPKc                         0x56D60001EF8C  71812B
  _EXTRA_ATTRIBUTE_CHANGE7getDataEPKc                   0x3C5100003C50 66352949771350B
  _RETURN7getDataEPKc                                   0xDCF90000A5FD 192929930936320B
  _SYN_UPGRADE_REWARD7getDataEPKc                       0x336C0E080400004 4542062141830B
  ardXml10getDataArrEv                                  0x1E4B10001418A  82918B
  ck_rewardXml10getDataArrEv                            0x2162568450251214 282591669329920B
  ck_rewardXml10getDataArrEv                            0x30182000A48 11839963695276886048B
  cocos2d                                               0x057E0F20     20B
  cocos2d                                               0x057E0F34    548B
  cocos2d                                               0x05601580   1708B
  cocos2d                                               0x05601C2C      8B
  cocos2d                                               0x05600C0C     12B
  cocos2d                                               0x05601C34      8B
  cocos2d                                               0x0560022C   2100B
  cocos2d                                               0x05794DF4     16B
  dXml10getDataArrEv                                    0x28CD700000000 535986148905174B
  epick_setXml10getDataMapEv                            0x41190040C1001461 7079941189256872193B
  ewardXml10getDataMapEv                                0xC806900008004011 1441151880758582400B
  getDataArrEv                                          0x1F5840001F580 551469505967496B
  getDataEPKc                                           0x10288040000000 8233155953950947B
  getDataEPKc                                           0x40530000404E 70785356021853B
  getDataEPKc                                           0x1397C00000000 329338092257280B
  getDataMapEv                                          0x2043204081640030 2310349667403047969B
  il11getDataInfoERNSt6__ndk113unordered_mapImP8MailInfoNS0_4hashImEENS0_8equal_toImEENS0_9allocatorINS0_4pairIKmS3_EEEEEE 0x101B300000000 107859B
  il12getDataCountEv                                    0x362F00000000  11001B
  ilDBUtil12getDataCountEv                              0x2060E00020608 569628627699215B
  ive_freepick_rewardXml10getDataArrEv                  0x800424200040000 594478451841436704B
  lDBUtil11getDataInfoERNSt6__ndk113unordered_mapImP8MailInfoNS0_4hashImEENS0_8equal_toImEENS0_9allocatorINS0_4pairIKmS3_EEEEEE 0x0001EFFB 283777079325834B
  tive_freepick_setXml10getDataMapEv                    0x6050A809004000 1801580588707151873B
  tle_up_rewardXml10getDataArrEv                        0x264E00004A1C  36250B


--- Step 2: Deep Disassembly of Key getData Methods ---

----------------------------------------------------------------------
  CMSG_BUILDING_OPERAT_RETURN::getData
  Address: 0x04FCD040, Size: 200B
  Total instructions: 50
  Memory reads: {'u16': 3, 'u8': 2}
  Function calls (BL): 0
  Field read pattern (first 30):
    0x04FCD044: u16   w8, [x1]
    0x04FCD050: u16   w9, [x1]
    0x04FCD060: u16   w9, [x1, #2]
    0x04FCD070: u8    w9, [x1, #4]
    0x04FCD0F0: u8    w8, [x1, #0x1b]

----------------------------------------------------------------------
  CMSG_HERO_INFO::getData
  Address: 0x217EC00000000, Size: 40061B
  ERROR: too many values to unpack (expected 3)

----------------------------------------------------------------------
  CMSG_ITEM_USE::getData
  Address: 0x050C0830, Size: 88B
  Total instructions: 22
  Memory reads: {'u16': 3, 'u32': 2}
  Function calls (BL): 0
  Field read pattern (first 30):
    0x050C0834: u16   w8, [x1]
    0x050C0840: u16   w9, [x1]
    0x050C0850: u16   w9, [x1, #2]
    0x050C0860: u32   w9, [x1, #4]
    0x050C0870: u32   w8, [x1, #8]

----------------------------------------------------------------------
  CMSG_LOGIN::getData
  Address: 0x0517B084, Size: 552B
  Total instructions: 138
  Memory reads: {'u64': 6, 'u16': 4, 'u32': 6, 'u8': 1}
  Function calls (BL): 4
  Field read pattern (first 30):
    0x0517B0A4: u64   x8, [x22, #0x28]
    0x0517B0B0: u16   w23, [x1]
    0x0517B0BC: u16   w8, [x1]
    0x0517B0CC: u16   w8, [x1, #2]
    0x0517B0DC: u32   w8, [x1, #4]
    0x0517B0EC: u32   w8, [x1, #8]
    0x0517B10C: u16   w19, [x1, #0x14]
    0x0517B1A0: u64   x0, [x8, #0x28]
    0x0517B1B8: u64   x11, [sp, #0x10]
    0x0517B1E0: u32   w9, [x1, x9]
    0x0517B200: u32   w10, [x1, x10]
    0x0517B220: u32   w9, [x1, x9]
    0x0517B240: u32   w10, [x1, x10]
    0x0517B258: u64   x10, [x1, x9]
    0x0517B270: u8    w9, [x1, x9]
    0x0517B27C: u64   x8, [x22, #0x28]
    0x0517B290: u64   x25, [sp, #0x30]
  Called functions (first 20):
    BL 0x5BDC440
    BL 0x5BDC520
    BL 0x5BDC460
    BL 0x5BDC4A0

----------------------------------------------------------------------
  CMSG_LOGIN_RETURN::getData
  Address: 0x0517B5F4, Size: 612B
  Total instructions: 153
  Memory reads: {'u64': 7, 'u16': 6, 'u8': 1}
  Function calls (BL): 7
  Field read pattern (first 30):
    0x0517B618: u64   x8, [x23, #0x28]
    0x0517B624: u16   w24, [x1]
    0x0517B630: u16   w8, [x1]
    0x0517B640: u16   w8, [x1, #2]
    0x0517B660: u16   w19, [x1, #0xc]
    0x0517B6F4: u64   x0, [x8, #0x20]
    0x0517B70C: u64   x11, [sp, #0x10]
    0x0517B734: u16   w12, [x1, x9]
    0x0517B74C: u16   w20, [x27]
    0x0517B7CC: u64   x0, [x8, #0x40]
    0x0517B7E0: u64   x10, [sp, #0x10]
    0x0517B800: u8    w10, [x25, x10]
    0x0517B824: u64   x8, [x23, #0x28]
    0x0517B838: u64   x27, [sp, #0x30]
  Called functions (first 20):
    BL 0x5BDC440
    BL 0x5BDC520
    BL 0x5BDC460
    BL 0x5BDC440
    BL 0x5BDC520
    BL 0x5BDC460
    BL 0x5BDC4A0

----------------------------------------------------------------------
  CMSG_START_MARCH::getData
  Address: 0x05211FE4, Size: 644B
  Total instructions: 161
  Memory reads: {'u16': 3, 'u8': 5, 'u64': 2, 'u32': 3}
  Function calls (BL): 5
  Field read pattern (first 30):
    0x05212008: u16   w22, [x1]
    0x05212014: u16   w8, [x1]
    0x05212024: u16   w8, [x1, #2]
    0x05212034: u8    w8, [x1, #4]
    0x05212074: u8    w9, [x1, #0x11]
    0x05212174: u64   x1, [sp, #0x10]
    0x05212178: u32   w9, [sp, #0xc]
    0x0521219C: u32   w27, [x1, x8]
    0x052121C8: u32   w9, [x1, x8]
    0x052121E8: u8    w8, [x1, x8]
    0x05212200: u64   x9, [x1, x8]
    0x05212218: u8    w9, [x1, x8]
    0x05212230: u8    w8, [x1, x8]
  Called functions (first 20):
    BL 0x5BDC440
    BL 0x5BDC520
    BL 0x5BDC460
    BL 0x334A83C
    BL 0x32F4380

----------------------------------------------------------------------
  CMSG_START_MARCH_NEW::getData
  Address: 0x05212778, Size: 848B
  Total instructions: 212
  Memory reads: {'u16': 3, 'u8': 10, 'u64': 9, 'u32': 4}
  Function calls (BL): 5
  Field read pattern (first 30):
    0x0521279C: u16   w22, [x1]
    0x052127A8: u16   w8, [x1]
    0x052127B8: u16   w8, [x1, #2]
    0x052127C8: u8    w8, [x1, #4]
    0x052127D8: u8    w8, [x1, #5]
    0x052127E8: u8    w8, [x1, #6]
    0x052127F8: u8    w8, [x1, #7]
    0x05212808: u8    w8, [x1, #8]
    0x05212848: u8    w9, [x1, #0x15]
    0x05212948: u64   x1, [sp, #0x10]
    0x0521294C: u32   w9, [sp, #0xc]
    0x05212970: u32   w24, [x1, x8]
    0x0521299C: u32   w9, [x1, x8]
    0x052129BC: u8    w8, [x1, x8]
    0x052129D0: u64   x8, [sp, #0x10]
    0x052129DC: u64   x10, [x8, x9]
    0x052129F8: u64   x8, [sp, #0x10]
    0x052129FC: u8    w10, [x8, x9]
    0x05212A1C: u64   x8, [sp, #0x10]
    0x05212A24: u8    w10, [x8, x10]
    0x05212A3C: u64   x8, [sp, #0x10]
    0x05212A44: u64   x10, [x8, x9]
    0x05212A64: u64   x8, [sp, #0x10]
    0x05212A6C: u8    w10, [x8, x10]
    0x05212A84: u64   x8, [sp, #0x10]
    0x05212A8C: u32   w9, [x8, x9]
  Called functions (first 20):
    BL 0x5BDC440
    BL 0x5BDC520
    BL 0x5BDC460
    BL 0x334A83C
    BL 0x32F4380

----------------------------------------------------------------------
  CMSG_SYNC_MARCH::getData
  Address: 0x051E9CA8, Size: 4436B
  Total instructions: 1024
  Memory reads: {'u64': 66, 'u16': 23, 'u8': 9, 'u32': 23}
  Function calls (BL): 21
  Field read pattern (first 30):
    0x051E9CCC: u64   x8, [x9, #0x28]
    0x051E9CD8: u16   w13, [x1]
    0x051E9D08: u16   w8, [x12]
    0x051E9D28: u16   w8, [x12, #2]
    0x051E9D48: u16   w8, [x12, #4]
    0x051E9D94: u64   x10, [sp, #0x20]
    0x051E9DC8: u64   x8, [sp, #0x20]
    0x051E9DE8: u64   x8, [sp, #0x20]
    0x051E9E08: u64   x8, [sp, #0x18]
    0x051E9E1C: u64   x8, [x8]
    0x051E9E48: u8    w8, [sp, #0xb0]
    0x051E9E50: u64   x0, [sp, #0xc0]
    0x051E9E60: u32   w13, [sp, #0x64]
    0x051E9E7C: u64   x12, [sp, #0x58]
    0x051E9E88: u64   x9, [x12, x9]
    0x051E9EB4: u16   w8, [x12, x8]
    0x051E9ED0: u64   x8, [x12, x8]
    0x051E9EEC: u8    w9, [x12, x9]
    0x051E9F0C: u32   w8, [x12, x8]
    0x051E9F38: u16   w9, [x12, x9]
    0x051E9F58: u16   w8, [x12, x8]
    0x051E9F78: u16   w9, [x12, x9]
    0x051E9F98: u16   w8, [x12, x8]
    0x051E9FB8: u32   w8, [x12, x8]
    0x051E9FE4: u16   w11, [x12, x9]
    0x051EA008: u16   w25, [x21]
    0x051EA080: u8    w8, [sp, #0xb0]
    0x051EA08C: u64   x0, [sp, #0xc0]
    0x051EA0B4: u64   x2, [sp, #0x58]
    0x051EA0BC: u32   w3, [sp, #0x64]
  Called functions (first 20):
    BL 0x5237B48
    BL 0x5BDC460
    BL 0x5C25A20
    BL 0x5BDCD20
    BL 0x5BDC460
    BL 0x5BDC440
    BL 0x5BDC520
    BL 0x5BDC460
    BL 0x3A881D4
    BL 0x5BDC460
    BL 0x3A883E0
    BL 0x5237DB4
    BL 0x5BDC460
    BL 0x5BDC460
    BL 0x50DB7D4
    BL 0x5BDC460
    BL 0x5BDC440
    BL 0x5BDC510
    BL 0x5BDC520
    BL 0x5BDC460

----------------------------------------------------------------------
  CMSG_SYNC_MARCH_ARMY_INFO::getData
  Address: 0x052011D8, Size: 644B
  Total instructions: 161
  Memory reads: {'u16': 6, 'u64': 7, 'u32': 3, 'u8': 2}
  Function calls (BL): 1
  Field read pattern (first 30):
    0x052011F0: u16   w20, [x1]
    0x05201214: u16   w8, [x1]
    0x05201234: u16   w8, [x1, #2]
    0x05201274: u16   w8, [x1, #0xc]
    0x0520130C: u64   x12, [x19]
    0x05201318: u32   w13, [x1, x13]
    0x0520133C: u64   x12, [x19]
    0x05201348: u16   w11, [x1, x11]
    0x05201370: u64   x12, [x19]
    0x0520137C: u16   w10, [x1, x10]
    0x05201398: u64   x12, [x19]
    0x052013A4: u32   w11, [x1, x11]
    0x052013BC: u64   x11, [x19]
    0x052013C4: u32   w12, [x1, x10]
    0x052013DC: u64   x11, [x19]
    0x052013E8: u8    w10, [x1, x10]
    0x05201408: u64   x10, [x19]
    0x05201414: u8    w11, [x1, x11]
  Called functions (first 20):
    BL 0x3A883E0

----------------------------------------------------------------------
  CMSG_SYNC_MARCH_ARMY_INFO_NEW::getData
  Address: 0x05211010, Size: 748B
  Total instructions: 187
  Memory reads: {'u16': 6, 'u64': 9, 'u32': 3, 'u8': 4}
  Function calls (BL): 1
  Field read pattern (first 30):
    0x05211028: u16   w20, [x1]
    0x0521104C: u16   w8, [x1]
    0x0521106C: u16   w8, [x1, #2]
    0x052110AC: u16   w8, [x1, #0xc]
    0x05211144: u64   x12, [x19]
    0x05211150: u32   w13, [x1, x13]
    0x05211174: u64   x12, [x19]
    0x05211180: u16   w11, [x1, x11]
    0x052111A8: u64   x12, [x19]
    0x052111B4: u16   w10, [x1, x10]
    0x052111D0: u64   x12, [x19]
    0x052111DC: u32   w11, [x1, x11]
    0x052111F4: u64   x11, [x19]
    0x052111FC: u32   w12, [x1, x10]
    0x05211214: u64   x11, [x19]
    0x0521121C: u8    w12, [x1, x10]
    0x05211234: u64   x11, [x19]
    0x05211240: u8    w10, [x1, x10]
    0x05211260: u64   x10, [x19]
    0x0521126C: u8    w11, [x1, x11]
    0x052112A8: u64   x10, [x19]
    0x052112B4: u8    w11, [x1, x11]
  Called functions (first 20):
    BL 0x3A883E0

----------------------------------------------------------------------
  CMSG_SYNC_MARCH_NEW::getData
  Address: 0x052028BC, Size: 4948B
  Total instructions: 1024
  Memory reads: {'u64': 65, 'u16': 23, 'u8': 9, 'u32': 25}
  Function calls (BL): 22
  Field read pattern (first 30):
    0x052028E0: u64   x8, [x9, #0x28]
    0x052028EC: u16   w13, [x1]
    0x05202918: u16   w8, [x12]
    0x05202938: u16   w8, [x12, #2]
    0x05202958: u16   w8, [x12, #4]
    0x052029AC: u64   x10, [sp, #0x30]
    0x052029DC: u64   x8, [sp, #8]
    0x052029E4: u64   x8, [sp, #0x30]
    0x05202A28: u64   x8, [x23]
    0x05202A64: u8    w8, [sp, #0xb0]
    0x05202A6C: u64   x0, [sp, #0xc0]
    0x05202A7C: u32   w13, [sp, #0x64]
    0x05202A98: u64   x12, [sp, #0x58]
    0x05202AA4: u64   x9, [x12, x9]
    0x05202AD0: u16   w8, [x12, x8]
    0x05202AEC: u64   x8, [x12, x8]
    0x05202B08: u8    w9, [x12, x9]
    0x05202B28: u32   w8, [x12, x8]
    0x05202B54: u16   w9, [x12, x9]
    0x05202B74: u16   w8, [x12, x8]
    0x05202B94: u16   w9, [x12, x9]
    0x05202BB4: u16   w8, [x12, x8]
    0x05202BD4: u32   w8, [x12, x8]
    0x05202C00: u16   w11, [x12, x9]
    0x05202C24: u16   w22, [x21]
    0x05202C9C: u8    w8, [sp, #0xb0]
    0x05202CA8: u64   x0, [sp, #0xc0]
    0x05202CBC: u64   x23, [sp, #0x28]
    0x05202CD4: u64   x2, [sp, #0x58]
    0x05202CDC: u32   w3, [sp, #0x64]
  Called functions (first 20):
    BL 0x5237B48
    BL 0x5BDC460
    BL 0x5C25A20
    BL 0x5BDCD20
    BL 0x5BDC460
    BL 0x5BDC440
    BL 0x5BDC520
    BL 0x5BDC460
    BL 0x3A881D4
    BL 0x5BDC460
    BL 0x3A883E0
    BL 0x5237DB4
    BL 0x5BDC460
    BL 0x5BDC460
    BL 0x50DB7D4
    BL 0x5BDC460
    BL 0x5BDC440
    BL 0x5BDC510
    BL 0x5BDC520
    BL 0x5BDC460

----------------------------------------------------------------------
  CMSG_SYN_ATTRIBUTE_CHANGE::getData
  Address: 0x04FB8C10, Size: 104B
  Total instructions: 26
  Memory reads: {'u16': 3, 'u32': 2, 'u64': 1}
  Function calls (BL): 0
  Field read pattern (first 30):
    0x04FB8C14: u16   w8, [x1]
    0x04FB8C20: u16   w9, [x1]
    0x04FB8C30: u16   w9, [x1, #2]
    0x04FB8C40: u32   w9, [x1, #4]
    0x04FB8C50: u64   x9, [x1, #8]
    0x04FB8C60: u32   w8, [x1, #0x10]

----------------------------------------------------------------------
  CMSG_SYN_EXTRA_ATTRIBUTE_CHANGE::getData
  Address: 0x0505D7E0, Size: 88B
  Total instructions: 22
  Memory reads: {'u16': 3, 'u32': 1, 'u64': 1}
  Function calls (BL): 0
  Field read pattern (first 30):
    0x0505D7E4: u16   w8, [x1]
    0x0505D7F0: u16   w9, [x1]
    0x0505D800: u16   w9, [x1, #2]
    0x0505D810: u32   w9, [x1, #4]
    0x0505D820: u64   x8, [x1, #8]

----------------------------------------------------------------------
  CMSG_SYN_SERVER_TIME::getData
  Address: 0x0527CC98, Size: 88B
  Total instructions: 22
  Memory reads: {'u16': 3}
  Function calls (BL): 0
  Field read pattern (first 30):
    0x0527CC9C: u16   w8, [x1]
    0x0527CCA8: u16   w9, [x1]
    0x0527CCB8: u16   w9, [x1, #2]


--- Step 3: All _RETURN Opcodes (Server Responses) ---

Total _RETURN opcodes: 303
Total SYN/SYNC opcodes: 119

  [AUTH/LOGIN] (5 opcodes)
    0x000C = CMSG_LOGIN_RETURN
    0x000F = CMSG_LOGIN_DISTRIBUTUON_RETURN
    0x0020 = CMSG_ENTER_GAME_RETURN
    0x0022 = CMSG_USERINFO_RETURN
    0x0024 = CMSG_QUICK_LOGIN_RETURN

  [BUILDING] (14 opcodes)
    0x009E = CMSG_BUILDING_OPERAT_RETURN
    0x15E1 = CMSG_LEAGUE_BUILDING_OPERAT_RETURN
    0x15E5 = CMSG_LEAGUE_BUILDING_DETAIL_RETURN
    0x15FB = CMSG_LOSTLAND_BUILDING_INDEX_OPEN_RETURN
    0x1B05 = CMSG_CLANPK_BUILDING_RETURN
    0x1B07 = CMSG_CLANPK_BUILD_UPGRADE_RETURN
    0x1B30 = CMSG_CLANPK_DEFEND_BUILDING_RETURN
    0x1C21 = CMSG_CHANGE_BUILDING_SKIN_RETURN
    0x1C25 = CMSG_BUILDING_SKIN_UPGRADE_LV_RETURN
    0x1C27 = CMSG_BUILDING_SKIN_SUIT_REWARD_RETURN
    0x1C29 = CMSG_BUILDING_SKIN_REWARD_RETURN
    0x1C2B = CMSG_UNLOCK_BUILDING_SKIN_RETURN
    0x1EAC = CMSG_AUTO_JOIN_BUILDUP_OPEN_RETURN
    0x1EAE = CMSG_AUTO_JOIN_BUILDUP_CLOSE_RETURN

  [EVENTS] (10 opcodes)
    0x02F5 = CMSG_QUERY_SPECIAL_EVENT_RETURN
    0x07E6 = CMSG_LEAGUE_BATTLEFIELD_ACTIVITY_VIEW_RETURN
    0x0F0C = CMSG_FORTRESS_ACTIVITY_VIEW_RETURN
    0x12CD = CMSG_SPECIAL_EVENT_DROP_LIMIT_RETURN
    0x15B2 = CMSG_LOSTLAND_ACTIVITY_VIEW_RETURN
    0x16C8 = CMSG_RETURN_EVENT_ACTION_RETURN
    0x16CD = CMSG_RETURN_EVENT_ACTION_RETURN_NEW
    0x1AFA = CMSG_CLANPK_ACTIVITY_VIEW_RETURN
    0x1B33 = CMSG_CLANPK_ACTIVITY_INFO_RETURN
    0x1FB0 = CMSG_LOSTLAND_RUSH_EVENT_RANK_RETURN

  [HERO] (11 opcodes)
    0x05E8 = CMSG_AREN_HERO_QUEUE_CHANGE_RETURN
    0x15BA = CMSG_LOSTLAND_DONATE_HEROCHIP_RETURN
    0x15BF = CMSG_LOSTLAND_BAN_HERO_RETURN
    0x15C1 = CMSG_LOSTLAND_HERO_VOTE_COUNT_RETURN
    0x170E = CMSG_HERO_COLLECTION_ACTION_RETURN
    0x1711 = CMSG_HERO_COLLECTION_PVE_RETURN
    0x1713 = CMSG_HERO_COLLECTION_REWARD_RETURN
    0x1B0B = CMSG_CLANPK_SET_DEFEND_HERO_RETURN
    0x1B0F = CMSG_CLANPK_SET_ASSIST_HERO_RETURN
    0x1B11 = CMSG_CLANPK_GIVE_ASSIST_HERO_RETURN
    0x1B15 = CMSG_CLANPK_ASSIST_HERO_RETURN

  [ITEMS/EQUIP] (6 opcodes)
    0x0795 = CMSG_ROYAL_SHOP_ITEM_CONFIG_RETURN
    0x0797 = CMSG_BUY_ROYAL_SHOP_ITEM_RETURN
    0x0799 = CMSG_ROYAL_SHOP_ITEM_INFO_RETURN
    0x0AF1 = CMSG_BUY_REWARD_POINT_SHOP_ITEM_RETURN
    0x0AF3 = CMSG_REWARD_POINT_SHOP_ITEM_INFO_RETURN
    0x1ACA = CMSG_DAMAGE_BUY_ITEM_RETURN

  [MARCH/COMBAT] (2 opcodes)
    0x1B0D = CMSG_CLANPK_SET_ATTACK_HERO_RETURN
    0x1B1B = CMSG_CLANPK_START_ATTACK_RETURN

  [MONSTERS] (5 opcodes)
    0x1F10 = CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_RETURN
    0x1F12 = CMSG_LEAGUE_BIG_BOSS_DONATE_RETURN
    0x1F14 = CMSG_LEAGUE_BIG_BOSS_POINT_RETURN
    0x1F18 = CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_RETURN
    0x1F1C = CMSG_LEAGUE_BIG_BOSS_EMPTYPOS_RETURN

  [OTHER] (162 opcodes)
    0x0261 = CMSG_QUERY_DOMINION_DEFEND_NUM_RETURN
    0x029F = CMSG_RANK_INFO_RETURN
    0x02A3 = CMSG_RANK_SIMPLE_INFO_RETURN
    0x02A9 = CMSG_LEAGUE_BOARD_RETURN
    0x02AB = CMSG_LEAGUE_BOARD_LEAVE_WORD_RETURN
    0x02B3 = CMSG_EXPEDITION_INFO_RETURN
    0x02B5 = CMSG_RAID_PLAYER_ERROR_RETURN
    0x02C7 = CMSG_FAVORITE_INFO_RETURN
    0x02C9 = CMSG_UPDATE_FAVORITE_RETURN
    0x02CB = CMSG_DEL_FAVORITE_RETURN
    0x02DB = CMSG_LEAGUE_LATEST_RETURN
    0x02F4 = CMSG_CYCLE_ACTION_RANK_RECORD_RETURN
    0x02F9 = CMSG_DOMINION_LATEST_RETURN
    0x039D = CMSG_LUCKY_TURNTABLE_TURN_RETURN
    0x039F = CMSG_LUCKY_TURNTABLE_TURN_NEW_SERVER_RETURN
    0x03A1 = CMSG_LUCKY_TURNTABLE_SET_PRIZE_RETURN
    0x05EA = CMSG_ARENA_RANK_INFO_RETURN
    0x05EE = CMSG_ARENA_MATCH_INFO_RETURN
    0x05F0 = CMSG_ARENA_CHANGE_MATCH_RETURN
    0x05F2 = CMSG_ARENA_CHALLENGE_MATCH_RETURN
    0x05F7 = CMSG_ARENA_DELETE_BATTLE_RECORD_RETURN
    0x05F9 = CMSG_ARENA_SET_BATTLE_RECORD_FLAG_RETURN
    0x0605 = CMSG_QUERY_DOMINION_ACTION_INTEGRAL_RETURN
    0x0607 = CMSG_QUERY_DOMINION_ACTION_HISTORY_RETURN
    0x0609 = CMSG_QUERY_KING_INFO_RETURN
    0x060C = CMSG_DOMINION_ACTION_SET_SLAVE_RETURN
    0x0613 = CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_RETURN
    0x0615 = CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_RETURN
    0x0617 = CMSG_QUERY_SERVER_KING_INFO_RETURN
    0x06A0 = CMSG_ACCUMULATION_RANK_RETURN
    0x0781 = CMSG_MATCH_SERVER_INFO_RETURN
    0x07B5 = CMSG_MOBILIZATION_ACTION_STATUS_RETURN
    0x07B9 = CMSG_MOBILIZATION_ACTION_RANK_INFO_RETURN
    0x07BB = CMSG_MOBILIZATION_CONTRIBUTE_INFO_RETURN
    0x07EA = CMSG_LEAGUE_BATTLEFIELD_SIGNUP_RETURN
    0x07EC = CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_RETURN
    0x07F6 = CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_RETURN
    0x0841 = CMSG_WORLD_BATTLE_ACTION_RETURN
    0x0843 = CMSG_WORLD_BATTLE_ACTION_DETAIL_RETURN
    0x0847 = CMSG_WORLD_BATTLE_PLAYER_RANK_RETURN
    0x0849 = CMSG_WORLD_BATTLE_GROUP_RANK_RETURN
    0x084B = CMSG_WORLD_BATTLE_OVERLORD_RECORD_RETURN
    0x0850 = CMSG_WORLD_BATTLE_SERVER_OFFICIAL_RETURN
    0x0852 = CMSG_WORLD_BATTLE_PLAYER_OFFICIAL_RETURN
    0x0854 = CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_RETURN
    0x0856 = CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_RETURN
    0x085A = CMSG_SYNC_FORCE_POWER_INFO_RETURN
    0x085C = CMSG_WORLD_BATTLE_ENTER_VIEW_RETURN
    0x0860 = CMSG_WORLD_BATTLE_DOMINION_RECORD_RETURN
    0x0869 = CMSG_ANNIVERSARY_DONATE_RETURN
    0x0925 = CMSG_INVEST_RETURN
    0x0927 = CMSG_INVEST_CANCEL_RETURN
    0x0929 = CMSG_INVEST_EARN_RETURN
    0x093A = CMSG_KNIGHT_ACTION_RETURN
    0x093C = CMSG_KNIGHT_ACTION_DETAIL_RETURN
    0x093E = CMSG_KNIGHT_ACTION_SET_BEGIN_TIME_RETURN
    0x0940 = CMSG_KNIGHT_ACTION_PLAYER_RANK_RETURN
    0x0942 = CMSG_KNIGHT_ACTION_LEAGUE_RANK_RETURN
    0x0961 = CMSG_WORLD_BATTLE_NEW_SIGN_UP_RETURN
    0x0963 = CMSG_WORLD_BATTLE_GROUP_INFO_RETURN
    0x0965 = CMSG_WORLD_BATTLE_GROUP_MEMBER_RETURN
    0x0967 = CMSG_WORLD_BATTLE_JOIN_GROUP_RETURN
    0x0969 = CMSG_WORLD_BATTLE_SET_POWER_RETURN
    0x096B = CMSG_WORLD_BATTLE_KICK_MEMBER_RETURN
    0x0970 = CMSG_WORLD_BATTLE_LEAVE_GROUP_RETURN
    0x099E = CMSG_COMMON_EXCHAGE_COUNT_RETURN
    0x09B1 = CMSG_ALL_CAMELS_RETURN
    0x09B3 = CMSG_DRIVE_CAMEL_RETURN
    0x09BE = CMSG_OPERATION_ACTION_RANK_RECORD_RETURN
    0x0A29 = CMSG_KING_CHESS_SIGNUP_RETURN
    0x0A2D = CMSG_KING_CHESS_ACTION_DETAIL_INFO_RETURN
    0x0A2F = CMSG_KING_CHESS_RANK_RETURN
    0x0A34 = CMSG_KING_CHESS_OCCUPY_INFO_RETURN
    0x0A4A = CMSG_KING_CHESS_USER_VALUE_RETURN
    0x0B56 = CMSG_LUCKY_LINE_OPEN_RETURN
    0x0B58 = CMSG_LUCKY_LINE_SET_PRIZE_RETURN
    0x0B62 = CMSG_KINGDOM_ACTION_RANK_RECORD_RETURN
    0x0B64 = CMSG_KINGDOM_SERVER_ACTION_VALUE_RETURN
    0x0C52 = CMSG_LEGION_CREATE_RETURN
    0x0C54 = CMSG_LEGION_LIST_RETURN
    0x0C56 = CMSG_LEGION_INFO_RETURN
    0x0C58 = CMSG_LEGION_JOIN_RETURN
    0x0C5D = CMSG_LEGION_ADD_MEMBER_LIST_RETURN
    0x0C61 = CMSG_CHANGE_LEGION_CHANGE_NAME_RETURN
    0x0C64 = CMSG_LEGION_RANK_RETURN
    0x0C66 = CMSG_LEGION_SET_TALENT_RETURN
    0x0C68 = CMSG_LEGION_CHANGE_POS_TIMES_RETURN
    0x0C6F = CMSG_LEGION_LATEST_RETURN
    0x0C71 = CMSG_LEGION_SELF_JOIN_RETURN
    0x0C73 = CMSG_LEGION_SELF_LEAVE_RETURN
    0x0C75 = CMSG_LEGION_BATTLE_MAP_INFO_RETURN
    0x0C77 = CMSG_LEGION_RESOURCE_RETURN
    0x0C79 = CMSG_LEGION_MEMBER_INFO_RETURN
    0x0C7B = CMSG_LEGION_ENEMY_POS_RETURN
    0x0C7D = CMSG_LEGION_VALUE_DETAIL_RETURN
    0x0CB6 = CMSG_NOVICE_FREE_PURCHASE_GET_AWARD_RETURN
    0x0E13 = CMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_RETURN
    0x0E17 = CMSG_LEGION_SEASON_ACTION_GUESS_INFO_RETURN
    0x0E19 = CMSG_LEGION_SEASON_ACTION_GUESS_BET_RETURN
    0x0E1B = CMSG_LEGION_SEASON_ACTION_PLAYOFF_RETURN
    0x0E1D = CMSG_LEGION_SEASON_ACTION_HIS_PLAYER_RETURN
    0x0E1F = CMSG_LEGION_SEASON_ACTION_HIS_MVP_RETURN
    0x0E21 = CMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_RETURN
    0x0E23 = CMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_RETURN
    0x0E28 = CMSG_LEGION_MEMBER_HIS_INFO_RETURN
    0x0E76 = CMSG_WHEEL_TURN_RETURN
    0x0F10 = CMSG_FORTRESS_SIGNUP_RETURN
    0x0F12 = CMSG_FORTRESS_RANK_VIEW_RETURN
    0x0F1D = CMSG_FORTRESS_LEVEL_RANK_VIEW_RETURN
    0x0F1F = CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_RETURN
    0x0F25 = CMSG_FORTRESS_USER_VALUE_RETURN
    0x0F3D = CMSG_LEAGUE_STATUS_RETURN
    0x0F3E = CMSG_LEAGUE_UPDATE_STATUS_RETURN
    0x11C7 = CMSG_FIXED_TIME_RETURN
    0x12F4 = CMSG_ACTIVEGIFTS_ACTION_RETURN
    0x12F9 = CMSG_ACTIVEGIFTS_SHOWACTION_RETURN
    0x12FB = CMSG_ACTIVEGIFTS_CHANGEGRANDPRIZE_RETURN
    0x1358 = CMSG_CUSTOMGIFTS_ACTION_RETURN
    0x138C = CMSG_WAR_LORD_ACTION_RANK_RETURN
    0x138E = CMSG_WAR_LORD_ACTION_MATCH_INFO_RETURN
    0x13BE = CMSG_SERVER_MISSION_RECEIVE_RETURN
    0x13C0 = CMSG_SERVER_MISSION_VIEW_RETURN
    0x1452 = CMSG_DAILYCONSUME_ACTION_RETURN
    0x15B8 = CMSG_LOSTLAND_DONATE_RESOURCE_RETURN
    0x15C3 = CMSG_LOSTLAND_CAMP_RANK_RETURN
    0x15C5 = CMSG_LOSTLAND_LEAGUE_RANK_RETURN
    0x15C7 = CMSG_LOSTLAND_PLAYER_RANK_RETURN
    0x15CD = CMSG_LOSTLAND_HISTORY_RETURN
    0x15CF = CMSG_LOSTLAND_LEAGUE_HISTORY_RETURN
    0x15D1 = CMSG_LOSTLAND_PLAYER_HISTORY_RETURN
    0x15D8 = CMSG_ENTER_LOSTLAND_ERROR_RETURN
    0x15F2 = CMSG_LOSTLAND_LEAGUE_LATEST_RETURN
    0x1669 = CMSG_LEAGUEPASS_GROUP_RANK_INFO_RETURN
    0x166B = CMSG_LEAGUEPASS_CONTRIBUTE_INFO_RETURN
    0x16B5 = CMSG_EXTRA_GIFTPACK_ACTION_RETURN_NEW
    0x16C6 = CMSG_SYNC_RETURN_EVNET_ACTION
    0x16CB = CMSG_SYNC_RETURN_EVNET_ACTION_NEW
    0x1772 = CMSG_RECHARGEBONUS_ACTION_RETURN
    0x183A = CMSG_CONTINUITY_GIFTPACK_ACTION_RETURN
    0x183F = CMSG_CONTINUITY_GIFTPACK_POINT_RETURN
    0x1841 = CMSG_CONTINUITY_GIFTPACK_DISCOUNT_RETURN
    0x186C = CMSG_FTRIEND_GIFT_PRESEND_RETURN
    0x18D3 = CMSG_KINGDOM_GIFT_ACTION_RETURN
    0x18D7 = CMSG_KINGDOM_GIFT_LEVEL_GIFT_RETURN
    0x1934 = CMSG_AUTO_HANDUP_CHANGE_RETURN
    0x19A3 = CMSG_NEWSERVER_SIGNFUND_UNLOCK_RETURN
    0x19CA = CMSG_MINI_GAME_RANK_RETURN
    0x19D0 = CMSG_MINI_GAME_PLAYER_RETURN
    0x1AC4 = CMSG_DAMAGE_GIFT_INFO_RETURN
    0x1AC6 = CMSG_DAMAGE_HELP_RETURN
    0x1ACC = CMSG_DAMAGE_SHARE_RETURN
    0x1AF8 = CMSG_CLANPK_SIGNUP_RETURN
    0x1AFC = CMSG_CLANPK_BATTLE_RECORD_RETURN
    0x1AFE = CMSG_CLANPK_LEVEL_RANK_VIEW_RETURN
    0x1B00 = CMSG_CLANPK_USER_RANK_VIEW_RETURN
    0x1B02 = CMSG_ENTER_CLANPK_RETURN
    0x1B09 = CMSG_CLANPK_DONATE_RETURN
    0x1B22 = CMSG_CLANPK_START_DEFEND_RETURN
    0x1B2E = CMSG_CLANPK_DEFEND_AMRY_RETURN
    0x1B35 = CMSG_CLANPK_CHECK_SET_DEF_RETURN
    0x1D4E = CMSG_DOUBLE_LOTTERY_PLAY_RETURN
    0x1E18 = CMSG_ALLFORONE_POINT_RETURN

  [QUESTS/REWARDS] (68 opcodes)
    0x0225 = CMSG_ACHIEVEMENT_RECEIVE_REWARD_RETURN
    0x0227 = CMSG_ACHIEVEMENT_SCORE_RECEIVE_REWARD_RETURN
    0x0229 = CMSG_ACHIEVEMENT_WEAR_RETURN
    0x022B = CMSG_POWER_TASKS_RETURN
    0x022D = CMSG_POWER_TASK_REWARD_RETURN
    0x0293 = CMSG_RANDOM_ONLINE_REWARD_RETURN
    0x0313 = CMSG_EVERY_DAY_GIFTPACK_REWARD_RETURN
    0x060F = CMSG_KING_REWARD_INFO_RETURN
    0x0611 = CMSG_BESTOW_KING_REWARD_RETURN
    0x062D = CMSG_RECEIVE_REWARD_RETURN
    0x0630 = CMSG_RECEIVE_REWARD_BATCH_RETURN
    0x069E = CMSG_RECEIVE_ACCUMULATION_REWARD_RETURN
    0x06FA = CMSG_BUY_MOBILIZATION_TASK_TIMES_RETURN
    0x06FC = CMSG_MICROPAYMENT_DAILY_REWARD_RETURN
    0x07B7 = CMSG_MOBILIZATION_ACTION_TASK_INFO_RETURN
    0x07BD = CMSG_MOBILIZATION_REWARD_CONFIG_RETURN
    0x07BF = CMSG_MOBILIZATION_GET_REWARD_RETURN
    0x07C1 = CMSG_MOBILIZATION_GET_TASK_RETURN
    0x07C3 = CMSG_MOBILIZATION_GIVE_UP_TASK_RETURN
    0x07C5 = CMSG_MOBILIZATION_FINISH_TASK_RETURN
    0x07EE = CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_RETURN
    0x07F0 = CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_RETURN
    0x086B = CMSG_ANNIVERSARY_DONATE_REWARD_RETURN
    0x086D = CMSG_ANNIVERSARY_SHARE_REWARD_RETURN
    0x0994 = CMSG_KING_ROAD_REWARD_RETURN
    0x09A0 = CMSG_COMMON_EXCHAGE_GET_REWARD_RETURN
    0x0A08 = CMSG_GAIN_EXP_REWARD_RETURN
    0x0C6B = CMSG_LORD_WAR_DISTRIBUTE_REWARD_INFO_RETURN
    0x0C6D = CMSG_BESTOW_LORD_WAR_REWARD_RETURN
    0x0E78 = CMSG_WHEEL_REWARD_RETURN
    0x0EA8 = CMSG_DAILY_RECHARGE_REWARD_RETURN
    0x0F21 = CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_RETURN
    0x0F23 = CMSG_BESTOW_FORTRESS_REWARD_RETURN
    0x12F6 = CMSG_ACTIVEGIFTS_REWARD_RETURN
    0x135B = CMSG_CUSTOMGIFTS_CHANGEREWARD_RETURN
    0x1454 = CMSG_DAILYCONSUME_REWARD_RETURN
    0x15CB = CMSG_LOSTLAND_MARK_REWARD_RETURN
    0x15DA = CMSG_LOSTLAND_ACHIEVEMENT_LIST_RETURN
    0x15DD = CMSG_LOSTLAND_ACHIEVEMENT_RETURN
    0x15DF = CMSG_LOSTLAND_ACHIEVEMENT_REWARD_RETURN
    0x1600 = CMSG_LOSTLAND_MONTH_CARD_REWARD_RETURN
    0x1667 = CMSG_LEAGUEPASS_ACTION_TASK_INFO_RETURN
    0x166D = CMSG_LEAGUEPASS_GET_REWARD_RETURN
    0x166F = CMSG_LEAGUEPASS_FRESH_TASK_RETURN
    0x1671 = CMSG_LEAGUEPASS_FINISH_TASK_RETURN
    0x16B3 = CMSG_EXTRA_GIFTPACK_REWARD_RETURN_NEW
    0x16C7 = CMSG_RETURN_EVENT_ACTION_REQUEST
    0x16C9 = CMSG_RETURN_EVENT_REWARD_REQUEST
    0x16CA = CMSG_RETURN_EVENT_REWARD_RETURN
    0x16CC = CMSG_RETURN_EVENT_ACTION_REQUEST_NEW
    0x16CE = CMSG_RETURN_EVENT_REWARD_REQUEST_NEW
    0x16CF = CMSG_RETURN_EVENT_REWARD_RETURN_NEW
    0x16E8 = CMSG_LOST_ERA_TASK_RECEIVE_RETURN
    0x16EA = CMSG_LOST_ERA_TASK_VIEW_RETURN
    0x1741 = CMSG_MERGE_EVNET_REWARD_RETURN
    0x1775 = CMSG_RECHARGEBONUS_REWARD_RETURN
    0x1790 = CMSG_LOST_KING_ROAD_REWARD_RETURN
    0x189E = CMSG_EVERY_DAY_GIFTPACK_REWARD_RETURN_NEW
    0x18D5 = CMSG_KINGDOM_GIFT_LEVEL_REWARD_RETURN
    0x18D9 = CMSG_KINGDOM_GIFT_TIME_REWARD_RETURN
    0x1999 = CMSG_NEWSERVER_RECORDCOST_REWARD_RETURN
    0x19A1 = CMSG_NEWSERVER_SIGNINFUND_REWARD_RETURN
    0x1B37 = CMSG_CLANPK_FIRST_LEVEL_REWARD_RETURN
    0x1D52 = CMSG_DOUBLE_LOTTERY_REWARD_HISTORY_RETURN
    0x1DE4 = CMSG_CONTINUOUS_TASK_ACTION_RETURN
    0x1DE7 = CMSG_CONTINUOUS_TASK_REWARD_RETURN
    0x1E16 = CMSG_ALLFORONE_REWARD_RETURN
    0x1FAE = CMSG_LOSTLAND_RUSH_EVENT_REWARD_RETURN

  [SHOP] (9 opcodes)
    0x0391 = CMSG_CAMEL_SHOP_BUY_RETURN
    0x0CB4 = CMSG_NOVICE_FREE_PURCHASE_BUY_GIFT_RETURN
    0x15BC = CMSG_LOSTLAND_SHOP_BUY_RETURN
    0x183D = CMSG_CONTINUITY_GIFTPACK_GOLDBUY_RETURN
    0x199C = CMSG_NEWSERVER_LIMITSHOP_BUY_RETURN
    0x199E = CMSG_NEWSERVER_LIMITSHOP_GIFT_RETURN
    0x19CC = CMSG_MINI_GAME_SHOP_BUY_RETURN
    0x1AC8 = CMSG_DAMAGE_BUY_RETURN
    0x1D50 = CMSG_DOUBLE_LOTTERY_SHOP_BUY_RETURN

  [SOCIAL] (11 opcodes)
    0x0270 = CMSG_CHAT_SEND_RETURN
    0x0277 = CMSG_CHAT_ADD_BOX_RETURN
    0x0278 = CMSG_CHAT_ADD_BUBBLE_RETURN
    0x027A = CMSG_CHAT_NAME_ERROR_RETURN
    0x027D = CMSG_CHAT_SET_BLOCK_CONDITION_RETURN
    0x0899 = CMSG_GROUP_CHAT_CREATE_RETURN
    0x089B = CMSG_GROUP_CHAT_DELETE_RETURN
    0x089D = CMSG_GROUP_CHAT_RENAME_RETURN
    0x089F = CMSG_GROUP_CHAT_ADD_MEMBER_RETURN
    0x08A2 = CMSG_GROUP_CHAT_MEMBER_LIST_RETURN
    0x1290 = CMSG_SET_CHAT_HONOR_RETURN

  [SYN/SYNC - Server Push] (119 opcodes)
    0x0033 = CMSG_SYN_ATTRIBUTE_CHANGE
    0x0037 = CMSG_SYN_EXTRA_ATTRIBUTE_CHANGE
    0x0043 = CMSG_SYN_SERVER_TIME
    0x004A = CMSG_SYN_VERSION_CONTROL
    0x01D4 = CMSG_SYN_CITYDEFENSE_FIRE
    0x01D5 = CMSG_SYN_UPGRADE_REWARD
    0x021C = CMSG_SYN_ALL_QUEST
    0x0244 = CMSG_SYNC_DOMINION_INFO
    0x0247 = CMSG_SYNC_DOMINION_SIMPLE_BATTLE_INFO
    0x0259 = CMSG_SYNC_DOMINION_OFFICIAL_INFO
    0x0282 = CMSG_SYN_SIGN_CONFIG
    0x0283 = CMSG_SYN_SIGN_INFO
    0x02F1 = CMSG_SYNC_CYCLE_ACTION
    0x02F2 = CMSG_SYNC_CYCLE_ACTION_ID
    0x039B = CMSG_SYNC_LUCKY_TURNTABLE_INFO
    0x05F4 = CMSG_SYNC_ARENA_INFO
    0x07B3 = CMSG_SYNC_MOBILIZATION_ACTION
    0x07C7 = CMSG_SYNC_MOBILIZATION_TASK_DELETE
    0x07C8 = CMSG_SYNC_MOBILIZATION_TASK_REFRESH
    0x07C9 = CMSG_SYNC_MOBILIZATION_UPDATE_MY_TASK
    0x07CA = CMSG_SYNC_MOBILIZATION_MY_TASK
    0x07E8 = CMSG_SYNC_LEAGUE_BATTLEFIELD_ACTION
    0x083F = CMSG_SYNC_WORLD_BATTLE_ACTION_CONFIG
    0x0859 = CMSG_SYNC_FORCE_POWER_INFO_REQUEST
    0x0867 = CMSG_SYNC_ANNIVERSARY_DONATE_INFO
    0x08A4 = CMSG_SYNC_GROUP_CHAT_ADD_MEMBER
    0x08A5 = CMSG_SYNC_GROUP_CHAT_DEL_MEMBER
    0x08A6 = CMSG_SYNC_GROUP_CHAT_EXIT_GROUP
    0x08A7 = CMSG_SYNC_GROUP_CHAT_LEAVE_SERVER
    0x08A8 = CMSG_SYNC_GROUP_CHAT_INFO
    0x08A9 = CMSG_SYNC_GROUP_CHAT_MEMBER_BE_ADD
    0x08AA = CMSG_SYNC_GROUP_CHAT_MEMBER_BE_DEL
    0x0938 = CMSG_SYNC_KNIGHT_ACTION_CONFIG
    0x0992 = CMSG_SYNC_KING_ROAD_QUEST_INFO
    0x0995 = CMSG_SYNC_KING_ROAD_ONE_QUEST_INFO
    0x099C = CMSG_SYNC_COMMON_EXCHAGE_ACTIVITY_INFO
    0x09A6 = CMSG_SYNC_LUCKY_SHOP_INFO
    0x09A8 = CMSG_SYNC_LUCKY_SHOP_FLAG
    0x09BA = CMSG_SYNC_OPERATION_ACTION_CONFIG
    0x09BC = CMSG_SYNC_OPERATION_ACTION
    0x09D8 = CMSG_SYNC_TREASURE_CARD_QUEST_INFO
    0x0A00 = CMSG_SYNC_CHAMPIONSHIP_CONFIG
    0x0A02 = CMSG_SYN_ALL_QUEST_CHAMPIONSHIP
    0x0A09 = CMSG_SYNC_CHAMPIONSHIP_GIFT_ID
    0x0A0A = CMSG_SYNC_CHAMPIONSHIP_BOX_ID
    0x0A0B = CMSG_SYNC_CHAMPIONSHIP_BANNER_ID
    0x0A2B = CMSG_SYNC_KING_CHESS_ACTION
    0x0A3D = CMSG_SYNC_LEAGUE_KING_CHESS_DEL
    0x0A3E = CMSG_SYNC_LEAGUE_KING_CHESS_ADD
    0x0A41 = CMSG_SYNC_DEFEND_INFO_KING_CHESS
    0x0B54 = CMSG_SYNC_LUCKY_LINE_INFO
    0x0B5E = CMSG_SYNC_KINGDOM_ACTION_CONFIG
    0x0B60 = CMSG_SYNC_KINGDOM_ACTION
    0x0C4E = CMSG_SYNC_LEAGUE_BATTLEFIELD_CONFIG
    0x0CB2 = CMSG_SYNC_NOVICE_FREE_PURCHASE_INFO
    0x0E74 = CMSG_SYNC_WHEEL_INFO
    0x0EA6 = CMSG_SYNC_DAILY_RECHARGE_INFO
    0x0F0E = CMSG_SYNC_FORTRESS_ACTION
    0x0F6E = CMSG_SYNC_COMMON_ACTION_TIME_CONFIG
    0x11C8 = CMSG_SYNC_FIXED_TIME
    0x125C = CMSG_SYNC_RUSH_ACTION_CONFIG
    0x125E = CMSG_SYNC_RUSH_ACTION
    0x128E = CMSG_SYNC_HONOR
    0x12F2 = CMSG_SYNC_ACTIVEGIFTS_CONFIG
    0x12F7 = CMSG_SYNC_ACTIVEGIFTS_TASK
    0x1356 = CMSG_SYNC_CUSTOMGIFTS_CONFIG
    0x1359 = CMSG_SYNC_CUSTOMGIFTS_GIFT
    0x1388 = CMSG_SYNC_WAR_LORD_ACTION_ID
    0x138A = CMSG_SYNC_WAR_LORD_ACTION
    0x1450 = CMSG_SYNC_DAILYCONSUME_CONFIG
    0x1455 = CMSG_SYNC_DAILYCONSUME_GOLD_CONSUME
    0x15AF = CMSG_SYNC_LOSTLAND_ACTION_CONFIG
    0x15BD = CMSG_SYNC_LOSTLAND_SHOP_BUY_TIMES
    0x15E6 = CMSG_SYNC_ALL_LEAGUEBUILD_BATTLE_COUNT
    0x15EB = CMSG_SYNC_LEAGUEBUILD_DEFEND_INFO
    0x15FE = CMSG_SYNC_LOSTLAND_MONTH_CARD_INFO
    0x1663 = CMSG_SYNC_LEAGUEPASS_ACTION
    0x1672 = CMSG_SYNC_LEAGUEPASS_TASK_REFRESH
    0x1673 = CMSG_SYNC_LEAGUEPASS_UPDATE_MY_TASK
    0x1674 = CMSG_SYNC_LEAGUEPASS_ADVANCEDGIFT
    0x16AF = CMSG_SYNC_EXTRA_GIFTPACK_ACTION_NEW
    0x16B0 = CMSG_SYNC_EXTRA_GIFTPACK_NEW
    0x16B1 = CMSG_SYNC_EXTRA_GIFTPACK_TASK_NEW
    0x173E = CMSG_SYNC_MERGE_EVNET_ACTION
    0x173F = CMSG_SYNC_MERGE_EVNET_ACTION_CONFIG
    0x1770 = CMSG_SYNC_RECHARGEBONUS_CONFIG
    0x1773 = CMSG_SYNC_RECHARGEBONUS_TIMES
    0x178E = CMSG_SYNC_LOST_KING_ROAD_QUEST_INFO
    0x1791 = CMSG_SYNC_LOST_KING_ROAD_ONE_QUEST_INFO
    0x1838 = CMSG_SYNC_CONTINUITY_GIFTPACK_ACTION
    0x183B = CMSG_SYNC_CONTINUITY_GIFTPACK_BUY
    0x186A = CMSG_SYNC_FTRIEND_GIFT_CONFIG
    0x18CE = CMSG_SYNC_KINGDOM_GIFT_CONFIG
    0x18CF = CMSG_SYNC_KINGDOM_GIFT_DATA
    0x18D0 = CMSG_SYNC_KINGDOM_GIFT_LEVEL
    0x18D1 = CMSG_SYNC_KINGDOM_GIFT_REWARD
    0x1932 = CMSG_SYNC_AUTO_HANDUP
    0x1996 = CMSG_SYNC_NEWSERVER_ACTION
    0x1997 = CMSG_SYNC_NEWSERVER_RECORDCOST
    0x199A = CMSG_SYNC_NEWSERVER_LIMITSHOP
    0x199F = CMSG_SYNC_NEWSERVER_SIGNINFUND
    0x19C8 = CMSG_SYNC_MINI_GAME_CONFIG
    0x19CD = CMSG_SYNC_MINI_GAME_INFO
    0x19CE = CMSG_SYNC_MINI_GAME_REWARD_TIMES
    0x1AC2 = CMSG_SYNC_DAMAGE_INFO
    0x1AF4 = CMSG_SYNC_CLANPK_CONFIG
    0x1AF5 = CMSG_SYNC_CLANPK_INFO
    0x1AF6 = CMSG_SYNC_CLANPK_FINAL_DETAIL_INFO
    0x1B17 = CMSG_SYNC_CLANPK_DEFEND_INFO
    0x1B19 = CMSG_SYNC_CLANPK_ATTACK_INFO
    0x1C22 = CMSG_SYNC_BUILDING_SKIN_INFO
    0x1DE2 = CMSG_SYNC_CONTINUOUS_TASK_ACTION
    0x1DE5 = CMSG_SYNC_CONTINUOUS_TASK_BUY
    0x1E14 = CMSG_SYNC_ALLFORONE_INFO
    0x1EAA = CMSG_SYNC_AUTO_JOIN_BUILDUP_INFO
    0x1F0E = CMSG_SYNC_LEAGUE_BIG_BOSS_CONFIG
    0x1F19 = CMSG_SYNC_LEAGUE_BIG_BOSS_INFO
    0x1F1A = CMSG_SYNC_LEAGUE_BIG_BOSS_REWARD_TIMES
    0x1FAC = CMSG_SYNC_LOSTLAND_RUSH_EVENT


================================================================================
PART B: PCAP ANALYSIS OF SERVER RESPONSES
================================================================================

Found 114 PCAP files
Scanning 25 priority PCAPs...
Total S2C packets collected: 5825
Unique S2C opcodes seen: 279


--- Step 4: _RETURN Opcodes Found in PCAPs ---

_RETURN opcodes with PCAP data: 17 / 303

  0x000C = CMSG_LOGIN_RETURN (6 samples)
    Total len: 68, Payload len: 64
    First 40B payload: C9 AA 1E 7C 00 00 00 00 0D 00 35 34 2E 39 33 2E 31 39 32 2E 32 34 30 58 1B 20 00 35 31 30 63 34 32 36 35 34 61 34 66 33
    Payload sizes: min=63, max=64, avg=63

  0x0020 = CMSG_ENTER_GAME_RETURN (3 samples)
    Total len: 5, Payload len: 1
    First 40B payload: 01
    Payload sizes: min=1, max=1, avg=1

  0x0022 = CMSG_USERINFO_RETURN (21 samples)
    Total len: 39, Payload len: 35
    First 40B payload: 20 00 63 32 31 61 36 31 62 31 35 32 36 62 35 36 62 38 66 34 61 31 37 37 61 30 35 66 65 62 36 39 31 37 02
    Payload sizes: min=35, max=35, avg=35

  0x0024 = CMSG_QUICK_LOGIN_RETURN (16 samples)
    Total len: 5, Payload len: 1
    First 40B payload: 03
    Payload sizes: min=1, max=1, avg=1

  0x009E = CMSG_BUILDING_OPERAT_RETURN (8 samples)
    Total len: 28, Payload len: 24
    First 40B payload: 05 00 00 00 00 35 00 34 00 16 00 75 34 00 00 00 00 00 00 C8 AF 00 00 03
    Payload sizes: min=24, max=24, avg=24

  0x022B = CMSG_POWER_TASKS_RETURN (21 samples)
    Total len: 216, Payload len: 212
    First 40B payload: 06 00 00 00 98 01 00 00 01 00 00 00 03 00 00 00 01 00 00 00 01 00 00 00 02 00 00 00 01 00 00 00 03 00 00 00 01 00 00 00
    Payload sizes: min=212, max=212, avg=212

  0x02F5 = CMSG_QUERY_SPECIAL_EVENT_RETURN (21 samples)
    Total len: 86, Payload len: 82
    First 40B payload: 04 00 B8 0B 00 00 80 78 B5 60 00 00 00 00 44 FC 7F F3 00 00 00 00 B9 0B 00 00 00 A5 CB 61 00 00 00 00 44 FC 7F F3 00 00
    Payload sizes: min=82, max=102, avg=82

  0x0795 = CMSG_ROYAL_SHOP_ITEM_CONFIG_RETURN (21 samples)
    Total len: 158, Payload len: 154
    First 40B payload: 0C 00 06 00 00 00 91 0B 00 00 64 00 00 00 06 00 00 00 92 0B 00 00 64 00 00 00 06 00 00 00 93 0B 00 00 64 00 00 00 06 00
    Payload sizes: min=154, max=154, avg=154

  0x0799 = CMSG_ROYAL_SHOP_ITEM_INFO_RETURN (21 samples)
    Total len: 6, Payload len: 2
    First 40B payload: 00 00
    Payload sizes: min=2, max=2, avg=2

  0x0841 = CMSG_WORLD_BATTLE_ACTION_RETURN (21 samples)
    Total len: 57, Payload len: 53
    First 40B payload: 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    Payload sizes: min=53, max=53, avg=53

  0x099E = CMSG_COMMON_EXCHAGE_COUNT_RETURN (95 samples)
    Total len: 12, Payload len: 8
    First 40B payload: 93 01 00 00 00 00 00 00
    Payload sizes: min=8, max=8, avg=8

  0x0A2D = CMSG_KING_CHESS_ACTION_DETAIL_INFO_RETURN (20 samples)
    Total len: 95, Payload len: 91
    First 40B payload: 08 00 00 00 00 00 00 00 5A 76 38 00 00 00 00 00 00 00 00 00 00 00 00 00 33 E2 A1 00 00 00 00 00 00 00 00 00 00 00 00 00
    Payload sizes: min=79, max=91, avg=82

  0x0AF3 = CMSG_REWARD_POINT_SHOP_ITEM_INFO_RETURN (24 samples)
    Total len: 22, Payload len: 18
    First 40B payload: 00 00 50 0D 49 68 00 00 00 00 14 53 4E 68 00 00 00 00
    Payload sizes: min=18, max=18, avg=18

  0x1358 = CMSG_CUSTOMGIFTS_ACTION_RETURN (4 samples)
    Total len: 28, Payload len: 24
    First 40B payload: 02 00 00 00 00 00 04 00 16 00 00 00 22 00 00 00 2B 00 00 00 2C 00 00 00
    Payload sizes: min=24, max=24, avg=24

  0x16CB = CMSG_SYNC_RETURN_EVNET_ACTION_NEW (21 samples)
    Total len: 34, Payload len: 30
    First 40B payload: 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    Payload sizes: min=30, max=30, avg=30

  0x170E = CMSG_HERO_COLLECTION_ACTION_RETURN (4 samples)
    Total len: 109, Payload len: 105
    First 40B payload: 02 00 00 00 6A 00 00 00 00 00 00 00 00 00 00 00 6A 00 00 00 00 00 00 05 00 01 00 00 00 01 00 00 00 1A B5 00 00 01 00 00
    Payload sizes: min=89, max=121, avg=109

  0x183A = CMSG_CONTINUITY_GIFTPACK_ACTION_RETURN (15 samples)
    Total len: 36, Payload len: 32
    First 40B payload: 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    Payload sizes: min=32, max=32, avg=32


--- Step 5: Detailed Decoding of Key Server Responses ---

----------------------------------------------------------------------
  0x0033 = CMSG_SYN_ATTRIBUTE_CHANGE
  Samples found: 12

  Sample 1 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 20B, Payload: 16B
    Hex: 07 00 00 00 A3 00 00 00 00 00 00 00 00 00 00 00
    Parsed: entry_count=7
      [0] id=0xA30000(10682368), type=0, val=0

  Sample 2 from PCAPdroid_25_Mar_07_29_40.pcap:
    Total raw: 20B, Payload: 16B
    Hex: 07 00 00 00 AC 00 00 00 00 00 00 00 00 00 00 00
    Parsed: entry_count=7
      [0] id=0xAC0000(11272192), type=0, val=0

  Sample 3 from PCAPdroid_27_Mar_09_17_04.pcap:
    Total raw: 20B, Payload: 16B
    Hex: 07 00 00 00 C8 00 00 00 00 00 00 00 00 00 00 00
    Parsed: entry_count=7
      [0] id=0xC80000(13107200), type=0, val=0

----------------------------------------------------------------------
  0x0043 = CMSG_SYN_SERVER_TIME
  Samples found: 8

  Sample 1 from PCAPdroid_25_Mar_07_29_40.pcap:
    Total raw: 20B, Payload: 16B
    Hex: 0A 2D 00 00 00 00 00 00 7B 1E C3 69 00 00 00 00
    Parsed: server_time=11530 (unix timestamp)
    Date: 1970-01-01 05:12:10
    field2=0

  Sample 2 from PCAPdroid_25_Mar_07_29_40.pcap:
    Total raw: 20B, Payload: 16B
    Hex: 15 3E 00 00 00 00 00 00 7F 1E C3 69 00 00 00 00
    Parsed: server_time=15893 (unix timestamp)
    Date: 1970-01-01 06:24:53
    field2=0

  Sample 3 from PCAPdroid_27_Mar_09_17_04.pcap:
    Total raw: 20B, Payload: 16B
    Hex: 46 FC 00 00 00 00 00 00 A3 DA C5 69 00 00 00 00
    Parsed: server_time=64582 (unix timestamp)
    Date: 1970-01-01 19:56:22
    field2=0

----------------------------------------------------------------------
  0x0042 = UNKNOWN_0x0042
  Samples found: 67

  Sample 1 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 12B, Payload: 8B
    Hex: 74 0E 22 00 00 00 00 00

  Sample 2 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 12B, Payload: 8B
    Hex: 16 49 22 00 00 00 00 00

  Sample 3 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 12B, Payload: 8B
    Hex: B7 83 22 00 00 00 00 00

----------------------------------------------------------------------
  0x000C = CMSG_LOGIN_RETURN
  Samples found: 6

  Sample 1 from actions_capture.pcap:
    Total raw: 68B, Payload: 64B
    Hex: C9 AA 1E 7C 00 00 00 00 0D 00 35 34 2E 39 33 2E 31 39 32 2E 32 34 30 58 1B 20 00 35 31 30 63 34 32 36 35 34 61 34 66 33 63 61 66 61 36 62 61 66 62 66 39 30 64 34 64 30 63 39 34 01
    Parsed: result_code=43721
    field2=0x7C1E
    field3=0x00000000 (0)
    field4=0x3435000D (875888653)
    field5=0x2E33392E (775108910)
    field6=0x2E323931 (775043377)
    field7=0x58303432 (1479554098)
    field8=0x3500201B (889200667)
    field9=0x34633031 (878915633)
    field10=0x34353632 (875902514)
    field11=0x33663461 (862336097)
    field12=0x61666163 (1634099555)
    field13=0x66616236 (1717658166)
    field14=0x30396662 (809068130)
    field15=0x30643464 (811873380)
    field16=0x01343963 (20199779)
    field17=0x000000D3 (211)

  Sample 2 from capture.pcap:
    Total raw: 68B, Payload: 64B
    Hex: C9 AA 1E 7C 00 00 00 00 0D 00 35 34 2E 39 33 2E 31 39 32 2E 32 34 30 58 1B 20 00 62 35 32 63 30 66 34 31 63 65 37 61 32 64 65 63 33 62 30 64 35 61 37 37 65 32 39 61 62 31 66 32 01
    Parsed: result_code=43721
    field2=0x7C1E
    field3=0x00000000 (0)
    field4=0x3435000D (875888653)
    field5=0x2E33392E (775108910)
    field6=0x2E323931 (775043377)
    field7=0x58303432 (1479554098)
    field8=0x6200201B (1644175387)
    field9=0x30633235 (811807285)
    field10=0x63313466 (1664169062)
    field11=0x32613765 (845231973)
    field12=0x33636564 (862152036)
    field13=0x35643062 (895758434)
    field14=0x65373761 (1698117473)
    field15=0x62613932 (1650538802)
    field16=0x01326631 (20080177)
    field17=0x000000D3 (211)

  Sample 3 from capture2.pcap:
    Total raw: 68B, Payload: 64B
    Hex: C9 AA 1E 7C 00 00 00 00 0D 00 35 34 2E 39 33 2E 31 39 32 2E 32 34 30 58 1B 20 00 30 31 30 65 65 65 35 64 31 61 63 37 61 39 30 30 35 34 61 62 31 34 65 36 32 34 62 31 63 33 64 34 01
    Parsed: result_code=43721
    field2=0x7C1E
    field3=0x00000000 (0)
    field4=0x3435000D (875888653)
    field5=0x2E33392E (775108910)
    field6=0x2E323931 (775043377)
    field7=0x58303432 (1479554098)
    field8=0x3000201B (805314587)
    field9=0x65653031 (1701130289)
    field10=0x31643565 (828650853)
    field11=0x61376361 (1631019873)
    field12=0x35303039 (892350521)
    field13=0x31626134 (828530996)
    field14=0x32366534 (842425652)
    field15=0x63316234 (1664180788)
    field16=0x01346433 (20210739)
    field17=0x000000D3 (211)

----------------------------------------------------------------------
  0x0071 = UNKNOWN_0x0071
  Samples found: 6

  Sample 1 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 74B, Payload: 70B
    Hex: E1 62 09 00 B6 00 00 00 01 00 ED 02 73 22 00 00 00 00 01 B0 03 00 00 43 02 3E 03 26 02 53 03 6D 03 00 00 00 00 0E 00 31 30 30 30 32 33 35 39 38 33 32 38 2C 30 B6 00 00 00 00 00 00

  Sample 2 from PCAPdroid_25_Mar_07_29_40.pcap:
    Total raw: 74B, Payload: 70B
    Hex: 34 63 09 00 B6 00 00 00 01 00 ED 02 73 22 00 00 00 00 01 B0 03 00 00 43 02 3E 03 53 02 55 03 81 02 00 00 00 00 0E 00 31 30 30 30 32 33 35 38 38 31 30 35 2C 30 B6 00 00 00 00 00 00

  Sample 3 from PCAPdroid_27_Mar_09_17_04.pcap:
    Total raw: 74B, Payload: 70B
    Hex: A5 9B 09 00 B6 00 00 00 01 00 ED 02 73 22 00 00 00 00 01 B0 03 00 00 43 02 3E 03 3A 02 25 03 8A 00 00 00 00 00 0E 00 31 30 30 30 32 34 37 31 38 34 33 32 2C 30 B6 00 00 00 00 00 00

----------------------------------------------------------------------
  0x006F = UNKNOWN_0x006F
  ** NOT FOUND in any PCAP **

----------------------------------------------------------------------
  0x00B8 = UNKNOWN_0x00B8
  Samples found: 26

  Sample 1 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 5B, Payload: 1B
    Hex: 00

  Sample 2 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 14B, Payload: 10B
    Hex: 01 01 00 00 00 01 FF 00 00 00
    field1=0x0101 (257)
    field2=0x0000 (0)
    field3=0x00FF0100 (16711936)

  Sample 3 from PCAPdroid_25_Mar_07_29_40.pcap:
    Total raw: 5B, Payload: 1B
    Hex: 00

----------------------------------------------------------------------
  0x0037 = CMSG_SYN_EXTRA_ATTRIBUTE_CHANGE
  Samples found: 4

  Sample 1 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 16B, Payload: 12B
    Hex: 16 00 00 00 73 19 C3 69 00 00 00 00
    Parsed: entry_count=22

  Sample 2 from PCAPdroid_25_Mar_07_29_40.pcap:
    Total raw: 16B, Payload: 12B
    Hex: 16 00 00 00 4B 1F C3 69 00 00 00 00
    Parsed: entry_count=22

  Sample 3 from PCAPdroid_28_Mar_10_41_12.pcap:
    Total raw: 16B, Payload: 12B
    Hex: 16 00 00 00 84 40 C7 69 00 00 00 00
    Parsed: entry_count=22

----------------------------------------------------------------------
  0x06C2 = UNKNOWN_0x06C2
  Samples found: 24

  Sample 1 from PCAPdroid_25_Mar_07_05_12.pcap:
    Total raw: 116B, Payload: 112B
    Hex: 04 00 00 00 01 00 00 00 05 00 55 0B 00 00 00 00 00 00 02 00 00 00 05 00 93 62 14 00 00 00 00 00 04 00 00 00 05 00 90 C3 13 00 00 00 00 00 08 00 00 00 05 00 35 B6 05 00 00 00 00 00
    Header u32: 4
    Alt: count_u16=4, field2_u16=0

  Sample 2 from PCAPdroid_25_Mar_07_29_40.pcap:
    Total raw: 116B, Payload: 112B
    Hex: 04 00 00 00 01 00 00 00 05 00 55 0B 00 00 00 00 00 00 02 00 00 00 05 00 93 62 14 00 00 00 00 00 04 00 00 00 05 00 90 C3 13 00 00 00 00 00 08 00 00 00 05 00 35 B6 05 00 00 00 00 00
    Header u32: 4
    Alt: count_u16=4, field2_u16=0

  Sample 3 from PCAPdroid_27_Mar_09_17_04.pcap:
    Total raw: 132B, Payload: 128B
    Hex: 04 00 00 00 01 00 00 00 05 00 0E 17 00 00 00 00 00 00 02 00 00 00 05 00 0F 72 14 00 00 00 00 00 04 00 00 00 05 00 9A C3 13 00 00 00 00 00 08 00 00 00 05 00 11 BD 05 00 00 00 00 00
    Header u32: 4
    Alt: count_u16=4, field2_u16=0


--- Step 6: SOLDIER_INFO (0x06C2) 27-Byte Entry Analysis ---
  Total SOLDIER_INFO packets: 24

  Sample 1 from PCAPdroid_25_Mar_07_05_12.pcap: 112B payload
  Full hex: 04 00 00 00 01 00 00 00 05 00 55 0B 00 00 00 00 00 00 02 00 00 00 05 00 93 62 14 00 00 00 00 00 04 00 00 00 05 00 90 C3 13 00 00 00 00 00 08 00 00 00 05 00 35 B6 05 00 00 00 00 00 04 00 00 00 01 00 00 00 74 43 01 00 02 00 00 00 40 F3 00 00 04 00 00 00 40 6C 01 00 08 00 00 00 C9 9A 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

  Header=4B (val=4), 4 entries of 27B

    Entry 0: 01 00 00 00 05 00 55 0B 00 00 00 00 00 00 02 00 00 00 05 00 93 62 14 00 00 00 00
      [A: u32x6+u16+u8]
        type_id: 1
        subtype: 190119941 (0xB550005)
        count: 0
        wounded: 131072 (0x20000)
        f5: 327680 (0x50000)
        f6: 1335955 (0x146293)
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8] <<LIKELY
        type_id: 1
        tier: 5
        count: 2901 (0xB55)
        wounded: 0
        f5: 2
        f6: 1653800965 (0x62930005)
        f7: 20
        f8: 0
        f9: 0
      [C: u16+u8+u32x6]
        type_id: 1
        tier: 0
        count: 1426064640 (0x55000500)
        wounded: 11
        f5: 33554432 (0x2000000)
        f6: 83886080 (0x5000000)
        f7: 342004480 (0x14629300)
        f8: 0
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 1
        type: 5
        tier: 0
        level: 85
        count: 11
        wounded: 33554432 (0x2000000)
        f5: 83886080 (0x5000000)
        f6: 342004480 (0x14629300)
        f7: 0
      [E: u16x2+u8+u32x5+u16] <<LIKELY
        type_id: 1
        tier: 0
        level: 5
        count: 742656 (0xB5500)
        wounded: 0
        f5: 512 (0x200)
        f6: 2466252032 (0x93000500)
        f7: 5218 (0x1462)
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 1
        f2: 190119941 (0xB550005)
        f3: 0
        f4: 131072 (0x20000)
        f5: 327680 (0x50000)
        f6: 1335955 (0x146293)
        f7: 0
        f8: 0

    Entry 1: 00 04 00 00 00 05 00 90 C3 13 00 00 00 00 00 08 00 00 00 05 00 35 B6 05 00 00 00
      [A: u32x6+u16+u8]
        type_id: 1024 (0x400)
        subtype: 2415920384 (0x90000500)
        count: 5059 (0x13C3)
        wounded: 134217728 (0x8000000)
        f5: 83886080 (0x5000000)
        f6: 95827200 (0x5B63500)
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 1024 (0x400)
        tier: 1280 (0x500)
        count: 331583488 (0x13C39000)
        wounded: 0
        f5: 2048 (0x800)
        f6: 889193728 (0x35000500)
        f7: 1462 (0x5B6)
        f8: 0
        f9: 0
      [C: u16+u8+u32x6] <<LIKELY
        type_id: 1024 (0x400)
        tier: 0
        count: 327680 (0x50000)
        wounded: 1295248 (0x13C390)
        f5: 0
        f6: 8
        f7: 3056926725 (0xB6350005)
        f8: 5
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 1024 (0x400)
        type: 0
        tier: 5
        level: 0
        count: 1295248 (0x13C390)
        wounded: 0
        f5: 8
        f6: 3056926725 (0xB6350005)
        f7: 5
      [E: u16x2+u8+u32x5+u16]
        type_id: 1024 (0x400)
        tier: 0
        level: 0
        count: 3280994309 (0xC3900005)
        wounded: 19
        f5: 524288 (0x80000)
        f6: 327680 (0x50000)
        f7: 374325 (0x5B635)
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 1024 (0x400)
        f2: 2415920384 (0x90000500)
        f3: 5059 (0x13C3)
        f4: 134217728 (0x8000000)
        f5: 83886080 (0x5000000)
        f6: 95827200 (0x5B63500)
        f7: 0
        f8: 0

    Entry 2: 00 00 04 00 00 00 01 00 00 00 74 43 01 00 02 00 00 00 40 F3 00 00 04 00 00 00 40
      [A: u32x6+u16+u8]
        type_id: 262144 (0x40000)
        subtype: 65536 (0x10000)
        count: 1131675648 (0x43740000)
        wounded: 131073 (0x20001)
        f5: 4081057792 (0xF3400000)
        f6: 262144 (0x40000)
        f7: 0
        f8: 64
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 262144 (0x40000)
        tier: 0
        count: 1
        wounded: 82804 (0x14374)
        f5: 2
        f6: 62272 (0xF340)
        f7: 4
        f8: 0
        f9: 64
      [C: u16+u8+u32x6]
        type_id: 0
        tier: 4
        count: 16777216 (0x1000000)
        wounded: 1946157056 (0x74000000)
        f5: 33554755 (0x2000143)
        f6: 1073741824 (0x40000000)
        f7: 67109107 (0x40000F3)
        f8: 1073741824 (0x40000000)
      [D: u32+u8x3+u32x5]
        id: 262144 (0x40000)
        type: 0
        tier: 0
        level: 1
        count: 1946157056 (0x74000000)
        wounded: 33554755 (0x2000143)
        f5: 1073741824 (0x40000000)
        f6: 67109107 (0x40000F3)
        f7: 1073741824 (0x40000000)
      [E: u16x2+u8+u32x5+u16] <<LIKELY
        type_id: 0
        tier: 4
        level: 0
        count: 256 (0x100)
        wounded: 21197824 (0x1437400)
        f5: 512 (0x200)
        f6: 15941632 (0xF34000)
        f7: 1024 (0x400)
        f8: 16384 (0x4000)
      [F: u32x6+u16+u8] <<LIKELY
        f1: 262144 (0x40000)
        f2: 65536 (0x10000)
        f3: 1131675648 (0x43740000)
        f4: 131073 (0x20001)
        f5: 4081057792 (0xF3400000)
        f6: 262144 (0x40000)
        f7: 0
        f8: 64

    Entry 3: 6C 01 00 08 00 00 00 C9 9A 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      [A: u32x6+u16+u8]
        type_id: 134218092 (0x800016C)
        subtype: 3372220416 (0xC9000000)
        count: 410 (0x19A)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 134218092 (0x800016C)
        tier: 0
        count: 26921216 (0x19AC900)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0
        f9: 0
      [C: u16+u8+u32x6] <<LIKELY
        type_id: 364 (0x16C)
        tier: 0
        count: 8
        wounded: 105161 (0x19AC9)
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 134218092 (0x800016C)
        type: 0
        tier: 0
        level: 0
        count: 105161 (0x19AC9)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
      [E: u16x2+u8+u32x5+u16]
        type_id: 364 (0x16C)
        tier: 2048 (0x800)
        level: 0
        count: 2596864000 (0x9AC90000)
        wounded: 1
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 134218092 (0x800016C)
        f2: 3372220416 (0xC9000000)
        f3: 410 (0x19A)
        f4: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0

  Sample 2 from PCAPdroid_25_Mar_07_29_40.pcap: 112B payload
  Full hex: 04 00 00 00 01 00 00 00 05 00 55 0B 00 00 00 00 00 00 02 00 00 00 05 00 93 62 14 00 00 00 00 00 04 00 00 00 05 00 90 C3 13 00 00 00 00 00 08 00 00 00 05 00 35 B6 05 00 00 00 00 00 04 00 00 00 01 00 00 00 74 43 01 00 02 00 00 00 40 F3 00 00 04 00 00 00 40 6C 01 00 08 00 00 00 C9 9A 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

  Header=4B (val=4), 4 entries of 27B

    Entry 0: 01 00 00 00 05 00 55 0B 00 00 00 00 00 00 02 00 00 00 05 00 93 62 14 00 00 00 00
      [A: u32x6+u16+u8]
        type_id: 1
        subtype: 190119941 (0xB550005)
        count: 0
        wounded: 131072 (0x20000)
        f5: 327680 (0x50000)
        f6: 1335955 (0x146293)
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8] <<LIKELY
        type_id: 1
        tier: 5
        count: 2901 (0xB55)
        wounded: 0
        f5: 2
        f6: 1653800965 (0x62930005)
        f7: 20
        f8: 0
        f9: 0
      [C: u16+u8+u32x6]
        type_id: 1
        tier: 0
        count: 1426064640 (0x55000500)
        wounded: 11
        f5: 33554432 (0x2000000)
        f6: 83886080 (0x5000000)
        f7: 342004480 (0x14629300)
        f8: 0
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 1
        type: 5
        tier: 0
        level: 85
        count: 11
        wounded: 33554432 (0x2000000)
        f5: 83886080 (0x5000000)
        f6: 342004480 (0x14629300)
        f7: 0
      [E: u16x2+u8+u32x5+u16] <<LIKELY
        type_id: 1
        tier: 0
        level: 5
        count: 742656 (0xB5500)
        wounded: 0
        f5: 512 (0x200)
        f6: 2466252032 (0x93000500)
        f7: 5218 (0x1462)
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 1
        f2: 190119941 (0xB550005)
        f3: 0
        f4: 131072 (0x20000)
        f5: 327680 (0x50000)
        f6: 1335955 (0x146293)
        f7: 0
        f8: 0

    Entry 1: 00 04 00 00 00 05 00 90 C3 13 00 00 00 00 00 08 00 00 00 05 00 35 B6 05 00 00 00
      [A: u32x6+u16+u8]
        type_id: 1024 (0x400)
        subtype: 2415920384 (0x90000500)
        count: 5059 (0x13C3)
        wounded: 134217728 (0x8000000)
        f5: 83886080 (0x5000000)
        f6: 95827200 (0x5B63500)
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 1024 (0x400)
        tier: 1280 (0x500)
        count: 331583488 (0x13C39000)
        wounded: 0
        f5: 2048 (0x800)
        f6: 889193728 (0x35000500)
        f7: 1462 (0x5B6)
        f8: 0
        f9: 0
      [C: u16+u8+u32x6] <<LIKELY
        type_id: 1024 (0x400)
        tier: 0
        count: 327680 (0x50000)
        wounded: 1295248 (0x13C390)
        f5: 0
        f6: 8
        f7: 3056926725 (0xB6350005)
        f8: 5
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 1024 (0x400)
        type: 0
        tier: 5
        level: 0
        count: 1295248 (0x13C390)
        wounded: 0
        f5: 8
        f6: 3056926725 (0xB6350005)
        f7: 5
      [E: u16x2+u8+u32x5+u16]
        type_id: 1024 (0x400)
        tier: 0
        level: 0
        count: 3280994309 (0xC3900005)
        wounded: 19
        f5: 524288 (0x80000)
        f6: 327680 (0x50000)
        f7: 374325 (0x5B635)
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 1024 (0x400)
        f2: 2415920384 (0x90000500)
        f3: 5059 (0x13C3)
        f4: 134217728 (0x8000000)
        f5: 83886080 (0x5000000)
        f6: 95827200 (0x5B63500)
        f7: 0
        f8: 0

    Entry 2: 00 00 04 00 00 00 01 00 00 00 74 43 01 00 02 00 00 00 40 F3 00 00 04 00 00 00 40
      [A: u32x6+u16+u8]
        type_id: 262144 (0x40000)
        subtype: 65536 (0x10000)
        count: 1131675648 (0x43740000)
        wounded: 131073 (0x20001)
        f5: 4081057792 (0xF3400000)
        f6: 262144 (0x40000)
        f7: 0
        f8: 64
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 262144 (0x40000)
        tier: 0
        count: 1
        wounded: 82804 (0x14374)
        f5: 2
        f6: 62272 (0xF340)
        f7: 4
        f8: 0
        f9: 64
      [C: u16+u8+u32x6]
        type_id: 0
        tier: 4
        count: 16777216 (0x1000000)
        wounded: 1946157056 (0x74000000)
        f5: 33554755 (0x2000143)
        f6: 1073741824 (0x40000000)
        f7: 67109107 (0x40000F3)
        f8: 1073741824 (0x40000000)
      [D: u32+u8x3+u32x5]
        id: 262144 (0x40000)
        type: 0
        tier: 0
        level: 1
        count: 1946157056 (0x74000000)
        wounded: 33554755 (0x2000143)
        f5: 1073741824 (0x40000000)
        f6: 67109107 (0x40000F3)
        f7: 1073741824 (0x40000000)
      [E: u16x2+u8+u32x5+u16] <<LIKELY
        type_id: 0
        tier: 4
        level: 0
        count: 256 (0x100)
        wounded: 21197824 (0x1437400)
        f5: 512 (0x200)
        f6: 15941632 (0xF34000)
        f7: 1024 (0x400)
        f8: 16384 (0x4000)
      [F: u32x6+u16+u8] <<LIKELY
        f1: 262144 (0x40000)
        f2: 65536 (0x10000)
        f3: 1131675648 (0x43740000)
        f4: 131073 (0x20001)
        f5: 4081057792 (0xF3400000)
        f6: 262144 (0x40000)
        f7: 0
        f8: 64

    Entry 3: 6C 01 00 08 00 00 00 C9 9A 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      [A: u32x6+u16+u8]
        type_id: 134218092 (0x800016C)
        subtype: 3372220416 (0xC9000000)
        count: 410 (0x19A)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 134218092 (0x800016C)
        tier: 0
        count: 26921216 (0x19AC900)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0
        f9: 0
      [C: u16+u8+u32x6] <<LIKELY
        type_id: 364 (0x16C)
        tier: 0
        count: 8
        wounded: 105161 (0x19AC9)
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 134218092 (0x800016C)
        type: 0
        tier: 0
        level: 0
        count: 105161 (0x19AC9)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
      [E: u16x2+u8+u32x5+u16]
        type_id: 364 (0x16C)
        tier: 2048 (0x800)
        level: 0
        count: 2596864000 (0x9AC90000)
        wounded: 1
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 134218092 (0x800016C)
        f2: 3372220416 (0xC9000000)
        f3: 410 (0x19A)
        f4: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0

  Sample 3 from PCAPdroid_27_Mar_09_17_04.pcap: 128B payload
  Full hex: 04 00 00 00 01 00 00 00 05 00 0E 17 00 00 00 00 00 00 02 00 00 00 05 00 0F 72 14 00 00 00 00 00 04 00 00 00 05 00 9A C3 13 00 00 00 00 00 08 00 00 00 05 00 11 BD 05 00 00 00 00 00 04 00 00 00 01 00 00 00 26 4F 01 00 02 00 00 00 B3 02 01 00 04 00 00 00 40 6C 01 00 08 00 00 00 9B A1 01 00 01 00 00 00 01 00 00 00 01 00 00 00 E4 CB C4 69 00 00 00 00 00 00 00 00

  Sample 4 from PCAPdroid_27_Mar_09_17_04.pcap: 128B payload
  Full hex: 04 00 00 00 01 00 00 00 05 00 93 0D 00 00 00 00 00 00 02 00 00 00 05 00 0F 72 14 00 00 00 00 00 04 00 00 00 05 00 9A C3 13 00 00 00 00 00 08 00 00 00 05 00 11 BD 05 00 00 00 00 00 04 00 00 00 01 00 00 00 26 4F 01 00 02 00 00 00 B3 02 01 00 04 00 00 00 40 6C 01 00 08 00 00 00 9B A1 01 00 01 00 00 00 01 00 00 00 01 00 00 00 E4 CB C4 69 00 00 00 00 00 00 00 00

  Sample 5 from PCAPdroid_28_Mar_10_41_12.pcap: 112B payload
  Full hex: 04 00 00 00 01 00 00 00 05 00 A5 BE 00 00 00 00 00 00 02 00 00 00 05 00 26 2F 14 00 00 00 00 00 04 00 00 00 05 00 9A C3 13 00 00 00 00 00 08 00 00 00 05 00 17 E1 05 00 00 00 00 00 04 00 00 00 01 00 00 00 2F 90 00 00 02 00 00 00 B7 26 01 00 04 00 00 00 40 6C 01 00 08 00 00 00 F1 6F 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

  Header=4B (val=4), 4 entries of 27B

    Entry 0: 01 00 00 00 05 00 A5 BE 00 00 00 00 00 00 02 00 00 00 05 00 26 2F 14 00 00 00 00
      [A: u32x6+u16+u8]
        type_id: 1
        subtype: 3198484485 (0xBEA50005)
        count: 0
        wounded: 131072 (0x20000)
        f5: 327680 (0x50000)
        f6: 1322790 (0x142F26)
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8] <<LIKELY
        type_id: 1
        tier: 5
        count: 48805 (0xBEA5)
        wounded: 0
        f5: 2
        f6: 791019525 (0x2F260005)
        f7: 20
        f8: 0
        f9: 0
      [C: u16+u8+u32x6]
        type_id: 1
        tier: 0
        count: 2768241920 (0xA5000500)
        wounded: 190
        f5: 33554432 (0x2000000)
        f6: 83886080 (0x5000000)
        f7: 338634240 (0x142F2600)
        f8: 0
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 1
        type: 5
        tier: 0
        level: 165
        count: 190
        wounded: 33554432 (0x2000000)
        f5: 83886080 (0x5000000)
        f6: 338634240 (0x142F2600)
        f7: 0
      [E: u16x2+u8+u32x5+u16]
        type_id: 1
        tier: 0
        level: 5
        count: 12494080 (0xBEA500)
        wounded: 0
        f5: 512 (0x200)
        f6: 637535488 (0x26000500)
        f7: 5167 (0x142F)
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 1
        f2: 3198484485 (0xBEA50005)
        f3: 0
        f4: 131072 (0x20000)
        f5: 327680 (0x50000)
        f6: 1322790 (0x142F26)
        f7: 0
        f8: 0

    Entry 1: 00 04 00 00 00 05 00 9A C3 13 00 00 00 00 00 08 00 00 00 05 00 17 E1 05 00 00 00
      [A: u32x6+u16+u8]
        type_id: 1024 (0x400)
        subtype: 2583692544 (0x9A000500)
        count: 5059 (0x13C3)
        wounded: 134217728 (0x8000000)
        f5: 83886080 (0x5000000)
        f6: 98637568 (0x5E11700)
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 1024 (0x400)
        tier: 1280 (0x500)
        count: 331586048 (0x13C39A00)
        wounded: 0
        f5: 2048 (0x800)
        f6: 385877248 (0x17000500)
        f7: 1505 (0x5E1)
        f8: 0
        f9: 0
      [C: u16+u8+u32x6] <<LIKELY
        type_id: 1024 (0x400)
        tier: 0
        count: 327680 (0x50000)
        wounded: 1295258 (0x13C39A)
        f5: 0
        f6: 8
        f7: 3776380933 (0xE1170005)
        f8: 5
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 1024 (0x400)
        type: 0
        tier: 5
        level: 0
        count: 1295258 (0x13C39A)
        wounded: 0
        f5: 8
        f6: 3776380933 (0xE1170005)
        f7: 5
      [E: u16x2+u8+u32x5+u16]
        type_id: 1024 (0x400)
        tier: 0
        level: 0
        count: 3281649669 (0xC39A0005)
        wounded: 19
        f5: 524288 (0x80000)
        f6: 327680 (0x50000)
        f7: 385303 (0x5E117)
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 1024 (0x400)
        f2: 2583692544 (0x9A000500)
        f3: 5059 (0x13C3)
        f4: 134217728 (0x8000000)
        f5: 83886080 (0x5000000)
        f6: 98637568 (0x5E11700)
        f7: 0
        f8: 0

    Entry 2: 00 00 04 00 00 00 01 00 00 00 2F 90 00 00 02 00 00 00 B7 26 01 00 04 00 00 00 40
      [A: u32x6+u16+u8]
        type_id: 262144 (0x40000)
        subtype: 65536 (0x10000)
        count: 2418999296 (0x902F0000)
        wounded: 131072 (0x20000)
        f5: 649527296 (0x26B70000)
        f6: 262145 (0x40001)
        f7: 0
        f8: 64
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 262144 (0x40000)
        tier: 0
        count: 1
        wounded: 36911 (0x902F)
        f5: 2
        f6: 75447 (0x126B7)
        f7: 4
        f8: 0
        f9: 64
      [C: u16+u8+u32x6]
        type_id: 0
        tier: 4
        count: 16777216 (0x1000000)
        wounded: 788529152 (0x2F000000)
        f5: 33554576 (0x2000090)
        f6: 3070230528 (0xB7000000)
        f7: 67109158 (0x4000126)
        f8: 1073741824 (0x40000000)
      [D: u32+u8x3+u32x5]
        id: 262144 (0x40000)
        type: 0
        tier: 0
        level: 1
        count: 788529152 (0x2F000000)
        wounded: 33554576 (0x2000090)
        f5: 3070230528 (0xB7000000)
        f6: 67109158 (0x4000126)
        f7: 1073741824 (0x40000000)
      [E: u16x2+u8+u32x5+u16] <<LIKELY
        type_id: 0
        tier: 4
        level: 0
        count: 256 (0x100)
        wounded: 9449216 (0x902F00)
        f5: 512 (0x200)
        f6: 19314432 (0x126B700)
        f7: 1024 (0x400)
        f8: 16384 (0x4000)
      [F: u32x6+u16+u8] <<LIKELY
        f1: 262144 (0x40000)
        f2: 65536 (0x10000)
        f3: 2418999296 (0x902F0000)
        f4: 131072 (0x20000)
        f5: 649527296 (0x26B70000)
        f6: 262145 (0x40001)
        f7: 0
        f8: 64

    Entry 3: 6C 01 00 08 00 00 00 F1 6F 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      [A: u32x6+u16+u8]
        type_id: 134218092 (0x800016C)
        subtype: 4043309056 (0xF1000000)
        count: 367 (0x16F)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [B: u32+u16+u32x4+u16x2+u8]
        type_id: 134218092 (0x800016C)
        tier: 0
        count: 24113408 (0x16FF100)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0
        f9: 0
      [C: u16+u8+u32x6] <<LIKELY
        type_id: 364 (0x16C)
        tier: 0
        count: 8
        wounded: 94193 (0x16FF1)
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [D: u32+u8x3+u32x5] <<LIKELY
        id: 134218092 (0x800016C)
        type: 0
        tier: 0
        level: 0
        count: 94193 (0x16FF1)
        wounded: 0
        f5: 0
        f6: 0
        f7: 0
      [E: u16x2+u8+u32x5+u16]
        type_id: 364 (0x16C)
        tier: 2048 (0x800)
        level: 0
        count: 1878065152 (0x6FF10000)
        wounded: 1
        f5: 0
        f6: 0
        f7: 0
        f8: 0
      [F: u32x6+u16+u8] <<LIKELY
        f1: 134218092 (0x800016C)
        f2: 4043309056 (0xF1000000)
        f3: 367 (0x16F)
        f4: 0
        f5: 0
        f6: 0
        f7: 0
        f8: 0


--- BONUS: Top 50 Most Frequent S2C Opcodes ---

  Opcode  Count Name                                               Avg Size
--------------------------------------------------------------------------------
  0x026D    317 CMSG_CHAT_HISTORY                                    1387B
  0x099E     95 CMSG_COMMON_EXCHAGE_COUNT_RETURN                        8B
  0x0042     67 ???                                                     8B
  0x11F8     45 ???                                                    44B
  0x007B     42 CMSG_NOTIFY_OWNER_CASTLE                                9B
  0x0085     42 ???                                                  2402B
  0x06EB     42 ???                                                    25B
  0x036C     38 ???                                                     4B
  0x01E7     34 ???                                                     4B
  0x0211     34 ???                                                    40B
  0x0064     31 CMSG_ITEM_INFO                                       4781B
  0x0098     29 ???                                                    23B
  0x020D     27 ???                                                    10B
  0x00B8     26 ???                                                     2B
  0x00AA     25 CMSG_HERO_INFO                                       6064B
  0x0078     25 ???                                                   619B
  0x06C2     24 ???                                                   124B
  0x0AF3     24 CMSG_REWARD_POINT_SHOP_ITEM_INFO_RETURN                18B
  0x039B     21 CMSG_SYNC_LUCKY_TURNTABLE_INFO                         40B
  0x0654     21 CMSG_AF_INFO                                          796B
  0x004A     21 CMSG_SYN_VERSION_CONTROL                               32B
  0x0034     21 ???                                                   434B
  0x01D4     21 CMSG_SYN_CITYDEFENSE_FIRE                               4B
  0x0A00     21 CMSG_SYNC_CHAMPIONSHIP_CONFIG                          36B
  0x0A0A     21 CMSG_SYNC_CHAMPIONSHIP_BOX_ID                           2B
  0x0A0B     21 CMSG_SYNC_CHAMPIONSHIP_BANNER_ID                        2B
  0x0A02     21 CMSG_SYN_ALL_QUEST_CHAMPIONSHIP                      1484B
  0x07E4     21 CMSG_SYS_LEAGUE_BATTLEFIELD_INFO                       32B
  0x0C4E     21 CMSG_SYNC_LEAGUE_BATTLEFIELD_CONFIG                    80B
  0x084E     21 CMSG_WORLD_BATTLEFIELD_SYS_INFO                        38B
  0x083F     21 CMSG_SYNC_WORLD_BATTLE_ACTION_CONFIG                   60B
  0x0F0A     21 CMSG_SYS_FORTRESS_INFO                                  1B
  0x0F0E     21 CMSG_SYNC_FORTRESS_ACTION                              56B
  0x15AF     21 CMSG_SYNC_LOSTLAND_ACTION_CONFIG                       56B
  0x15F4     21 ???                                                   127B
  0x15C9     21 CMSG_LOSTLAND_DONATE_INFO                              50B
  0x15B0     21 CMSG_SYS_LOSTLAND_INFO                                155B
  0x020E     21 ???                                                     5B
  0x0267     21 ???                                                     4B
  0x060D     21 ???                                                     8B
  0x080C     21 ???                                                     4B
  0x1A90     21 CMSG_DINAR_BACK_INFO                                   36B
  0x0321     21 ???                                                   331B
  0x00B7     21 ???                                                   104B
  0x05E6     21 CMSG_AREN_HERO_QUEUE_INFO                              22B
  0x02E4     21 CMSG_STATUS_INFO                                        2B
  0x02E6     21 CMSG_STATUS_EXTRA_INFO                                  2B
  0x030C     21 ???                                                 42059B
  0x094D     21 ???                                                    12B
  0x030F     21 ???                                                     1B
```
