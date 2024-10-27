class Room:
    def __init__(self, name, tier, upgrades_to=None, rewards=None):
        self.name = name
        self.tier = tier
        self.upgrades_to = upgrades_to  # Name of the next-tier room
        self.rewards = rewards or []

t0_room_names = ['Antechamber', 'Apex of Atzoatl', 'Banquet Hall', 'Cellar', 'Chasm', 'Cloister', 'Entrance', 'Halls', 'Passageways', 'Pits', 'Tombs', 'Tunnels']
rooms = {name: Room(name, 0) for name in t0_room_names}

room_list_list = [
    ['Sacrificial Chamber', 'Hall of Offerings', 'Apex of Ascension', 'C: ancient orb effect, vial?'],
    ['Armourer\'s Workshop', 'Armoury', 'Chamber of Iron', 'F: chests containing armor'],
    ['Jeweller\'s Workshop', 'Jewellery Forge', 'Glittering Halls', 'D: chests containing jewellery, inc rarity'],
    ['Guardhouse', 'Barracks', 'Hall of War', 'D: increased pack size'],
    ['Hatchery', 'Automaton Lab', 'Hybridisation Chamber', 'F: 10c unique or minion mods'],
    ['Vault', 'Treasury', 'Wealth of the Vaal', 'C: chests w/ currency'],
    ['Pools of Restoration', 'Sanctum of Vitality', 'Sanctum of Immortality', 'B: 1d unique or life/ES mods'],
    ['Explosives Room', 'Demolition Lab', 'Shrine of Unmaking', '?: open passage'],
    ['Workshop', 'Engineering Department', 'Factory', 'D: moar items'],
    ['Storage Room', 'Warehouses', 'Museum of Artefacts', 'D: chests containing items'],
    ['Trap Workshop', 'Temple Defense Workshop', 'Defense Research Lab', 'C: 30c unique or speed mods'],
    ['Hall of Mettle', 'Hall of Heroes', 'Hall of Legends', 'F: legion mechanic'],
    ['Corruption Chamber', 'Catalyst of Corruption', 'Locus of Corruption', 'SSS: double corrupt!'],
    ['Flame Workshop', 'Omnitect Forge', 'Crucible of Flame', 'C: 5c unique or good resistance mods'],
    ['Shrine of Empowerment', 'Sanctum of Unity', 'Temple Nexus', 'A: upgrades adjacent room(s) by 1 tier'],
    ['Poison Garden', 'Cultivar Chamber', 'Toxic Grove', 'F: 2c unique or chaos damage mods'],
    ['Sparring Room', 'Arena of Valour', 'Hall of Champions', 'F: chests containing weapons'],
    ['Tempest Generator', 'Hurricane Engine', 'Storm of Corruption', 'C: tempest mechanic?, good damage mods'],
    ['Torment Cells', 'Torture Cages', 'Sadist\'s Den', 'F: tormented spirit mechanic'],
    ['Surveyor\'s Study', 'Office of Cartography', 'Atlas of Worlds', 'C: chests containing maps'],
    ['Royal Meeting Room', 'Hall of Lords', 'Throne of Atziri', 'F: fight temple final boss'],
    ['Lightning Workshop', 'Omnitect Reactor Plant', 'Conduit of Lightning', 'C: 10c unique or mana mods, including bussin -8 total mana cost'],
    ['Gemcutter\'s Workshop', 'Department of Thaumaturgy', 'Doryani\'s Institute', 'SSS: double corrupt gem!'],
    ['Strongbox Chamber', 'Hall of Locks', 'Court of Sealed Death', 'F: strongbox mechanic'],
    ['Splinter Research Lab', 'Breach Containment Chamber', 'House of the Others', 'F: breach mechanic'],
]

for room_list in room_list_list:
    t1 = Room(room_list[0], 1, room_list[1], [room_list[3]])
    t2 = Room(room_list[1], 2, room_list[2], [room_list[3]])
    t3 = Room(room_list[2], 3, None, [room_list[3]])
    rooms.update({room_list[0]: t1, room_list[1]: t2, room_list[2]: t3})
