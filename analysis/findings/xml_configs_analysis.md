# Game Configuration Data Analysis - libgame.so

Extracted from ARM64 ELF binary `.rodata` section.

## Summary

| Category | Count |
|---|---|
| XML config files | 690 |
| URLs | 7 |
| IP addresses | 112 |
| API paths | 0 |
| CDN/asset paths | 27 |
| Error messages | 4930 |
| Debug/mechanic strings | 48578 |
| Item type strings | 29946 |
| JSON-related strings | 257 |

---
## 1. XML Configuration Files

**Total: 690 XML references found**

### Alliance (18 files)

| Offset | Filename |
|---|---|
| `0x025AD427` | `xml/activity_roud_award.xml` |
| `0x025861E1` | `xml/battle_animation.xml` |
| `0x02620B56` | `xml/battle_test.xml` |
| `0x025D3AFB` | `xml/clanpk_barrage.xml` |
| `0x0261433C` | `xml/clanpk_base.xml` |
| `0x025FA6B0` | `xml/clanpk_donate.xml` |
| `0x02607219` | `xml/clanpk_help.xml` |
| `0x025AD535` | `xml/clanpk_rank.xml` |
| `0x025AD549` | `xml/clanpk_shop.xml` |
| `0x025AD600` | `xml/elemental_war_desc.xml` |
| `0x02593385` | `xml/elemental_war_target.xml` |
| `0x025B3831` | `xml/guild_standoff.xml` |
| `0x0261A966` | `xml/lord_war_target.xml` |
| `0x02620D78` | `xml/lost_alliance_buff.xml` |
| `0x025F4175` | `xml/lost_alliance_icon.xml` |
| `0x0260095B` | `xml/lost_alliance_territory.xml` |
| `0x025FA8C0` | `xml/reduce_price_help_plan.xml` |
| `0x02571D80` | `xml/warlord_point.xml` |

### Animation (3 files)

| Offset | Filename |
|---|---|
| `0x0259943D` | `xml/arenaEffect.xml` |
| `0x025B9B96` | `xml/lord_effect.xml` |
| `0x0257F8E6` | `xml/operation_action.xml` |

### Audio (1 files)

| Offset | Filename |
|---|---|
| `0x025AD45F` | `xml/arenaSound.xml` |

### Buildings (32 files)

| Offset | Filename |
|---|---|
| `0x025A3577` | `xml/bloody_war_event_city.xml` |
| `0x025EDEF3` | `xml/bloody_war_event_city_desc.xml` |
| `0x025B9A11` | `xml/build_removecd.xml` |
| `0x0259F894` | `xml/building_base.xml` |
| `0x025E0AEC` | `xml/building_weight.xml` |
| `0x025CCFEE` | `xml/castle_fund.xml` |
| `0x0259F8AA` | `xml/castle_glory.xml` |
| `0x0257F695` | `xml/castle_up_arrow.xml` |
| `0x025B3799` | `xml/city_signature.xml` |
| `0x0260D183` | `xml/city_skin.xml` |
| `0x025994BE` | `xml/city_skin_source.xml` |
| `0x025FA697` | `xml/clanpk_build_def.xml` |
| `0x0259F8E5` | `xml/clanpk_build_pos.xml` |
| `0x0261A7CB` | `xml/clanpk_build_space.xml` |
| `0x02627271` | `xml/clanpk_build_special.xml` |
| `0x025C6A56` | `xml/clear_castle.xml` |
| `0x025C6A9E` | `xml/client_building_skin.xml` |
| `0x025F0FF3` | `xml/elemental_war_event_city.xml` |
| `0x025C6B9C` | `xml/Innercity_skin.xml` |
| `0x02600904` | `xml/Innercity_skin_effecttype.xml` |
| `0x025C6BB3` | `xml/Innercity_skin_quality.xml` |
| `0x025D3C41` | `xml/innercity_skin_source.xml` |
| `0x0261A8BF` | `xml/InnerDefinedCity.xml` |
| `0x025C0443` | `xml/lord_war_event_city.xml` |
| `0x025D3CD5` | `xml/lost_alliance_build.xml` |
| `0x02571BA7` | `xml/lost_altar_base.xml` |
| `0x025996D2` | `xml/novice_map_buildings.xml` |
| `0x025DA79D` | `xml/rebuilding_oasise.xml` |
| `0x02600ADE` | `xml/rebuilding_oasise_task.xml` |
| `0x0260D45D` | `xml/set_buildskin.xml` |
| `0x025D3E59` | `xml/userDefinedCity.xml` |
| `0x0258FF2A` | `xml/world_champion_event_city.xml` |

### Chat (7 files)

| Offset | Filename |
|---|---|
| `0x0258CACD` | `xml/chat_bubble.xml` |
| `0x025AD504` | `xml/chat_bubble_source.xml` |
| `0x025E0B2A` | `xml/chat_face.xml` |
| `0x026272E6` | `xml/greedygame_chat.xml` |
| `0x0261A948` | `xml/league_rank_mail.xml` |
| `0x0261A9BD` | `xml/mail_monitor.xml` |
| `0x02586566` | `xml/specialmail.xml` |

### Gacha (4 files)

| Offset | Filename |
|---|---|
| `0x025786E5` | `xml/crest_draw.xml` |
| `0x0258CB40` | `xml/doublelottery_base.xml` |
| `0x025A68C4` | `xml/doublelottery_group.xml` |
| `0x0262DB7A` | `xml/open_sesame_wheel.xml` |

### Heroes (24 files)

| Offset | Filename |
|---|---|
| `0x0256B403` | `xml/arena_skillTip.xml` |
| `0x02571A77` | `xml/bloody_war_event_talent.xml` |
| `0x0260D1AD` | `xml/clear_hero.xml` |
| `0x0259F98C` | `xml/hero_legend_base.xml` |
| `0x02620CA3` | `xml/hero_legend_comic.xml` |
| `0x025C6B3D` | `xml/hero_legend_lv.xml` |
| `0x02599579` | `xml/hero_legend_skill_type.xml` |
| `0x02586372` | `xml/hero_legend_task.xml` |
| `0x025933BE` | `xml/herocollection_event.xml` |
| `0x0262DA77` | `xml/herocollection_operation_event.xml` |
| `0x0261A898` | `xml/herocollection_package.xml` |
| `0x02620CBD` | `xml/herocollection_pve.xml` |
| `0x026143F4` | `xml/herocollection_recharge.xml` |
| `0x026008D3` | `xml/herocollection_story.xml` |
| `0x025C6B5D` | `xml/herocollection_task.xml` |
| `0x0256B53C` | `xml/herolottery_base.xml` |
| `0x02599598` | `xml/herolottery_group.xml` |
| `0x0259FA65` | `xml/lord_skill.xml` |
| `0x02571BBF` | `xml/lost_ban_hero.xml` |
| `0x025AD768` | `xml/luckystar_group.xml` |
| `0x0258CCBD` | `xml/open_sesame_hero.xml` |
| `0x025FA882` | `xml/open_sesame_random_hero.xml` |
| `0x0260D419` | `xml/pet_skill_upgrade.xml` |
| `0x02571DC8` | `xml/world_champion_event_leader.xml` |

### Items (243 files)

| Offset | Filename |
|---|---|
| `0x025D7421` | `resource/local/language.xml` |
| `0x025EAB51` | `resource/local/verson.xml` |
| `0x025F726F` | `resource/sound/sound.xml` |
| `0x0259C715` | `resource/test/test_config.xml` |
| `0x0261767B` | `resource/xml/activity_icon.xml` |
| `0x025EA8F0` | `resource/xml/anabasis_reset.xml` |
| `0x02596212` | `resource/xml/army_loss.xml` |
| `0x025DD88A` | `resource/xml/army_march_facade.xml` |
| `0x025A348F` | `resource/xml/armyskill.xml` |
| `0x02610D96` | `resource/xml/ballisticActConfig.xml` |
| `0x0256E697` | `resource/xml/banner_info.xml` |
| `0x025F0EA6` | `resource/xml/battleScene.xml` |
| `0x025B6A73` | `resource/xml/box.xml` |
| `0x02623E15` | `resource/xml/buff.xml` |
| `0x0257C563` | `resource/xml/buff_effect.xml` |
| `0x0258FE54` | `resource/xml/build_area.xml` |
| `0x025A34AF` | `resource/xml/building_function.xml` |
| `0x025754EC` | `resource/xml/building_levelup_info.xml` |
| `0x025B6B16` | `resource/xml/chat_face.xml` |
| `0x025F10B7` | `resource/xml/city_hp.xml` |
| `0x02610E1A` | `resource/xml/city_plus.xml` |
| `0x025EAABA` | `resource/xml/client_building.xml` |
| `0x0263C3CC` | `resource/xml/client_global.xml` |
| `0x0260A052` | `resource/xml/client_operate.xml` |
| `0x025C3430` | `resource/xml/client_system_box.xml` |
| `0x025FD75A` | `resource/xml/combo.xml` |
| `0x026177A9` | `resource/xml/daily_tasks.xml` |
| `0x025EA9DA` | `resource/xml/daily_tasks_reward.xml` |
| `0x02582DBB` | `resource/xml/dominion_build_client.xml` |
| `0x025CA016` | `resource/xml/dominion_infomation_icon.xml` |
| `0x025FD84D` | `resource/xml/dominion_place.xml` |
| `0x0259614B` | `resource/xml/drop_client.xml` |
| `0x02623F8D` | `resource/xml/effect.xml` |
| `0x0260A0F9` | `resource/xml/emoji.xml` |
| `0x025DD903` | `resource/xml/equip.xml` |
| `0x02610EBC` | `resource/xml/global.xml` |
| `0x0262A5D8` | `resource/xml/harbor.xml` |
| `0x025EAAF0` | `resource/xml/hero.xml` |
| `0x025D7384` | `resource/xml/hero_equip.xml` |
| `0x025F78C7` | `resource/xml/hero_legend_pve_scenario.xml` |
| `0x02582EB9` | `resource/xml/hero_level_grow.xml` |
| `0x025BD0B3` | `resource/xml/hero_star_grow.xml` |
| `0x0256EA3D` | `resource/xml/herocollection_pve_scenario.xml` |
| `0x0256E93A` | `resource/xml/Illegality_new.xml` |
| `0x026110A2` | `resource/xml/Illegality_new_exact.xml` |
| `0x025D0A3C` | `resource/xml/item.xml` |
| `0x02575688` | `resource/xml/item_shop.xml` |
| `0x02568637` | `resource/xml/item_speedup.xml` |
| `0x0261DC9C` | `resource/xml/league_accelerate.xml` |
| `0x02623FD1` | `resource/xml/league_science.xml` |
| `0x02568655` | `resource/xml/league_shop.xml` |
| `0x0260A659` | `resource/xml/league_short_name.xml` |
| `0x0257C72B` | `resource/xml/login_server.xml` |
| `0x025F754C` | `resource/xml/lord_head.xml` |
| `0x02562181` | `resource/xml/lord_order.xml` |
| `0x02623FFB` | `resource/xml/mail.xml` |
| `0x025FD831` | `resource/xml/map_client.xml` |
| `0x025A36A1` | `resource/xml/map_neighbour.xml` |
| `0x025BD04B` | `resource/xml/market.xml` |
| `0x0260A0A8` | `resource/xml/model.xml` |
| `0x026041B8` | `resource/xml/name.xml` |
| `0x025C34B6` | `resource/xml/npc_league.xml` |
| `0x02610F50` | `resource/xml/package_shop.xml` |
| `0x025D09F2` | `resource/xml/package_show.xml` |
| `0x025BD122` | `resource/xml/push.xml` |
| `0x025AA3A5` | `resource/xml/pve_scenario.xml` |
| `0x025621B3` | `resource/xml/quest.xml` |
| `0x025A9DA0` | `resource/xml/queue_config.xml` |
| `0x025D73A0` | `resource/xml/rank.xml` |
| `0x025C3573` | `resource/xml/science.xml` |
| `0x025A9CEF` | `resource/xml/server_map.xml` |
| `0x025D73C2` | `resource/xml/shop.xml` |
| `0x025D0A7F` | `resource/xml/skill.xml` |
| `0x025D0AD1` | `resource/xml/skillbuff.xml` |
| `0x02617893` | `resource/xml/soldier.xml` |
| `0x0258FFE8` | `resource/xml/soldier_population.xml` |
| `0x0257C51D` | `resource/xml/soldierBattle.xml` |
| `0x0262A635` | `resource/xml/soul.xml` |
| `0x0261DCCF` | `resource/xml/soul_evo.xml` |
| `0x025CA0C6` | `resource/xml/special_event.xml` |
| `0x0259C926` | `resource/xml/special_global.xml` |
| `0x0261DBE5` | `resource/xml/special_store.xml` |
| `0x025F111B` | `resource/xml/system_mail.xml` |
| `0x02575601` | `resource/xml/trap_constructor.xml` |
| `0x0263C3EB` | `resource/xml/ui_common_icon.xml` |
| `0x025B6BC2` | `resource/xml/up_reward.xml` |
| `0x025961F6` | `resource/xml/valuecount.xml` |
| `0x025EAAA2` | `resource/xml/vip_lv.xml` |
| `0x0257C7AB` | `resource/xml/wishing_pool.xml` |
| `0x025A6759` | `xml/achievement_score_reward.xml` |
| `0x025F3F19` | `xml/active_freepick_reward.xml` |
| `0x025C698B` | `xml/active_gifts.xml` |
| `0x025E0A13` | `xml/active_gifts_skin.xml` |
| `0x025650F7` | `xml/active_gifts_task.xml` |
| `0x025EDE6D` | `xml/activity_chess_guild_reward.xml` |
| `0x025931F4` | `xml/activity_chess_mark_reward.xml` |
| `0x025A6785` | `xml/activity_gift_pack.xml` |
| `0x02565156` | `xml/activity_knight_guild_reward.xml` |
| `0x02593220` | `xml/activity_knight_number_reward.xml` |
| `0x02607131` | `xml/activity_knight_point_reward.xml` |
| `0x02565189` | `xml/activity_knight_reward.xml` |
| `0x026271DE` | `xml/activity_rank_reward.xml` |
| `0x025651BD` | `xml/ad_item.xml` |
| `0x02593270` | `xml/AlarmItem.xml` |
| `0x0257F627` | `xml/all_for_one_reward.xml` |
| `0x0260D0DB` | `xml/arena_reward.xml` |
| `0x025AD472` | `xml/army_lossreward.xml` |
| `0x02571A2B` | `xml/black_current_reward.xml` |
| `0x025C0227` | `xml/bloody_war_event_bet_reward.xml` |
| `0x02599472` | `xml/bloody_war_event_season_reward.xml` |
| `0x025F3FBC` | `xml/bloody_war_prematch_reward_l.xml` |
| `0x025DA48D` | `xml/bloody_war_prematch_reward_p.xml` |
| `0x0259F86B` | `xml/bloody_war_prematch_reward_t.xml` |
| `0x025E7606` | `xml/bulk_rewards.xml` |
| `0x025CD002` | `xml/castle_up_reward.xml` |
| `0x025D3AEA` | `xml/chat_box.xml` |
| `0x0257F6AD` | `xml/clanpk_build_item.xml` |
| `0x025D3B12` | `xml/clanpk_player_reward.xml` |
| `0x02620BC5` | `xml/clanpk_rank_reward.xml` |
| `0x0256B4A3` | `xml/clear_item.xml` |
| `0x0256B4B6` | `xml/continuity_gift_pack.xml` |
| `0x025D3B2F` | `xml/continuity_gift_reward.xml` |
| `0x025A6896` | `xml/continuity_gift_token.xml` |
| `0x02593313` | `xml/daily_consume.xml` |
| `0x025E0B87` | `xml/daily_guild_reward.xml` |
| `0x025D3B4E` | `xml/daily_recharge_reward.xml` |
| `0x025D3B6C` | `xml/daily_shop_reward.xml` |
| `0x0257F6D3` | `xml/daily_tasks_reward.xml` |
| `0x025C02E7` | `xml/dessert_make_drop.xml` |
| `0x025AD5DD` | `xml/doublelottery_drop.xml` |
| `0x025C6ACC` | `xml/drop_show.xml` |
| `0x02586298` | `xml/elemental_war_event_lord_reward.xml` |
| `0x02593362` | `xml/elemental_war_event_reward.xml` |
| `0x025EDF99` | `xml/elemental_war_league_reward.xml` |
| `0x025EDFBD` | `xml/equip.xml` |
| `0x025B3800` | `xml/everyday_gift.xml` |
| `0x025E0BE1` | `xml/everyday_gift_new.xml` |
| `0x0260D21B` | `xml/everyday_gift_new_correct.xml` |
| `0x025C0368` | `xml/extra_gift_pack.xml` |
| `0x025862E2` | `xml/extra_gift_pack_quest.xml` |
| `0x02599504` | `xml/extra_gift_pack_reward.xml` |
| `0x025C0380` | `xml/fans_reward.xml` |
| `0x0262DA3A` | `xml/financial_expert_reward.xml` |
| `0x025E0BFB` | `xml/fixed_accumulation_reward.xml` |
| `0x025CD086` | `xml/friend_gift.xml` |
| `0x0260D23D` | `xml/general_shop_gift_pack.xml` |
| `0x02600872` | `xml/giant_invasion_treasure.xml` |
| `0x025652D5` | `xml/gift_invaluable.xml` |
| `0x02571B2C` | `xml/goodluck_drop.xml` |
| `0x025A68E8` | `xml/greedygame_resource.xml` |
| `0x0258634F` | `xml/guild_standoff_reward_duel.xml` |
| `0x026008A5` | `xml/guild_standoff_reward_rank.xml` |
| `0x025F4045` | `xml/guild_standoff_reward_star.xml` |
| `0x0260D263` | `xml/hero_equip.xml` |
| `0x025F4084` | `xml/herolottery_drop.xml` |
| `0x0258639C` | `xml/Innercity_upgrade_reward.xml` |
| `0x025A6956` | `xml/invite_reward.xml` |
| `0x0259F9FC` | `xml/item_refining.xml` |
| `0x025A696C` | `xml/kingdom_gift.xml` |
| `0x025FA77B` | `xml/kingdom_gift_reward_level.xml` |
| `0x0256B578` | `xml/kingdom_gift_reward_time.xml` |
| `0x025CD0E2` | `xml/kingdom_gift_reward_token.xml` |
| `0x0260D2D9` | `xml/kingdomreward_base.xml` |
| `0x02620D20` | `xml/kingdomreward_dialog.xml` |
| `0x02627323` | `xml/kingdomreward_lv.xml` |
| `0x025B9B4A` | `xml/kingdomreward_task.xml` |
| `0x0256B5AF` | `xml/kvk_reward.xml` |
| `0x025CD138` | `xml/latch_collider_property.xml` |
| `0x025CD158` | `xml/latch_gem_icon.xml` |
| `0x025787E4` | `xml/latch_object_property.xml` |
| `0x025FA79D` | `xml/latch_physics_materials.xml` |
| `0x025AD6F4` | `xml/league_event_rank_reward.xml` |
| `0x02565390` | `xml/league_event_reward.xml` |
| `0x025F410D` | `xml/league_gift.xml` |
| `0x025E0CC9` | `xml/lord_equip.xml` |
| `0x0259965B` | `xml/lord_equip_ment_suit.xml` |
| `0x025EE02B` | `xml/lord_gem.xml` |
| `0x025E77DF` | `xml/lord_gem_unlock.xml` |
| `0x025C040F` | `xml/lord_gem_upgrade.xml` |
| `0x025DA60A` | `xml/lord_material.xml` |
| `0x025C0428` | `xml/lord_material_type.xml` |
| `0x0260D37A` | `xml/lord_war_event_league_reward.xml` |
| `0x025DA629` | `xml/lord_war_event_lord_reward.xml` |
| `0x025F4157` | `xml/lord_war_event_reward.xml` |
| `0x025B390D` | `xml/lost_event_pre_reward.xml` |
| `0x025FA822` | `xml/lost_event_pre_reward_solo.xml` |
| `0x025B9C10` | `xml/lost_event_reward.xml` |
| `0x025AD739` | `xml/lost_rush_event_reward.xml` |
| `0x025EE062` | `xml/lucky_gift.xml` |
| `0x025B3948` | `xml/luna_shop_lucky_gift.xml` |
| `0x02620E06` | `xml/luxury_reward.xml` |
| `0x025C6C65` | `xml/magicLamp_treasure_base.xml` |
| `0x0260D3BE` | `xml/magicLamp_treasure_reward.xml` |
| `0x02571C3F` | `xml/magicLamp_treasure_score.xml` |
| `0x02571C60` | `xml/merge_item.xml` |
| `0x0262DB1D` | `xml/merge_reward.xml` |
| `0x025C6CA2` | `xml/navigation_rank_reward.xml` |
| `0x02578883` | `xml/novice_reward.xml` |
| `0x025C6CDE` | `xml/open_sesame_goods.xml` |
| `0x025A6AC4` | `xml/open_sesame_random_goods.xml` |
| `0x025B9C69` | `xml/open_sesame_reward_model.xml` |
| `0x025B9C9D` | `xml/PinBallMaterial.xml` |
| `0x0262DBD3` | `xml/place_item.xml` |
| `0x026073DD` | `xml/points_bidding_item.xml` |
| `0x02600AFD` | `xml/recharge_accumulation_reward.xml` |
| `0x025A6B15` | `xml/recharge_reward.xml` |
| `0x025654ED` | `xml/recycle_item.xml` |
| `0x025D3DC8` | `xml/red_envelopes_item.xml` |
| `0x02599782` | `xml/red_envelopes_reward.xml` |
| `0x0262DC0F` | `xml/reduce_price_gift.xml` |
| `0x02627451` | `xml/reduce_price_help_reward.xml` |
| `0x025621D2` | `xml/resource.xml` |
| `0x0257C6DE` | `xml/ResourcePath.xml` |
| `0x0259FB84` | `xml/rush_event_reward.xml` |
| `0x0258652E` | `xml/secret_item.xml` |
| `0x025C05AA` | `xml/server_merge_reward.xml` |
| `0x02620ECC` | `xml/shop_gift.xml` |
| `0x0262DC79` | `xml/subscribe_reward.xml` |
| `0x025B39F0` | `xml/super4choose1_reward.xml` |
| `0x025F430E` | `xml/task_reward.xml` |
| `0x0260D4B4` | `xml/total_recharge_reward.xml` |
| `0x025CD38E` | `xml/treasure.xml` |
| `0x0262DC92` | `xml/treasure_box.xml` |
| `0x0259FBFB` | `xml/treasure_card.xml` |
| `0x02600BA7` | `xml/treasure_card_drop.xml` |
| `0x02627506` | `xml/treasure_card_refresh.xml` |
| `0x0261AB28` | `xml/treasure_card_Shuffle.xml` |
| `0x025E7903` | `xml/treasure_card_skin.xml` |
| `0x0261AB46` | `xml/treasure_config.xml` |
| `0x025EE158` | `xml/trigger_gift.xml` |
| `0x025934F8` | `xml/upgrade_reward.xml` |
| `0x026145EF` | `xml/vip_reward.xml` |
| `0x025B3A0D` | `xml/warlord_phase_rank_reward.xml` |
| `0x025FA932` | `xml/warlord_phase_reward.xml` |
| `0x02578962` | `xml/warlord_rank_reward_single.xml` |
| `0x0261AB66` | `xml/warlord_rank_reward_total.xml` |
| `0x025F4330` | `xml/weekly_pass_reward.xml` |
| `0x0262DCA7` | `xml/wheel_of_gift.xml` |
| `0x025B3A2F` | `xml/wheel_of_gift_cycle.xml` |
| `0x026074A0` | `xml/world_champion_event_l_reward.xml` |
| `0x0257FA1D` | `xml/world_champion_event_s_reward.xml` |
| `0x025FA965` | `xml/world_champion_event_t_reward.xml` |
| `0x02578989` | `xml/yahtzee_game_reward.xml` |

### Localization (1 files)

| Offset | Filename |
|---|---|
| `0x025C34E4` | `xml/TextureAlias.xml` |

### Maps (26 files)

| Offset | Filename |
|---|---|
| `0x0259F815` | `xml/adventure_coordinate.xml` |
| `0x025B3747` | `xml/bloody_war_event_map.xml` |
| `0x025B9A95` | `xml/elemental_war_event_map.xml` |
| `0x025AD629` | `xml/elemental_war_warzone.xml` |
| `0x026272C7` | `xml/giant_invasion_monster.xml` |
| `0x025D3C69` | `xml/kingdom_strategy.xml` |
| `0x025B9B7C` | `xml/loop_boss_monster.xml` |
| `0x02600997` | `xml/lost_dominion_terrain.xml` |
| `0x025AD789` | `xml/map_block.xml` |
| `0x0258CC8E` | `xml/map_chat_channel.xml` |
| `0x025C050E` | `xml/map_hide_block.xml` |
| `0x02617879` | `xml/monster.xml` |
| `0x0260D3EE` | `xml/novice_map_march.xml` |
| `0x02578864` | `xml/novice_map_monster.xml` |
| `0x02571C7A` | `xml/novice_map_scene.xml` |
| `0x025DA707` | `xml/novice_world_trend.xml` |
| `0x025CD307` | `xml/secrectmonster.xml` |
| `0x0261E394` | `xml/storymap.xml` |
| `0x025B3A56` | `xml/world_champion_event.xml` |
| `0x02571DA5` | `xml/world_champion_event_force.xml` |
| `0x02565588` | `xml/world_champion_event_rule.xml` |
| `0x025D3E89` | `xml/world_champion_event_score.xml` |
| `0x0261ABB4` | `xml/world_champion_p_title.xml` |
| `0x025FA98B` | `xml/world_champion_power.xml` |
| `0x0258CD99` | `xml/world_champion_s_title.xml` |
| `0x02620F9F` | `xml/world_champion_title.xml` |

### Other (203 files)

| Offset | Filename |
|---|---|
| `0x025F7583` | `.xml` |
| `0x025A9DDF` | `_diff.xml` |
| `0x026113AC` | `PlayerDefault%lld.xml` |
| `0x025F141A` | `PlayerDefault.xml` |
| `0x026274EB` | `Simulator/xml/soultest.xml` |
| `0x025F4F02` | `UserDefault.xml` |
| `0x0262D84F` | `xml/achievement.xml` |
| `0x026070E4` | `xml/active_freepick.xml` |
| `0x0257858F` | `xml/active_freepick_set.xml` |
| `0x025FA5FC` | `xml/active_recharge_bonus.xml` |
| `0x025C0185` | `xml/activity_chess.xml` |
| `0x025785C2` | `xml/activity_chess_boss.xml` |
| `0x025D3A47` | `xml/activity_chess_buff.xml` |
| `0x025C01A9` | `xml/activity_chess_land_colour.xml` |
| `0x0260075A` | `xml/activity_chess_land_position.xml` |
| `0x025DA3AF` | `xml/activity_chess_mark.xml` |
| `0x025E0A39` | `xml/activity_chess_npc.xml` |
| `0x026070FC` | `xml/activity_chess_point.xml` |
| `0x0256511D` | `xml/activity_Collections.xml` |
| `0x0260D0A3` | `xml/activity_source.xml` |
| `0x025DA3E5` | `xml/activity_source_buy.xml` |
| `0x02620B19` | `xml/activity_switch.xml` |
| `0x02586161` | `xml/activity_target_type.xml` |
| `0x0259F7DA` | `xml/activity_time.xml` |
| `0x026142AB` | `xml/ad_id.xml` |
| `0x0262D8C3` | `xml/ad_pop.xml` |
| `0x0258617E` | `xml/adventure_base.xml` |
| `0x0261A740` | `xml/all_for_one.xml` |
| `0x0257F642` | `xml/anniversary_donate.xml` |
| `0x02607187` | `xml/auto_hangup.xml` |
| `0x0262D93A` | `xml/black_current_coming.xml` |
| `0x025994A2` | `xml/boss_art.xml` |
| `0x025E75F4` | `xml/boss_base.xml` |
| `0x02571A97` | `xml/boss_lv.xml` |
| `0x025C0252` | `xml/byzantine.xml` |
| `0x025B377C` | `xml/camel.xml` |
| `0x025FA67D` | `xml/championship_base.xml` |
| `0x0260D15A` | `xml/championship_lv.xml` |
| `0x02565260` | `xml/civilization.xml` |
| `0x02600824` | `xml/clear_pet.xml` |
| `0x02600836` | `xml/clear_solder.xml` |
| `0x0262D9D4` | `xml/collect_energy.xml` |
| `0x025E762D` | `xml/Combo.xml` |
| `0x0261A7ED` | `xml/consumption.xml` |
| `0x025E763B` | `xml/crest_prestige_attributes.xml` |
| `0x025C02BE` | `xml/crest_prestige_base.xml` |
| `0x025DA4FA` | `xml/crest_prestige_evolution.xml` |
| `0x025932F6` | `xml/crest_prestige_group.xml` |
| `0x02586269` | `xml/desert_trade.xml` |
| `0x025B9A5B` | `xml/desert_trade_truck.xml` |
| `0x025B37EB` | `xml/dessert_make.xml` |
| `0x0257870B` | `xml/dessert_make_refresh.xml` |
| `0x025AD5AF` | `xml/dessert_make_skin.xml` |
| `0x025E76A1` | `xml/dessert_make_taste.xml` |
| `0x025EDF7E` | `xml/dinar_back.xml` |
| `0x025FD7AD` | `xml/dominion.xml` |
| `0x0256E6FF` | `xml/dominion_profit_configure.xml` |
| `0x02607271` | `xml/download.xml` |
| `0x025E76CC` | `xml/era.xml` |
| `0x025652AA` | `xml/era_global.xml` |
| `0x025D3BAF` | `xml/friend_invited_basic.xml` |
| `0x025FA6F3` | `xml/friend_invited_token.xml` |
| `0x025C6AFB` | `xml/full_recharge.xml` |
| `0x025933A2` | `xml/giant_invasion.xml` |
| `0x025E0C3E` | `xml/Gif.xml` |
| `0x025CD0A7` | `xml/goodluck_base.xml` |
| `0x0258CBB1` | `xml/goodluck_group.xml` |
| `0x02599554` | `xml/greedygame_group.xml` |
| `0x02571B42` | `xml/happy_marbles.xml` |
| `0x025B9AFA` | `xml/happy_marbles_prob.xml` |
| `0x025F4068` | `xml/happy_marbles_track.xml` |
| `0x02607309` | `xml/Illegality_new.xml` |
| `0x025C6B79` | `xml/Illegality_new_exact.xml` |
| `0x025BD0DB` | `xml/image_path.xml` |
| `0x02620CEA` | `xml/imperial_base.xml` |
| `0x025995E8` | `xml/invasion.xml` |
| `0x025A6940` | `xml/invasion_time.xml` |
| `0x0262DAC6` | `xml/kvk_point.xml` |
| `0x02627347` | `xml/latch_behavior.xml` |
| `0x0261A922` | `xml/latch_collide.xml` |
| `0x02600926` | `xml/latch_condition.xml` |
| `0x02599615` | `xml/latch_fall_collide.xml` |
| `0x025CD16F` | `xml/latch_level.xml` |
| `0x0260D316` | `xml/latch_object_state.xml` |
| `0x025E77AE` | `xml/latch_objects.xml` |
| `0x025F40F7` | `xml/latch_physics.xml` |
| `0x025653B4` | `xml/loadingimage.xml` |
| `0x025FA7D1` | `xml/loop_boss_base.xml` |
| `0x0257F7CE` | `xml/loop_boss_target_type.xml` |
| `0x02620D58` | `xml/Lord_Att_Filter.xml` |
| `0x02578828` | `xml/lord_catch.xml` |
| `0x025CD1DC` | `xml/lord_Dressup.xml` |
| `0x0260D35F` | `xml/lord_grow_lv.xml` |
| `0x0259FA4E` | `xml/lord_grow_type.xml` |
| `0x025E0CE5` | `xml/lord_level_grow.xml` |
| `0x025B9BB4` | `xml/lord_parts.xml` |
| `0x025FA7F0` | `xml/lost_achievement.xml` |
| `0x025C045F` | `xml/lost_activity_switch.xml` |
| `0x0259FA78` | `xml/lost_area.xml` |
| `0x0258642A` | `xml/lost_camp.xml` |
| `0x025FA809` | `xml/lost_crystal_gen.xml` |
| `0x025BCF89` | `xml/lost_dominion.xml` |
| `0x02614471` | `xml/lost_dominion_npc.xml` |
| `0x0260097B` | `xml/lost_dominion_state.xml` |
| `0x0261A999` | `xml/lost_global.xml` |
| `0x0256541A` | `xml/lost_imperial_base.xml` |
| `0x025EE04A` | `xml/lost_month_card.xml` |
| `0x02578846` | `xml/lost_refresh.xml` |
| `0x0258CC61` | `xml/lucky_line.xml` |
| `0x025B3937` | `xml/luckypot.xml` |
| `0x025C04ED` | `xml/luckypot_lattice.xml` |
| `0x025AD7A5` | `xml/medal_system.xml` |
| `0x0256B6A7` | `xml/merge_base.xml` |
| `0x0257F890` | `xml/merge_new.xml` |
| `0x025D3D27` | `xml/merge_ps.xml` |
| `0x025D3D38` | `xml/merge_scroe.xml` |
| `0x0262DB32` | `xml/mini_game_sheep.xml` |
| `0x025E0D55` | `xml/move_server_time.xml` |
| `0x0261A9D2` | `xml/name_random.xml` |
| `0x02600A04` | `xml/nameplate_skin.xml` |
| `0x0262740D` | `xml/navigation.xml` |
| `0x0256545D` | `xml/navigation_base.xml` |
| `0x025A6A72` | `xml/navigation_lv.xml` |
| `0x0261451C` | `xml/news.xml` |
| `0x025C0525` | `xml/noble_lv.xml` |
| `0x0262DB4E` | `xml/noble_state.xml` |
| `0x0259FB01` | `xml/npc_ask.xml` |
| `0x025EE0B6` | `xml/npc_dia.xml` |
| `0x026073A8` | `xml/online.xml` |
| `0x02600A56` | `xml/open_sesame.xml` |
| `0x0257F8BC` | `xml/open_sesame_buff.xml` |
| `0x025FA862` | `xml/open_sesame_buff_client.xml` |
| `0x025864DD` | `xml/open_sesame_enemy.xml` |
| `0x0261A9F4` | `xml/open_sesame_layer.xml` |
| `0x0262DB62` | `xml/open_sesame_npc.xml` |
| `0x025AD7C0` | `xml/open_sesame_random_enemy.xml` |
| `0x0259FB11` | `xml/open_sesame_random_npc.xml` |
| `0x02600A79` | `xml/operation_mark.xml` |
| `0x02600A90` | `xml/operation_point.xml` |
| `0x025D3D52` | `xml/other_activity.xml` |
| `0x0259342F` | `xml/pet_base.xml` |
| `0x0258CCD6` | `xml/pet_feed_gold.xml` |
| `0x025DA73E` | `xml/pet_library.xml` |
| `0x0262DBB2` | `xml/pet_lv.xml` |
| `0x02600AA8` | `xml/pet_shoot_base.xml` |
| `0x025B9C8A` | `xml/pet_source.xml` |
| `0x0259972D` | `xml/PinBallRecord.xml` |
| `0x0257F8FF` | `xml/placement.xml` |
| `0x025AD7FE` | `xml/play_preview.xml` |
| `0x0260D433` | `xml/player_limit.xml` |
| `0x0257C760` | `xml/plist.xml` |
| `0x0261AA2C` | `xml/plots.xml` |
| `0x025DA778` | `xml/Point_base.xml` |
| `0x025D3D7C` | `xml/points_bidding.xml` |
| `0x025AD81D` | `xml/power_up.xml` |
| `0x025B39B2` | `xml/power_up_part.xml` |
| `0x0261456C` | `xml/PrevImage.xml` |
| `0x0261AA3A` | `xml/product_showcase_login.xml` |
| `0x025F4221` | `xml/pve.xml` |
| `0x0258CCF3` | `xml/pve_power_up.xml` |
| `0x025EE0F3` | `xml/rebels.xml` |
| `0x025A6AFE` | `xml/recharge_point.xml` |
| `0x02620E55` | `xml/record_cost_group_base.xml` |
| `0x02620E74` | `xml/record_cost_group_config.xml` |
| `0x0258CD13` | `xml/red_envelopes_auto.xml` |
| `0x025A6B2D` | `xml/red_envelopes_limit.xml` |
| `0x02620E95` | `xml/red_envelopes_merge.xml` |
| `0x02599763` | `xml/red_envelopes_personal.xml` |
| `0x025F422D` | `xml/red_envelopes_weekactivity.xml` |
| `0x02600B42` | `xml/reduce_price_base.xml` |
| `0x0259979F` | `xml/retrieve_base.xml` |
| `0x025C0586` | `xml/second_key.xml` |
| `0x0262DC41` | `xml/Secret_base.xml` |
| `0x025EE121` | `xml/secret_boss.xml` |
| `0x025E0DF9` | `xml/secret_level.xml` |
| `0x02571D0C` | `xml/server_merge_res.xml` |
| `0x0257891A` | `xml/server_merge_time.xml` |
| `0x0256B73A` | `xml/server_version.xml` |
| `0x025E0E1B` | `xml/server_whitelist.xml` |
| `0x025CD33A` | `xml/sign_in_fund_base.xml` |
| `0x025E0E34` | `xml/sign_in_fund_config.xml` |
| `0x025D3E16` | `xml/solomon.xml` |
| `0x02571D4A` | `xml/solomon_position.xml` |
| `0x025E78E4` | `xml/solomon_random.xml` |
| `0x02604096` | `xml/soul_cost.xml` |
| `0x0261AAE3` | `xml/SoulSmelting.xml` |
| `0x025D3E42` | `xml/special_global.xml` |
| `0x025F42DD` | `xml/special_login.xml` |
| `0x0261AAF8` | `xml/surprise.xml` |
| `0x025C05D9` | `xml/threedays_base.xml` |
| `0x02571D6C` | `xml/tradeprices.xml` |
| `0x02620F3F` | `xml/trading.xml` |
| `0x025C6D49` | `xml/tribute.xml` |
| `0x025EE16D` | `xml/unlock_lv.xml` |
| `0x02600BF1` | `xml/week_activity_type.xml` |
| `0x02620F72` | `xml/week_card.xml` |
| `0x025C6D64` | `xml/weekly_base.xml` |
| `0x0261AB88` | `xml/weekly_calendar.xml` |
| `0x0261ABA0` | `xml/weekly_pass.xml` |
| `0x025E0E8E` | `xml/weekly_pass_get.xml` |
| `0x025B9D81` | `xml/weekly_pass_lv.xml` |
| `0x02593519` | `xml/yahtzee_game.xml` |
| `0x0259FC29` | `xml/yahtzee_game_point.xml` |

### Pvp (18 files)

| Offset | Filename |
|---|---|
| `0x0262D8EA` | `xml/arena.xml` |
| `0x025861CD` | `xml/arena_robot.xml` |
| `0x0259F845` | `xml/arena_robot_name.xml` |
| `0x02620C4B` | `xml/fixed_accumulation_rank.xml` |
| `0x02586300` | `xml/fixed_team_rank.xml` |
| `0x02599604` | `xml/kvk_rank.xml` |
| `0x025B6C0C` | `xml/league.xml` |
| `0x0260D341` | `xml/league_exchange.xml` |
| `0x025A69FF` | `xml/league_medal_system.xml` |
| `0x025F4136` | `xml/league_recharge.xml` |
| `0x025B38D3` | `xml/league_recommend.xml` |
| `0x025D3CAF` | `xml/league_short_name.xml` |
| `0x026009EB` | `xml/match_rules.xml` |
| `0x025FA845` | `xml/merge_rank.xml` |
| `0x025E0D8E` | `xml/operation_rank.xml` |
| `0x0261454D` | `xml/pet_shoot_rank.xml` |
| `0x0257F949` | `xml/rank_worship.xml` |
| `0x02586592` | `xml/yahtzee_game_rank.xml` |

### Quests (63 files)

| Offset | Filename |
|---|---|
| `0x026271FB` | `xml/activity_rush_event.xml` |
| `0x025A67B2` | `xml/ad_event.xml` |
| `0x0258CA43` | `xml/adventure_chapter.xml` |
| `0x02571A01` | `xml/af_event_pack.xml` |
| `0x025AD4B6` | `xml/bloody_war_event.xml` |
| `0x025E75D5` | `xml/bloody_war_event_score.xml` |
| `0x0261A797` | `xml/bloody_war_event_season_skin.xml` |
| `0x025786AE` | `xml/championship_task.xml` |
| `0x025AD566` | `xml/daily_recharge.xml` |
| `0x025AD57D` | `xml/daily_tasks.xml` |
| `0x0260D1FF` | `xml/elemental_war_event.xml` |
| `0x02620C13` | `xml/elemental_war_event_buff.xml` |
| `0x0258CB6A` | `xml/elemental_war_event_score.xml` |
| `0x02571AFF` | `xml/era_task.xml` |
| `0x025652BD` | `xml/era_task_unlock.xml` |
| `0x0261A83B` | `xml/event_pack.xml` |
| `0x02599523` | `xml/financial_expert_task.xml` |
| `0x0259F947` | `xml/friend_invited_task.xml` |
| `0x0257877E` | `xml/guild_standoff_task.xml` |
| `0x025F40BE` | `xml/imperial_task.xml` |
| `0x02565347` | `xml/kvk_event.xml` |
| `0x0260D2FB` | `xml/latch_event.xml` |
| `0x025C03FA` | `xml/league_event.xml` |
| `0x02599641` | `xml/league_event_task.xml` |
| `0x025FA7BD` | `xml/league_task.xml` |
| `0x025A6A3F` | `xml/lord_war_event.xml` |
| `0x025653DB` | `xml/lord_war_event_buff.xml` |
| `0x025C6C1A` | `xml/lord_war_event_score.xml` |
| `0x025E7803` | `xml/lost_daily_base.xml` |
| `0x0258643C` | `xml/lost_daily_task.xml` |
| `0x025B9BD3` | `xml/lost_era_task.xml` |
| `0x025DA656` | `xml/lost_era_task_unlock.xml` |
| `0x0261448B` | `xml/lost_event_desc.xml` |
| `0x025B9BE9` | `xml/lost_event_pre_phase2.xml` |
| `0x0259FA96` | `xml/lost_event_pre_phase3.xml` |
| `0x026009B5` | `xml/lost_event_score.xml` |
| `0x0262DAF7` | `xml/lost_imperial_task.xml` |
| `0x025E785C` | `xml/lost_rush_event.xml` |
| `0x0257F83E` | `xml/lost_rush_event_rank.xml` |
| `0x026144BF` | `xml/lost_rush_event_score.xml` |
| `0x0257F87C` | `xml/merge_event.xml` |
| `0x02600A1B` | `xml/navigation_event_task.xml` |
| `0x025A6AA2` | `xml/open_sesame_event.xml` |
| `0x0256549A` | `xml/open_sesame_random_event.xml` |
| `0x025EE0CC` | `xml/plot_quest_correspond.xml` |
| `0x0259FB45` | `xml/plot_quest_new.xml` |
| `0x0257F91D` | `xml/power_tasks.xml` |
| `0x026073F9` | `xml/product_showcase_event.xml` |
| `0x025B9CCC` | `xml/Quantity_task.xml` |
| `0x02607438` | `xml/return_event.xml` |
| `0x025DA7D4` | `xml/return_event_base.xml` |
| `0x02627480` | `xml/return_event_pack.xml` |
| `0x025788DE` | `xml/return_event_pay.xml` |
| `0x025F4264` | `xml/return_event_pay_group.xml` |
| `0x025A6B4F` | `xml/return_event_sign_in.xml` |
| `0x02565502` | `xml/rush_event.xml` |
| `0x0258CD46` | `xml/rush_event_score.xml` |
| `0x0256B726` | `xml/Secret_task.xml` |
| `0x0262DC63` | `xml/special_event.xml` |
| `0x025D3E26` | `xml/special_event_limit.xml` |
| `0x025838C6` | `xml/task_guide.xml` |
| `0x0261AB09` | `xml/task_setting.xml` |
| `0x0257894C` | `xml/warlord_event.xml` |

### Research (2 files)

| Offset | Filename |
|---|---|
| `0x025C6A6B` | `xml/clear_league_science.xml` |
| `0x025C6A88` | `xml/clear_science.xml` |

### Shop (21 files)

| Offset | Filename |
|---|---|
| `0x02578696` | `xml/camel_shop_show.xml` |
| `0x02565243` | `xml/championship_package.xml` |
| `0x025E76E4` | `xml/financial_expert_pack.xml` |
| `0x025E770B` | `xml/general_shop.xml` |
| `0x025F40AA` | `xml/huawei_pack.xml` |
| `0x025FA742` | `xml/imperial_shop.xml` |
| `0x025A6A1B` | `xml/limit_shop_base.xml` |
| `0x0257F7B4` | `xml/limit_shop_config.xml` |
| `0x025F41A7` | `xml/lucky_shop.xml` |
| `0x025C04D5` | `xml/lucky_shop_base.xml` |
| `0x025F41C6` | `xml/lucky_shop_new.xml` |
| `0x02620DF4` | `xml/luna_shop.xml` |
| `0x0258648F` | `xml/luna_shop_config.xml` |
| `0x025EE08B` | `xml/noble_shop.xml` |
| `0x025DA6EA` | `xml/novice_free_purchase.xml` |
| `0x025D3D69` | `xml/Point_shop.xml` |
| `0x0259346E` | `xml/reduce_price_shop.xml` |
| `0x02565515` | `xml/shop_buy_one.xml` |
| `0x0257F99E` | `xml/shop_gold.xml` |
| `0x0261AAAE` | `xml/sign_package.xml` |
| `0x025F42F3` | `xml/super4choose1_pack.xml` |

### Troops (17 files)

| Offset | Filename |
|---|---|
| `0x02614279` | `xml/activity_knight.xml` |
| `0x0257F5F2` | `xml/activity_knight_mark.xml` |
| `0x025B99B2` | `xml/activity_knight_monster.xml` |
| `0x0256B3B7` | `xml/activity_knight_monster_name.xml` |
| `0x0257861D` | `xml/army_loss.xml` |
| `0x025B3723` | `xml/army_skin.xml` |
| `0x025AD6B0` | `xml/knight_glory.xml` |
| `0x025A6989` | `xml/knight_glory_monster.xml` |
| `0x025C6D1D` | `xml/soldierAct.xml` |
| `0x0259FBBC` | `xml/soldiers_effect.xml` |
| `0x02565538` | `xml/soldiers_hero_talent.xml` |
| `0x026274B3` | `xml/soldiers_random_group.xml` |
| `0x02620EEF` | `xml/soldiers_recruit.xml` |
| `0x025A6BAA` | `xml/soldiers_talent_type.xml` |
| `0x02586552` | `xml/soldiers_up.xml` |
| `0x026145C7` | `xml/soldiers_up_global.xml` |
| `0x02600B8E` | `xml/soldiers_up_type.xml` |

### Ui (5 files)

| Offset | Filename |
|---|---|
| `0x025651DB` | `xml/anniversary_donate_dialogue.xml` |
| `0x02614588` | `xml/ruins_search_base.xml` |
| `0x0259FB69` | `xml/ruins_search_group.xml` |
| `0x025B73F9` | `xml/tutorial.xml` |
| `0x0256F115` | `xml/tutorial_2.xml` |

### Vip (2 files)

| Offset | Filename |
|---|---|
| `0x025CD024` | `xml/clear_vip.xml` |
| `0x02627428` | `xml/privilege.xml` |

---
## 2. URLs and Server Endpoints

### URLs

| Offset | URL |
|---|---|
| `0x025B5F39` | `http://` |
| `0x0256DDA5` | `http://%s` |
| `0x025833E2` | `http://snd-storage30.igg.com/push.php` |
| `0x02589C40` | `http://static-cq.igg.com` |
| `0x02569DD7` | `http://static-cq.igg.com/H5Games/web/index.html` |
| `0x02624569` | `https://graph.facebook.com/v5.0/me/apprequests?limit=%d&access_token=%s` |
| `0x025B7154` | `https://graph.facebook.com/v5.0/me/invitable_friends?limit=%d&access_token=%s` |

### IP Addresses

| Offset | String |
|---|---|
| `0x0257219B` | `127.0.0.1` |
| `0x025C7392` | `127.0.0.1/` |
| `0x0262E88E` | `2.1.0.0` |
| `0x025A938B` | `2.16.840.1.101.3.4.3.17` |
| `0x025A2B35` | `2.16.840.1.101.3.4.3.18` |
| `0x025CFE73` | `2.16.840.1.101.3.4.3.19` |
| `0x02561C8C` | `3.7.14.1` |
| `0x02609F0A` | `52.80.53.87` |
| `0x026037B8` | `AES-128-CBC:AES128:2.16.840.1.101.3.4.1.2` |
| `0x025DD041` | `AES-128-CCM:id-aes128-CCM:2.16.840.1.101.3.4.1.7` |
| `0x0261D224` | `AES-128-CFB:2.16.840.1.101.3.4.1.4` |
| `0x025A9358` | `AES-128-ECB:2.16.840.1.101.3.4.1.1` |
| `0x02567CD2` | `AES-128-GCM:id-aes128-GCM:2.16.840.1.101.3.4.1.6` |
| `0x02629BA2` | `AES-128-OFB:2.16.840.1.101.3.4.1.3` |
| `0x025E3849` | `AES-128-WRAP-PAD:id-aes128-wrap-pad:AES128-WRAP-PAD:2.16.840.1.101.3.4.1.8` |
| `0x025D68A5` | `AES-128-WRAP:id-aes128-wrap:AES128-WRAP:2.16.840.1.101.3.4.1.5` |
| `0x02574CE8` | `AES-128-XTS:1.3.111.2.1619.0.1.1` |
| `0x025FCF6B` | `AES-192-CBC:AES192:2.16.840.1.101.3.4.1.22` |
| `0x0257BCA7` | `AES-192-CCM:id-aes192-CCM:2.16.840.1.101.3.4.1.27` |
| `0x025A2A6F` | `AES-192-CFB:2.16.840.1.101.3.4.1.24` |
| `0x025F6BE4` | `AES-192-ECB:2.16.840.1.101.3.4.1.21` |
| `0x025A2A93` | `AES-192-GCM:id-aes192-GCM:2.16.840.1.101.3.4.1.26` |
| `0x02629B7E` | `AES-192-OFB:2.16.840.1.101.3.4.1.23` |
| `0x025A2AC5` | `AES-192-WRAP-PAD:id-aes192-wrap-pad:AES192-WRAP-PAD:2.16.840.1.101.3.4.1.28` |
| `0x0258F4B4` | `AES-192-WRAP:id-aes192-wrap:AES192-WRAP:2.16.840.1.101.3.4.1.25` |
| `0x025F6C08` | `AES-256-CBC:AES256:2.16.840.1.101.3.4.1.42` |
| `0x02616D21` | `AES-256-CCM:id-aes256-CCM:2.16.840.1.101.3.4.1.47` |
| `0x025A2A4B` | `AES-256-CFB:2.16.840.1.101.3.4.1.44` |
| `0x025B607D` | `AES-256-ECB:2.16.840.1.101.3.4.1.41` |
| `0x025F6C33` | `AES-256-GCM:id-aes256-GCM:2.16.840.1.101.3.4.1.46` |
| `0x025BC77B` | `AES-256-OFB:2.16.840.1.101.3.4.1.43` |
| `0x02595782` | `AES-256-WRAP-PAD:id-aes256-wrap-pad:AES256-WRAP-PAD:2.16.840.1.101.3.4.1.48` |
| `0x02574D09` | `AES-256-WRAP:id-aes256-wrap:AES256-WRAP:2.16.840.1.101.3.4.1.45` |
| `0x0259BE18` | `AES-256-XTS:1.3.111.2.1619.0.1.2` |
| `0x025D688C` | `AES:2.16.840.1.101.3.4.1` |
| `0x025D681F` | `BLAKE2B-512:BLAKE2b512:1.3.6.1.4.1.1722.12.2.1.16` |
| `0x02574B5D` | `BLAKE2BMAC:1.3.6.1.4.1.1722.12.2.1` |
| `0x025A28D6` | `BLAKE2S-256:BLAKE2s256:1.3.6.1.4.1.1722.12.2.2.8` |
| `0x025A2907` | `BLAKE2SMAC:1.3.6.1.4.1.1722.12.2.2` |
| `0x025BC7F2` | `CAMELLIA-128-CBC:CAMELLIA128:1.2.392.200011.61.1.1.1.2` |
| `0x02603804` | `CAMELLIA-128-CFB:0.3.4401.5.3.1.9.4` |
| `0x0259BE39` | `CAMELLIA-128-CTR:0.3.4401.5.3.1.9.9` |
| `0x0261D26C` | `CAMELLIA-128-ECB:0.3.4401.5.3.1.9.1` |
| `0x025A2B11` | `CAMELLIA-128-OFB:0.3.4401.5.3.1.9.3` |
| `0x02588DE3` | `CAMELLIA-192-CBC:CAMELLIA192:1.2.392.200011.61.1.1.1.3` |
| `0x025CFE4E` | `CAMELLIA-192-CFB:0.3.4401.5.3.1.9.24` |
| `0x0258F52B` | `CAMELLIA-192-CTR:0.3.4401.5.3.1.9.29` |
| `0x026097EF` | `CAMELLIA-192-ECB:0.3.4401.5.3.1.9.21` |
| `0x025CFE29` | `CAMELLIA-192-OFB:0.3.4401.5.3.1.9.23` |
| `0x025E9F86` | `CAMELLIA-256-CBC:CAMELLIA256:1.2.392.200011.61.1.1.1.4` |
| `0x025C964A` | `CAMELLIA-256-CFB:0.3.4401.5.3.1.9.44` |
| `0x0261D290` | `CAMELLIA-256-CTR:0.3.4401.5.3.1.9.49` |
| `0x0261D247` | `CAMELLIA-256-ECB:0.3.4401.5.3.1.9.41` |
| `0x02609814` | `CAMELLIA-256-OFB:0.3.4401.5.3.1.9.43` |
| `0x025FCFD0` | `DES-EDE-ECB:DES-EDE:1.3.14.3.2.17` |
| `0x02588E1A` | `DES3-WRAP:id-smime-alg-CMS3DESwrap:1.2.840.113549.1.9.16.3.6` |
| `0x025C951D` | `DSA-SHA2-224:DSA-SHA224:dsa_with_SHA224:2.16.840.1.101.3.4.3.1` |
| `0x025FCDF2` | `DSA-SHA2-256:DSA-SHA256:dsa_with_SHA256:2.16.840.1.101.3.4.3.2` |
| `0x02574BD3` | `DSA-SHA2-384:DSA-SHA384:dsa_with_SHA384:id-dsa-with-sha384:1.2.840.1.101.3.4.3.3` |
| `0x025AFB3F` | `DSA-SHA2-512:DSA-SHA512:dsa_with_SHA512:id-dsa-with-sha512:1.2.840.1.101.3.4.3.4` |
| `0x02588D5C` | `DSA-SHA3-224:dsa_with_SHA3-224:id-dsa-with-sha3-224:2.16.840.1.101.3.4.3.5` |
| `0x02574C24` | `DSA-SHA3-256:dsa_with_SHA3-256:id-dsa-with-sha3-256:2.16.840.1.101.3.4.3.6` |
| `0x0258F355` | `DSA-SHA3-384:dsa_with_SHA3-384:id-dsa-with-sha3-384:2.16.840.1.101.3.4.3.7` |
| `0x025E9E2D` | `DSA-SHA3-512:dsa_with_SHA3-512:id-dsa-with-sha3-512:2.16.840.1.101.3.4.3.8` |
| `0x0262361F` | `ECDSA-SHA3-224:ecdsa_with_SHA3-224:id-ecdsa-with-sha3-224:2.16.840.1.101.3.4.3.9` |
| `0x0257BB64` | `ECDSA-SHA3-256:ecdsa_with_SHA3-256:id-ecdsa-with-sha3-256:2.16.840.1.101.3.4.3.10` |
| `0x02610485` | `ECDSA-SHA3-384:ecdsa_with_SHA3-384:id-ecdsa-with-sha3-384:2.16.840.1.101.3.4.3.11` |
| `0x025E9E78` | `ECDSA-SHA3-512:ecdsa_with_SHA3-512:id-ecdsa-with-sha3-512:2.16.840.1.101.3.4.3.12` |
| `0x025FCD92` | `ED25519:1.3.101.112` |
| `0x0260366D` | `ED448:1.3.101.113` |
| `0x025BC646` | `KMAC-128:KMAC128:2.16.840.1.101.3.4.2.19` |
| `0x02588CA1` | `KMAC-256:KMAC256:2.16.840.1.101.3.4.2.20` |
| `0x025F05D8` | `ML-DSA-44:MLDSA44:2.16.840.1.101.3.4.3.17:id-ml-dsa-44` |
| `0x0260367F` | `ML-DSA-65:MLDSA65:2.16.840.1.101.3.4.3.18:id-ml-dsa-65` |
| `0x025CFCA3` | `ML-DSA-87:MLDSA87:2.16.840.1.101.3.4.3.19:id-ml-dsa-87` |
| `0x0257BADE` | `ML-KEM-1024:MLKEM1024:id-alg-ml-kem-1024:2.16.840.1.101.3.4.4.3` |
| `0x025BC6A8` | `ML-KEM-512:MLKEM512:id-alg-ml-kem-512:2.16.840.1.101.3.4.4.1` |
| `0x02588CCA` | `ML-KEM-768:MLKEM768:id-alg-ml-kem-768:2.16.840.1.101.3.4.4.2` |
| `0x02567C10` | `RIPEMD-160:RIPEMD160:RIPEMD:RMD160:1.3.36.3.2.1` |
| `0x025A92F5` | `RSA-RIPEMD160:ripemd160WithRSA:1.3.36.3.3.1.2` |
| `0x025C955C` | `RSA-SHA3-224:id-rsassa-pkcs1-v1_5-with-sha3-224:2.16.840.1.101.3.4.3.13` |
| `0x02631EBF` | `RSA-SHA3-256:id-rsassa-pkcs1-v1_5-with-sha3-256:2.16.840.1.101.3.4.3.14` |
| `0x025AFBD6` | `RSA-SHA3-384:id-rsassa-pkcs1-v1_5-with-sha3-384:2.16.840.1.101.3.4.3.15` |
| `0x0259BD9B` | `RSA-SHA3-512:id-rsassa-pkcs1-v1_5-with-sha3-512:2.16.840.1.101.3.4.3.16` |
| `0x02603633` | `SCRYPT:id-scrypt:1.3.6.1.4.1.11591.4.11` |
| `0x025E9D88` | `SHA1:SHA-1:SSL3-SHA1:1.3.14.3.2.26` |
| `0x02588C5C` | `SHA2-224:SHA-224:SHA224:2.16.840.1.101.3.4.2.4` |
| `0x025A287C` | `SHA2-256:SHA-256:SHA256:2.16.840.1.101.3.4.2.1` |
| `0x025F6B59` | `SHA2-384:SHA-384:SHA384:2.16.840.1.101.3.4.2.2` |
| `0x025DCF74` | `SHA2-512/224:SHA-512/224:SHA512-224:2.16.840.1.101.3.4.2.5` |
| `0x026235BB` | `SHA2-512/256:SHA-512/256:SHA512-256:2.16.840.1.101.3.4.2.6` |
| `0x0261D025` | `SHA2-512:SHA-512:SHA512:2.16.840.1.101.3.4.2.3` |
| `0x0259BD38` | `SHA3-224:2.16.840.1.101.3.4.2.7` |
| `0x025DCFAF` | `SHA3-256:2.16.840.1.101.3.4.2.8` |
| `0x02631E54` | `SHA3-384:2.16.840.1.101.3.4.2.9` |
| `0x026103F1` | `SHA3-512:2.16.840.1.101.3.4.2.10` |
| `0x025A28AB` | `SHAKE-128:SHAKE128:2.16.840.1.101.3.4.2.11` |
| `0x0258F285` | `SHAKE-256:SHAKE256:2.16.840.1.101.3.4.2.12` |
| `0x025E9DEE` | `SLH-DSA-SHA2-128f:id-slh-dsa-sha2-128f:2.16.840.1.101.3.4.3.21` |
| `0x025C2D02` | `SLH-DSA-SHA2-128s:id-slh-dsa-sha2-128s:2.16.840.1.101.3.4.3.20` |
| `0x0256DE67` | `SLH-DSA-SHA2-192f:id-slh-dsa-sha2-192f:2.16.840.1.101.3.4.3.23` |
| `0x025A2957` | `SLH-DSA-SHA2-192s:id-slh-dsa-sha2-192s:2.16.840.1.101.3.4.3.22` |
| `0x025822CE` | `SLH-DSA-SHA2-256f:id-slh-dsa-sha2-256f:2.16.840.1.101.3.4.3.25` |
| `0x025BC6F8` | `SLH-DSA-SHA2-256s:id-slh-dsa-sha2-256s:2.16.840.1.101.3.4.3.24` |
| `0x0258F314` | `SLH-DSA-SHAKE-128f:id-slh-dsa-shake-128f:2.16.840.1.101.3.4.3.27` |
| `0x025C94DC` | `SLH-DSA-SHAKE-128s:id-slh-dsa-shake-128s:2.16.840.1.101.3.4.3.26` |
| `0x0258230D` | `SLH-DSA-SHAKE-192f:id-slh-dsa-shake-192f:2.16.840.1.101.3.4.3.29` |
| `0x02610444` | `SLH-DSA-SHAKE-192s:id-slh-dsa-shake-192s:2.16.840.1.101.3.4.3.28` |
| `0x025A92B4` | `SLH-DSA-SHAKE-256f:id-slh-dsa-shake-256f:2.16.840.1.101.3.4.3.31` |
| `0x02616C13` | `SLH-DSA-SHAKE-256s:id-slh-dsa-shake-256s:2.16.840.1.101.3.4.3.30` |
| `0x0257BAA9` | `X25519:1.3.101.110` |
| `0x02616C02` | `X448:1.3.101.111` |

### API Paths

*None found*

### CDN / Asset Paths

| Offset | Path |
|---|---|
| `0x025CDD39` | `... FileUtilsAndroid::assetmanager is nullptr` |
| `0x025A9BA8` | `Resuming from previous unfinished update, %d files remains to be finished.` |
| `0x025EA8C2` | `Start to update %d files from remote package.` |
| `0x0260EDD4` | `TLSv1.3 read client key update` |
| `0x0260EDF3` | `TLSv1.3 read server key update` |
| `0x025D5313` | `TLSv1.3 write client key update` |
| `0x0259A804` | `TLSv1.3 write server key update` |
| `0x0256E4E1` | `UPDATE "%w".%s SET sql = sqlite_rename_parent(sql, %Q, %Q) WHERE %s;` |
| `0x02623BD4` | `UPDATE "%w".%s SET sql = substr(sql,1,%d) || ', ' || %Q || substr(sql,%d) WHERE type = 'table' AND name = %Q` |
| `0x02582B97` | `UPDATE "%w".sqlite_sequence set name = %Q WHERE name = %Q` |
| `0x025B66DE` | `UPDATE %Q.%s SET rootpage=%d WHERE #%d AND rootpage=#%d` |
| `0x025E40DF` | `UPDATE %Q.%s SET sql = CASE WHEN type = 'trigger' THEN sqlite_rename_trigger(sql, %Q)ELSE sqlite_rename_table(sql, %Q) END, tbl_name = %Q, name = CASE WHEN type='table' THEN %Q WHEN name LIKE 'sqlite_autoindex%%' AND type='index' THEN 'sqlite_autoindex_' || %Q || substr(name,%d+18) ELSE name END WHERE tbl_name=%Q COLLATE nocase AND (type='table' OR type='index' OR type='trigger');` |
| `0x025D6EB0` | `UPDATE %Q.%s SET type='%s', name=%Q, tbl_name=%Q, rootpage=#%d, sql=%Q WHERE rowid=#%d` |
| `0x025E425F` | `UPDATE %Q.%s SET type='table', name=%Q, tbl_name=%Q, rootpage=0, sql=%Q WHERE rowid=#%d` |
| `0x0259981B` | `assets/` |
| `0x02600C74` | `cocos2dx-update-temp-package.zip` |
| `0x025E7D4F` | `ev update fd=%d, action '%s%s' -> '%s%s' (%d/%d r/w)` |
| `0x02627F1C` | `file:///android_asset/` |
| `0x02603F5E` | `mydownload/` |
| `0x0258DB2D` | `png_read_update_info/png_start_read_image: duplicate call` |
| `0x025A7A36` | `png_start_read_image/png_read_update_info: duplicate call` |
| `0x0261EF37` | `ui/buildupdatelist.csb` |
| `0x02584545` | `ui/buildupdatelist_1.csb` |
| `0x025F8885` | `ui/mod_download_item.csb` |
| `0x0258AC84` | `ui/mod_download_main.csb` |
| `0x0260043C` | `ui/secondary_password_update.csb` |
| `0x02607271` | `xml/download.xml` |

---
## 3. Error / Constraint Messages

**Total: 4930 error strings found**

### "not enough" (3 strings)

- `0x025C7E74`: `Not enough image data`
- `0x0261C247`: `not enough data`
- `0x0259C746`: `not enough space`

### "full" (347 strings)

- `0x027F9F90`: `15CRechargeFullUI`
- `0x027DDCA5`: `16FullScreenFollow`
- `0x028B4D31`: `16Full_rechargeXml`
- `0x027F9FBC`: `17CRechargeFullIcon`
- `0x026A5484`: `20CRechargeFullManager`
- `0x027F9FA2`: `23CRechargeFullRewardCell`
- `0x025F44E9`: `Connection pool is full, closing the oldest of %zu/%u`
- `0x0257FFA4`: `Disk full or allocation exceeded`
- `0x025730AE`: `FULL_NAME`
- `0x02587226`: `FullName`
- `0x025CB10F`: `FullScreenEffRoot`
- `0x025EAA51`: `Fulleffort`
- `0x0261DB97`: `Fulleffort_vip`
- `0x027F9FE7`: `NSt6__ndk110__function6__funcINS_6__bindIM15CRechargeFullUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x027FA167`: `NSt6__ndk110__function6__funcINS_6__bindIM17CRechargeFullIconFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x026A549B`: `NSt6__ndk110__function6__funcINS_6__bindIM20CRechargeFullManagerFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x0288A61B`: `NSt6__ndk110__function6__funcIZN13CSecretBossUI11onFullClickEvE3$_0NS_9allocatorIS3_EEFvPN10cocostudio8timeline5FrameEEEE`
- `0x0288B289`: `NSt6__ndk110__function6__funcIZN13CSecretBossUI24onRespenFullAttackReturnERK34CMSG_ATTACK_SECRET_BOSS_TEN_RETURNE3$_0NS_9allocatorIS6_EEFvvEEE`
- `0x027FA0E2`: `NSt6__ndk110__function6__funcIZN15CRechargeFullUI10updateTimeEvE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x02812044`: `NSt6__ndk110__function6__funcIZN16HeroExpeditionUI19onFullButtonClickedEvE3$_0NS_9allocatorIS3_EEFvRK16eMessageBoxEventEEE`
- `0x026D281F`: `NSt6__ndk110__function6__funcIZN17CMainCityBuilding24changToResourceFullModelEPN7cocos2d2ui6WidgetEE3$_0NS_9allocatorIS7_EEFvvEEE`
- `0x026D29D3`: `NSt6__ndk110__function6__funcIZN17CMainCityBuilding24changToResourceFullModelEPN7cocos2d2ui6WidgetEE3$_1NS_9allocatorIS7_EEFvlEEE`
- `0x027FA26A`: `NSt6__ndk110__function6__funcIZN17CRechargeFullIcon14bindControllerEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefEEEE`
- `0x027FA309`: `NSt6__ndk110__function6__funcIZN17CRechargeFullIcon7refreshEvE3$_0NS_9allocatorIS3_EEFNS_12basic_stringIcNS_11char_traitsIcEENS4_IcEEEEfEEE`
- `0x027FA3BA`: `NSt6__ndk110__function6__funcIZN17CRechargeFullIcon7refreshEvE3$_1NS_9allocatorIS3_EEFvvEEE`
- `0x02720D60`: `NSt6__ndk110__function6__funcIZN21MainCityBuildingGuide24changToResourceFullModelEPN7cocos2d2ui6WidgetEE3$_0NS_9allocatorIS7_EEFvvEEE`
- `0x02720E35`: `NSt6__ndk110__function6__funcIZN21MainCityBuildingGuide24changToResourceFullModelEPN7cocos2d2ui6WidgetEE3$_1NS_9allocatorIS7_EEFvlEEE`
- `0x026D28A1`: `NSt6__ndk110__function6__funcIZZN17CMainCityBuilding24changToResourceFullModelEPN7cocos2d2ui6WidgetEENK3$_0clEvEUliE_NS_9allocatorIS8_EEFvlEEE`
- `0x027FA0B1`: `NSt6__ndk114unary_functionIP15CRechargeFullUIvEE`
- `0x027FA237`: `NSt6__ndk114unary_functionIP17CRechargeFullIconvEE`
- `0x026A55BB`: `NSt6__ndk115binary_functionIP20CRechargeFullManagerPKcvEE`
- `0x027FA079`: `NSt6__ndk118__weak_result_typeIM15CRechargeFullUIFvvEEE`
- `0x027FA1FD`: `NSt6__ndk118__weak_result_typeIM17CRechargeFullIconFvvEEE`
- `0x026A557C`: `NSt6__ndk118__weak_result_typeIM20CRechargeFullManagerFvPKcEEE`
- `0x027FA048`: `NSt6__ndk16__bindIM15CRechargeFullUIFvvEJPS1_EEE`
- `0x027FA1CA`: `NSt6__ndk16__bindIM17CRechargeFullIconFvvEJPS1_EEE`
- `0x026A5525`: `NSt6__ndk16__bindIM20CRechargeFullManagerFvPKcEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x026329F0`: `REINDEXEDESCAPEACHECKEYBEFOREIGNOREGEXPLAINSTEADDATABASELECTABLEFTHENDEFERRABLELSEXCEPTRANSACTIONATURALTERAISEXCLUSIVEXISTSAVEPOINTERSECTRIGGEREFERENCESCONSTRAINTOFFSETEMPORARYUNIQUERYATTACHAVINGROUPDATEBEGINNERELEASEBETWEENOTNULLIKECASCADELETECASECOLLATECREATECURRENT_DATEDETACHIMMEDIATEJOINSERTMATCHPLANALYZEPRAGMABORTVALUESVIRTUALIMITWHENWHERENAMEAFTEREPLACEANDEFAULTAUTOINCREMENTCASTCOLUMNCOMMITCONFLICTCROSSCURRENT_TIMESTAMPRIMARYDEFERREDISTINCTDROPFAILFROMFULLGLOBYIFISNULLORDERESTRICTOUTERIGHTROLLBACKROWUNIONUSINGVACUUMVIEWINITIALLYHerF`
- `0x025A3269`: `RIGHT and FULL OUTER JOINs are not currently supported`
- `0x026307A5`: `SSL negotiation finished successfully`
- `0x0288A695`: `ZN13CSecretBossUI11onFullClickEvE3$_0`
- `0x0288B318`: `ZN13CSecretBossUI24onRespenFullAttackReturnERK34CMSG_ATTACK_SECRET_BOSS_TEN_RETURNE3$_0`
- `0x027FA140`: `ZN15CRechargeFullUI10updateTimeEvE3$_0`
- `0x028120BF`: `ZN16HeroExpeditionUI19onFullButtonClickedEvE3$_0`
- `0x026D2988`: `ZN17CMainCityBuilding24changToResourceFullModelEPN7cocos2d2ui6WidgetEE3$_0`
- `0x026D2A55`: `ZN17CMainCityBuilding24changToResourceFullModelEPN7cocos2d2ui6WidgetEE3$_1`
- `0x027FA2DC`: `ZN17CRechargeFullIcon14bindControllerEvE3$_0`
- `0x027FA395`: `ZN17CRechargeFullIcon7refreshEvE3$_0`
- `0x027FA416`: `ZN17CRechargeFullIcon7refreshEvE3$_1`
- `0x02720DE6`: `ZN21MainCityBuildingGuide24changToResourceFullModelEPN7cocos2d2ui6WidgetEE3$_0`
- *...and 297 more*

### "limit" (990 strings)

- `0x02593CEE`: `/Users/ls/cocos2d-x-3rd-party-libs-src/contrib/android-arm64/chipmunk/src/cpRotaryLimitJoint.c`
- `0x028B62F0`: `15Player_limitXml`
- `0x0266B647`: `16LimitShopManager`
- `0x027B7B48`: `18EventPageLimitShop`
- `0x027CB6AF`: `18LimitShopPreviewUI`
- `0x028B55DF`: `18Limit_shop_baseXml`
- `0x027CB9FA`: `19LimitShopRewardItem`
- `0x028B55F5`: `20Limit_shop_configXml`
- `0x028538CB`: `20LostLandHeroLimitTip`
- `0x027CBA10`: `22LimitShopRewardRowCell`
- `0x028B6572`: `22Red_envelopes_limitXml`
- `0x028B6A6E`: `22Special_event_limitXml`
- `0x0266B65A`: `23LimitShopBuySucessEvent`
- `0x027CB676`: `25LimitShopPreviewGoodsCell`
- `0x027CB692`: `26LimitShopPreviewDayTabCell`
- `0x0266C32D`: `32LimitShopPareareBuyForDaibiEvent`
- `0x026284E6`: `ACTIVE_CONN_ID_LIMIT appears multiple times`
- `0x0259A937`: `ACTIVE_CONN_ID_LIMIT is malformed`
- `0x025FBB1B`: `AEAD_LIMIT_REACHED`
- `0x025D45F5`: `Allowing sub-requests (like DoH) to override max connection limit`
- `0x025E0B4D`: `AtkLimit`
- `0x025E0DC3`: `BuyLimit`
- `0x0259A9E4`: `CONNECTION_ID_LIMIT_ERROR`
- `0x025E456B`: `ChatVIPLimited`
- `0x0262A466`: `ConditionLimit`
- `0x0258D669`: `Constraint is not a rotary limit joint.`
- `0x025D7314`: `CycleActionLimit`
- `0x025B3A4B`: `DailyLimit`
- `0x025B9EE2`: `Discarding connection #%ld from %zu to reach destination limit of %zu`
- `0x026211B0`: `Discarding connection #%ld from %zu to reach total limit of %zu`
- `0x02575598`: `Draw_GoldTen_Limit`
- `0x025D09A1`: `Draw_Gold_Limit`
- `0x025E4654`: `Exceeded stackLimit in readValue().`
- `0x025C3467`: `ExpeditionLevelLimit`
- `0x0258D7E5`: `Fail to play %s cause by limited max instance of AudioEngine`
- `0x02580527`: `Fail to play %s cause by limited max instance of AudioProfile`
- `0x025AE358`: `Fail to play %s cause by limited minimum delay`
- `0x025D3DE3`: `FreeHelpNumLimit`
- `0x0261AA65`: `FreeHelpRewardLimit`
- `0x0257C62C`: `GlobalChatLvLimit`
- `0x025E0EA6`: `GroupNumLimit`
- `0x02620EB1`: `HelpLimit`
- `0x025EA9C7`: `HeroDrawTimesLimit`
- `0x02620F26`: `HeroTroopLimit`
- `0x025C1241`: `Image height exceeds user limit in IHDR`
- `0x0256C3DF`: `Image width exceeds user limit in IHDR`
- `0x025FA762`: `InviteGoldLimit`
- `0x025A3214`: `LIMIT clause should come after %s not before`
- `0x025D0A2B`: `LevLimitBreached`
- `0x025B99E0`: `LimitCity`
- *...and 940 more*

### "cannot" (127 strings)

- `0x02610BC9`: `%s %T cannot reference objects in database %s`
- `0x02600E06`: `%s cannot be done over CONNECT`
- `0x02581310`: `Algorithm %s cannot be found`
- `0x02614EEB`: `Bodies cannot be put to sleep during a query or a call to cpSpaceStep(). Put these calls into a post-step callback.`
- `0x025BA112`: `CSeq cannot be set as a custom header.`
- `0x02601070`: `Cannot APPEND with unknown input file size`
- `0x025B3D69`: `Cannot APPEND without a mailbox.`
- `0x02593836`: `Cannot FETCH without a UID.`
- `0x02621331`: `Cannot SELECT without a mailbox.`
- `0x025A9A5F`: `Cannot add a NOT NULL column with default value NULL`
- `0x025EA710`: `Cannot add a PRIMARY KEY column`
- `0x02623B99`: `Cannot add a REFERENCES column with non-NULL default value`
- `0x02617528`: `Cannot add a UNIQUE column`
- `0x02561F5F`: `Cannot add a column to a view`
- `0x025C325D`: `Cannot add a column with non-constant default`
- `0x025E9CEB`: `Cannot find certificate signature algorithm`
- `0x025E33C3`: `Cannot open file`
- `0x0257FAD6`: `Cannot open file [`
- `0x025EE5DD`: `Cannot pause RTP`
- `0x02578F94`: `Cannot quantize more than %d color components`
- `0x0256BEDF`: `Cannot quantize to fewer than %d colors`
- `0x02578FC2`: `Cannot quantize to more than %d colors`
- `0x0262E6F6`: `Cannot remove a body that was not added to the space. (Removed twice maybe?)`
- `0x02579148`: `Cannot remove a constraint that was not added to the space. (Removed twice maybe?)`
- `0x025A0550`: `Cannot remove a shape that was not added to the space. (Removed twice maybe?)`
- `0x02593D6E`: `Cannot remove the designated static body for the space.`
- `0x0261AFBD`: `Cannot rewind mime/post data`
- `0x0256BEA1`: `Cannot transcode due to multiple use of quantization table %d`
- `0x0257294A`: `Cannot use a non-sleeping body as a group identifier.`
- `0x025E3C9F`: `Cannot use autodetected salt length`
- `0x0260D885`: `Cannot use sigv4 authentication with path-as-is flag`
- `0x02599C91`: `Cannot write a 0 size RTP packet.`
- `0x0258DC33`: `Compression buffer size cannot be changed because it is in use`
- `0x02573201`: `Compression buffer size cannot be reduced below 6`
- `0x025E1454`: `Connection #%ld is not open enough, cannot reuse`
- `0x02599D01`: `FTP: cannot figure out the host in the PASV response`
- `0x0260D844`: `HTTP server does not seem to support byte ranges. Cannot resume.`
- `0x0261B15E`: `LDAP: cannot bind`
- `0x0258F833`: `ML-KEM keys cannot be mutated`
- `0x025B413D`: `Non-dynamic bodies cannot be put to sleep.`
- `0x0261B1E7`: `Server upgrade cannot be used`
- `0x025EE590`: `Session ID cannot be set as a custom header.`
- `0x025C7769`: `Sleeping is not enabled on the space. You cannot sleep a body without setting a sleep time threshold on the space.`
- `0x02616B22`: `Suite B: cannot sign P-384 with P-256`
- `0x02614F5F`: `The body is already sleeping and it's group cannot be reassigned.`
- `0x02627BED`: `The number of contact points cannot be changed.`
- `0x025DB0AB`: `This operation cannot be done safely during a call to cpSpaceStep() or during a query. Put these calls into a post-step callback.`
- `0x025D4944`: `You cannot change the body on an active shape. You must remove the shape from the space before changing the body.`
- `0x025728D9`: `You cannot manually reindex objects while the space is locked. Wait until the current query or step is complete.`
- `0x025BA557`: `You cannot set the mass of kinematic or static bodies.`
- *...and 77 more*

### "fail" (649 strings)

- `0x0259A114`: `"SetPlayState fail"`
- `0x025C796F`: `"create audio player fail"`
- `0x02572A7E`: `"create opensl engine fail"`
- `0x025A08D3`: `"create output mix fail"`
- `0x02572A9A`: `"get the engine interface fail"`
- `0x02607EEE`: `"get the play interface fail"`
- `0x0259A0F6`: `"get the seek interface fail"`
- `0x026018D0`: `"get the volume interface fail"`
- `0x025C0FFB`: `"realize the engine fail"`
- `0x026151C6`: `"realize the output mix fail"`
- `0x025F4E16`: `"realize the player fail"`
- `0x02593651`: `%s failed`
- `0x0258FA67`: `%s failed to acquire mutex`
- `0x0261D770`: `%s failed to broadcast`
- `0x0256E311`: `%s failed to release mutex`
- `0x026151E4`: `%s,%d message:create player for %s fail`
- `0x0256BF88`: `) failed!`
- `0x027F6753`: `20CGiftPackBuyFaildTip`
- `0x02881A0E`: `23DailyRewardADLoadFailUI`
- `0x02881A28`: `26DailyRewardADPlayFailureUI`
- `0x02621621`: `A memory function failed`
- `0x0257F60F`: `AdLoadFail`
- `0x0260079D`: `AdOpenFail`
- `0x025E7D8F`: `Authentication failed: %d`
- `0x025C0799`: `Bind to local port %d failed, trying next`
- `0x02578643`: `BroadcastFail`
- `0x026113E5`: `CGiftPackManager::buyFail: %ld`
- `0x025EAFFF`: `CMSG_LOAD_AD_FAILURE`
- `0x0257FCAC`: `CONNECT tunnel failed, response %d`
- `0x025A9148`: `CRL signature failure`
- `0x025CD981`: `Chunk callback failed`
- `0x025D4A0C`: `Classloader failed to find class of %s`
- `0x025BA151`: `Command failed: %d`
- `0x025ADD91`: `DATA failed: %d`
- `0x025A84CD`: `DSO failure`
- `0x025CD997`: `ECH attempted but failed`
- `0x0262DED5`: `Error while processing content unencoding: Unknown failure within decompression software.`
- `0x0262E2D7`: `FTP: The server failed to connect to data port`
- `0x025C72E9`: `FTP: command PORT failed`
- `0x025A01A9`: `FTP: command REST failed`
- `0x025A0170`: `FTP: could not retrieve (RETR failed) the specified file`
- `0x025C062A`: `Fail to get android build version.`
- `0x025F412D`: `FailMail`
- `0x025E0B73`: `FailReward`
- `0x025EE345`: `Failed EPSV attempt, exiting`
- `0x0259FEB6`: `Failed EPSV attempt. Disabling EPSV`
- `0x0257FDE5`: `Failed FTP upload: %0d`
- `0x025FB012`: `Failed binding local connection end`
- `0x02578E35`: `Failed initialization`
- `0x025EE46E`: `Failed reading the chunked-encoded stream`
- *...and 599 more*

### "invalid" (429 strings)

- `0x025EA2FA`: `%s has invalid md size %d`
- `0x025A93E1`: `%s invalid private 's' vector`
- `0x02582450`: `%s invalid public 't' vector`
- `0x025B502D`: `<INVALID>`
- `0x02631BF4`: `<invalid length=%d>`
- `0x02614BA1`: `An invalid 'part' argument was passed as argument`
- `0x025A022E`: `An invalid CURLU pointer was passed as argument`
- `0x025828C8`: `An invalid regex grammar has been requested.`
- `0x02603C53`: `DW_EH_PE_datarel is invalid with a datarelBase of 0`
- `0x0258D1D8`: `Got invalid RTSP request`
- `0x025CD892`: `Got invalid RTSP request: RTSPREQ_LAST`
- `0x025E88A8`: `ICC profile length invalid (not a multiple of 4)`
- `0x025B5E14`: `INVALID (EMPTY)`
- `0x025F554C`: `INVALID_TOKEN`
- `0x0260EA9B`: `Ignoring invalid time value`
- `0x025AE21B`: `Index error: The specified contact index is invalid for this arbiter`
- `0x025F6D6A`: `Invalid %s private key length`
- `0x02617084`: `Invalid %s public key length`
- `0x025FAD8E`: `Invalid Content-Length: value`
- `0x025CE2DA`: `Invalid IHDR data`
- `0x02593A3F`: `Invalid IPv6 address format`
- `0x02607CD7`: `Invalid JPEG file structure: %s before SOF`
- `0x0262E59B`: `Invalid JPEG file structure: missing SOS marker`
- `0x025C0DA0`: `Invalid JPEG file structure: two SOF markers`
- `0x025801EB`: `Invalid JPEG file structure: two SOI markers`
- `0x025726C0`: `Invalid OCSP response`
- `0x02601440`: `Invalid OCSP response status: %s (%d)`
- `0x025DB055`: `Invalid SOS parameters for sequential JPEG`
- `0x026212D7`: `Invalid TIMEVALUE`
- `0x0259C37A`: `Invalid access!`
- `0x0259A4D5`: `Invalid attempt to read row data`
- `0x02573284`: `Invalid background palette index`
- `0x0261B7B6`: `Invalid bit depth for RGB image`
- `0x0261B7D6`: `Invalid bit depth for RGBA image`
- `0x0257A4A1`: `Invalid bit depth for grayscale image`
- `0x025C7ED3`: `Invalid bit depth for grayscale+alpha image`
- `0x02601E64`: `Invalid bit depth for paletted image`
- `0x025E87EE`: `Invalid bit depth in IHDR`
- `0x02607CB0`: `Invalid color quantization mode change`
- `0x02587344`: `Invalid color type in IHDR`
- `0x025CE288`: `Invalid color type/bit depth combination in IHDR`
- `0x025C0D48`: `Invalid component ID %d in SOS`
- `0x02573261`: `Invalid compression type specified`
- `0x02607C9B`: `Invalid crop request`
- `0x025CD9B0`: `Invalid easy handle`
- `0x025AFF76`: `Invalid enc public key`
- `0x025EEE6F`: `Invalid filter method in IHDR`
- `0x025EEF1E`: `Invalid filter type specified`
- `0x02608075`: `Invalid format for pCAL parameter`
- `0x025B4ABB`: `Invalid iCCP compression method`
- *...and 379 more*

### "denied" (12 strings)

- `0x025EE722`: `Access denied to remote resource`
- `0x025B9FF7`: `Access denied. %c`
- `0x02578CA2`: `Access denied: %03d`
- `0x0262E380`: `Login denied`
- `0x025A00DA`: `Remote access denied: %d`
- `0x025659AD`: `STARTTLS denied`
- `0x025B3E8D`: `STARTTLS denied, code %d`
- `0x025936E1`: `Server denied you to change to the given directory`
- `0x025C16E8`: `access denied`
- `0x02603DE4`: `access permission denied`
- `0x025B03C3`: `authorization denied`
- `0x02629062`: `tlsv1 alert access denied`

### "expired" (41 strings)

- `0x025CFB20`: `CRL has expired`
- `0x027551A3`: `NSt6__ndk110__function6__funcIZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_NS_9allocatorIS3_EEFvfEEE`
- `0x025AE08F`: `OCSP response has expired`
- `0x02755212`: `ZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_`
- `0x0068D9C9`: `_ZN12PlatformImpl14expiredSessionEv`
- `0x00695C86`: `_ZN19HeroSkillPlayHelper27CheckBuffSkillEffectExpiredEf`
- `0x00A42E99`: `_ZN19SLocalMapObjectInfo14setExpiredTimeEm`
- `0x00ADB9DB`: `_ZN21KingdomGiftRewardCell20_notifyRewardExpiredEv`
- `0x00892604`: `_ZN21SLuckyLotteryCategory19setExpiredRequestedEb`
- `0x010024F2`: `_ZN7cocos2d12PUBeamRender15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x01000C6D`: `_ZN7cocos2d14PUSlaveEmitter15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x01003DAC`: `_ZN7cocos2d19PURibbonTrailRender15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x010057FF`: `_ZN7cocos2d33PUDoPlacementParticleEventHandler15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x00A14D7F`: `_ZNK15SLocalMarchInfo9isExpiredEv`
- `0x0077B0E6`: `_ZNK16SKingdomGiftMeta9isExpiredEv`
- `0x00A42EC4`: `_ZNK19SLocalMapObjectInfo14getExpiredTimeEv`
- `0x00A42E73`: `_ZNK19SLocalMapObjectInfo9isExpiredEv`
- `0x008925D2`: `_ZNK21SLuckyLotteryCategory18isExpiredRequestedEv`
- `0x00893189`: `_ZNK29SLuckyLotteryHistoryRecordSet17isSyncTimeExpiredEv`
- `0x00ADC804`: `_ZNSt6__ndk110__function6__funcIZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_NS_9allocatorIS3_EEFvfEED0Ev`
- `0x00ADD5C6`: `_ZTINSt6__ndk110__function6__funcIZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_NS_9allocatorIS3_EEFvfEEE`
- `0x00ADC8B4`: `_ZTIZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_`
- `0x00ADD639`: `_ZTSNSt6__ndk110__function6__funcIZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_NS_9allocatorIS3_EEFvfEEE`
- `0x00ADC878`: `_ZTSZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_`
- `0x00ADC6B1`: `_ZTVNSt6__ndk110__function6__funcIZN21KingdomGiftRewardCell20_notifyRewardExpiredEvEUlfE_NS_9allocatorIS3_EEFvfEEE`
- `0x0100586C`: `_ZThn104_N7cocos2d33PUDoPlacementParticleEventHandler15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x01000D15`: `_ZThn504_N7cocos2d14PUSlaveEmitter15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x0100254A`: `_ZThn88_N7cocos2d12PUBeamRender15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x01003E0B`: `_ZThn88_N7cocos2d19PURibbonTrailRender15particleExpiredEPNS_18PUParticleSystem3DEPNS_12PUParticle3DE`
- `0x02624C74`: `_notifyRewardExpired`
- `0x02607C7E`: `add, session already expired`
- `0x0068A046`: `android_expiredSession`
- `0x02573569`: `certificate expired`
- `0x0262995B`: `certificate has expired`
- `0x010AF522`: `dtls1_is_timer_expired`
- `0x02575465`: `expiredSession`
- `0x02599C37`: `multi_timeout() says this has expired`
- `0x025EF9DD`: `read timeout expired`
- `0x00682E49`: `sqlite3_expired`
- `0x02594EBB`: `ssl/tls alert certificate expired`
- `0x02581D5D`: `status expired`

### "locked" (69 strings)

- `0x0262E743`: `!cpSpaceIsLocked(space)`
- `0x02565D11`: `!space->locked`
- `0x0275B418`: `30LostLandTechBuildingLockedCell`
- `0x010C0DDF`: `BN_MONT_CTX_set_locked`
- `0x026159C0`: `DATA_BLOCKED`
- `0x025A13BD`: `DATA_BLOCKED valid only in 0/1-RTT`
- `0x025E80B8`: `SSL shutdown send blocked`
- `0x025B4F87`: `STREAMS_BLOCKED_BIDI`
- `0x0256C976`: `STREAMS_BLOCKED_UNI`
- `0x026221A9`: `STREAM_DATA_BLOCKED`
- `0x025A7F14`: `STREAM_DATA_BLOCKED frame for TX only stream`
- `0x026083E2`: `STREAM_DATA_BLOCKED valid only in 0/1-RTT`
- `0x00944C65`: `_ZN10PetManager37getAllCouldUnlockAndUnlockedPetSkillsEv`
- `0x009CCF40`: `_ZN15TaskDataManager19isDailyTaskUnlockedERK14DailyTasksData`
- `0x00699E4A`: `_ZN16HeroTroopManager14_isTroopLockedEP9HeroTroop`
- `0x00D649FC`: `_ZN17CLordSkillUseCell8isLockedEv`
- `0x00D7BAA7`: `_ZN23LostLandEventKingRoadUI10SDayItemUi9SetLockedEb`
- `0x0096D98D`: `_ZN24COnlineRewardsVipManager13isBoxUnlockedEi`
- `0x00BCD557`: `_ZN26EventPage7DaysKingRoadTask10SDayItemUi9SetLockedEb`
- `0x00D7003B`: `_ZN30DominionBuildingViewPlayerCell10initLockedEv`
- `0x00D6FFDB`: `_ZN30DominionBuildingViewPlayerCell16createLockedCellEv`
- `0x00AF2378`: `_ZN30LostLandTechBuildingLockedCell14bindControllerEv`
- `0x00AF1388`: `_ZN30LostLandTechBuildingLockedCell6createEi`
- `0x00AF0E75`: `_ZN30LostLandTechBuildingLockedCell8cellSizeEv`
- `0x00AF2350`: `_ZN30LostLandTechBuildingLockedCellD0Ev`
- `0x00AF2328`: `_ZN30LostLandTechBuildingLockedCellD2Ev`
- `0x007C35FF`: `_ZN31LostLandScienceNBuildingManager23_loadLockedBuildingListEv`
- `0x00A714C2`: `_ZN7cocos2d2ui8PageView14setTouchLockedEb`
- `0x00827E6E`: `_ZNK21CChatHeadFrameManager19IsHeadFrameUnlockedEi`
- `0x00AF23AE`: `_ZNK30LostLandTechBuildingLockedCell8isLockedEv`
- `0x00AF1B2F`: `_ZNK30LostLandTechBuildingNormalCell8isLockedEv`
- `0x00AF2B48`: `_ZTI30LostLandTechBuildingLockedCell`
- `0x00AF2B6D`: `_ZTS30LostLandTechBuildingLockedCell`
- `0x00AF13F9`: `_ZTV30LostLandTechBuildingLockedCell`
- `0x00AF240D`: `_ZThn840_N30LostLandTechBuildingLockedCellD0Ev`
- `0x00AF23DE`: `_ZThn840_N30LostLandTechBuildingLockedCellD1Ev`
- `0x0257C0A5`: `condition_variable::timed wait: mutex not locked`
- `0x0261D6BE`: `condition_variable::wait: mutex not locked`
- `0x0100E045`: `cpSpaceIsLocked`
- `0x0257A7FD`: `data_blocked`
- `0x02623B83`: `database %s is locked`
- `0x0257C410`: `database is locked`
- `0x025F705B`: `database schema is locked: %s`
- `0x025E42D6`: `database table is locked`
- `0x025B65FA`: `database table is locked: %s`
- `0x025A1406`: `depack_do_frame_data_blocked`
- `0x025DBB80`: `depack_do_frame_stream_data_blocked`
- `0x0261BBBC`: `depack_do_frame_streams_blocked`
- `0x02629F3F`: `drbg_ctr_set_ctx_params_locked`
- `0x02581273`: `engine_unlocked_finish`
- *...and 19 more*

### "busy" (13 strings)

- `0x0272C6E7`: `17TutCond_BuildBusy`
- `0x025FDFBD`: `BuildBusy`
- `0x009600F2`: `_ZN17CMainCityBuilding6isBusyEv`
- `0x00A61E6C`: `_ZN17TutCond_BuildBusy5checkEP12TiXmlElement`
- `0x00A45662`: `_ZN21MainCityBuildingGuide6isBusyEv`
- `0x00A671F0`: `_ZTI17TutCond_BuildBusy`
- `0x00A67208`: `_ZTS17TutCond_BuildBusy`
- `0x00A671D8`: `_ZTV17TutCond_BuildBusy`
- `0x0261D847`: `bind on a busy prepared statement: [%s]`
- `0x006837AD`: `sqlite3_busy_handler`
- `0x006837DB`: `sqlite3_busy_timeout`
- `0x00683414`: `sqlite3_stmt_busy`
- `0x026043EE`: `tid_chat_main_send_busy`

### "cooldown" (26 strings)

- `0x025F4190`: `CoolDown`
- `0x0281B84C`: `NSt6__ndk110__function6__funcIZN25DominionBuildingSpeedUpUI18updateCoolDownTimeEvE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x026022B4`: `RXKU cooldown internal error`
- `0x0281B8BC`: `ZN25DominionBuildingSpeedUpUI18updateCoolDownTimeEvE3$_0`
- `0x0087F47B`: `_ZN10PlayerUser17getLeagueCoolDownEv`
- `0x0082CFF8`: `_ZN11ChatManager15setCoolDownTimeEv`
- `0x0082DAC6`: `_ZN11ChatManager22setRequestCoolDownTimeEv`
- `0x0082DA66`: `_ZN11ChatManager26getSendMessageCoolDownTimeEv`
- `0x0082DA36`: `_ZN11ChatManager27isInSendMessageCoolDownTimeEv`
- `0x0082DA95`: `_ZN11ChatManager28isInRequesetTimeCoolDownTimeEv`
- `0x0069C24A`: `_ZN11SoldierNode15_AiFireCooldownEf`
- `0x00B29D63`: `_ZN13BattleVideoUI18_onSchedulCooldownEf`
- `0x00693A7C`: `_ZN13BattleVideoUI19SetQuitCooldownTimeEt`
- `0x00DB043F`: `_ZN14MergePetGameUI15setCooldownTimeEt`
- `0x00DB0466`: `_ZN14MergePetGameUI18_onSchedulCooldownEf`
- `0x0069FEBB`: `_ZN15BattleVideoRoot19setQuitCooldownTimeEt`
- `0x00D273D9`: `_ZN17CLeagueTechDonate17addCoolDownEffectEPKc`
- `0x0090F9DE`: `_ZN18CLeagueTechManager12isInCoolDownEv`
- `0x0080542A`: `_ZN19CBargainGiftManager26getSendMessageCoolDownTimeEv`
- `0x0085730F`: `_ZN24CDominionBuildingManager22setRequestCoolDownTimeEv`
- `0x008572D1`: `_ZN24CDominionBuildingManager28isInRequesetTimeCoolDownTimeEv`
- `0x0096DAB7`: `_ZN24COnlineRewardsVipManager20getCoolDownTotalTimeEv`
- `0x0090F4BF`: `_ZN25DominionBuildingSpeedUpUI18updateCoolDownTimeEv`
- `0x025E0394`: `m_pTextCoolDownTime`
- `0x025736DA`: `ossl_qrl_enc_level_set_key_cooldown_done`
- `0x010B9B1E`: `ossl_qrl_enc_level_set_key_cooldown_done`

### "already" (56 strings)

- `0x0260E15E`: `Console already started. 'stop' it before calling 'listen' again`
- `0x0262783A`: `File already completely downloaded`
- `0x025DAAF2`: `File already completely uploaded`
- `0x025A7D1F`: `IP address was already set`
- `0x025E11B9`: `Mime post already completely uploaded`
- `0x0261AF73`: `PREAUTH connection, already authenticated`
- `0x0260DB01`: `Remote file already exists`
- `0x02584CFA`: `Text_AlreadyFriend`
- `0x025CD9C4`: `The easy handle is already added to a multi handle`
- `0x025FAD64`: `The entire document is already downloaded`
- `0x0258283A`: `The future has already been retrieved from the promise or packaged_task.`
- `0x025F0AC4`: `The state of the promise has already been set.`
- `0x0262E75B`: `This static index is already associated with a dynamic index.`
- `0x025BA5B8`: `You have already added this body to this space. You must not add it a second time.`
- `0x02586DF0`: `You have already added this constraint to this space. You must not add it a second time.`
- `0x025B40DC`: `You have already added this shape to this space. You must not add it a second time.`
- `0x025E1485`: `[WS] curl_ws_send() called with smaller 'buflen' than bytes already buffered in previous call, %zu vs %zu`
- `0x0091BA8A`: `_ZN15LogicLeagueBoss15getAlreadyItemsEv`
- `0x007068E7`: `_ZN16LogicAchievement13getAlreadyNumEv`
- `0x0097B7BC`: `_ZN8LogicPVE21getChapterAlreadyStarEi`
- `0x0074CE9A`: `_ZNK23ElementalBuffWarManager26GetAlreadyEnterBattleTimesEv`
- `0x007DB8CC`: `_ZNK24COverlordActivityManager26GetAlreadyEnterBattleTimesEv`
- `0x00753DC7`: `_ZNK26CEmperorWarActivityManager26GetAlreadyEnterBattleTimesEv`
- `0x0258EDBE`: `already instantiated`
- `0x02628D8C`: `already loaded`
- `0x0261B00E`: `attempt to borrow xfer_buf when already borrowed`
- `0x025FAE67`: `attempt to borrow xfer_ulbuf when already borrowed`
- `0x02567AE9`: `cert already in hash table`
- `0x0256D0B5`: `certificate already present`
- `0x0258E057`: `connection already has a default stream`
- `0x025E9CB3`: `crl already delta`
- `0x0259B250`: `custom ext handler already installed`
- `0x025C2153`: `dane already enabled`
- `0x026174F0`: `database %s is already in use`
- `0x025B6790`: `database is already attached`
- `0x025E9C24`: `distpoint already set`
- `0x025CF71B`: `drbg already initialized`
- `0x025CEF66`: `dso already loaded`
- `0x02599A67`: `easy handle already used in multi handle`
- `0x025B238A`: `friend_text_already_Application`
- `0x02575900`: `grpchat_text_mail_alreadyquit`
- `0x02583453`: `guild_check_msg_alreadyapply`
- `0x025A31BE`: `index %s already exists`
- `0x025A51CF`: `m_pPanelAlreadyFriend`
- `0x0257DE3B`: `m_pTextAlreadyBid`
- `0x025C7192`: `master easy %u already gone.`
- `0x0260F5F5`: `pkey application asn1 method already registered`
- `0x025F045B`: `policy language already defined`
- `0x025CFAB1`: `policy path length already defined`
- `0x0262285C`: `provider already exists`
- *...and 6 more*

### "too many" (33 strings)

- `0x025DB080`: `Application transferred too many scanlines`
- `0x0261B6EA`: `Row has too many bytes to allocate in memory`
- `0x02615443`: `Too many IDATs found`
- `0x025E1F72`: `Too many bytes for PNG signature`
- `0x025AE155`: `Too many color components: %d, max %d`
- `0x02578D0B`: `Too many response headers, %d is max`
- `0x02621D7E`: `png_set_keep_unknown_chunks: too many chunks`
- `0x02608AC3`: `response too many hdrlines`
- `0x02595DFA`: `too many SQL variables`
- `0x0257C200`: `too many arguments on function %T`
- `0x02568355`: `too many attached databases - max %d`
- `0x02573E23`: `too many bytes`
- `0x025EA694`: `too many columns in %s`
- `0x025D6F1E`: `too many columns in result set`
- `0x0259C54F`: `too many columns on %s`
- `0x025AEF5D`: `too many iterations`
- `0x02622B0A`: `too many key updates`
- `0x025C1485`: `too many length or distance symbols`
- `0x0259C457`: `too many levels of trigger recursion`
- `0x025EF77C`: `too many names`
- `0x025C1F10`: `too many pipes`
- `0x025A1019`: `too many profiles`
- `0x0256D009`: `too many records`
- `0x025B54C3`: `too many redirections`
- `0x026089F3`: `too many retries`
- `0x0259A58C`: `too many sPLT chunks`
- `0x0258146B`: `too many temporary variables`
- `0x02610B8E`: `too many terms in %s BY clause`
- `0x025E4070`: `too many terms in ORDER BY clause`
- `0x025D05CE`: `too many terms in compound SELECT`
- `0x025D50CA`: `too many text chunks`
- `0x025BAB60`: `too many unknown chunks`
- `0x02622B1F`: `too many warn alerts`

### "not allow" (22 strings)

- `0x025A9A47`: `%s mode not allowed: %s`
- `0x0258925F`: `An empty regex is not allowed in the POSIX grammar.`
- `0x025A9716`: `Explicit digest not allowed with EdDSA operations`
- `0x025AE464`: `MNG features are not allowed in a PNG datastream`
- `0x02595B98`: `No padding not allowed with RSA-PSS`
- `0x025F6DF6`: `OAEP padding not allowed for signing / verifying`
- `0x02575172`: `PKCS#1 padding not allowed with RSA-PSS`
- `0x025DAC04`: `Received HTTP/0.9 when not allowed`
- `0x02599E9C`: `SSL session does not allow earlydata`
- `0x025DCD9D`: `Suite B: curve not allowed for this LOS`
- `0x025801BC`: `Suspension not allowed here`
- `0x0257519A`: `X.931 padding not allowed with RSA-PSS`
- `0x025E4035`: `aggregate functions are not allowed in the GROUP BY clause`
- `0x025F67C4`: `digest not allowed`
- `0x02609362`: `mgf1 digest not allowed`
- `0x02609DB0`: `parameters are not allowed in views`
- `0x02616AE2`: `proxy certificates not allowed, please set the appropriate flag`
- `0x0257C222`: `qualified table names are not allowed on INSERT, UPDATE, and DELETE statements within triggers`
- `0x025F7091`: `the INDEXED BY clause is not allowed on UPDATE or DELETE statements within triggers`
- `0x025682A8`: `the NOT INDEXED clause is not allowed on UPDATE or DELETE statements within triggers`
- `0x025815D4`: `wrap mode not allowed`
- `0x025BCAA9`: `xof digests not allowed`

### "error" (1104 strings)

- `0x025A264F`: `%*s<Parse Error>`
- `0x025CDF7C`: `%s error:%u`
- `0x025E1443`: `.netrc error: %s`
- `0x0269B4F1`: `19ErrorMessageManager`
- `0x025687D0`: `>>set_opent_time_error`
- `0x025F555A`: `APPLICATION_ERROR`
- `0x025EEABD`: `Aborting due to Chipmunk error: `
- `0x025ADE3B`: `An authentication function returned an error`
- `0x010BFE96`: `BIO_dgram_non_fatal_error`
- `0x010BB3EE`: `BIO_fd_non_fatal_error`
- `0x025BA36A`: `BIO_new return NULL, OpenSSL error %s`
- `0x0256BD4C`: `BIO_new_mem_buf NULL, OpenSSL error %s`
- `0x010BFD20`: `BIO_sock_error`
- `0x010BF945`: `BIO_sock_non_fatal_error`
- `0x025CE025`: `Base64Utils: error decoding`
- `0x025DB6AE`: `CRC error`
- `0x025B5EB4`: `CRL path validation error`
- `0x025B0E44`: `CSystemEnvironment: error`
- `0x025FB6EF`: `Can't discard critical data on CRC error`
- `0x010BE702`: `ERR_add_error_data`
- `0x010C7C96`: `ERR_add_error_mem_bio`
- `0x010C7C84`: `ERR_add_error_txt`
- `0x010C7C1A`: `ERR_add_error_vdata`
- `0x0100A7BE`: `ERR_clear_error`
- `0x010C7B6A`: `ERR_error_string`
- `0x0100A5FA`: `ERR_error_string_n`
- `0x010C7B7B`: `ERR_func_error_string`
- `0x0100A7B0`: `ERR_get_error`
- `0x010C7A08`: `ERR_get_error_all`
- `0x010C7A1A`: `ERR_get_error_line`
- `0x010C7A2D`: `ERR_get_error_line_data`
- `0x010C7BEC`: `ERR_get_next_error_library`
- `0x010C7B55`: `ERR_lib_error_string`
- `0x0100A5DB`: `ERR_peek_error`
- `0x010C7A81`: `ERR_peek_error_all`
- `0x010C7A6D`: `ERR_peek_error_data`
- `0x010C7A59`: `ERR_peek_error_func`
- `0x010C7A45`: `ERR_peek_error_line`
- `0x010C7A94`: `ERR_peek_error_line_data`
- `0x0100AA3B`: `ERR_peek_last_error`
- `0x010C7AF8`: `ERR_peek_last_error_all`
- `0x010C7ADF`: `ERR_peek_last_error_data`
- `0x010C7AC6`: `ERR_peek_last_error_func`
- `0x010C7AAD`: `ERR_peek_last_error_line`
- `0x010C7B10`: `ERR_peek_last_error_line_data`
- `0x010C7CAC`: `ERR_print_errors`
- `0x010C7C70`: `ERR_print_errors_cb`
- `0x010C7CBD`: `ERR_print_errors_fp`
- `0x010BF916`: `ERR_reason_error_string`
- `0x010AFE0E`: `ERR_set_error`
- *...and 1054 more*

### "timeout" (98 strings)

- `0x025A6DE6`: `%s connect timeout after %ldms, move on!`
- `0x0262E14C`: `%s pollset[], timeouts=%zu, paused %d/%d (r/w)`
- `0x0258D151`: `%s pollset[fd=%d %s%s, fd=%d %s%s], timeouts=%zu`
- `0x025D4323`: `%s pollset[fd=%d %s%s], timeouts=%zu`
- `0x02572281`: `%s pollset[fds=%u], timeouts=%zu`
- `0x02578C1B`: `%s starting (timeout=%ldms)`
- `0x0256B8E1`: `Accept timeout occurred while waiting server connect`
- `0x0262777C`: `Connection timeout after %ld ms`
- `0x025FABA1`: `FTP response timeout`
- `0x025C179F`: `MAX_IDLE_TIMEOUT appears multiple times`
- `0x025D5448`: `MAX_IDLE_TIMEOUT is malformed`
- `0x0284582D`: `NSt6__ndk110__function6__funcIZN7LoginUI12loginTimeOutEfE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x0262E17B`: `PENDING handle timeout`
- `0x025ADA61`: `Proxy CONNECT aborted due to timeout`
- `0x025F4B63`: `SSL shutdown timeout`
- `0x010B4D08`: `SSL_CTX_get_timeout`
- `0x010B4CF4`: `SSL_CTX_set_timeout`
- `0x0100A3F6`: `SSL_SESSION_get_timeout`
- `0x010B4ADF`: `SSL_SESSION_set_timeout`
- `0x010B2490`: `SSL_get_default_timeout`
- `0x010B3CE0`: `SSL_get_event_timeout`
- `0x025ADE9F`: `Timeout waiting for block %d ACK.  Retries = %d`
- `0x025A720F`: `Timeout waiting for block %d ACK. Retries = %d`
- `0x025ADDDB`: `Timeout was reached`
- `0x025C7058`: `We got a 421 - timeout`
- `0x02845884`: `ZN7LoginUI12loginTimeOutEfE3$_0`
- `0x0262DF59`: `[SHUTDOWN] destroy, %zu connections, timeout=%dms`
- `0x02565B34`: `[WS] Timeout waiting for socket becoming writable`
- `0x006C57A4`: `_ZN10CGameLogic14onLoginTimeOutEv`
- `0x00A1568C`: `_ZN10KingdomMap16SSearchCacheMeta16s_nTimeoutSecondE`
- `0x008406D2`: `_ZN19CCityDurableManager26runTimeOutCanAddDurabilityEi`
- `0x008404A0`: `_ZN19CCityDurableManager35bindTimeOutCanAddDurabilityFunctionEPvNSt6__ndk18functionIFvvEEE`
- `0x008404FB`: `_ZN19CCityDurableManager37unBindTimeOutCanAddDurabilityFunctionEPv`
- `0x00991781`: `_ZN20CRedEnvelopesManager18showTimeoutMessageEv`
- `0x00990994`: `_ZN20CRedEnvelopesManager20examEnvelopesTimeoutEv`
- `0x0099054A`: `_ZN20CRedEnvelopesManager21onMsgLuckyGiftTimeoutEPKc`
- `0x009906B7`: `_ZN20CRedEnvelopesManager30onCMSG_MERGE_GAME_GIFT_TIMEOUTEPKc`
- `0x009205DF`: `_ZN20LeagueJoinTipManager9onTimeOutEv`
- `0x00993D7A`: `_ZN22LogicRedEnvelopesBonus18showTimeoutMessageEv`
- `0x00DF9AB4`: `_ZN22RedEnvelopesListUICell11showTimeOutEv`
- `0x00990DEA`: `_ZN23CMSG_LUCKY_GIFT_TIMEOUT7getDataEPKc`
- `0x00F9CABF`: `_ZN23CMSG_LUCKY_GIFT_TIMEOUT8packDataER8CIStream`
- `0x00990DC9`: `_ZN23CMSG_LUCKY_GIFT_TIMEOUTC1Ev`
- `0x00F9CA9E`: `_ZN23CMSG_LUCKY_GIFT_TIMEOUTC2Ev`
- `0x00724E1E`: `_ZN27CChessBattleActivityManager37_onBattlefieldTimeoutClearBattlefieldEv`
- `0x00991208`: `_ZN28CMSG_MERGE_GAME_GIFT_TIMEOUT7getDataEPKc`
- `0x00FAA186`: `_ZN28CMSG_MERGE_GAME_GIFT_TIMEOUT8packDataER8CIStream`
- `0x009911E2`: `_ZN28CMSG_MERGE_GAME_GIFT_TIMEOUTC1Ev`
- `0x00FAA160`: `_ZN28CMSG_MERGE_GAME_GIFT_TIMEOUTC2Ev`
- `0x006C3680`: `_ZN7LoginUI11stopTimeOutEv`
- *...and 48 more*

### "disconnect" (11 strings)

- `0x025C2C72`: ` peer has disconnected%s`
- `0x0261AFDA`: `Connection disconnected`
- `0x025BA00F`: `Got DISCONNECT`
- `0x025D4562`: `Too old connection (%ld ms idle, max idle is %ld ms), disconnect it`
- `0x025D45A6`: `Too old connection (created %ld ms ago, max lifetime is %ld ms), disconnect it`
- `0x006C7C05`: `_ZN14MessageSubject10disconnectEv`
- `0x00F583B4`: `_ZN7NetCtrl10disConnectEv`
- `0x00A51F29`: `_ZN7NetCtrl22disConnectAndClearDataEv`
- `0x026219EE`: `disconnect`
- `0x0257226D`: `server disconnected`
- `0x02614B16`: `smtp_disconnect(), finished`

### "missing" (112 strings)

- `0x025FD5BE`: ` missing from index `
- `0x0257FA9F`: ` part is missing meshPartId or materialId`
- `0x0259C48B`: `%d of %d pages missing from overflow list starting at %d`
- `0x02615F37`: `'id' or 'name' missing`
- `0x010B4947`: `EVP_PKEY_missing_parameters`
- `0x025EE498`: `Illegal or missing hexadecimal sequence`
- `0x0261DD7E`: `Missing ',' or ']' in array declaration`
- `0x0256E88F`: `Missing ',' or '}' in object declaration`
- `0x025DDAF1`: `Missing ':' after object member name`
- `0x0261DD5C`: `Missing '}' or object member name`
- `0x025F6A8E`: `Missing Authority Key Identifier`
- `0x025A731A`: `Missing Huffman code table entry`
- `0x025BAA9C`: `Missing IHDR before IDAT`
- `0x025A7A1D`: `Missing PLTE before IDAT`
- `0x025C93DA`: `Missing Subject Key Identifier`
- `0x0256E645`: `Missing the second \u in surrogate pair`
- `0x025C0884`: `SASL: %s is missing %s`
- `0x025F4582`: `SASL: %s is missing username`
- `0x025F4861`: `URL using bad/illegal format or missing URL`
- `0x025C09F7`: `aws-sigv4: region missing in parameters and hostname`
- `0x0261AF0E`: `aws-sigv4: service missing in parameters and hostname`
- `0x02607FB3`: `base64Decode: encoding incomplete: at least 2 bits missing`
- `0x0257238D`: `end of response with %ld bytes missing`
- `0x025B541C`: `field missing`
- `0x025BB9D0`: `log conf missing description`
- `0x0257AF63`: `log conf missing key`
- `0x025657D3`: `lookup word is missing`
- `0x0260F525`: `missing %s digest_sign function:%s`
- `0x02594B53`: `missing %s digest_sign_init:%s`
- `0x025A8362`: `missing %s digest_verify function:%s`
- `0x025E2ACA`: `missing %s digest_verify_init:%s`
- `0x025BB720`: `missing %s init:%s`
- `0x0259AEB5`: `missing %s newctx or freectx:%s`
- `0x025E2AA4`: `missing %s params getter or setter:%s`
- `0x025D5AE8`: `missing %s sign_init or sign_message_init:%s`
- `0x025D5AC9`: `missing %s signing function:%s`
- `0x025A19FB`: `missing %s verification function:%s`
- `0x02573C45`: `missing %s verify_init or verify_message_init:%s`
- `0x02587D8D`: `missing %s verify_recover:%s`
- `0x025A0FF9`: `missing IHDR`
- `0x0260EAB7`: `missing LZ dictionary`
- `0x025FC143`: `missing OID`
- `0x0259BF23`: `missing SHA3 digest algorithms while creating %s key`
- `0x02581687`: `missing asn1 encoding`
- `0x025EF590`: `missing asn1 eos`
- `0x025C30BE`: `missing cek alg`
- `0x025AF060`: `missing central gen key`
- `0x0257AF27`: `missing certid`
- `0x02610965`: `missing cipher`
- `0x0258E6F0`: `missing close square bracket`
- *...and 62 more*

### "insufficient" (25 strings)

- `0x02586D08`: `Insufficient memory (case %d)`
- `0x025BAB38`: `Insufficient memory for hIST chunk data`
- `0x0259432A`: `Insufficient memory for pCAL parameter`
- `0x025B4A97`: `Insufficient memory for pCAL params`
- `0x025C13F9`: `Insufficient memory for pCAL purpose`
- `0x0260EB8C`: `Insufficient memory for pCAL units`
- `0x02608097`: `Insufficient memory to process iCCP chunk`
- `0x025C143A`: `Insufficient memory to process iCCP profile`
- `0x0256C4A5`: `Insufficient memory to process text chunk`
- `0x0257A41C`: `Insufficient memory to store text`
- `0x02627AC8`: `Insufficient randomness`
- `0x025B646D`: `There was insufficient memory to convert the expression into a finite state machine.`
- `0x0258F9D5`: `There was insufficient memory to determine whether the regular expression could match the specified character sequence.`
- `0x00E5BF62`: `_ZN24CWatchTowerQueueDetailUI28insufficientBuildLevelNoticeEv`
- `0x025911A0`: `honor_value_insufficient_tips`
- `0x0261C257`: `insufficient data space`
- `0x025F670F`: `insufficient drbg strength`
- `0x025F516C`: `insufficient memory`
- `0x025AE504`: `insufficient memory to read chunk`
- `0x025C1F53`: `insufficient param size`
- `0x02573E04`: `insufficient secure data space`
- `0x0256C7DA`: `insufficient security`
- `0x0261CB8B`: `randomness source strength insufficient`
- `0x0262907C`: `tlsv1 alert insufficient security`
- `0x0257DA9C`: `vip_lv_insufficient_go`

### "other" (763 strings)

- `0x0261CC4D`: ` (Empty)`
- `0x0259C1F4`: `%s exceeds name buffer length`
- `0x025A93FF`: `%s public key hash mismatch`
- `0x025BA243`: `(Empty suboption?)`
- `0x027DFD02`: `15EmptyNodeReader`
- `0x027B24AE`: `16EventPageEmptyUI`
- `0x028769FD`: `16PetInfoCellEmpty`
- `0x028B50EB`: `17Illegality_newXml`
- `0x0284327E`: `22LegionWarRankEmptyCell`
- `0x028B5100`: `23Illegality_new_exactXml`
- `0x026214F0`: `A requested feature, protocol or option was not found built-in in this libcurl due to a build-time decision.`
- `0x0262781C`: `ACCT rejected by server: %03d`
- `0x02589505`: `AFEvent key empty!!!: %d `
- `0x026014F8`: `Application transferred too few scanlines`
- `0x026219D7`: `Attachment not found: `
- `0x025D4B42`: `Bone not found: `
- `0x0260843C`: `CRYPTO_BUFFER_EXCEEDED`
- `0x02596B9C`: `CSoldier::update---CC_SHOW_EMPTY_IMG---can't load(%s)`
- `0x0258D12E`: `Client ID length mismatched: [%zu]`
- `0x025AE115`: `Component index %d: mismatching sampling ratio %d:%d, %d:%d, %c`
- `0x025A73A4`: `Corrupt JPEG data: %u extraneous bytes before marker 0x%02x`
- `0x0260153F`: `Corrupt JPEG data: bad Huffman code`
- `0x025D48B6`: `Corrupt JPEG data: bad arithmetic code`
- `0x025DB01D`: `Corrupt JPEG data: found marker 0x%02x instead of RST%d`
- `0x025AE1E4`: `Corrupt JPEG data: premature end of data segment`
- `0x025D6E86`: `Corruption detected in cell %d on page %d`
- `0x025897DC`: `Duplicate key: '`
- `0x02623125`: `Duplicated name `%s'`
- `0x025CDC81`: `Empty JPEG image (DNL not supported)`
- `0x0258F1E8`: `Empty Subject Alternative Name extension`
- `0x02583037`: `Empty escape sequence in string`
- `0x025A733B`: `Empty input file`
- `0x02600FD0`: `Empty reply from server`
- `0x0261B449`: `EmptyCsb.csb`
- `0x025666E8`: `EmptyFragments`
- `0x025804EE`: `Event not found: `
- `0x025658A5`: `Exceeded storage allocation`
- `0x0261B0D6`: `Exceeded the maximum allowed file size (%ld) with %ld bytes`
- `0x0259FD7A`: `Exception`
- `0x0258FC2C`: `Expression tree is too large (maximum depth %d)`
- `0x025BBD1F`: `Hold Instruction Reject`
- `0x0256C12F`: `IK bone not found: `
- `0x02631D6C`: `IP address mismatch`
- `0x025DABD3`: `Ignoring duplicate digest auth header.`
- `0x025721F6`: `Illegal STS header skipped`
- `0x0258D024`: `Illegal port number in EPSV reply`
- `0x02583097`: `Illegality`
- `0x025CFBA7`: `Issuer name empty`
- `0x0260DD7B`: `JPEG parameter struct mismatch: library thinks size is %u, caller expects %u`
- `0x02586AEA`: `Malformed ACK packet, rejecting`
- *...and 713 more*

---
## 4. Debug / Game Mechanic Strings

**Total: 48578 strings across 20 categories**

### Alliance (10 strings)

- `0x02619772`: `ui/alliance_help.csb`
- `0x025B8B38`: `ui/alliance_help_exchange_cell.csb`
- `0x025DFB49`: `ui/alliance_help_list.csb`
- `0x025DFC12`: `ui/alliance_shop.csb`
- `0x02577813`: `ui/alliance_shop_cell.csb`
- `0x0257F4B3`: `ui/alliance_war.csb`
- `0x026005AD`: `ui/alliance_war_1.csb`
- `0x0259F6E4`: `ui/alliance_war_member.csb`
- `0x025F3261`: `ui/alliance_war_record.csb`
- `0x0258543A`: `ui/alliance_war_record_1.csb`

### Attack (3044 strings)

- `0x025AE3DB`: `/cc_2x2_white_image`
- `0x0286142A`: `12BossAttackUI`
- `0x02860ABF`: `13AlienAttackUI`
- `0x028708EE`: `14OverlordAttack`
- `0x02860AAD`: `15AlienAttackCell`
- `0x02718B43`: `15MapAttackEffect`
- `0x02864421`: `15MonsterAttackUI`
- `0x0279B025`: `17AutoAttackRebelUI`
- `0x0276E095`: `17BlackComingAttack`
- `0x02861BC9`: `17ChessBossAttackUI`
- `0x02816E40`: `17KnightGloryAttack`
- `0x0286440D`: `17MonsterAttackCell`
- `0x028A50BB`: `18CWarDamageRecoupUI`
- `0x028B6879`: `19Server_whitelistXml`
- `0x028A50A4`: `20CWarDamageRecoupCell`
- `0x0279A4FD`: `21AutoAttackRebelTeamUI`
- `0x0276F0D4`: `21BlackComingDamageRank`
- `0x027326C7`: `21TutFunc_DoArenaAttack`
- `0x0263CEE0`: `21WarDamageRecoupConfig`
- `0x02730D42`: `22TutFunc_DominionAttack`
- `0x0279B039`: `23AutoAttackRebelTeamCell`
- `0x026F5BC0`: `23CWarDamageRecoupManager`
- `0x02810826`: `23HeroLegendMonsterAttack`
- `0x02810840`: `23LegendDupAttackHeroCell`
- `0x028378FA`: `24LeagueWarRallyCellAttack`
- `0x0279DB08`: `25AutoHangupAttackMonsterUI`
- `0x0276F0EC`: `25BlackComingDamageRankCell`
- `0x028AF9E2`: `26KingdomBountyQuestAttackUI`
- `0x0280D766`: `27HeroCollectionMonsterAttack`
- `0x0276F108`: `28BlackComingDamageRankSubCell`
- `0x027B59CD`: `28EventPageGoodLuckScratchItem`
- `0x02734328`: `28TutFunc_OpenSesameAttackHero`
- `0x028AFF29`: `29KingdomBountyQuestAttackUICsd`
- `0x027B59AC`: `30EventPageGoodLuckScratchItemBg`
- `0x0280D784`: `31HeroCollectionDupAttackHeroCell`
- `0x025A3A41`: `ACTIVITY_OPENSESAME_ATTACK_MONSTER_RECV`
- `0x02589962`: `AlienLabyrintAttackResult`
- `0x025E4555`: `AnabasisAttackProtect`
- `0x02575532`: `Attack`
- `0x025620CD`: `AttackCost`
- `0x02620B9A`: `AttackHero`
- `0x026177CB`: `AttackIcon`
- `0x025EAA0F`: `AttackMonster`
- `0x025DDF24`: `AttackPower`
- `0x025EDE60`: `AttackReward`
- `0x025FD77A`: `Attack_Cost`
- `0x0257F5E6`: `Attack_Time`
- `0x025DE15E`: `AutoHangUpAttackMonster,No monster of this level found!!!`
- `0x02596615`: `CANNON_BATTLE_DAMAGE`
- `0x025A356D`: `CanAttack`
- `0x026177EF`: `CannonAttackTime`
- `0x02586454`: `CannonDamageMax`
- `0x025E784C`: `CannonDamageMin`
- `0x025B99F9`: `DamageIncrease`
- `0x0256B5F9`: `DefaultDamage`
- `0x025F7CF7`: `DoArenaAttack`
- `0x0262481F`: `DominionAttack`
- `0x025D3C8D`: `EnergyAttack`
- `0x0260A195`: `Extra non-whitespace after JSON value.`
- `0x025961CA`: `HitEffect`
- `0x025E0DAE`: `HitRange`
- `0x0279D81A`: `NSt6__ndk110__function6__baseIFN21AutoAttackRebelTeamUI15TeamCheckResultEiEEE`
- `0x026834E1`: `NSt6__ndk110__function6__baseIFvRK21CMSG_SYNC_DAMAGE_INFOEEE`
- `0x02683DED`: `NSt6__ndk110__function6__baseIFvRK22CMSG_DAMAGE_BUY_RETURNEEE`
- `0x02684700`: `NSt6__ndk110__function6__baseIFvRK23CMSG_DAMAGE_HELP_NOTIFYEEE`
- `0x02683AF4`: `NSt6__ndk110__function6__baseIFvRK23CMSG_DAMAGE_HELP_RETURNEEE`
- `0x02684400`: `NSt6__ndk110__function6__baseIFvRK24CMSG_DAMAGE_SHARE_RETURNEEE`
- `0x026840F1`: `NSt6__ndk110__function6__baseIFvRK27CMSG_DAMAGE_BUY_ITEM_RETURNEEE`
- `0x026837E4`: `NSt6__ndk110__function6__baseIFvRK28CMSG_DAMAGE_GIFT_INFO_RETURNEEE`
- `0x02653BEC`: `NSt6__ndk110__function6__baseIFvRK28CMSG_SYNC_CLANPK_ATTACK_INFOEEE`
- `0x02889937`: `NSt6__ndk110__function6__baseIFvRK30CMSG_ATTACK_SECRET_BOSS_RETURNEEE`
- `0x02655B39`: `NSt6__ndk110__function6__baseIFvRK30CMSG_CLANPK_THUNDER_ATTACK_ENDEEE`
- `0x0265581C`: `NSt6__ndk110__function6__baseIFvRK31CMSG_CLANPK_ATTACK_BUILDING_ENDEEE`
- `0x02654547`: `NSt6__ndk110__function6__baseIFvRK31CMSG_CLANPK_START_ATTACK_RETURNEEE`
- `0x026554F4`: `NSt6__ndk110__function6__baseIFvRK33CMSG_CLANPK_ATTACK_BUILDING_BEGINEEE`
- `0x02889C58`: `NSt6__ndk110__function6__baseIFvRK34CMSG_ATTACK_SECRET_BOSS_TEN_RETURNEEE`
- `0x02652C8F`: `NSt6__ndk110__function6__baseIFvRK34CMSG_CLANPK_SET_ATTACK_HERO_RETURNEEE`
- `0x02654B93`: `NSt6__ndk110__function6__baseIFvRK35CMSG_UPDATE_CLANPK_ATTACK_AMRY_INFOEEE`
- `0x026F6CFD`: `NSt6__ndk110__function6__baseIFvRK37CMSG_ACTIVITY_LOOP_BOSS_ATTACK_RETURNEEE`
- `0x026DA397`: `NSt6__ndk110__function6__baseIFvRK38CMSG_OPEN_SESAME_ATTACK_MONSTER_RETURNEEE`
- *...and 2964 more*

### Box (3643 strings)

- `0x02846498`: `10InputBoxUI`
- `0x02873173`: `10PVEBoxCell`
- `0x02873166`: `10PVEBoxInfo`
- `0x028B4499`: `11Chat_boxXml`
- `0x02686A24`: `13LogicLuckyBox`
- `0x02869613`: `14MessageBoxOnce`
- `0x0286971B`: `14MessageBoxText`
- `0x0286D2E5`: `14VipBoxDetailUI`
- `0x02868BD0`: `15CMessageBoxItem`
- `0x0289E646`: `15TaskBoxDetailUI`
- `0x0289F6BE`: `15TaskPlotBoxCell`
- `0x028B6BA2`: `15Treasure_boxXml`
- `0x027BDAE5`: `16SolomonChooseBox`
- `0x02868369`: `17CMessageBoxChoice`
- `0x027A2C0A`: `17CommonBoxDetailUI`
- `0x0286879F`: `18CMessageBoxConfirm`
- `0x0286837D`: `19CMessageBoxChoiceEx`
- `0x0283FF00`: `19LegionWarAwardBoxUI`
- `0x027CE321`: `19LunaShopBoxDetailUI`
- `0x0275E32C`: `19NavigationBoxInfoUI`
- `0x02796BDF`: `19RechargeBoxDetailUI`
- `0x0282FC7E`: `20CLeagueDonateBoxCell`
- `0x027EBB78`: `20GreedyGameConfirmBox`
- `0x02862DCD`: `20GuildTrapTroopTipbox`
- `0x027D5BBC`: `20SweetyActivityMsgBox`
- `0x027E79EB`: `21FriendUIPageInviteBox`
- `0x0283FEE8`: `21LegionWarAwardBoxCell`
- `0x028999CF`: `21LordEquipMatBoxInfoUI`
- `0x028698EB`: `21MsgBoxTodayNoPromptUI`
- `0x0275E314`: `21NavigationBoxInfoCell`
- `0x0289E67C`: `21TaskLoadingBarBoxCell`
- `0x0286834F`: `23CMessageBoxChoiceNormal`
- `0x02780C54`: `23ChatPresetTextListBoxUI`
- `0x027CBBAE`: `23EventOperationsLuckyBox`
- `0x028999B5`: `23LordEquipMatBoxInfoCell`
- `0x0286810B`: `23MessageBoxBuyAndUseItem`
- `0x027394B0`: `24ActivityMarkBoxPreviewUI`
- `0x0273AE8F`: `25ActivityLoadingBarBoxCell`
- `0x0274B5C2`: `27ActivityElementalAwardBoxUI`
- `0x02767040`: `27BuyGoodsInBatchesConfirmBox`
- `0x0274B5A2`: `29ActivityElementalAwardBoxCell`
- `0x027740C8`: `33ChampionshipPackDetailCellChatBox`
- `0x028B4718`: `8ComboXml`
- `0x0263C337`: `9BoxConfig`
- `0x027DDCCA`: `9EditBoxEx`
- `0x028BBBBB`: `BN7cocos2d13PUBoxColliderE`
- `0x028BC373`: `BN7cocos2d14CCPUBoxEmitterE`
- `0x025F73C6`: `BoxID`
- `0x025DA441`: `BoxId`
- `0x025CD036`: `BoxMoveL`
- `0x025E0B7E`: `BoxMoveR`
- `0x025685C0`: `BoxName`
- `0x025E765D`: `BoxOpen`
- `0x025685C8`: `BoxType`
- `0x0260084B`: `BoxUnopened`
- `0x02604395`: `CHAT_BOX_UNLOCK_SUCCESS`
- `0x025B3D69`: `Cannot APPEND without a mailbox.`
- `0x02621331`: `Cannot SELECT without a mailbox.`
- `0x0259CBCD`: `Championship_ChatBoxInfo`
- `0x025E47CA`: `Championship_SignBoxChanged`
- `0x025A6830`: `ChatBox`
- `0x025E1970`: `CheckBox`
- `0x025F4D10`: `CheckBoxReader`
- `0x025E871A`: `FONTBOUNDINGBOX`
- `0x0106CCAD`: `FT_Glyph_Get_CBox`
- `0x010AC5D6`: `FT_Outline_Get_CBox`
- `0x02601CD6`: `FontBBox`
- `0x02611A71`: `Image_Box`
- `0x01052932`: `Java_org_cocos2dx_lib_Cocos2dxEditBoxHelper_editBoxEditingChanged`
- `0x01052778`: `Java_org_cocos2dx_lib_Cocos2dxEditBoxHelper_editBoxEditingDidBegin`
- `0x01052974`: `Java_org_cocos2dx_lib_Cocos2dxEditBoxHelper_editBoxEditingDidEnd`
- `0x025CA3B5`: `LUCKYBOX_ATTRIBUTE`
- `0x025B6E8F`: `LUCKYBOX_NEW_SERVER_RETURN`
- `0x026112AF`: `LUCKYBOX_RETURN`
- `0x0261129F`: `LUCKYBOX_UPDATE`
- `0x025A3504`: `LordEquipbox`
- `0x0262A49C`: `LordGembox`
- `0x0258FEF1`: `LordMatbox`
- `0x025A9C59`: `LordSteelbox`
- `0x0260D911`: `Mailbox UIDVALIDITY has changed`
- *...and 3563 more*

### Build (10186 strings)

- `0x02724870`: `11CRuinsBuild`
- `0x0272487E`: `11IRuinsBuild`
- `0x02771618`: `12BuildingSkin`
- `0x02727126`: `14CBuildingModel`
- `0x0288C770`: `14ScienceBuildLv`
- `0x027645FA`: `15AutoJoinBuildup`
- `0x02689B03`: `15BuildingLvUpTip`
- `0x0278290B`: `15CBuildingBuyRes`
- `0x0276FEDF`: `15CBuildingInfoUI`
- `0x02783DAA`: `15CBuildingUseRes`
- `0x0272488C`: `15CRuinsBuildMine`
- `0x0272A30C`: `15TutCond_BuildLV`
- `0x0277164D`: `16BuildingSkinCell`
- `0x028B4378`: `16Building_baseXml`
- `0x027840C2`: `16CNewBuildingCell`
- `0x02745682`: `16ClanWarBuildItem`
- `0x028B6890`: `16Set_buildskinXml`
- `0x0272AC99`: `16TutCond_BuildNum`
- `0x028B4363`: `17Build_removecdXml`
- `0x02785FE0`: `17BuildingCellWiget`
- `0x02721D4F`: `17BuildingNameWiget`
- `0x027855D4`: `17CBuildingBuffCell`
- `0x02782B6E`: `17CBuildingCitySkin`
- `0x0276F9EC`: `17CBuildingInfoList`
- `0x026D2250`: `17CMainCityBuilding`
- `0x026F6F58`: `17LogicLoopBuilding`
- `0x0272C6E7`: `17TutCond_BuildBusy`
- `0x028B438C`: `18Building_weightXml`
- `0x027855E8`: `18CBuildingSkillCell`
- `0x02785FF4`: `18CNewBuildingDetail`
- `0x0284DA10`: `18DominionBuildingUI`
- `0x0272B027`: `18TutCond_BuildFirst`
- `0x027645E4`: `19AutoJoinBuildupCell`
- `0x02689C03`: `19BuildingSkinManager`
- `0x02783D7E`: `19BuildingUseResCell1`
- `0x02783D94`: `19BuildingUseResCell2`
- `0x02786009`: `19CBaseBuildingDetail`
- `0x028B10B5`: `19CBattleMapBuildCell`
- `0x0263C342`: `19CBuildingAreaConfig`
- `0x0276F913`: `19CBuildingDetailCell`
- `0x0276F9D6`: `19CBuildingDetailInfo`
- `0x028B4559`: `19Clanpk_build_defXml`
- `0x028B4588`: `19Clanpk_build_posXml`
- `0x0278407F`: `19ListNewBuildingCell`
- `0x02784095`: `19PageNewBuildingCell`
- `0x027BD0F7`: `19RebuildOasisBoxCell`
- `0x026E056A`: `19RebuildOasisManager`
- `0x0272BB67`: `19TutCond_BuildsLevel`
- `0x0272DB6E`: `19TutFunc_BuildingSay`
- `0x0272DAEC`: `19TutFunc_UnlockBuild`
- `0x02772A4D`: `20BuildingThemeBufCell`
- `0x026D1AF2`: `20CBuildingDataManager`
- `0x027840AB`: `20CCreateNewBuildingUI`
- `0x027855A1`: `20CHonorBuildingDetail`
- `0x028B4570`: `20Clanpk_build_itemXml`
- `0x0284D9F9`: `20DominionBuildingCell`
- `0x027BD0C8`: `20RebuildOasisTaskCell`
- `0x028B646E`: `20Rebuilding_oasiseXml`
- `0x02689AEB`: `21BuildingBuyResManager`
- `0x02771627`: `21BuildingSkinTitleCell`
- `0x0276F929`: `21CBuildingDetailListUI`
- `0x02721D63`: `21CityBuildingNameWiget`
- `0x02743AD0`: `21ClanWarBuildAttribute`
- `0x02743B48`: `21ClanWarBuildDefenceUI`
- `0x027457A2`: `21ClanWarBuildUpgradeUI`
- `0x028B459F`: `21Clanpk_build_spaceXml`
- `0x0284E848`: `21DominionBuildHeroCell`
- `0x0284D868`: `21DominionBuildingDesUI`
- `0x0284ED08`: `21DominionBuildingVewUI`
- `0x027BD0DF`: `21EventPageRebuildOasis`
- `0x02720C0C`: `21MainCityBuildingGuide`
- `0x02682E54`: `22AutoJoinBuildupManager`
- `0x0263C358`: `22CBuildingLevelUpConfig`
- `0x02785611`: `22CHonorBuildingBuffCell`
- `0x0278562A`: `22CHonorBuildingCondCell`
- `0x0286FD05`: `22CollectionBuildingInfo`
- `0x027DD940`: `22FortressWarResBuilding`
- `0x02843FB1`: `22LegionWarRuleBuildCell`
- `0x0275A93C`: `22LostLandBuildingInfoUI`
- `0x028B58CF`: `22Lost_alliance_buildXml`
- *...and 10106 more*

### Chest (1 strings)

- `0x006AEF9C`: `_ZN11CBuffEffect21clearCacheStringValueEv`

### Gacha (2425 strings)

- `0x02792E3C`: `10HeroDrawUI`
- `0x028B4789`: `13Crest_drawXml`
- `0x027901A4`: `13DrawOneEffect`
- `0x02790664`: `13DrawTenEffect`
- `0x02790BDC`: `13HeroDrawNewUI`
- `0x02792E49`: `15DrawOneEffectUI`
- `0x02792E5B`: `15DrawTenEffectUI`
- `0x027332BC`: `16TutFunc_HeroDraw`
- `0x02790C04`: `17DrawEffectPosNode`
- `0x026A1954`: `17LogicLuckyLottery`
- `0x02731AF8`: `17TutFunc_DoTenDraw`
- `0x027929EC`: `18HeroDrawSelectHero`
- `0x02697CE8`: `18LogicDoubleLottery`
- `0x028B5093`: `19Herolottery_baseXml`
- `0x028B50AA`: `19Herolottery_dropXml`
- `0x027F3A34`: `19LuckyLotteryBingoUI`
- `0x027189FB`: `19NodeTreeOrderDrawer`
- `0x028B50C1`: `20Herolottery_groupXml`
- `0x027F3C9B`: `20LuckyLotteryGamePage`
- `0x028B4963`: `21Doublelottery_baseXml`
- `0x028B497C`: `21Doublelottery_dropXml`
- `0x028B4995`: `22Doublelottery_groupXml`
- `0x02792A01`: `22HeroDrawSelectHeroCell`
- `0x027923C2`: `22HeroDrawShowRecordCell`
- `0x027F3B18`: `23LuckyLotteryBuyResultUI`
- `0x027F4465`: `23LuckyLotteryGamePageCsd`
- `0x027A614D`: `24EventPageDoubleLotteryUI`
- `0x027F3B89`: `24LuckyLotteryDelayRequest`
- `0x027F3B32`: `25LuckyLotteryBuyResultCell`
- `0x027A5FB2`: `26EventPageDoubleLotteryRank`
- `0x027F3B4E`: `26LuckyLotteryBuyResultUICsd`
- `0x027F3C5D`: `26LuckyLotteryCategoryRowCsd`
- `0x027A821B`: `27EventPageDoubleLotteryUICsd`
- `0x027F3B6B`: `27LuckyLotteryCategoryRowItem`
- `0x027F44A5`: `27LuckyLotteryHistoryRecordUI`
- `0x027F387D`: `27LuckyLotteryWinnerBriefItem`
- `0x027F3AF9`: `28LuckyLotteryBuyResultCellCsd`
- `0x027F389B`: `28LuckyLotteryWinnerWatingItem`
- `0x027A612D`: `29EventPageDoubleLotteryRankCsd`
- `0x027A60E8`: `30EventPageDoubleLotteryRankCell`
- `0x027F3C7A`: `30LuckyLotteryCategoryRowItemCsd`
- `0x027F48D3`: `30LuckyLotteryHistoryRecordUICsd`
- `0x027F491E`: `30LuckyLotteryWinnerBriefItemCsd`
- `0x027A5E7B`: `31EventPageDoubleLotteryLevelCell`
- `0x027F3835`: `31LuckyLotteryHistoryMyRecordItem`
- `0x027F493F`: `31LuckyLotteryWinnerWatingItemCsd`
- `0x027A6109`: `33EventPageDoubleLotteryRankCellCsd`
- `0x027A5F8D`: `34EventPageDoubleLotteryLevelCellCsd`
- `0x027F447F`: `35LuckyLotteryHistoryMyRecordyItemCsd`
- `0x027F3857`: `35LuckyLotteryHistoryWinnerRecordItem`
- `0x027F48F4`: `39LuckyLotteryHistoryWinnerRecordyItemCsd`
- `0x025960EB`: `BadgeDraw`
- `0x02604A3A`: `DoTenDraw`
- `0x025D09C8`: `DrawUnlockLv`
- `0x02575598`: `Draw_GoldTen_Limit`
- `0x025D09A1`: `Draw_Gold_Limit`
- `0x025BD704`: `Guide_Pet_Summon`
- `0x025896D3`: `HeroDraw`
- `0x025EA9C7`: `HeroDrawTimesLimit`
- `0x0258ACDB`: `HeroDraw_noTip_%lld`
- `0x025BE7E9`: `HeroDraw_noTip_money_%lld`
- `0x025AB475`: `HeroDraw_time_%lld`
- `0x025C4B2D`: `HeroDraw_time_money_%lld`
- `0x025F402A`: `IconLottery`
- `0x025FA6C6`: `IconLotteryEffect`
- `0x025DA593`: `Invitedrawnum`
- `0x025B3886`: `Invitelottery`
- `0x0259664E`: `LuckyLotteryWinEffFlag_%lld`
- `0x028C2E67`: `N7cocos2d8DrawNodeE`
- `0x02792FE3`: `NSt6__ndk110__function6__baseIFvRK14ClientDrawInfoEEE`
- `0x026A1AFC`: `NSt6__ndk110__function6__baseIFvRK17CMSG_LOTTERY_INFOEEE`
- `0x026A1DE4`: `NSt6__ndk110__function6__baseIFvRK27CMSG_LOTTERY_BETTING_RETURNEEE`
- `0x026A243E`: `NSt6__ndk110__function6__baseIFvRK30CMSG_LOTTERY_OPEN_AWARD_RETURNEEE`
- `0x02697EBD`: `NSt6__ndk110__function6__baseIFvRK31CMSG_DOUBLE_LOTTERY_CONFIG_INFOEEE`
- `0x026981ED`: `NSt6__ndk110__function6__baseIFvRK31CMSG_DOUBLE_LOTTERY_PLAY_RETURNEEE`
- `0x026EC29A`: `NSt6__ndk110__function6__baseIFvRK31CMSG_INVITE_DRAW_LOTTERY_RETURNEEE`
- `0x026A2109`: `NSt6__ndk110__function6__baseIFvRK34CMSG_LOTTERY_CUR_STAGE_INFO_RETURNEEE`
- `0x02698529`: `NSt6__ndk110__function6__baseIFvRK35CMSG_DOUBLE_LOTTERY_SHOP_BUY_RETURNEEE`
- `0x026A277B`: `NSt6__ndk110__function6__baseIFvRK38CMSG_LOTTERY_OPEN_AWARD_HISTORY_RETURNEEE`
- `0x027930F8`: `NSt6__ndk110__function6__funcINS_6__bindIM10HeroDrawUIFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- *...and 2345 more*

### Gather (38 strings)

- `0x02887A63`: `NSt6__ndk110__function6__funcIZN12CRuinsMineUI20showCollectingStatusEvE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x02887AC8`: `ZN12CRuinsMineUI20showCollectingStatusEvE3$_0`
- `0x0068538A`: `_ZN10AFAppEvent10GatherOnceEv`
- `0x006849CB`: `_ZN10AFAppEvent15GatherTimber50kEv`
- `0x00A0D7FE`: `_ZN10KingdomMap17isInCollectingNowEv`
- `0x00A0D7D4`: `_ZN10KingdomMap21isSelfCollectingInPosEtt`
- `0x00E123CE`: `_ZN12CRuinsMineUI20showCollectingStatusEv`
- `0x00A1DD52`: `_ZN20CMapTimeProgressInfo26_updateCollectingDispStateEv`
- `0x00A44F33`: `_ZN21MainCityBuildingGuide13getHarvestNumEv`
- `0x00F8346B`: `_ZN25SMSG_ADD_COLLECT_RESOURCE7getDataEPKc`
- `0x00F83438`: `_ZN25SMSG_ADD_COLLECT_RESOURCE8packDataER8CIStream`
- `0x00F838F1`: `_ZN25SMSG_ADD_COLLECT_RESOURCEC1Ev`
- `0x00F83415`: `_ZN25SMSG_ADD_COLLECT_RESOURCEC2Ev`
- `0x00F834F2`: `_ZN28SMSG_UPDATE_COLLECT_RESOURCE7getDataEPKc`
- `0x00F834BC`: `_ZN28SMSG_UPDATE_COLLECT_RESOURCE8packDataER8CIStream`
- `0x00F83914`: `_ZN28SMSG_UPDATE_COLLECT_RESOURCEC1Ev`
- `0x00F83496`: `_ZN28SMSG_UPDATE_COLLECT_RESOURCEC2Ev`
- `0x0108C41D`: `_ZN7cocos2d13Configuration13gatherGPUInfoEv`
- `0x007C2E21`: `_ZNK17CMainCityBuilding13getHarvestNumEv`
- `0x007C2F24`: `_ZNK17CMainCityBuilding18getHarvestCapacityEv`
- `0x00828B2D`: `_ZNK17ChatHornorManager20gatherHornorShowInfoE10EHonorType`
- `0x00828DE2`: `_ZNK17ChatHornorManager20gatherHornorShowInfoEi`
- `0x007C2F75`: `_ZNK20LostLandBuildingMeta20getProduceHarvestNumEv`
- `0x010F322C`: `_ZNSt6__ndk111__money_getIcE13__gather_infoEbRKNS_6localeERNS_10money_base7patternERcS8_RNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEESF_SF_SF_Ri`
- `0x010F34B0`: `_ZNSt6__ndk111__money_getIwE13__gather_infoEbRKNS_6localeERNS_10money_base7patternERwS8_RNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEERNS9_IwNSA_IwEENSC_IwEEEESJ_SJ_Ri`
- `0x010F36A8`: `_ZNSt6__ndk111__money_putIcE13__gather_infoEbbRKNS_6localeERNS_10money_base7patternERcS8_RNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEESF_SF_Ri`
- `0x010F38E3`: `_ZNSt6__ndk111__money_putIwE13__gather_infoEbbRKNS_6localeERNS_10money_base7patternERwS8_RNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEERNS9_IwNSA_IwEENSC_IwEEEESJ_Ri`
- `0x010C5B8F`: `ecp_nistz256_gather_w5`
- `0x010C5BBE`: `ecp_nistz256_gather_w7`
- `0x02584CC8`: `elemental_war_zone_gather_score1`
- `0x02591D69`: `elemental_war_zone_gather_score2`
- `0x02575446`: `gather_battle`
- `0x025FD629`: `gather_once`
- `0x0258FD01`: `gather_timber50k`
- `0x0256855F`: `harvest_num`
- `0x0259C79A`: `harvest_type`
- `0x025715A1`: `m_pLayoutCollecting`
- `0x0259168F`: `m_pPanelGather`

### Gift (7426 strings)

- `0x0259CA79`: `%lld_GiveGift.tmp`
- `0x02627D84`: `/sys/devices/system/cpu/present`
- `0x027F8ED7`: `11CGiftPackUI`
- `0x027F8EC8`: `12GiftPackCell`
- `0x028B68B7`: `12Shop_giftXml`
- `0x027F58C1`: `13CGiftBuyOneUI`
- `0x0281F459`: `13CLeagueGiftUI`
- `0x02754D54`: `13KingdomGiftUI`
- `0x028B5BCF`: `13Lucky_giftXml`
- `0x027F6594`: `14CGiftPack3thUI`
- `0x027F87B5`: `14CGiftPackPopUI`
- `0x028B4CCF`: `14Friend_giftXml`
- `0x02751F9E`: `14GiveGiftShopUI`
- `0x028B5545`: `14League_giftXml`
- `0x028B3C1F`: `15Active_giftsXml`
- `0x0279FDBF`: `15BargainGiftHelp`
- `0x027A1240`: `15BargainGiftShop`
- `0x027F5E8B`: `15CGiftBuySuccess`
- `0x0263C5AD`: `15CGiftPackConfig`
- `0x0265FFB2`: `15GiveGiftManager`
- `0x026A592D`: `15GoldGiftManager`
- `0x028B5246`: `15Kingdom_giftXml`
- `0x028B6C57`: `15Trigger_giftXml`
- `0x027F5418`: `16CGiftBuyOneTipUI`
- `0x026A4D4B`: `16CGiftPackManager`
- `0x028B4B78`: `16Everyday_giftXml`
- `0x02649295`: `16LogicActiveGifts`
- `0x028B6E01`: `16Wheel_of_giftXml`
- `0x027F6892`: `17CGiftPackCastleUI`
- `0x0281F414`: `17CLeagueGiftUICell`
- `0x027C4027`: `17EventSevenDayGift`
- `0x027C7189`: `17GeneralShopGiftUI`
- `0x026878D9`: `17LogicSevenDayGift`
- `0x027A0671`: `18BargainGiftHelpCsd`
- `0x027A1A12`: `18BargainGiftShopCsd`
- `0x026A4832`: `18CGiftBuyOneManager`
- `0x028B4BC4`: `18Extra_gift_packXml`
- `0x027C719D`: `18GeneralShopGiftRow`
- `0x028B4DCE`: `18Gift_invaluableXml`
- `0x02751C36`: `18GiveGiftPersonCell`
- `0x0280C9F4`: `18HeroCollectionGift`
- `0x02663AFE`: `18KingdomGiftManager`
- `0x02880896`: `18ReturnBackGiftPack`
- `0x027A0BF4`: `19BargainGiftPackPage`
- `0x02683195`: `19CBargainGiftManager`
- `0x027A3CBB`: `19CDailySmallGiftCell`
- `0x027F7919`: `19CGiftPackDetailCell`
- `0x027F79D5`: `19CGiftPackDetailPage`
- `0x027C71B2`: `19GeneralShopGiftItem`
- `0x02751C0B`: `19GiveGiftPackageCell`
- `0x028B3C32`: `20Active_gifts_skinXml`
- `0x028B3C4A`: `20Active_gifts_taskXml`
- `0x027F6753`: `20CGiftPackBuyFaildTip`
- `0x027F5E9D`: `20CGiftPackBuyItemCell`
- `0x0281F428`: `20CLeagueGiftUIBoxCell`
- `0x027A332B`: `20CustomGiftChooseItem`
- `0x027AD948`: `20EventPageActiveGifts`
- `0x027A1A27`: `20EventPageBargainGift`
- `0x028B4B8C`: `20Everyday_gift_newXml`
- `0x0265E107`: `20ExtraGiftPackManager`
- `0x028B6617`: `20Reduce_price_giftXml`
- `0x028B3DB7`: `21Activity_gift_packXml`
- `0x026A4998`: `21CDailyFreeGiftManager`
- `0x0265795B`: `21CustomGiftPackManager`
- `0x027C400F`: `21EventSevenDayGiftCell`
- `0x027516AB`: `21GiveGiftGiveHistoryUI`
- `0x0287F6FC`: `21ReturnBackNewGiftPack`
- `0x028A973C`: `21WeeklyCycleGiftShopUI`
- `0x027A0686`: `22BargainGiftHistoryList`
- `0x027A1223`: `22BargainGiftPackPageCsd`
- `0x026928D6`: `22CDailySmallGiftManager`
- `0x027A4C8B`: `22CDailySmallGiftNewCell`
- `0x027F713A`: `22CGiftPackDailyFreeGift`
- `0x027F81B0`: `22CGiftPackPopPageViewUI`
- `0x027F6879`: `22CGiftShopCastleTabCell`
- `0x02750BF5`: `22GiveGiftChoicePersonUI`
- `0x0280C9DB`: `22HeroCollectionGiftCell`
- `0x028A93B7`: `22WeeklyCycleGiftShopCsd`
- `0x028A9707`: `22WeeklyCycleGiftShopRow`
- `0x028B6E15`: `22Wheel_of_gift_cycleXml`
- *...and 7346 more*

### Heal (236 strings)

- `0x0257905D`: `At marker 0x%02x, recovery action %d`
- `0x010C0378`: `BN_CTX_secure_new`
- `0x010C0363`: `BN_CTX_secure_new_ex`
- `0x010C09A3`: `BN_secure_new`
- `0x010CEAA7`: `CRYPTO_secure_actual_size`
- `0x010CEA7C`: `CRYPTO_secure_allocated`
- `0x010C0975`: `CRYPTO_secure_clear_free`
- `0x010B19F6`: `CRYPTO_secure_free`
- `0x010C12B8`: `CRYPTO_secure_malloc`
- `0x010CDFE0`: `CRYPTO_secure_malloc_done`
- `0x010CEA1A`: `CRYPTO_secure_malloc_init`
- `0x010CEA5B`: `CRYPTO_secure_malloc_initialized`
- `0x010CEA94`: `CRYPTO_secure_used`
- `0x010B297C`: `CRYPTO_secure_zalloc`
- `0x025C9FC8`: `CureFairyTime`
- `0x025759EE`: `NEWSOLDIER_CURE_FINISH`
- `0x026ACCD8`: `NSt6__ndk110__function6__baseIFvRK29CMSG_SOLDIER_CURE_OVER_RETURNEEE`
- `0x026AC309`: `NSt6__ndk110__function6__baseIFvRK31CMSG_SOLDIER_NORMAL_CURE_RETURNEEE`
- `0x026AC639`: `NSt6__ndk110__function6__baseIFvRK35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNEEE`
- `0x026AC98E`: `NSt6__ndk110__function6__baseIFvRK42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNEEE`
- `0x026ACC36`: `NSt6__ndk110__function6__funcINS_6__bindIM15LogicNewSoldierFvRK29CMSG_SOLDIER_CURE_OVER_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AC265`: `NSt6__ndk110__function6__funcINS_6__bindIM15LogicNewSoldierFvRK31CMSG_SOLDIER_NORMAL_CURE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AC591`: `NSt6__ndk110__function6__funcINS_6__bindIM15LogicNewSoldierFvRK35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AC8DF`: `NSt6__ndk110__function6__funcINS_6__bindIM15LogicNewSoldierFvRK42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026ACB22`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI29CMSG_SOLDIER_CURE_OVER_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026AC14D`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI31CMSG_SOLDIER_NORMAL_CURE_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026AC471`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026AC7B1`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026ACDE5`: `NSt6__ndk115binary_functionIP15LogicNewSoldierRK29CMSG_SOLDIER_CURE_OVER_RETURNvEE`
- `0x026AC41C`: `NSt6__ndk115binary_functionIP15LogicNewSoldierRK31CMSG_SOLDIER_NORMAL_CURE_RETURNvEE`
- `0x026AC758`: `NSt6__ndk115binary_functionIP15LogicNewSoldierRK35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNvEE`
- `0x026ACAC2`: `NSt6__ndk115binary_functionIP15LogicNewSoldierRK42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNvEE`
- `0x026ACD8D`: `NSt6__ndk118__weak_result_typeIM15LogicNewSoldierFvRK29CMSG_SOLDIER_CURE_OVER_RETURNEEE`
- `0x026AC3C2`: `NSt6__ndk118__weak_result_typeIM15LogicNewSoldierFvRK31CMSG_SOLDIER_NORMAL_CURE_RETURNEEE`
- `0x026AC6FA`: `NSt6__ndk118__weak_result_typeIM15LogicNewSoldierFvRK35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNEEE`
- `0x026ACA5D`: `NSt6__ndk118__weak_result_typeIM15LogicNewSoldierFvRK42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNEEE`
- `0x026ACD1D`: `NSt6__ndk16__bindIM15LogicNewSoldierFvRK29CMSG_SOLDIER_CURE_OVER_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x026AC350`: `NSt6__ndk16__bindIM15LogicNewSoldierFvRK31CMSG_SOLDIER_NORMAL_CURE_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x026AC684`: `NSt6__ndk16__bindIM15LogicNewSoldierFvRK35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x026AC9E0`: `NSt6__ndk16__bindIM15LogicNewSoldierFvRK42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x02595065`: `Secure Electronic Transactions`
- `0x0262C76F`: `Text_Health`
- `0x026ACBC5`: `ZN14MessageSubject16registerListenerI29CMSG_SOLDIER_CURE_OVER_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x026AC1F2`: `ZN14MessageSubject16registerListenerI31CMSG_SOLDIER_NORMAL_CURE_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x026AC51A`: `ZN14MessageSubject16registerListenerI35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x026AC861`: `ZN14MessageSubject16registerListenerI42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x00982308`: `_ZN10PetManager10getHuntNumER12ObscuredTypeIiE`
- `0x009822A8`: `_ZN10PetManager19setArrowItemRealNumE12ObscuredTypeIiEb`
- `0x00981969`: `_ZN10PetManager23requestPetHuntResultNewEj12ObscuredTypeIiES1_`
- `0x008BE872`: `_ZN14MessageSubject16registerListenerI29CMSG_SOLDIER_CURE_OVER_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEE`
- `0x008BE3FB`: `_ZN14MessageSubject16registerListenerI31CMSG_SOLDIER_NORMAL_CURE_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEE`
- `0x008BE572`: `_ZN14MessageSubject16registerListenerI35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEE`
- `0x008BE702`: `_ZN14MessageSubject16registerListenerI42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEE`
- `0x008C04CB`: `_ZN15LogicNewSoldier11getCureInfoEi`
- `0x008C04A4`: `_ZN15LogicNewSoldier14getAllCureInfoEv`
- `0x008C0403`: `_ZN15LogicNewSoldier14getAllCureTimeEv`
- `0x008C03B2`: `_ZN15LogicNewSoldier14getCureEndTimeEv`
- `0x008BEC74`: `_ZN15LogicNewSoldier14setCureEndTimeElb`
- `0x008C03D9`: `_ZN15LogicNewSoldier17getRemainCureTimeEv`
- `0x008C0269`: `_ZN15LogicNewSoldier22requestSoldierCureOverEv`
- `0x008BFF70`: `_ZN15LogicNewSoldier22requestSoldierGoldCureERKNSt6__ndk13mapIiiNS0_4lessIiEENS0_9allocatorINS0_4pairIKiiEEEEEE`
- `0x008BFE6F`: `_ZN15LogicNewSoldier24requestSoldierNormalCureERKNSt6__ndk13mapIiiNS0_4lessIiEENS0_9allocatorINS0_4pairIKiiEEEEEEb`
- `0x008BF671`: `_ZN15LogicNewSoldier24showSoldierCureFinishTipEi`
- `0x008BE81F`: `_ZN15LogicNewSoldier26onSOLDIER_CURE_OVER_RETURNERK29CMSG_SOLDIER_CURE_OVER_RETURN`
- `0x008C0040`: `_ZN15LogicNewSoldier27requestSoldierGoldSpeedCureEv`
- `0x008C00E0`: `_ZN15LogicNewSoldier27requestSoldierItemSpeedCureEii`
- `0x008BE3A4`: `_ZN15LogicNewSoldier28onSOLDIER_NORMAL_CURE_RETURNERK31CMSG_SOLDIER_NORMAL_CURE_RETURN`
- `0x008BE513`: `_ZN15LogicNewSoldier32onSOLDIER_ITEM_SPEED_CURE_RETURNERK35CMSG_SOLDIER_ITEM_SPEED_CURE_RETURN`
- `0x008BE695`: `_ZN15LogicNewSoldier39onSOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURNERK42CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_RETURN`
- `0x008BF310`: `_ZN15SoldierCureInfoC1Ev`
- `0x00FBA09F`: `_ZN15SoldierCureInfoC2Ev`
- `0x0076C0CE`: `_ZN17SObscureCryptoKey8InstanceEv`
- `0x0097F768`: `_ZN17SObscureCryptoKeyC1Ev`
- `0x0097F783`: `_ZN17SObscureCryptoKeyC2Ev`
- `0x0069E4F9`: `_ZN22TroopBattleDataManager18_calculateCureArmyERNSt6__ndk13mapIi9SArmyMetaNS0_4lessIiEENS0_9allocatorINS0_4pairIKiS2_EEEEEERNS1_Ii10SRoundDataS4_NS5_INS6_IS7_SC_EEEEEE`
- `0x007DCC4C`: `_ZN24COverlordActivityManager12setSeasonCurEi`
- `0x00AC293C`: `_ZN28ActivityElementalBuffApplyUI17_onJumpToHospitalEv`
- `0x008CE719`: `_ZN28CMSG_SYNC_ITEM_RECOVERY_TIME7getDataEPKc`
- `0x00F798A2`: `_ZN28CMSG_SYNC_ITEM_RECOVERY_TIME8packDataER8CIStream`
- `0x008CE6F3`: `_ZN28CMSG_SYNC_ITEM_RECOVERY_TIMEC1Ev`
- *...and 156 more*

### March (1856 strings)

- `0x02718A75`: `11CMarchModel`
- `0x02864100`: `11MarchInfoUI`
- `0x02864BB2`: `12CMarchBackUI`
- `0x028640F0`: `13MarchInfoCell`
- `0x02707417`: `14MenuInfo_March`
- `0x02864CB0`: `15CMarchSpeedUpUI`
- `0x02718A83`: `15CMarchTentModel`
- `0x0263C371`: `16CArmyMarchFacade`
- `0x027073B3`: `18MenuInfo_MarchLine`
- `0x02864CC2`: `19CMarchSpeedUpItemUI`
- `0x026B0801`: `19ILocalMarchListener`
- `0x028B5F53`: `19Novice_map_marchXml`
- `0x026B07EA`: `20KBVirtualMarchAction`
- `0x0271C7ED`: `20MarchSpeedupItemCell`
- `0x02718BE5`: `21MarchModelAttackParam`
- `0x0271C7D5`: `21MarchSpeedupShutcutUI`
- `0x02732D8C`: `22TutFunc_NoviceMapMarch`
- `0x0273246A`: `24TutFunc_StorySetMapMarch`
- `0x028B1079`: `25CWorldTrendTradeMarchCell`
- `0x028B0496`: `25KingdomBountyQuestMarchUI`
- `0x02733BF2`: `25TutFunc_FocusTradingMarch`
- `0x02732485`: `27TutFunc_StoryFollowMapMarch`
- `0x028B08BB`: `28KingdomBountyQuestMarchUICsd`
- `0x02732DDD`: `28TutFunc_NoviceMapRemoveMarch`
- `0x02732E1D`: `31TutFunc_NoviceMapSetMarchStatus`
- `0x025EB12D`: `CMSG_SYNC_MARCH_NEW: %d`
- `0x025F7D17`: `FocusTradingMarch`
- `0x02589DD0`: `MarchModel_Delay_Call_onArrived`
- `0x02620D99`: `MarchTime`
- `0x0270281A`: `NSt6__ndk110__function6__baseIFbP11CMarchModelEEE`
- `0x0270218A`: `NSt6__ndk110__function6__baseIFbR14ModelMarchInfoEEE`
- `0x02715D96`: `NSt6__ndk110__function6__baseIFbR15SLocalMarchInfoEEE`
- `0x0270EF0F`: `NSt6__ndk110__function6__baseIFvP11CMarchModelEEE`
- `0x0271D913`: `NSt6__ndk110__function6__baseIFvRK19CMSG_SYNC_MARCH_NEWEEE`
- `0x026FE61B`: `NSt6__ndk110__function6__baseIFvRK21CMSG_NOTIFY_MARCH_ENDEEE`
- `0x0270082D`: `NSt6__ndk110__function6__baseIFvRK21CMSG_SYNC_TRADE_MARCHEEE`
- `0x026FD3E7`: `NSt6__ndk110__function6__baseIFvRK22CMSG_SYNC_REMOVE_MARCHEEE`
- `0x026FE063`: `NSt6__ndk110__function6__baseIFvRK23CMSG_NOTIFY_OWNER_MARCHEEE`
- `0x028642BD`: `NSt6__ndk110__function6__baseIFvRK28CMSG_SELF_MARCH_QUEUE_RETURNEEE`
- `0x026C1857`: `NSt6__ndk110__function6__baseIFvRK29CMSG_START_TRADE_MARCH_RETURNEEE`
- `0x0271B928`: `NSt6__ndk110__function6__baseIFvRK29CMSG_SYNC_MARCH_ARMY_INFO_NEWEEE`
- `0x026C1223`: `NSt6__ndk110__function6__baseIFvRK30CMSG_GET_DOMINION_MARCH_RETURNEEE`
- `0x0271803F`: `NSt6__ndk110__function6__baseIFvRK32CMSG_CASTLE_PET_SKILL_SLOW_MARCHEEE`
- `0x02700425`: `NSt6__ndk110__function6__baseIFvRK37CMSG_INVESTIGATION_TRADE_MARCH_RETURNEEE`
- `0x026FE586`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFvRK21CMSG_NOTIFY_MARCH_ENDEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02700798`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFvRK21CMSG_SYNC_TRADE_MARCHEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026FD351`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFvRK22CMSG_SYNC_REMOVE_MARCHEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026FDFCC`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFvRK23CMSG_NOTIFY_OWNER_MARCHEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02700380`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFvRK37CMSG_INVESTIGATION_TRADE_MARCH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0270A167`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFviiimRKNS_4listIiNS_9allocatorIiEEEEiimiEJPS3_10EMarchTypeRKiSF_RKmRKNS_12placeholders4__phILi1EEERKNSJ_ILi2EEE16ESceneObjectTypeiiEEENS5_ISR_EEFvS9_iEEE`
- `0x0270EFE9`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFviiimRKNS_4listIiNS_9allocatorIiEEEEiimiEJPS3_10EMarchTypeRKtSF_RKmRKNS_12placeholders4__phILi1EEERKNSJ_ILi2EEE16ESceneObjectTypeiRiEEENS5_ISS_EEFvS9_iEEE`
- `0x0270CFFC`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFviiimRKNS_4listIiNS_9allocatorIiEEEEiimiEJPS3_10EMarchTypeRiSE_RKmRKNS_12placeholders4__phILi1EEERKNSI_ILi2EEE16ESceneObjectTypeSG_iEEENS5_ISQ_EEFvS9_iEEE`
- `0x027102BE`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFviiimRKNS_4listIiNS_9allocatorIiEEEEiimiEJPS3_10EMarchTypeRiSE_RKmRKNS_12placeholders4__phILi1EEERKNSI_ILi2EEE16ESceneObjectTypeiiEEENS5_ISQ_EEFvS9_iEEE`
- `0x02816F57`: `NSt6__ndk110__function6__funcINS_6__bindIM10KingdomMapFviiimRKNS_4listIiNS_9allocatorIiEEEEiimiEJPS3_10EMarchTypeRiSE_RmRKNS_12placeholders4__phILi1EEERKNSH_ILi2EEE16ESceneObjectTypeSF_SE_EEENS5_ISP_EEFvS9_iEEE`
- `0x0271A7DF`: `NSt6__ndk110__function6__funcINS_6__bindIM11CMarchModelFvRK19CMSG_SYNC_NAME_INFOEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0271AAB3`: `NSt6__ndk110__function6__funcINS_6__bindIM11CMarchModelFvRK29CMSG_BATTLE_LEADERID_RESPONSEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02864220`: `NSt6__ndk110__function6__funcINS_6__bindIM11MarchInfoUIFvRK28CMSG_SELF_MARCH_QUEUE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02864BC1`: `NSt6__ndk110__function6__funcINS_6__bindIM12CMarchBackUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02864CD8`: `NSt6__ndk110__function6__funcINS_6__bindIM15CMarchSpeedUpUIFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x02864E1D`: `NSt6__ndk110__function6__funcINS_6__bindIM15CMarchSpeedUpUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x0271B886`: `NSt6__ndk110__function6__funcINS_6__bindIM15CMarchTentModelFvRK29CMSG_SYNC_MARCH_ARMY_INFO_NEWEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x028321E0`: `NSt6__ndk110__function6__funcINS_6__bindIM16LeagueTradeMapUIFvRK30CMSG_GET_DOMINION_MARCH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C17B1`: `NSt6__ndk110__function6__funcINS_6__bindIM19CLeagueTradeManagerFvRK29CMSG_START_TRADE_MARCH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C117C`: `NSt6__ndk110__function6__funcINS_6__bindIM19CLeagueTradeManagerFvRK30CMSG_GET_DOMINION_MARCH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02864FA1`: `NSt6__ndk110__function6__funcINS_6__bindIM19CMarchSpeedUpItemUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x0271C8E3`: `NSt6__ndk110__function6__funcINS_6__bindIM20MarchSpeedupItemCellFvPN7cocos2d3RefEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0271D875`: `NSt6__ndk110__function6__funcINS_6__bindIM21MarchSpeedupShutcutUIFvRK19CMSG_SYNC_MARCH_NEWEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0271D5B0`: `NSt6__ndk110__function6__funcINS_6__bindIM21MarchSpeedupShutcutUIFvRK25CMSG_SYN_ATTRIBUTE_CHANGEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0271D417`: `NSt6__ndk110__function6__funcINS_6__bindIM21MarchSpeedupShutcutUIFvRKNS_6vectorIiNS_9allocatorIiEEEES9_EJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS5_ISL_EEFvS9_S9_EEE`
- `0x028B06FA`: `NSt6__ndk110__function6__funcINS_6__bindIM25KingdomBountyQuestMarchUIFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02717FA1`: `NSt6__ndk110__function6__funcINS_6__bindIM9MapEffectFvRK32CMSG_CASTLE_PET_SKILL_SLOW_MARCHEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x027069C4`: `NSt6__ndk110__function6__funcIZN10KingdomMap11followMarchEmfE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x0270D9A9`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_1NS_9allocatorIS6_EEFvmiEEE`
- `0x0270DA4D`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_2NS_9allocatorIS6_EEFvmiEEE`
- `0x0270DAF1`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_3NS_9allocatorIS6_EEFvS5_EEE`
- `0x0270DE17`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_4NS_9allocatorIS6_EEFvRK17tModelPopMenuInfoP12ModelPopMenuRK14SimpleCSReaderPNS3_2ui6WidgetEEEE`
- `0x0270DB96`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_5NS_9allocatorIS6_EEFvS5_EEE`
- `0x0270DEFF`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_6NS_9allocatorIS6_EEFvS5_EEE`
- `0x0270DFA4`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_7NS_9allocatorIS6_EEFvS5_EEE`
- `0x0270E42F`: `NSt6__ndk110__function6__funcIZN10KingdomMap15onShowMarchMenuEPN7cocos2d3RefEmE3$_8NS_9allocatorIS6_EEFvRK17tModelPopMenuInfoP12ModelPopMenuRK14SimpleCSReaderPNS3_2ui6WidgetEEEE`
- *...and 1776 more*

### Rally (378 strings)

- `0x02804854`: `16HeroCellForRally`
- `0x0283795C`: `16LeagueWarRallyUI`
- `0x02837915`: `18LeagueWarRallyCell`
- `0x028354E1`: `20LeagueWarRallyJoinUI`
- `0x0283551C`: `23LeagueWarRallyListLogic`
- `0x02835536`: `24LeagueWarRallyPlayerCell`
- `0x0283792A`: `25LeagueWarRallyCellDefence`
- `0x028354F8`: `33LeagueWarRallyListTableViewSource`
- `0x0278C21A`: `NSt6__ndk110__function6__baseIFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x02804966`: `NSt6__ndk110__function6__funcINS_6__bindIM16HeroCellForRallyFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x0283A586`: `NSt6__ndk110__function6__funcINS_6__bindIM16LeagueWarRallyUIFvvEJPS3_EEENS_9allocatorIS7_EEFvfEEE`
- `0x028373BB`: `NSt6__ndk110__function6__funcINS_6__bindIM20LeagueWarRallyJoinUIFvPN7cocos2d3RefEfmEJPS3_RKNS_12placeholders4__phILi1EEERfRmEEENS_9allocatorISH_EEFvS6_EEE`
- `0x0283750C`: `NSt6__ndk110__function6__funcINS_6__bindIM20LeagueWarRallyJoinUIFvPN7cocos2d3RefEfmEJPS3_RKNS_12placeholders4__phILi1EEERfmEEENS_9allocatorISG_EEFvS6_EEE`
- `0x02837271`: `NSt6__ndk110__function6__funcINS_6__bindIM20LeagueWarRallyJoinUIFvPN7cocos2d3RefEmEJPS3_RKNS_12placeholders4__phILi1EEERmEEENS_9allocatorISG_EEFvS6_EEE`
- `0x02836D35`: `NSt6__ndk110__function6__funcINS_6__bindIM20LeagueWarRallyJoinUIFvRK34CMSG_SYNC_DOMINION_DETAIL_INFO_NEWEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02835734`: `NSt6__ndk110__function6__funcINS_6__bindIRKNS_8functionIFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEEJRKNS_12placeholders4__phILi1EEES8_EEENS_9allocatorISI_EEFvS6_EEE`
- `0x0270582C`: `NSt6__ndk110__function6__funcIZN10KingdomMap23onSyncLeagueRallyBattleERK32CMSG_SYNC_LEAGUE_BATTLE_INFO_NEWE3$_0NS_9allocatorIS6_EEFvfEEE`
- `0x02815F1D`: `NSt6__ndk110__function6__funcIZN14ChessDefenceUI12initControlsEvE3$_2NS_9allocatorIS3_EEFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x0283A507`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI12initControlsEvE3$_0NS_9allocatorIS3_EEFvN17LeagueDataManager6eEventEPKvEEE`
- `0x0283A6AF`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI12initControlsEvE3$_1NS_9allocatorIS3_EEFvPKcEEE`
- `0x0283A73C`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI12initControlsEvE3$_2NS_9allocatorIS3_EEFvPKcEEE`
- `0x02839C10`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EEFvPNS4_3RefEEEE`
- `0x02839DDD`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_1NSA_ISY_EEFvPNS4_3RefEEEE`
- `0x02839FAA`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_2NSA_ISY_EEFvPNS4_3RefEEEE`
- `0x0283A177`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_3NSA_ISY_EEFvPNS4_3RefEEEE`
- `0x0283A344`: `NSt6__ndk110__function6__funcIZN16LeagueWarRallyUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_4NSA_ISY_EESJ_EE`
- `0x0278C18F`: `NSt6__ndk110__function6__funcIZN17DominionDefenceUI12initControlsEvE3$_2NS_9allocatorIS3_EEFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x0283888D`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell13showTradeInfoERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_0NS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x02837EA8`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell14initControllerERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcbbE3$_0NS_9allocatorIS9_EEFvPN7cocos2d3RefEEEE`
- `0x02837FC5`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell14initControllerERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcbbE3$_1NS_9allocatorIS9_EEFvPN7cocos2d3RefEEEE`
- `0x028380E2`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell14initControllerERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcbbE3$_2NS_9allocatorIS9_EEFvPN7cocos2d3RefEEEE`
- `0x028381FF`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell9initTitleERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcE3$_0NS_9allocatorIS9_EEFNS_12basic_stringIcNS_11char_traitsIcEENSA_IcEEEEfEEE`
- `0x0283832E`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell9initTitleERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcE3$_1NS_9allocatorIS9_EEFvvEEE`
- `0x02838546`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell9initTitleERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcE3$_2NS_9allocatorIS9_EEFNS_12basic_stringIcNS_11char_traitsIcEENSA_IcEEEEfEEE`
- `0x02838675`: `NSt6__ndk110__function6__funcIZN18LeagueWarRallyCell9initTitleERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcE3$_3NS_9allocatorIS9_EEFvvEEE`
- `0x02836816`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI11doExitRallyEPN7cocos2d3RefEmE3$_0NS_9allocatorIS6_EEFvRK16eMessageBoxEventEEE`
- `0x028368D8`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI11doExitRallyEPN7cocos2d3RefEmE3$_1NS_9allocatorIS6_EEFvRK16eMessageBoxEventEEE`
- `0x0283760E`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI11doJoinRallyEPN7cocos2d3RefEfmE3$_0NS_9allocatorIS6_EEFvRKNS_4listIiNS7_IiEEEEiEEE`
- `0x028376D5`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI11doJoinRallyEPN7cocos2d3RefEfmE3$_1NS_9allocatorIS6_EEFvRKNS_4listIiNS7_IiEEEEiEEE`
- `0x0283779C`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI11doJoinRallyEPN7cocos2d3RefEfmE3$_2NS_9allocatorIS6_EEFvRK16eMessageBoxEventEEE`
- `0x02835C14`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI12initControlsEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x02835DF7`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI12initControlsEvE3$_1NS_9allocatorIS3_EEFvN17LeagueDataManager6eEventEPKvEEE`
- `0x02835FBA`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI12initControlsEvE3$_2NS_9allocatorIS3_EEFvRK28CMSG_ANSWER_USE_SPECIAL_ITEMEEE`
- `0x0283699A`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI17refreshBattleInfoEPKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_0NS_9allocatorIS7_EEFNS_12basic_stringIcNS_11char_traitsIcEENS8_IcEEEEfEEE`
- `0x02836AD9`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI17refreshBattleInfoEPKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_1NS_9allocatorIS7_EEFNS_12basic_stringIcNS_11char_traitsIcEENS8_IcEEEEfEEE`
- `0x02836C18`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI17refreshBattleInfoEPKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_2NS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x02836F1A`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI17refreshBattleInfoEPKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_3NS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x02837037`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI17refreshBattleInfoEPKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_4NS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x02837154`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI17refreshBattleInfoEPKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_5NS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x028361D6`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI8initDataEPKvE3$_0NS_9allocatorIS5_EEFvRK38CMSG_RESPONSE_BUILDUP_BATTLE_MOVE_TIMEEEE`
- `0x028362DA`: `NSt6__ndk110__function6__funcIZN20LeagueWarRallyJoinUI8initDataEPKvE3$_1NS_9allocatorIS5_EEFvRK30CMSG_SYNC_DEFEND_HERO_INFO_NEWEEE`
- `0x0285004B`: `NSt6__ndk110__function6__funcIZN21GuildBuldingDefenceUI12initControlsEvE3$_1NS_9allocatorIS3_EEFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x0282CD39`: `NSt6__ndk110__function6__funcIZN22LeagueReinforcementsUI12initControlsEvE3$_1NS_9allocatorIS3_EEFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x02836388`: `NSt6__ndk110__function6__funcIZN23LeagueWarRallyListLogic14initPlayerCellEP24LeagueWarRallyPlayerCellE3$_0NS_9allocatorIS5_EEFvPN7cocos2d3RefEEEE`
- `0x02836467`: `NSt6__ndk110__function6__funcIZN23LeagueWarRallyListLogic16setHostTableViewEPN7cocos2d9extension9TableViewEE3$_0NS_9allocatorIS7_EEFvPNS3_3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x02836715`: `NSt6__ndk110__function6__funcIZN23LeagueWarRallyListLogic16setHostTableViewEPN7cocos2d9extension9TableViewEE3$_1NS_9allocatorIS7_EEFvPNS3_3RefEP24LeagueWarRallyPlayerCellEEE`
- `0x02835B03`: `NSt6__ndk110__function6__funcIZN24LeagueWarRallyPlayerCell11SetAsLeaderEbE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefEEEE`
- `0x02835A47`: `NSt6__ndk110__function6__funcIZN24LeagueWarRallyPlayerCell8initDataERKNS2_10PlayerInfoEjbbbE3$_0NS_9allocatorIS6_EEFvvEEE`
- `0x028392FD`: `NSt6__ndk110__function6__funcIZN25LeagueWarRallyCellDefence8initDataERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEE3$_0NS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x02815FA5`: `NSt6__ndk110__function6__funcIZZN14ChessDefenceUI12initControlsEvENK3$_2clEPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEUlRK16eMessageBoxEventE_NS_9allocatorISC_EEFvSB_EEE`
- `0x0278C268`: `NSt6__ndk110__function6__funcIZZN17DominionDefenceUI12initControlsEvENK3$_2clEPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEUlRK16eMessageBoxEventE_NS_9allocatorISC_EEFvSB_EEE`
- `0x028383C9`: `NSt6__ndk110__function6__funcIZZN18LeagueWarRallyCell9initTitleERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcENK3$_1clEvEUlvE_NS_9allocatorISA_EEFvvEEE`
- `0x02838710`: `NSt6__ndk110__function6__funcIZZN18LeagueWarRallyCell9initTitleERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEPKcENK3$_3clEvEUlvE_NS_9allocatorISA_EEFvvEEE`
- `0x02835CA2`: `NSt6__ndk110__function6__funcIZZN20LeagueWarRallyJoinUI12initControlsEvENK3$_0clEPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEUlRK16eMessageBoxEventE_NS_9allocatorISC_EEFvSB_EEE`
- `0x028500DA`: `NSt6__ndk110__function6__funcIZZN21GuildBuldingDefenceUI12initControlsEvENK3$_1clEPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEUlRK16eMessageBoxEventE_NS_9allocatorISC_EEFvSB_EEE`
- `0x0282CDC9`: `NSt6__ndk110__function6__funcIZZN22LeagueReinforcementsUI12initControlsEvENK3$_1clEPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEUlRK16eMessageBoxEventE_NS_9allocatorISC_EEFvSB_EEE`
- `0x028394E4`: `NSt6__ndk110__function6__funcIZZN25LeagueWarRallyCellDefence8initDataERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEENK3$_0clEPN7cocos2d3RefEEUlvE0_NS_9allocatorISB_EEFvvEEE`
- `0x02839621`: `NSt6__ndk110__function6__funcIZZN25LeagueWarRallyCellDefence8initDataERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEENK3$_0clEPN7cocos2d3RefEEUlvE1_NS_9allocatorISB_EEFvvEEE`
- `0x0283975E`: `NSt6__ndk110__function6__funcIZZN25LeagueWarRallyCellDefence8initDataERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEENK3$_0clEPN7cocos2d3RefEEUlvE2_NS_9allocatorISB_EEFvvEEE`
- `0x028393A9`: `NSt6__ndk110__function6__funcIZZN25LeagueWarRallyCellDefence8initDataERKN17LeagueDataManager33ClientLeagueBuildupBattleSyncInfoEENK3$_0clEPN7cocos2d3RefEEUlvE_NS_9allocatorISB_EEFvvEEE`
- `0x02804A33`: `NSt6__ndk114unary_functionIP16HeroCellForRallyvEE`
- `0x0283A653`: `NSt6__ndk114unary_functionIP16LeagueWarRallyUIvEE`
- `0x02836EBD`: `NSt6__ndk115binary_functionIP20LeagueWarRallyJoinUIRK34CMSG_SYNC_DOMINION_DETAIL_INFO_NEWvEE`
- `0x028359FD`: `NSt6__ndk115binary_functionIPN7cocos2d3RefEP24LeagueWarRallyPlayerCellvEE`
- `0x028049FA`: `NSt6__ndk118__weak_result_typeIM16HeroCellForRallyFvvEEE`
- `0x0283A61A`: `NSt6__ndk118__weak_result_typeIM16LeagueWarRallyUIFvvEEE`
- `0x028374BF`: `NSt6__ndk118__weak_result_typeIM20LeagueWarRallyJoinUIFvPN7cocos2d3RefEfmEEE`
- `0x0283736F`: `NSt6__ndk118__weak_result_typeIM20LeagueWarRallyJoinUIFvPN7cocos2d3RefEmEEE`
- `0x02836E5B`: `NSt6__ndk118__weak_result_typeIM20LeagueWarRallyJoinUIFvRK34CMSG_SYNC_DOMINION_DETAIL_INFO_NEWEEE`
- `0x02835854`: `NSt6__ndk118__weak_result_typeINS_8functionIFvPN7cocos2d3RefEP24LeagueWarRallyPlayerCellEEEEE`
- *...and 298 more*

### Reinforce (1478 strings)

- `0x02631B95`: `%*s<Not Supported>`
- `0x0257B9F8`: `%*s<Unsupported tag %d>`
- `0x0258204A`: `%*sVersion: <unsupported>`
- `0x025A71F1`: `%s (unsupported)`
- `0x0272C49C`: `17TutCond_DefendNPC`
- `0x02855E0C`: `19CMailDefendHeroCell`
- `0x0272BB51`: `19TutCond_DefendTrade`
- `0x0278B9DF`: `20DominionDefendBackUI`
- `0x0278B9C6`: `22DominionDefendBackCell`
- `0x0282C900`: `22LeagueReinforcementsUI`
- `0x0272C651`: `23TutCond_DefendNPCResult`
- `0x0272DB24`: `24TutFunc_ShowDefendResult`
- `0x026033F9`: `<unsupported>`
- `0x025685D0`: `AnabasisDefendProtect`
- `0x0261B360`: `Backing store not supported`
- `0x025E4545`: `BuildDefendTime`
- `0x0256BB7C`: `CONNECT tunnel: unsupported ALPN(%d) negotiated`
- `0x025896BF`: `CastleDefendProtect`
- `0x025A6F5C`: `Chunky upload is not supported by HTTP 1.0`
- `0x0259C82C`: `CityDefend`
- `0x025F4D53`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/cocostudio/ActionTimeline/CCActionTimelineCache.cpp`
- `0x0256C015`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/cocostudio/ActionTimeline/CSLoader.cpp`
- `0x02607DE7`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/cocostudio/CCArmatureAnimation.cpp`
- `0x025803EF`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Animation.c`
- `0x025D4AAE`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/AnimationState.c`
- `0x02593E5B`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/AnimationStateData.c`
- `0x02607E78`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Atlas.c`
- `0x025A7615`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/AtlasAttachmentLoader.c`
- `0x025D4B53`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Attachment.c`
- `0x025A0736`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/AttachmentLoader.c`
- `0x025A752A`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Bone.c`
- `0x02580469`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/BoneData.c`
- `0x025A769B`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/BoundingBoxAttachment.c`
- `0x025A759F`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Event.c`
- `0x02601712`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/EventData.c`
- `0x025A069A`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/IkConstraint.c`
- `0x02565E20`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/IkConstraintData.c`
- `0x0260E034`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Json.c`
- `0x026150CE`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/MeshAttachment.c`
- `0x025DB1EF`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/PolygonBatch.cpp`
- `0x02565EAB`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/RegionAttachment.c`
- `0x02627E3A`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Skeleton.c`
- `0x025CDEDA`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/SkeletonAnimation.cpp`
- `0x025E8244`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/SkeletonData.c`
- `0x0256C0B2`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/SkeletonJson.c`
- `0x0260178C`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/SkeletonRenderer.cpp`
- `0x0260181C`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Skin.c`
- `0x025BA6F4`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/SkinnedMeshAttachment.c`
- `0x025C0F3E`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/Slot.c`
- `0x025C78CB`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/SlotData.c`
- `0x025EEC1E`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/extension.c`
- `0x025A07B7`: `D:/CQ1/tiger/trunk/program/client/ccoc_70/Game/proj.android-studio/../../cocos2d-x/cocos/editor-support/spine/spine-cocos2dx.cpp`
- `0x025B406F`: `DCT scaled block size %dx%d not supported`
- `0x025DC01F`: `DSO support routines`
- `0x025BCBC6`: `DW_EH_PE_aligned pointer encoding not supported`
- `0x0256E374`: `DW_EH_PE_funcrel pointer encoding not supported`
- `0x025F0BAC`: `DW_EH_PE_textrel pointer encoding not supported`
- `0x025BCFC0`: `DefendCDTime`
- `0x0260400E`: `DefendHero`
- `0x026118F1`: `DefendNPC`
- `0x026118FB`: `DefendNPCResult`
- `0x02610EB2`: `DefendNpc`
- `0x02610ED4`: `DefendTime`
- `0x025C3CDF`: `DefendTrade`
- `0x02584179`: `DefenderPanel`
- `0x02566F52`: `Dynamic engine loading support`
- `0x010B5938`: `EVP_PKEY_digestsign_supports_digest`
- `0x025DB5CF`: `EdgeEvent - collinear points not supported`
- `0x025DCC70`: `EdiPartyName:<unsupported>`
- `0x025CDC81`: `Empty JPEG image (DNL not supported)`
- `0x025FD2FF`: `Explicit digest not supported for ML-DSA operations`
- `0x025751C1`: `Explicit digest not supported for SLH-DSA operations`
- `0x0260D844`: `HTTP server does not seem to support byte ranges. Cannot resume.`
- `0x02627D5C`: `JNI interface version 1.4 not supported`
- `0x02611380`: `KING_DEFEND_INFO`
- `0x025FB307`: `Maximum supported image dimension is %u pixels`
- `0x026B6E1F`: `NSt6__ndk110__function6__baseIFvRK21CMSG_SYNC_DEFEND_INFOEEE`
- `0x02756F30`: `NSt6__ndk110__function6__baseIFvRK24CMSG_SYNC_DEFEND_VERSIONEEE`
- `0x026538E1`: `NSt6__ndk110__function6__baseIFvRK28CMSG_SYNC_CLANPK_DEFEND_INFOEEE`
- `0x0265679D`: `NSt6__ndk110__function6__baseIFvRK30CMSG_CLANPK_DEFEND_AMRY_RETURNEEE`
- *...and 1398 more*

### Research (86 strings)

- `0x02731263`: `22TutFunc_DoTechResearch`
- `0x0260A731`: `DoTechResearch`
- `0x02731307`: `NSt6__ndk110__function6__funcINS_6__bindIM22TutFunc_DoTechResearchFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x027315A0`: `NSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_NS_9allocatorIS5_EEFvS4_EEE`
- `0x027314F5`: `NSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_NS_9allocatorIS6_EEFvS5_EEE`
- `0x02731468`: `NSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE0_NS_9allocatorIS3_EEFvvEEE`
- `0x0273127C`: `NSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE_NS_9allocatorIS3_EEFvvEEE`
- `0x02731611`: `NSt6__ndk110__function6__funcIZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES4_EUlvE_NS_9allocatorIS6_EEFvvEEE`
- `0x0273142C`: `NSt6__ndk115binary_functionIP22TutFunc_DoTechResearchPKcvEE`
- `0x027313EB`: `NSt6__ndk118__weak_result_typeIM22TutFunc_DoTechResearchFvPKcEEE`
- `0x02731392`: `NSt6__ndk16__bindIM22TutFunc_DoTechResearchFvPKcEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x027316D6`: `ZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_`
- `0x02731567`: `ZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_`
- `0x027314CA`: `ZN22TutFunc_DoTechResearch6doNextEvEUlvE0_`
- `0x027312DD`: `ZN22TutFunc_DoTechResearch6doNextEvEUlvE_`
- `0x0273168F`: `ZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES1_EUlvE_`
- `0x00D264E8`: `_ZN13CLeagueTechUI22showTechStudyIngEffectEv`
- `0x0095FC8B`: `_ZN15CScienceManager20isResearchScienceNowEN13SScienceQueue10EQueueTypeE`
- `0x009A5AF3`: `_ZN15CScienceManager21showCancelResearchTipEi`
- `0x00962139`: `_ZN15CScienceManager30sendMsgToCancelScienceResearchEN13SScienceQueue10EQueueTypeE`
- `0x0090F144`: `_ZN18CLeagueTechManager14isStudyingTechEv`
- `0x00A75987`: `_ZN22TutFunc_DoTechResearch5clearEv`
- `0x00A759AB`: `_ZN22TutFunc_DoTechResearch6doNextEv`
- `0x00A75B2A`: `_ZN22TutFunc_DoTechResearch9onMessageEPKc`
- `0x007C350B`: `_ZN27LostLandStudyingScienceMetaC1Eii`
- `0x007C33DC`: `_ZN27LostLandStudyingScienceMetaC2Eii`
- `0x00AF2EC5`: `_ZN27LostLandStudyingScienceMetaD2Ev`
- `0x007C3402`: `_ZNK27LostLandStudyingScienceMeta13getLeftSecondEv`
- `0x007C347E`: `_ZNK27LostLandStudyingScienceMeta14getLeftPercentEv`
- `0x007C34B2`: `_ZNK27LostLandStudyingScienceMeta7isValidEv`
- `0x00A75D01`: `_ZNSt6__ndk110__function6__funcINS_6__bindIM22TutFunc_DoTechResearchFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EED0Ev`
- `0x00A76044`: `_ZNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_NS_9allocatorIS5_EEFvS4_EED0Ev`
- `0x00A75F10`: `_ZNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_NS_9allocatorIS6_EEFvS5_EED0Ev`
- `0x00A75E4B`: `_ZNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE0_NS_9allocatorIS3_EEFvvEED0Ev`
- `0x00A75C3F`: `_ZNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE_NS_9allocatorIS3_EEFvvEED0Ev`
- `0x00A761F6`: `_ZNSt6__ndk110__function6__funcIZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES4_EUlvE_NS_9allocatorIS6_EEFvvEED0Ev`
- `0x00A8356C`: `_ZTI22TutFunc_DoTechResearch`
- `0x00A83670`: `_ZTINSt6__ndk110__function6__funcINS_6__bindIM22TutFunc_DoTechResearchFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x00A83A50`: `_ZTINSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_NS_9allocatorIS5_EEFvS4_EEE`
- `0x00A83964`: `_ZTINSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_NS_9allocatorIS6_EEFvS5_EEE`
- `0x00A83898`: `_ZTINSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE0_NS_9allocatorIS3_EEFvvEEE`
- `0x00A835A6`: `_ZTINSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE_NS_9allocatorIS3_EEFvvEEE`
- `0x00A83B3A`: `_ZTINSt6__ndk110__function6__funcIZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES4_EUlvE_NS_9allocatorIS6_EEFvvEEE`
- `0x00A83813`: `_ZTINSt6__ndk115binary_functionIP22TutFunc_DoTechResearchPKcvEE`
- `0x00A83853`: `_ZTINSt6__ndk118__weak_result_typeIM22TutFunc_DoTechResearchFvPKcEEE`
- `0x00A75DEE`: `_ZTINSt6__ndk16__bindIM22TutFunc_DoTechResearchFvPKcEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x00A76138`: `_ZTIZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_`
- `0x00A76007`: `_ZTIZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_`
- `0x00A75EE1`: `_ZTIZN22TutFunc_DoTechResearch6doNextEvEUlvE0_`
- `0x00A75CD3`: `_ZTIZN22TutFunc_DoTechResearch6doNextEvEUlvE_`
- `0x00A762C4`: `_ZTIZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES1_EUlvE_`
- `0x00A83589`: `_ZTS22TutFunc_DoTechResearch`
- `0x00A836FF`: `_ZTSNSt6__ndk110__function6__funcINS_6__bindIM22TutFunc_DoTechResearchFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x00A83AC5`: `_ZTSNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_NS_9allocatorIS5_EEFvS4_EEE`
- `0x00A839DA`: `_ZTSNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_NS_9allocatorIS6_EEFvS5_EEE`
- `0x00A838FE`: `_ZTSNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE0_NS_9allocatorIS3_EEFvvEEE`
- `0x00A8360B`: `_ZTSNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE_NS_9allocatorIS3_EEFvvEEE`
- `0x00A83BBC`: `_ZTSNSt6__ndk110__function6__funcIZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES4_EUlvE_NS_9allocatorIS6_EEFvvEEE`
- `0x00A837D3`: `_ZTSNSt6__ndk115binary_functionIP22TutFunc_DoTechResearchPKcvEE`
- `0x00A8378E`: `_ZTSNSt6__ndk118__weak_result_typeIM22TutFunc_DoTechResearchFvPKcEEE`
- `0x00A75D91`: `_ZTSNSt6__ndk16__bindIM22TutFunc_DoTechResearchFvPKcEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x00A760FC`: `_ZTSZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_`
- `0x00A75FCA`: `_ZTSZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_`
- `0x00A75EB2`: `_ZTSZN22TutFunc_DoTechResearch6doNextEvEUlvE0_`
- `0x00A75CA5`: `_ZTSZN22TutFunc_DoTechResearch6doNextEvEUlvE_`
- `0x00A76279`: `_ZTSZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES1_EUlvE_`
- `0x00A7F0AD`: `_ZTV22TutFunc_DoTechResearch`
- `0x00A75A9B`: `_ZTVNSt6__ndk110__function6__funcINS_6__bindIM22TutFunc_DoTechResearchFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x00A75BCA`: `_ZTVNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlP12ModelPopMenuE_NS_9allocatorIS5_EEFvS4_EEE`
- `0x00A75B54`: `_ZTVNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlPN7cocos2d4NodeEE_NS_9allocatorIS6_EEFvS5_EEE`
- `0x00A75A35`: `_ZTVNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE0_NS_9allocatorIS3_EEFvvEEE`
- `0x00A759D0`: `_ZTVNSt6__ndk110__function6__funcIZN22TutFunc_DoTechResearch6doNextEvEUlvE_NS_9allocatorIS3_EEFvvEEE`
- `0x00A76174`: `_ZTVNSt6__ndk110__function6__funcIZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES4_EUlvE_NS_9allocatorIS6_EEFvvEEE`
- `0x00A760BA`: `_ZZN22TutFunc_DoTechResearch6doNextEvENKUlP12ModelPopMenuE_clES1_`
- `0x00A75F87`: `_ZZN22TutFunc_DoTechResearch6doNextEvENKUlPN7cocos2d4NodeEE_clES2_`
- `0x02613E84`: `check_main_research_time`
- `0x02613E42`: `m_pTextScience_research`
- `0x0257820B`: `mesbox_queue_research_btn`
- `0x025C3A13`: `mesbox_queue_research_check`
- `0x0257F356`: `mesbox_use_gold_research_check`
- *...and 6 more*

### Reward (13983 strings)

- `0x02764BB5`: `10RewardCell`
- `0x028A3462`: `11CUpRewardUI`
- `0x02887BAB`: `11RuinsReward`
- `0x02764BC2`: `12RewardEffect`
- `0x028A3470`: `12UpRewardCell`
- `0x02788F90`: `13COnlineReward`
- `0x028B5390`: `13Kvk_rewardXml`
- `0x028B6CA5`: `13Vip_rewardXml`
- `0x02795925`: `14EmpireRewardUI`
- `0x028B4C13`: `14Fans_rewardXml`
- `0x027E46FB`: `14FriendRewardUI`
- `0x02879AA8`: `14LordAtkBonusUI`
- `0x028B6B1D`: `14Task_rewardXml`
- `0x028B40C1`: `15Arena_rewardXml`
- `0x028B43A2`: `15Bulk_rewardsXml`
- `0x0273D544`: `15CItemRewardCell`
- `0x0263C59B`: `15CUpRewardConfig`
- `0x028819B5`: `15DailyRewardADUI`
- `0x028B5DF4`: `15Merge_rewardXml`
- `0x02764BD1`: `15NewRewardEffect`
- `0x0286F257`: `15OnlineRewardsUI`
- `0x02875D84`: `15PetHuntRewardUI`
- `0x02795912`: `16EmpireRewardCell`
- `0x027E46E8`: `16FriendRewardCell`
- `0x0281BB0E`: `16GuildRewardTipUI`
- `0x028B521E`: `16Invite_rewardXml`
- `0x028B5CAB`: `16Luxury_rewardXml`
- `0x028B5F9A`: `16Novice_rewardXml`
- `0x028819DF`: `17DailyRewardADCell`
- `0x027BD69F`: `17EventPageRewardAd`
- `0x0289E632`: `17TaskBoxRewardCell`
- `0x028B4122`: `18Army_lossrewardXml`
- `0x02751C21`: `18GiveGiftRewardCell`
- `0x02879A93`: `18LordAtkBonusCellUI`
- `0x027B85F5`: `18LordGrowRewardCell`
- `0x027B860A`: `18LordGrowRewardItem`
- `0x0276D0C6`: `18PlotTaskRewardCell`
- `0x028B64DB`: `18Recharge_rewardXml`
- `0x027BF0F6`: `19CSubscriptionReward`
- `0x028B4421`: `19Castle_up_rewardXml`
- `0x02881A45`: `19DailyRewardADRuleUI`
- `0x0289CE44`: `19FanActivityRewardUI`
- `0x028B5303`: `19Kingdomreward_lvXml`
- `0x027CB9FA`: `19LimitShopRewardItem`
- `0x0287A59E`: `19LordRewardSettingUI`
- `0x0275E389`: `19NavigationRewardBox`
- `0x02764BE3`: `19NewRewardEffectCell`
- `0x028B6AC3`: `19Subscribe_rewardXml`
- `0x027BF555`: `19Super4Choose1Reward`
- `0x028B24E6`: `19YahtzeeGameRewardUI`
- `0x0269AAE7`: `20CEmpireRewardManager`
- `0x0289CC31`: `20CFacebookShareReward`
- `0x028B486C`: `20Daily_shop_rewardXml`
- `0x027958E0`: `20EmpireRewardRecordUI`
- `0x02818AEB`: `20GeneralBoxRewardCell`
- `0x0265F2C1`: `20GiftPackBonusManager`
- `0x028B5AC9`: `20Lost_event_rewardXml`
- `0x0275C3C0`: `20MobilizationRewardUI`
- `0x0275E35B`: `20NavigationRewardCell`
- `0x0275E372`: `20NavigationRewardItem`
- `0x0286BCC1`: `20OnlineRewardsPageEra`
- `0x027D436A`: `20OpenSesameRewardView`
- `0x028B676B`: `20Rush_event_rewardXml`
- `0x028A2A78`: `20TroopAdvanceUpReward`
- `0x028B403F`: `21All_for_one_rewardXml`
- `0x028B4626`: `21Clanpk_rank_rewardXml`
- `0x028819C7`: `21DailyRewardADItemCell`
- `0x0288199D`: `21DailyRewardADRuleCell`
- `0x028B4822`: `21Daily_guild_rewardXml`
- `0x028B4896`: `21Daily_tasks_rewardXml`
- `0x02768662`: `21DropBoxRewardViewerUI`
- `0x027BD6B3`: `21EventPageRewardAdCell`
- `0x0289CDEE`: `21FanActivityRewardCell`
- `0x02752E5B`: `21GuildStandoffRewardUI`
- `0x02790BEC`: `21HeroDrawPrizePoolItem`
- `0x02754D3C`: `21KingdomGiftRewardCell`
- `0x028B52CF`: `21Kingdomreward_baseXml`
- `0x028B531A`: `21Kingdomreward_taskXml`
- `0x02818564`: `21KnightGloryRewardView`
- `0x027CC323`: `21LuckyWheelExtraReward`
- *...and 13903 more*

### Scout (155 strings)

- `0x02855E42`: `17CMailSpyTitleCell`
- `0x02855D96`: `20CMailSpyResourceItem`
- `0x02855DAD`: `22CMailSpyResourceCellUI`
- `0x0286491A`: `6CSpyUI`
- `0x028560FC`: `NSt6__ndk110__function6__funcINS_6__bindIM17CMailSpyTitleCellFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02864922`: `NSt6__ndk110__function6__funcINS_6__bindIM6CSpyUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x028649F5`: `NSt6__ndk110__function6__funcIZN6CSpyUI7setInfoERK9SpyUIInfoE3$_0NS_9allocatorIS6_EEFvPN7cocos2d3RefEEEE`
- `0x028561CC`: `NSt6__ndk114unary_functionIP17CMailSpyTitleCellvEE`
- `0x028649CE`: `NSt6__ndk114unary_functionIP6CSpyUIvEE`
- `0x02856192`: `NSt6__ndk118__weak_result_typeIM17CMailSpyTitleCellFvvEEE`
- `0x028649A0`: `NSt6__ndk118__weak_result_typeIM6CSpyUIFvvEEE`
- `0x0285615F`: `NSt6__ndk16__bindIM17CMailSpyTitleCellFvvEJPS1_EEE`
- `0x02864979`: `NSt6__ndk16__bindIM6CSpyUIFvvEJPS1_EEE`
- `0x02864A5E`: `ZN6CSpyUI7setInfoERK9SpyUIInfoE3$_0`
- `0x0068531C`: `_ZN10AFAppEvent14ScoutOtherturfEv`
- `0x00A0BB70`: `_ZN10KingdomMap15callCastleSpyUIEmiiifPKcS1_`
- `0x00A0BC3B`: `_ZN10KingdomMap22callDominionTradeSpyUIEmiPKc`
- `0x00A0BB9D`: `_ZN10KingdomMap9callSpyUIEmiiifPKcS1_NS_12ECallSpyTypeE`
- `0x006B3D20`: `_ZN13CGlobalConfig13getSpyInfoCfgEv`
- `0x00D8B9C1`: `_ZN17CMailSpyTitleCell11onClickDownEv`
- `0x00D8BBCB`: `_ZN17CMailSpyTitleCell11refreshPageEv`
- `0x00D8B94B`: `_ZN17CMailSpyTitleCell12onClickShareEv`
- `0x00D8B8F9`: `_ZN17CMailSpyTitleCell13onClickDeleteEv`
- `0x00D8B869`: `_ZN17CMailSpyTitleCell14bindControllerEv`
- `0x00D8B921`: `_ZN17CMailSpyTitleCell15onClickPositionEv`
- `0x00D8B972`: `_ZN17CMailSpyTitleCell17onClickCollectionEv`
- `0x00D8BB40`: `_ZN17CMailSpyTitleCell6createEv`
- `0x00D8BB78`: `_ZN17CMailSpyTitleCell7setDataERK12SpyTitleData`
- `0x00D8B99E`: `_ZN17CMailSpyTitleCell9onClickUpEv`
- `0x00D8BBA8`: `_ZN17CMailSpyTitleCell9refreshUIEv`
- `0x00D8C5A9`: `_ZN17CMailSpyTitleCellD0Ev`
- `0x00D8C58E`: `_ZN17CMailSpyTitleCellD2Ev`
- `0x00D8AA96`: `_ZN20CMailSpyResourceItem14bindControllerEv`
- `0x00D8AAC2`: `_ZN20CMailSpyResourceItem6createERK19MailSpyREsourceData14E_SPY_SHOW_NUM`
- `0x00D8AB26`: `_ZN20CMailSpyResourceItem6initUIERK19MailSpyREsourceData14E_SPY_SHOW_NUM`
- `0x00D8C29B`: `_ZN20CMailSpyResourceItemD0Ev`
- `0x00D8C27D`: `_ZN20CMailSpyResourceItemD2Ev`
- `0x00D8ACDD`: `_ZN22CMailSpyResourceCellUI10reSizeCellEv`
- `0x00D8AC99`: `_ZN22CMailSpyResourceCellUI11initNumShowE24E_SPY_SHOW_NUM_TITLE_COL`
- `0x00D8AB9D`: `_ZN22CMailSpyResourceCellUI12initResourceERK19MailSpyREsourceData14E_SPY_SHOW_NUM`
- `0x00D8AB6F`: `_ZN22CMailSpyResourceCellUI14bindControllerEv`
- `0x00D8ABEF`: `_ZN22CMailSpyResourceCellUI6createERKNSt6__ndk16vectorI19MailSpyREsourceDataNS0_9allocatorIS2_EEEE24E_SPY_SHOW_NUM_TITLE_COL14E_SPY_SHOW_NUM`
- `0x00D8C323`: `_ZN22CMailSpyResourceCellUID0Ev`
- `0x00D8C303`: `_ZN22CMailSpyResourceCellUID2Ev`
- `0x00DACB3D`: `_ZN6CSpyUI10onClickSpyEv`
- `0x00DACBDD`: `_ZN6CSpyUI12initControlsEv`
- `0x00DACBF8`: `_ZN6CSpyUI13getUIFilePathEv`
- `0x00DACA21`: `_ZN6CSpyUI14bindControllerERKNSt6__ndk18functionIFPN7cocos2d4NodeERKNS0_12basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEbEEERKNS1_IFbSC_RKNS1_IFvvEEEEEERKNS1_IFbPNS2_2ui6WidgetESK_EEE`
- `0x00DACC32`: `_ZN6CSpyUI14updateResourceEv`
- `0x00DACC14`: `_ZN6CSpyUI16SC_CCB_FILE_PATHE`
- `0x00DACC4F`: `_ZN6CSpyUI22onMainPlayerAttrChangeE15AttributeNumber`
- `0x00A0BC09`: `_ZN6CSpyUI7setInfoERK9SpyUIInfo`
- `0x00DACCC1`: `_ZN6CSpyUI9getDialogEv`
- `0x00DACB56`: `_ZN6CSpyUI9onAddFoodEv`
- `0x00A0BBFA`: `_ZN6CSpyUIC1Ev`
- `0x00DAC951`: `_ZN6CSpyUIC2Ev`
- `0x00DAC9CE`: `_ZN6CSpyUID0Ev`
- `0x00DAC991`: `_ZN6CSpyUID1Ev`
- `0x00DAC96C`: `_ZN6CSpyUID2Ev`
- `0x00A0BC29`: `_ZN9SpyUIInfoD2Ev`
- `0x00D8C84D`: `_ZNSt6__ndk110__function6__funcINS_6__bindIM17CMailSpyTitleCellFvvEJPS3_EEENS_9allocatorIS7_EEFvvEED0Ev`
- `0x00DACCD8`: `_ZNSt6__ndk110__function6__funcINS_6__bindIM6CSpyUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEED0Ev`
- `0x00D8CE5C`: `_ZTI17CMailSpyTitleCell`
- `0x00D8CD10`: `_ZTI20CMailSpyResourceItem`
- `0x00D8CD46`: `_ZTI22CMailSpyResourceCellUI`
- `0x00DACD8A`: `_ZTI6CSpyUI`
- `0x00D8CFE8`: `_ZTINSt6__ndk110__function6__funcINS_6__bindIM17CMailSpyTitleCellFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x00DACDA2`: `_ZTINSt6__ndk110__function6__funcINS_6__bindIM6CSpyUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x00D8D12B`: `_ZTINSt6__ndk114unary_functionIP17CMailSpyTitleCellvEE`
- `0x00DACEB5`: `_ZTINSt6__ndk114unary_functionIP6CSpyUIvEE`
- `0x00D8D162`: `_ZTINSt6__ndk118__weak_result_typeIM17CMailSpyTitleCellFvvEEE`
- `0x00DACEE0`: `_ZTINSt6__ndk118__weak_result_typeIM6CSpyUIFvvEEE`
- `0x00D8C8EC`: `_ZTINSt6__ndk16__bindIM17CMailSpyTitleCellFvvEJPS1_EEE`
- `0x00DACD5F`: `_ZTINSt6__ndk16__bindIM6CSpyUIFvvEJPS1_EEE`
- `0x00D8CE74`: `_ZTS17CMailSpyTitleCell`
- `0x00D8CD2B`: `_ZTS20CMailSpyResourceItem`
- `0x00D8CD63`: `_ZTS22CMailSpyResourceCellUI`
- `0x00DACD96`: `_ZTS6CSpyUI`
- `0x00D8D04F`: `_ZTSNSt6__ndk110__function6__funcINS_6__bindIM17CMailSpyTitleCellFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x00DACDFD`: `_ZTSNSt6__ndk110__function6__funcINS_6__bindIM6CSpyUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- *...and 75 more*

### Shield (391 strings)

- `0x02718B69`: `14CastleBubbleUI`
- `0x028B44A8`: `14Chat_bubbleXml`
- `0x0268A078`: `18CChatBubbleManager`
- `0x02775956`: `18ChatBubbleSelectUI`
- `0x028B44BA`: `21Chat_bubble_sourceXml`
- `0x02614329`: `Bubble`
- `0x025A6842`: `BubbleNameTid`
- `0x02617720`: `BubbleSigh`
- `0x0256EB48`: `CHAT_BUBBLE_UNLOCK_SUCCESS`
- `0x025DDD6D`: `ChatBubbleRedTip%lld`
- `0x0261C558`: `E-mail Protection`
- `0x0268AB8B`: `NSt6__ndk110__function6__baseIFvRK27CMSG_CHAT_ADD_BUBBLE_RETURNEEE`
- `0x0268AD9B`: `NSt6__ndk110__function6__funcINS_6__bindIM18CChatBubbleManagerFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0268A54C`: `NSt6__ndk110__function6__funcINS_6__bindIM18CChatBubbleManagerFvRK14CMSG_ITEM_INFOEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0268A393`: `NSt6__ndk110__function6__funcINS_6__bindIM18CChatBubbleManagerFvRK25CMSG_SYN_ATTRIBUTE_CHANGEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0268AAE8`: `NSt6__ndk110__function6__funcINS_6__bindIM18CChatBubbleManagerFvRK27CMSG_CHAT_ADD_BUBBLE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02775C40`: `NSt6__ndk110__function6__funcINS_6__bindIM18ChatBubbleSelectUIFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0277638A`: `NSt6__ndk110__function6__funcINS_6__bindIM18ChatBubbleSelectUIFvPN7cocos2d3RefEiiEJPS3_RKNS_12placeholders4__phILi1EEERKNSB_ILi2EEERKNSB_ILi3EEEEEENS_9allocatorISL_EEFvS6_iiEEE`
- `0x02775B22`: `NSt6__ndk110__function6__funcINS_6__bindIM18ChatBubbleSelectUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x0268A9D8`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI27CMSG_CHAT_ADD_BUBBLE_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x0268ACEC`: `NSt6__ndk110__function6__funcIZN18CChatBubbleManager28initBubbleRefreshDelayCallerEvE3$_0NS_9allocatorIS3_EEFvlEEE`
- `0x0277596B`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI13initWithParamEiE3$_0NS_9allocatorIS3_EEFvfEEE`
- `0x027759FC`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI14bindControllerEvE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x02775A8F`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI14bindControllerEvE3$_1NS_9allocatorIS3_EEFvvEEE`
- `0x02775F82`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_0NS_9allocatorIS5_EEFvvEEE`
- `0x0277607D`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_1NS_9allocatorIS5_EEFvPN7cocos2d3RefEEEE`
- `0x02776186`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_2NS_9allocatorIS5_EEFvvEEE`
- `0x02776281`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_3NS_9allocatorIS5_EEFvPN7cocos2d3RefEEEE`
- `0x02775DE5`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI8updateUIEvE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x02775E6A`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI8updateUIEvE3$_1NS_9allocatorIS3_EEFvvEEE`
- `0x02775EEF`: `NSt6__ndk110__function6__funcIZN18ChatBubbleSelectUI8updateUIEvE3$_2NS_9allocatorIS3_EEFvPN7cocos2d3RefEEEE`
- `0x02775C0C`: `NSt6__ndk114unary_functionIP18ChatBubbleSelectUIvEE`
- `0x0268AF2F`: `NSt6__ndk115binary_functionIP18CChatBubbleManagerPN7cocos2d11EventCustomEvEE`
- `0x0268A692`: `NSt6__ndk115binary_functionIP18CChatBubbleManagerRK14CMSG_ITEM_INFOvEE`
- `0x0268A4FA`: `NSt6__ndk115binary_functionIP18CChatBubbleManagerRK25CMSG_SYN_ATTRIBUTE_CHANGEvEE`
- `0x0268AC98`: `NSt6__ndk115binary_functionIP18CChatBubbleManagerRK27CMSG_CHAT_ADD_BUBBLE_RETURNvEE`
- `0x02775D98`: `NSt6__ndk115binary_functionIP18ChatBubbleSelectUIPN7cocos2d11EventCustomEvEE`
- `0x0268AEDD`: `NSt6__ndk118__weak_result_typeIM18CChatBubbleManagerFvPN7cocos2d11EventCustomEEEE`
- `0x0268A646`: `NSt6__ndk118__weak_result_typeIM18CChatBubbleManagerFvRK14CMSG_ITEM_INFOEEE`
- `0x0268A4A3`: `NSt6__ndk118__weak_result_typeIM18CChatBubbleManagerFvRK25CMSG_SYN_ATTRIBUTE_CHANGEEEE`
- `0x0268AC3F`: `NSt6__ndk118__weak_result_typeIM18CChatBubbleManagerFvRK27CMSG_CHAT_ADD_BUBBLE_RETURNEEE`
- `0x02775D46`: `NSt6__ndk118__weak_result_typeIM18ChatBubbleSelectUIFvPN7cocos2d11EventCustomEEEE`
- `0x027764B8`: `NSt6__ndk118__weak_result_typeIM18ChatBubbleSelectUIFvPN7cocos2d3RefEiiEEE`
- `0x02775BD1`: `NSt6__ndk118__weak_result_typeIM18ChatBubbleSelectUIFvvEEE`
- `0x0268AE73`: `NSt6__ndk16__bindIM18CChatBubbleManagerFvPN7cocos2d11EventCustomEEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x0268A5E2`: `NSt6__ndk16__bindIM18CChatBubbleManagerFvRK14CMSG_ITEM_INFOEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x0268A434`: `NSt6__ndk16__bindIM18CChatBubbleManagerFvRK25CMSG_SYN_ATTRIBUTE_CHANGEEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x0268ABCE`: `NSt6__ndk16__bindIM18CChatBubbleManagerFvRK27CMSG_CHAT_ADD_BUBBLE_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x02775CDC`: `NSt6__ndk16__bindIM18ChatBubbleSelectUIFvPN7cocos2d11EventCustomEEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x0277643B`: `NSt6__ndk16__bindIM18ChatBubbleSelectUIFvPN7cocos2d3RefEiiEJPS1_RKNS_12placeholders4__phILi1EEERKNS9_ILi2EEERKNS9_ILi3EEEEEE`
- `0x02775B9D`: `NSt6__ndk16__bindIM18ChatBubbleSelectUIFvvEJPS1_EEE`
- `0x025B1822`: `Panel_shield`
- `0x025B3906`: `Shield`
- `0x025A3562`: `ShieldCost`
- `0x025651FF`: `ShieldTime`
- `0x025FC713`: `TBB Protection Profile`
- `0x0259B7B2`: `TPM Protection Profile`
- `0x0268AA79`: `ZN14MessageSubject16registerListenerI27CMSG_CHAT_ADD_BUBBLE_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x0276A819`: `ZN17CBagItemShopAllUI22onChatBubbleUnlockSuccEPN7cocos2d11EventCustomEE3$_0`
- `0x0268AD5F`: `ZN18CChatBubbleManager28initBubbleRefreshDelayCallerEvE3$_0`
- `0x027759CF`: `ZN18ChatBubbleSelectUI13initWithParamEiE3$_0`
- `0x02775A61`: `ZN18ChatBubbleSelectUI14bindControllerEvE3$_0`
- `0x02775AF4`: `ZN18ChatBubbleSelectUI14bindControllerEvE3$_1`
- `0x0277601B`: `ZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_0`
- `0x02776124`: `ZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_1`
- `0x0277621F`: `ZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_2`
- `0x02776328`: `ZN18ChatBubbleSelectUI24updateSelectBubbleBottomEN18CChatBubbleManager19stuBubbleStatusDataEE3$_3`
- `0x02775E43`: `ZN18ChatBubbleSelectUI8updateUIEvE3$_0`
- `0x02775EC8`: `ZN18ChatBubbleSelectUI8updateUIEvE3$_1`
- `0x02775F5B`: `ZN18ChatBubbleSelectUI8updateUIEvE3$_2`
- `0x0281DCAB`: `ZN20LeagueDominionInfoUI22onShieldEnabledClickedEPN7cocos2d3RefEiE3$_0`
- `0x0281DE8E`: `ZN20LeagueDominionInfoUI25onAllShieldEnabledClickedEPN7cocos2d3RefEE3$_0`
- `0x008240AC`: `_Z17ChatBubbleSortCmpRKiS0_`
- `0x0087ED69`: `_Z17setBubbleUIStatusPN7cocos2d2ui4TextERKNSt6__ndk112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEib`
- `0x006CC0F1`: `_ZN10CGameLogic15getShieldServerEv`
- `0x00B50205`: `_ZN10ChatMainUI27updateBubbleAndHornorTipNumEv`
- `0x00A0C87F`: `_ZN10KingdomMap12canUseShieldEv`
- `0x00A0C89F`: `_ZN10KingdomMap23checkAndNoticeShieldUseEv`
- `0x0096B241`: `_ZN11CMainCityUI15delNpcBubbleTipERNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEE`
- `0x00B52B7B`: `_ZN11ChatGroupUI27updateBubbleAndHornorTipNumEv`
- *...and 311 more*

### Speedup (1539 strings)

- `0x0266F95C`: `13RushEventData`
- `0x028B675A`: `13Rush_eventXml`
- `0x028128BA`: `14CItemSpeedUpUI`
- `0x026E5B76`: `14LogicRushEvent`
- `0x0267DD43`: `15RushRankManager`
- `0x0281288D`: `16CItemSpeedUpCell`
- `0x0273CC1F`: `18ActivityRushRankUI`
- `0x027D4D89`: `18EventPageRushEvent`
- `0x028B5B65`: `18Lost_rush_eventXml`
- `0x026E5B60`: `19ClientRushEventData`
- `0x027D55E7`: `19EventPageRushRankUI`
- `0x02853220`: `19LostLandEventRushUI`
- `0x028B6783`: `19Rush_event_scoreXml`
- `0x02836515`: `20LeagueWarSpeedUpCell`
- `0x0272FF80`: `20TutFunc_DoAccelerate`
- `0x027D59D4`: `21EventPageRushSourceUI`
- `0x02730435`: `21TutFunc_DoAccelerate2`
- `0x028B3EFE`: `22Activity_rush_eventXml`
- `0x027D52A2`: `22EventPageRushEventCell`
- `0x027D5595`: `22EventPageRushRankCell1`
- `0x027D55AE`: `22EventPageRushRankCell2`
- `0x02815030`: `22OneClickAccelerateCell`
- `0x02815049`: `22OneClickAccelerateTime`
- `0x028128A0`: `23CItemSpeedUpPackageCell`
- `0x027D59EC`: `23EventPageRushSourceCell`
- `0x028B5B7B`: `23Lost_rush_event_rankXml`
- `0x0266F96C`: `24LostLandEventRushManager`
- `0x028B5BB3`: `24Lost_rush_event_scoreXml`
- `0x0263C4CD`: `25CItemSpeedUpConfigManager`
- `0x026D929A`: `25OneClickAccelerateManager`
- `0x0273CC34`: `26ActivityRushRankUIRankCell`
- `0x0266F93E`: `27ClientLostLandRushEventData`
- `0x027D55C7`: `29EventPageRushRankCell2ItemRow`
- `0x025D0A69`: `CritAccelerate`
- `0x025AA775`: `DoAccelerate`
- `0x02575DF5`: `DoAccelerate2`
- `0x02617A8C`: `E_RUSH_RANK_DETAIL_INFO_RETURN`
- `0x026E607F`: `NSt6__ndk110__function6__baseIFvRK29CMSG_SYNC_ACTIVITY_RUSH_EVENTEEE`
- `0x0266FB46`: `NSt6__ndk110__function6__baseIFvRK29CMSG_SYNC_LOSTLAND_RUSH_EVENTEEE`
- `0x026E66F7`: `NSt6__ndk110__function6__baseIFvRK36CMSG_ACTIVITY_RUSH_EVENT_RANK_RETURNEEE`
- `0x0267020E`: `NSt6__ndk110__function6__baseIFvRK36CMSG_LOSTLAND_RUSH_EVENT_RANK_RETURNEEE`
- `0x026E5D51`: `NSt6__ndk110__function6__baseIFvRK36CMSG_SYNC_ACTIVITY_RUSH_EVENT_CONFIGEEE`
- `0x02812B64`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvPN7cocos2d3RefENS4_2ui6Slider9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x02812FDC`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvPN7cocos2d3RefENS4_2ui8PageView9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x028129C2`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvPN7cocos2d3RefENS4_2ui9TextField9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x02812CFD`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvbEJPS3_bEEENS_9allocatorIS7_EEFvvEEE`
- `0x028128CB`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x026E5FDE`: `NSt6__ndk110__function6__funcINS_6__bindIM14LogicRushEventFvRK29CMSG_SYNC_ACTIVITY_RUSH_EVENTEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026E664F`: `NSt6__ndk110__function6__funcINS_6__bindIM14LogicRushEventFvRK36CMSG_ACTIVITY_RUSH_EVENT_RANK_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026E5CA9`: `NSt6__ndk110__function6__funcINS_6__bindIM14LogicRushEventFvRK36CMSG_SYNC_ACTIVITY_RUSH_EVENT_CONFIGEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0267DD55`: `NSt6__ndk110__function6__funcINS_6__bindIM15RushRankManagerFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x02814C30`: `NSt6__ndk110__function6__funcINS_6__bindIM16CItemSpeedUpCellFviEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISC_EEFviiEEE`
- `0x0273D1C4`: `NSt6__ndk110__function6__funcINS_6__bindIM18ActivityRushRankUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x027D5082`: `NSt6__ndk110__function6__funcINS_6__bindIM18EventPageRushEventFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x027D5227`: `NSt6__ndk110__function6__funcINS_6__bindIM18EventPageRushEventFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x027D4DB8`: `NSt6__ndk110__function6__funcINS_6__bindIM18EventPageRushEventFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x027D58B2`: `NSt6__ndk110__function6__funcINS_6__bindIM19EventPageRushRankUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x0285350A`: `NSt6__ndk110__function6__funcINS_6__bindIM19LostLandEventRushUIFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x028536B3`: `NSt6__ndk110__function6__funcINS_6__bindIM19LostLandEventRushUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x02853236`: `NSt6__ndk110__function6__funcINS_6__bindIM19LostLandEventRushUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x0283652C`: `NSt6__ndk110__function6__funcINS_6__bindIM20LeagueWarSpeedUpCellFvRKNS_6vectorIiNS_9allocatorIiEEEES9_EJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS5_ISL_EEFvS9_S9_EEE`
- `0x027D53E0`: `NSt6__ndk110__function6__funcINS_6__bindIM22EventPageRushEventCellFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x027D52BB`: `NSt6__ndk110__function6__funcINS_6__bindIM22EventPageRushEventCellFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x02815062`: `NSt6__ndk110__function6__funcINS_6__bindIM22OneClickAccelerateTimeFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02814D70`: `NSt6__ndk110__function6__funcINS_6__bindIM23CItemSpeedUpPackageCellFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x027D5A93`: `NSt6__ndk110__function6__funcINS_6__bindIM23EventPageRushSourceCellFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x0266FA9B`: `NSt6__ndk110__function6__funcINS_6__bindIM24LostLandEventRushManagerFvRK29CMSG_SYNC_LOSTLAND_RUSH_EVENTEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0267015C`: `NSt6__ndk110__function6__funcINS_6__bindIM24LostLandEventRushManagerFvRK36CMSG_LOSTLAND_RUSH_EVENT_RANK_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0281340B`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI10updateTimeEiiE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x02813490`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI10updateTimeEiiE3$_1NS_9allocatorIS3_EEFvvEEE`
- `0x02812DF8`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0281317B`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI14getWidgetAsyncERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEERKNS_8functionIFvPN7cocos2d2ui6WidgetEbEEEE3$_0NS6_ISK_EEFvvEEE`
- `0x028139B3`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_0NS_9allocatorIS3_EEFviiiEEE`
- `0x02813A46`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_1NS_9allocatorIS3_EEFviiiEEE`
- `0x02813AD9`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_2NS_9allocatorIS3_EEFviiiEEE`
- `0x02813B6C`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_3NS_9allocatorIS3_EEFviiiEEE`
- `0x02813BFF`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_4NS_9allocatorIS3_EEFviiiEEE`
- `0x02813C92`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_5NS_9allocatorIS3_EEFviiiEEE`
- `0x02813D25`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_6NS_9allocatorIS3_EEFviiiEEE`
- `0x02813DB8`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_7NS_9allocatorIS3_EEFvRNS_6vectorI11NumberValueNS4_IS7_EEEEiEEE`
- *...and 1459 more*

### Teleport (8 strings)

- `0x025BAF7A`: `DISABLE_ACTIVE_MIGRATION appears multiple times`
- `0x0258E120`: `DISABLE_ACTIVE_MIGRATION is malformed`
- `0x02581BD6`: `Migration Controller Attestation Service`
- `0x0256D877`: `Migration Controller Registration Service`
- `0x00D9A229`: `_ZN7cocos2d9extension10ScrollView17relocateContainerEb`
- `0x0256C8F2`: `disable_active_migration`
- `0x0260FE0F`: `tcg-ce-migrationControllerAttestationService`
- `0x02622F47`: `tcg-ce-migrationControllerRegistrationService`

### Train (444 strings)

- `0x025E18A3`: `!constraint->space`
- `0x02574958`: `%*sPath Length Constraint: `
- `0x02599F34`: `/Users/ls/cocos2d-x-3rd-party-libs-src/contrib/android-arm64/chipmunk/src/cpConstraint.c`
- `0x0286303E`: `16MapDetailTrainUI`
- `0x028B697A`: `19Soldiers_recruitXml`
- `0x02822D7F`: `27LeagueInfoChangeCellRecruit`
- `0x027F4C2F`: `32GameNewsSoldierTrainedReportCell`
- `0x027F4B00`: `35GameNewsSoldierTrainedReportCellCsd`
- `0x025FDF96`: `AutoRecruit`
- `0x025F0361`: `BASIC_CONSTRAINTS`
- `0x010D795D`: `BASIC_CONSTRAINTS_free`
- `0x010D7906`: `BASIC_CONSTRAINTS_it`
- `0x010D7947`: `BASIC_CONSTRAINTS_new`
- `0x025A2776`: `Basic Constraints of CA cert not marked critical`
- `0x02579148`: `Cannot remove a constraint that was not added to the space. (Removed twice maybe?)`
- `0x025EEB49`: `Constraint is attached to a NULL body.`
- `0x02593CC4`: `Constraint is not a damped rotary spring.`
- `0x0258D5EB`: `Constraint is not a damped spring.`
- `0x0260DDFB`: `Constraint is not a groove joint.`
- `0x02607D39`: `Constraint is not a pin joint.`
- `0x02627C40`: `Constraint is not a pivot joint.`
- `0x02627C1D`: `Constraint is not a ratchet joint.`
- `0x0258D669`: `Constraint is not a rotary limit joint.`
- `0x02593D4D`: `Constraint is not a slide joint.`
- `0x025E45DA`: `ItemRecruit`
- `0x0297AFAD`: `N12_GLOBAL__N_116itanium_demangle32ConstrainedTypeTemplateParamDeclE`
- `0x02610191`: `NAME_CONSTRAINTS`
- `0x010D897D`: `NAME_CONSTRAINTS_check`
- `0x010D8994`: `NAME_CONSTRAINTS_check_CN`
- `0x010D8967`: `NAME_CONSTRAINTS_free`
- `0x010D8902`: `NAME_CONSTRAINTS_it`
- `0x010D8952`: `NAME_CONSTRAINTS_new`
- `0x02811716`: `NSt6__ndk110__function6__baseIFvRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNEEE`
- `0x02811670`: `NSt6__ndk110__function6__funcINS_6__bindIM16HeroExpeditionUIFvRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02822D9D`: `NSt6__ndk110__function6__funcINS_6__bindIM27LeagueInfoChangeCellRecruitFvPN7cocos2d3RefENS4_2ui9TextField9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x028A4C67`: `NSt6__ndk110__function6__funcINS_6__bindIM6WallUIFvRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02811556`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI32CMSG_HERO_SOLDIER_RECRUIT_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x02781D53`: `NSt6__ndk110__function6__funcIZN15CCityPlusDetail19createTrainBuffCellERiE3$_1NS_9allocatorIS4_EEFvvEEE`
- `0x028120F0`: `NSt6__ndk110__function6__funcIZN16HeroExpeditionUI16tryShowClickMaskENS2_13eRecruitStateERKNS_4listIiNS_9allocatorIiEEEEE3$_0NS5_ISA_EEFvPN7cocos2d4NodeEEEE`
- `0x028121F4`: `NSt6__ndk110__function6__funcIZN16HeroExpeditionUI16tryShowClickMaskENS2_13eRecruitStateERKNS_4listIiNS_9allocatorIiEEEEE3$_1NS5_ISA_EEFvPN7cocos2d4NodeEEEE`
- `0x0286327A`: `NSt6__ndk110__function6__funcIZN16MapDetailTrainUI8initDataEPKvE3$_0NS_9allocatorIS5_EEFNS_12basic_stringIcNS_11char_traitsIcEENS6_IcEEEEfEEE`
- `0x0286332F`: `NSt6__ndk110__function6__funcIZN16MapDetailTrainUI8initDataEPKvE3$_1NS_9allocatorIS5_EEFvvEEE`
- `0x028633B4`: `NSt6__ndk110__function6__funcIZN16MapDetailTrainUI8initDataEPKvE3$_2NS_9allocatorIS5_EEFNS_12basic_stringIcNS_11char_traitsIcEENS6_IcEEEEfEEE`
- `0x026D39AC`: `NSt6__ndk110__function6__funcIZN17CMainCityBuilding15changeToRecruitEPN7cocos2d2ui6WidgetEE3$_0NS_9allocatorIS7_EEFvvEEE`
- `0x02823027`: `NSt6__ndk110__function6__funcIZN27LeagueInfoChangeCellRecruit12bindCellCtrlEvEUlPN7cocos2d3RefEE0_NS_9allocatorIS6_EEFvS5_EEE`
- `0x028230EA`: `NSt6__ndk110__function6__funcIZN27LeagueInfoChangeCellRecruit12bindCellCtrlEvEUlPN7cocos2d3RefEE1_NS_9allocatorIS6_EEFvS5_EEE`
- `0x02822F66`: `NSt6__ndk110__function6__funcIZN27LeagueInfoChangeCellRecruit12bindCellCtrlEvEUlPN7cocos2d3RefEE_NS_9allocatorIS6_EEFvS5_EEE`
- `0x026D3A25`: `NSt6__ndk110__function6__funcIZZN17CMainCityBuilding15changeToRecruitEPN7cocos2d2ui6WidgetEENK3$_0clEvEUliE_NS_9allocatorIS8_EEFvlEEE`
- `0x0281182E`: `NSt6__ndk115binary_functionIP16HeroExpeditionUIRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNvEE`
- `0x028A4DBC`: `NSt6__ndk115binary_functionIP6WallUIRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNvEE`
- `0x028117D2`: `NSt6__ndk118__weak_result_typeIM16HeroExpeditionUIFvRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNEEE`
- `0x02822EF8`: `NSt6__ndk118__weak_result_typeIM27LeagueInfoChangeCellRecruitFvPN7cocos2d3RefENS2_2ui9TextField9EventTypeEEEE`
- `0x028A4D6B`: `NSt6__ndk118__weak_result_typeIM6WallUIFvRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNEEE`
- `0x0281175E`: `NSt6__ndk16__bindIM16HeroExpeditionUIFvRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x02822E65`: `NSt6__ndk16__bindIM27LeagueInfoChangeCellRecruitFvPN7cocos2d3RefENS2_2ui9TextField9EventTypeEEJPS1_RKNS_12placeholders4__phILi1EEERKNSC_ILi2EEEEEE`
- `0x028A4D02`: `NSt6__ndk16__bindIM6WallUIFvRK32CMSG_HERO_SOLDIER_RECRUIT_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x025BC3E2`: `OSSL_BASIC_ATTR_CONSTRAINTS`
- `0x010D78D4`: `OSSL_BASIC_ATTR_CONSTRAINTS_free`
- `0x010D7855`: `OSSL_BASIC_ATTR_CONSTRAINTS_it`
- `0x010D78B4`: `OSSL_BASIC_ATTR_CONSTRAINTS_new`
- `0x025BC423`: `POLICY_CONSTRAINTS`
- `0x010D8AD9`: `POLICY_CONSTRAINTS_free`
- `0x010D8AAC`: `POLICY_CONSTRAINTS_it`
- `0x010D8AC2`: `POLICY_CONSTRAINTS_new`
- `0x026329F0`: `REINDEXEDESCAPEACHECKEYBEFOREIGNOREGEXPLAINSTEADDATABASELECTABLEFTHENDEFERRABLELSEXCEPTRANSACTIONATURALTERAISEXCLUSIVEXISTSAVEPOINTERSECTRIGGEREFERENCESCONSTRAINTOFFSETEMPORARYUNIQUERYATTACHAVINGROUPDATEBEGINNERELEASEBETWEENOTNULLIKECASCADELETECASECOLLATECREATECURRENT_DATEDETACHIMMEDIATEJOINSERTMATCHPLANALYZEPRAGMABORTVALUESVIRTUALIMITWHENWHERENAMEAFTEREPLACEANDEFAULTAUTOINCREMENTCASTCOLUMNCOMMITCONFLICTCROSSCURRENT_TIMESTAMPRIMARYDEFERREDISTINCTDROPFAILFROMFULLGLOBYIFISNULLORDERESTRICTOUTERIGHTROLLBACKROWUNIONUSINGVACUUMVIEWINITIALLYHerF`
- `0x025A606B`: `UDEF_TrainLv`
- `0x025EFEB6`: `X509v3 Basic Attribute Certificate Constraints`
- `0x025EFA6F`: `X509v3 Basic Constraints`
- `0x025EFEE5`: `X509v3 Delegated Name Constraints`
- `0x0256D7E9`: `X509v3 Holder Name Constraints`
- `0x02608ED8`: `X509v3 Name Constraints`
- `0x025E3012`: `X509v3 Policy Constraints`
- `0x025C76B4`: `You have already added this constraint to another space. You cannot add it to a second.`
- `0x02586DF0`: `You have already added this constraint to this space. You must not add it a second time.`
- `0x028115FC`: `ZN14MessageSubject16registerListenerI32CMSG_HERO_SOLDIER_RECRUIT_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x02781DBB`: `ZN15CCityPlusDetail19createTrainBuffCellERiE3$_1`
- `0x0281218D`: `ZN16HeroExpeditionUI16tryShowClickMaskENS_13eRecruitStateERKNSt6__ndk14listIiNS1_9allocatorIiEEEEE3$_0`
- `0x02812291`: `ZN16HeroExpeditionUI16tryShowClickMaskENS_13eRecruitStateERKNSt6__ndk14listIiNS1_9allocatorIiEEEEE3$_1`
- `0x02863308`: `ZN16MapDetailTrainUI8initDataEPKvE3$_0`
- `0x0286338D`: `ZN16MapDetailTrainUI8initDataEPKvE3$_1`
- *...and 364 more*

### Upgrade (1251 strings)

- `0x02593A0B`: ` (upgraded to SSL)`
- `0x026A9D6C`: `17LogicEvolvedBadge`
- `0x028B6C7A`: `17Upgrade_rewardXml`
- `0x027A8ADA`: `18CCastleUpgradeCell`
- `0x02800F63`: `19HeroBadgePageEvolve`
- `0x028B5706`: `19Lord_gem_upgradeXml`
- `0x0280BA97`: `19UpgradeResourceCell`
- `0x028B6269`: `20Pet_skill_upgradeXml`
- `0x027A8E05`: `21CCastleUpgradeCellNew`
- `0x0272CCA8`: `22TutCond_HeroCanUpgrade`
- `0x027FF7AC`: `23HeroBadgeChoiceEvolveUI`
- `0x027FFD11`: `24HeroBadgeEvolvedResultUI`
- `0x02810DB0`: `27HeroLegendSkillUpgradeTipUI`
- `0x028B51DC`: `27Innercity_upgrade_rewardXml`
- `0x028190EC`: `27LatchAdventureUpgradeTipsUI`
- `0x0288DA19`: `28CScienceUpgradeSkillTimeCell`
- `0x02810D75`: `29HeroLegendSkillUpgradeTipCell`
- `0x027A8AEF`: `32EventOperationsPageCastleUpgrade`
- `0x027A8E1D`: `35EventOperationsPageCastleUpgradeNew`
- `0x025B700A`: `HERO_BADGE_CHOICE_EVOLVE_COMPLETE`
- `0x02563FF2`: `HeroBadgeEvolve%lld`
- `0x025EB393`: `HeroCanUpgrade`
- `0x0260D47E`: `IconUpgrade`
- `0x02635B2B`: `NSt6__ndk110__function6__baseIFvRK23CMSG_SYN_UPGRADE_REWARDEEE`
- `0x026DE2CA`: `NSt6__ndk110__function6__baseIFvRK29CMSG_PET_UPGRADE_SKILL_RETURNEEE`
- `0x026AA2FC`: `NSt6__ndk110__function6__baseIFvRK30CMSG_HONOR_SOUL_UPGRADE_RETURNEEE`
- `0x026CC4EC`: `NSt6__ndk110__function6__baseIFvRK30CMSG_LORD_SKILL_UPGRADE_RETURNEEE`
- `0x026CC817`: `NSt6__ndk110__function6__baseIFvRK36CMSG_LORD_SKILL_UPGRADE_BATCH_RETURNEEE`
- `0x026BEF93`: `NSt6__ndk110__function6__baseIFvRK43CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_STARTEEE`
- `0x026BF320`: `NSt6__ndk110__function6__baseIFvRK46CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_COMPLETEEEE`
- `0x02635A94`: `NSt6__ndk110__function6__funcINS_6__bindIM10AFAppEventFvRK23CMSG_SYN_UPGRADE_REWARDEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026DE22D`: `NSt6__ndk110__function6__funcINS_6__bindIM10PetManagerFvRK29CMSG_PET_UPGRADE_SKILL_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0284ABB1`: `NSt6__ndk110__function6__funcINS_6__bindIM12CLordSkillUIFvRK30CMSG_LORD_SKILL_UPGRADE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0284AD66`: `NSt6__ndk110__function6__funcINS_6__bindIM12CLordSkillUIFvRK36CMSG_LORD_SKILL_UPGRADE_BATCH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026CC44A`: `NSt6__ndk110__function6__funcINS_6__bindIM14LogicLordSkillFvRK30CMSG_LORD_SKILL_UPGRADE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026CC76F`: `NSt6__ndk110__function6__funcINS_6__bindIM14LogicLordSkillFvRK36CMSG_LORD_SKILL_UPGRADE_BATCH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0284B1DE`: `NSt6__ndk110__function6__funcINS_6__bindIM16CLordSkillInfoUIFvRK30CMSG_LORD_SKILL_UPGRADE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0284B3A3`: `NSt6__ndk110__function6__funcINS_6__bindIM16CLordSkillInfoUIFvRK36CMSG_LORD_SKILL_UPGRADE_BATCH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AAF08`: `NSt6__ndk110__function6__funcINS_6__bindIM17LogicEvolvedBadgeFvRK27CMSG_HERO_SOUL_EMBED_RESULTEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026A9F41`: `NSt6__ndk110__function6__funcINS_6__bindIM17LogicEvolvedBadgeFvRK27CMSG_HONOR_SOUL_INFO_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AA576`: `NSt6__ndk110__function6__funcINS_6__bindIM17LogicEvolvedBadgeFvRK27CMSG_HONOR_SOUL_WASH_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AA257`: `NSt6__ndk110__function6__funcINS_6__bindIM17LogicEvolvedBadgeFvRK30CMSG_HONOR_SOUL_UPGRADE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AABDA`: `NSt6__ndk110__function6__funcINS_6__bindIM17LogicEvolvedBadgeFvRK33CMSG_HERO_HONOR_SOUL_EMBED_RESULTEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026AA896`: `NSt6__ndk110__function6__funcINS_6__bindIM17LogicEvolvedBadgeFvRK35CMSG_HONOR_SOUL_WASH_REPLACE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x027A8B12`: `NSt6__ndk110__function6__funcINS_6__bindIM18CCastleUpgradeCellFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x026BEEE0`: `NSt6__ndk110__function6__funcINS_6__bindIM18CLeagueTechManagerFvRK43CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_STARTEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026BF26A`: `NSt6__ndk110__function6__funcINS_6__bindIM18CLeagueTechManagerFvRK46CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_COMPLETEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02800F79`: `NSt6__ndk110__function6__funcINS_6__bindIM19HeroBadgePageEvolveFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02801122`: `NSt6__ndk110__function6__funcINS_6__bindIM19HeroBadgePageEvolveFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x0280BE3C`: `NSt6__ndk110__function6__funcINS_6__bindIM19UpgradeResourceCellFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x027A8E43`: `NSt6__ndk110__function6__funcINS_6__bindIM21CCastleUpgradeCellNewFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d3RefEEEE`
- `0x027FF970`: `NSt6__ndk110__function6__funcINS_6__bindIM23HeroBadgeChoiceEvolveUIFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x027FF7C6`: `NSt6__ndk110__function6__funcINS_6__bindIM23HeroBadgeChoiceEvolveUIFviPK14SHeroBadgeMetaEJPS3_RKNS_12placeholders4__phILi1EEERKNSB_ILi2EEEEEENS_9allocatorISI_EEFviPS4_EEE`
- `0x027FFB29`: `NSt6__ndk110__function6__funcINS_6__bindIM23HeroBadgeChoiceEvolveUIFviiPK14SHeroBadgeMetabEJPS3_RKNS_12placeholders4__phILi1EEERKNSB_ILi2EEERKNSB_ILi3EEERKNSB_ILi4EEEEEENS_9allocatorISO_EEFviiS6_bEEE`
- `0x028194B8`: `NSt6__ndk110__function6__funcINS_6__bindIM27LatchAdventureUpgradeTipsUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x027A8C27`: `NSt6__ndk110__function6__funcINS_6__bindIM32EventOperationsPageCastleUpgradeFvPN7cocos2d3RefENS4_2ui10ScrollView9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x027A9155`: `NSt6__ndk110__function6__funcINS_6__bindIM35EventOperationsPageCastleUpgradeNewFvPN7cocos2d3RefENS4_2ui10ScrollView9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x0276D598`: `NSt6__ndk110__function6__funcIZN10PlotTaskUI31jumpToMainCityAndGuideToUpgradeEvE3$_0NS_9allocatorIS3_EEFvlEEE`
- `0x026E595D`: `NSt6__ndk110__function6__funcIZN12RuinsManager11showUpgradeEbE3$_0NS_9allocatorIS3_EEFvP8CRuinsUIEEE`
- `0x02781629`: `NSt6__ndk110__function6__funcIZN13ChatUseHornUI16showUpgradeVipLvEiE3$_0NS_9allocatorIS3_EEFvRK16eMessageBoxEventEEE`
- `0x0263598C`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI23CMSG_SYN_UPGRADE_REWARDEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026DE119`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI29CMSG_PET_UPGRADE_SKILL_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026AA141`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI30CMSG_HONOR_SOUL_UPGRADE_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026CC334`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI30CMSG_LORD_SKILL_UPGRADE_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026CC64D`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI36CMSG_LORD_SKILL_UPGRADE_BATCH_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026BEDB0`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI43CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_STARTEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x026BF134`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI46CMSG_LEAGUE_SCIENCE_BROADCAST_UPGRADE_COMPLETEEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x027DA45E`: `NSt6__ndk110__function6__funcIZN15CFariyProduceUI20onClickButtonUpgradeEvE3$_0NS_9allocatorIS3_EEFvlEEE`
- `0x026A9D80`: `NSt6__ndk110__function6__funcIZN17LogicEvolvedBadge28post_HONOR_SOUL_WASH_REQUESTEjiiE3$_0NS_9allocatorIS3_EEFviEEE`
- `0x0289BCDA`: `NSt6__ndk110__function6__funcIZN17LordEquipItemInfo9onUpgradeEvE3$_0NS_9allocatorIS3_EEFvRK16eMessageBoxEventEEE`
- `0x026C7C7D`: `NSt6__ndk110__function6__funcIZN18LogicLordEquipment21requestUpgradeGemHoleEiijRKNS_3mapIjjNS_4lessIjEENS_9allocatorINS_4pairIKjjEEEEEEE3$_0NS6_ISE_EEFviEEE`
- `0x0280122D`: `NSt6__ndk110__function6__funcIZN19HeroBadgePageEvolve14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EESJ_EE`
- `0x028013F6`: `NSt6__ndk110__function6__funcIZN19HeroBadgePageEvolve14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_1NSA_ISY_EESJ_EE`
- `0x028015BF`: `NSt6__ndk110__function6__funcIZN19HeroBadgePageEvolve14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_2NSA_ISY_EEFvPNS4_3RefENSR_8CheckBox9EventTypeEEEE`
- `0x0280183B`: `NSt6__ndk110__function6__funcIZN19HeroBadgePageEvolve36_on_event_HERO_BADGE_EVOLOVE_SUCCESSEPN7cocos2d11EventCustomEE3$_0NS_9allocatorIS6_EEFvlEEE`
- `0x0280192A`: `NSt6__ndk110__function6__funcIZN19HeroBadgePageEvolve36_on_event_HERO_BADGE_EVOLOVE_SUCCESSEPN7cocos2d11EventCustomEE3$_1NS_9allocatorIS6_EEFvlEEE`
- `0x028017AA`: `NSt6__ndk110__function6__funcIZN19HeroBadgePageEvolve6onShowEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefEEEE`
- `0x02801A19`: `NSt6__ndk110__function6__funcIZN19HeroBadgePageEvolve7SStarUi16playStarUpEffectEvE3$_0NS_9allocatorIS4_EEFvvEEE`
- `0x02848E16`: `NSt6__ndk110__function6__funcIZN19LordEquipmentInfoUI9onUpgradeEvE3$_0NS_9allocatorIS3_EEFvRK16eMessageBoxEventEEE`
- `0x0280BAAD`: `NSt6__ndk110__function6__funcIZN19UpgradeResourceCell11setCellInfoERNS2_10CellParamsERKNS_8functionIFvvEEEE3$_0NS_9allocatorISA_EES6_EE`
- *...and 1171 more*

---
## 5. Item Type / Category Constants

**Total: 29946 item-related strings**

### Speedup (681)

- `0x028128BA`: `14CItemSpeedUpUI`
- `0x02864CB0`: `15CMarchSpeedUpUI`
- `0x0281288D`: `16CItemSpeedUpCell`
- `0x02864CC2`: `19CMarchSpeedUpItemUI`
- `0x02836515`: `20LeagueWarSpeedUpCell`
- `0x0271C7ED`: `20MarchSpeedupItemCell`
- `0x0271C7D5`: `21MarchSpeedupShutcutUI`
- `0x028128A0`: `23CItemSpeedUpPackageCell`
- `0x0263C4CD`: `25CItemSpeedUpConfigManager`
- `0x0281B655`: `25DominionBuildingSpeedUpUI`
- `0x02812B64`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvPN7cocos2d3RefENS4_2ui6Slider9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x02812FDC`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvPN7cocos2d3RefENS4_2ui8PageView9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x028129C2`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvPN7cocos2d3RefENS4_2ui9TextField9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x02812CFD`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvbEJPS3_bEEENS_9allocatorIS7_EEFvvEEE`
- `0x028128CB`: `NSt6__ndk110__function6__funcINS_6__bindIM14CItemSpeedUpUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02864CD8`: `NSt6__ndk110__function6__funcINS_6__bindIM15CMarchSpeedUpUIFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- `0x02864E1D`: `NSt6__ndk110__function6__funcINS_6__bindIM15CMarchSpeedUpUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02814C30`: `NSt6__ndk110__function6__funcINS_6__bindIM16CItemSpeedUpCellFviEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISC_EEFviiEEE`
- `0x02864FA1`: `NSt6__ndk110__function6__funcINS_6__bindIM19CMarchSpeedUpItemUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x0283652C`: `NSt6__ndk110__function6__funcINS_6__bindIM20LeagueWarSpeedUpCellFvRKNS_6vectorIiNS_9allocatorIiEEEES9_EJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS5_ISL_EEFvS9_S9_EEE`
- `0x0271C8E3`: `NSt6__ndk110__function6__funcINS_6__bindIM20MarchSpeedupItemCellFvPN7cocos2d3RefEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0271D875`: `NSt6__ndk110__function6__funcINS_6__bindIM21MarchSpeedupShutcutUIFvRK19CMSG_SYNC_MARCH_NEWEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0271D5B0`: `NSt6__ndk110__function6__funcINS_6__bindIM21MarchSpeedupShutcutUIFvRK25CMSG_SYN_ATTRIBUTE_CHANGEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0271D417`: `NSt6__ndk110__function6__funcINS_6__bindIM21MarchSpeedupShutcutUIFvRKNS_6vectorIiNS_9allocatorIiEEEES9_EJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS5_ISL_EEFvS9_S9_EEE`
- `0x02814D70`: `NSt6__ndk110__function6__funcINS_6__bindIM23CItemSpeedUpPackageCellFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x0281B671`: `NSt6__ndk110__function6__funcINS_6__bindIM25DominionBuildingSpeedUpUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02727956`: `NSt6__ndk110__function6__funcIZN14CBuildingModel19playResourceSpeedUpEvE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x0281340B`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI10updateTimeEiiE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x02813490`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI10updateTimeEiiE3$_1NS_9allocatorIS3_EEFvvEEE`
- `0x02813515`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI12initTimeFunsEvE3$_0NS_9allocatorIS3_EEFvR8timeDataii12BuildingTypeEEE`
- `0x028135F3`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI12initTimeFunsEvE3$_1NS_9allocatorIS3_EEFvR8timeDataii12BuildingTypeEEE`
- `0x02813693`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI12initTimeFunsEvE3$_2NS_9allocatorIS3_EEFvR8timeDataii12BuildingTypeEEE`
- `0x02813733`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI12initTimeFunsEvE3$_3NS_9allocatorIS3_EEFvR8timeDataii12BuildingTypeEEE`
- `0x028137D3`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI12initTimeFunsEvE3$_4NS_9allocatorIS3_EEFvR8timeDataii12BuildingTypeEEE`
- `0x02813873`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI12initTimeFunsEvE3$_5NS_9allocatorIS3_EEFvR8timeDataii12BuildingTypeEEE`
- `0x02813913`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI12initTimeFunsEvE3$_6NS_9allocatorIS3_EEFvR8timeDataii12BuildingTypeEEE`
- `0x02812DF8`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0281317B`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI14getWidgetAsyncERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEERKNS_8functionIFvPN7cocos2d2ui6WidgetEbEEEE3$_0NS6_ISK_EEFvvEEE`
- `0x028139B3`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_0NS_9allocatorIS3_EEFviiiEEE`
- `0x02813A46`: `NSt6__ndk110__function6__funcIZN14CItemSpeedUpUI17initClickItemFunsEvE3$_1NS_9allocatorIS3_EEFviiiEEE`
- *...and 641 more*

### Resource (1712)

- `0x025A7973`: `%!PS-Adobe-3.0 Resource-CIDFont`
- `0x025BA97D`: `.resource/`
- `0x0285726B`: `13CMailResource`
- `0x02770614`: `14CBuyResourceUI`
- `0x02788F52`: `14CDailyResource`
- `0x0263CDFC`: `15CResourceConfig`
- `0x02718A95`: `16MapResourceModel`
- `0x0285727B`: `17CMailResourceItem`
- `0x02707403`: `17MenuInfo_Resource`
- `0x02857256`: `18CMailResourceTitle`
- `0x026C3B70`: `18LordAvatarResource`
- `0x0288C733`: `19ScienceResourceList`
- `0x0288C749`: `19ScienceResourceTime`
- `0x0280BA97`: `19UpgradeResourceCell`
- `0x02770625`: `20CBuyResourceTypeCell`
- `0x02855D96`: `20CMailSpyResourceItem`
- `0x02855DAD`: `22CMailSpyResourceCellUI`
- `0x028B4E4E`: `22Greedygame_resourceXml`
- `0x0285523D`: `23CMailBattleResourceItem`
- `0x026C3BA2`: `24CustomLordAvatarResource`
- `0x0276344D`: `25ArenaBattleResourceCellUI`
- `0x02855257`: `25CMailBattleResourceCellUI`
- `0x02644BC0`: `25ResourceAccConsumeManager`
- `0x026C3B85`: `26LordAvatarDownloadResource`
- `0x0272F956`: `26TutFunc_WaitForMapResource`
- `0x02728F48`: `28GuideFunc_WaitForMapResource`
- `0x02797B7B`: `30EventPageResourcesAccConsumeUI`
- `0x02758F40`: `40LostLandActivityPreStageDonateResourceUI`
- `0x02758F6B`: `47LostLandActivityPreStageBatchesDonateResourceUI`
- `0x025EE722`: `Access denied to remote resource`
- `0x0257C713`: `DonateResource`
- `0x025A34F8`: `FlyResource`
- `0x025A597E`: `Image_Resource`
- `0x00689D31`: `Java_com_jniCallback_retDownloadAvatarResource`
- `0x00689D04`: `Java_com_jniCallback_retUploadAvatarResource`
- `0x02620B8E`: `MaxResource`
- `0x02679F58`: `NSt6__ndk110__function6__baseIFvRK27CMSG_LEGION_RESOURCE_RETURNEEE`
- `0x027DC1FF`: `NSt6__ndk110__function6__baseIFvRK29CMSG_FORTRESS_RESOURCE_RETURNEEE`
- `0x02671837`: `NSt6__ndk110__function6__baseIFvRK36CMSG_LOSTLAND_DONATE_RESOURCE_RETURNEEE`
- `0x02857DD1`: `NSt6__ndk110__function6__funcINS_6__bindIM13CMailResourceFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- *...and 1672 more*

### Equipment (902)

- `0x027688C0`: `15EquipmentCellUI`
- `0x026C56A9`: `18LogicLordEquipment`
- `0x02848706`: `19LordEquipmentInfoUI`
- `0x02846C0B`: `21LordEquipmentChangeUI`
- `0x028490CF`: `23LordEquipmentSuitInfoUI`
- `0x02849748`: `23LordEquipmentSuitListUI`
- `0x02847D36`: `24LordEquipmentGemChangeUI`
- `0x028485AD`: `24LordEquipmentInfoOtherUI`
- `0x025C055A`: `Equipment`
- `0x028477F0`: `NSt6__ndk110__function6__baseIFviN19LordEquipmentInfoUI4TypeEEEE`
- `0x02769544`: `NSt6__ndk110__function6__funcINS_6__bindIM15EquipmentCellUIFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C57BF`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK19CMSG_LORD_EQUIP_SYNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C5AA3`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK23CMSG_LORD_NEW_EQUIP_SYNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C66EE`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK24CMSG_LORD_GEM_PUT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C7033`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK25CMSG_LORD_EQUIP_MERGE_SYNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C6D28`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK26CMSG_LORD_EQUIP_PUT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C63DB`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK28CMSG_LORD_PACKAGE_ADD_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C5DA5`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK28CMSG_LORD_PACKAGE_SET_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C60C0`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK28CMSG_LORD_PACKAGE_USE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C79C8`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK31CMSG_LORD_GEM_HOLE_LV_UP_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C69FD`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK32CMSG_LORD_EQUIP_DECOMPOSE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C7693`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK32CMSG_LORD_GEM_HOLE_UNLOCK_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026C734D`: `NSt6__ndk110__function6__funcINS_6__bindIM18LogicLordEquipmentFvRK35CMSG_SYNC_LORD_EQUIP_GEM_LEVEL_INFOEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0284871C`: `NSt6__ndk110__function6__funcINS_6__bindIM19LordEquipmentInfoUIFvRK24CMSG_LORD_GEM_PUT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x028488D5`: `NSt6__ndk110__function6__funcINS_6__bindIM19LordEquipmentInfoUIFvRK26CMSG_LORD_EQUIP_PUT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02848A96`: `NSt6__ndk110__function6__funcINS_6__bindIM19LordEquipmentInfoUIFvRK32CMSG_LORD_EQUIP_DECOMPOSE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02848C6F`: `NSt6__ndk110__function6__funcINS_6__bindIM19LordEquipmentInfoUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02847466`: `NSt6__ndk110__function6__funcINS_6__bindIM21LordEquipmentChangeUIFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02846C23`: `NSt6__ndk110__function6__funcINS_6__bindIM21LordEquipmentChangeUIFvRK24CMSG_LORD_GEM_PUT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0284718E`: `NSt6__ndk110__function6__funcINS_6__bindIM21LordEquipmentChangeUIFvRK25CMSG_LORD_EQUIP_MERGE_SYNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02846DE4`: `NSt6__ndk110__function6__funcINS_6__bindIM21LordEquipmentChangeUIFvRK26CMSG_LORD_EQUIP_PUT_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02846FAD`: `NSt6__ndk110__function6__funcINS_6__bindIM21LordEquipmentChangeUIFvRK32CMSG_LORD_EQUIP_DECOMPOSE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02847353`: `NSt6__ndk110__function6__funcINS_6__bindIM21LordEquipmentChangeUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x028490E9`: `NSt6__ndk110__function6__funcINS_6__bindIM23LordEquipmentSuitInfoUIFvRK28CMSG_LORD_PACKAGE_SET_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02849364`: `NSt6__ndk110__function6__funcINS_6__bindIM23LordEquipmentSuitInfoUIFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x02849CED`: `NSt6__ndk110__function6__funcINS_6__bindIM23LordEquipmentSuitListUIFvPN7cocos2d3RefEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02849762`: `NSt6__ndk110__function6__funcINS_6__bindIM23LordEquipmentSuitListUIFvRK28CMSG_LORD_PACKAGE_ADD_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x0284993B`: `NSt6__ndk110__function6__funcINS_6__bindIM23LordEquipmentSuitListUIFvRK28CMSG_LORD_PACKAGE_SET_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02849B14`: `NSt6__ndk110__function6__funcINS_6__bindIM23LordEquipmentSuitListUIFvRK28CMSG_LORD_PACKAGE_USE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02848422`: `NSt6__ndk110__function6__funcINS_6__bindIM24LordEquipmentGemChangeUIFvPN7cocos2d3RefEiiEJPS3_RKNS_12placeholders4__phILi1EEERKNSB_ILi2EEERKNSB_ILi3EEEEEENS_9allocatorISL_EEFvS6_iiEEE`
- *...and 862 more*

### Gem (1487)

- `0x028B56E1`: `11Lord_gemXml`
- `0x02898ED1`: `15EquipGemHoleUse`
- `0x028026F4`: `17HeroBadgePageMall`
- `0x028B5429`: `17Latch_gem_iconXml`
- `0x02898EBC`: `18LordEquipGemHoleUI`
- `0x028B56F0`: `18Lord_gem_unlockXml`
- `0x0269B4F1`: `19ErrorMessageManager`
- `0x028B5706`: `19Lord_gem_upgradeXml`
- `0x0284A5E4`: `20CLordRemoveGemItemUI`
- `0x0269B76F`: `20DailyRechargeManager`
- `0x02899109`: `20EquipGemHoleBatchUse`
- `0x027E8B88`: `20FriendUIPageMyFriend`
- `0x027E7D93`: `21FriendUIPageMilestone`
- `0x027E901C`: `21FriendUIPageMyInvited`
- `0x0289999D`: `21LordEquipGemHoleUICsd`
- `0x026D926E`: `22CNoviceRechargeManager`
- `0x026A2EC9`: `22GeneralRechargeManager`
- `0x0269A948`: `25DynamicCtrlPackageManager`
- `0x027E7DAB`: `25FriendUIPageMilestoneCell`
- `0x027E9034`: `25FriendUIPageMyInvitedCell`
- `0x027CFD09`: `26EventPageMonthCard_Coupons`
- `0x027CF5E0`: `28EventOperationsPageMonthCard`
- `0x02586454`: `CannonDamageMax`
- `0x025E784C`: `CannonDamageMin`
- `0x025673DF`: `Certificate Management Key Generation Authority`
- `0x025AD6DB`: `DefaultGemIcon`
- `0x0256D8B9`: `Distributed Management Task Force Registry`
- `0x025B9AD7`: `ExchangeMax`
- `0x02571B71`: `GemIcon`
- `0x025C6BF6`: `Gems`
- `0x02623F60`: `LordEquitGem`
- `0x02617746`: `LordGemFilter`
- `0x0262A49C`: `LordGembox`
- `0x025C231D`: `Management`
- `0x026422B4`: `N5latch12GetGemsStateE`
- `0x026C678E`: `NSt6__ndk110__function6__baseIFvRK24CMSG_LORD_GEM_PUT_RETURNEEE`
- `0x02847F07`: `NSt6__ndk110__function6__baseIFvRK26CMSG_LORD_GEM_MERGE_RETURNEEE`
- `0x02897EDE`: `NSt6__ndk110__function6__baseIFvRK30CMSG_LORD_GEM_DECOMPOSE_RETURNEEE`
- `0x026C7A6F`: `NSt6__ndk110__function6__baseIFvRK31CMSG_LORD_GEM_HOLE_LV_UP_RETURNEEE`
- `0x026C773B`: `NSt6__ndk110__function6__baseIFvRK32CMSG_LORD_GEM_HOLE_UNLOCK_RETURNEEE`
- *...and 1447 more*

### Material (389)

- `0x0257FA9F`: ` part is missing meshPartId or materialId`
- `0x028B575B`: `16Lord_materialXml`
- `0x028B6292`: `18PinBallMaterialXml`
- `0x028958DE`: `19LordMaterialForgeUI`
- `0x028B576F`: `21Lord_material_typeXml`
- `0x028B54AD`: `26Latch_physics_materialsXml`
- `0x025E44E3`: `LordEquipMaterialAutoForge`
- `0x028BB415`: `N7cocos2d10PUMaterialE`
- `0x028BB4A7`: `N7cocos2d22CCPUMaterialTranslatorE`
- `0x028BB456`: `N7cocos2d24PUMaterialPassTranslatorE`
- `0x028BB42C`: `N7cocos2d29PUMaterialTechniqueTranslatorE`
- `0x028BB47B`: `N7cocos2d31PUMaterialTextureUnitTranslatorE`
- `0x0289769C`: `NSt6__ndk110__function6__baseIFvRK31CMSG_LORD_MATERIAL_MERGE_RETURNEEE`
- `0x02897B9D`: `NSt6__ndk110__function6__baseIFvRK35CMSG_LORD_MATERIAL_DECOMPOSE_RETURNEEE`
- `0x028975F4`: `NSt6__ndk110__function6__funcINS_6__bindIM19LordMaterialForgeUIFvRK31CMSG_LORD_MATERIAL_MERGE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x02897AF1`: `NSt6__ndk110__function6__funcINS_6__bindIM19LordMaterialForgeUIFvRK35CMSG_LORD_MATERIAL_DECOMPOSE_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x028974DC`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI31CMSG_LORD_MATERIAL_MERGE_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x028979D1`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI35CMSG_LORD_MATERIAL_DECOMPOSE_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x0289744B`: `NSt6__ndk110__function6__funcIZN16LordEquipForgeUI15onClickMaterialEiE3$_0NS_9allocatorIS3_EEFviEEE`
- `0x02895EA7`: `NSt6__ndk110__function6__funcIZN18LordEquipForgeBase12initMaterialEPKNS2_13PanelMaterialERKNS_4pairIiiEEE3$_0NS_9allocatorISA_EEFviiEEE`
- `0x0289804E`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EESJ_EE`
- `0x02898217`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_1NSA_ISY_EESJ_EE`
- `0x028983E0`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_2NSA_ISY_EESJ_EE`
- `0x028985A9`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_3NSA_ISY_EEFvPNS4_3RefENSR_6Slider9EventTypeEEEE`
- `0x02898792`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_4NSA_ISY_EESJ_EE`
- `0x0289895B`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_5NSA_ISY_EESJ_EE`
- `0x02898B24`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_6NSA_ISY_EESJ_EE`
- `0x02898CED`: `NSt6__ndk110__function6__funcIZN19LordMaterialForgeUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_7NSA_ISY_EESJ_EE`
- `0x028977B7`: `NSt6__ndk115binary_functionIP19LordMaterialForgeUIRK31CMSG_LORD_MATERIAL_MERGE_RETURNvEE`
- `0x02897CC4`: `NSt6__ndk115binary_functionIP19LordMaterialForgeUIRK35CMSG_LORD_MATERIAL_DECOMPOSE_RETURNvEE`
- `0x02897759`: `NSt6__ndk118__weak_result_typeIM19LordMaterialForgeUIFvRK31CMSG_LORD_MATERIAL_MERGE_RETURNEEE`
- `0x02897C62`: `NSt6__ndk118__weak_result_typeIM19LordMaterialForgeUIFvRK35CMSG_LORD_MATERIAL_DECOMPOSE_RETURNEEE`
- `0x028976E3`: `NSt6__ndk16__bindIM19LordMaterialForgeUIFvRK31CMSG_LORD_MATERIAL_MERGE_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x02897BE8`: `NSt6__ndk16__bindIM19LordMaterialForgeUIFvRK35CMSG_LORD_MATERIAL_DECOMPOSE_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x010B28D7`: `SSL_export_keying_material`
- `0x010B28F2`: `SSL_export_keying_material_early`
- `0x02897581`: `ZN14MessageSubject16registerListenerI31CMSG_LORD_MATERIAL_MERGE_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x02897A7A`: `ZN14MessageSubject16registerListenerI35CMSG_LORD_MATERIAL_DECOMPOSE_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x028974AF`: `ZN16LordEquipForgeUI15onClickMaterialEiE3$_0`
- `0x02895F2F`: `ZN18LordEquipForgeBase12initMaterialEPKNS_13PanelMaterialERKNSt6__ndk14pairIiiEEE3$_0`
- *...and 349 more*

### Shield (34)

- `0x0281DB15`: `NSt6__ndk110__function6__funcIZN20LeagueDominionInfoUI22onShieldEnabledClickedEPN7cocos2d3RefEiE3$_0NS_9allocatorIS6_EEFvRK16eMessageBoxEventEEE`
- `0x0281DCF2`: `NSt6__ndk110__function6__funcIZN20LeagueDominionInfoUI25onAllShieldEnabledClickedEPN7cocos2d3RefEE3$_0NS_9allocatorIS6_EEFvRK16eMessageBoxEventEEE`
- `0x0281DBA6`: `NSt6__ndk110__function6__funcIZZN20LeagueDominionInfoUI22onShieldEnabledClickedEPN7cocos2d3RefEiENK3$_0clERK16eMessageBoxEventEUlvE_NS_9allocatorISA_EEFvvEEE`
- `0x0281DD85`: `NSt6__ndk110__function6__funcIZZN20LeagueDominionInfoUI25onAllShieldEnabledClickedEPN7cocos2d3RefEENK3$_0clERK16eMessageBoxEventEUlvE_NS_9allocatorISA_EEFvvEEE`
- `0x025B1822`: `Panel_shield`
- `0x025B3906`: `Shield`
- `0x025A3562`: `ShieldCost`
- `0x025651FF`: `ShieldTime`
- `0x0281DCAB`: `ZN20LeagueDominionInfoUI22onShieldEnabledClickedEPN7cocos2d3RefEiE3$_0`
- `0x0281DE8E`: `ZN20LeagueDominionInfoUI25onAllShieldEnabledClickedEPN7cocos2d3RefEE3$_0`
- `0x0281DC44`: `ZZN20LeagueDominionInfoUI22onShieldEnabledClickedEPN7cocos2d3RefEiENK3$_0clERK16eMessageBoxEventEUlvE_`
- `0x0281DE25`: `ZZN20LeagueDominionInfoUI25onAllShieldEnabledClickedEPN7cocos2d3RefEENK3$_0clERK16eMessageBoxEventEUlvE_`
- `0x006CC0F1`: `_ZN10CGameLogic15getShieldServerEv`
- `0x00A0C87F`: `_ZN10KingdomMap12canUseShieldEv`
- `0x00A0C89F`: `_ZN10KingdomMap23checkAndNoticeShieldUseEv`
- `0x00D0251B`: `_ZN20LeagueDominionInfoUI22onShieldEnabledClickedEPN7cocos2d3RefEi`
- `0x00D01F7B`: `_ZN20LeagueDominionInfoUI25onAllShieldEnabledClickedEPN7cocos2d3RefE`
- `0x00D02D77`: `_ZN22LeagueDominionInfoCell15onShieldClickedEPN7cocos2d3RefEi`
- `0x02617DF1`: `domain_war_shield_tips`
- `0x025E692D`: `guild_msg_dominion_shield`
- `0x025ECE5F`: `m_pBtnShield`
- `0x025C57B8`: `m_pButtonShield`
- `0x025FF676`: `m_pImgShield`
- `0x025631BA`: `m_pListViewShield`
- `0x0259850C`: `no_activate_shield_tips`
- `0x0259234C`: `open_shield_all`
- `0x025FDE1E`: `open_shield_single`
- `0x0259CFD4`: `shield_cd_text`
- `0x0259D018`: `shield_continues_text`
- `0x02575BA7`: `shield_mithril_cost`
- `0x025FD938`: `shield_server`
- `0x025CC0E3`: `touchShield`
- `0x025766A1`: `ui/chat_talkinfo_shields.csb`
- `0x02591341`: `ui/chat_talkinfo_shields_cell.csb`

### Boost (5)

- `0x006A3507`: `_ZN5boost8lockfree5queueIP13DownloaderResNS0_8capacityILm1024EEENS_9parameter5void_ES7_ED2Ev`
- `0x008B54C3`: `_ZN5boost8lockfree5queueIPN15HeroDataManager15PostWebHeroInfoENS0_8capacityILm1024EEENS_9parameter5void_ES8_ED2Ev`
- `0x0262B7F5`: `black_current_coming_boost_text_1`
- `0x025FE76E`: `black_current_coming_boost_text_11`
- `0x02584276`: `black_current_coming_boost_text_5`

### Food (98)

- `0x028743C8`: `15PetExchangeFood`
- `0x025F37C7`: `Button_AddFood`
- `0x026DF14C`: `NSt6__ndk110__function6__baseIFvRK28CMSG_PET_EXCHNGE_FOOD_RETURNEEE`
- `0x026DF0B0`: `NSt6__ndk110__function6__funcINS_6__bindIM10PetManagerFvRK28CMSG_PET_EXCHNGE_FOOD_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x028743DA`: `NSt6__ndk110__function6__funcINS_6__bindIM15PetExchangeFoodFvvEJPS3_EEENS_9allocatorIS7_EEFvvEEE`
- `0x028AD456`: `NSt6__ndk110__function6__funcIZN11CWishPoolUI15onClickWishFoodEvE3$_0NS_9allocatorIS3_EEFvRK16eMessageBoxEventEEE`
- `0x026DEF9E`: `NSt6__ndk110__function6__funcIZN14MessageSubject16registerListenerI28CMSG_PET_EXCHNGE_FOOD_RETURNEEvPvRKNS_8functionIFvRKT_EEEEUlPKcE_NS_9allocatorISG_EEFvSF_EEE`
- `0x028744A4`: `NSt6__ndk114unary_functionIP15PetExchangeFoodvEE`
- `0x026DF24C`: `NSt6__ndk115binary_functionIP10PetManagerRK28CMSG_PET_EXCHNGE_FOOD_RETURNvEE`
- `0x026DF1FA`: `NSt6__ndk118__weak_result_typeIM10PetManagerFvRK28CMSG_PET_EXCHNGE_FOOD_RETURNEEE`
- `0x0287446C`: `NSt6__ndk118__weak_result_typeIM15PetExchangeFoodFvvEEE`
- `0x026DF190`: `NSt6__ndk16__bindIM10PetManagerFvRK28CMSG_PET_EXCHNGE_FOOD_RETURNEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x0287443B`: `NSt6__ndk16__bindIM15PetExchangeFoodFvvEJPS1_EEE`
- `0x0262DBA8`: `ScoreFood`
- `0x02626819`: `UDEF_FoodLv`
- `0x028AD4C8`: `ZN11CWishPoolUI15onClickWishFoodEvE3$_0`
- `0x026DF040`: `ZN14MessageSubject16registerListenerI28CMSG_PET_EXCHNGE_FOOD_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEEEUlPKcE_`
- `0x00981DBA`: `_ZN10PetManager20getExchangeFoodCountEv`
- `0x00981B54`: `_ZN10PetManager22requestPetExchangeFoodEi`
- `0x009803BD`: `_ZN10PetManager23responsePetExchangeFoodERK28CMSG_PET_EXCHNGE_FOOD_RETURN`
- `0x00E70E60`: `_ZN11CWishPoolUI15onClickWishFoodEv`
- `0x00980407`: `_ZN14MessageSubject16registerListenerI28CMSG_PET_EXCHNGE_FOOD_RETURNEEvPvRKNSt6__ndk18functionIFvRKT_EEE`
- `0x00DE06E4`: `_ZN15PetExchangeFood12initControlsEv`
- `0x00DE04E9`: `_ZN15PetExchangeFood13getUIFilePathEv`
- `0x00DE0555`: `_ZN15PetExchangeFood14bindControllerERKNSt6__ndk18functionIFPN7cocos2d4NodeERKNS0_12basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEbEEERKNS1_IFbSC_RKNS1_IFvvEEEEEERKNS1_IFbPNS2_2ui6WidgetESK_EEE`
- `0x00DE050F`: `_ZN15PetExchangeFood15SC_UI_FILE_PATHE`
- `0x00DE0685`: `_ZN15PetExchangeFood23onExchangeButtonClickedEv`
- `0x00DE0536`: `_ZN15PetExchangeFood7onCloseEv`
- `0x00DE0709`: `_ZN15PetExchangeFood8initDataERKN4Core10DataStreamE`
- `0x00DE073D`: `_ZN15PetExchangeFood9getDialogEv`
- `0x00DE0A06`: `_ZN15PetExchangeFoodC1Ev`
- `0x00DE03AB`: `_ZN15PetExchangeFoodC2Ev`
- `0x00DE046E`: `_ZN15PetExchangeFoodD0Ev`
- `0x00DE0413`: `_ZN15PetExchangeFoodD1Ev`
- `0x00DE03DA`: `_ZN15PetExchangeFoodD2Ev`
- `0x009FD20D`: `_ZN16CWishPoolManager27isFirstTimesUseGoldWishFoodEv`
- `0x009FD2AD`: `_ZN16CWishPoolManager28setFirstTimesUseGoldWishFoodEb`
- `0x00BFAC08`: `_ZN23EventPageSweetyActivity14onAddFoodClickEi`
- `0x00BFAE48`: `_ZN23EventPageSweetyActivity15onFoodItemClickEi`
- `0x00BFAC37`: `_ZN23EventPageSweetyActivity17setFoodsByPlateIDE24eSweetyActivityPlateType`
- *...and 58 more*

### Stone (180)

- `0x027E7DC7`: `15MilestoneTaskUI`
- `0x027E7DD9`: `17MilestoneTaskCell`
- `0x027E7DED`: `20MilestoneTaskSubCell`
- `0x027E5BC7`: `24FriendMilestonePackageUI`
- `0x025DA834`: `CostOne`
- `0x025BD158`: `LuckyStoneItemId`
- `0x027E7332`: `NSt6__ndk110__function6__funcINS_6__bindIM24FriendMilestonePackageUIFvPN7cocos2d11EventCustomEEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x027E71FC`: `NSt6__ndk110__function6__funcINS_6__bindIM24FriendMilestonePackageUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x027E8761`: `NSt6__ndk110__function6__funcIZN15MilestoneTaskUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EESJ_EE`
- `0x027E8922`: `NSt6__ndk110__function6__funcIZN15MilestoneTaskUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_1NSA_ISY_EESJ_EE`
- `0x027E8AE3`: `NSt6__ndk110__function6__funcIZN17MilestoneTaskCell14bindControllerEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefEEEE`
- `0x027E7029`: `NSt6__ndk110__function6__funcIZN24FriendMilestonePackageUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EESJ_EE`
- `0x027E72F8`: `NSt6__ndk114unary_functionIP24FriendMilestonePackageUIvEE`
- `0x027E749C`: `NSt6__ndk115binary_functionIP24FriendMilestonePackageUIPN7cocos2d11EventCustomEvEE`
- `0x027E7444`: `NSt6__ndk118__weak_result_typeIM24FriendMilestonePackageUIFvPN7cocos2d11EventCustomEEEE`
- `0x027E72B7`: `NSt6__ndk118__weak_result_typeIM24FriendMilestonePackageUIFvvEEE`
- `0x027E73D4`: `NSt6__ndk16__bindIM24FriendMilestonePackageUIFvPN7cocos2d11EventCustomEEJPS1_RKNS_12placeholders4__phILi1EEEEEE`
- `0x027E727D`: `NSt6__ndk16__bindIM24FriendMilestonePackageUIFvvEJPS1_EEE`
- `0x025894E5`: `Pack_Moonstone`
- `0x027E8853`: `ZN15MilestoneTaskUI14bindControllerERKNSt6__ndk18functionIFPN7cocos2d4NodeERKNS0_12basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEbEEERKNS1_IFbSC_RKNS1_IFvvEEEEEERKNS1_IFbPNS2_2ui6WidgetESK_EEEE3$_0`
- `0x027E8A14`: `ZN15MilestoneTaskUI14bindControllerERKNSt6__ndk18functionIFPN7cocos2d4NodeERKNS0_12basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEbEEERKNS1_IFbSC_RKNS1_IFvvEEEEEERKNS1_IFbPNS2_2ui6WidgetESK_EEEE3$_1`
- `0x027E8B55`: `ZN17MilestoneTaskCell14bindControllerEvE3$_0`
- `0x027E7124`: `ZN24FriendMilestonePackageUI14bindControllerERKNSt6__ndk18functionIFPN7cocos2d4NodeERKNS0_12basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEbEEERKNS1_IFbSC_RKNS1_IFvvEEEEEERKNS1_IFbPNS2_2ui6WidgetESK_EEEE3$_0`
- `0x00C6A2C8`: `_ZN11FriendUINew17showMilestonePageEv`
- `0x00CB13EC`: `_ZN11HeroBadgeUp17_updateStoneCountEi`
- `0x00B14A16`: `_ZN15BadgeFusionList15updateLeftStoneEv`
- `0x00C6E5A0`: `_ZN15MilestoneTaskUI11setShowFlagEib`
- `0x00C6E23E`: `_ZN15MilestoneTaskUI12initControlsEv`
- `0x00C6E112`: `_ZN15MilestoneTaskUI13getUIFilePathEv`
- `0x00C6E138`: `_ZN15MilestoneTaskUI14bindControllerERKNSt6__ndk18functionIFPN7cocos2d4NodeERKNS0_12basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEbEEERKNS1_IFbSC_RKNS1_IFvvEEEEEERKNS1_IFbPNS2_2ui6WidgetESK_EEE`
- `0x00C6E32C`: `_ZN15MilestoneTaskUI14updateTaskListEv`
- `0x00C6E3F5`: `_ZN15MilestoneTaskUI16tableCellAtIndexEPN7cocos2d9extension9TableViewEl`
- `0x00C6E2A6`: `_ZN15MilestoneTaskUI17initEventListenerEv`
- `0x00C6DFAE`: `_ZN15MilestoneTaskUI19removeEventListenerEv`
- `0x00C6E353`: `_ZN15MilestoneTaskUI21tableCellSizeForIndexEPN7cocos2d9extension9TableViewEl`
- `0x00C6E4FA`: `_ZN15MilestoneTaskUI24numberOfCellsInTableViewEPN7cocos2d9extension9TableViewE`
- `0x00C6E263`: `_ZN15MilestoneTaskUI8initDataEPKv`
- `0x00C6EB37`: `_ZN15MilestoneTaskUI9getDialogEv`
- `0x00C6E285`: `_ZN15MilestoneTaskUI9refreshUIEv`
- `0x00C6DF4D`: `_ZN15MilestoneTaskUIC1Ev`
- *...and 140 more*

### Wood (28)

- `0x028AD3BC`: `NSt6__ndk110__function6__funcIZN11CWishPoolUI15onClickWishWoodEvE3$_0NS_9allocatorIS3_EEFvRK16eMessageBoxEventEEE`
- `0x0259272E`: `UDEF_WoodLv`
- `0x028AD42E`: `ZN11CWishPoolUI15onClickWishWoodEvE3$_0`
- `0x00E70E3C`: `_ZN11CWishPoolUI15onClickWishWoodEv`
- `0x009FD1D8`: `_ZN16CWishPoolManager27isFirstTimesUseGoldWishWoodEv`
- `0x009FD277`: `_ZN16CWishPoolManager28setFirstTimesUseGoldWishWoodEb`
- `0x007C3312`: `_ZN6Player10getWoodNumEv`
- `0x00DA1F76`: `_ZN7CMainUI22onPlayerAttrChangeWoodEv`
- `0x00E49B75`: `_ZN8CTradeUI10setWoodNumEi`
- `0x00E49DAE`: `_ZN8CTradeUI17onWoodSliderLogicEv`
- `0x00E49A7B`: `_ZN8CTradeUI23onTextFieldCallbackWoodEPN7cocos2d3RefENS0_2ui9TextField9EventTypeE`
- `0x025EB313`: `m_pLayerwoodA`
- `0x02604997`: `m_pLayerwoodA_floor`
- `0x025837BA`: `m_pLayerwoodB`
- `0x02617EEB`: `m_pLayerwoodB_floor`
- `0x025FDEBA`: `m_pLayerwoodC`
- `0x02575CBF`: `m_pLayerwoodC_floor`
- `0x02589EC3`: `m_pLayerwoodD`
- `0x025C3BDB`: `m_pLayerwoodD_floor`
- `0x025D7A93`: `m_pTextWood`
- `0x025F3D73`: `m_pTextWood_Num`
- `0x02617F35`: `m_pWoodImgLockTipA`
- `0x025D126B`: `m_pWoodImgLockTipB`
- `0x025837C8`: `m_pWoodImgLockTipC`
- `0x0259D0D0`: `m_pWoodImgLockTipD`
- `0x0261E3C1`: `m_pWoodTextLockTip%d`
- `0x025D127E`: `m_pWoodTxtLockTipBg%d`
- `0x025A4807`: `wood`

### Ore (4834)

- `0x025C91B9`: `            Not Before: `
- `0x028BBD7A`: ` AN7cocos2d17PUGeometryRotatorE`
- `0x02586822`: `%s%sclose instead of sending %ld more bytes`
- `0x025B9F9A`: `%s%sclose instead of sending unknown amount of more bytes`
- `0x0289CE6E`: `14AppShopScoreUI`
- `0x02870F44`: `15BattleScoreCell`
- `0x027A8239`: `15EventLuckyStore`
- `0x026878C7`: `15LogicLuckyStore`
- `0x02727ECF`: `16CIgnoreScaleNode`
- `0x02874DA4`: `16PetHuntScoreCell`
- `0x027DCBAC`: `17FortresWarScoreUI`
- `0x027372CF`: `18AchievementScoreUI`
- `0x0263C560`: `19CSpecialStoreConfig`
- `0x027DCA84`: `19FortresWarScoreCell`
- `0x028B5AE1`: `19Lost_event_scoreXml`
- `0x02760750`: `19OverlordScoreUICell`
- `0x028B6783`: `19Rush_event_scoreXml`
- `0x027372E4`: `20AchievementScoreCell`
- `0x0274A5D1`: `20ClanWarScoreResultUI`
- `0x0274DAD6`: `20ElementalScoreUICell`
- `0x02750A7B`: `21EmperorWarScoreUICell`
- `0x027D2D80`: `21OpenSesameHeroRecover`
- `0x02740305`: `22ChessBattleScoreUICell`
- `0x0283F2E5`: `22LegionSeasonWarScoreUI`
- `0x02760398`: `23ActivityOverlordScoreUI`
- `0x028B5853`: `23Lord_war_event_scoreXml`
- `0x028725CE`: `23OverlordSelfScoreInfoUI`
- `0x0272FBD8`: `23TutFunc_WaitForEnterMap`
- `0x0274D901`: `24ActivityElementalScoreUI`
- `0x027DCBC0`: `24ElementalWarScoreGetCell`
- `0x0283D4BD`: `24LegionSeasonWarScoreCell`
- `0x028B5BB3`: `24Lost_rush_event_scoreXml`
- `0x0272FC9D`: `24TutFunc_WaitForEnterCity`
- `0x02750802`: `25ActivityEmperorWarScoreUI`
- `0x028B424A`: `25Bloody_war_event_scoreXml`
- `0x0274A5B5`: `25ClanWarScoreCompareViewUI`
- `0x02729479`: `25GuideFunc_WaitForEnterMap`
- `0x0273FBDF`: `26ActivityChessBattleScoreUI`
- `0x0273F3ED`: `26BlackKnightActivityScoreUI`
- `0x02753974`: `26GuildStandoffTaskScoreItem`
- *...and 4794 more*

### Gold (963)

- `0x028B68C7`: `12Shop_goldXml`
- `0x026A592D`: `15GoldGiftManager`
- `0x028B620D`: `16Pet_feed_goldXml`
- `0x027E43E8`: `18FriendGoldRankCell`
- `0x0272C6CE`: `22TutCond_HaveGoldWorker`
- `0x027F7949`: `23CGiftPackDetailCellGold`
- `0x027968B3`: `33EventOperationsPageNewGoldConsume`
- `0x025CD23E`: `ActivityGold`
- `0x025EA970`: `BuyGoldTime`
- `0x0256B712`: `ChargeGold`
- `0x02565289`: `Cost_gold`
- `0x02599548`: `Cost_gold_n`
- `0x02575598`: `Draw_GoldTen_Limit`
- `0x025D09A1`: `Draw_Gold_Limit`
- `0x0261EBCF`: `EVENT_BANK_GOLD_NUM_SET`
- `0x025620D8`: `Employ_Gold`
- `0x025B0599`: `Gold`
- `0x0261A221`: `Gold%d`
- `0x025C349F`: `GoldItemId`
- `0x025B9CE9`: `GoldNum`
- `0x025BD02A`: `GoldTenItemId`
- `0x025F7404`: `Gold_cost`
- `0x02582DEB`: `GoldoCost`
- `0x025FA8AE`: `Golds`
- `0x025931D5`: `GrandPrizeGold`
- `0x0259D1B4`: `HaveGoldWorker`
- `0x025863BD`: `InviteGold`
- `0x025FA762`: `InviteGoldLimit`
- `0x025896DC`: `ItemGold`
- `0x025BCFCD`: `ItemGoldTen`
- `0x026DEE5D`: `NSt6__ndk110__function6__baseIFvRK25CMSG_PET_FEED_GOLD_RETURNEEE`
- `0x026EB93F`: `NSt6__ndk110__function6__baseIFvRK26CMSG_INVITE_GOLD_LIST_RESPEEE`
- `0x026B3E25`: `NSt6__ndk110__function6__baseIFvRK27CMSG_LATCH_GOLD_PASS_RETURNEEE`
- `0x026A6B18`: `NSt6__ndk110__function6__baseIFvRK29CMSG_GOODLUCK_GOLD_BUY_RETURNEEE`
- `0x02691D31`: `NSt6__ndk110__function6__baseIFvRK35CMSG_SYNC_DAILYCONSUME_GOLD_CONSUMEEEE`
- `0x02690F8E`: `NSt6__ndk110__function6__baseIFvRK39CMSG_CONTINUITY_GIFTPACK_GOLDBUY_RETURNEEE`
- `0x026FA8CA`: `NSt6__ndk110__function6__baseIFvRK41CMSG_SUPERCHAMPIONSHIP_GOLD_UNLOCK_RETURNEEE`
- `0x026DEDC4`: `NSt6__ndk110__function6__funcINS_6__bindIM10PetManagerFvRK25CMSG_PET_FEED_GOLD_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026A6A78`: `NSt6__ndk110__function6__funcINS_6__bindIM13LogicGoodLuckFvRK29CMSG_GOODLUCK_GOLD_BUY_RETURNEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISF_EEFvS6_EEE`
- `0x026A593F`: `NSt6__ndk110__function6__funcINS_6__bindIM15GoldGiftManagerFvPKcEJPS3_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISE_EEFvS5_EEE`
- *...and 923 more*

### Token (400)

- `0x027E9050`: `22MyInvitedTokenRewardUI`
- `0x028B4D16`: `23Friend_invited_tokenXml`
- `0x028B476D`: `24Continuity_gift_tokenXml`
- `0x027E9069`: `24MyInvitedTokenRewardCell`
- `0x028B5298`: `28Kingdom_gift_reward_tokenXml`
- `0x027AFA64`: `34EventPageContinuityGiftPackTokenUI`
- `0x027AFA89`: `36EventPageContinuityGiftPackTokenCell`
- `0x0262C21B`: `?iggid=%lld&token=%s&server_id=%d&area_id=%d&lose_rank=%d&server_rank=%d&enable_se=%d&probability=%f&language=%s&http_url=%s`
- `0x0261A801`: `GroupToken`
- `0x025884AD`: `ICC or token signature`
- `0x025F554C`: `INVALID_TOKEN`
- `0x006896D5`: `Java_com_jniCallback_onFetchToken`
- `0x00689BBE`: `Java_com_jniCallback_requestSSOTokenCallback`
- `0x0261BBDC`: `NEW_TOKEN`
- `0x025DBB45`: `NEW_TOKEN can only be sent by a server`
- `0x025F5500`: `NEW_TOKEN valid only in 1-RTT`
- `0x027E9E6A`: `NSt6__ndk110__function6__funcINS_6__bindIM22MyInvitedTokenRewardUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x027B0A24`: `NSt6__ndk110__function6__funcINS_6__bindIM34EventPageContinuityGiftPackTokenUIFvvEJPS3_EEENS_9allocatorIS7_EEFvPN7cocos2d11EventCustomEEEE`
- `0x02636859`: `NSt6__ndk110__function6__funcIZ33Java_com_jniCallback_onFetchTokenE3$_0NS_9allocatorIS2_EEFvvEEE`
- `0x02637346`: `NSt6__ndk110__function6__funcIZ44Java_com_jniCallback_requestSSOTokenCallbackE3$_0NS_9allocatorIS2_EEFvvEEE`
- `0x02638328`: `NSt6__ndk110__function6__funcIZN11AuthManager24initSSOTokenCallBackDataEvE3$_0NS_9allocatorIS3_EEFvRKNS_12basic_stringIcNS_11char_traitsIcEENS4_IcEEEESC_EEE`
- `0x02638459`: `NSt6__ndk110__function6__funcIZN11AuthManager24initSSOTokenCallBackDataEvE3$_1NS_9allocatorIS3_EEFvRKNS_12basic_stringIcNS_11char_traitsIcEENS4_IcEEEESC_EEE`
- `0x02638527`: `NSt6__ndk110__function6__funcIZN11AuthManager24initSSOTokenCallBackDataEvE3$_2NS_9allocatorIS3_EEFvRKNS_12basic_stringIcNS_11char_traitsIcEENS4_IcEEEESC_EEE`
- `0x026E83EE`: `NSt6__ndk110__function6__funcIZN16CFacebookManager18FetchFacebookTokenERKNS_8functionIFvNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEEEEE3$_0NS7_ISE_EESA_EE`
- `0x027F6457`: `NSt6__ndk110__function6__funcIZN20CGiftPackBuyItemCell9initTokenEiRKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEESA_SA_iRKNS_8functionIFivEEEE3$_0NS6_ISG_EEFviiEEE`
- `0x027E9ACC`: `NSt6__ndk110__function6__funcIZN22MyInvitedTokenRewardUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EESJ_EE`
- `0x027E9C9B`: `NSt6__ndk110__function6__funcIZN22MyInvitedTokenRewardUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_1NSA_ISY_EESJ_EE`
- `0x027E9F98`: `NSt6__ndk110__function6__funcIZN24MyInvitedTokenRewardCell14bindControllerEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefEEEE`
- `0x02754C7A`: `NSt6__ndk110__function6__funcIZN25KingdomGiftRewardItemCell7setDataEPK20SKingdomGiftTokenCfgiE3$_0NS_9allocatorIS6_EEFviiEEE`
- `0x027B0B82`: `NSt6__ndk110__function6__funcIZN36EventPageContinuityGiftPackTokenCell14bindControllerEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefEEEE`
- `0x027E9F60`: `NSt6__ndk114unary_functionIP22MyInvitedTokenRewardUIvEE`
- `0x027B0B3E`: `NSt6__ndk114unary_functionIP34EventPageContinuityGiftPackTokenUIvEE`
- `0x027E9F21`: `NSt6__ndk118__weak_result_typeIM22MyInvitedTokenRewardUIFvvEEE`
- `0x027B0AF3`: `NSt6__ndk118__weak_result_typeIM34EventPageContinuityGiftPackTokenUIFvvEEE`
- `0x027E9EE9`: `NSt6__ndk16__bindIM22MyInvitedTokenRewardUIFvvEJPS1_EEE`
- `0x027B0AAF`: `NSt6__ndk16__bindIM34EventPageContinuityGiftPackTokenUIFvvEJPS1_EEE`
- `0x0261A8FC`: `RewardToken`
- `0x025E0C72`: `RewardToken2`
- `0x0263087B`: `STATELESS_RESET_TOKEN appears multiple times`
- `0x025EF136`: `STATELESS_RESET_TOKEN encountered internal error`
- *...and 360 more*

### Fragment (60)

- `0x025941D2`: ` if ( texColor.a <= CC_alpha_value ) discard; gl_FragColor = texColor * v_fragmentColor; }`
- `0x025E8585`: ` texColor.a = texture2D(CC_Texture1, v_texCoord).r; if ( texColor.a <= 0.01 ) discard; gl_FragColor = texColor * v_fragmentColor; }`
- `0x02572EC1`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; uniform vec4 u_effectColor; uniform vec4 u_textColor; void main() { float dist = texture2D(CC_Texture0, v_texCoord).a; float width = 0.04; float alpha = smoothstep(0.5-width, 0.5+width, dist); float mu = smoothstep(0.5, 1.0, sqrt(dist)); vec4 color = u_effectColor*(1.0-alpha) + u_textColor*alpha; gl_FragColor = v_fragmentColor * vec4(color.rgb, max(alpha,mu)*color.a); }`
- `0x025C7B9E`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; uniform vec4 u_effectColor; uniform vec4 u_textColor; void main() { vec4 sample = texture2D(CC_Texture0, v_texCoord); float fontAlpha = sample.a; float outlineAlpha = sample.r; if (outlineAlpha > 0.0){ vec4 color = u_textColor * fontAlpha + u_effectColor * (1.0 - fontAlpha); gl_FragColor = v_fragmentColor * vec4( color.rgb,max(fontAlpha,outlineAlpha)*color.a); } else { discard; } }`
- `0x025DB4FE`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; uniform vec4 u_textColor; void main() { gl_FragColor = v_fragmentColor * vec4(u_textColor.rgb, u_textColor.a * texture2D(CC_Texture0, v_texCoord).a ); }`
- `0x026152AC`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; uniform vec4 u_textColor; void main() { vec4 color = texture2D(CC_Texture0, v_texCoord); float dist = color.a; float width = 0.04; float alpha = smoothstep(0.5-width, 0.5+width, dist) * u_textColor.a; gl_FragColor = v_fragmentColor * vec4(u_textColor.rgb,alpha); }`
- `0x0260E323`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; void main() { gl_FragColor = v_fragmentColor * texture2D(CC_Texture0, v_texCoord); }`
- `0x02601A28`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; void main() { gl_FragColor = vec4( v_fragmentColor.rgb, v_fragmentColor.a * texture2D(CC_Texture0, v_texCoord).a ); }`
- `0x0258D948`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; void main() { vec4 color = texture2D(CC_Texture0, v_texCoord); color.a = texture2D(CC_Texture1, v_texCoord).r; color = v_fragmentColor * color; if(color.b-color.g > 0.075 && color.b-color.r > 0.075) { color = vec4(color.b+(1.0-color.b)*0.2, color.g, color.r, color.a); } gl_FragColor = color; }`
- `0x025B44B0`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; void main() { vec4 color = v_fragmentColor * texture2D(CC_Texture0, v_texCoord); if(color.b-color.g > 0.075 && color.b-color.r > 0.075) { color = vec4(color.b+(1.0-color.b)*0.2, color.g, color.r, color.a); } gl_FragColor = color; }`
- `0x02566242`: ` varying vec4 v_fragmentColor; varying vec2 v_texCoord; void main() { vec4 color = vec4(0.0); color = texture2D(CC_Texture0, v_texCoord); color.a = texture2D(CC_Texture1, v_texCoord).r; gl_FragColor = v_fragmentColor * color; }`
- `0x025940BB`: ` varying vec4 v_fragmentColor; void main() { gl_FragColor = v_fragmentColor; }`
- `0x02621BFA`: ` void main() { gl_Position = CC_MVPMatrix * a_position; gl_PointSize = a_texCoord.x; v_fragmentColor = a_color; }`
- `0x0260E285`: ` void main() { gl_Position = CC_MVPMatrix * a_position; gl_PointSize = u_pointSize; v_fragmentColor = u_color; }`
- `0x025C7B03`: ` void main() { gl_Position = CC_MVPMatrix * a_position; v_fragmentColor = a_color; v_texCoord = a_texCoord; }`
- `0x025E1CBE`: ` void main() { gl_Position = CC_MVPMatrix * a_position; v_fragmentColor = a_color; }`
- `0x025CE13C`: ` void main() { gl_Position = CC_PMatrix * a_position; v_fragmentColor = a_color; v_texCoord = a_texCoord; }`
- `0x02572B53`: `<GLProgram = %08zX | Program = %i, VertexShader = %i, FragmentShader = %i>`
- `0x025ADE75`: `Bad fragment`
- `0x025666E8`: `EmptyFragments`
- `0x0259C4E0`: `Fragmentation of %d bytes reported as %d on page %d`
- `0x025D44F7`: `No fragment part in the URL`
- `0x02580C3C`: `SSL_CTX_set_tlsext_max_fragment_length`
- `0x010B57D8`: `SSL_CTX_set_tlsext_max_fragment_length`
- `0x010B5822`: `SSL_SESSION_get_max_fragment_length`
- `0x025B4DAD`: `SSL_set_tlsext_max_fragment_length`
- `0x010B57FF`: `SSL_set_tlsext_max_fragment_length`
- `0x025D46A5`: `[WS] CLOSE frame must not be fragmented`
- `0x025CDAEC`: `[WS] No ongoing fragmented message to continue`
- `0x02627A94`: `[WS] PING frame must not be fragmented`
- `0x025C73CA`: `[WS] PONG frame must not be fragmented`
- `0x025A7256`: `[WS] fragmented message interrupted by new BINARY msg`
- `0x025B3F94`: `[WS] fragmented message interrupted by new TEXT msg`
- `0x025EE80A`: `[WS] invalid fragmented CLOSE frame`
- `0x025E1538`: `[WS] invalid fragmented PING frame`
- `0x02586B25`: `[WS] invalid fragmented PONG frame`
- `0x025F4A1C`: `[WS] no flags given; interpreting as continuation fragment for compatibility`
- `0x025DAE56`: `[WS] no ongoing fragmented message to resume`
- `0x00AE98C4`: `_ZN24LostLandActivityPreStage23selectStageHeroFragmentEi`
- `0x00AE9B56`: `_ZN24LostLandActivityPreStage26setStageHeroFragmentEffectEib`
- *...and 20 more*

### Scroll (683)

- `0x027073A4`: `12ScrollFollow`
- `0x0282D011`: `17LeagueScrollMsgUI`
- `0x028B8E94`: `25CUIScrollViewTouchWrapper`
- `0x027337C8`: `25TutFunc_ScrollToRuinsDoor`
- `0x02734306`: `31TutFunc_ScrollToSpecPosInSesame`
- `0x0273327F`: `32TutFunc_SetTutorialScrollEnabled`
- `0x025F2A2D`: `ExtraRewardScrollToPos`
- `0x025E6023`: `LuckyWheelAutoScroll%lld`
- `0x025F8ED1`: `LuckyWheelScrollToPos`
- `0x028BFC8A`: `N10cocostudio16ScrollViewReaderE`
- `0x028C1BF3`: `N7cocos2d2ui10ScrollViewE`
- `0x028BAB0E`: `N7cocos2d9extension10ScrollViewE`
- `0x026FD193`: `N7cocos2d9extension18ScrollViewDelegateE`
- `0x02726B23`: `NSt6__ndk110__function6__baseIFvPN7cocos2d3RefENS2_2ui10ScrollView9EventTypeEEEE`
- `0x027A8C27`: `NSt6__ndk110__function6__funcINS_6__bindIM32EventOperationsPageCastleUpgradeFvPN7cocos2d3RefENS4_2ui10ScrollView9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x027A9155`: `NSt6__ndk110__function6__funcINS_6__bindIM35EventOperationsPageCastleUpgradeNewFvPN7cocos2d3RefENS4_2ui10ScrollView9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x02708DE5`: `NSt6__ndk110__function6__funcINS_6__bindIM38HackScrollViewForStoppedAnimatedScrollFbPN7cocos2d5TouchEPNS4_5EventEEJPS3_RKNS_12placeholders4__phILi1EEERKNSD_ILi2EEEEEENS_9allocatorISK_EEFbS6_S8_EEE`
- `0x02708FA5`: `NSt6__ndk110__function6__funcINS_6__bindIM38HackScrollViewForStoppedAnimatedScrollFvPN7cocos2d5TouchEPNS4_5EventEEJPS3_RKNS_12placeholders4__phILi1EEERKNSD_ILi2EEEEEENS_9allocatorISK_EEFvS6_S8_EEE`
- `0x027E4F19`: `NSt6__ndk110__function6__funcINS_6__bindIM8FriendUIFvPN7cocos2d3RefENS4_2ui10ScrollView9EventTypeEEJPS3_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS6_S9_EEE`
- `0x028BAB2F`: `NSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d9extension10ScrollViewEFbPNS3_5TouchEPNS3_5EventEEJPS5_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFbS7_S9_EEE`
- `0x028BAE03`: `NSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d9extension10ScrollViewEFvPNS3_4NodeEEJPS5_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISG_EEFvS7_EEE`
- `0x027E0399`: `NSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d9extension10ScrollViewEFvPNS3_5TouchEPNS3_5EventEEJP11CUIPageViewRKNS_12placeholders4__phILi1EEERKNSF_ILi2EEEEEENS_9allocatorISM_EEFvS7_S9_EEE`
- `0x028BACC8`: `NSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d9extension10ScrollViewEFvPNS3_5TouchEPNS3_5EventEEJPS5_RKNS_12placeholders4__phILi1EEERKNSE_ILi2EEEEEENS_9allocatorISL_EEFvS7_S9_EEE`
- `0x028BAFA4`: `NSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d9extension10ScrollViewEFvvEJPS5_EEENS_9allocatorIS9_EEFvvEEE`
- `0x0277CB5A`: `NSt6__ndk110__function6__funcIZN10ChatMainUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_1NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0277D803`: `NSt6__ndk110__function6__funcIZN10ChatMainUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_7NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0277DBA0`: `NSt6__ndk110__function6__funcIZN10ChatMainUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_9NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x02702037`: `NSt6__ndk110__function6__funcIZN10KingdomMap19scrollViewDidScrollEPN7cocos2d9extension10ScrollViewEE3$_0NS_9allocatorIS7_EEFvvEEE`
- `0x02723531`: `NSt6__ndk110__function6__funcIZN11CMainCityUI22moveScrollViewAndClickEi12BuildingTypeE3$_0NS_9allocatorIS4_EEFvlEEE`
- `0x027235E2`: `NSt6__ndk110__function6__funcIZN11CMainCityUI22moveScrollViewAndClickEi12BuildingTypeE3$_1NS_9allocatorIS4_EEFvlEEE`
- `0x02722C6D`: `NSt6__ndk110__function6__funcIZN11CMainCityUI24moveScrollViewToBuidlingERfiE3$_0NS_9allocatorIS4_EEFvvEEE`
- `0x0277F577`: `NSt6__ndk110__function6__funcIZN11ChatGroupUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_1NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0277FF9A`: `NSt6__ndk110__function6__funcIZN11GroupChatUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0277F0D4`: `NSt6__ndk110__function6__funcIZN12CLeagueBoard23initLeagueBoardChatListEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefENS6_2ui10ScrollView9EventTypeEEEE`
- `0x02873DAD`: `NSt6__ndk110__function6__funcIZN13PetCircleView16scrollToPetIndexEiE3$_0NS_9allocatorIS3_EEFvvEEE`
- `0x02825FF4`: `NSt6__ndk110__function6__funcIZN14LeagueInviteUI12initControlsEvE3$_0NS_9allocatorIS3_EEFvPN7cocos2d3RefENS6_2ui10ScrollView9EventTypeEEEE`
- `0x027D378E`: `NSt6__ndk110__function6__funcIZN14OpenSesameMain14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0284BD99`: `NSt6__ndk110__function6__funcIZN15CLordSkillUseUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0277E0CC`: `NSt6__ndk110__function6__funcIZN15ChatTwoPersonUI14bindControllerERKNS_8functionIFPN7cocos2d4NodeERKNS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEbEEERKNS3_IFbSE_RKNS3_IFvvEEEEEERKNS3_IFbPNS4_2ui6WidgetESM_EEEE3$_0NSA_ISY_EEFvPNS4_3RefENSR_10ScrollView9EventTypeEEEE`
- `0x0272169F`: `NSt6__ndk110__function6__funcIZN16CMainCityGuideUI24moveScrollViewToBuidlingEfiNS_8functionIFvvEEEE3$_0NS_9allocatorIS6_EES4_EE`
- *...and 643 more*

### Chest (1)

- `0x006AEF9C`: `_ZN11CBuffEffect21clearCacheStringValueEv`

### Key (5277)

- `0x026032D1`: `        Public key OCSP hash: `
- `0x02565B8A`: `   Unable to load public key`
- `0x025800C5`: `  Certificate level %d: Public key type %s%s (%d/%d Bits/secBits), signed using %s`
- `0x02580194`: ` public key hash: sha256//%s`
- `0x025E9B05`: `%*sContains Source Of Authority (SOA) Public Key Certificates: `
- `0x0261C9F4`: `%*sIssuer Key Hash: `
- `0x025678FB`: `%*sKey Id: `
- `0x02623269`: `%12sPublic Key Algorithm: `
- `0x0261CA60`: `%s PRIVATE KEY`
- `0x025C9D34`: `%s USING INTEGER PRIMARY KEY`
- `0x0256CECB`: `%s key generation:%s`
- `0x025A2C09`: `%s private key does not match its pubkey part`
- `0x025A93FF`: `%s public key hash mismatch`
- `0x02614DB9`: `-----BEGIN PUBLIC KEY-----`
- `0x02614DD5`: `-----END PUBLIC KEY-----`
- `0x028B679A`: `13Second_keyXml`
- `0x0287B425`: `15PrisionUseKeyUI`
- `0x025DD487`: `2kdf-key-check`
- `0x010BCC7E`: `AES_set_decrypt_key`
- `0x010BCC6A`: `AES_set_encrypt_key`
- `0x02589505`: `AFEvent key empty!!!: %d `
- `0x025A8D01`: `ANY PRIVATE KEY`
- `0x025E9AE5`: `AUTHORITY_KEYID`
- `0x010D6FC6`: `AUTHORITY_KEYID_free`
- `0x010D6F77`: `AUTHORITY_KEYID_it`
- `0x010D6FB2`: `AUTHORITY_KEYID_new`
- `0x02582A9D`: `AUTOINCREMENT is only allowed on an INTEGER PRIMARY KEY`
- `0x0261762A`: `AUTO_LOGIN_FLAG_KEY`
- `0x0068D9ED`: `AUTO_LOGIN_FLAG_KEY`
- `0x0260FDEB`: `Additional Platform Key Certificate`
- `0x0259B56A`: `Any Extended Key Usage`
- `0x025B0792`: `ApplyForceGrooveKeyEvent`
- `0x025952A1`: `Attestation Identity Key Certificate`
- `0x025CFBB9`: `Authority Key Identifier marked critical`
- `0x025DD119`: `BARE_PUBKEY`
- `0x010BF68C`: `BF_set_key`
- `0x02561CFF`: `Bad ptr map entry key=%d expected=(%d,%d) got=(%d,%d)`
- `0x025A91BA`: `CA cert does not include key usage extension`
- `0x02629973`: `CA certificate key too weak`
- `0x010C13EE`: `CAST_set_key`
- *...and 5237 more*

### Weapon (5)

- `0x027B55DB`: `NSt6__ndk110__function6__funcIZN26EventPageGiantInvasionGame16playWeaponActionENS2_12WeaponActionEE3$_0NS_9allocatorIS4_EEFvvEEE`
- `0x027B56A5`: `NSt6__ndk110__function6__funcIZN26EventPageGiantInvasionGame16playWeaponActionENS2_12WeaponActionEE3$_1NS_9allocatorIS4_EEFvvEEE`
- `0x027B565C`: `ZN26EventPageGiantInvasionGame16playWeaponActionENS_12WeaponActionEE3$_0`
- `0x027B5726`: `ZN26EventPageGiantInvasionGame16playWeaponActionENS_12WeaponActionEE3$_1`
- `0x00BE254C`: `_ZN26EventPageGiantInvasionGame16playWeaponActionENS_12WeaponActionE`

### Armor (23)

- `0x006AF464`: `_ZN23CBuildingFunctionConfig16readArmoryConfigEP12TiXmlElement`
- `0x006AFF2B`: `_ZN23CBuildingFunctionConfig17getArmoryFunctionE12BuildingTypei`
- `0x02575513`: `armory`
- `0x02571763`: `armory_forge_attr_lv_2`
- `0x025BFF4A`: `armory_forge_attr_name_2`
- `0x02618831`: `armory_forge_attr_name_3`
- `0x0260CDFD`: `armory_forge_count_blue`
- `0x02599221`: `armory_forge_count_red`
- `0x02614003`: `armory_forge_equip_count`
- `0x025EDC69`: `armory_forge_lv`
- `0x025FA318`: `armory_forge_name`
- `0x0260CE71`: `armory_forge_suits_num1`
- `0x02578353`: `armory_forge_suits_num2`
- `0x025C6616`: `armory_forge_suits_type3`
- `0x025F99B0`: `armory_forge_tips_1`
- `0x025AD03F`: `armory_forge_tips_4`
- `0x025BF630`: `armory_forge_tips_5`
- `0x02613FBB`: `armory_forge_title_1`
- `0x0257174E`: `armory_forge_title_2`
- `0x02620886`: `armory_forge_title_3`
- `0x0262089B`: `armory_forge_title_5`
- `0x02585E2E`: `armory_forge_title_6`
- `0x0260CE4C`: `armory_forge_title_7`

### Ring (7830)

- `0x0256E59B`: `()Ljava/lang/String;`
- `0x025EA7F1`: `(I)Ljava/lang/String;`
- `0x025BCDBF`: `(IILjava/lang/String;)V`
- `0x0258FE3D`: `(ILjava/lang/String;)V`
- `0x02621919`: `(ILjava/lang/String;F)V`
- `0x025E8311`: `(ILjava/lang/String;Ljava/lang/String;)V`
- `0x0258D798`: `(ILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V`
- `0x025F0E4B`: `(ILjava/lang/String;Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/String;)V`
- `0x02595F40`: `(ILjava/lang/String;[Ljava/lang/String;)V`
- `0x02595F6A`: `(I[Ljava/lang/String;[Ljava/lang/String;)V`
- `0x025B045C`: `(JLjava/lang/String;J)V`
- `0x025B68FE`: `(JLjava/lang/String;Ljava/lang/String;)V`
- `0x025729F6`: `(Ljava/lang/String;)Ljava/lang/Class;`
- `0x02627EC9`: `(Ljava/lang/String;)Ljava/net/HttpURLConnection;`
- `0x02609EE4`: `(Ljava/lang/String;)V`
- `0x025E192B`: `(Ljava/lang/String;)Z`
- `0x026218F2`: `(Ljava/lang/String;D)D`
- `0x025E81D4`: `(Ljava/lang/String;D)V`
- `0x0260DF5F`: `(Ljava/lang/String;F)F`
- `0x0261B3DD`: `(Ljava/lang/String;F)V`
- `0x025D49C5`: `(Ljava/lang/String;FF)Ljava/lang/String;`
- `0x0259A029`: `(Ljava/lang/String;I)I`
- `0x025B41DC`: `(Ljava/lang/String;I)V`
- `0x025B41A3`: `(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;`
- `0x02610CDF`: `(Ljava/lang/String;Ljava/lang/String;)V`
- `0x0256840A`: `(Ljava/lang/String;Ljava/lang/String;I)V`
- `0x025BA62C`: `(Ljava/lang/String;Ljava/lang/String;IIII)V`
- `0x026175F0`: `(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V`
- `0x025B687B`: `(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;II)V`
- `0x02575487`: `(Ljava/lang/String;Z)V`
- `0x025C7844`: `(Ljava/lang/String;Z)Z`
- `0x025655E9`: `(Ljava/lang/String;ZFFF)I`
- `0x0258D746`: `(Ljava/net/HttpURLConnection;)Ljava/lang/String;`
- `0x025E82DF`: `(Ljava/net/HttpURLConnection;Ljava/lang/String;)I`
- `0x025B4294`: `(Ljava/net/HttpURLConnection;Ljava/lang/String;)Ljava/lang/String;`
- `0x025EEC9F`: `(Ljava/net/HttpURLConnection;Ljava/lang/String;)V`
- `0x025DB29B`: `(Ljava/net/HttpURLConnection;Ljava/lang/String;Ljava/lang/String;)V`
- `0x026218BB`: `([BLjava/lang/String;IIIIIIIIZFFFFZIIIIF)Z`
- `0x025729CB`: `([BLjava/lang/String;Ljava/lang/String;)[B`
- `0x025A33EF`: `([Ljava/lang/String;[Ljava/lang/String;)V`
- *...and 7790 more*

### Other (4354)

- `0x0259C1F4`: `%s exceeds name buffer length`
- `0x025E11DF`: `%s pollset[] has POLLIN, but there is still buffered input to consume -> mark as dirty`
- `0x0286A501`: `10CNobleBuff`
- `0x0263C384`: `11CBuffConfig`
- `0x0263C392`: `11CBuffEffect`
- `0x0281529F`: `11ChessBuffUI`
- `0x0280330D`: `11HeroBadgeUp`
- `0x028A38DF`: `12CVipBuffCell`
- `0x02766291`: `14BadgeFusionUse`
- `0x027CF540`: `14CMonthCardBuff`
- `0x026F57BC`: `14VipBuffManager`
- `0x02765CD0`: `15BadgeFusionList`
- `0x0276E7C2`: `15BlackComingBuff`
- `0x027CF551`: `15CBattleCardBuff`
- `0x028032FB`: `15HeroBadgeUpCell`
- `0x028087FC`: `16CHeroRuneExample`
- `0x02782389`: `16CityBuffStatusUI`
- `0x02794EF0`: `16EmpireBuffInfoUI`
- `0x027FCC85`: `17ArmyBadgeUPInfoUI`
- `0x027855D4`: `17CBuildingBuffCell`
- `0x028152AD`: `17ChessBuffItemCell`
- `0x028B4703`: `17Collect_energyXml`
- `0x02803D17`: `17HeroBadgeUpUseTip`
- `0x026A9D6C`: `17LogicEvolvedBadge`
- `0x027CF578`: `18CMonthCardBuffCell`
- `0x027CF563`: `18CMonthCardBuffList`
- `0x027BF540`: `18CSubscriptionBuffs`
- `0x028A545A`: `18CWatchTowerDefBuff`
- `0x0278239C`: `18CityBuffStatusCell`
- `0x027FE4D2`: `18HeroBadgeAdvanceUI`
- `0x02803D2B`: `18HeroBadgeUpItemUse`
- `0x028948B3`: `18LordEquipBluePrint`
- `0x02850820`: `18LostLandCrystalMsg`
- `0x02854418`: `18LostLandUseCrystal`
- `0x027D09AC`: `18OpenSesameBuffView`
- `0x027FCC6F`: `19ArmyBadgeUPInfoCell`
- `0x02765544`: `19BadgeFusionBatchUse`
- `0x0276582B`: `19BadgeFusionChangeUI`
- `0x027CF58D`: `19CBattleCardBuffCell`
- `0x027DD1F6`: `19FortressWarBuffCell`
- *...and 4314 more*

---
## 6. JSON-Related Strings

**Total: 257 JSON-related strings**

| Offset | String |
|---|---|
| `0x025B0ED0` | `.json` |
| `0x025D7719` | `GrdyGameRportReview_%lld.json` |
| `0x0103FE6D` | `Json_create` |
| `0x0103FE60` | `Json_dispose` |
| `0x0103FE52` | `Json_getError` |
| `0x0103FE95` | `Json_getFloat` |
| `0x0103FEA3` | `Json_getInt` |
| `0x0103FE79` | `Json_getItem` |
| `0x0103FE86` | `Json_getString` |
| `0x028C01E1` | `NSt6__ndk110__function6__baseIFPN7cocos2d4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x028C0547` | `NSt6__ndk110__function6__baseIFPN7cocos2d9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x028C00F8` | `NSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_4NodeERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EEE` |
| `0x028C0459` | `NSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_9ComponentERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EEE` |
| `0x028C03C1` | `NSt6__ndk115binary_functionIPN7cocos2d8CSLoaderERKN9rapidjson12GenericValueINS4_4UTF8IcEENS4_19MemoryPoolAllocatorINS4_12CrtAllocatorEEEEEPNS1_4NodeEEE` |
| `0x028C0735` | `NSt6__ndk115binary_functionIPN7cocos2d8CSLoaderERKN9rapidjson12GenericValueINS4_4UTF8IcEENS4_19MemoryPoolAllocatorINS4_12CrtAllocatorEEEEEPNS1_9ComponentEEE` |
| `0x028C0324` | `NSt6__ndk118__weak_result_typeIMN7cocos2d8CSLoaderEFPNS1_4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x028C0693` | `NSt6__ndk118__weak_result_typeIMN7cocos2d8CSLoaderEFPNS1_9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x028C026F` | `NSt6__ndk16__bindIMN7cocos2d8CSLoaderEFPNS1_4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEJPS2_RKNS_12placeholders4__phILi1EEEEEE` |
| `0x028C05D9` | `NSt6__ndk16__bindIMN7cocos2d8CSLoaderEFPNS1_9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEJPS2_RKNS_12placeholders4__phILi1EEEEEE` |
| `0x006A9CFC` | `_ZGVZN9rapidjson12GenericValueINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEEixEPKcE9NullValue` |
| `0x01013D74` | `_ZN10cocostudio10ActionNode18initWithDictionaryERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPN7cocos2d3RefE` |
| `0x0103205F` | `_ZN10cocostudio10TextReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01014701` | `_ZN10cocostudio12ActionObject18initWithDictionaryERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPN7cocos2d3RefE` |
| `0x00C5EAB4` | `_ZN10cocostudio12ButtonReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102C33D` | `_ZN10cocostudio12LayoutReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102F914` | `_ZN10cocostudio12SliderReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01027F9A` | `_ZN10cocostudio12WidgetReader15getResourcePathERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEERKNSt6__ndk112basic_stringIcNSB_11char_traitsIcEENSB_9allocatorIcEEEEN7cocos2d2ui6Widget14TextureResTypeE` |
| `0x01027DE7` | `_ZN10cocostudio12WidgetReader23setAnchorPointForWidgetEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102757F` | `_ZN10cocostudio12WidgetReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x00C5EB5E` | `_ZN10cocostudio12WidgetReader31setColorPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102AF85` | `_ZN10cocostudio14CheckBoxReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102CE09` | `_ZN10cocostudio14ListViewReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102E40E` | `_ZN10cocostudio14PageViewReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x010135F4` | `_ZN10cocostudio15ActionManagerEx18initWithDictionaryEPKcRKN9rapidjson12GenericValueINS3_4UTF8IcEENS3_19MemoryPoolAllocatorINS3_12CrtAllocatorEEEEEPN7cocos2d3RefE` |
| `0x0102BA00` | `_ZN10cocostudio15ImageViewReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01030318` | `_ZN10cocostudio15TextAtlasReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0103150E` | `_ZN10cocostudio15TextFieldReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0101E02D` | `_ZN10cocostudio16DataReaderHelper10decodeBoneERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0101E1EF` | `_ZN10cocostudio16DataReaderHelper10decodeNodeEPNS_8BaseDataERKN9rapidjson12GenericValueINS3_4UTF8IcEENS3_19MemoryPoolAllocatorINS3_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0101E3D7` | `_ZN10cocostudio16DataReaderHelper11decodeFrameERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0101E163` | `_ZN10cocostudio16DataReaderHelper13decodeContourERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x0101D779` | `_ZN10cocostudio16DataReaderHelper13decodeTextureERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x0101D63E` | `_ZN10cocostudio16DataReaderHelper14decodeArmatureERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0101E0C6` | `_ZN10cocostudio16DataReaderHelper14decodeMovementERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0101D6DB` | `_ZN10cocostudio16DataReaderHelper15decodeAnimationERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0101E296` | `_ZN10cocostudio16DataReaderHelper17decodeBoneDisplayERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0101E336` | `_ZN10cocostudio16DataReaderHelper18decodeMovementBoneERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPNS0_9_DataInfoE` |
| `0x0102016F` | `_ZN10cocostudio16DictionaryHelper16getIntValue_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKci` |
| `0x01020824` | `_ZN10cocostudio16DictionaryHelper18getArrayCount_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKci` |
| `0x010206F8` | `_ZN10cocostudio16DictionaryHelper18getFloatValue_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcf` |
| `0x0101FFAC` | `_ZN10cocostudio16DictionaryHelper19getStringValue_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcSC_` |
| `0x0102078D` | `_ZN10cocostudio16DictionaryHelper20getBooleanValue_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcb` |
| `0x010200DB` | `_ZN10cocostudio16DictionaryHelper21checkObjectExist_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x01020BD3` | `_ZN10cocostudio16DictionaryHelper21checkObjectExist_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKc` |
| `0x01020C6A` | `_ZN10cocostudio16DictionaryHelper21checkObjectExist_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEi` |
| `0x01020044` | `_ZN10cocostudio16DictionaryHelper21getSubDictionary_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKc` |
| `0x010205CB` | `_ZN10cocostudio16DictionaryHelper21getSubDictionary_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKci` |
| `0x01020663` | `_ZN10cocostudio16DictionaryHelper21getSubDictionary_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEi` |
| `0x010208B9` | `_ZN10cocostudio16DictionaryHelper25getIntValueFromArray_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcii` |
| `0x010209F5` | `_ZN10cocostudio16DictionaryHelper26getBoolValueFromArray_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcib` |
| `0x01020B35` | `_ZN10cocostudio16DictionaryHelper27getDictionaryFromArray_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKci` |
| `0x01020956` | `_ZN10cocostudio16DictionaryHelper27getFloatValueFromArray_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcif` |
| `0x01020A93` | `_ZN10cocostudio16DictionaryHelper28getStringValueFromArray_jsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKciSC_` |
| `0x0102DB4F` | `_ZN10cocostudio16LoadingBarReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102CEB5` | `_ZN10cocostudio16ScrollViewReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01030C1D` | `_ZN10cocostudio16TextBMFontReader26setPropsFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x010218EB` | `_ZN10cocostudio22WidgetPropertiesReader23setAnchorPointForWidgetEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102145B` | `_ZN10cocostudio26WidgetPropertiesReader025012createWidgetERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcSC_` |
| `0x0102199C` | `_ZN10cocostudio26WidgetPropertiesReader025024widgetFromJsonDictionaryERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x01021E0C` | `_ZN10cocostudio26WidgetPropertiesReader025034setPropsForLabelFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01021BC4` | `_ZN10cocostudio26WidgetPropertiesReader025035setPropsForButtonFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01021F91` | `_ZN10cocostudio26WidgetPropertiesReader025035setPropsForLayoutFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01022117` | `_ZN10cocostudio26WidgetPropertiesReader025035setPropsForSliderFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01021A3D` | `_ZN10cocostudio26WidgetPropertiesReader025035setPropsForWidgetFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01021C85` | `_ZN10cocostudio26WidgetPropertiesReader025037setPropsForCheckBoxFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01022427` | `_ZN10cocostudio26WidgetPropertiesReader025038setPropsForAllWidgetFromJsonDictionaryEPNS_20WidgetReaderProtocolEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEE` |
| `0x01021D48` | `_ZN10cocostudio26WidgetPropertiesReader025038setPropsForImageViewFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x010221D8` | `_ZN10cocostudio26WidgetPropertiesReader025038setPropsForTextFieldFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01021ECC` | `_ZN10cocostudio26WidgetPropertiesReader025039setPropsForLabelAtlasFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x0102229C` | `_ZN10cocostudio26WidgetPropertiesReader025039setPropsForLoadingBarFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01022052` | `_ZN10cocostudio26WidgetPropertiesReader025039setPropsForScrollViewFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01021AFE` | `_ZN10cocostudio26WidgetPropertiesReader025040setColorPropsForWidgetFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01022361` | `_ZN10cocostudio26WidgetPropertiesReader025040setPropsForLabelBMFontFromJsonDictionaryEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x01022506` | `_ZN10cocostudio26WidgetPropertiesReader025044setPropsForAllCustomWidgetFromJsonDictionaryERKNSt6__ndk112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINSE_4UTF8IcEENSE_19MemoryPoolAllocatorINSE_12CrtAllocatorEEEEE` |
| `0x01021525` | `_ZN10cocostudio26WidgetPropertiesReader030012createWidgetERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEPKcSC_` |
| `0x0102271B` | `_ZN10cocostudio26WidgetPropertiesReader030024widgetFromJsonDictionaryERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x010227BC` | `_ZN10cocostudio26WidgetPropertiesReader030038setPropsForAllWidgetFromJsonDictionaryEPNS_20WidgetReaderProtocolEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEE` |
| `0x0102289B` | `_ZN10cocostudio26WidgetPropertiesReader030044setPropsForAllCustomWidgetFromJsonDictionaryERKNSt6__ndk112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEEPN7cocos2d2ui6WidgetERKN9rapidjson12GenericValueINSE_4UTF8IcEENSE_19MemoryPoolAllocatorINSE_12CrtAllocatorEEEEE` |
| `0x010349E6` | `_ZN10cocostudio8timeline19ActionTimelineCache12loadTimelineERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01034EEA` | `_ZN10cocostudio8timeline19ActionTimelineCache13loadSkewFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x010351FC` | `_ZN10cocostudio8timeline19ActionTimelineCache14loadColorFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01035330` | `_ZN10cocostudio8timeline19ActionTimelineCache14loadEventFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01034E51` | `_ZN10cocostudio8timeline19ActionTimelineCache14loadScaleFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x010353C9` | `_ZN10cocostudio8timeline19ActionTimelineCache15loadZOrderFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01035295` | `_ZN10cocostudio8timeline19ActionTimelineCache16loadTextureFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01034D1A` | `_ZN10cocostudio8timeline19ActionTimelineCache16loadVisibleFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01034DB5` | `_ZN10cocostudio8timeline19ActionTimelineCache17loadPositionFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01035022` | `_ZN10cocostudio8timeline19ActionTimelineCache17loadRotationFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x010350BE` | `_ZN10cocostudio8timeline19ActionTimelineCache20loadAnchorPointFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x0103515D` | `_ZN10cocostudio8timeline19ActionTimelineCache20loadInnerActionFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x01034F82` | `_ZN10cocostudio8timeline19ActionTimelineCache21loadRotationSkewFrameERKN9rapidjson12GenericValueINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x010212F5` | `_ZN10cocostudio9GUIReader23registerTypeAndCallBackERKNSt6__ndk112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEENS1_8functionIFPN7cocos2d3RefEvEEESD_MSC_FvS9_SD_RKN9rapidjson12GenericValueINSG_4UTF8IcEENSG_19MemoryPoolAllocatorINSG_12CrtAllocatorEEEEEE` |
| `0x01020EAF` | `_ZN10cocostudio9GUIReader23registerTypeAndCallBackERKNSt6__ndk112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEEPFPN7cocos2d3RefEvESC_MSB_FvS9_SC_RKN9rapidjson12GenericValueINSF_4UTF8IcEENSF_19MemoryPoolAllocatorINSF_12CrtAllocatorEEEEEE` |
| `0x00A48FAA` | `_ZN11CMainCityUI20jsonArrayTowaterArgsERKN9rapidjson12GenericValueINS0_4UTF8IcEENS0_19MemoryPoolAllocatorINS0_12CrtAllocatorEEEEERKNSt6__ndk112basic_stringIcNSA_11char_traitsIcEENSA_9allocatorIcEEEERNS_10SWaterArgsE` |
| `0x00A48F20` | `_ZN11CMainCityUI8addWaterEPKcPN7cocos2d4NodeERN9rapidjson15GenericDocumentINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x006A4678` | `_ZN15AssetDownloader8loadJsonERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERN9rapidjson15GenericDocumentINS9_4UTF8IcEENS9_19MemoryPoolAllocatorINS9_12CrtAllocatorEEEEE` |
| `0x010AB356` | `_ZN15UtilPlistReader12getJsonValueERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEERN9rapidjson15GenericDocumentINS9_4UTF8IcEENS9_19MemoryPoolAllocatorINS9_12CrtAllocatorEEEEE` |
| `0x00A46D15` | `_ZN16CMainCityGuideUI20jsonArrayTowaterArgsERKN9rapidjson12GenericValueINS0_4UTF8IcEENS0_19MemoryPoolAllocatorINS0_12CrtAllocatorEEEEERKNSt6__ndk112basic_stringIcNSA_11char_traitsIcEENSA_9allocatorIcEEEERNS_10SWaterArgsE` |
| `0x00A47876` | `_ZN16CMainCityGuideUI8addWaterEPKcPN7cocos2d4NodeERN9rapidjson15GenericDocumentINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEE` |
| `0x00FD0C56` | `_ZN7cocos2d11getChildMapERNSt6__ndk13mapIiNS0_6vectorIiNS0_9allocatorIiEEEENS0_4lessIiEENS3_INS0_4pairIKiS5_EEEEEEPNS_8SkinDataERKN9rapidjson12GenericValueINSG_4UTF8IcEENSG_19MemoryPoolAllocatorINSG_12CrtAllocatorEEEEE` |
| `0x00FD1DBD` | `_ZN7cocos2d8Bundle3D20loadMeshDataJson_0_1ERNS_9MeshDatasE` |
| `0x00FD2341` | `_ZN7cocos2d8Bundle3D20loadMeshDataJson_0_2ERNS_9MeshDatasE` |
| `0x00FD224A` | `_ZN7cocos2d8Bundle3D24loadMaterialDataJson_0_1ERNS_13MaterialDatasE` |
| `0x00FD228E` | `_ZN7cocos2d8Bundle3D24loadMaterialDataJson_0_2ERNS_13MaterialDatasE` |
| `0x00FD2083` | `_ZN7cocos2d8Bundle3D25parseNodesRecursivelyJsonERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEEb` |
| `0x01039DB1` | `_ZN7cocos2d8CSLoader10loadSpriteERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x01039F2C` | `_ZN7cocos2d8CSLoader10loadWidgetERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x0103A09A` | `_ZN7cocos2d8CSLoader12loadComAudioERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x01039E2D` | `_ZN7cocos2d8CSLoader12loadParticleERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x01039D33` | `_ZN7cocos2d8CSLoader12loadSubGraphERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x0103AEA7` | `_ZN7cocos2d8CSLoader13loadComponentERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x01039AD2` | `_ZN7cocos2d8CSLoader14loadSimpleNodeERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x01039EAB` | `_ZN7cocos2d8CSLoader15loadTMXTiledMapERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x0103A53E` | `_ZN7cocos2d8CSLoader8initNodeEPNS_4NodeERKN9rapidjson12GenericValueINS3_4UTF8IcEENS3_19MemoryPoolAllocatorINS3_12CrtAllocatorEEEEE` |
| `0x0103AC21` | `_ZN7cocos2d8CSLoader8loadNodeERKN9rapidjson12GenericValueINS1_4UTF8IcEENS1_19MemoryPoolAllocatorINS1_12CrtAllocatorEEEEE` |
| `0x00FDD5B1` | `_ZN7cocos2d9extension8Manifest10parseAssetERKNSt6__ndk112basic_stringIcNS2_11char_traitsIcEENS2_9allocatorIcEEEERKN9rapidjson12GenericValueINSB_4UTF8IcEENSB_19MemoryPoolAllocatorINSB_12CrtAllocatorEEEEE` |
| `0x00FDD3C5` | `_ZN7cocos2d9extension8Manifest11loadVersionERKN9rapidjson15GenericDocumentINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x00FDD2A0` | `_ZN7cocos2d9extension8Manifest12loadManifestERKN9rapidjson15GenericDocumentINS2_4UTF8IcEENS2_19MemoryPoolAllocatorINS2_12CrtAllocatorEEEEE` |
| `0x00FDD7FF` | `_ZN7cocos2d9extension8Manifest13parseModAssetERKNSt6__ndk112basic_stringIcNS2_11char_traitsIcEENS2_9allocatorIcEEEERKN9rapidjson12GenericValueINSB_4UTF8IcEENSB_19MemoryPoolAllocatorINSB_12CrtAllocatorEEEEE` |
| `0x006A9C8F` | `_ZN9rapidjson12GenericValueINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE9AddMemberERS6_S7_RS5_` |
| `0x006AB0C2` | `_ZN9rapidjson12PrettyWriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE10StartArrayEv` |
| `0x006AB353` | `_ZN9rapidjson12PrettyWriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE11StartObjectEv` |
| `0x006AB148` | `_ZN9rapidjson12PrettyWriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE12PrettyPrefixENS_4TypeE` |
| `0x006AB255` | `_ZN9rapidjson12PrettyWriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE6DoubleEd` |
| `0x006AB65F` | `_ZN9rapidjson12PrettyWriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE6Uint64Em` |
| `0x006AB55D` | `_ZN9rapidjson12PrettyWriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE8EndArrayEj` |
| `0x006AB4D9` | `_ZN9rapidjson12PrettyWriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE9EndObjectEj` |
| `0x006A4F3E` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE10ParseArrayILj0ENS_19GenericStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x00FD2665` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE10ParseArrayILj1ENS_25GenericInsituStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x006A50E9` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE10ParseValueILj0ENS_19GenericStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x00FD27D0` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE10ParseValueILj1ENS_25GenericInsituStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x006A533F` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseNumberILj0ENS_19GenericStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x00FD29D1` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseNumberILj1ENS_25GenericInsituStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x006A4E8E` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseObjectILj0ENS_19GenericStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x00FD25AF` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseObjectILj1ENS_25GenericInsituStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x006A5039` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseStringILj0ENS_19GenericStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x00FD271A` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseStringILj1ENS_25GenericInsituStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEvRT0_RT1_` |
| `0x006A4D82` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE5ParseILj0ENS_19GenericStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEbRT0_RT1_` |
| `0x00FD2500` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE5ParseILj1ENS_25GenericInsituStringStreamIS2_EENS_15GenericDocumentIS2_S5_EEEEbRT0_RT1_` |
| `0x006A5251` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE9ParseHex4INS_19GenericStringStreamIS2_EEEEjRT_` |
| `0x00FD2944` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE9ParseHex4INS_25GenericInsituStringStreamIS2_EEEEjRT_` |
| `0x006A4E2B` | `_ZN9rapidjson13GenericReaderINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEED2Ev` |
| `0x006A4738` | `_ZN9rapidjson15GenericDocumentINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseStreamILj0ENS_19GenericStringStreamIS2_EEEERS6_RT0_` |
| `0x00FD103C` | `_ZN9rapidjson15GenericDocumentINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE11ParseStreamILj1ENS_25GenericInsituStringStreamIS2_EEEERS6_RT0_` |
| `0x006A52D8` | `_ZN9rapidjson15GenericDocumentINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE6StringEPKcjb` |
| `0x006A933D` | `_ZN9rapidjson15GenericDocumentINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEED2Ev` |
| `0x006AB07B` | `_ZN9rapidjson19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEED2Ev` |
| `0x006A4FF5` | `_ZN9rapidjson19MemoryPoolAllocatorINS_12CrtAllocatorEE7ReallocEPvmm` |
| `0x006AB5E0` | `_ZN9rapidjson6WriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE10WriteInt64El` |
| `0x006AB3DA` | `_ZN9rapidjson6WriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE11WriteStringEPKcj` |
| `0x006AB45D` | `_ZN9rapidjson6WriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE8WriteIntEi` |
| `0x006AB1D8` | `_ZN9rapidjson6WriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE9WriteBoolEb` |
| `0x006AB2D6` | `_ZN9rapidjson6WriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEE9WriteNullEv` |
| `0x006AB006` | `_ZN9rapidjson6WriterINS_19GenericStringBufferINS_4UTF8IcEENS_12CrtAllocatorEEES3_NS_19MemoryPoolAllocatorIS4_EEED2Ev` |
| `0x006AAE04` | `_ZNK9rapidjson12GenericValueINS_4UTF8IcEENS_19MemoryPoolAllocatorINS_12CrtAllocatorEEEE6AcceptINS_12PrettyWriterINS_19GenericStringBufferIS2_S4_EES2_S5_EEEERKS6_RT_` |
| `0x0103B5CC` | `_ZNSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_4NodeERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EED0Ev` |
| `0x0103B9AC` | `_ZNSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_9ComponentERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EED0Ev` |
| `0x0102318B` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEMN7cocos2d3RefEFvRKS7_PS9_RKN9rapidjson12GenericValueINSD_4UTF8IcEENSD_19MemoryPoolAllocatorINSD_12CrtAllocatorEEEEEEEENS_22__unordered_map_hasherIS7_SP_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SP_SU_SS_Lb1EEENS5_ISP_EEE11__do_rehashILb1EEEvm` |
| `0x0102111A` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEMN7cocos2d3RefEFvRKS7_PS9_RKN9rapidjson12GenericValueINSD_4UTF8IcEENSD_19MemoryPoolAllocatorINSD_12CrtAllocatorEEEEEEEENS_22__unordered_map_hasherIS7_SP_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SP_SU_SS_Lb1EEENS5_ISP_EEE25__emplace_unique_key_argsIS7_JNS_4pairISA_SO_EEEEENS11_INS_15__hash_iteratorIPNS_11__hash_nodeISP_PvEEEEbEERKT_DpOT0_` |
| `0x01022B4A` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEEMN7cocos2d3RefEFvRKS7_PS9_RKN9rapidjson12GenericValueINSD_4UTF8IcEENSD_19MemoryPoolAllocatorINSD_12CrtAllocatorEEEEEEEENS_22__unordered_map_hasherIS7_SP_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SP_SU_SS_Lb1EEENS5_ISP_EEE25__emplace_unique_key_argsIS7_JRKNS_21piecewise_construct_tENS_5tupleIJSB_EEENS14_IJEEEEEENS_4pairINS_15__hash_iteratorIPNS_11__hash_nodeISP_PvEEEEbEERKT_DpOT0_` |
| `0x01034B63` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN10cocostudio8timeline5FrameERKN9rapidjson12GenericValueINSD_4UTF8IcEENSD_19MemoryPoolAllocatorINSD_12CrtAllocatorEEEEEEEEEENS_22__unordered_map_hasherIS7_SP_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SP_SU_SS_Lb1EEENS5_ISP_EEE4findIS7_EENS_15__hash_iteratorIPNS_11__hash_nodeISP_PvEEEERKT_` |
| `0x0103B82C` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d4NodeERKN9rapidjson12GenericValueINSC_4UTF8IcEENSC_19MemoryPoolAllocatorINSC_12CrtAllocatorEEEEEEEEEENS_22__unordered_map_hasherIS7_SO_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SO_ST_SR_Lb1EEENS5_ISO_EEE11__do_rehashILb1EEEvm` |
| `0x01039B52` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d4NodeERKN9rapidjson12GenericValueINSC_4UTF8IcEENSC_19MemoryPoolAllocatorINSC_12CrtAllocatorEEEEEEEEEENS_22__unordered_map_hasherIS7_SO_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SO_ST_SR_Lb1EEENS5_ISO_EEE25__emplace_unique_key_argsIS7_JNS_4pairIS7_SN_EEEEENS10_INS_15__hash_iteratorIPNS_11__hash_nodeISO_PvEEEEbEERKT_DpOT0_` |
| `0x0103AC9A` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d4NodeERKN9rapidjson12GenericValueINSC_4UTF8IcEENSC_19MemoryPoolAllocatorINSC_12CrtAllocatorEEEEEEEEEENS_22__unordered_map_hasherIS7_SO_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SO_ST_SR_Lb1EEENS5_ISO_EEE25__emplace_unique_key_argsIS7_JRKNS_21piecewise_construct_tENS_5tupleIJRKS7_EEENS13_IJEEEEEENS_4pairINS_15__hash_iteratorIPNS_11__hash_nodeISO_PvEEEEbEERKT_DpOT0_` |
| `0x0103BC1B` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d9ComponentERKN9rapidjson12GenericValueINSC_4UTF8IcEENSC_19MemoryPoolAllocatorINSC_12CrtAllocatorEEEEEEEEEENS_22__unordered_map_hasherIS7_SO_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SO_ST_SR_Lb1EEENS5_ISO_EEE11__do_rehashILb1EEEvm` |
| `0x0103A118` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d9ComponentERKN9rapidjson12GenericValueINSC_4UTF8IcEENSC_19MemoryPoolAllocatorINSC_12CrtAllocatorEEEEEEEEEENS_22__unordered_map_hasherIS7_SO_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SO_ST_SR_Lb1EEENS5_ISO_EEE25__emplace_unique_key_argsIS7_JNS_4pairIS7_SN_EEEEENS10_INS_15__hash_iteratorIPNS_11__hash_nodeISO_PvEEEEbEERKT_DpOT0_` |
| `0x0103AF26` | `_ZNSt6__ndk112__hash_tableINS_17__hash_value_typeINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d9ComponentERKN9rapidjson12GenericValueINSC_4UTF8IcEENSC_19MemoryPoolAllocatorINSC_12CrtAllocatorEEEEEEEEEENS_22__unordered_map_hasherIS7_SO_NS_4hashIS7_EENS_8equal_toIS7_EELb1EEENS_21__unordered_map_equalIS7_SO_ST_SR_Lb1EEENS5_ISO_EEE25__emplace_unique_key_argsIS7_JRKNS_21piecewise_construct_tENS_5tupleIJRKS7_EEENS13_IJEEEEEENS_4pairINS_15__hash_iteratorIPNS_11__hash_nodeISO_PvEEEEbEERKT_DpOT0_` |
| `0x0103A3D0` | `_ZNSt6__ndk14pairINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d4NodeERKN9rapidjson12GenericValueINSB_4UTF8IcEENSB_19MemoryPoolAllocatorINSB_12CrtAllocatorEEEEEEEEED2Ev` |
| `0x0103A2FE` | `_ZNSt6__ndk14pairINS_12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_8functionIFPN7cocos2d9ComponentERKN9rapidjson12GenericValueINSB_4UTF8IcEENSB_19MemoryPoolAllocatorINSB_12CrtAllocatorEEEEEEEEED2Ev` |
| `0x0103C03D` | `_ZTINSt6__ndk110__function6__baseIFPN7cocos2d4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103C5C2` | `_ZTINSt6__ndk110__function6__baseIFPN7cocos2d9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103BDD2` | `_ZTINSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_4NodeERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EEE` |
| `0x0103C348` | `_ZTINSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_9ComponentERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EEE` |
| `0x0103C20B` | `_ZTINSt6__ndk115binary_functionIPN7cocos2d8CSLoaderERKN9rapidjson12GenericValueINS4_4UTF8IcEENS4_19MemoryPoolAllocatorINS4_12CrtAllocatorEEEEEPNS1_4NodeEEE` |
| `0x0103C79F` | `_ZTINSt6__ndk115binary_functionIPN7cocos2d8CSLoaderERKN9rapidjson12GenericValueINS4_4UTF8IcEENS4_19MemoryPoolAllocatorINS4_12CrtAllocatorEEEEEPNS1_9ComponentEEE` |
| `0x0103C2A7` | `_ZTINSt6__ndk118__weak_result_typeIMN7cocos2d8CSLoaderEFPNS1_4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103C840` | `_ZTINSt6__ndk118__weak_result_typeIMN7cocos2d8CSLoaderEFPNS1_9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103B773` | `_ZTINSt6__ndk16__bindIMN7cocos2d8CSLoaderEFPNS1_4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEJPS2_RKNS_12placeholders4__phILi1EEEEEE` |
| `0x0103BB5D` | `_ZTINSt6__ndk16__bindIMN7cocos2d8CSLoaderEFPNS1_9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEJPS2_RKNS_12placeholders4__phILi1EEEEEE` |
| `0x0103BFAC` | `_ZTSNSt6__ndk110__function6__baseIFPN7cocos2d4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103C52C` | `_ZTSNSt6__ndk110__function6__baseIFPN7cocos2d9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103BEBF` | `_ZTSNSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_4NodeERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EEE` |
| `0x0103C43A` | `_ZTSNSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_9ComponentERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EEE` |
| `0x0103C16F` | `_ZTSNSt6__ndk115binary_functionIPN7cocos2d8CSLoaderERKN9rapidjson12GenericValueINS4_4UTF8IcEENS4_19MemoryPoolAllocatorINS4_12CrtAllocatorEEEEEPNS1_4NodeEEE` |
| `0x0103C6FE` | `_ZTSNSt6__ndk115binary_functionIPN7cocos2d8CSLoaderERKN9rapidjson12GenericValueINS4_4UTF8IcEENS4_19MemoryPoolAllocatorINS4_12CrtAllocatorEEEEEPNS1_9ComponentEEE` |
| `0x0103C0CE` | `_ZTSNSt6__ndk118__weak_result_typeIMN7cocos2d8CSLoaderEFPNS1_4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103C658` | `_ZTSNSt6__ndk118__weak_result_typeIMN7cocos2d8CSLoaderEFPNS1_9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEEE` |
| `0x0103B6BA` | `_ZTSNSt6__ndk16__bindIMN7cocos2d8CSLoaderEFPNS1_4NodeERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEJPS2_RKNS_12placeholders4__phILi1EEEEEE` |
| `0x0103BA9F` | `_ZTSNSt6__ndk16__bindIMN7cocos2d8CSLoaderEFPNS1_9ComponentERKN9rapidjson12GenericValueINS5_4UTF8IcEENS5_19MemoryPoolAllocatorINS5_12CrtAllocatorEEEEEEJPS2_RKNS_12placeholders4__phILi1EEEEEE` |
| `0x010399E5` | `_ZTVNSt6__ndk110__function6__funcINS_6__bindIMN7cocos2d8CSLoaderEFPNS3_4NodeERKN9rapidjson12GenericValueINS7_4UTF8IcEENS7_19MemoryPoolAllocatorINS7_12CrtAllocatorEEEEEEJPS4_RKNS_12placeholders4__phILi1EEEEEENS_9allocatorISP_EEFS6_SG_EEE` |
| ... | *(57 more)* |
