import random, copy, mysql.connector
#=========================SQL CONNECTION===============================#
connection = mysql.connector.connect(host="localhost", database="pokedex", user="root", passwd="F@ng2525!")
cursor = connection.cursor()
#=========================STAGE MULTIPLIER=============================#
# Each stat has a stage. The stat is multiplied by a certain fraction depending on the stage.
stage_multiplier = {6:(8/2),5:(7/2),4:(6/2),3:(5/2),2:(4/2),1:(3/2),0:(2/2),
                    -1:(2/3),-2:(2/4),-3:(2/5),-4:(2/6),-5:(2/7),-6:(2/8)}

#============================POKEMON===================================#
class Pokemon:
    def __init__(self, name, level, type1, type2, hp, attack, defense, spatt, spdef, speed):
        self.name = name
        self.level = level
        self.type1= type1
        self.type2 = type2
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.spatt = spatt
        self.spdef = spdef
        self.speed = speed

        self.att_stg = 0
        self.def_stg = 0
        self.spatt_stg = 0
        self.spdef_stg = 0
        self.spd_stg = 0
        self.evd_stg = 0
        self.acc_stg = 0
        self.priority = 1

        self.status = "Normal"
        self.status_count = 0
        self.psn_count = 0
        self.red_phys_count = 0
        self.red_spec_count = 0
        self.counter_attack = 0
        self.focus_count = 0
        self.move_count = 0

        self.can_attack = True
        self.new_move = True
        self.no_lowered_stats = False
        self.took_damage = False
        self.leech_seeded = False
        self.thrash_mode = False
        self.is_flying = False
        self.is_digging = False
        self.is_charging = False

        self.moveset = []
        self.base_stats = {"hp":0,"attack":0,"defense":0,"spatt":0,"spdef":0,"speed":0}

        self.disabled_move = {}
        self.disabled_count = 0

    def __repr__(self):
        return ("Name: {}\nLevel: {}\nType 1: {}\nType 2: {}\nHP: {}\nAttack: {}\nDefense: {}\n"
                "Sp. Attack: {}\nSp. Defense: {}\nSpeed: {}".format
                (self.name, self.level, self.type1, self.type2,
                 self.hp, self.attack, self.defense, self.spatt, self.spdef, self.speed))

    def stat_multiplier(self):
        self.max_hp = round((((2 * self.hp + 94) * self.level)/100) + self.level + 10)
        self.hp = round((((2 * self.hp + 94) * self.level)/100) + self.level + 10)
        self.attack = round((((2 * self.attack + 94) * self.level)/100) + 5)
        self.defense = round((((2 * self.defense + 94) * self.level)/100) + 5)
        self.spatt = round((((2 * self.spatt + 94) * self.level)/100) + 5)
        self.spdef = round((((2 * self.spdef + 94) * self.level)/100) + 5)
        self.speed = round((((2 * self.speed + 94) * self.level)/100) + 5)

#=======================BATTLE FUNCTIONS===============================#
def who_is_faster(user1, move1, user2, move2):
    if move1['name'] == "Quick Attack":
        user1.priority += 1
    if move2['name'] == "Quick Attack":
        user2.priority += 1
    if move1['effect'] == "reaction":
        user1.priority -= 1
    if move2['effect'] == "reaction":
        user2.priority -= 1
    if user1.priority > user2.priority:
        faster_combatant = user1
        fast_move = move1
        slower_combatant = user2
        slow_move = move2
        return faster_combatant, fast_move, slower_combatant, slow_move
    elif user2.priority > user1.priority:
        faster_combatant = user2
        fast_move = move2
        slower_combatant = user1
        slow_move = move1
        return faster_combatant, fast_move, slower_combatant, slow_move
    else:
        if user1.speed > user2.speed:
            faster_combatant = user1
            fast_move = move1
            slower_combatant = user2
            slow_move = move2
            return faster_combatant, fast_move, slower_combatant, slow_move
        elif user2.speed > user1.speed:
            faster_combatant = user2
            fast_move = move2
            slower_combatant = user1
            slow_move = move1
            return faster_combatant, fast_move, slower_combatant, slow_move
        else:
            x = [user1, user2]
            faster_combatant = random.choice(x)
            x.remove(faster_combatant)
            slower_combatant = x[0]
            if faster_combatant.name == user1.name:
                fast_move = move1
            else:
                fast_move = move2
            if slower_combatant.name == user1.name:
                slow_move = move1
            else:
                slow_move = move2
            return faster_combatant, fast_move, slower_combatant, slow_move

