# replace paths like /moonycompany/ with ur pythonanywhere path
# change photon and the company name (user names) and change the admin password so at /admin of ur python site u enter it in and pls change webhook

import os, json, sqlite3, secrets, base64, time, hmac, hashlib, random, string, traceback, uuid
import requests as N
import ipaddress as I
from flask import Flask, request, jsonify, send_file, render_template_string

M = str
L = dict
G = Exception
E = print

app = Flask(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
DB_PATH        = os.environ.get('DB_PATH',         '/home/MoonyCompany/mysite/userdata.db')
SITE_PATH      = os.environ.get('SITE_PATH',       '/home/MoonyCompany/mysite')
JWT_SECRET     = os.environ.get('JWT_SECRET',      secrets.token_hex(32))
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD',  'moony2hp67')

PHOTON_APP_ID       = os.environ.get('PHOTON_APP_ID',       'photon fusion app id but required fusion 2 and set url to ur py site then /auth')
PHOTON_VOICE_APP_ID = os.environ.get('PHOTON_VOICE_APP_ID', 'photon voice app id')
GAME_DATA_URL       = os.environ.get('GAME_DATA_URL',       'go to the prod folder of this repo')
ATTEST_EXPIRES_AT   = int(os.environ.get('ATTEST_EXPIRES_AT', '1820877961'))

OWNER_USER_ID   = os.environ.get('OWNER_USER_ID',   '2e8aace0-282d-4c3d-b9d4-6a3b3ba2c2a6')
OWNER_CUSTOM_ID = os.environ.get('OWNER_CUSTOM_ID', '82897467945336016')
OWNER_USERNAME  = os.environ.get('OWNER_USERNAME',  '<color=purple>OWNER</color>')

HARD_CURRENCY   = int(os.environ.get('HARD_CURRENCY',   '30000000'))
SOFT_CURRENCY   = int(os.environ.get('SOFT_CURRENCY',   '20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
RESEARCH_POINTS = int(os.environ.get('RESEARCH_POINTS', '20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
STASH_COLS      = int(os.environ.get('STASH_COLS', '16'))
STASH_ROWS      = int(os.environ.get('STASH_ROWS', '8'))

PUBLIC_SOFT_CURRENCY   = int(os.environ.get('PUBLIC_SOFT_CURRENCY',   '20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
PUBLIC_RESEARCH_POINTS = int(os.environ.get('PUBLIC_RESEARCH_POINTS', '20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
PUBLIC_STASH_COLS      = int(os.environ.get('PUBLIC_STASH_COLS', '16'))
PUBLIC_STASH_ROWS      = int(os.environ.get('PUBLIC_STASH_ROWS', '8'))

intoxicated_USERNAME  = os.environ.get('intoxicated_USERNAME', '<color=red>owner</color>')
intoxicated_USER_ID   = os.environ.get('intoxicated_USER_ID',  '3626339de1aaf650b2b4f82b7c1bc191')
intoxicated_CUSTOM_ID = os.environ.get('intoxicated_CUSTOM_ID','61789000786606283')
COMPANY_USERNAME      = os.environ.get('COMPANY_USERNAME', 'change user (everyones user)')

DISCORD_WEBHOOK = os.environ.get(
    'DISCORD_WEBHOOK',
    'https://discord.com/api/webhooks/webhook id/webhook token'
)

# ── File paths for econ JSON files (from doc2) ────────────────────────────────
dih2 = os.environ.get('ECON_PATH_2', os.path.join(SITE_PATH, 'data2'))
dih3 = os.environ.get('ECON_PATH_3', os.path.join(SITE_PATH, 'data3'))

# ═══════════════════════════════════════════════════════════════════════════════
#  ALL AVATAR ITEMS (every item from doc2's storage166 inventory)
# ═══════════════════════════════════════════════════════════════════════════════
ALL_AVATAR_ITEMS = [
    "acc_ear_l_earring_banana", "acc_ear_l_earring_roundgold", "acc_ear_l_earring_samuraiwarriorearring",
    "acc_ear_l_earring_samuraiwarriorearring_dual", "acc_ear_l_earring_samuraiwarriorearring_orange",
    "acc_ear_r_earring_roundgold", "acc_ear_r_earring_samuraiwarriorearring",
    "acc_ear_r_earring_samuraiwarriorearring_dual", "acc_ear_r_earring_samuraiwarriorearring_orange",
    "acc_face_cybersuit_helmet", "acc_face_glasses_blue", "acc_face_glasses_coloredvisor",
    "acc_face_glasses_coloredvisor_orange", "acc_face_glasses_coolglasses", "acc_face_glasses_dinoshades",
    "acc_face_glasses_dinoshades_car", "acc_face_glasses_dinoshades_rugged", "acc_face_glasses_dinoshades_salmon",
    "acc_face_glasses_geek", "acc_face_glasses_geek_yellow", "acc_face_glasses_greensunset",
    "acc_face_glasses_greensunset_blue", "acc_face_glasses_greensunset_yellow", "acc_face_glasses_heart",
    "acc_face_glasses_holiday", "acc_face_glasses_lightvisor", "acc_face_glasses_pink",
    "acc_face_glasses_rayban", "acc_face_glasses_rayban_rose", "acc_face_glasses_redshades",
    "acc_face_glasses_round", "acc_face_glasses_shuttershadesdiscord", "acc_face_glasses_shuttershadesdiscord_gold",
    "acc_face_glasses_spiky", "acc_face_glasses_sunglasses", "acc_face_glasses_tacticalrobovisor",
    "acc_face_glasses_tacticalrobovisor_copper", "acc_face_glasses_tacticalvisor",
    "acc_face_glasses_tacticalvisor_emo", "acc_face_glasses_tacticalvisor_pale", "acc_face_glasses_visor",
    "acc_face_glasses_yellow", "acc_face_goggles", "acc_face_goggles_aura", "acc_face_goggles_green",
    "acc_face_goggles_red", "acc_face_sunglasses_damaged", "acc_fit_animesuit", "acc_fit_animesuit_blue",
    "acc_fit_animesuitfemale", "acc_fit_animesuitfemale_black", "acc_fit_apocalypsesurvivor",
    "acc_fit_apocalypsesurvivor_banana", "acc_fit_apocalypsesurvivor_bloodorange",
    "acc_fit_apocalypsesurvivor_blueberry", "acc_fit_aquaarmor", "acc_fit_aquaarmor_green",
    "acc_fit_aquaarmor_red", "acc_fit_arbordaydruid", "acc_fit_arbordayshaman", "acc_fit_arbordaytree",
    "acc_fit_bluehooded_jacket", "acc_fit_broccoli", "acc_fit_brown_basic_tanktop",
    "acc_fit_brown_hooded_zip_up_jacket", "acc_fit_bunnyoutfit", "acc_fit_bunnyoutfit_blackwhite",
    "acc_fit_bunnyoutfit_blue", "acc_fit_bunnyoutfit_yellow", "acc_fit_business_suit",
    "acc_fit_business_suit_heartsuit", "acc_fit_chinesewarriorarmor", "acc_fit_chinesewarriorarmor_gold",
    "acc_fit_cincodemayo", "acc_fit_cincodemayo_crimson", "acc_fit_cincodemayo_forest",
    "acc_fit_cincodemayo_saffron", "acc_fit_cincodemayoblanket", "acc_fit_cincodemayoblanket_crimson",
    "acc_fit_cincodemayoblanket_forest", "acc_fit_cincodemayoblanket_saffron", "acc_fit_clownoutfit",
    "acc_fit_coloredjacket", "acc_fit_coloredjacket_fire", "acc_fit_coloredjacket_red",
    "acc_fit_coolsuit", "acc_fit_coolsuit_bluewhite", "acc_fit_coolsuit_purplewhite",
    "acc_fit_cubes", "acc_fit_cubes_frog", "acc_fit_cubes_gorilla", "acc_fit_cubes_shepherd",
    "acc_fit_cupidoutfit", "acc_fit_cybersuit", "acc_fit_demolitionjumpsuit",
    "acc_fit_demolitionjumpsuit_aura", "acc_fit_demolitionjumpsuit_green", "acc_fit_demolitionjumpsuit_red",
    "acc_fit_demonboyband", "acc_fit_demonboyband_glowblue", "acc_fit_demonboyband_glowgreen",
    "acc_fit_demonboyband_glowpurple", "acc_fit_denimjacket", "acc_fit_denimjacket_hippie",
    "acc_fit_discobutt", "acc_fit_discobutt_phoenix", "acc_fit_diversuit", "acc_fit_diversuit_green",
    "acc_fit_diversuit_rusty", "acc_fit_diversuit_yellow", "acc_fit_dwarf", "acc_fit_dwarf_blue",
    "acc_fit_dwarf_tin", "acc_fit_dwarf_wood", "acc_fit_early_bird_tshirt", "acc_fit_eastervest",
    "acc_fit_eastervest_blue", "acc_fit_eastervest_yellow", "acc_fit_eggsuit", "acc_fit_eggsuit_b",
    "acc_fit_eggsuit_chocolate", "acc_fit_eggsuit_golden", "acc_fit_elfoutfit", "acc_fit_elfoutfit_blue",
    "acc_fit_elfoutfit_pink", "acc_fit_face_glasses_eyepatch", "acc_fit_face_glasses_eyepatch_desert",
    "acc_fit_face_glasses_eyepatch_green", "acc_fit_face_glasses_eyepatch_snow", "acc_fit_fallleafponcho",
    "acc_fit_ghostbuster_jacket", "acc_fit_ghostcloth", "acc_fit_gladiatorarmor",
    "acc_fit_gladiatorarmor_cat", "acc_fit_gladiatorarmor_frog", "acc_fit_gladiatorarmor_gorilla",
    "acc_fit_gladiatorarmor_pug", "acc_fit_gladiatorarmor_skeleton", "acc_fit_glowgrilla",
    "acc_fit_glowgrilla_purple", "acc_fit_glowjacket_pink", "acc_fit_glowjacket_red",
    "acc_fit_grapplesoldier_uniform", "acc_fit_grapplesoldier_uniform_black",
    "acc_fit_grapplesoldier_uniform_blue", "acc_fit_grapplesoldier_uniform_red",
    "acc_fit_grimreaper", "acc_fit_grimreaper_gold", "acc_fit_grimreaper_red", "acc_fit_grimreaper_white",
    "acc_fit_grimreaperpremium", "acc_fit_halloween_jacket", "acc_fit_halloween_shirt",
    "acc_fit_halloweenskeletonshirt", "acc_fit_halloweenskeletonshirt_blue",
    "acc_fit_halloweenskeletonshirt_red", "acc_fit_halloweenskeletonshirt_yellow",
    "acc_fit_hawaiiangirl", "acc_fit_hawaiiangirl_blonde", "acc_fit_hawaiiangirl_brown",
    "acc_fit_hawaiianshirt", "acc_fit_hawaiianshirt_blue", "acc_fit_hawaiianshirt_yellow",
    "acc_fit_hawaiianshirtgold", "acc_fit_hazmatsuit", "acc_fit_hazmatsuit_blue",
    "acc_fit_hazmatsuit_green", "acc_fit_hazmatsuit_orange", "acc_fit_hazmatsuit_pink",
    "acc_fit_hazmatsuit_purple", "acc_fit_hazmatsuit_red", "acc_fit_head_animehair_longa",
    "acc_fit_head_animehair_longb", "acc_fit_head_animehair_shorta", "acc_fit_head_animehair_shortb",
    "acc_fit_head_animehair_shortc", "acc_fit_head_apocalypsesurvivor",
    "acc_fit_head_apocalypsesurvivor_banana", "acc_fit_head_apocalypsesurvivor_bloodorange",
    "acc_fit_head_apocalypsesurvivor_blueberry", "acc_fit_head_aquaarmor",
    "acc_fit_head_aquaarmor_green", "acc_fit_head_aquaarmor_red", "acc_fit_head_bunnyears",
    "acc_fit_head_bunnyears_blue", "acc_fit_head_bunnyears_yellow", "acc_fit_head_cube",
    "acc_fit_head_cube_frog", "acc_fit_head_cube_gorilla", "acc_fit_head_cube_shepherd",
    "acc_fit_head_cupidhair", "acc_fit_head_demonboyband", "acc_fit_head_demonboyband_glowblue",
    "acc_fit_head_demonboyband_glowgreen", "acc_fit_head_demonboyband_glowpurple",
    "acc_fit_head_diversuit", "acc_fit_head_diversuit_green", "acc_fit_head_diversuit_rusty",
    "acc_fit_head_diversuit_yellow", "acc_fit_head_dwarfhelmet", "acc_fit_head_dwarfhelmet_blue",
    "acc_fit_head_dwarfhelmet_tin", "acc_fit_head_dwarfhelmet_wood", "acc_fit_head_elfhat",
    "acc_fit_head_elfhat_blue", "acc_fit_head_elfhat_pink", "acc_fit_head_glowgrilla",
    "acc_fit_head_glowgrilla_purple", "acc_fit_head_hair_spikey", "acc_fit_head_hawaiiangirl",
    "acc_fit_head_hawaiiangirl_blonde", "acc_fit_head_hawaiiangirl_brown", "acc_fit_head_headband",
    "acc_fit_head_headband_desert", "acc_fit_head_headband_red", "acc_fit_head_headband_snow",
    "acc_fit_head_kingofhearts", "acc_fit_head_kingofhearts_blue", "acc_fit_head_kpopvisor",
    "acc_fit_head_kpopvisor_black", "acc_fit_head_kpopvisor_blue", "acc_fit_head_kpopvisor_darkpuple",
    "acc_fit_head_mohawk", "acc_fit_head_piratebandana", "acc_fit_head_queenofheartscrown",
    "acc_fit_head_racerhelmet", "acc_fit_head_racerhelmet_black", "acc_fit_head_racerhelmet_white",
    "acc_fit_head_racerhelmet_yellow", "acc_fit_head_redknight", "acc_fit_head_redknight_summon",
    "acc_fit_head_rockhair", "acc_fit_head_rockhair_redblonde", "acc_fit_head_romanhelmet",
    "acc_fit_head_romanhelmet_cat", "acc_fit_head_romanhelmet_frog", "acc_fit_head_romanhelmet_gorilla",
    "acc_fit_head_romanhelmet_pug", "acc_fit_head_romanhelmet_skeleton", "acc_fit_head_santa",
    "acc_fit_head_santa_blue", "acc_fit_head_santa_purple", "acc_fit_head_spacehelmet",
    "acc_fit_head_spacehelmet_blue", "acc_fit_head_spacehelmet_orange", "acc_fit_head_spacehelmet_rainbow",
    "acc_fit_head_squidgamedollhair", "acc_fit_head_squidgamedollhair_brunette",
    "acc_fit_head_steampunkmask", "acc_fit_head_steampunkmask_boat", "acc_fit_head_steampunkmask_fireengine",
    "acc_fit_head_steampunkmask_tinman", "acc_fit_head_sungear", "acc_fit_head_supermask",
    "acc_fit_head_supermask_atom", "acc_fit_head_supermask_leaf", "acc_fit_head_supermask_recycle",
    "acc_fit_head_tacticalmininghelmet", "acc_fit_head_tacticalmininghelmet_almandine",
    "acc_fit_head_tacticalmininghelmet_diamond", "acc_fit_head_tacticalmininghelmet_emerald",
    "acc_fit_head_tie", "acc_fit_head_tie_blue", "acc_fit_head_warrior_ascendant",
    "acc_fit_head_warrior_ascendant_dark", "acc_fit_head_warrior_engineer", "acc_fit_head_warrior_scholar",
    "acc_fit_holidaysuit", "acc_fit_itemployee", "acc_fit_itemployee_blue", "acc_fit_jacketleatherfuture",
    "acc_fit_kilt", "acc_fit_kilt_blue", "acc_fit_kilt_red", "acc_fit_kilt_yellow",
    "acc_fit_kingofhearts", "acc_fit_kingofhearts_red", "acc_fit_knightarmorscarf",
    "acc_fit_kpop", "acc_fit_kpop_black", "acc_fit_kpop_purple", "acc_fit_kpop_white",
    "acc_fit_kungfucoat", "acc_fit_kungfucoat_black", "acc_fit_kungfucoat_blue",
    "acc_fit_leatherjacket", "acc_fit_lifejacket", "acc_fit_lifejacket_blue",
    "acc_fit_lifejacket_green", "acc_fit_lifejacket_orange", "acc_fit_mask_samuraiwarriormouthlock",
    "acc_fit_necromancer", "acc_fit_nfljersey", "acc_fit_nfljersey_bear", "acc_fit_nfljersey_cat",
    "acc_fit_nfljersey_frog", "acc_fit_nfljersey_pug", "acc_fit_nfljersey_skeleton",
    "acc_fit_ogretop", "acc_fit_orcmage", "acc_fit_orcmage_summon", "acc_fit_parkranger",
    "acc_fit_parkranger_car", "acc_fit_parkranger_rugged", "acc_fit_parkranger_salmon",
    "acc_fit_pilgrim", "acc_fit_piratecoat", "acc_fit_piratecoat_red", "acc_fit_piratevest",
    "acc_fit_policeman", "acc_fit_policeman_brown", "acc_fit_potofgold", "acc_fit_potofgold_flames",
    "acc_fit_potofgold_gold", "acc_fit_potofgold_green", "acc_fit_princessdress",
    "acc_fit_princessdress_green", "acc_fit_queenofheartsdress", "acc_fit_racerjacket",
    "acc_fit_racerjacket_black", "acc_fit_racerjacket_white", "acc_fit_racerjacket_yellow",
    "acc_fit_redknight", "acc_fit_redknight_summon", "acc_fit_rustic_brown_winter_coat",
    "acc_fit_samurai", "acc_fit_samurai_purple", "acc_fit_samurai_red", "acc_fit_samurai_white",
    "acc_fit_samuraiwarrior", "acc_fit_samuraiwarrior_dual", "acc_fit_samuraiwarrior_orange",
    "acc_fit_samuraiwarrior_pink", "acc_fit_santa", "acc_fit_santa_blue", "acc_fit_santa_purple",
    "acc_fit_securityguard", "acc_fit_securityguard_green", "acc_fit_shoegloves",
    "acc_fit_sneakingsuit", "acc_fit_sneakingsuit_desert", "acc_fit_sneakingsuit_green",
    "acc_fit_sneakingsuit_snow", "acc_fit_spacesuit", "acc_fit_spacesuit_blue",
    "acc_fit_spacesuit_orange", "acc_fit_spacesuit_rainbow", "acc_fit_squidgamedoll",
    "acc_fit_squidgamedoll_brunette", "acc_fit_squidgamefrontman", "acc_fit_squidgamefrontman_white",
    "acc_fit_squidgamejacket", "acc_fit_squidgamejacket_purple", "acc_fit_squidgamejacket_red",
    "acc_fit_squidgamejacketparticipant", "acc_fit_steampunkrobot", "acc_fit_steampunkrobot_boat",
    "acc_fit_steampunkrobot_fireengine", "acc_fit_steampunkrobot_tinman", "acc_fit_supermansuit",
    "acc_fit_supermansuit_atom", "acc_fit_supermansuit_leaf", "acc_fit_supermansuit_recycle",
    "acc_fit_sweater_turkey", "acc_fit_tacticalarmor", "acc_fit_tacticalarmor_emo",
    "acc_fit_tacticalarmor_pale", "acc_fit_tacticalmining", "acc_fit_tacticalmining_almandine",
    "acc_fit_tacticalmining_diamond", "acc_fit_tacticalmining_emerald", "acc_fit_tacticalroboarmor",
    "acc_fit_tacticalroboarmor_copper", "acc_fit_tight_fit_blue_tshirt",
    "acc_fit_tight_fit_blue_tshirt_heartshirt", "acc_fit_turkeyhunter", "acc_fit_tuxleprechaun",
    "acc_fit_varsityjacket", "acc_fit_varsityjacket_black", "acc_fit_varsityjacket_gold",
    "acc_fit_varsityjacket_gold2", "acc_fit_varsityjacket_toasty", "acc_fit_viking",
    "acc_fit_viking_firestorm", "acc_fit_viking_flaxen", "acc_fit_viking_twilight",
    "acc_fit_warrior_ascendant", "acc_fit_warrior_ascendant_dark", "acc_fit_warrior_engineer",
    "acc_fit_warrior_scholar", "acc_fit_winterscarf", "acc_fit_worndownemployee",
    "acc_fit_worndownemployee_green", "acc_head_alienears", "acc_head_arbordaycrown",
    "acc_head_arbordaydruidhoodie", "acc_head_artisthat", "acc_head_banana_hat", "acc_head_beach_hat",
    "acc_head_beanie", "acc_head_beerhat", "acc_head_beret", "acc_head_beret_blue",
    "acc_head_beret_red", "acc_head_beret_yellow", "acc_head_black_1984_headphones", "acc_head_cap",
    "acc_head_catearscap", "acc_head_cathelmet", "acc_head_cathelmet_phoenix",
    "acc_head_chinesewarriorhelmet", "acc_head_chinesewarriorhelmet_gold", "acc_head_clownhat",
    "acc_head_coloredcap", "acc_head_coloredcap_fire", "acc_head_coloredcap_red", "acc_head_cone",
    "acc_head_cop", "acc_head_cowboy_hat", "acc_head_creatorcap", "acc_head_crochethat",
    "acc_head_crown", "acc_head_egghat", "acc_head_egghat_b", "acc_head_egghat_chocolate",
    "acc_head_egghat_golden", "acc_head_fedora_hat", "acc_head_frogeyes", "acc_head_goldenhalo",
    "acc_head_gopro", "acc_head_gopro_easter", "acc_head_goprojune", "acc_head_grapplesoldier_beret",
    "acc_head_grapplesoldier_beret_black", "acc_head_grapplesoldier_beret_blue",
    "acc_head_grapplesoldier_beret_red", "acc_head_grimreapercrown", "acc_head_hardhat",
    "acc_head_hardhat_canopy", "acc_head_hazmathelmet", "acc_head_hazmathelmet_blue",
    "acc_head_hazmathelmet_green", "acc_head_hazmathelmet_orange", "acc_head_hazmathelmet_pink",
    "acc_head_hazmathelmet_purple", "acc_head_hazmathelmet_red", "acc_head_horns",
    "acc_head_jesterhat", "acc_head_knifehat", "acc_head_kungfuhat", "acc_head_mage_hat",
    "acc_head_mexicanhat_redblack", "acc_head_mimic_hat", "acc_head_minerhat",
    "acc_head_minerhat_aura", "acc_head_minerhat_green", "acc_head_minerhat_red", "acc_head_mop",
    "acc_head_nflhelmet", "acc_head_nflhelmet_bear", "acc_head_nflhelmet_cat",
    "acc_head_nflhelmet_dog", "acc_head_nflhelmet_frog", "acc_head_nflhelmet_skeleton",
    "acc_head_parkranger", "acc_head_parkranger_car", "acc_head_parkranger_rugged",
    "acc_head_parkranger_salmon", "acc_head_partyhat", "acc_head_patriothat", "acc_head_pilgrimhat",
    "acc_head_pimp_hat", "acc_head_piratehat", "acc_head_piratehat_red", "acc_head_plunger",
    "acc_head_policehat", "acc_head_policehat_brown", "acc_head_propeller_cap", "acc_head_rainbow",
    "acc_head_rainbow_gold", "acc_head_rainbow_green", "acc_head_rainbow_ofdarkness",
    "acc_head_ricepattyhat", "acc_head_ricepattyhat_blue", "acc_head_securityguard",
    "acc_head_securityguard_green", "acc_head_sombrero", "acc_head_sombrero_crimson",
    "acc_head_sombrero_forest", "acc_head_sombrero_saffron", "acc_head_summerhat",
    "acc_head_summerhat_blue", "acc_head_summerhat_golden", "acc_head_summerhat_yellow",
    "acc_head_sweatband", "acc_head_tallcowboy_hat", "acc_head_tiara", "acc_head_tiara_gold",
    "acc_head_toilet_hat", "acc_head_top_hat", "acc_head_tophatclover", "acc_head_turkeyhat",
    "acc_head_turkeyhunter", "acc_head_vikinghelmet", "acc_head_vikinghelmet_firestorm",
    "acc_head_vikinghelmet_flaxen", "acc_head_vikinghelmet_twilight", "acc_head_winterglasses",
    "acc_head_winterhat", "acc_mask_arbordayshaman", "acc_mask_diademuertos", "acc_mask_hazmat",
    "acc_mask_hazmat_blue", "acc_mask_hazmat_green", "acc_mask_hazmat_orange", "acc_mask_hazmat_pink",
    "acc_mask_hazmat_purple", "acc_mask_hazmat_red", "acc_mask_jason", "acc_mask_medicalmask",
    "acc_mask_samuraimaskdemon", "acc_mask_samuraimaskdemon_purple", "acc_mask_samuraimaskdemon_red",
    "acc_mask_samuraimaskdemon_white", "acc_mask_squidgame", "acc_mask_squidgame_nut",
    "acc_mask_squidgame_star", "acc_mask_squidgamefrontman", "acc_mask_squidgamefrontman_gold",
    "acc_mouthcorner_lolipop", "acc_mouthcorner_lolipop_green", "acc_mouthcorner_rose",
    "acc_mouthcorner_tusks", "acc_mouthcorner_tusks_summon", "acc_nosetip_bunny",
    "acc_nosetip_bunny_blackwhite", "acc_nosetip_bunny_blue", "acc_nosetip_bunny_yellow",
    "acc_nosetip_clownnose", "acc_nosetip_steampunkmask", "acc_nosetip_steampunkmask_boat",
    "acc_nosetip_steampunkmask_fireengine", "acc_nosetip_steampunkmask_tinman",
    "animal_cat", "animal_chameleon", "animal_crab", "animal_cyborg_duck", "animal_duck",
    "animal_frog", "animal_germanshep", "animal_goat", "animal_gorilla", "animal_kitten",
    "animal_mole", "animal_polarbear", "animal_pug", "animal_rabbit", "animal_raccoon",
    "animal_reindeer", "animal_shark", "animal_shark_goblin", "animal_shark_hammer",
    "animal_skeletongorilla", "animal_tiger", "animal_trex", "animal_trex_shorthands",
    "animal_trex_winged", "animal_turkey", "animal_turtle",
    "bp_arm_l_cat", "bp_arm_l_chameleon", "bp_arm_l_crab", "bp_arm_l_demonarms", "bp_arm_l_duck",
    "bp_arm_l_duck_metal", "bp_arm_l_frog", "bp_arm_l_germanshep", "bp_arm_l_goat",
    "bp_arm_l_goldarms", "bp_arm_l_gorilla", "bp_arm_l_gorilla_og", "bp_arm_l_hookarms",
    "bp_arm_l_iceyarms", "bp_arm_l_kitten", "bp_arm_l_mole", "bp_arm_l_polarbear", "bp_arm_l_pug",
    "bp_arm_l_rabbit", "bp_arm_l_raccoon", "bp_arm_l_reindeer", "bp_arm_l_shark",
    "bp_arm_l_skeletongorilla", "bp_arm_l_slinkyarms", "bp_arm_l_tiger", "bp_arm_l_trex",
    "bp_arm_l_trex_short", "bp_arm_l_trex_wing", "bp_arm_l_turkey", "bp_arm_l_turtle",
    "bp_arm_r_cat", "bp_arm_r_chameleon", "bp_arm_r_crab", "bp_arm_r_demonarms", "bp_arm_r_duck",
    "bp_arm_r_duck_metal", "bp_arm_r_frog", "bp_arm_r_germanshep", "bp_arm_r_goat",
    "bp_arm_r_goldarms", "bp_arm_r_gorilla", "bp_arm_r_gorilla_og", "bp_arm_r_hookarms",
    "bp_arm_r_iceyarms", "bp_arm_r_kitten", "bp_arm_r_mole", "bp_arm_r_polarbear", "bp_arm_r_pug",
    "bp_arm_r_rabbit", "bp_arm_r_raccoon", "bp_arm_r_reindeer", "bp_arm_r_shark",
    "bp_arm_r_skeletongorilla", "bp_arm_r_slinkyarms", "bp_arm_r_tiger", "bp_arm_r_trex",
    "bp_arm_r_trex_short", "bp_arm_r_trex_wing", "bp_arm_r_turkey", "bp_arm_r_turtle",
    "bp_butt_bigbutt", "bp_butt_bigbutt_animals", "bp_butt_bigbutt_ducky", "bp_butt_bigbutt_galaxy",
    "bp_butt_bigbutt_golden", "bp_butt_bigbutt_hearts", "bp_butt_bigbutt_leaves", "bp_butt_cat",
    "bp_butt_chameleon", "bp_butt_crab", "bp_butt_duck", "bp_butt_frog", "bp_butt_germanshep",
    "bp_butt_goat", "bp_butt_gorilla", "bp_butt_kitten", "bp_butt_mole", "bp_butt_polarbear",
    "bp_butt_pug", "bp_butt_rabbit", "bp_butt_raccoon", "bp_butt_reindeer", "bp_butt_shark",
    "bp_butt_skeletongorilla", "bp_butt_tiger", "bp_butt_trex", "bp_butt_turkey", "bp_butt_turtle",
    "bp_eye_alieneyes", "bp_eye_buttoneyes", "bp_eye_cat", "bp_eye_chameleon", "bp_eye_crab",
    "bp_eye_demoneyes", "bp_eye_duck", "bp_eye_duck_cyborg", "bp_eye_frog", "bp_eye_frogeyes",
    "bp_eye_germanshep", "bp_eye_gloweyes", "bp_eye_goat", "bp_eye_goldeyes", "bp_eye_gorilla",
    "bp_eye_hearteyes", "bp_eye_kitten", "bp_eye_lenseyes", "bp_eye_lizardeyes", "bp_eye_mole",
    "bp_eye_ninjaeyes", "bp_eye_polarbear", "bp_eye_pug", "bp_eye_rabbit", "bp_eye_raccoon",
    "bp_eye_reindeer", "bp_eye_roboeyes", "bp_eye_shark", "bp_eye_skeletongorilla", "bp_eye_tiger",
    "bp_eye_trex", "bp_eye_turkey", "bp_eye_turtle",
    "bp_head_cat", "bp_head_chameleon", "bp_head_chameleon_crest", "bp_head_chameleon_horns",
    "bp_head_crab", "bp_head_duck", "bp_head_duck_cyborg", "bp_head_frog", "bp_head_germanshep",
    "bp_head_goat", "bp_head_goat_ramhorns", "bp_head_goat_shorthorns", "bp_head_gorilla",
    "bp_head_kitten", "bp_head_mole", "bp_head_polarbear", "bp_head_pug", "bp_head_rabbit",
    "bp_head_rabbit_foldedear", "bp_head_rabbit_lopear", "bp_head_raccoon", "bp_head_reindeer",
    "bp_head_shark", "bp_head_shark_goblin", "bp_head_shark_hammer", "bp_head_skeletongorilla",
    "bp_head_tiger", "bp_head_trex", "bp_head_turkey", "bp_head_turtle",
    "bp_tail_ankytail", "bp_tail_bananapeeltail", "bp_tail_cat", "bp_tail_chameleon",
    "bp_tail_donkeypintail", "bp_tail_duck", "bp_tail_electricalcordtail", "bp_tail_germanshep",
    "bp_tail_goat", "bp_tail_kitten", "bp_tail_mole", "bp_tail_polarbear", "bp_tail_pug",
    "bp_tail_rabbit", "bp_tail_raccoon", "bp_tail_reindeer", "bp_tail_shark", "bp_tail_tiger",
    "bp_tail_trex", "bp_tail_turkey",
    "bp_torso_cat", "bp_torso_chameleon", "bp_torso_crab", "bp_torso_duck", "bp_torso_frog",
    "bp_torso_germanshep", "bp_torso_goat", "bp_torso_gorilla", "bp_torso_kitten", "bp_torso_mole",
    "bp_torso_polarbear", "bp_torso_pug", "bp_torso_rabbit", "bp_torso_raccoon", "bp_torso_reindeer",
    "bp_torso_shark", "bp_torso_skeletongorilla", "bp_torso_tiger", "bp_torso_trex",
    "bp_torso_turkey", "bp_torso_turtle", "bp_torso_turtle_shell2", "bp_torso_turtle_shell3",
    "bp_torso_turtle_shell4",
    "character_battle_shark", "character_chame_leo", "character_delta_hare", "character_goat",
    "character_goat_ram", "character_goat_smallhorns", "character_grim_gorilla",
    "character_metal_duck", "character_mole_a_tov", "character_polar_paws", "character_shelllong",
    "character_sigma_frog", "character_swag_stag", "character_trex_pirate",
    "character_trex_pirate_crew", "character_turkey_hunter",
    "outfit_anime_fem_black", "outfit_anime_fem_pink", "outfit_anime_mas_blue", "outfit_anime_mas_white",
    "outfit_apocalypsesurvivor", "outfit_apocalypsesurvivor_banana",
    "outfit_apocalypsesurvivor_bloodorange", "outfit_apocalypsesurvivor_blueberry",
    "outfit_aquaarmor", "outfit_aquaarmor_green", "outfit_aquaarmor_red",
    "outfit_arborday_druid", "outfit_arborday_shaman", "outfit_arborday_tree",
    "outfit_armor_king", "outfit_bunny", "outfit_bunny_blackwhite", "outfit_bunny_blue",
    "outfit_bunny_yellow", "outfit_bunnydrip_blue", "outfit_bunnydrip_pink", "outfit_bunnydrip_yellow",
    "outfit_chinese_warrior", "outfit_chinese_warrior_gold", "outfit_cincodemayo",
    "outfit_cincodemayo_crimson", "outfit_cincodemayo_forest", "outfit_cincodemayo_saffron",
    "outfit_cincodemayoblanket", "outfit_cincodemayoblanket_crimson", "outfit_cincodemayoblanket_forest",
    "outfit_cincodemayoblanket_saffron", "outfit_clown", "outfit_cube", "outfit_cube_frog",
    "outfit_cube_gorilla", "outfit_cube_shepherd", "outfit_cupid", "outfit_cybersuit",
    "outfit_cyborg_punk", "outfit_deltahare_blue", "outfit_deltahare_desert", "outfit_deltahare_green",
    "outfit_deltahare_snow", "outfit_demolitionjumpsuit", "outfit_demolitionjumpsuit_green",
    "outfit_demolitionjumpsuit_red", "outfit_demonboyband", "outfit_demonboyband_glowblue",
    "outfit_demonboyband_glowgreen", "outfit_demonboyband_glowpurple", "outfit_discobutt",
    "outfit_discobutt_phoenix", "outfit_diversuit", "outfit_diversuit_green", "outfit_diversuit_rusty",
    "outfit_diversuit_yellow", "outfit_dwarf", "outfit_dwarf_blue", "outfit_dwarf_tin",
    "outfit_dwarf_wood", "outfit_eggsuit_chocolate", "outfit_eggsuit_colorful_green",
    "outfit_eggsuit_colorful_purple", "outfit_eggsuit_golden", "outfit_elf_blue", "outfit_elf_green",
    "outfit_elf_pink", "outfit_employee_suit_blue", "outfit_employee_suit_gold",
    "outfit_employee_suit_purple", "outfit_fallponcho", "outfit_fur_future", "outfit_gladiator",
    "outfit_gladiator_cat", "outfit_gladiator_frog", "outfit_gladiator_gorilla",
    "outfit_gladiator_pug", "outfit_gladiator_skeletongorilla", "outfit_glowgrilla",
    "outfit_glowgrilla_purple", "outfit_grapplesoldier", "outfit_grapplesoldier_black",
    "outfit_grapplesoldier_blue", "outfit_grapplesoldier_red", "outfit_grimreaper_premium",
    "outfit_hawaiian", "outfit_hawaiian_blue", "outfit_hawaiian_yellow", "outfit_hawaiiangirl",
    "outfit_hawaiiangirl_blonde", "outfit_hawaiiangirl_brown", "outfit_hazmat_blue",
    "outfit_hazmat_green", "outfit_hazmat_orange", "outfit_hazmat_pink", "outfit_hazmat_purple",
    "outfit_hazmat_red", "outfit_hazmat_yellow", "outfit_hippie", "outfit_irish_kilt",
    "outfit_irish_kilt_blue", "outfit_irish_kilt_red", "outfit_irish_kilt_yellow",
    "outfit_it_employee_blue", "outfit_it_employee_brown", "outfit_kingofhearts_blue",
    "outfit_kingofhearts_red", "outfit_kpop", "outfit_kpop_black", "outfit_kpop_purple",
    "outfit_kpop_white", "outfit_kungfu_black", "outfit_kungfu_blue", "outfit_kungfu_orange",
    "outfit_leprachaun", "outfit_liona", "outfit_necromancer", "outfit_neon_miner",
    "outfit_nfljersey_bear", "outfit_nfljersey_cat", "outfit_nfljersey_frog",
    "outfit_nfljersey_gorilla", "outfit_nfljersey_pug", "outfit_nfljersey_skeleton",
    "outfit_og_fit1", "outfit_og_fit2", "outfit_orcmage", "outfit_orcmage_summon",
    "outfit_parkranger", "outfit_parkranger_car", "outfit_parkranger_rugged", "outfit_parkranger_salmon",
    "outfit_pilgrim", "outfit_pirate_blue", "outfit_pirate_crew", "outfit_pirate_red",
    "outfit_policeman_blue", "outfit_policeman_brown", "outfit_potofgold", "outfit_potofgold_flames",
    "outfit_potofgold_gold", "outfit_potofgold_green", "outfit_punkrock", "outfit_queenofhearts",
    "outfit_racerjacket_black", "outfit_racerjacket_red", "outfit_racerjacket_white",
    "outfit_racerjacket_yellow", "outfit_redknight", "outfit_redknight_summon", "outfit_rocker",
    "outfit_samurai", "outfit_samurai_purple", "outfit_samurai_red", "outfit_samurai_white",
    "outfit_samuraiwarrior", "outfit_samuraiwarrior_dual", "outfit_samuraiwarrior_orange",
    "outfit_samuraiwarrior_pink", "outfit_santa", "outfit_santa_blue", "outfit_santa_purple",
    "outfit_securityguard_green", "outfit_securityguard_white", "outfit_shiny_swim_set",
    "outfit_spacesuit", "outfit_spacesuit_blue", "outfit_spacesuit_orange", "outfit_spacesuit_rainbow",
    "outfit_squidgame_pink", "outfit_squidgame_purple", "outfit_squidgame_red",
    "outfit_squidgamedoll", "outfit_squidgamedoll_brunette", "outfit_squidgamefrontman",
    "outfit_squidgamefrontman_white", "outfit_steampunkrobot", "outfit_steampunkrobot_boat",
    "outfit_steampunkrobot_fireengine", "outfit_steampunkrobot_tinman", "outfit_supermansuit",
    "outfit_supermansuit_atom", "outfit_supermansuit_leaf", "outfit_supermansuit_recycle",
    "outfit_tacticalarmor", "outfit_tacticalarmor_emo", "outfit_tacticalarmor_pale",
    "outfit_tacticalarmor_robo", "outfit_tacticalarmor_robo_copper", "outfit_tacticalmining",
    "outfit_tacticalmining_almandine", "outfit_tacticalmining_diamond", "outfit_tacticalmining_emerald",
    "outfit_teamblue", "outfit_teamblue_fire", "outfit_teamred", "outfit_thanksgiving_turkey",
    "outfit_trek", "outfit_valentines_suit", "outfit_valentines_youme", "outfit_viking",
    "outfit_viking_firestorm", "outfit_viking_flaxen", "outfit_viking_twilight",
    "outfit_warrior_ascendant", "outfit_warrior_ascendant_dark", "outfit_warrior_engineer",
    "outfit_warrior_scholar", "outfit_worndownemployee_blue", "outfit_worndownemployee_green",
]

# ═══════════════════════════════════════════════════════════════════════════════
#  DATABASE
# ═══════════════════════════════════════════════════════════════════════════════
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        ip TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        custom_id TEXT NOT NULL,
        create_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS banned_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        custom_id TEXT,
        device_id TEXT,
        token TEXT,
        reason TEXT DEFAULT '',
        banned_at REAL NOT NULL
    )''')
    for col in ('device_id', 'token'):
        try:
            cur.execute(f'ALTER TABLE banned_entries ADD COLUMN {col} TEXT')
        except Exception:
            pass
    cur.execute('''CREATE TABLE IF NOT EXISTS user_cosmetics (
        custom_id TEXT PRIMARY KEY,
        avatar_json TEXT NOT NULL DEFAULT '{}',
        inventory_json TEXT NOT NULL DEFAULT '{"items":[]}',
        updated_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_stash (
        custom_id TEXT PRIMARY KEY,
        stash_json TEXT NOT NULL DEFAULT '{"items":[],"version":1}',
        updated_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS server_config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_wallet (
        custom_id TEXT PRIMARY KEY,
        hard_currency INTEGER NOT NULL DEFAULT 0,
        soft_currency TEXT NOT NULL DEFAULT '0',
        research_points TEXT NOT NULL DEFAULT '0',
        stash_cols INTEGER NOT NULL DEFAULT 16,
        stash_rows INTEGER NOT NULL DEFAULT 8,
        updated_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_overrides (
        custom_id TEXT PRIMARY KEY,
        username TEXT,
        metadata_json TEXT DEFAULT '{}',
        notes TEXT DEFAULT '',
        role TEXT DEFAULT 'player',
        updated_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS named_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT NOT NULL,
        custom_id TEXT NOT NULL,
        token TEXT NOT NULL,
        refresh_token TEXT NOT NULL,
        created_at REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_research (
        custom_id TEXT PRIMARY KEY,
        nodes_json TEXT NOT NULL DEFAULT '{"nodes":[]}',
        updated_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_prefs (
        custom_id TEXT PRIMARY KEY,
        prefs_json TEXT NOT NULL DEFAULT '{}',
        updated_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_loadout (
        custom_id TEXT PRIMARY KEY,
        loadout_json TEXT NOT NULL DEFAULT '{}',
        updated_time REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_action TEXT NOT NULL,
        target TEXT,
        detail TEXT,
        performed_at REAL NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_tokens (
        custom_id TEXT PRIMARY KEY,
        token TEXT NOT NULL,
        refresh_token TEXT NOT NULL,
        device_id TEXT DEFAULT '',
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL
    )''')
    try:
        cur.execute('ALTER TABLE user_tokens ADD COLUMN device_id TEXT DEFAULT ""')
    except Exception:
        pass
    cur.execute('''CREATE TABLE IF NOT EXISTS spawn_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id TEXT NOT NULL,
        pos_x REAL NOT NULL,
        pos_y REAL NOT NULL,
        pos_z REAL NOT NULL,
        scale REAL DEFAULT 1.0,
        color_hue INTEGER DEFAULT 0,
        color_sat INTEGER DEFAULT 0,
        custom_id TEXT,
        spawned INTEGER DEFAULT 0,
        created_at REAL NOT NULL,
        expires_at REAL
    )''')
    conn.commit()
    conn.close()

init_db()

# ═══════════════════════════════════════════════════════════════════════════════
#  BAN HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def is_banned(ip=None, custom_id=None, device_id=None, token=None):
    conn = get_conn()
    try:
        conditions, params = [], []
        if ip:        conditions.append('ip = ?');        params.append(ip)
        if custom_id: conditions.append('custom_id = ?'); params.append(custom_id)
        if device_id: conditions.append('device_id = ?'); params.append(device_id)
        if token:     conditions.append('token = ?');     params.append(token)
        if not conditions:
            return False, None
        where = ' OR '.join(f'({c})' for c in conditions)
        row = conn.execute(
            f'SELECT reason FROM banned_entries WHERE {where} LIMIT 1', params
        ).fetchone()
        if row:
            return True, row['reason'] or 'Banned by admin'
        return False, None
    finally:
        conn.close()

def add_ban(ip=None, custom_id=None, device_id=None, token=None, reason=''):
    conn = get_conn()
    conn.execute(
        'INSERT INTO banned_entries (ip, custom_id, device_id, token, reason, banned_at) VALUES (?,?,?,?,?,?)',
        (ip, custom_id, device_id, token, reason, time.time())
    )
    conn.commit()
    conn.close()

def remove_ban(ip=None, custom_id=None, device_id=None, token=None):
    conn = get_conn()
    clauses, params = [], []
    if ip:        clauses.append('ip=?');        params.append(ip)
    if custom_id: clauses.append('custom_id=?'); params.append(custom_id)
    if device_id: clauses.append('device_id=?'); params.append(device_id)
    if token:     clauses.append('token=?');     params.append(token)
    if clauses:
        conn.execute(f'DELETE FROM banned_entries WHERE {" OR ".join(clauses)}', params)
    conn.commit()
    conn.close()

def get_all_bans():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM banned_entries ORDER BY banned_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ═══════════════════════════════════════════════════════════════════════════════
#  BLOCK BANNED IPS / TOKENS / DEVICES - FIXED VERSION
# ═══════════════════════════════════════════════════════════════════════════════
@app.before_request
def block_banned():
    # Skip ban check for admin routes
    if request.path.startswith('/admin'):
        return None

    # Skip ban check for static files
    if request.path.startswith('/static'):
        return None

    ip = get_ip()
    custom_id = None
    device_id = None
    token_val = None

    # Try to get custom_id from database
    try:
        conn = get_conn()
        row = conn.execute('SELECT custom_id FROM users WHERE ip=?', (ip,)).fetchone()
        if row:
            custom_id = row['custom_id']
            # Get token and device_id if available
            tok_row = conn.execute('SELECT token, device_id FROM user_tokens WHERE custom_id=?', (custom_id,)).fetchone()
            if tok_row:
                token_val = tok_row['token']
                device_id = tok_row['device_id']
        conn.close()
    except Exception:
        pass

    # Also check Authorization header for token
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token_val = auth_header[7:].strip()

    # Also check token query parameter
    if not token_val:
        token_val = request.args.get('token', '')

    # Check if banned by any criteria
    banned, reason = is_banned(
        ip=ip,
        custom_id=custom_id,
        device_id=device_id or None,
        token=token_val or None
    )

    if banned:
        # Return a proper JSON response with 403 status
        return jsonify({
            'error': 'banned',
            'reason': reason or 'You have been banned from this server.',
            'message': reason or 'You have been banned from this server.',
        }), 403

    # Not banned, allow request to continue
    return None

# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def get_ip():
    xff = request.headers.get('X-Forwarded-For')
    if xff:
        return xff.split(',')[0].strip()
    return request.remote_addr

def is_trusted(ip_address):
    try:
        trusted_ips = set(filter(None, [x.strip() for x in os.environ.get('TRUSTED_PUBLIC_IPS', 'Make this your ip').split(',')]))
        if ip_address in trusted_ips:
            return True
        ip = I.ip_address(ip_address)
        for net in trusted_nets:
            try:
                if ip in I.ip_network(net, strict=False):
                    return True
            except ValueError:
                continue
        return False
    except ValueError:
        return False

def get_or_create_user(ip):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT custom_id, username FROM users WHERE ip=?', (ip,))
    result = cur.fetchone()
    if result:
        conn.close()
        return {'custom_id': result['custom_id'], 'username': result['username']}, False
    username  = 'user_' + ''.join(random.choices(string.ascii_letters, k=6))
    custom_id = ''.join(random.choices(string.digits, k=17))
    cur.execute('INSERT INTO users (ip, username, custom_id, create_time) VALUES (?,?,?,?)',
                (ip, username, custom_id, time.time()))
    conn.commit()
    conn.close()
    return {'custom_id': custom_id, 'username': username}, True

def get_or_create_user_token(custom_id, device_id=''):
    conn = get_conn()
    row = conn.execute('SELECT token, refresh_token FROM user_tokens WHERE custom_id=?', (custom_id,)).fetchone()
    if row:
        conn.close()
        return {'token': row['token'], 'refresh_token': row['refresh_token']}
    pair = make_token_pair(custom_id)
    conn.execute(
        '''INSERT INTO user_tokens (custom_id, token, refresh_token, device_id, created_at, updated_at)
           VALUES (?,?,?,?,?,?)''',
        (custom_id, pair['token'], pair['refresh_token'], device_id or '', time.time(), time.time())
    )
    conn.commit()
    conn.close()
    return pair

def refresh_user_token(custom_id, device_id=''):
    pair = make_token_pair(custom_id)
    conn = get_conn()
    conn.execute(
        '''INSERT INTO user_tokens (custom_id, token, refresh_token, device_id, created_at, updated_at)
           VALUES (?,?,?,?,?,?)
           ON CONFLICT(custom_id) DO UPDATE SET
           token=excluded.token, refresh_token=excluded.refresh_token,
           device_id=excluded.device_id, updated_at=excluded.updated_at''',
        (custom_id, pair['token'], pair['refresh_token'], device_id or '', time.time(), time.time())
    )
    conn.commit()
    conn.close()
    return pair

def update_device_id(custom_id, device_id):
    if not device_id:
        return
    conn = get_conn()
    conn.execute('UPDATE user_tokens SET device_id=?, updated_at=? WHERE custom_id=?',
                 (device_id, time.time(), custom_id))
    conn.commit()
    conn.close()

def get_user_wallet(custom_id):
    conn = get_conn()
    row = conn.execute('SELECT * FROM user_wallet WHERE custom_id=?', (custom_id,)).fetchone()
    conn.close()
    if row:
        return {
            'hardCurrency':   row['hard_currency'],
            'softCurrency':   int(row['soft_currency']),
            'researchPoints': int(row['research_points']),
            'stashCols':      row['stash_cols'],
            'stashRows':      row['stash_rows'],
        }
    return None

def save_user_wallet(custom_id, hard, soft, research, cols, rows):
    conn = get_conn()
    conn.execute('''INSERT INTO user_wallet (custom_id, hard_currency, soft_currency, research_points, stash_cols, stash_rows, updated_time)
        VALUES (?,?,?,?,?,?,?) ON CONFLICT(custom_id) DO UPDATE SET
        hard_currency=excluded.hard_currency, soft_currency=excluded.soft_currency,
        research_points=excluded.research_points, stash_cols=excluded.stash_cols,
        stash_rows=excluded.stash_rows, updated_time=excluded.updated_time
    ''', (custom_id, hard, str(soft), str(research), cols, rows, time.time()))
    conn.commit()
    conn.close()

def get_user_override(custom_id):
    conn = get_conn()
    row = conn.execute('SELECT * FROM user_overrides WHERE custom_id=?', (custom_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def save_user_override(custom_id, username=None, metadata=None, notes=None, role=None):
    conn = get_conn()
    existing = conn.execute('SELECT * FROM user_overrides WHERE custom_id=?', (custom_id,)).fetchone()
    if existing:
        updates, params = [], []
        if username  is not None: updates.append('username=?');      params.append(username)
        if metadata  is not None: updates.append('metadata_json=?'); params.append(json.dumps(metadata) if isinstance(metadata, dict) else metadata)
        if notes     is not None: updates.append('notes=?');         params.append(notes)
        if role      is not None: updates.append('role=?');          params.append(role)
        updates.append('updated_time=?'); params.append(time.time())
        params.append(custom_id)
        conn.execute(f'UPDATE user_overrides SET {",".join(updates)} WHERE custom_id=?', params)
    else:
        conn.execute('''INSERT INTO user_overrides (custom_id, username, metadata_json, notes, role, updated_time)
            VALUES (?,?,?,?,?,?)''', (
            custom_id,
            username or '',
            json.dumps(metadata) if isinstance(metadata, dict) else (metadata or '{}'),
            notes or '',
            role or 'player',
            time.time()
        ))
    conn.commit()
    conn.close()

def get_user_research(custom_id):
    conn = get_conn()
    row = conn.execute('SELECT nodes_json FROM user_research WHERE custom_id=?', (custom_id,)).fetchone()
    conn.close()
    return json.loads(row['nodes_json']) if row else None

def save_user_research(custom_id, nodes_data):
    conn = get_conn()
    conn.execute('''INSERT INTO user_research (custom_id, nodes_json, updated_time)
        VALUES (?,?,?) ON CONFLICT(custom_id) DO UPDATE SET
        nodes_json=excluded.nodes_json, updated_time=excluded.updated_time
    ''', (custom_id, json.dumps(nodes_data), time.time()))
    conn.commit()
    conn.close()

def get_user_prefs(custom_id):
    conn = get_conn()
    row = conn.execute('SELECT prefs_json FROM user_prefs WHERE custom_id=?', (custom_id,)).fetchone()
    conn.close()
    return json.loads(row['prefs_json']) if row else None

def save_user_prefs(custom_id, prefs):
    conn = get_conn()
    conn.execute('''INSERT INTO user_prefs (custom_id, prefs_json, updated_time)
        VALUES (?,?,?) ON CONFLICT(custom_id) DO UPDATE SET
        prefs_json=excluded.prefs_json, updated_time=excluded.updated_time
    ''', (custom_id, json.dumps(prefs), time.time()))
    conn.commit()
    conn.close()

def get_user_loadout(custom_id):
    conn = get_conn()
    row = conn.execute('SELECT loadout_json FROM user_loadout WHERE custom_id=?', (custom_id,)).fetchone()
    conn.close()
    return json.loads(row['loadout_json']) if row else None

def save_user_loadout(custom_id, loadout):
    conn = get_conn()
    conn.execute('''INSERT INTO user_loadout (custom_id, loadout_json, updated_time)
        VALUES (?,?,?) ON CONFLICT(custom_id) DO UPDATE SET
        loadout_json=excluded.loadout_json, updated_time=excluded.updated_time
    ''', (custom_id, json.dumps(loadout), time.time()))
    conn.commit()
    conn.close()

def save_named_token(label, custom_id, token, refresh_token):
    conn = get_conn()
    conn.execute('INSERT INTO named_tokens (label, custom_id, token, refresh_token, created_at) VALUES (?,?,?,?,?)',
                 (label, custom_id, token, refresh_token, time.time()))
    conn.commit()
    conn.close()

def get_named_tokens():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM named_tokens ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_named_token(token_id):
    conn = get_conn()
    conn.execute('DELETE FROM named_tokens WHERE id=?', (token_id,))
    conn.commit()
    conn.close()

def audit(action, target=None, detail=None):
    try:
        conn = get_conn()
        conn.execute('INSERT INTO audit_log (admin_action, target, detail, performed_at) VALUES (?,?,?,?)',
                     (action, target, detail, time.time()))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_user_cosmetics(custom_id):
    conn = get_conn()
    row = conn.execute('SELECT avatar_json, inventory_json FROM user_cosmetics WHERE custom_id=?', (custom_id,)).fetchone()
    conn.close()
    if row:
        return json.loads(row['avatar_json']), json.loads(row['inventory_json'])
    return None, None

def get_user_stash(custom_id):
    conn = get_conn()
    row = conn.execute('SELECT stash_json FROM user_stash WHERE custom_id=?', (custom_id,)).fetchone()
    conn.close()
    return json.loads(row['stash_json']) if row else None

def save_user_cosmetics(custom_id, avatar, inventory):
    conn = get_conn()
    conn.execute('''INSERT INTO user_cosmetics (custom_id, avatar_json, inventory_json, updated_time)
        VALUES (?,?,?,?) ON CONFLICT(custom_id) DO UPDATE SET
        avatar_json=excluded.avatar_json, inventory_json=excluded.inventory_json, updated_time=excluded.updated_time
    ''', (custom_id, json.dumps(avatar), json.dumps(inventory), time.time()))
    conn.commit()
    conn.close()

def save_user_stash(custom_id, stash):
    conn = get_conn()
    conn.execute('''INSERT INTO user_stash (custom_id, stash_json, updated_time)
        VALUES (?,?,?) ON CONFLICT(custom_id) DO UPDATE SET
        stash_json=excluded.stash_json, updated_time=excluded.updated_time
    ''', (custom_id, json.dumps(stash), time.time()))
    conn.commit()
    conn.close()

def get_config(key, default=''):
    conn = get_conn()
    row = conn.execute('SELECT value FROM server_config WHERE key=?', (key,)).fetchone()
    conn.close()
    return row['value'] if row else default

def set_config(key, value):
    conn = get_conn()
    conn.execute('''INSERT INTO server_config (key, value) VALUES (?,?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value''', (key, value))
    conn.commit()
    conn.close()

# ── JWT ───────────────────────────────────────────────────────────────────────
def b64enc(obj):
    return base64.urlsafe_b64encode(
        json.dumps(obj, separators=(',', ':')).encode()
    ).decode().rstrip('=')

def b64decode_json(s):
    return json.loads(base64.urlsafe_b64decode(s + '=' * (-len(s) % 4)).decode())

def b64encode_json(obj):
    return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode().rstrip('=')

def make_jwt(user_id):
    now = int(time.time())
    header  = {'alg': 'HS256', 'typ': 'JWT'}
    payload = {
        'tid': secrets.token_hex(16),
        'uid': user_id,
        'usn': secrets.token_hex(5),
        'vrs': {
            'authID':          secrets.token_hex(20),
            'clientUserAgent': os.environ.get('CLIENT_USER_AGENT', 'MetaQuest 1.16.3.1138_5edcbd98'),
            'deviceID':        secrets.token_hex(20),
            'loginType':       os.environ.get('LOGIN_TYPE', 'meta_quest'),
        },
        'exp': now + 72000,
        'iat': now,
    }
    h = b64enc(header)
    p = b64enc(payload)
    sig = hmac.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip('=')
    return f"{h}.{p}.{sig_b64}"

def make_token_pair(user_id=None):
    uid = user_id or secrets.token_hex(16)
    return {'token': make_jwt(uid), 'refresh_token': make_jwt(uid)}

# ═══════════════════════════════════════════════════════════════════════════════
#  STATIC DATA
# ═══════════════════════════════════════════════════════════════════════════════
BOOTSTRAP_PAYLOAD = {
    'payload': json.dumps({
        "updateType": "Optional", "attestResult": "Valid",
        "attestTokenExpiresAt": ATTEST_EXPIRES_AT,
        "photonAppID": PHOTON_APP_ID, "photonVoiceAppID": PHOTON_VOICE_APP_ID,
        "termsAcceptanceNeeded": [], "dailyMissionDateKey": "",
        "dailyMissions": None, "dailyMissionResetTime": 0,
        "serverTimeUnix": int(time.time()), "gameDataURL": GAME_DATA_URL
    })
}

ECON_ITEMS = {'payload': '[{"id":"item_apple","netID":71,"name":"Apple","description":"An apple a day keeps the doctor away!","category":"Consumables","price":200,"value":7,"isLoot":true,"isPurchasable":false,"isUnique":false,"isDevOnly":false},{"id":"item_arrow","netID":103,"name":"Arrow","description":"Can be attached to the crossbow.","category":"Ammo","price":199,"value":8,"isLoot":false,"isPurchasable":true,"isUnique":false,"isDevOnly":false},{"id":"item_arrow_heart","netID":116,"name":"Heart Arrow","description":"A love-themed arrow that will have your targets seeing hearts! ","category":"Ammo","price":199,"value":8,"isLoot":false,"isPurchasable":true,"isUnique":false,"isDevOnly":false}]'}

OWNER_WALLET = json.dumps({
    'stashCols': STASH_COLS, 'stashRows': STASH_ROWS,
    'hardCurrency': HARD_CURRENCY, 'softCurrency': SOFT_CURRENCY,
    'researchPoints': RESEARCH_POINTS
})

OWNER_ACCOUNT = {
    'user': {
        'id': OWNER_USER_ID, 'username': OWNER_USERNAME,
        'lang_tag': 'en', 'metadata': '{}', 'edge_count': 4,
        'create_time': '2024-08-24T07:30:12Z', 'update_time': '2025-04-05T21:00:27Z'
    },
    'wallet': OWNER_WALLET,
    'custom_id': OWNER_CUSTOM_ID
}

ALL_RESEARCH_NODES = [
    'node_arrow', 'node_arrow_heart', 'node_arrow_lightbulb', 'node_backpack',
    'node_backpack_large', 'node_backpack_large_basketball', 'node_backpack_large_clover',
    'node_balloon', 'node_balloon_heart', 'node_baseball_bat', 'node_boxfan',
    'node_clapper', 'node_cluster_grenade', 'node_company_ration', 'node_crossbow',
    'node_crossbow_heart', 'node_crowbar', 'node_disposable_camera', 'node_dynamite',
    'node_dynamite_cube', 'node_flaregun', 'node_flashbang', 'node_flashlight_mega',
    'node_football', 'node_frying_pan', 'node_glowsticks', 'node_heart_gun',
    'node_hookshot', 'node_hoverpad', 'node_impact_grenade', 'node_impulse_grenade',
    'node_item_nut_shredder', 'node_jetpack', 'node_lance', 'node_mega_broccoli',
    'node_mini_broccoli', 'node_ogre_hands', 'node_pickaxe', 'node_pickaxe_cny',
    'node_pickaxe_cube', 'node_plunger', 'node_pogostick', 'node_police_baton',
    'node_quiver', 'node_quiver_heart', 'node_revolver', 'node_revolver_ammo',
    'node_rpg', 'node_rpg_ammo', 'node_rpg_cny', 'node_saddle', 'node_shield',
    'node_shield_bones', 'node_shield_police', 'node_shotgun', 'node_shotgun_ammo',
    'node_skill_backpack_cap_1', 'node_skill_backpack_cap_2', 'node_skill_backpack_cap_3',
    'node_skill_explosive_1', 'node_skill_gundamage_1', 'node_skill_health_1',
    'node_skill_health_2', 'node_skill_left_hip_attachment', 'node_skill_melee_1',
    'node_skill_melee_2', 'node_skill_melee_3', 'node_skill_right_hip_attachment',
    'node_skill_selling_1', 'node_skill_selling_2', 'node_skill_selling_3',
    'node_stick_armbones', 'node_stick_bone', 'node_sticker_dispenser',
    'node_sticky_dynamite', 'node_tablet', 'node_teleport_grenade', 'node_theramin',
    'node_tripwire_explosive', 'node_umbrella', 'node_umbrella_clover',
    'node_whoopie', 'node_zipline_gun', 'node_zipline_rope'
]

# Full avatar inventory JSON string (used in storage objects)
ALL_AVATAR_ITEMS_JSON = json.dumps({"items": ALL_AVATAR_ITEMS})

DEFAULT_STORAGE_OBJECTS = [
    {
        'collection': 'user_avatar', 'key': '0', 'user_id': OWNER_USER_ID,
        'value': json.dumps({
            'butt': 'bp_butt_kitten', 'head': 'bp_head_kitten', 'tail': '',
            'torso': 'bp_torso_kitten', 'armLeft': 'bp_arm_l_kitten',
            'eyeLeft': 'bp_eye_kitten', 'armRight': 'bp_arm_r_kitten',
            'eyeRight': 'bp_eye_kitten', 'accessories': ['acc_head_mop'],
            'primaryColor': '604170'
        }),
        'version': '7a326a2a4d0639a5f08e3116bb99a3bf', 'permission_read': 2,
        'create_time': '2024-10-29T00:22:08Z', 'update_time': '2025-04-04T03:55:19Z'
    },
    {
        'collection': 'user_inventory', 'key': 'avatar', 'user_id': OWNER_USER_ID,
        'value': ALL_AVATAR_ITEMS_JSON,
        'version': 'b6a38347a29ec461a06d5e30ed8b3cd8', 'permission_read': 1,
        'create_time': '2024-10-29T00:22:08Z', 'update_time': '2025-04-05T06:21:14Z'
    },
    {
        'collection': 'user_inventory', 'key': 'avatar', 'user_id': intoxicated_USER_ID,
        'value': ALL_AVATAR_ITEMS_JSON,
        'version': '7a326a2a4d0639a5f08e3116bb99a3bf', 'permission_read': 1,
        'create_time': '2024-10-29T00:22:08Z', 'update_time': '2025-04-05T06:21:14Z'
    },
    {
        'collection': 'user_inventory', 'key': 'research', 'user_id': OWNER_USER_ID,
        'value': json.dumps({'nodes': ALL_RESEARCH_NODES}),
        'version': 'bb49186ef5806541f461f4c9f3f4f871', 'permission_read': 1,
        'create_time': '2025-02-20T00:51:38Z', 'update_time': '2025-02-20T01:15:06Z'
    },
    {
        'collection': 'user_inventory', 'key': 'stash', 'user_id': OWNER_USER_ID,
        'value': json.dumps({'items': [], 'stashPos': 0, 'version': 1}),
        'version': '8e192e752405b279447f0523a9049fdd', 'permission_read': 1, 'permission_write': 1,
        'create_time': '2025-02-20T00:51:38Z', 'update_time': '2025-04-05T10:03:13Z'
    },
    {
        'collection': 'user_inventory', 'key': 'stash_upgrades', 'user_id': OWNER_USER_ID,
        'value': json.dumps({"upgrades": ["col_1","col_2","col_3","col_4","col_5","col_6","col_7","col_8","row_1","row_2","row_3","row_4","row_5","row_6","row_7","row_8","mtl_1","mtl_2","mtl_3","mtl_4","mtl_5","mtl_6","mtl_7","mtl_8"]}),
        'version': 'af1feb89bd8c849f5f16a4754577be04', 'permission_read': 1,
        'create_time': '2025-07-23T23:32:02Z', 'update_time': '2025-08-07T17:05:15Z'
    },
    {
        'collection': 'user_inventory', 'key': 'gameplay_loadout', 'user_id': OWNER_USER_ID,
        'value': json.dumps({'version': 1}),
        'version': '77efb8e3fa276d4674932392a66555e4', 'permission_read': 1, 'permission_write': 1,
        'create_time': '2025-02-20T00:51:50Z', 'update_time': '2025-04-05T21:06:17Z'
    },
    {
        'collection': 'user_preferences', 'key': 'gameplay_items', 'user_id': OWNER_USER_ID,
        'value': json.dumps({'recents': [
            'item_backpack_small_base', 'item_flaregun', 'item_tele_grenade',
            'item_glowstick', 'item_jetpack', 'item_stick_bone', 'item_dynamite_cube',
            'item_tablet', 'item_plunger', 'item_flashlight_mega'
        ], 'favorites': ['item_flaregun']}),
        'version': '80aae98f75aab68ca6540247a17cc4a1', 'permission_read': 1, 'permission_write': 1,
        'create_time': '2025-02-20T00:52:27Z', 'update_time': '2025-04-05T21:04:05Z'
    },
    {
        'collection': 'user_preferences', 'key': 'common', 'user_id': OWNER_USER_ID,
        'value': json.dumps({"appearOffline": False}),
        'version': 'd56295314bb7a4c43e13da9c446a77a8', 'permission_read': 1, 'permission_write': 1,
        'create_time': '2025-06-11T03:57:33Z', 'update_time': '2025-08-07T18:09:40Z'
    },
]

def make_gameplay_loadout(custom_id=None):
    if custom_id:
        user_loadout_data = get_user_loadout(custom_id)
        if user_loadout_data and user_loadout_data.get('children') is not None:
            return {
                "objects": [{
                    "collection": "user_inventory", "key": "gameplay_loadout",
                    "permission_read": 1, "permission_write": 1,
                    "value": json.dumps({"version": 1, "back": user_loadout_data})
                }]
            }
    try:
        raw = get_config('spawn_loadout_items', '')
        children = json.loads(raw) if raw else []
        if not children:
            raise ValueError("Empty loadout")
    except Exception:
        children = [
            {"itemID": "item_jetpack",  "scaleModifier": 100, "colorHue": 50, "colorSaturation": 50},
            {"itemID": "item_flaregun", "scaleModifier": 100, "colorHue": 80, "colorSaturation": 60},
        ]
    return {
        "objects": [{
            "collection": "user_inventory", "key": "gameplay_loadout",
            "permission_read": 1, "permission_write": 1,
            "value": json.dumps({"version": 1, "back": {
                "itemID":          get_config('backpack_item',  os.environ.get("BACKPACK_ITEM",  "item_backpack_large_base")),
                "scaleModifier":   int(get_config('backpack_scale', os.environ.get("BACKPACK_SCALE", "120"))),
                "colorHue":        int(get_config('backpack_hue',   os.environ.get("BACKPACK_HUE",   "50"))),
                "colorSaturation": int(get_config('backpack_sat',   os.environ.get("BACKPACK_SAT",   "50"))),
                "children":        children,
            }})
        }]
    }

def build_storage_for_user(user_id, custom_id):
    avatar_override, inventory_override = get_user_cosmetics(custom_id)
    stash_override    = get_user_stash(custom_id)
    research_override = get_user_research(custom_id)
    prefs_override    = get_user_prefs(custom_id)
    loadout           = make_gameplay_loadout(custom_id)
    objects = []
    for obj in DEFAULT_STORAGE_OBJECTS:
        new_obj = obj.copy()
        new_obj['user_id'] = user_id
        key = obj.get('key')
        col = obj.get('collection')
        if col == 'user_avatar' and key == '0' and avatar_override:
            new_obj['value'] = json.dumps(avatar_override)
        elif col == 'user_inventory' and key == 'avatar' and inventory_override:
            new_obj['value'] = json.dumps(inventory_override)
        elif col == 'user_inventory' and key == 'stash' and stash_override:
            new_obj['value'] = json.dumps(stash_override)
        elif col == 'user_inventory' and key == 'research' and research_override:
            new_obj['value'] = json.dumps(research_override)
        elif col == 'user_preferences' and key == 'gameplay_items' and prefs_override:
            new_obj['value'] = json.dumps(prefs_override)
        elif col == 'user_inventory' and key == 'gameplay_loadout':
            new_obj['value'] = loadout['objects'][0]['value']
        objects.append(new_obj)
    return objects

# ═══════════════════════════════════════════════════════════════════════════════
#  DISCORD LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
@app.after_request
def log_to_discord(response):
    if request.path.startswith('/admin'):
        return response
    method       = request.method
    url          = request.url
    path         = request.path
    headers      = dict(request.headers)
    body         = request.get_data(as_text=True)
    query_params = dict(request.args)
    status_code  = response.status_code
    message = {
        'content': f"📡 **Request to: {path}**",
        'embeds': [{'title': 'Request Details', 'fields': [
            {'name': 'Method',       'value': method,         'inline': True},
            {'name': 'Path',         'value': path,           'inline': True},
            {'name': 'Status Code',  'value': M(status_code), 'inline': True},
            {'name': 'Full URL',     'value': url,            'inline': False},
            {'name': 'Query Params', 'value': f"```json\n{json.dumps(query_params, indent=2)}```" if query_params else '*(none)*', 'inline': False},
            {'name': 'Headers',      'value': f"```json\n{json.dumps(headers, indent=2)}```",    'inline': False},
            {'name': 'Body',         'value': f"```json\n{body}```" if body else '*(empty)*',    'inline': False},
        ], 'color': 65280 if status_code < 400 else 16711680}]
    }
    try:
        N.post(DISCORD_WEBHOOK, json=message, timeout=3)
    except G:
        pass
    return response

# ═══════════════════════════════════════════════════════════════════════════════
#  GAME SERVER ROUTES  (doc1 primary + doc2 extras merged)
# ═══════════════════════════════════════════════════════════════════════════════

# ── Auth / Custom authenticate ────────────────────────────────────────────────
@app.route('/v2/account/authenticate/custom', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/3/v2/account/authenticate/custom', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/account/authenticate/custom', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def route_auth_custom():
    ip = get_ip()
    user, _ = get_or_create_user(ip)
    custom_id = user['custom_id'] if user else secrets.token_hex(16)
    device_id = ''
    try:
        data = request.get_json(force=True) or {}
        device_id = data.get('device_id') or data.get('deviceID') or ''
    except Exception:
        pass
    # doc2: ban specific usernames
    username_param = request.args.get("username", "")
    if username_param == "xmissalexanderx":
        return jsonify({"error": "banned for 48 hours REASON: racism"}), 403
    pair = get_or_create_user_token(custom_id, device_id)
    if device_id:
        update_device_id(custom_id, device_id)
    return jsonify(pair)

# ── Account (main) ────────────────────────────────────────────────────────────
@app.route('/v2/account', methods=['GET', 'PUT'])
@app.route('/3/v2/account', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/account', methods=['GET', 'POST', 'PUT'])
def route_account():
    if request.method == 'PUT':
        r = jsonify({})
        r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        r.headers['Content-Type'] = 'application/json'
        r.headers['Grpc-Metadata-Content-Type'] = 'application/grpc'
        return r
    try:
        ip = get_ip()
        user, _ = get_or_create_user(ip)
        if user is None:
            raise G('DB failed')
        custom_id = user['custom_id']
        user_id   = str(uuid.uuid5(uuid.NAMESPACE_DNS, custom_id))

        # doc2: per-username overrides (checked first if token present)
        token = request.args.get("token", "") or request.headers.get("Authorization", "")
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        token_username = None
        try:
            payload = b64decode_json(token.split(".")[1])
            token_username = payload.get("usn")
        except Exception:
            pass

        if token_username:
            per_user = _get_per_username_account(token_username, custom_id, user_id)
            if per_user:
                return jsonify(per_user)

        override = get_user_override(custom_id)
        username = COMPANY_USERNAME
        if is_trusted(ip):
            username = intoxicated_USERNAME
        if override and override.get('username'):
            username = override['username']

        metadata = {'isDeveloper': M(is_trusted(ip))}
        if override and override.get('role') == 'admin':
            metadata['isDeveloper'] = 'True'
            metadata['role'] = 'admin'
        if override and override.get('metadata_json'):
            try:
                extra = json.loads(override['metadata_json'])
                metadata.update(extra)
            except Exception:
                pass

        wallet_data = get_user_wallet(custom_id)
        if wallet_data:
            wallet = json.dumps({
                'stashCols':      wallet_data['stashCols'],
                'stashRows':      wallet_data['stashRows'],
                'hardCurrency':   wallet_data['hardCurrency'],
                'softCurrency':   wallet_data['softCurrency'],
                'researchPoints': wallet_data['researchPoints'],
            })
        else:
            wallet = json.dumps({
                'stashCols':      PUBLIC_STASH_COLS,
                'stashRows':      PUBLIC_STASH_ROWS,
                'hardCurrency':   0,
                'softCurrency':   PUBLIC_SOFT_CURRENCY,
                'researchPoints': PUBLIC_RESEARCH_POINTS,
            })

        return jsonify({
            'user': {
                'id': user_id, 'username': username,
                'lang_tag': 'en',
                'metadata': json.dumps(metadata),
                'edge_count': 4,
                'create_time': '2024-08-24T07:30:12Z',
                'update_time': '2025-04-05T21:00:27Z'
            },
            'wallet': wallet,
            'custom_id': custom_id
        })
    except G as e:
        E(f"[FALLBACK] {e}")
        traceback.print_exc()
        return jsonify(OWNER_ACCOUNT)

def _get_per_username_account(username, custom_id, user_id):
    """Return per-username account overrides from doc2, or None to fall through."""
    special = {
        "unitygame": ("<color=purple>Exploding_Car</color>", "24968022896116226", 99999999999),
        "skibb.ok":  ("<color=yellow>Skibb.Gay</color>",     "24968022896116226", 99999999999),
        "Omelette180": ("<color=purple>COOL PERSON</color>:Omelette", "24968022896116226", 1000000),
        "sergiovr":  ("<color=red>SKIBIDI RIZZ</color>",     custom_id, 1000000),
        "FakeXera":  ("<color=purple>Fake Xera</color>",     custom_id, 1000000),
        "GunyahJohnVr": ("<size=5><color=green>Gunyah</color></size>", custom_id, 1000000),
        "SD_WatchOD": ("<color=blue>Watch</color>",          custom_id, 1000000),
        "kris_kovidov": ("<color=purple>kris_kovidov</color>", custom_id, 1000000),
        "N5.tuff":   ("<color=red>OWNER</color>: N5",        "4938276150923746", 1000000),
    }
    if username not in special:
        return None
    disp, cid, curr = special[username]
    return {
        "user": {
            "id": user_id,
            "username": disp,
            "display_name": disp,
            "lang_tag": "en",
            "metadata": json.dumps({"isDeveloper": True}),
            "edge_count": 240,
            "create_time": "2024-08-24T04:20:56Z",
            "update_time": "2025-07-25T18:41:17Z"
        },
        "wallet": json.dumps({
            "stashCols": PUBLIC_STASH_COLS, "stashRows": PUBLIC_STASH_ROWS,
            "hardCurrency": curr, "softCurrency": curr, "researchPoints": curr
        }),
        "custom_id": cid
    }

# ── Account alt (owner) ───────────────────────────────────────────────────────
@app.route('/v2/account1', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def route_account1():
    return jsonify(OWNER_ACCOUNT)

@app.route('/v2/account/alt2', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def route_account_alt2():
    return jsonify({'objects': DEFAULT_STORAGE_OBJECTS})

# ── Session / Device ──────────────────────────────────────────────────────────
@app.route('/v2/account/session/refresh', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/3/v2/account/session/refresh', methods=['POST', 'GET'])
@app.route('/nnnnaakamacloud.c/v2/account/session/refresh', methods=['POST'])
def route_session_refresh():
    ip = get_ip()
    user, _ = get_or_create_user(ip)
    if user:
        return jsonify(get_or_create_user_token(user['custom_id']))
    return jsonify(make_token_pair())

@app.route('/v2/account/link/device', methods=['POST'])
@app.route('/3/v2/account/link/device', methods=['POST', 'GET'])
@app.route('/nnnnaakamacloud.c/v2/account/link/device', methods=['POST', 'GET'])
def route_link_device():
    try:
        data = request.get_json(force=True) or {}
        device_id = data.get('id') or data.get('device_id') or data.get('deviceID') or ''
        if device_id:
            ip = get_ip()
            user, _ = get_or_create_user(ip)
            if user:
                update_device_id(user['custom_id'], device_id)
    except Exception:
        pass
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    user_id_out = secrets.token_hex(16)
    try:
        payload = b64decode_json(token.split(".")[1])
        user_id_out = payload.get("uid", user_id_out)
    except Exception:
        pass
    return jsonify({
        'id': secrets.token_hex(16), 'user_id': user_id_out,
        'linked': True, 'create_time': '2025-01-15T18:08:45Z'
    })

# ── Attest ────────────────────────────────────────────────────────────────────
@app.route('/v2/rpc/attest.start', methods=['POST'])
@app.route('/3/v2/rpc/attest.start', methods=['POST'])
@app.route('/nnnnaakamacloud.c/v2/rpc/attest.start', methods=['POST'])
def route_attest():
    return jsonify({'payload': json.dumps({'status': 'success', 'attestResult': 'Valid', 'message': 'Attestation validated'})})

# ── Bootstrap ─────────────────────────────────────────────────────────────────
@app.route('/v2/rpc/clientBootstrap', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/3/v2/rpc/clientBootstrap', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/v2/rpc/clientBootstrap', methods=['GET', 'POST'])
def route_bootstrap():
    return jsonify(BOOTSTRAP_PAYLOAD)

# ── Storage ───────────────────────────────────────────────────────────────────
@app.route('/v2/storage', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/3/v2/storage', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage', methods=['GET', 'POST', 'PUT'])
def route_storage():
    if request.method == 'PUT':
        return "ok", 200
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            if data and 'object_ids' in data:
                first     = data['object_ids'][0] if data['object_ids'] else {}
                user_id   = first.get('user_id')
                custom_id = first.get('custom_id', '')
                if not custom_id and user_id:
                    ip = get_ip()
                    user, _ = get_or_create_user(ip)
                    if user:
                        custom_id = user['custom_id']
                if user_id:
                    return jsonify({'objects': build_storage_for_user(user_id, custom_id)})
                return jsonify({'objects': []})
            # fallthrough: return default storage with all items
            return jsonify(_default_storage_response())
        except G as e:
            E(f"Storage error: {e}")
            return jsonify({'objects': []})
    return jsonify(_default_storage_response())

def _default_storage_response():
    """Return the full storage payload with all avatar items for any user."""
    ip = get_ip()
    user, _ = get_or_create_user(ip)
    custom_id = user['custom_id'] if user else ''
    user_id   = str(uuid.uuid5(uuid.NAMESPACE_DNS, custom_id)) if custom_id else OWNER_USER_ID
    return {'objects': build_storage_for_user(user_id, custom_id)}

# ── Econ items ────────────────────────────────────────────────────────────────
@app.route('/v2/storage/econ_gameplay_items', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/3/v2/storage/econ_gameplay_items', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_gameplay_items', methods=['GET', 'POST', 'PUT'])
def route_econ_items():
    # Try loading from file first (doc2 approach), fall back to static (doc1)
    try:
        path = request.path
        base = dih3 if path.startswith('/nnnnaakamacloud.c') else dih2
        fpath = os.path.join(base, 'econ_gameplay_items.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_gameplay_items", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify(ECON_ITEMS)

@app.route('/v2/storage/econ_avatar_items', methods=['GET', 'POST', 'PUT'])
@app.route('/3/v2/storage/econ_avatar_items', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_avatar_items', methods=['GET', 'POST', 'PUT'])
def route_econ_avatar_items():
    try:
        path = request.path
        base = dih3 if path.startswith('/nnnnaakamacloud.c') else dih2
        fpath = os.path.join(base, 'econ_avatar_items.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_avatar_items", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify({"objects": []})

@app.route('/v2/storage/econ_research_nodes', methods=['GET', 'POST', 'PUT'])
@app.route('/3/v2/storage/econ_research_nodes', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_research_nodes', methods=['GET', 'POST', 'PUT'])
def route_econ_research_nodes():
    try:
        path = request.path
        base = dih3 if path.startswith('/nnnnaakamacloud.c') else dih2
        fpath = os.path.join(base, 'econ_research_nodes.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_research_nodes", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify({"objects": []})

@app.route('/v2/storage/econ_products', methods=['GET', 'POST', 'PUT'])
@app.route('/3/v2/storage/econ_products', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_products', methods=['GET', 'POST', 'PUT'])
def route_econ_products():
    try:
        path = request.path
        base = dih3 if path.startswith('/nnnnaakamacloud.c') else dih2
        fpath = os.path.join(base, 'econ_products.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_products", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify({"objects": []})

@app.route('/v2/storage/econ_stash_upgrades', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_stash_upgrades', methods=['GET', 'POST', 'PUT'])
def route_econ_stash_upgrades():
    try:
        path = request.path
        base = dih3 if path.startswith('/nnnnaakamacloud.c') else dih2
        fpath = os.path.join(base, 'econ_stash_upgrades.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_stash_upgrades", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify({"objects": []})

@app.route('/v2/storage/econ_loot_table_bindings', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_loot_table_bindings', methods=['GET', 'POST', 'PUT'])
def route_econ_loot_table_bindings():
    try:
        fpath = os.path.join(dih2, 'econ_loot_table_bindings.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_loot_table_bindings", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify({"objects": []})

@app.route('/v2/storage/econ_loot_table', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_loot_table', methods=['GET', 'POST', 'PUT'])
def route_econ_loot_table():
    try:
        fpath = os.path.join(dih2, 'econ_loot_table.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_loot_table", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify({"objects": []})

@app.route('/v2/storage/econ_crafting_materials', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_crafting_materials', methods=['GET', 'POST', 'PUT'])
def route_econ_crafting_materials():
    try:
        fpath = os.path.join(dih2, 'econ_crafting_materials.json')
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
        newdata = {"objects": []}
        for e in data:
            newdata["objects"].append({
                "collection": "econ_crafting_materials", "key": e["id"],
                "user_id": "00000000-0000-0000-0000-000000000000",
                "value": json.dumps(e), "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
                "permission_read": 2,
                "create_time": "2025-05-28T16:03:59Z", "update_time": "2025-06-11T16:16:56Z"
            })
        return jsonify(newdata)
    except Exception:
        return jsonify({"objects": []})

# ── Mining ────────────────────────────────────────────────────────────────────
@app.route('/v2/rpc/mining.balance', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/v2/rpc/mining.balance', methods=['POST', 'GET'])
def route_mining():
    hard     = int(os.environ.get('MINING_HARD_CURRENCY',   '20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
    research = int(os.environ.get('MINING_RESEARCH_POINTS', '99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999'))
    return jsonify({'payload': json.dumps({'hardCurrency': hard, 'researchPoints': research})}), 200

# ── Purchases ─────────────────────────────────────────────────────────────────
@app.route('/v2/rpc/purchase.list', methods=['GET'])
@app.route('/3/v2/rpc/purchase.list', methods=['GET'])
@app.route('/nnnnaakamacloud.c/v2/rpc/purchase.list', methods=['GET'])
def route_purchase_list():
    return jsonify({'payload': json.dumps({'purchases': [
        {
            'user_id': "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
            'product_id': 'RESEARCH_PACK', 'transaction_id': secrets.token_hex(16), 'store': 3,
            'purchase_time': {'seconds': 1741450711},
            'create_time':   {'seconds': 1741450837, 'nanos': 694669000},
            'update_time':   {'seconds': 1741450837, 'nanos': 694669000},
            'refund_time': {}, 'provider_response': json.dumps({'success': True}), 'environment': 2
        },
        {
            'user_id': "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
            'product_id': 'G.O.A.T_BUNDLE', 'transaction_id': secrets.token_hex(16), 'store': 3,
            'purchase_time': {'seconds': 1741450591},
            'create_time':   {'seconds': 1741450722, 'nanos': 851245000},
            'update_time':   {'seconds': 1741450722, 'nanos': 851245000},
            'refund_time': {}, 'provider_response': json.dumps({'success': True}), 'environment': 2
        },
        {
            'user_id': "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236", 'product_id': 'KPOP_GOLD',
            'transaction_id': '716802304855579', 'store': 3,
            'purchase_time': {'seconds': 1754458259},
            'create_time':   {'seconds': 1754458305, 'nanos': 154543000},
            'update_time':   {'seconds': 1754458305, 'nanos': 154543000},
            'refund_time': {}, 'provider_response': json.dumps({'success': True, 'grant_time': 1754458259}), 'environment': 2
        },
        {
            'user_id': "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236", 'product_id': 'CHAMELEON_BUNDLE',
            'transaction_id': '642819158920561', 'store': 3,
            'purchase_time': {'seconds': 1748315321},
            'create_time':   {'seconds': 1748315350, 'nanos': 615822000},
            'update_time':   {'seconds': 1748315350, 'nanos': 615822000},
            'refund_time': {}, 'provider_response': json.dumps({'success': True, 'grant_time': 1748315321}), 'environment': 2
        },
    ]})}), 200

@app.route('/v2/rpc/purchase.avatarItems', methods=['POST'])
@app.route('/3/v2/rpc/purchase.avatarItems', methods=['POST'])
def route_purchase_avatar():
    return jsonify({'payload': ''})

@app.route('/v2/rpc/purchase.gameplayItems', methods=['POST'])
@app.route('/3/v2/rpc/purchase.gameplayItems', methods=['POST'])
def route_purchase_gameplay():
    return jsonify({'payload': ''})

# ── Research unlock ───────────────────────────────────────────────────────────
@app.route('/v2/rpc/research.unlock', methods=['POST'])
@app.route('/3/v2/rpc/research.unlock', methods=['POST'])
@app.route('/nnnnaakamacloud.c/v2/rpc/research.unlock', methods=['POST'])
def route_research_unlock():
    return jsonify({
        "payload": json.dumps({"succeeded": True, "wallet": {"softCurrency": 418291, "hardCurrency": 418291, "researchPoints": 418291}})
    })

# ── Wallet update ─────────────────────────────────────────────────────────────
@app.route('/v2/rpc/updateWalletSoftCurrency', methods=['POST', 'GET'])
@app.route('/3/v2/rpc/updateWalletSoftCurrency', methods=['POST', 'GET'])
def route_update_wallet():
    return jsonify({"Payload": "{\"ok\"}"})

# ── Avatar update ─────────────────────────────────────────────────────────────
@app.route('/v2/rpc/avatar.update', methods=['GET', 'POST', 'PUT'])
@app.route('/3/v2/rpc/avatar.update', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/rpc/avatar.update', methods=['POST'])
def route_avatar_update():
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    try:
        payload = b64decode_json(token.split(".")[1])
        _ = payload["usn"]
    except Exception:
        return jsonify({"error": "invalid token"}), 403
    return jsonify({"payload": "{\"succeeded\":true,\"errorCode\":\"\"}"})

# ── Sanctions ─────────────────────────────────────────────────────────────────
@app.route('/v2/rpc/user.getActiveSanctions', methods=['GET'])
@app.route('/3/v2/rpc/user.getActiveSanctions', methods=['GET'])
@app.route('/nnnnaakamacloud.c/v2/rpc/user.getActiveSanctions', methods=['GET'])
def route_sanctions():
    return jsonify({"payload": "[]"})

# ── User lookup ───────────────────────────────────────────────────────────────
@app.route('/v2/user', methods=['POST', 'GET'])
@app.route('/nnnnaakamacloud.c/v2/user', methods=['POST', 'GET'])
def route_user():
    id_param = request.args.get("ids")
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    try:
        payload = b64decode_json(token.split(".")[1])
        username = payload["usn"]
    except Exception:
        return jsonify({"error": "invalid token"}), 403
    return jsonify({"username": username, "id": id_param})

# ── Friends ───────────────────────────────────────────────────────────────────
@app.route('/v2/friends', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/v2/friends', methods=['GET', 'POST'])
def route_friends():
    return jsonify({
        "friends": [
            {
                "user": {
                    "id": "8c1acc32f2454fb9a9a76fb6dfbf572f",
                    "username": "<color=red>OWNER</color>: THUNDA",
                    "display_name": "<color=red>OWNER</color>: THUNDA",
                    "lang_tag": "en",
                    "metadata": "{\"IsDeveloper\": true}",
                    "create_time": "2024-10-19T10:33:56Z",
                    "update_time": "2025-07-23T17:58:40Z"
                },
                "state": 1,
                "update_time": "2025-02-20T13:46:53Z",
                "metadata": "{\"IsDeveloper\": true}"
            }
        ],
        "cursor": "M_-DAwEBDmVkZ2VMaXN0Q3Vyc29yAf-EAAECAQVTdGF0ZQEEAAEIUG9zaXRpb24BBAAAAA3_hAL4MIT4gPadsnQA"
    })

# ── Promo redeem ──────────────────────────────────────────────────────────────
@app.route('/3/v2/rpc/promo.redeem', methods=['POST', 'GET'])
@app.route('/v2/rpc/promo.redeem', methods=['POST', 'GET'])
def route_promo_redeem():
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    try:
        payload = b64decode_json(token.split(".")[1])
        _ = payload["usn"]
    except Exception:
        return jsonify({"error": "invalid token"}), 403
    return jsonify({"payload": json.dumps({"succeeded": False, "errorCode": "INVALID_CODE"})})

# ── Photon auth ───────────────────────────────────────────────────────────────
@app.route('/auth', methods=['GET', 'POST'])
@app.route('/Halloween/authenticEate/Redo/Sigma', methods=['GET', 'POST'])
def route_photon_auth():
    auth_token = request.args.get('auth_token')
    userid = secrets.token_hex(16)
    sessionid = secrets.token_hex(12)
    return jsonify({
        'ResultCode': 1,
        'Message': 'Authentication successful' if auth_token else 'Authenticated without token',
        'UserId': userid,
        'SessionID': sessionid,
        'Authenticated': True
    }), 200

# ── Preauth (doc2) ────────────────────────────────────────────────────────────
@app.route('/nnnnaakamacloud/api/v1/preauth', methods=['POST'])
def route_preauth():
    playershit = request.get_json() or {}
    AttestID   = str(uuid.uuid4())
    PUI        = playershit.get("platformUserID", "")
    DeviceID   = request.headers.get("X-Device-Id", "")
    FBItype    = request.headers.get("User-Agent", "")
    data_in    = f"{PUI}|{DeviceID}|{FBItype}"
    salt       = os.urandom(16)
    digest     = hashlib.sha256(salt + data_in.encode()).digest()
    nonce      = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    mid        = len(nonce) // 2
    nonce      = nonce[:mid] + "-" + nonce[mid:]
    return jsonify({
        "time": "gfshrtfhfghjfgd",
        "updateType": "Skidding",
        "attestID": AttestID,
        "attestNonce": nonce
    })

# ── Root ──────────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/', methods=['GET', 'POST'])
def route_root():
    return jsonify({"token": "b"}), 200

# ── Game data zip ─────────────────────────────────────────────────────────────
@app.route('/game-data-prod.zip')
def route_game_data():
    file_name = os.environ.get('GAME_DATA_FILE', 'April.zip')
    file_path = os.path.join(SITE_PATH, file_name)
    if not os.path.exists(file_path):
        return 'File not found', 404
    try:
        return send_file(file_path, mimetype='application/zip',
                         as_attachment=False, download_name=file_name, max_age=3600)
    except G as e:
        return f"Error: {M(e)}", 500

# ── Item spawn queue (polled by game client) ──────────────────────────────────
@app.route('/v2/rpc/admin.spawn', methods=['POST'])
def route_admin_spawn():
    try:
        data = request.get_json(force=True) or {}
        custom_id = data.get('custom_id')
        conn = get_conn()
        now = time.time()
        conn.execute('DELETE FROM spawn_queue WHERE expires_at IS NOT NULL AND expires_at < ?', (now,))
        rows = conn.execute(
            'SELECT * FROM spawn_queue WHERE spawned=0 AND (custom_id IS NULL OR custom_id=?) ORDER BY created_at ASC LIMIT 10',
            (custom_id,)
        ).fetchall()
        spawns = []
        for row in rows:
            spawns.append({
                'id': row['id'],
                'itemID': row['item_id'],
                'position': {'x': row['pos_x'], 'y': row['pos_y'], 'z': row['pos_z']},
                'scale': row['scale'],
                'colorHue': row['color_hue'],
                'colorSaturation': row['color_sat']
            })
            conn.execute('UPDATE spawn_queue SET spawned=1 WHERE id=?', (row['id'],))
        conn.commit()
        conn.close()
        return jsonify({'payload': json.dumps({'spawns': spawns})})
    except Exception as e:
        E(f"Spawn error: {e}")
        return jsonify({'payload': json.dumps({'spawns': []})}), 500

# ── Debug ─────────────────────────────────────────────────────────────────────
@app.route('/debug', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def route_debug():
    method  = request.method
    url     = request.url
    headers = dict(request.headers)
    body    = request.get_data(as_text=True)
    message = {
        'content': '📡 **/debug request received**',
        'embeds': [{'title': 'Request Info', 'fields': [
            {'name': 'Method',  'value': method, 'inline': True},
            {'name': 'URL',     'value': url,    'inline': False},
            {'name': 'Headers', 'value': f"```json\n{json.dumps(headers, indent=2)}```", 'inline': False},
            {'name': 'Body',    'value': f"```json\n{body}```" if body else '*(empty)*',  'inline': False},
        ], 'color': 65484}]
    }
    try:
        N.post(DISCORD_WEBHOOK, json=message, timeout=3)
    except G as e:
        return f"Failed to send to Discord: {e}", 500
    return 'Sent debug to discord', 200

# ═══════════════════════════════════════════════════════════════════════════════
#  ADMIN PANEL HTML  (unchanged from doc1)
# ═══════════════════════════════════════════════════════════════════════════════
ADMIN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>X ADMIN</title>
<link href="https://fonts.googleapis.com/css2?family=Syne+Mono&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b0b0f;--surface:#111118;--border:#2a2a3a;--accent:#7c3aed;--accent2:#06b6d4;--warn:#f59e0b;--danger:#ef4444;--ok:#22c55e;--text:#e2e8f0;--muted:#64748b;--mono:'Syne Mono',monospace;--display:'Syne',sans-serif;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:var(--mono);font-size:13px;min-height:100vh;}
#login-screen{display:flex;align-items:center;justify-content:center;min-height:100vh;background:radial-gradient(ellipse at 50% 40%,#1e0a3c 0%,#0b0b0f 70%);}
.login-box{border:1px solid var(--accent);padding:48px 40px;width:360px;background:var(--surface);box-shadow:0 0 60px #7c3aed33;}
.login-box h1{font-family:var(--display);font-size:2rem;font-weight:800;color:var(--accent);letter-spacing:-0.02em;margin-bottom:6px;}
.login-box p{color:var(--muted);margin-bottom:32px;font-size:12px;letter-spacing:.05em;}
.login-box input{width:100%;padding:12px;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);font-size:14px;margin-bottom:12px;outline:none;transition:border-color .2s;}
.login-box input:focus{border-color:var(--accent);}
.login-box button{width:100%;padding:13px;background:var(--accent);border:none;color:#fff;font-family:var(--display);font-weight:700;font-size:14px;letter-spacing:.08em;cursor:pointer;transition:opacity .2s;}
.login-box button:hover{opacity:.85;}
.login-err{color:var(--danger);font-size:12px;margin-top:8px;min-height:16px;}
#shell{display:none;}
.topbar{height:52px;border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 16px;background:var(--surface);gap:2px;flex-wrap:wrap;}
.topbar-brand{font-family:var(--display);font-weight:800;font-size:1.1rem;color:var(--accent);letter-spacing:-0.01em;margin-right:auto;}
.topbar-brand span{color:var(--accent2);}
.tab-btn{background:none;border:none;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;padding:6px 9px;border-bottom:2px solid transparent;transition:color .15s,border-color .15s;}
.tab-btn.active{color:var(--text);border-color:var(--accent);}
.tab-btn:hover:not(.active){color:var(--text);}
.content{padding:28px;max-width:1300px;margin:0 auto;}
.panel-title{font-family:var(--display);font-weight:800;font-size:1.4rem;margin-bottom:24px;letter-spacing:-0.02em;}
.panel-title span{color:var(--accent);}
.tab-panel{display:none;}.tab-panel.active{display:block;}
.card{background:var(--surface);border:1px solid var(--border);padding:24px;margin-bottom:20px;}
.card label{display:block;color:var(--muted);font-size:11px;letter-spacing:.15em;text-transform:uppercase;margin-bottom:8px;}
.card input,.card select{width:100%;padding:10px 12px;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);font-size:13px;outline:none;margin-bottom:16px;transition:border-color .2s;}
.card input:focus,.card select:focus{border-color:var(--accent2);}
.btn{padding:10px 24px;border:none;cursor:pointer;font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.1em;text-transform:uppercase;transition:opacity .2s;}
.btn:hover{opacity:.8;}
.btn-primary{background:var(--accent);color:#fff;}
.btn-cyan{background:var(--accent2);color:#0b0b0f;}
.btn-ok{background:var(--ok);color:#0b0b0f;}
.btn-danger{background:var(--danger);color:#fff;}
.btn-warn{background:var(--warn);color:#0b0b0f;}
.btn-ghost{background:transparent;border:1px solid var(--border);color:var(--muted);}
.btn-sm{padding:6px 14px;font-size:11px;}
.btn-xs{padding:4px 10px;font-size:10px;}
.token-output{background:#0b0b0f;border:1px solid var(--border);padding:16px;margin-top:16px;word-break:break-all;font-size:11px;color:var(--accent2);line-height:1.7;max-height:220px;overflow-y:auto;display:none;cursor:pointer;}
.copy-hint{font-size:11px;color:var(--muted);margin-top:6px;}
.search-row{display:flex;gap:12px;margin-bottom:16px;}
.search-row input{flex:1;padding:10px 12px;background:var(--surface);border:1px solid var(--border);color:var(--text);font-family:var(--mono);font-size:13px;outline:none;}
.search-row input:focus{border-color:var(--accent2);}
.table-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;}
th{text-align:left;padding:10px 14px;color:var(--muted);font-size:11px;letter-spacing:.1em;text-transform:uppercase;border-bottom:1px solid var(--border);background:var(--surface);}
td{padding:9px 14px;border-bottom:1px solid #1a1a24;vertical-align:middle;}
tr:hover td{background:#13131c;}
.badge{display:inline-block;padding:2px 8px;font-size:10px;letter-spacing:.08em;text-transform:uppercase;}
.badge-ok{background:#052e16;color:var(--ok);}
.badge-danger{background:#1c0909;color:var(--danger);}
.badge-warn{background:#2a1800;color:var(--warn);}
.badge-cyan{background:#002a30;color:var(--accent2);}
.badge-purple{background:#1e0a3c;color:#c084fc;}
.editor-layout{display:grid;grid-template-columns:260px 1fr;gap:20px;}
.player-list-panel{background:var(--surface);border:1px solid var(--border);max-height:680px;overflow-y:auto;}
.player-list-panel .search-box{padding:10px;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--surface);z-index:1;}
.player-list-panel .search-box input{width:100%;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);padding:7px 10px;outline:none;font-size:12px;}
.player-entry{padding:10px 14px;cursor:pointer;border-bottom:1px solid #1a1a24;transition:background .1s;}
.player-entry:hover{background:#13131c;}
.player-entry.selected{background:#1e0a3c;border-left:3px solid var(--accent);}
.player-entry .pname{font-size:12px;color:var(--text);}
.player-entry .pid{font-size:10px;color:var(--muted);margin-top:2px;}
.player-entry .prole{font-size:10px;color:var(--accent2);margin-top:1px;}
.editor-panel{background:var(--surface);border:1px solid var(--border);padding:22px;overflow-y:auto;max-height:680px;}
.editor-panel h3{font-family:var(--display);font-weight:700;font-size:1rem;margin-bottom:18px;color:var(--accent2);}
.field-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;}
.field-grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px;}
.field-group label{display:block;color:var(--muted);font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:5px;}
.field-group input,.field-group select{width:100%;padding:8px 10px;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);font-size:12px;outline:none;transition:border-color .2s;}
.field-group input:focus,.field-group select:focus{border-color:var(--accent);}
textarea.json-edit{width:100%;min-height:180px;background:#0b0b0f;border:1px solid var(--border);color:var(--accent2);font-family:var(--mono);font-size:11px;padding:12px;outline:none;resize:vertical;line-height:1.6;}
textarea.json-edit:focus{border-color:var(--accent);}
.stash-item-row{display:flex;gap:6px;align-items:center;margin-bottom:6px;background:#0b0b0f;padding:7px 9px;border:1px solid var(--border);}
.stash-item-row input{flex:1;background:transparent;border:none;color:var(--text);font-family:var(--mono);font-size:12px;outline:none;}
.stash-item-row input::placeholder{color:var(--muted);}
.stash-num{width:65px!important;flex:none!important;}
.toast{position:fixed;bottom:24px;right:24px;padding:12px 20px;font-size:12px;border-left:4px solid var(--ok);background:var(--surface);border-top:1px solid var(--border);border-right:1px solid var(--border);border-bottom:1px solid var(--border);opacity:0;transform:translateY(10px);transition:opacity .25s,transform .25s;pointer-events:none;z-index:999;}
.toast.show{opacity:1;transform:translateY(0);}
.toast.err{border-left-color:var(--danger);}
.notice{padding:14px;background:#0d0d18;border:1px solid var(--border);color:var(--muted);font-size:12px;margin-bottom:16px;}
.row-btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px;}
.section-sep{border:none;border-top:1px solid var(--border);margin:18px 0;}
.acc-items-list{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;}
.acc-tag{display:flex;align-items:center;gap:5px;background:#1e0a3c;padding:3px 8px;font-size:11px;}
.acc-tag button{background:none;border:none;color:var(--danger);cursor:pointer;font-size:13px;line-height:1;padding:0;}
.stat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;margin-bottom:24px;}
.stat-card{background:var(--surface);border:1px solid var(--border);padding:18px 20px;}
.stat-card .sv{font-family:var(--display);font-size:1.8rem;font-weight:800;color:var(--accent);margin-bottom:4px;}
.stat-card .sk{font-size:11px;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;}
.tabs-inner{display:flex;gap:8px;margin-bottom:16px;border-bottom:1px solid var(--border);padding-bottom:8px;}
.itab{background:none;border:none;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;padding:4px 10px;border-bottom:2px solid transparent;}
.itab.on{color:var(--text);border-color:var(--accent2);}
.named-token-row{display:flex;gap:8px;align-items:center;background:#0b0b0f;padding:10px 12px;border:1px solid var(--border);margin-bottom:8px;flex-wrap:wrap;}
.named-token-row .nt-label{font-size:12px;color:var(--accent2);min-width:120px;}
.named-token-row .nt-cid{font-size:11px;color:var(--muted);flex:1;}
.named-token-row .nt-token{font-size:10px;color:var(--text);flex:2;word-break:break-all;cursor:pointer;}
.audit-row td{font-size:11px;}
.research-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px;margin-bottom:16px;max-height:300px;overflow-y:auto;background:#0b0b0f;padding:12px;border:1px solid var(--border);}
.rnode{display:flex;align-items:center;gap:6px;padding:4px 6px;cursor:pointer;}
.rnode:hover{background:#1a1a24;}
.rnode input[type=checkbox]{accent-color:var(--accent);}
.rnode label{font-size:11px;cursor:pointer;}
.ban-form{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;align-items:flex-end;}
.ban-form input{padding:9px 10px;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);font-size:12px;outline:none;flex:1;min-width:120px;}
.ban-form input:focus{border-color:var(--danger);}
</style>
</head>
<body>
<div id="login-screen">
  <div class="login-box">
    <h1>X</h1>
    <p>// ADMIN CONTROL PANEL //</p>
    <input type="password" id="pw-input" placeholder="Admin password">
    <button onclick="doLogin()">ENTER</button>
    <div class="login-err" id="login-err"></div>
  </div>
</div>
<div id="shell">
  <div class="topbar">
    <div class="topbar-brand">X <span>ADMIN</span></div>
    <button class="tab-btn active" onclick="switchTab('dashboard',this)">Dashboard</button>
    <button class="tab-btn" onclick="switchTab('players',this)">Players</button>
    <button class="tab-btn" onclick="switchTab('roles',this)">Roles</button>
    <button class="tab-btn" onclick="switchTab('bans',this)">Bans</button>
    <button class="tab-btn" onclick="switchTab('tokens',this)">Tokens</button>
    <button class="tab-btn" onclick="switchTab('cosmetics',this)">Cosmetics</button>
    <button class="tab-btn" onclick="switchTab('stash',this)">Stash</button>
    <button class="tab-btn" onclick="switchTab('loadout',this)">Loadout</button>
    <button class="tab-btn" onclick="switchTab('wallet',this)">Wallet</button>
    <button class="tab-btn" onclick="switchTab('research',this)">Research</button>
    <button class="tab-btn" onclick="switchTab('prefs',this)">Prefs</button>
    <button class="tab-btn" onclick="switchTab('spawn',this)">Spawn</button>
    <button class="tab-btn" onclick="switchTab('audit',this)">Audit</button>
  </div>
  <div class="content">
    <!-- DASHBOARD -->
    <div class="tab-panel active" id="tab-dashboard">
      <div class="panel-title">Server <span>Dashboard</span></div>
      <div class="stat-grid" id="stat-grid"></div>
      <div class="card">
        <label>Quick Actions</label>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
          <button class="btn btn-cyan" onclick="loadDashboard()">↺ REFRESH</button>
          <button class="btn btn-primary" onclick="switchTabByName('players')">PLAYERS</button>
          <button class="btn btn-warn" onclick="switchTabByName('roles')">ROLES</button>
          <button class="btn btn-danger" onclick="switchTabByName('bans')">BANS</button>
          <button class="btn btn-ok" onclick="switchTabByName('spawn')">SPAWN ITEMS</button>
          <button class="btn btn-ghost" onclick="switchTabByName('audit')">AUDIT LOG</button>
        </div>
      </div>
      <div class="card">
        <label>Recent Players</label>
        <div class="table-wrap"><table>
          <thead><tr><th>Username</th><th>In-Game Name</th><th>Custom ID</th><th>IP</th><th>Role</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody id="recent-tbody"></tbody>
        </table></div>
      </div>
    </div>
    <!-- PLAYERS -->
    <div class="tab-panel" id="tab-players">
      <div class="panel-title">Player <span>Registry</span></div>
      <div class="search-row">
        <input type="text" id="player-search" placeholder="Search IP, username, custom ID..." oninput="filterPlayers()">
        <button class="btn btn-cyan" onclick="loadPlayers()">↺ REFRESH</button>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Username</th><th>In-Game Name</th><th>Custom ID</th><th>IP</th><th>Role</th><th>Joined</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody id="players-tbody"></tbody>
        </table>
      </div>
    </div>
    <!-- ROLES -->
    <div class="tab-panel" id="tab-roles">
      <div class="panel-title">Role <span>Management</span></div>
      <div class="card">
        <label>Set Player Role &amp; In-Game Name</label>
        <div class="field-grid">
          <div class="field-group"><label>Custom ID</label><input type="text" id="role-cid" placeholder="12345678901234567"></div>
          <div class="field-group"><label>Role</label><select id="role-select"><option value="player">Player</option><option value="moderator">Moderator</option><option value="admin">Admin</option><option value="vip">VIP</option></select></div>
        </div>
        <div class="field-group" style="margin-bottom:16px;"><label>In-Game Username (supports color tags)</label><input type="text" id="role-username" placeholder="&lt;color=red&gt;Admin&lt;/color&gt;Name"></div>
        <div class="notice">💡 Color tags: &lt;color=red&gt;, &lt;color=blue&gt;, &lt;color=green&gt;, &lt;color=yellow&gt;, &lt;color=purple&gt;</div>
        <div class="row-btns"><button class="btn btn-primary" onclick="updateRole()">SAVE ROLE</button><button class="btn btn-ghost" onclick="clearRoleForm()">CLEAR</button></div>
      </div>
      <div class="search-row"><input type="text" id="role-search" placeholder="Search..." oninput="filterRoles()"><button class="btn btn-cyan" onclick="loadPlayers().then(renderRoles)">↺ REFRESH</button></div>
      <div class="table-wrap"><table><thead><tr><th>Username</th><th>In-Game Name</th><th>Custom ID</th><th>Role</th><th>Actions</th></tr></thead><tbody id="roles-tbody"></tbody></table></div>
    </div>
    <!-- BANS -->
    <div class="tab-panel" id="tab-bans">
      <div class="panel-title">Ban <span>Manager</span></div>
      <div class="card">
        <label>Add Ban</label>
        <div class="ban-form">
          <input type="text" id="ban-ip" placeholder="IP (optional)">
          <input type="text" id="ban-cid" placeholder="Custom ID (optional)">
          <input type="text" id="ban-reason" placeholder="Reason">
          <button class="btn btn-danger" onclick="addBan()">BAN</button>
        </div>
        <div class="notice">💡 Ban by IP, Custom ID, or both. At least one is required.</div>
      </div>
      <div class="search-row"><input type="text" id="ban-search" placeholder="Search bans..." oninput="filterBans()"><button class="btn btn-cyan" onclick="loadBans()">↺ REFRESH</button></div>
      <div class="table-wrap"><table><thead><tr><th>IP</th><th>Custom ID</th><th>Reason</th><th>Banned At</th><th>Actions</th></tr></thead><tbody id="bans-tbody"></tbody></table></div>
    </div>
    <!-- TOKENS -->
    <div class="tab-panel" id="tab-tokens">
      <div class="panel-title">Token <span>Generator</span></div>
      <div class="tabs-inner"><button class="itab on" onclick="tokenTab('generate',this)">Generate</button><button class="itab" onclick="tokenTab('saved',this)">Saved Tokens</button></div>
      <div id="token-generate-panel">
        <div class="card">
          <label>User ID / Custom ID (blank = random)</label><input type="text" id="token-uid" placeholder="e.g. 2e8aace0-282d-4c3d-b9d4-6a3b3ba2c2a6">
          <label>Label (optional — saves the token)</label><input type="text" id="token-label" placeholder="e.g. my_headset">
          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <button class="btn btn-primary" onclick="genToken()">GENERATE</button>
            <button class="btn btn-cyan" onclick="genTokenOwner()">OWNER TOKEN</button>
            <button class="btn btn-ok" onclick="genAndSaveToken()">GENERATE &amp; SAVE</button>
          </div>
          <div class="token-output" id="token-output"></div>
          <div class="copy-hint" id="copy-hint"></div>
        </div>
        <div class="notice">⚠️ Tokens expire in 20 hours. JWT_SECRET env var must stay consistent across restarts.</div>
      </div>
      <div id="token-saved-panel" style="display:none;">
        <div class="card"><label>Saved / Named Tokens</label><div id="named-tokens-list"><div style="color:var(--muted);font-size:12px;">Loading...</div></div><button class="btn btn-cyan" style="margin-top:12px;" onclick="loadNamedTokens()">↺ REFRESH</button></div>
      </div>
    </div>
    <!-- COSMETICS -->
    <div class="tab-panel" id="tab-cosmetics">
      <div class="panel-title">Cosmetic <span>Editor</span></div>
      <div class="editor-layout">
        <div class="player-list-panel"><div class="search-box"><input type="text" placeholder="Filter..." id="cosm-search" oninput="filterSidebar('cosm',this.value)"></div><div id="cosm-player-list"></div></div>
        <div class="editor-panel" id="cosm-editor"><div style="color:var(--muted);font-size:12px;">← Select a player</div></div>
      </div>
    </div>
    <!-- STASH -->
    <div class="tab-panel" id="tab-stash">
      <div class="panel-title">Stash <span>Editor</span></div>
      <div class="editor-layout">
        <div class="player-list-panel"><div class="search-box"><input type="text" placeholder="Filter..." id="stash-search" oninput="filterSidebar('stash',this.value)"></div><div id="stash-player-list"></div></div>
        <div class="editor-panel" id="stash-editor"><div style="color:var(--muted);font-size:12px;">← Select a player</div></div>
      </div>
    </div>
    <!-- LOADOUT -->
    <div class="tab-panel" id="tab-loadout">
      <div class="panel-title">Spawn <span>Loadout</span></div>
      <div class="tabs-inner"><button class="itab on" onclick="loadoutTab('global',this)">Global Default</button><button class="itab" onclick="loadoutTab('peruser',this)">Per-Player</button></div>
      <div id="loadout-global-panel">
        <div class="card">
          <div class="field-grid">
            <div class="field-group"><label>Backpack item ID</label><input type="text" id="bp-item" value="item_backpack_large_base"></div>
            <div class="field-group"><label>Scale</label><input type="number" id="bp-scale" value="120" min="50" max="300"></div>
            <div class="field-group"><label>Color Hue</label><input type="number" id="bp-hue" value="50" min="0" max="360"></div>
            <div class="field-group"><label>Color Saturation</label><input type="number" id="bp-sat" value="50" min="0" max="100"></div>
          </div>
        </div>
        <div class="card">
          <label>Spawn Items</label>
          <div id="loadout-item-list" style="margin-bottom:12px;"></div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;"><input type="text" id="new-loadout-item" placeholder="item_jetpack" style="flex:1;padding:9px 10px;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);outline:none;"><button class="btn btn-cyan" onclick="addLoadoutItem()">+ ADD</button></div>
          <div style="margin-bottom:8px;color:var(--muted);font-size:11px;letter-spacing:.1em;text-transform:uppercase;">Quick add</div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:20px;" id="loadout-quickadd"></div>
          <button class="btn btn-primary" onclick="saveLoadout()">SAVE LOADOUT</button>
        </div>
        <div class="notice">💡 Changes take effect immediately for new connections.</div>
      </div>
      <div id="loadout-peruser-panel" style="display:none;">
        <div class="editor-layout">
          <div class="player-list-panel"><div class="search-box"><input type="text" placeholder="Filter..." id="loadout-search" oninput="filterSidebar('loadout',this.value)"></div><div id="loadout-player-list"></div></div>
          <div class="editor-panel" id="loadout-editor"><div style="color:var(--muted);font-size:12px;">← Select a player</div></div>
        </div>
      </div>
    </div>
    <!-- WALLET -->
    <div class="tab-panel" id="tab-wallet">
      <div class="panel-title">Wallet <span>Editor</span></div>
      <div class="editor-layout">
        <div class="player-list-panel"><div class="search-box"><input type="text" placeholder="Filter..." id="wallet-search" oninput="filterSidebar('wallet',this.value)"></div><div id="wallet-player-list"></div></div>
        <div class="editor-panel" id="wallet-editor"><div style="color:var(--muted);font-size:12px;">← Select a player</div></div>
      </div>
    </div>
    <!-- RESEARCH -->
    <div class="tab-panel" id="tab-research">
      <div class="panel-title">Research <span>Nodes</span></div>
      <div class="editor-layout">
        <div class="player-list-panel"><div class="search-box"><input type="text" placeholder="Filter..." id="research-search" oninput="filterSidebar('research',this.value)"></div><div id="research-player-list"></div></div>
        <div class="editor-panel" id="research-editor"><div style="color:var(--muted);font-size:12px;">← Select a player</div></div>
      </div>
    </div>
    <!-- PREFS -->
    <div class="tab-panel" id="tab-prefs">
      <div class="panel-title">Player <span>Preferences</span></div>
      <div class="editor-layout">
        <div class="player-list-panel"><div class="search-box"><input type="text" placeholder="Filter..." id="prefs-search" oninput="filterSidebar('prefs',this.value)"></div><div id="prefs-player-list"></div></div>
        <div class="editor-panel" id="prefs-editor"><div style="color:var(--muted);font-size:12px;">← Select a player</div></div>
      </div>
    </div>
    <!-- SPAWN -->
    <div class="tab-panel" id="tab-spawn">
      <div class="panel-title">Item <span>Spawning</span></div>
      <div class="card">
        <label>Spawn Item at Position</label>
        <div class="field-grid-3">
          <div class="field-group"><label>Item ID</label><input type="text" id="spawn-item-id" placeholder="item_jetpack" value="item_jetpack"></div>
          <div class="field-group"><label>Target Custom ID (blank = global)</label><input type="text" id="spawn-custom-id" placeholder="Leave blank for all players"></div>
          <div class="field-group"><label>Scale</label><input type="number" id="spawn-scale" value="1.0" step="0.1" min="0.1"></div>
        </div>
        <div class="field-grid-3">
          <div class="field-group"><label>Pos X</label><input type="number" id="spawn-x" value="0" step="0.1"></div>
          <div class="field-group"><label>Pos Y</label><input type="number" id="spawn-y" value="0" step="0.1"></div>
          <div class="field-group"><label>Pos Z</label><input type="number" id="spawn-z" value="0" step="0.1"></div>
        </div>
        <div class="field-grid-3">
          <div class="field-group"><label>Color Hue (0-360)</label><input type="number" id="spawn-hue" value="0" min="0" max="360"></div>
          <div class="field-group"><label>Color Saturation (0-100)</label><input type="number" id="spawn-sat" value="0" min="0" max="100"></div>
          <div class="field-group"><label>Expires In Seconds (0=never)</label><input type="number" id="spawn-expires" value="300" min="0"></div>
        </div>
        <div class="notice">💡 Items: item_jetpack, item_flaregun, item_dynamite, item_tablet, item_crossbow, item_revolver, item_shotgun, item_shield, item_hookshot</div>
        <div class="row-btns">
          <button class="btn btn-primary" onclick="spawnItem()">SPAWN</button>
          <button class="btn btn-warn" onclick="spawnPreset('item_jetpack')">JETPACK</button>
          <button class="btn btn-warn" onclick="spawnPreset('item_flaregun')">FLAREGUN</button>
          <button class="btn btn-warn" onclick="spawnPreset('item_dynamite')">DYNAMITE</button>
          <button class="btn btn-cyan" onclick="loadSpawnQueue()">↺ REFRESH QUEUE</button>
        </div>
      </div>
      <div class="card">
        <label>Spawn Queue</label>
        <div class="table-wrap"><table><thead><tr><th>Item</th><th>Position</th><th>Target</th><th>Status</th><th>Created</th><th>Actions</th></tr></thead><tbody id="spawn-queue-tbody"></tbody></table></div>
      </div>
    </div>
    <!-- AUDIT -->
    <div class="tab-panel" id="tab-audit">
      <div class="panel-title">Audit <span>Log</span></div>
      <div class="search-row"><input type="text" id="audit-search" placeholder="Filter actions..." oninput="filterAudit()"><button class="btn btn-cyan" onclick="loadAudit()">↺ REFRESH</button><button class="btn btn-danger" onclick="clearAudit()">CLEAR LOG</button></div>
      <div class="table-wrap"><table><thead><tr><th>Time</th><th>Action</th><th>Target</th><th>Detail</th></tr></thead><tbody id="audit-tbody"></tbody></table></div>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
let PW='', PLAYERS=[], BANS=[], AUDIT_ROWS=[], ALL_NODES=[], SPAWN_QUEUE=[];
let selCosm=null,selStash=null,selWallet=null,selResearch=null,selPrefs=null,selLoadoutUser=null;
let _loadoutItems=[], _stashItems=[], _ulItems=[];
const LOADOUT_PRESETS=['item_jetpack','item_flaregun','item_dynamite','item_tablet','item_flashlight_mega','item_plunger','item_crossbow','item_revolver','item_shotgun','item_pickaxe','item_hookshot','item_rpg','item_shield','item_zipline_gun','item_glowstick','item_tele_grenade','item_pogostick','item_hoverpad'];
async function doLogin(){const pw=document.getElementById('pw-input').value;const r=await fetch('/admin/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pw})});const d=await r.json();if(d.ok){PW=pw;document.getElementById('login-screen').style.display='none';document.getElementById('shell').style.display='block';loadDashboard();}else document.getElementById('login-err').textContent='✖ Wrong password';}
document.getElementById('pw-input').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin();});
function switchTab(name,btn){document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.getElementById('tab-'+name).classList.add('active');btn.classList.add('active');const sidebarTabs=['cosmetics','stash','wallet','research','prefs'];if(sidebarTabs.includes(name))renderSidebars();if(name==='loadout')loadLoadout();if(name==='bans')loadBans();if(name==='audit')loadAudit();if(name==='tokens')loadNamedTokens();if(name==='dashboard')loadDashboard();if(name==='spawn')loadSpawnQueue();if(name==='players')loadPlayers();if(name==='roles'){loadPlayers();renderRoles();}}
function switchTabByName(name){const btn=Array.from(document.querySelectorAll('.tab-btn')).find(b=>b.getAttribute('onclick')&&b.getAttribute('onclick').includes("'"+name+"'"));if(btn)btn.click();}
function toast(msg,err=false){const t=document.getElementById('toast');t.textContent=msg;t.className='toast show'+(err?' err':'');clearTimeout(t._tid);t._tid=setTimeout(()=>t.classList.remove('show'),3000);}
async function api(path,method='GET',body=null){const opts={method,headers:{'X-Admin-Password':PW}};if(body){opts.headers['Content-Type']='application/json';opts.body=JSON.stringify(body);}const r=await fetch(path,opts);if(!r.ok&&r.status!==200){const txt=await r.text();throw new Error(txt);}return r.json();}
async function loadDashboard(){try{const [players,bans]=await Promise.all([api('/admin/api/players'),api('/admin/api/bans')]);PLAYERS=players;BANS=bans;const banned=players.filter(p=>p.banned).length;const admins=players.filter(p=>p.role==='admin').length;const mods=players.filter(p=>p.role==='moderator').length;document.getElementById('stat-grid').innerHTML=[{v:players.length,k:'Total Players'},{v:banned,k:'Banned'},{v:players.length-banned,k:'Active'},{v:admins,k:'Admins'},{v:mods,k:'Moderators'},{v:bans.length,k:'Ban Entries'},].map(s=>`<div class="stat-card"><div class="sv">${s.v}</div><div class="sk">${s.k}</div></div>`).join('');document.getElementById('recent-tbody').innerHTML=players.slice(0,10).map(p=>playerRow(p,true)).join('');}catch(e){toast('Dashboard load error',true);}}
async function loadPlayers(){PLAYERS=await api('/admin/api/players');renderPlayers(PLAYERS);renderRoles();renderSidebars();return PLAYERS;}
function filterPlayers(){const q=document.getElementById('player-search').value.toLowerCase();renderPlayers(PLAYERS.filter(p=>p.username.toLowerCase().includes(q)||p.ip.includes(q)||p.custom_id.includes(q)||(p.override_username||'').toLowerCase().includes(q)));}
function playerRow(p,compact=false){const roleColor={'admin':'badge-purple','moderator':'badge-warn','vip':'badge-cyan','player':'badge-ok'}[p.role||'player']||'badge-ok';const actionBtns=compact?`<button class="btn btn-primary btn-xs" onclick="goEditCosm('${p.custom_id}','${esc(p.override_username||p.username)}')">COSM</button><button class="btn ${p.banned?'btn-ok':'btn-danger'} btn-xs" onclick="${p.banned?`unbanQuick('${p.ip}','${p.custom_id}')`:`quickBan('${p.ip}','${p.custom_id}')`}">${p.banned?'UNBAN':'BAN'}</button>`:`<button class="btn btn-warn btn-xs" onclick="editRole('${p.custom_id}','${esc(p.override_username||'')}','${p.role||'player'}')">ROLE</button><button class="btn btn-cyan btn-xs" onclick="quickToken('${p.custom_id}')">TOKEN</button><button class="btn btn-primary btn-xs" onclick="goEditCosm('${p.custom_id}','${esc(p.override_username||p.username)}')">COSM</button><button class="btn btn-warn btn-xs" onclick="goEditStash('${p.custom_id}','${esc(p.override_username||p.username)}')">STASH</button><button class="btn btn-ghost btn-xs" onclick="goEditWallet('${p.custom_id}','${esc(p.override_username||p.username)}')">WALLET</button><button class="btn btn-ghost btn-xs" onclick="goEditResearch('${p.custom_id}','${esc(p.override_username||p.username)}')">RES</button><button class="btn btn-ghost btn-xs" onclick="goEditPrefs('${p.custom_id}','${esc(p.override_username||p.username)}')">PREFS</button><button class="btn ${p.banned?'btn-ok':'btn-danger'} btn-xs" onclick="${p.banned?`unbanQuick('${p.ip}','${p.custom_id}')`:`quickBan('${p.ip}','${p.custom_id}')`}">${p.banned?'UNBAN':'BAN'}</button>`;return `<tr><td>${esc(p.username)}</td><td style="color:var(--accent2);">${esc(p.override_username||'—')}</td><td style="color:var(--muted);font-size:11px;">${p.custom_id}</td><td style="color:var(--accent2);">${p.ip}</td><td><span class="badge ${roleColor}">${p.role||'player'}</span></td>${!compact?`<td style="color:var(--muted);font-size:11px;">${new Date(p.create_time*1000).toLocaleString()}</td>`:''}<td><span class="badge ${p.banned?'badge-danger':'badge-ok'}">${p.banned?'BANNED':'ACTIVE'}</span></td><td><div style="display:flex;gap:4px;flex-wrap:wrap;">${actionBtns}</div></td></tr>`;}
function renderPlayers(list){document.getElementById('players-tbody').innerHTML=list.length?list.map(p=>playerRow(p)).join(''):'<tr><td colspan="8" style="color:var(--muted);text-align:center;padding:24px;">No players found</td></tr>';}
function renderRoles(list){const l=list||PLAYERS;document.getElementById('roles-tbody').innerHTML=l.length?l.map(p=>{const roleColor={'admin':'badge-purple','moderator':'badge-warn','vip':'badge-cyan','player':'badge-ok'}[p.role||'player']||'badge-ok';return `<tr><td>${esc(p.username)}</td><td style="color:var(--accent2);">${esc(p.override_username||'—')}</td><td style="font-size:11px;color:var(--muted);">${p.custom_id}</td><td><span class="badge ${roleColor}">${p.role||'player'}</span></td><td><button class="btn btn-primary btn-xs" onclick="editRole('${p.custom_id}','${esc(p.override_username||'')}','${p.role||'player'}')">EDIT</button></td></tr>`;}).join(''):'<tr><td colspan="5" style="color:var(--muted);text-align:center;padding:24px;">No players</td></tr>';}
function filterRoles(){const q=document.getElementById('role-search').value.toLowerCase();renderRoles(PLAYERS.filter(p=>p.username.toLowerCase().includes(q)||p.custom_id.includes(q)||(p.override_username||'').toLowerCase().includes(q)||(p.role||'').includes(q)));}
function editRole(cid,username,role){switchTabByName('roles');document.getElementById('role-cid').value=cid;document.getElementById('role-username').value=username;document.getElementById('role-select').value=role;}
function clearRoleForm(){document.getElementById('role-cid').value='';document.getElementById('role-username').value='';document.getElementById('role-select').value='player';}
async function updateRole(){const cid=document.getElementById('role-cid').value.trim();const username=document.getElementById('role-username').value.trim();const role=document.getElementById('role-select').value;if(!cid){toast('Enter a custom ID',true);return;}const res=await api('/admin/api/role','POST',{custom_id:cid,username,role});if(res.ok){toast('Role updated!');clearRoleForm();await loadPlayers();}else toast('Failed',true);}
async function loadBans(){BANS=await api('/admin/api/bans');renderBans(BANS);}
function filterBans(){const q=document.getElementById('ban-search').value.toLowerCase();renderBans(BANS.filter(b=>(b.ip||'').includes(q)||(b.custom_id||'').includes(q)||(b.reason||'').toLowerCase().includes(q)));}
function renderBans(list){document.getElementById('bans-tbody').innerHTML=list.length?list.map(b=>`<tr><td style="color:var(--accent2);">${b.ip||'—'}</td><td style="color:var(--muted);font-size:11px;">${b.custom_id||'—'}</td><td>${esc(b.reason||'')}</td><td style="color:var(--muted);font-size:11px;">${new Date(b.banned_at*1000).toLocaleString()}</td><td><button class="btn btn-ok btn-sm" onclick="removeBan(${b.id})">UNBAN</button></td></tr>`).join(''):'<tr><td colspan="5" style="color:var(--muted);text-align:center;padding:24px;">No bans</td></tr>';}
async function addBan(){const ip=document.getElementById('ban-ip').value.trim()||null;const cid=document.getElementById('ban-cid').value.trim()||null;const reason=document.getElementById('ban-reason').value.trim()||'Admin ban';if(!ip&&!cid){toast('Enter IP or Custom ID',true);return;}const res=await api('/admin/api/bans','POST',{ip,custom_id:cid,reason});if(res.ok){toast('Banned!');document.getElementById('ban-ip').value='';document.getElementById('ban-cid').value='';document.getElementById('ban-reason').value='';loadBans();loadPlayers();}else toast('Failed',true);}
async function quickBan(ip,cid){const res=await api('/admin/api/bans','POST',{ip,custom_id:cid,reason:'Admin ban'});if(res.ok){toast(`Banned`);loadPlayers();loadBans();}else toast('Failed',true);}
async function unbanQuick(ip,cid){const ban=BANS.find(b=>b.ip===ip||b.custom_id===cid);if(ban)await removeBan(ban.id);else{toast('Ban not found',true);}}
async function removeBan(id){const res=await api(`/admin/api/bans/${id}`,'DELETE');if(res.ok){toast('Unbanned!');loadBans();loadPlayers();}else toast('Failed',true);}
function tokenTab(name,btn){document.querySelectorAll('.itab').forEach(b=>b.classList.remove('on'));btn.classList.add('on');document.getElementById('token-generate-panel').style.display=name==='generate'?'':'none';document.getElementById('token-saved-panel').style.display=name==='saved'?'':'none';if(name==='saved')loadNamedTokens();}
async function quickToken(cid){const res=await api('/admin/api/token','POST',{user_id:cid});showToken(res);switchTabByName('tokens');}
async function genToken(){const uid=document.getElementById('token-uid').value.trim()||undefined;showToken(await api('/admin/api/token','POST',uid?{user_id:uid}:{}));}
async function genTokenOwner(){showToken(await api('/admin/api/token','POST',{user_id:'__OWNER_ID__'}));}
async function genAndSaveToken(){const uid=document.getElementById('token-uid').value.trim()||undefined;const label=document.getElementById('token-label').value.trim()||('token_'+Date.now());const res=await api('/admin/api/token','POST',uid?{user_id:uid,label,save:true}:{label,save:true});showToken(res);if(res.token)toast('Token saved!');}
function showToken(data){const el=document.getElementById('token-output');el.style.display='block';el.innerHTML=`<b style="color:var(--muted);font-size:10px;">USER ID</b>\n${data.user_id||'—'}\n\n<b style="color:var(--muted);font-size:10px;">TOKEN</b>\n${data.token}\n\n<b style="color:var(--muted);font-size:10px;">REFRESH TOKEN</b>\n${data.refresh_token}`;el.onclick=()=>{navigator.clipboard.writeText(JSON.stringify(data,null,2));toast('Copied!');};document.getElementById('copy-hint').textContent='↑ Click to copy as JSON';}
async function loadNamedTokens(){const list=await api('/admin/api/tokens');document.getElementById('named-tokens-list').innerHTML=list.length?list.map(t=>`<div class="named-token-row"><div class="nt-label">${esc(t.label)}</div><div class="nt-cid">${t.custom_id}</div><div class="nt-token" onclick="copyNT('${esc(t.token)}','${esc(t.refresh_token)}')" title="Click to copy">${t.token.substring(0,40)}...</div><div style="font-size:10px;color:var(--muted);">${new Date(t.created_at*1000).toLocaleString()}</div><button class="btn btn-danger btn-xs" onclick="deleteNamedToken(${t.id})">DEL</button></div>`).join(''):'<div style="color:var(--muted);font-size:12px;padding:8px 0;">No saved tokens yet.</div>';}
function copyNT(token,refresh){navigator.clipboard.writeText(JSON.stringify({token,refresh_token:refresh},null,2));toast('Copied!');}
async function deleteNamedToken(id){const res=await api(`/admin/api/tokens/${id}`,'DELETE');if(res.ok){toast('Deleted!');loadNamedTokens();}else toast('Failed',true);}
function makePlayerEntry(p,selId,fn){const sel=selId===p.custom_id;return `<div class="player-entry ${sel?'selected':''}" onclick="${fn}('${p.custom_id}','${esc(p.override_username||p.username)}')"><div class="pname">${esc(p.override_username||p.username)}</div><div class="pid">${p.custom_id}</div><div class="prole">${p.role||'player'} · ${p.ip}</div></div>`;}
function renderSidebars(){const map={cosm:[selCosm,'selectCosm'],stash:[selStash,'selectStash'],wallet:[selWallet,'selectWallet'],research:[selResearch,'selectResearch'],prefs:[selPrefs,'selectPrefs'],loadout:[selLoadoutUser,'selectLoadoutUser']};for(const [prefix,[sel,fn]] of Object.entries(map)){const el=document.getElementById(prefix+'-player-list');if(el)el.innerHTML=PLAYERS.map(p=>makePlayerEntry(p,sel,fn)).join('');}}
function filterSidebar(prefix,q){document.querySelectorAll(`#${prefix}-player-list .player-entry`).forEach(el=>el.style.display=el.textContent.toLowerCase().includes(q.toLowerCase())?'':'none');}
async function selectCosm(cid,name){selCosm=cid;renderSidebars();const data=await api(`/admin/api/cosmetics/${cid}`);renderCosmEditor(cid,name,data);}
function renderCosmEditor(cid,name,data){const av=data.avatar||{};const inv=data.inventory||{items:[]};window._accList=[...(av.accessories||[])];document.getElementById('cosm-editor').innerHTML=`<h3>Editing: ${esc(name)}</h3><div class="field-grid">${['head','torso','armLeft','armRight','eyeLeft','eyeRight','butt','tail'].map(k=>`<div class="field-group"><label>${k}</label><input type="text" id="av_${k}" value="${esc(av[k]||'')}" placeholder="bp_..."></div>`).join('')}<div class="field-group"><label>Primary Color</label><input type="text" id="av_primaryColor" value="${esc(av.primaryColor||'604170')}"></div></div><div class="field-group" style="margin-bottom:16px;"><label>Accessories</label><div class="acc-items-list" id="acc-list">${window._accList.map((a,i)=>`<div class="acc-tag">${esc(a)}<button onclick="removeAcc(${i})">×</button></div>`).join('')}</div><div style="display:flex;gap:8px;margin-top:8px;"><input type="text" id="new-acc" placeholder="acc_head_mop" style="flex:1;padding:8px;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);outline:none;"><button class="btn btn-ghost btn-sm" onclick="addAcc()">+ ADD</button></div></div><hr class="section-sep" style="border:none;border-top:1px solid var(--border);margin:18px 0;"><div class="field-group"><label>Inventory Items JSON</label><textarea class="json-edit" id="inv-edit">${esc(JSON.stringify(inv.items||[],null,2))}</textarea></div><div class="row-btns"><button class="btn btn-primary" onclick="saveCosm('${cid}')">SAVE</button><button class="btn btn-ghost" onclick="selectCosm('${cid}','${esc(name)}')">↺ RELOAD</button></div>`;}
function removeAcc(i){window._accList.splice(i,1);refreshAccDisplay();}
function addAcc(){const v=document.getElementById('new-acc').value.trim();if(!v)return;window._accList.push(v);document.getElementById('new-acc').value='';refreshAccDisplay();}
function refreshAccDisplay(){document.getElementById('acc-list').innerHTML=window._accList.map((a,i)=>`<div class="acc-tag">${esc(a)}<button onclick="removeAcc(${i})">×</button></div>`).join('');}
async function saveCosm(cid){const av={};for(const k of['head','torso','armLeft','armRight','eyeLeft','eyeRight','butt','tail','primaryColor'])av[k]=document.getElementById('av_'+k).value;av.accessories=window._accList;let items;try{items=JSON.parse(document.getElementById('inv-edit').value);}catch(e){toast('Invalid JSON',true);return;}const res=await api(`/admin/api/cosmetics/${cid}`,'POST',{avatar:av,inventory:{items}});if(res.ok)toast('Cosmetics saved!');else toast('Save failed',true);}
async function selectStash(cid,name){selStash=cid;renderSidebars();const data=await api(`/admin/api/stash/${cid}`);renderStashEditor(cid,name,data.stash);}
function renderStashEditor(cid,name,stash){const items=(stash&&stash.items)||[];window._stashItems=JSON.parse(JSON.stringify(items));document.getElementById('stash-editor').innerHTML=`<h3>Stash: ${esc(name)}</h3><button class="btn btn-cyan btn-sm" onclick="addStashItem()" style="margin-bottom:12px;">+ ADD ITEM</button><div id="stash-items-list">${items.map(renderStashRow).join('')}</div><hr style="border:none;border-top:1px solid var(--border);margin:18px 0;"><div class="field-group"><label>Raw Stash JSON</label><textarea class="json-edit" id="stash-raw" style="min-height:240px;">${esc(JSON.stringify(stash,null,2))}</textarea></div><div class="row-btns"><button class="btn btn-primary" onclick="saveStashRaw('${cid}')">SAVE RAW JSON</button><button class="btn btn-warn" onclick="saveStashItems('${cid}')">SAVE ITEM LIST</button><button class="btn btn-ghost" onclick="selectStash('${cid}','${esc(name)}')">↺ RELOAD</button></div>`;}
function renderStashRow(item,i){return `<div class="stash-item-row" id="stash-row-${i}"><input type="text" value="${esc(item.itemID||'')}" placeholder="item_jetpack" onchange="_stashItems[${i}].itemID=this.value"><input type="number" class="stash-num" value="${item.colorHue||0}" placeholder="Hue" onchange="_stashItems[${i}].colorHue=+this.value"><input type="number" class="stash-num" value="${item.colorSaturation||0}" placeholder="Sat" onchange="_stashItems[${i}].colorSaturation=+this.value"><input type="number" class="stash-num" value="${item.scaleModifier||0}" placeholder="Scale" onchange="_stashItems[${i}].scaleModifier=+this.value"><button class="btn btn-danger btn-xs" onclick="_stashItems.splice(${i},1);document.getElementById('stash-items-list').innerHTML=_stashItems.map(renderStashRow).join('')">✕</button></div>`;}
function addStashItem(){window._stashItems.push({itemID:'',colorHue:0,colorSaturation:0,scaleModifier:0,children:[]});document.getElementById('stash-items-list').innerHTML=window._stashItems.map(renderStashRow).join('');}
async function saveStashItems(cid){const res=await api(`/admin/api/stash/${cid}`,'POST',{stash:{items:window._stashItems,version:1}});if(res.ok)toast('Stash saved!');else toast('Save failed',true);}
async function saveStashRaw(cid){let stash;try{stash=JSON.parse(document.getElementById('stash-raw').value);}catch(e){toast('Invalid JSON',true);return;}const res=await api(`/admin/api/stash/${cid}`,'POST',{stash});if(res.ok)toast('Stash saved!');else toast('Save failed',true);}
async function selectWallet(cid,name){selWallet=cid;renderSidebars();const data=await api(`/admin/api/wallet/${cid}`);renderWalletEditor(cid,name,data);}
function renderWalletEditor(cid,name,data){const w=data.wallet||{};document.getElementById('wallet-editor').innerHTML=`<h3>Wallet: ${esc(name)}</h3><p style="color:var(--muted);font-size:11px;margin-bottom:16px;">Leave blank / 0 to use server defaults.</p><div class="field-grid"><div class="field-group"><label>Hard Currency</label><input type="text" id="w_hard" value="${esc(String(w.hardCurrency||0))}"></div><div class="field-group"><label>Soft Currency</label><input type="text" id="w_soft" value="${esc(String(w.softCurrency||0))}"></div><div class="field-group"><label>Research Points</label><input type="text" id="w_research" value="${esc(String(w.researchPoints||0))}"></div><div class="field-group"><label>Stash Cols</label><input type="number" id="w_cols" value="${w.stashCols||16}"></div><div class="field-group"><label>Stash Rows</label><input type="number" id="w_rows" value="${w.stashRows||8}"></div></div><div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;"><button class="btn btn-ghost btn-sm" onclick="wPreset(0,0,0)">ZERO</button><button class="btn btn-ghost btn-sm" onclick="wPreset(1000,100000,50000)">STARTER</button><button class="btn btn-warn btn-sm" onclick="wPreset(30000000,'20000000000000000000','20000000000000000000')">MAXED</button></div><div class="row-btns"><button class="btn btn-primary" onclick="saveWallet('${cid}')">SAVE WALLET</button><button class="btn btn-danger btn-sm" onclick="resetWallet('${cid}')">RESET TO DEFAULT</button><button class="btn btn-ghost" onclick="selectWallet('${cid}','${esc(name)}')">↺ RELOAD</button></div>`;}
function wPreset(hard,soft,research){document.getElementById('w_hard').value=hard;document.getElementById('w_soft').value=soft;document.getElementById('w_research').value=research;}
async function saveWallet(cid){const res=await api(`/admin/api/wallet/${cid}`,'POST',{hard_currency:parseInt(document.getElementById('w_hard').value)||0,soft_currency:document.getElementById('w_soft').value||'0',research_points:document.getElementById('w_research').value||'0',stash_cols:parseInt(document.getElementById('w_cols').value)||16,stash_rows:parseInt(document.getElementById('w_rows').value)||8,});if(res.ok)toast('Wallet saved!');else toast('Save failed',true);}
async function resetWallet(cid){const res=await api(`/admin/api/wallet/${cid}`,'DELETE');if(res.ok){toast('Wallet reset!');selectWallet(cid,'');}else toast('Failed',true);}
async function selectResearch(cid,name){selResearch=cid;renderSidebars();const data=await api(`/admin/api/research/${cid}`);renderResearchEditor(cid,name,data.research||{nodes:[]});}
async function renderResearchEditor(cid,name,nodes){if(!ALL_NODES.length){const d=await api('/admin/api/all_nodes');ALL_NODES=d.nodes||[];}const checked=new Set(nodes.nodes||[]);const grid=ALL_NODES.map((n,i)=>`<div class="rnode"><input type="checkbox" id="rn_${i}" ${checked.has(n)?'checked':''}><label for="rn_${i}">${n.replace('node_','')}</label></div>`).join('');document.getElementById('research-editor').innerHTML=`<h3>Research: ${esc(name)}</h3><div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;"><button class="btn btn-ok btn-sm" onclick="ALL_NODES.forEach((_,i)=>document.getElementById('rn_'+i).checked=true)">SELECT ALL</button><button class="btn btn-danger btn-sm" onclick="ALL_NODES.forEach((_,i)=>document.getElementById('rn_'+i).checked=false)">CLEAR ALL</button></div><div class="research-grid">${grid}</div><div class="row-btns"><button class="btn btn-primary" onclick="saveResearch('${cid}')">SAVE</button><button class="btn btn-ghost" onclick="selectResearch('${cid}','${esc(name)}')">↺ RELOAD</button></div>`;}
async function saveResearch(cid){const nodes=ALL_NODES.filter((_,i)=>document.getElementById('rn_'+i).checked);const res=await api(`/admin/api/research/${cid}`,'POST',{nodes});if(res.ok)toast('Research saved!');else toast('Save failed',true);}
async function selectPrefs(cid,name){selPrefs=cid;renderSidebars();const data=await api(`/admin/api/prefs/${cid}`);renderPrefsEditor(cid,name,data.prefs);}
function renderPrefsEditor(cid,name,prefs){const p=prefs||{recents:[],favorites:[]};document.getElementById('prefs-editor').innerHTML=`<h3>Preferences: ${esc(name)}</h3><div class="field-group" style="margin-bottom:14px;"><label>Recent Items (JSON array)</label><textarea class="json-edit" id="prefs-recents">${esc(JSON.stringify(p.recents||[],null,2))}</textarea></div><div class="field-group" style="margin-bottom:14px;"><label>Favorites (JSON array)</label><textarea class="json-edit" id="prefs-favorites" style="min-height:100px;">${esc(JSON.stringify(p.favorites||[],null,2))}</textarea></div><div class="field-group" style="margin-bottom:14px;"><label>Full Prefs JSON (overrides above)</label><textarea class="json-edit" id="prefs-raw" style="min-height:160px;">${esc(JSON.stringify(p,null,2))}</textarea></div><div class="row-btns"><button class="btn btn-primary" onclick="savePrefsRaw('${cid}')">SAVE RAW JSON</button><button class="btn btn-warn" onclick="savePrefsFields('${cid}')">SAVE FIELDS</button><button class="btn btn-ghost" onclick="selectPrefs('${cid}','${esc(name)}')">↺ RELOAD</button></div>`;}
async function savePrefsRaw(cid){let p;try{p=JSON.parse(document.getElementById('prefs-raw').value);}catch(e){toast('Invalid JSON',true);return;}const res=await api(`/admin/api/prefs/${cid}`,'POST',{prefs:p});if(res.ok)toast('Prefs saved!');else toast('Save failed',true);}
async function savePrefsFields(cid){let recents,favorites;try{recents=JSON.parse(document.getElementById('prefs-recents').value);}catch(e){toast('Invalid recents JSON',true);return;}try{favorites=JSON.parse(document.getElementById('prefs-favorites').value);}catch(e){toast('Invalid favorites JSON',true);return;}const res=await api(`/admin/api/prefs/${cid}`,'POST',{prefs:{recents,favorites}});if(res.ok)toast('Prefs saved!');else toast('Save failed',true);}
function loadoutTab(name,btn){document.querySelectorAll('.itab').forEach(b=>b.classList.remove('on'));btn.classList.add('on');document.getElementById('loadout-global-panel').style.display=name==='global'?'':'none';document.getElementById('loadout-peruser-panel').style.display=name==='peruser'?'':'none';if(name==='peruser')renderSidebars();}
async function loadLoadout(){const data=await api('/admin/api/loadout');_loadoutItems=data.items||[];document.getElementById('bp-item').value=data.backpack||'item_backpack_large_base';document.getElementById('bp-scale').value=data.scale||120;document.getElementById('bp-hue').value=data.hue||50;document.getElementById('bp-sat').value=data.sat||50;renderLoadoutItems();const qa=document.getElementById('loadout-quickadd');if(!qa.children.length){LOADOUT_PRESETS.forEach(p=>{const b=document.createElement('button');b.className='btn btn-ghost btn-sm';b.style.fontFamily='var(--mono)';b.style.fontSize='11px';b.textContent=p.replace('item_','');b.onclick=()=>{_loadoutItems.push({itemID:p,scaleModifier:100,colorHue:50,colorSaturation:50});renderLoadoutItems();};qa.appendChild(b);});}}
function renderLoadoutItems(){document.getElementById('loadout-item-list').innerHTML=_loadoutItems.length?_loadoutItems.map((it,i)=>`<div class="stash-item-row"><input type="text" value="${esc(it.itemID)}" placeholder="item_id" onchange="_loadoutItems[${i}].itemID=this.value"><input type="number" class="stash-num" value="${it.scaleModifier||100}" placeholder="Scale" onchange="_loadoutItems[${i}].scaleModifier=+this.value"><input type="number" class="stash-num" value="${it.colorHue||50}" placeholder="Hue" onchange="_loadoutItems[${i}].colorHue=+this.value"><input type="number" class="stash-num" value="${it.colorSaturation||50}" placeholder="Sat" onchange="_loadoutItems[${i}].colorSaturation=+this.value"><button class="btn btn-danger btn-xs" onclick="_loadoutItems.splice(${i},1);renderLoadoutItems()">✕</button></div>`).join(''):'<div style="color:var(--muted);font-size:12px;padding:8px 0;">No items.</div>';}
function addLoadoutItem(){const id=document.getElementById('new-loadout-item').value.trim();if(!id)return;_loadoutItems.push({itemID:id,scaleModifier:100,colorHue:50,colorSaturation:50});document.getElementById('new-loadout-item').value='';renderLoadoutItems();}
async function saveLoadout(){const res=await api('/admin/api/loadout','POST',{items:_loadoutItems,backpack:document.getElementById('bp-item').value.trim(),scale:+document.getElementById('bp-scale').value,hue:+document.getElementById('bp-hue').value,sat:+document.getElementById('bp-sat').value});if(res.ok)toast('Loadout saved!');else toast('Save failed',true);}
async function selectLoadoutUser(cid,name){selLoadoutUser=cid;renderSidebars();const data=await api(`/admin/api/user_loadout/${cid}`);renderUserLoadoutEditor(cid,name,data.loadout);}
function renderUserLoadoutEditor(cid,name,loadout){const l=loadout||{itemID:'item_backpack_large_base',scaleModifier:120,colorHue:50,colorSaturation:50,children:[]};window._ulItems=JSON.parse(JSON.stringify(l.children||[]));document.getElementById('loadout-editor').innerHTML=`<h3>Loadout: ${esc(name)}</h3><div class="field-grid"><div class="field-group"><label>Backpack item</label><input type="text" id="ul_item" value="${esc(l.itemID||'item_backpack_large_base')}"></div><div class="field-group"><label>Scale</label><input type="number" id="ul_scale" value="${l.scaleModifier||120}"></div><div class="field-group"><label>Hue</label><input type="number" id="ul_hue" value="${l.colorHue||50}"></div><div class="field-group"><label>Saturation</label><input type="number" id="ul_sat" value="${l.colorSaturation||50}"></div></div><label style="display:block;color:var(--muted);font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Spawn Items</label><div id="ul-item-list" style="margin-bottom:10px;">${window._ulItems.map(renderULRow).join('')}</div><div style="display:flex;gap:8px;margin-bottom:16px;"><input type="text" id="new-ul-item" placeholder="item_jetpack" style="flex:1;padding:8px;background:#0b0b0f;border:1px solid var(--border);color:var(--text);font-family:var(--mono);outline:none;"><button class="btn btn-cyan btn-sm" onclick="addULItem()">+ ADD</button></div><div class="row-btns"><button class="btn btn-primary" onclick="saveUserLoadout('${cid}')">SAVE</button><button class="btn btn-danger btn-sm" onclick="resetUserLoadout('${cid}')">RESET TO GLOBAL</button><button class="btn btn-ghost" onclick="selectLoadoutUser('${cid}','${esc(name)}')">↺ RELOAD</button></div>`;}
function renderULRow(item,i){return `<div class="stash-item-row"><input type="text" value="${esc(item.itemID||'')}" onchange="_ulItems[${i}].itemID=this.value"><input type="number" class="stash-num" value="${item.scaleModifier||100}" placeholder="Scale" onchange="_ulItems[${i}].scaleModifier=+this.value"><input type="number" class="stash-num" value="${item.colorHue||50}" placeholder="Hue" onchange="_ulItems[${i}].colorHue=+this.value"><input type="number" class="stash-num" value="${item.colorSaturation||50}" placeholder="Sat" onchange="_ulItems[${i}].colorSaturation=+this.value"><button class="btn btn-danger btn-xs" onclick="_ulItems.splice(${i},1);document.getElementById('ul-item-list').innerHTML=_ulItems.map(renderULRow).join('')">✕</button></div>`;}
function addULItem(){const id=document.getElementById('new-ul-item').value.trim();if(!id)return;window._ulItems.push({itemID:id,scaleModifier:100,colorHue:50,colorSaturation:50});document.getElementById('new-ul-item').value='';document.getElementById('ul-item-list').innerHTML=window._ulItems.map(renderULRow).join('');}
async function saveUserLoadout(cid){const loadout={itemID:document.getElementById('ul_item').value,scaleModifier:+document.getElementById('ul_scale').value,colorHue:+document.getElementById('ul_hue').value,colorSaturation:+document.getElementById('ul_sat').value,children:window._ulItems};const res=await api(`/admin/api/user_loadout/${cid}`,'POST',{loadout});if(res.ok)toast('User loadout saved!');else toast('Save failed',true);}
async function resetUserLoadout(cid){const res=await api(`/admin/api/user_loadout/${cid}`,'DELETE');if(res.ok){toast('Reset to global!');selectLoadoutUser(cid,'');}else toast('Failed',true);}
async function loadSpawnQueue(){SPAWN_QUEUE=await api('/admin/api/spawn/queue');renderSpawnQueue(SPAWN_QUEUE);}
function renderSpawnQueue(list){document.getElementById('spawn-queue-tbody').innerHTML=list.length?list.map(s=>`<tr><td style="color:var(--accent2);">${esc(s.item_id)}</td><td style="font-size:11px;">(${(+s.pos_x).toFixed(1)}, ${(+s.pos_y).toFixed(1)}, ${(+s.pos_z).toFixed(1)})</td><td style="font-size:11px;color:var(--muted);">${s.custom_id||'Global'}</td><td><span class="badge ${s.spawned?'badge-ok':'badge-warn'}">${s.spawned?'SPAWNED':'PENDING'}</span></td><td style="font-size:11px;color:var(--muted);">${new Date(s.created_at*1000).toLocaleString()}</td><td><button class="btn btn-danger btn-xs" onclick="deleteSpawn(${s.id})">DEL</button></td></tr>`).join(''):'<tr><td colspan="6" style="color:var(--muted);text-align:center;padding:24px;">No items in queue</td></tr>';}
async function spawnItem(){const itemID=document.getElementById('spawn-item-id').value.trim();if(!itemID){toast('Enter an item ID',true);return;}const res=await api('/admin/api/spawn','POST',{item_id:itemID,custom_id:document.getElementById('spawn-custom-id').value.trim()||null,pos_x:parseFloat(document.getElementById('spawn-x').value)||0,pos_y:parseFloat(document.getElementById('spawn-y').value)||0,pos_z:parseFloat(document.getElementById('spawn-z').value)||0,scale:parseFloat(document.getElementById('spawn-scale').value)||1.0,color_hue:parseInt(document.getElementById('spawn-hue').value)||0,color_sat:parseInt(document.getElementById('spawn-sat').value)||0,expires_in:parseInt(document.getElementById('spawn-expires').value)||0,});if(res.ok){toast(`Spawned ${itemID}!`);loadSpawnQueue();}else toast('Spawn failed',true);}
function spawnPreset(itemID){document.getElementById('spawn-item-id').value=itemID;spawnItem();}
async function deleteSpawn(id){const res=await api(`/admin/api/spawn/${id}`,'DELETE');if(res.ok){toast('Deleted!');loadSpawnQueue();}else toast('Failed',true);}
async function loadAudit(){AUDIT_ROWS=await api('/admin/api/audit');renderAudit(AUDIT_ROWS);}
function filterAudit(){const q=document.getElementById('audit-search').value.toLowerCase();renderAudit(AUDIT_ROWS.filter(r=>(r.admin_action||'').toLowerCase().includes(q)||(r.target||'').toLowerCase().includes(q)||(r.detail||'').toLowerCase().includes(q)));}
function renderAudit(list){document.getElementById('audit-tbody').innerHTML=list.length?list.map(r=>`<tr class="audit-row"><td style="color:var(--muted);">${new Date(r.performed_at*1000).toLocaleString()}</td><td style="color:var(--accent2);">${esc(r.admin_action)}</td><td>${esc(r.target||'—')}</td><td style="color:var(--muted);">${esc(r.detail||'')}</td></tr>`).join(''):'<tr><td colspan="4" style="color:var(--muted);text-align:center;padding:24px;">No audit entries</td></tr>';}
async function clearAudit(){if(!confirm('Clear entire audit log?'))return;const res=await api('/admin/api/audit','DELETE');if(res.ok){toast('Log cleared!');loadAudit();}else toast('Failed',true);}
function goEditCosm(cid,name){switchTabByName('cosmetics');setTimeout(()=>selectCosm(cid,name),120);}
function goEditStash(cid,name){switchTabByName('stash');setTimeout(()=>selectStash(cid,name),120);}
function goEditWallet(cid,name){switchTabByName('wallet');setTimeout(()=>selectWallet(cid,name),120);}
function goEditResearch(cid,name){switchTabByName('research');setTimeout(()=>selectResearch(cid,name),120);}
function goEditPrefs(cid,name){switchTabByName('prefs');setTimeout(()=>selectPrefs(cid,name),120);}
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;');}
</script>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════════════════════════
#  ADMIN ROUTES  (unchanged from doc1)
# ═══════════════════════════════════════════════════════════════════════════════
def check_auth():
    pw = request.headers.get('X-Admin-Password') or request.args.get('pw', '')
    return pw == ADMIN_PASSWORD

@app.route('/admin')
def admin_index():
    return render_template_string(ADMIN_HTML.replace('__OWNER_ID__', OWNER_USER_ID))

@app.route('/admin/api/auth', methods=['POST'])
def admin_auth():
    data = request.get_json(force=True) or {}
    if data.get('password') == ADMIN_PASSWORD:
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'Bad password'}), 403

@app.route('/admin/api/players')
def admin_players():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_conn()
    rows = conn.execute('SELECT ip, username, custom_id, create_time FROM users ORDER BY create_time DESC').fetchall()
    conn.close()
    result = []
    for r in rows:
        banned, ban_reason = is_banned(ip=r['ip'], custom_id=r['custom_id'])
        override = get_user_override(r['custom_id'])
        result.append({
            'ip': r['ip'], 'username': r['username'], 'custom_id': r['custom_id'],
            'create_time': r['create_time'], 'banned': banned, 'ban_reason': ban_reason or '',
            'role': (override or {}).get('role', 'player'),
            'override_username': (override or {}).get('username', ''),
            'notes': (override or {}).get('notes', ''),
        })
    return jsonify(result)

@app.route('/admin/api/role', methods=['POST'])
def admin_role_update():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    custom_id = data.get('custom_id', '').strip()
    username  = data.get('username', '').strip()
    role      = data.get('role', 'player')
    if not custom_id: return jsonify({'error': 'custom_id required'}), 400
    save_user_override(custom_id, username=username or None, role=role)
    audit('role_update', target=custom_id, detail=f'role={role} username={username}')
    return jsonify({'ok': True})

@app.route('/admin/api/bans', methods=['GET'])
def admin_bans_get():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(get_all_bans())

@app.route('/admin/api/bans', methods=['POST'])
def admin_bans_add():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    ip = data.get('ip') or None; custom_id = data.get('custom_id') or None
    reason = data.get('reason', '').strip() or 'Banned by admin'
    if not ip and not custom_id: return jsonify({'error': 'Provide ip or custom_id'}), 400
    add_ban(ip=ip, custom_id=custom_id, reason=reason)
    audit('ban', target=ip or custom_id, detail=reason)
    return jsonify({'ok': True})

@app.route('/admin/api/bans/<int:ban_id>', methods=['DELETE'])
def admin_bans_remove(ban_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_conn(); conn.execute('DELETE FROM banned_entries WHERE id=?', (ban_id,)); conn.commit(); conn.close()
    audit('unban', target=str(ban_id))
    return jsonify({'ok': True})

@app.route('/admin/api/ban/<path:ip>', methods=['POST'])
def admin_ban_legacy(ip):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    add_ban(ip=ip, reason='Admin ban'); return jsonify({'ok': True})

@app.route('/admin/api/unban/<path:ip>', methods=['POST'])
def admin_unban_legacy(ip):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    remove_ban(ip=ip); return jsonify({'ok': True})

@app.route('/admin/api/ban/custom/<custom_id>', methods=['POST'])
def admin_ban_custom_legacy(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    add_ban(custom_id=custom_id, reason='Admin ban'); return jsonify({'ok': True})

@app.route('/admin/api/unban/custom/<custom_id>', methods=['POST'])
def admin_unban_custom_legacy(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    remove_ban(custom_id=custom_id); return jsonify({'ok': True})

@app.route('/admin/api/token', methods=['POST'])
def admin_token():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    user_id = data.get('user_id') or secrets.token_hex(16)
    label = data.get('label', ''); do_save = data.get('save', False)
    pair = make_token_pair(user_id); pair['user_id'] = user_id
    if do_save and label:
        save_named_token(label, user_id, pair['token'], pair['refresh_token'])
        audit('token_saved', target=user_id, detail=label)
    return jsonify(pair)

@app.route('/admin/api/tokens', methods=['GET'])
def admin_tokens_list():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(get_named_tokens())

@app.route('/admin/api/tokens/<int:token_id>', methods=['DELETE'])
def admin_tokens_delete(token_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    delete_named_token(token_id); audit('token_deleted', target=str(token_id))
    return jsonify({'ok': True})

@app.route('/admin/api/cosmetics/<custom_id>', methods=['GET'])
def admin_cosmetics_get(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    avatar, inventory = get_user_cosmetics(custom_id)
    if not avatar:
        avatar = {'butt':'bp_butt_gorilla','head':'bp_head_gorilla','tail':'','torso':'bp_torso_gorilla',
                  'armLeft':'bp_arm_l_gorilla','eyeLeft':'bp_eye_gorilla','armRight':'bp_arm_r_gorilla',
                  'eyeRight':'bp_eye_gorilla','accessories':[],'primaryColor':'604170'}
    if not inventory: inventory = {'items': []}
    return jsonify({'custom_id': custom_id, 'avatar': avatar, 'inventory': inventory})

@app.route('/admin/api/cosmetics/<custom_id>', methods=['POST'])
def admin_cosmetics_set(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    save_user_cosmetics(custom_id, data.get('avatar', {}), data.get('inventory', {'items': []}))
    audit('cosmetics_set', target=custom_id); return jsonify({'ok': True})

@app.route('/admin/api/stash/<custom_id>', methods=['GET'])
def admin_stash_get(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'custom_id': custom_id, 'stash': get_user_stash(custom_id) or {'items': [], 'version': 1}})

@app.route('/admin/api/stash/<custom_id>', methods=['POST'])
def admin_stash_set(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    save_user_stash(custom_id, data.get('stash', {'items': [], 'version': 1}))
    audit('stash_set', target=custom_id); return jsonify({'ok': True})

@app.route('/admin/api/wallet/<custom_id>', methods=['GET'])
def admin_wallet_get(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'custom_id': custom_id, 'wallet': get_user_wallet(custom_id) or {}})

@app.route('/admin/api/wallet/<custom_id>', methods=['POST'])
def admin_wallet_set(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    save_user_wallet(custom_id, data.get('hard_currency', 0), data.get('soft_currency', '0'),
                     data.get('research_points', '0'), data.get('stash_cols', 16), data.get('stash_rows', 8))
    audit('wallet_set', target=custom_id, detail=f"hard={data.get('hard_currency')} soft={data.get('soft_currency')}")
    return jsonify({'ok': True})

@app.route('/admin/api/wallet/<custom_id>', methods=['DELETE'])
def admin_wallet_reset(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_conn(); conn.execute('DELETE FROM user_wallet WHERE custom_id=?', (custom_id,)); conn.commit(); conn.close()
    audit('wallet_reset', target=custom_id); return jsonify({'ok': True})

@app.route('/admin/api/research/<custom_id>', methods=['GET'])
def admin_research_get(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'custom_id': custom_id, 'research': get_user_research(custom_id) or {'nodes': []}})

@app.route('/admin/api/research/<custom_id>', methods=['POST'])
def admin_research_set(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}; nodes = data.get('nodes', [])
    save_user_research(custom_id, {'nodes': nodes})
    audit('research_set', target=custom_id, detail=f'{len(nodes)} nodes'); return jsonify({'ok': True})

@app.route('/admin/api/all_nodes', methods=['GET'])
def admin_all_nodes():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'nodes': ALL_RESEARCH_NODES})

@app.route('/admin/api/prefs/<custom_id>', methods=['GET'])
def admin_prefs_get(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'custom_id': custom_id, 'prefs': get_user_prefs(custom_id) or {'recents': [], 'favorites': []}})

@app.route('/admin/api/prefs/<custom_id>', methods=['POST'])
def admin_prefs_set(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    save_user_prefs(custom_id, data.get('prefs', {}))
    audit('prefs_set', target=custom_id); return jsonify({'ok': True})

@app.route('/admin/api/user_loadout/<custom_id>', methods=['GET'])
def admin_user_loadout_get(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'custom_id': custom_id, 'loadout': get_user_loadout(custom_id)})

@app.route('/admin/api/user_loadout/<custom_id>', methods=['POST'])
def admin_user_loadout_set(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    save_user_loadout(custom_id, data.get('loadout', {}))
    audit('user_loadout_set', target=custom_id); return jsonify({'ok': True})

@app.route('/admin/api/user_loadout/<custom_id>', methods=['DELETE'])
def admin_user_loadout_reset(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_conn(); conn.execute('DELETE FROM user_loadout WHERE custom_id=?', (custom_id,)); conn.commit(); conn.close()
    audit('user_loadout_reset', target=custom_id); return jsonify({'ok': True})

@app.route('/admin/api/override/<custom_id>', methods=['GET'])
def admin_override_get(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(get_user_override(custom_id) or {})

@app.route('/admin/api/override/<custom_id>', methods=['POST'])
def admin_override_set(custom_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    save_user_override(custom_id, username=data.get('username'), metadata=data.get('metadata'),
                       notes=data.get('notes'), role=data.get('role'))
    audit('override_set', target=custom_id, detail=str(data)); return jsonify({'ok': True})

@app.route('/admin/api/loadout', methods=['GET'])
def admin_loadout_get():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    raw = get_config('spawn_loadout_items', '[]')
    try: items = json.loads(raw)
    except Exception: items = []
    return jsonify({'items': items, 'backpack': get_config('backpack_item', 'item_backpack_large_base'),
                    'scale': get_config('backpack_scale', '120'), 'hue': get_config('backpack_hue', '50'),
                    'sat': get_config('backpack_sat', '50')})

@app.route('/admin/api/loadout', methods=['POST'])
def admin_loadout_set():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    set_config('spawn_loadout_items', json.dumps(data.get('items', [])))
    set_config('backpack_item',  data.get('backpack', 'item_backpack_large_base'))
    set_config('backpack_scale', str(data.get('scale', 120)))
    set_config('backpack_hue',   str(data.get('hue',   50)))
    set_config('backpack_sat',   str(data.get('sat',   50)))
    audit('global_loadout_set'); return jsonify({'ok': True})

@app.route('/admin/api/spawn', methods=['POST'])
def admin_spawn_item():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json(force=True) or {}
    item_id = data.get('item_id', '').strip()
    if not item_id: return jsonify({'error': 'item_id required'}), 400
    pos_x = float(data.get('pos_x', 0)); pos_y = float(data.get('pos_y', 0)); pos_z = float(data.get('pos_z', 0))
    scale = float(data.get('scale', 1.0)); hue = int(data.get('color_hue', 0)); sat = int(data.get('color_sat', 0))
    custom_id = data.get('custom_id') or None; expires_in = int(data.get('expires_in', 0))
    expires_at = (time.time() + expires_in) if expires_in > 0 else None
    conn = get_conn()
    conn.execute('INSERT INTO spawn_queue (item_id, pos_x, pos_y, pos_z, scale, color_hue, color_sat, custom_id, created_at, expires_at) VALUES (?,?,?,?,?,?,?,?,?,?)',
                 (item_id, pos_x, pos_y, pos_z, scale, hue, sat, custom_id, time.time(), expires_at))
    conn.commit()
    spawn_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    audit('item_spawn', target=custom_id or 'global', detail=f'{item_id} at ({pos_x},{pos_y},{pos_z})')
    return jsonify({'ok': True, 'spawn_id': spawn_id})

@app.route('/admin/api/spawn/queue', methods=['GET'])
def admin_spawn_queue():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_conn()
    rows = conn.execute('SELECT * FROM spawn_queue ORDER BY created_at DESC LIMIT 100').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/admin/api/spawn/<int:spawn_id>', methods=['DELETE'])
def admin_spawn_delete(spawn_id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_conn(); conn.execute('DELETE FROM spawn_queue WHERE id=?', (spawn_id,)); conn.commit(); conn.close()
    audit('spawn_delete', target=str(spawn_id)); return jsonify({'ok': True})

@app.route('/admin/api/audit', methods=['GET'])
def admin_audit_get():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    limit = int(request.args.get('limit', 200))
    conn = get_conn()
    rows = conn.execute('SELECT * FROM audit_log ORDER BY performed_at DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/admin/api/audit', methods=['DELETE'])
def admin_audit_clear():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_conn(); conn.execute('DELETE FROM audit_log'); conn.commit(); conn.close()
    return jsonify({'ok': True})

# ═══════════════════════════════════════════════════════════════════════════════
#  WSGI ENTRY
# ═══════════════════════════════════════════════════════════════════════════════
A2 = appp