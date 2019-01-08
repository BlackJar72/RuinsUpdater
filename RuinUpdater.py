import fileinput
import random
import sys
import re
import os

mappings = {
    "0":"air",
    "1":"stone",
    "2":"grass",
    "3":"dirt",
    "4":"cobblestone",
    "5":"planks",
    "6":"sapling",
    "7":"bedrock",
    "8":"flowing_water",
    "9":"water",
    "10":"flowing_lava",
    "11":"lava",
    "12":"sand",
    "13":"gravel",
    "14":"gold_ore",
    "15":"iron_ore",
    "16":"coal_ore",
    "17":"log",
    "18":"leaves",
    "19":"sponge",
    "20":"glass",
    "21":"lapis_ore",
    "22":"lapis_block",
    "23":"dispenser",
    "24":"sandstone",
    "25":"noteblock",
    "26":"bed",
    "27":"golden_rail",
    "28":"detector_rail",
    "29":"sticky_piston",
    "30":"web",
    "31":"tallgrass",
    "32":"deadbush",
    "33":"piston",
    "34":"piston_head",
    "35":"wool",
    "36":"piston_extension",
    "37":"yellow_flower",
    "38":"red_flower",
    "39":"brown_mushroom",
    "40":"red_mushroom",
    "41":"gold_block",
    "42":"iron_block",
    "43":"double_stone_slab",
    "44":"stone_slab",
    "45":"brick_block",
    "46":"tnt",
    "47":"bookshelf",
    "48":"mossy_cobblestone",
    "49":"obsidian",
    "50":"torch",
    "51":"fire",
    "52":"mob_spawner",
    "53":"oak_stairs",
    "54":"chest",
    "55":"redstone_wire",
    "56":"diamond_ore",
    "57":"diamond_block",
    "58":"crafting_table",
    "59":"wheat",
    "60":"farmland",
    "61":"furnace",
    "62":"lit_furnace",
    "63":"standing_sign",
    "64":"wooden_door",
    "65":"ladder",
    "66":"rail",
    "67":"stone_stairs",
    "68":"wall_sign",
    "69":"lever",
    "70":"stone_pressure_plate",
    "71":"iron_door",
    "72":"wooden_pressure_plate",
    "73":"redstone_ore",
    "74":"lit_redstone_ore",
    "75":"unlit_redstone_torch",
    "76":"redstone_torch",
    "77":"stone_button",
    "78":"snow_layer",
    "79":"ice",
    "80":"snow",
    "81":"cactus",
    "82":"clay",
    "83":"reeds",
    "84":"jukebox",
    "85":"fence",
    "86":"pumpkin",
    "87":"netherrack",
    "88":"soul_sand",
    "89":"glowstone",
    "90":"portal",
    "91":"lit_pumpkin",
    "92":"cake",
    "93":"unpowered_repeater",
    "94":"powered_repeater",
    "95":"stained_glass",
    "96":"trapdoor",
    "97":"monster_egg",
    "98":"stonebrick",
    "99":"brown_mushroom_block",
    "100":"red_mushroom_block",
    "101":"iron_bars",
    "102":"glass_pane",
    "103":"melon_block",
    "104":"pumpkin_stem",
    "105":"melon_stem",
    "106":"vine",
    "107":"fence_gate",
    "108":"brick_stairs",
    "109":"stone_brick_stairs",
    "110":"mycelium",
    "111":"waterlily",
    "112":"nether_brick",
    "113":"nether_brick_fence",
    "114":"nether_brick_stairs",
    "115":"nether_wart",
    "116":"enchanting_table",
    "117":"brewing_stand",
    "118":"cauldron",
    "119":"end_portal",
    "120":"end_portal_frame",
    "121":"end_stone",
    "122":"dragon_egg",
    "123":"redstone_lamp",
    "124":"lit_redstone_lamp",
    "125":"double_wooden_slab",
    "126":"wooden_slab",
    "127":"cocoa",
    "128":"sandstone_stairs",
    "129":"emerald_ore",
    "130":"ender_chest",
    "131":"tripwire_hook",
    "132":"tripwire",
    "133":"emerald_block",
    "134":"spruce_stairs",
    "135":"birch_stairs",
    "136":"jungle_stairs",
    "137":"command_block",
    "138":"beacon",
    "139":"cobblestone_wall",
    "140":"flower_pot",
    "141":"carrots",
    "142":"potatoes",
    "143":"wooden_button",
    "144":"skull",
    "145":"anvil",
    "146":"trapped_chest",
    "147":"light_weighted_pressure_plate",
    "148":"heavy_weighted_pressure_plate",
    "149":"unpowered_comparator",
    "150":"powered_comparator",
    "151":"daylight_detector",
    "152":"redstone_block",
    "153":"quartz_ore",
    "154":"hopper",
    "155":"quartz_block",
    "156":"quartz_stairs",
    "157":"activator_rail",
    "158":"dropper",
    "159":"stained_hardened_clay",
    "160":"stained_glass_pane",
    "161":"leaves2",
    "162":"log2",
    "163":"acacia_stairs",
    "164":"dark_oak_stairs",
    "165":"slime",
    "170":"hay_block",
    "171":"carpet",
    "172":"hardened_clay",
    "173":"coal_block",
    "174":"packed_ice",
    "175":"double_plant"
}