def did_it_hit(attacker, move, defender):
    if defender.type1 in move["no effect"] or defender.type2 in move["no effect"]:
        return False
    if move['name'] == "Dream Eater":
        if defender.status != "Sleep":
            return False
    if move['target'] == "recharge" and attacker.move_count == 1:
        return True
    if move['name'] == "Hyper Beam" and attacker.move_count == 1:
        return True
    if defender.is_flying is True:
        if move['name'] == "Thunder" or move['name'] == "Gust":
            r = random.randint(1, 100)
            if (stage_multiplier[attacker.acc_stg] / stage_multiplier[defender.evd_stg]) * move['accuracy'] >= r:
                return True
            else:
                return False
        else:
            return False
    if defender.is_digging is True:
        if move['name'] == "Earthquake" or move['name'] == "Fissure":
            r = random.randint(1, 100)
            if (stage_multiplier[attacker.acc_stg] / stage_multiplier[defender.evd_stg]) * move['accuracy'] >= r:
                return True
            else:
                return False
        else:
            return False
    r = random.randint(1,100)
    if (stage_multiplier[attacker.acc_stg]/stage_multiplier[defender.evd_stg]) * move['accuracy'] >= r:
        return True
    else:
        return False

def how_many_attacks(user, move):
    attack_loop = 1
    if move['target'] == "attack loop":
        effect = eval(move['effect'])
        attack_loop = effect()
        return attack_loop
    if move['target'] == "recharge" and user.move_count == 1:
        attack_loop = 0
        return attack_loop
    if move['name'] == "Hyper Beam" and user.is_charging is True:
        attack_loop = 0
        return attack_loop
    return attack_loop

def damage_multiplier(attacker, move, defender):
    damage = 0
    random_multiple = random.uniform(0.85,1.00)
    if move['category'] == "Physical":
        damage += ((2 * attacker.level / 5 + 2) * move['power'] * (attacker.attack / defender.defense) + 2) / 50
    if move['category'] == "Special":
        damage += ((2 * attacker.level / 5 + 2) * move['power'] * (attacker.spatt / defender.spdef) + 2) / 50
    damage *= random_multiple
    if attacker.type1 == move['type'] or attacker.type2 == move['type']:
        damage *= 1.5
    if defender.type1 in move["super"]:
        damage *= 2
    if defender.type2 in move["super"]:
        damage *= 2
    if defender.type1 in move["weak"]:
        damage /= 2
    if defender.type2 in move["weak"]:
        damage /= 2
    if defender.is_flying is True:
        if move['name'] == "Gust":
            damage *= 2
    if defender.is_digging is True:
        if move['name'] == "Earthquake":
            damage *= 2
    if move['target'] == "advanced_crit" or attacker.focus_count > 0:
        adv_crit_hit = random.randint(1, 8)
        if adv_crit_hit == 1:
            print("Critical hit!")
            damage *= 2
    crit_hit = random.randint(1,24)
    if crit_hit == 1:
        damage *= 2
    if move['target'] == "wrapped_up":
        i = random.randint(2, 5)
        damage += (defender.max_hp / 8) * i
    if defender.red_phys_count > 0 and move['category'] == "Physical":
        damage /= 2
    if defender.red_spec_count > 0 and move['category'] == "Special":
        damage /= 2
    if move['target'] == "counter":
        damage = attacker.counter_attack * 2
    damage = round(damage)
    return damage

def flat_damage(user, move1, enemy, move2):
    if move1['name'] == "Dragon Rage":
        damage = 40
        enemy.hp -= damage
        if move2['name'] == "Counter":
            enemy.counter_attack += damage
        if move2['name'] == "Bide" and enemy.new_move == False:
            enemy.counter_attack += damage
    if move1['name'] == "Sonic Boom":
        damage = 20
        enemy.hp -= damage
        if move2['name'] == "Counter":
            enemy.counter_attack += damage
        if move2['name'] == "Bide" and enemy.new_move == False:
            enemy.counter_attack += damage
    if move1['name'] == "Super Fang":
        if enemy.type1 == "Ghost" or enemy.type2 == "Ghost":
            print("It had no effect!")
        else:
            if enemy.hp == 1:
                enemy.hp -= 1
            else:
                damage = round(enemy.hp / 2)
                enemy.hp -= damage
                if move2['name'] == "Counter":
                    enemy.counter_attack += damage
                if move2['name'] == "Bide" and enemy.new_move == False:
                    enemy.counter_attack += damage
    if move1['name'] == "Night Shade" or move1['name'] == "Seismic Toss":
        damage = user.level
        enemy.hp -= damage
        if move2['name'] == "Counter":
            enemy.counter_attack += damage
        if move2['name'] == "Bide" and enemy.new_move == False:
            enemy.counter_attack += damage
    if move1['name'] == "Psywave":
        i = random.randint(50, 150)
        damage = round((user.level * i) / 100)
        enemy.hp -= damage
        if move2['name'] == "Counter":
            enemy.counter_attack += damage
        if move2['name'] == "Bide" and enemy.new_move == False:
            enemy.counter_attack += damage

def flinch_check(pokemon, move):
    if pokemon.type1 != "Ghost" or pokemon.type2 != "Ghost":
        if move['effect'] == "flinch":
            i = random.randint(1, 10)
            if move['target'] == "thirty":
                if i <= 3:
                    return False
            elif move['target'] == "ten":
                if i == 1:
                    return False
    return True

def status_effects(user, enemy):
    # Check for frozen
    if user.status == "Frozen":
        user.can_attack = False
    # Check for sleep
    if user.status == "Sleep":
        user.can_attack = False
    # Check for confusion
    if user.status == "Confused":
        i = random.randint(1, 2)
        if i == 1:
            user.hp -= round(((2 * user.level / 5 + 2) * 40 * (user.attack / enemy.defense) + 2) / 50)
            user.can_attack = False
    # Check for paralysis
    if user.status == "Paralyzed":
        i = random.randint(1, 4)
        if i == 1:
            user.can_attack = False

def status_check(user, enemy):
    if user.status == "Sleep" or user.status == "Frozen" or user.status == "Confused":
        if user.status_count > 0:
            user.status_count -= 1
        else:
            user.status = "Normal"
            user.thrash_mode = False
    if user.status == "Burned":
        brn_dmg = round(user.max_hp / 16)
        user.hp -= brn_dmg
    if user.status == "Poisoned":
        psn_dmg = round(user.max_hp / 16)
        user.hp -= psn_dmg
    if user.status == "Badly Poisoned":
        psn_dmg = round(user.max_hp * (user.psn_count / 16))
        user.hp -= psn_dmg
        user.psn_count += 1
    if user.leech_seeded == True:
        user.hp -= round(user.max_hp / 8)
        enemy.hp += round(user.max_hp / 8)

def defensive_check(user):
    if user.red_phys_count > 0:
        user.red_phys_count -= 1
    if user.red_spec_count > 0:
        user.red_spec_count -= 1

def disabled_effects(user):
    if user.disabled_count > 0:
        user.disabled_count -= 1
    else:
        if bool(user.disabled_move) != False:
            user.moveset.append(user.disabled_move)
            user.disabled_move.clear()

def recharge_move_effects(user):
    if user.is_flying is True and user.move_count == 0:
        user.is_flying = False
        user.new_move = True
    if user.is_digging is True and user.move_count == 0:
        user.is_digging = False
        user.new_move = True
    if user.is_charging is True and user.move_count == 0:
        user.is_charging = False
        user.new_move = True

def the_hb_effect(user, move):
    if move['name'] == "Hyper Beam" and user.is_charging is False:
        recharge_move(user)

def move_counters(user):
    if user.move_count > 0:
        user.move_count -= 1
    if user.focus_count > 0:
        user.focus_count -= 1

def getting_angry(user, move):
    if user.took_damage is True and move['name'] == "Rage":
        raise_att_one(user)

def steal_health(user, move, dmg):
    if move['target'] == "absorbed":
        user.hp += round(dmg / 2)
        if user.hp > user.max_hp:
            user.hp = user.max_hp

def self_inflicted(user, move, dmg):
    if move['target'] == "self-dmg":
        user.hp -= round(dmg / 4)