ruleReplace = {
    'acceptable_target_blocks',
    'unacceptable_target_block'
}


spawnersEasy   = ['Zombie']
spawnersMedium = ['Zombie', 'Skeleton', 'Spider']
spawnersHard   = ['Creeper', 'Cave_Spider', 'Blaze']


rulePat     = re.compile('^rule\\d+=\\d+,\\s*\\d+,')
rulePart    = re.compile('^\\d+,\\s*\\d+,')
equalDelim  = re.compile('\\s*=\\s*')
comaDelim   = re.compile('\\s*,\\s*')
hyphenDelim = re.compile('-')


if len(sys.argv) > 2:
  whereToPut = sys.argv[2]
else:
  whereToPut = 'updater-out'


def processFile(fileName): 
  outfile = open(os.path.join(whereToPut, fileName), 'w')
  try: 
    infiledat = open(fileName, 'r').readlines()
    for line in infiledat:
      outfile.write(processLine(line))
  except:
    print("Error reading file {0}; aborting".format(fileName))
    outfile.close()
    os.remove(os.path.join(whereToPut, fileName))
    return
  outfile.close()


def processLine(line):
  pieces = equalDelim.split(line)
  if pieces[0][0:4] == 'rule':
    line = updateRuleLineBetter(pieces, 2)
  if pieces[0].strip() in ruleReplace:
    line = updateRuleLineBetter(pieces, 0)
  return line


def makeMultiSpawners(level):
  if level == 'MediumMobSpawn':
    return ','.join(["MobSpawner:" + name for name in spawnersMedium])
  elif level == 'HardMobSpawn':
    return ','.join(["MobSpawner:" + name for name in spawnersHard])
  else:
    return ','.join(["MobSpawner:" + name for name in spawnersEasy])


def makeSpawners(level):
  if level == 'MediumMobSpawn':
    return 'MobSpaner:{0}'.format(spawnersMedium[random.randrange(len(spawnersMedium))])
  elif level == 'HardMobSpawn':
    return 'MobSpaner:{0}'.format(spabwersHard[random.randrange(len(spawnersHard))])
  else:
    return 'MobSpaner:{0}'.format(spawnersEasy[random.randrange(len(spawnersEasy))])


def makeGenericSpawner(level):
    return 'mob_spawner'


if len(sys.argv) > 3 and sys.argv[3][0:3].lower() == 'one':
  spawnerFunc = makeSpawners
elif len(sys.argv) > 3 and sys.argv[3][0:4].lower() == 'many':
  spawnerFunc = makeMultiSpawners
else:
  spawnerFunc = makeGenericSpawner


def updateRuleLineBetter(line, offset):
  blocks = comaDelim.split(line[1].strip('\n'))
  bout = [x for x in blocks[0:offset]]
  #print(bout)
  for block in blocks[offset:]:		
    parts = hyphenDelim.split(block)
    if parts[0].isnumeric():
      if len(parts) > 1:
        bout.append(mappings[parts[0]] + "-" + parts[1])
      else:
        bout.append(mappings[parts[0]])
    #elif block[-8:] == 'MobSpawn':      
    #  bout.append(spawnerFunc(block)) #bout.append(makeSpawner(block))
    else:
      bout.append(block)
  #print(bout)
  return (line[0] + "=" + ','.join(bout) + '\n')


def processDirectory(name):
  for fname in os.listdir(name):
    it = os.path.join(name, fname)
    if os.path.isdir(it):
      outdir = os.path.join(whereToPut, it)
      if not os.path.exists(outdir):
        os.makedirs(outdir)
      processDirectory(os.path.join(it))
    else:
      processFile(os.path.join(it))


def startProcess(name):
    if os.path.isdir(name):
      if not os.path.exists(os.path.join(whereToPut, name)):
        os.makedirs(os.path.join(whereToPut, name))
      processDirectory(name)
    else:
      processFile(name)


def main():
  startProcess(sys.argv[1])


if __name__ == "__main__":
  random.seed()
  main()