#===========================STAT STAGES================================#
def raise_att_one(user):
    try:
        user.att_stg += 1
        user.attack = round(
            ((((2 * user.base_stats['attack'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.att_stg])
    except:
        if user.att_stg > 6:
            user.att_stg = 6

def raise_att_two(user):
    try:
        user.att_stg += 2
        user.attack = round(
            ((((2 * user.base_stats['attack'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.att_stg])
    except:
        if user.att_stg > 6:
            user.att_stg = 6

def raise_def_one(user):
    try:
        user.def_stg += 1
        user.defense = round(
            ((((2 * user.base_stats['defense'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.def_stg])
    except:
        if user.def_stg > 6:
            user.def_stg = 6

def raise_def_two(user):
    try:
        user.def_stg += 2
        user.defense = round(
            ((((2 * user.base_stats['defense'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.def_stg])
    except:
        if user.def_stg > 6:
            user.def_stg = 6

def raise_spatt_one(user):
    try:
        user.spatt_stg += 1
        user.spatt = round(
            ((((2 * user.base_stats['spatt'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.spatt_stg])
    except:
        if user.spatt_stg > 6:
            user.spatt_stg = 6

def raise_spdef_two(user):
    try:
        user.spdef_stg += 2
        user.spdef = round(
            ((((2 * user.base_stats['spdef'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.spdef_stg])
    except:
        if user.spdef_stg > 6:
            user.spdef_stg = 6

def raise_speed_two(user):
    try:
        user.spd_stg += 2
        user.speed = round(
            ((((2 * user.base_stats['speed'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.spd_stg])
    except:
        if user.spd_stg > 6:
            user.spd_stg = 6

def raise_evade_one(user):
    if user.evd_stg < 6:
        user.evd_stg += 1
    else:
        user.evd_stg = 6

def raise_evade_two(user):
    if user.evd_stg < 6:
        user.evd_stg += 2
    else:
        user.evd_stg = 6

def lower_att_one(enemy):
    if enemy.no_lowered_stats == True:
        return
    try:
        enemy.att_stg -= 1
        enemy.attack = round(
            ((((2 * enemy.base_stats['attack'] + 94) * enemy.level) / 100) + 5) * stage_multiplier[enemy.att_stg])
    except:
        if enemy.att_stg < 6:
            enemy.att_stg = -6

def lower_def_one(enemy):
    if enemy.no_lowered_stats == True:
        return
    try:
        enemy.def_stg -= 1
        enemy.defense = round(
            ((((2 * enemy.base_stats['defense'] + 94) * enemy.level) / 100) + 5) * stage_multiplier[enemy.def_stg])
    except:
        if enemy.def_stg < 6:
            enemy.def_stg = -6

def lower_def_two(enemy):
    if enemy.no_lowered_stats == True:
        return
    try:
        enemy.def_stg -= 2
        enemy.defense = round(
            ((((2 * enemy.base_stats['defense'] + 94) * enemy.level) / 100) + 5) * stage_multiplier[enemy.def_stg])
    except:
        if enemy.def_stg < 6:
            enemy.def_stg = -6

def lower_speed_one(enemy):
    if enemy.no_lowered_stats == True:
        return
    try:
        enemy.spd_stg -= 1
        enemy.speed = round(
            ((((2 * enemy.base_stats['speed'] + 94) * enemy.level) / 100) + 5) * stage_multiplier[enemy.spd_stg])
    except:
        if enemy.spd_stg < 6:
            enemy.spd_stg = -6

def lower_acc_one(enemy):
    if enemy.no_lowered_stats == True:
        return
    if enemy.acc_stg > -6:
        enemy.acc_stg -= 1
    else:
        enemy.acc_stg = -6

#======================DAMAGE & STAT STAGES============================#
def dmg_lwr_att(user):
    i = random.randint(1,10)
    if i == 1:
        lower_att_one(user)

def dmg_lwr_def(user):
    i = random.randint(1,10)
    if i == 1:
        lower_def_one(user)

def dmg_lwr_sp_def(user):
    i = random.randint(1,10)
    if i == 1:
        try:
            user.spdef_stg -= 1
            user.spdef = round(
                ((((2 * user.base_stats['spdef'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.spdef_stg])
        except:
            if user.spdef_stg < 6:
                user.spdef_stg = -6

def dmg_lwr_spd(user):
    i = random.randint(1,10)
    if i == 1:
        try:
            user.spd_stg -= 1
            user.speed = round(
                ((((2 * user.base_stats['speed'] + 94) * user.level) / 100) + 5) * stage_multiplier[user.spd_stg])
        except:
            if user.spd_stg < 6:
                user.spd_stg = -6

#==========================STATUS FUNCTIONS============================#
#===========BURN===============#
def get_burned(enemy):
    if enemy.type1 == "Fire" or enemy.type2 == "Fire":
        return
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i == 1:
            enemy.status = "Burned"
    else:
        return

def get_burned_30(enemy):
    if enemy.type1 == "Fire" or enemy.type2 == "Fire":
        return
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i <= 3:
            enemy.status = "Burned"
    else:
        return

#==========CONFUSE=============#
def get_confused(enemy):
    if enemy.status == "Normal":
        enemy.status = "Confused"
        enemy.status_count = random.randint(2,5)
    else:
        return

def get_confused_10(enemy):
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i == 1:
            enemy.status = "Confused"
            enemy.status_count = random.randint(2, 5)
    else:
        return

#==========FREEZE==============#
def get_frozen(enemy):
    if enemy.type1 == "Ice" or enemy.type2 == "Ice":
        return
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i == 1:
            enemy.status = "Frozen"
            enemy.status_count = random.randint(1,5)
    else:
        return

#=========PARALYZE=============#
def get_paralyzed(enemy):
    if enemy.type1 == "Electric" or enemy.type2 == "Electric":
        return
    if enemy.status == "Normal":
        enemy.status = "Paralyzed"
        enemy.speed = round(enemy.speed * 0.25)
    else:
        return

def get_paralyzed_10(enemy):
    if enemy.type1 == "Electric" or enemy.type2 == "Electric":
        return
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i == 1:
            enemy.status = "Paralyzed"
            enemy.speed = round(enemy.speed * 0.25)
    else:
        return

def get_paralyzed_30(enemy):
    if enemy.type1 == "Electric" or enemy.type2 == "Electric":
        return
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i <= 3:
            enemy.status = "Paralyzed"
            enemy.speed = round(enemy.speed * 0.25)
    else:
        return

#==========POISON==============#
def get_poisoned(enemy):
    if enemy.type1 == "Poison" or enemy.type2 == "Poison":
        return
    if enemy.status == "Normal":
        enemy.status = "Poisoned"
    else:
        return

def get_toxic(enemy):
    if enemy.type1 == "Poison" or enemy.type2 == "Poison":
        return
    if enemy.status == "Normal":
        enemy.status = "Badly Poisoned"
        enemy.psn_count = 1
    else:
        return

def get_poisoned_20(enemy):
    if enemy.type1 == "Poison" or enemy.type2 == "Poison":
        return
    if enemy.status == "Normal":
        i = random.randint(1, 5)
        if i == 1:
            enemy.status = "Poisoned"
    else:
        return

def get_poisoned_30(enemy):
    if enemy.type1 == "Poison" or enemy.type2 == "Poison":
        return
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i <= 3:
            enemy.status = "Poisoned"
    else:
        return

def get_poisoned_40(enemy):
    if enemy.type1 == "Poison" or enemy.type2 == "Poison":
        return
    if enemy.status == "Normal":
        i = random.randint(1,10)
        if i <= 4:
            enemy.status = "Poisoned"
    else:
        return

#===========SLEEP==============#
def get_sleep(enemy):
    if enemy.status == "Normal":
        enemy.status = "Sleep"
        enemy.status_count = random.randint(1,5)
    else:
        return

#============================MOVE FUNCTIONS============================#
def times_two():
    return 2

def multi_attack():
    i = random.randint(2,5)
    return i

def suicide(user):
    user.hp -= user.hp

def heal(user):
    if user.hp < user.max_hp:
        user.hp += round(user.max_hp / 2)
        if user.hp > user.max_hp:
            user.hp = user.max_hp
    else:
        return

def reset_stats(user, enemy):
    user.status = "Normal"
    user.att_stg = 0
    user.def_stg = 0
    user.spatt_stg = 0
    user.spdef_stg = 0
    user.spd_stg = 0
    user.evd_stg = 0
    user.acc_stg = 0
    enemy.status = "Normal"
    enemy.att_stg = 0
    enemy.def_stg = 0
    enemy.spatt_stg = 0
    enemy.spdef_stg = 0
    enemy.spd_stg = 0
    enemy.evd_stg = 0
    enemy.acc_stg = 0

def stat_stasis(user):
    user.no_lowered_stats = True

def leeched(enemy):
    if enemy.leech_seeded == True:
        return
    else:
        enemy.leech_seeded = True

def tri_att(enemy):
    i = random.randint(1,5)
    if i == 1 and enemy.status == "Normal":
        j = random.randint(1,3)
        if j == 1:
            if enemy.type1 == "Ice" or enemy.type2 == "Ice":
                return
            else:
                enemy.status = "Frozen"
        elif j == 2:
            if enemy.type1 != "Fire":
                enemy.status = "Burned"
        else:
            if enemy.type1 != "Electric":
                enemy.status = "Paralyzed"

def resting(user):
    if user.status == "Sleep":
        return
    else:
        user.status = "Sleep"
        user.status_count = 2
        user.hp = user.max_hp

def disabled(enemy):
    if len(enemy.moveset) <= 3:
        return
    else:
        i = random.randint(1,8)
        move = random.randint(0,3)
        enemy.disabled_move = enemy.moveset[move]
        enemy.moveset.remove(enemy.moveset[move])
        enemy.disabled_count = i

def reduce_physical(user):
    if user.red_phys_count > 0:
        return
    else:
        user.red_phys_count = 5

def reduce_special(user):
    if user.red_spec_count > 0:
        return
    else:
        user.red_spec_count = 5

def convert(user):
    user.type1 = user.moveset[0]['type']
    user.type2 = user.moveset[0]['type']

def copy_cat(user, move, enemy):
    user.moveset.remove(move)
    i = random.randint(0,3)
    user.moveset.append(enemy.moveset[i])

def reaction(user):
    user.priority = 0

def transforming(user, enemy):
    user.type1 = enemy.type1
    user.type2 = enemy.type2
    user.attack = enemy.attack
    user.defense = enemy.defense
    user.spatt = enemy.spatt
    user.spdef = enemy.spdef
    user.speed = enemy.speed
    user.moveset = enemy.moveset

def swiftly(user, enemy):
    user.acc_stg = 0
    user.evd_stg = 0
    enemy.acc_stg = 0
    enemy.evd_stg = 0

def thrashing(user):
    if user.move_count > 0:
        return
    else:
        i = random.randint(2,3)
        user.move_count = i
        user.thrash_mode = True
        user.new_move = False

def i_love_thrashing(user):
    user.new_move = True
    user.thrash_mode = False
    get_confused(user)

def biding_time(user):
    if user.move_count > 0:
        return
    else:
        i = random.randint(3,4)
        user.move_count = i
        user.new_move = False

def flying_high(user):
    if user.is_flying is True:
        return
    else:
        user.is_flying = True
        user.move_count = 1
        user.new_move = False

def digging_deep(user):
    if user.is_digging is True:
        return
    else:
        user.is_digging = True
        user.move_count = 1
        user.new_move = False

def recharge_move(user):
    if user.is_charging is True:
        return
    else:
        user.is_charging = True
        user.move_count = 1
        user.new_move = False

def recharging_loop(user, move):
    if move['target'] == "recharge":
        if move['name'] == "Fly":
            flying_high(user)
        elif move['name'] == "Dig":
            digging_deep(user)
        else:
            recharge_move(user)

def get_focused(user):
    user.focus_count = 2

def random_attack():
    i = random.randint(1, 163)
    r_select = cursor.execute(
        "select name, type, category, power, accuracy, effect, target, super, weak, no_effect "
        "from moves where number = %s", (i,))
    r_sel = cursor.fetchone()
    r_sel_ls = list(r_sel)
    new_move = {"name": r_sel_ls[0],"type": r_sel_ls[1],"category": r_sel_ls[2],"power": r_sel_ls[3],
                "accuracy": r_sel_ls[4],"effect": r_sel_ls[5],"target": r_sel_ls[6],"super": r_sel_ls[7],
                "weak": r_sel_ls[8],"no effect":r_sel_ls[9]}
    return new_move

#=======================POKEMON SELECTION==============================#
player_pokemon = input("Which Pokemon will you choose? ")
enemy_pokemon = input("Which Pokemon will your rival choose? ")

p_selection = cursor.execute(
    "select name, type1, type2, hp, attack, defense, spatt, spdef, speed from pokemon where number = %s",
                                                                                        (player_pokemon,))
p_sel = cursor.fetchone()
p_sel_ls = list(p_sel)

e_selection = cursor.execute(
    "select name, type1, type2, hp, attack, defense, spatt, spdef, speed from pokemon where number = %s",
                                                                                        (enemy_pokemon,))
e_sel = cursor.fetchone()
e_sel_ls = list(e_sel)

player = Pokemon(p_sel_ls[0],int(input("What level is your Pokemon? ")),
                 p_sel_ls[1],p_sel_ls[2],p_sel_ls[3],p_sel_ls[4],p_sel_ls[5],p_sel_ls[6],p_sel_ls[7],p_sel_ls[8])
enemy = Pokemon(e_sel_ls[0],int(input("What level is the enemy Pokemon? ")),
                e_sel_ls[1],e_sel_ls[2],e_sel_ls[3],e_sel_ls[4],e_sel_ls[5],e_sel_ls[6],e_sel_ls[7],e_sel_ls[8])

player.base_stats['hp'] = p_sel_ls[3]
player.base_stats['attack'] = p_sel_ls[4]
player.base_stats['defense'] = p_sel_ls[5]
player.base_stats['spatt'] = p_sel_ls[6]
player.base_stats['spdef'] = p_sel_ls[7]
player.base_stats['speed'] = p_sel_ls[8]

enemy.base_stats['hp'] = e_sel_ls[3]
enemy.base_stats['attack'] = e_sel_ls[4]
enemy.base_stats['defense'] = e_sel_ls[5]
enemy.base_stats['spatt'] = e_sel_ls[6]
enemy.base_stats['spdef'] = e_sel_ls[7]
enemy.base_stats['speed'] = e_sel_ls[8]

player.stat_multiplier()
enemy.stat_multiplier()
#=========================MOVE SELECTION===============================#
def move_selection(user):
    get_moves = 4
    while get_moves > 0:
        move = input("What move do you want for {}? ".format(user.name))
        u_move = cursor.execute(
            "select name, type, category, power, accuracy, effect, target, super, weak, no_effect "
            "from moves where name = %s", (move, ))
        move_sel = cursor.fetchone()
        move_ls = list(move_sel)
        user_move = {"name": move_ls[0], "type": move_ls[1], "category": move_ls[2], "power": move_ls[3],
                        "accuracy": move_ls[4], "effect": move_ls[5], "target": move_ls[6], "super": move_ls[7],
                        "weak": move_ls[8], "no effect": move_ls[9]}
        user.moveset.append(user_move)
        get_moves -= 1

move_selection(player)
move_selection(enemy)
#======================================================================================================================#

player_copy = copy.deepcopy(player)
enemy_copy = copy.deepcopy(enemy)

player_wins = 0
player_draws = 0
enemy_wins = 0
enemy_draws = 0

print("****************")
print(player)
print("****************")
print(enemy)
print("****************")

battle = 0
while battle < 1000:
    if player.hp > 0 and enemy.hp > 0:
        player.priority = 1
        enemy.priority = 1
        if player.new_move is True:
            player_move = random.choice(player.moveset)
        if enemy.new_move is True:
            enemy_move = random.choice(enemy.moveset)
        if player_move['name'] == "Metronome":
            player_move = random_attack()
        if enemy_move['name'] == "Metronome":
            enemy_move = random_attack()
        faster_pokemon, faster_move, slower_pokemon, slower_move = who_is_faster(player, player_move, enemy, enemy_move)
        faster_pokemon.can_attack = True
        slower_pokemon.can_attack = True
        faster_pokemon.took_damage = False
        slower_pokemon.took_damage = False
        # =======================FASTER POKEMON ================================#
        # Check frozen, sleep, confusion, paralysis
        status_effects(faster_pokemon, slower_pokemon)
        # ******************** Faster Pokemon Takes Turn ********************
        if faster_move == faster_pokemon.disabled_move:
            faster_pokemon.can_attack = False
        if faster_move['name'] == "Bide":
            if faster_pokemon.new_move == False:
                if faster_pokemon.move_count > 0:
                    faster_pokemon.can_attack = False
                else:
                    damage = (faster_pokemon.counter_attack * 2)
                    slower_pokemon.hp -= damage
                    faster_pokemon.counter_attack = 0
                    faster_pokemon.new_move = True
                    faster_pokemon.can_attack = False
        if slower_pokemon.hp <= 0:
            if player.hp <= 0:
                enemy_wins += 1
            if enemy.hp <= 0:
                player_wins += 1
            player = copy.deepcopy(player_copy)
            enemy = copy.deepcopy(enemy_copy)
            battle += 1
            continue
        if faster_pokemon.can_attack is True:
            if faster_move['target'] == "Self":
                effect = eval(faster_move['effect'])
                effect(faster_pokemon)
            if faster_move['name'] == "Swift":
                swiftly(faster_pokemon, slower_pokemon)
            # Enters the recharge loop for moves like Dig and Hyper Beam
            recharging_loop(faster_pokemon, faster_move)
            if did_it_hit(faster_pokemon, faster_move, slower_pokemon) is True:
                # Handles moves that do the same amount of damage when used
                flat_damage(faster_pokemon, faster_move, slower_pokemon, slower_move)
                if faster_move['target'] == "Both":
                    effect = eval(faster_move['effect'])
                    effect(faster_pokemon, slower_pokemon)
                elif faster_move['target'] == "copied":
                    effect = eval(faster_move['effect'])
                    effect(faster_pokemon, faster_move, slower_pokemon)
                elif faster_move['target'] == "death":
                    slower_pokemon.hp = 0
                else:
                    # Handles consecutive-round attacks like Double Kick or Fury Swipes
                    attack_loop = how_many_attacks(faster_pokemon, faster_move)
                    while attack_loop > 0:
                        if faster_move['target'] == "thrash_it":
                            effect = eval(faster_move['effect'])
                            effect(faster_pokemon)
                        damage = damage_multiplier(faster_pokemon, faster_move, slower_pokemon)
                        slower_pokemon.hp -= damage
                        if slower_move['name'] == "Counter":
                            slower_pokemon.counter_attack = damage
                        if slower_move['name'] == "Bide":
                            if slower_pokemon.new_move == False:
                                if slower_pokemon.move_count > 0:
                                    slower_pokemon.counter_attack += damage
                        # User gains health for moves like Absorb
                        steal_health(faster_pokemon, faster_move, damage)
                        # User deals self-damage from moves like Take Down
                        self_inflicted(faster_pokemon, faster_move, damage)
                        if faster_move['name'] == "Rage":
                            faster_pokemon.new_move = False
                        # Effects for if Slower Pokemon is using Rage
                        getting_angry(slower_pokemon, slower_move)
                        slower_pokemon.took_damage = True
                        faster_pokemon.counter_attack = 0
                        attack_loop -= 1
                if faster_pokemon.hp <= 0 and slower_pokemon.hp <= 0:
                    player_draws += 1
                    enemy_draws += 1
                    player = copy.deepcopy(player_copy)
                    enemy = copy.deepcopy(enemy_copy)
                    battle += 1
                    continue
                if slower_pokemon.hp <= 0:
                    if player.hp <= 0:
                        enemy_wins += 1
                    if enemy.hp <= 0:
                        player_wins += 1
                    player = copy.deepcopy(player_copy)
                    enemy = copy.deepcopy(enemy_copy)
                    battle += 1
                    continue
                if faster_move['target'] == "Enemy":
                    effect = eval(faster_move['effect'])
                    effect(slower_pokemon)
            else:
                if faster_move['target'] == "kick":
                    faster_pokemon.hp -= 1
        faster_pokemon.can_attack = True
        # Effects for using Hyper Beam
        the_hb_effect(faster_pokemon, faster_move)
        # Handles a disabled move
        disabled_effects(faster_pokemon)
        # Handles moves with charging or skipping effects like Dig or Hyper Beam
        recharge_move_effects(faster_pokemon)
        # Check for reduction to damage effects
        defensive_check(faster_pokemon)
        # Tracks counters for moves
        move_counters(faster_pokemon)
        # If user uses Thrash, they become confused
        if faster_pokemon.move_count == 0 and faster_pokemon.thrash_mode is True:
            i_love_thrashing(faster_pokemon)
        # Check for damage effects like Burn, Poison, or Leech Seed
        status_check(faster_pokemon, slower_pokemon)
        if faster_pokemon.hp <= 0:
            if player.hp <= 0:
                enemy_wins += 1
            if enemy.hp <= 0:
                player_wins += 1
            player = copy.deepcopy(player_copy)
            enemy = copy.deepcopy(enemy_copy)
            battle += 1
            continue
# ******************************************************************************************************************** #
        # =======================SLOWER POKEMON ================================#
        # Check if flinched
        slower_pokemon.can_attack = flinch_check(slower_pokemon, faster_move)
        # Check frozen, sleep, confusion, paralysis
        status_effects(slower_pokemon, faster_pokemon)
        # ******************** Slower Pokemon Takes Turn ********************
        if slower_move['target'] == "copy":
            slower_move = faster_move
        if slower_move == slower_pokemon.disabled_move:
            slower_pokemon.can_attack = False
        if slower_move['name'] == "Bide":
            if slower_pokemon.new_move == False:
                if slower_pokemon.move_count > 0:
                    slower_pokemon.can_attack = False
                else:
                    damage = (slower_pokemon.counter_attack * 2)
                    faster_pokemon.hp -= damage
                    slower_pokemon.counter_attack = 0
                    slower_pokemon.new_move = True
                    slower_pokemon.can_attack = False
        if faster_pokemon.hp <= 0:
            if player.hp <= 0:
                enemy_wins += 1
            if enemy.hp <= 0:
                player_wins += 1
            player = copy.deepcopy(player_copy)
            enemy = copy.deepcopy(enemy_copy)
            battle += 1
            continue
        if slower_pokemon.can_attack is True:
            if slower_move['target'] == "Self":
                effect = eval(slower_move['effect'])
                effect(slower_pokemon)
            if slower_move['name'] == "Swift":
                swiftly(slower_pokemon, faster_pokemon)
            # Enters the recharge loop for moves like Dig and Hyper Beam
            recharging_loop(slower_pokemon, slower_move)
            if did_it_hit(slower_pokemon, slower_move, faster_pokemon) is True:
                # Handles moves that do the same amount of damage when used
                flat_damage(slower_pokemon, slower_move, faster_pokemon, faster_move)
                if slower_move['target'] == "Both":
                    effect = eval(slower_move['effect'])
                    effect(slower_pokemon, faster_pokemon)
                elif slower_move['target'] == "copied":
                    effect = eval(slower_move['effect'])
                    effect(slower_pokemon, slower_move, faster_pokemon)
                elif slower_move['target'] == "death":
                    faster_pokemon.hp = 0
                else:
                    # Handles consecutive-round attacks like Double Kick or Fury Swipes
                    attack_loop = how_many_attacks(slower_pokemon, slower_move)
                    while attack_loop > 0:
                        if slower_move['target'] == "thrash_it":
                            effect = eval(slower_move['effect'])
                            effect(slower_pokemon)
                        damage = damage_multiplier(slower_pokemon, slower_move, faster_pokemon)
                        faster_pokemon.hp -= damage
                        if faster_move['name'] == "Bide":
                            if faster_pokemon.move_count > 0:
                                faster_pokemon.counter_attack += damage
                        # User gains health for moves like Absorb
                        steal_health(slower_pokemon, slower_move, damage)
                        # User deals self-damage from moves like Take Down
                        self_inflicted(slower_pokemon, slower_move, damage)
                        if slower_move['name'] == "Rage":
                            slower_pokemon.new_move = False
                        # Effects for if Faster Pokemon is using Rage
                        getting_angry(faster_pokemon, faster_move)
                        faster_pokemon.took_damage = True
                        if slower_move['name'] == "Counter":
                            slower_pokemon.counter_attack = 0
                        attack_loop -= 1
                if faster_pokemon.hp <= 0 and slower_pokemon.hp <= 0:
                    player_draws += 1
                    enemy_draws += 1
                    player = copy.deepcopy(player_copy)
                    enemy = copy.deepcopy(enemy_copy)
                    battle += 1
                    continue
                if faster_pokemon.hp <= 0:
                    if player.hp <= 0:
                        enemy_wins += 1
                    if enemy.hp <= 0:
                        player_wins += 1
                    player = copy.deepcopy(player_copy)
                    enemy = copy.deepcopy(enemy_copy)
                    battle += 1
                    continue
                if slower_move['target'] == "Enemy":
                    effect = eval(slower_move['effect'])
                    effect(faster_pokemon)
            else:
                if slower_move['target'] == "kick":
                    slower_pokemon.hp -= 1
        slower_pokemon.can_attack = True
        # Effects for using Hyper Beam
        the_hb_effect(slower_pokemon, slower_move)
        # Handles a disabled move
        disabled_effects(slower_pokemon)
        # Handles moves with charging or skipping effects like Dig or Hyper Beam
        recharge_move_effects(slower_pokemon)
        # Check for reduction to damage effects
        defensive_check(slower_pokemon)
        # Tracks counters for moves
        move_counters(slower_pokemon)
        # If user uses Thrash, they become confused
        if slower_pokemon.move_count == 0 and slower_pokemon.thrash_mode is True:
            i_love_thrashing(slower_pokemon)
        # Check for damage effects like Burn, Poison, or Leech Seed
        status_check(slower_pokemon, faster_pokemon)
        if slower_pokemon.hp <= 0:
            if player.hp <= 0:
                enemy_wins += 1
            if enemy.hp <= 0:
                player_wins += 1
            player = copy.deepcopy(player_copy)
            enemy = copy.deepcopy(enemy_copy)
            battle += 1
            continue

win_percentage = (player_wins / 1000) * 100
print(f"You have a {win_percentage}% chance of winning.")