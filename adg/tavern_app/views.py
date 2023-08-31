from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from .forms import CreateGameForm, JoinGameForm, RoleAssignmentForm, GameDialogueForm, StartGameForm, CombatLogForm
from .models import Game, GameUser, Role, Gender, Dialogue, GameDialogue, NPC, Type, Weapon, Armor, Ability, Enemy, GameEnemy, CombatLog, GameScene
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.db.models import Count
from django.http import JsonResponse


def simple_view(request):
    return HttpResponse("LEEEROY JEEEEENKINS! LETS GOOOOOOO - David Lorenz & Jordan Philyaw - Hackathon May 2023")


def seed(request):
    if request.user.is_superuser == False:
        return redirect('tavern_app:home')

    # users are special because they get created with a hashed password with create_user
    user1 = User.objects.create_user(username='john', email='jlennon@beatles.com', password='imagine')
    user2 = User.objects.create_user(username='paul', email='pmccartney@beatles.com', password='let it be')
    user3 = User.objects.create_user(username='george', email='gharrison@beatles.com',password='my sweet lord')
    user4 = User.objects.create_user(username='ringo', email='rstarr@beatles.com', password='yellow submarine')
    user5 = User.objects.create_user(username='eleanor', email='erigby@beatles.com', password='lonely people')
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    user5.save()

    # games
    game1 = Game(name="Game Seed 1", creator=user1, game_started=False, game_over=False, password="apple")
    game2 = Game(name="Game Seed 2", creator=user2, game_started=False, game_over=False, password="banana")
    game3 = Game(name="Game Seed 3", creator=user3, game_started=False, game_over=False, password="carrot")
    game4 = Game(name="Game Seed 4", creator=user4, game_started=False, game_over=False, password="date")
    Game.objects.bulk_create([
        game1,
        game2,
        game3,
        game4,
    ])

    # types
    type1 = Type(name="Light", strength=2, weakness=5)
    type2 = Type(name="Dark", strength=3, weakness=1)
    type3 = Type(name="Stone", strength=4, weakness=2)
    type4 = Type(name="Forest", strength=5, weakness=3)
    type5 = Type(name="Wind", strength=1, weakness=4)
    type6 = Type(name="Normal", strength=6, weakness=6)
    Type.objects.bulk_create([
        type1,
        type2,
        type3,
        type4,
        type5,
        type6,
    ])

    # roles
    role1 = Role(name="WHITEMAGE", type=type1, start_hp=100, start_mp=100, start_attack=10, start_defense=20, start_myst_attack=15, start_myst_defense=20, start_speed=25)
    role2 = Role(name="BLACKMAGE", type=type2, start_hp=80, start_mp=120, start_attack=15, start_defense=10, start_myst_attack=35, start_myst_defense=10, start_speed=30)
    role3 = Role(name="PALADIN", type=type3, start_hp=120, start_mp=80, start_attack=20, start_defense=30, start_myst_attack=10, start_myst_defense=20, start_speed=20)
    role4 = Role(name="ARCHER", type=type4, start_hp=110, start_mp=90, start_attack=35, start_defense=15, start_myst_attack=10, start_myst_defense=10, start_speed=30)
    role5 = Role(name="BARD", type=type5, start_hp=90, start_mp=110, start_attack=20, start_defense=20, start_myst_attack=20, start_myst_defense=20, start_speed=20)
    Role.objects.bulk_create([
        role1,
        role2,
        role3,
        role4,
        role5,
    ])

    # genders
    gender1 = Gender(name="MALE")
    gender2 = Gender(name="FEMALE")
    Gender.objects.bulk_create([
        gender1,
        gender2,
    ])

    # weapons
    weapon1 = Weapon(name="Wood Staff", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon2 = Weapon(name="Wood Sword", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon3 = Weapon(name="Wood Bow", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon4 = Weapon(name="Wood Flute", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon5 = Weapon(name="Longsword", attack_mod=26, myst_attack_mod=12, speed_mod=10, mp_mod=12)
    weapon6 = Weapon(name="Longbow", attack_mod=26, myst_attack_mod=10, speed_mod=12, mp_mod=12)
    weapon7 = Weapon(name="Ivory Rod", attack_mod=10, myst_attack_mod=20, speed_mod=10, mp_mod=20)
    weapon8 = Weapon(name="Obsidian Wand", attack_mod=10, myst_attack_mod=22, speed_mod=10, mp_mod=18)
    weapon9 = Weapon(name="Melodious Lute", attack_mod=10, myst_attack_mod=20, speed_mod=12, mp_mod=18)
    weapon10 = Weapon(name="Holy Avenger", attack_mod=30, myst_attack_mod=25, speed_mod=15, mp_mod=20)
    weapon11 = Weapon(name="Shadowstrike", attack_mod=35, myst_attack_mod=15, speed_mod=20, mp_mod=20)
    weapon12 = Weapon(name="Divine Scepter", attack_mod=15, myst_attack_mod=30, speed_mod=15, mp_mod=30)
    weapon13 = Weapon(name="Voidcaller", attack_mod=15, myst_attack_mod=30, speed_mod=15, mp_mod=30)
    weapon14 = Weapon(name="Symphony Harp", attack_mod=15, myst_attack_mod=30, speed_mod=17, mp_mod=28)
    weapon15 = Weapon(name="Excalibur", attack_mod=45, myst_attack_mod=30, speed_mod=20, mp_mod=25)
    weapon16 = Weapon(name="Arbalest", attack_mod=53, myst_attack_mod=20, speed_mod=22, mp_mod=25)
    weapon17 = Weapon(name="Seraph's Wand", attack_mod=20, myst_attack_mod=40, speed_mod=20, mp_mod=40)
    weapon18 = Weapon(name="Ulrich Tome", attack_mod=20, myst_attack_mod=40, speed_mod=20, mp_mod=40)
    weapon19 = Weapon(name="Seranade Baton", attack_mod=20, myst_attack_mod=38, speed_mod=22, mp_mod=40)
    Weapon.objects.bulk_create([
        weapon1,
        weapon2,
        weapon3,
        weapon4,
        weapon5,
        weapon6,
        weapon7,
        weapon8,
        weapon9,
        weapon10,
        weapon11,
        weapon12,
        weapon13,
        weapon14,
        weapon15,
        weapon16,
        weapon17,
        weapon18,
        weapon19,
    ])

    # armor
    armor1 = Armor(name="Cloth Tunic", defense_mod=5, myst_defense_mod=5, speed_mod=5, hp_mod=5, mp_mod=5)
    armor2 = Armor(name="Steel Plate Armor", defense_mod=20, myst_defense_mod=20, speed_mod=10, hp_mod=15, mp_mod=10)
    armor3 = Armor(name="Leather Armor", defense_mod=15, myst_defense_mod=15, speed_mod=15, hp_mod=15, mp_mod=15)
    armor4 = Armor(name="Acolyte's Robes", defense_mod=18, myst_defense_mod=20, speed_mod=10, hp_mod=12, mp_mod=15)
    armor5 = Armor(name="Sorcerer's Robes", defense_mod=10, myst_defense_mod=20, speed_mod=15, hp_mod=10, mp_mod=20)
    armor6 = Armor(name="Harmonist's Cummerbund", defense_mod=10, myst_defense_mod=20, speed_mod=15, hp_mod=10, mp_mod=20)
    armor7 = Armor(name="Radiant Valor Plate", defense_mod=20, myst_defense_mod=25, speed_mod=15, hp_mod=30, mp_mod=23)
    armor8 = Armor(name="Elven Windwrap", defense_mod=20, myst_defense_mod=20, speed_mod=30, hp_mod=25, mp_mod=18)
    armor9 = Armor(name="Archmage's Vestments", defense_mod=25, myst_defense_mod=18, speed_mod=20, hp_mod=25, mp_mod=25)
    armor10 = Armor(name="Warlock's Cloak", defense_mod=25, myst_defense_mod=20, speed_mod=20, hp_mod=20, mp_mod=28)
    armor11 = Armor(name="Virtuoso's Ensemble", defense_mod=25, myst_defense_mod=20, speed_mod=23, hp_mod=20, mp_mod=25)
    armor12 = Armor(name="Divine Warplate", defense_mod=40, myst_defense_mod=40, speed_mod=20, hp_mod=30, mp_mod=20)
    armor13 = Armor(name="Galestrider Vest", defense_mod=35, myst_defense_mod=35, speed_mod=35, hp_mod=25, mp_mod=20)
    armor14 = Armor(name="Celestrial Regalia", defense_mod=25, myst_defense_mod=40, speed_mod=30, hp_mod=25, mp_mod=30)
    armor15 = Armor(name="Shadowweave Cape", defense_mod=20, myst_defense_mod=40, speed_mod=35, hp_mod=20, mp_mod=35)
    armor16 = Armor(name="Maestro's Tailcoat", defense_mod=20, myst_defense_mod=40, speed_mod=35, hp_mod=20, mp_mod=35)
    Armor.objects.bulk_create([
        armor1,
        armor2,
        armor3,
        armor4,
        armor5,
        armor6,
        armor7,
        armor8,
        armor9,
        armor10,
        armor11,
        armor12,
        armor13,
        armor14,
        armor15,
        armor16,
    ])

    # abilities
    ability1 = Ability(name="Attack", type=type6, mp_cost=0, threat=1, min_damage=1, max_damage=5)
    ability2 = Ability(name="Myst Attack Test", type=type6, mp_cost=3, myst_attack_flag=True, threat=1, min_damage=1, max_damage=4)
    ability3 = Ability(name="Reg Attack Test", type=type6, mp_cost=4, myst_attack_flag=False, threat=1, min_damage=1, max_damage=6)
    Ability.objects.bulk_create([
        ability1,
        ability2,
        ability3,
    ])

    # gameuser
    gameuser1 = GameUser(
        game=game1,
        user=user1,
        role=role1,
        gender=gender1,
        is_ready=True,
        current_hp=role1.start_hp,
        current_mp=role1.start_mp,
        current_attack=role1.start_attack,
        current_defense=role1.start_defense,
        current_myst_attack=role1.start_myst_attack,
        current_myst_defense=role1.start_myst_defense,
        current_speed=role1.start_speed,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
    )
    gameuser2 = GameUser(
        game=game1,
        user=user2,
        role=role2,
        gender=gender2,
        is_ready=True,
        current_hp=role2.start_hp,
        current_mp=role2.start_mp,
        current_attack=role2.start_attack,
        current_defense=role2.start_defense,
        current_myst_attack=role2.start_myst_attack,
        current_myst_defense=role2.start_myst_defense,
        current_speed=role2.start_speed,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
    )
    gameuser3 = GameUser(
        game=game1,
        user=user3,
        role=role3,
        gender=gender2,
        is_ready=True,
        current_hp=role3.start_hp,
        current_mp=role3.start_mp,
        current_attack=role3.start_attack,
        current_defense=role3.start_defense,
        current_myst_attack=role3.start_myst_attack,
        current_myst_defense=role3.start_myst_defense,
        current_speed=role3.start_speed,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
    )
    gameuser4 = GameUser(
        game=game1,
        user=user4,
        role=role4,
        gender=gender1,
        is_ready=True,
        current_hp=role4.start_hp,
        current_mp=role4.start_mp,
        current_attack=role4.start_attack,
        current_defense=role4.start_defense,
        current_myst_attack=role4.start_myst_attack,
        current_myst_defense=role4.start_myst_defense,
        current_speed=role4.start_speed,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
    )
    gameuser5 = GameUser(
        game=game2,
        user=user2,
        role=role2,
        gender=gender1,
        is_ready=True,
        current_hp=role2.start_hp,
        current_mp=role2.start_mp,
        current_attack=role2.start_attack,
        current_defense=role2.start_defense,
        current_myst_attack=role2.start_myst_attack,
        current_myst_defense=role2.start_myst_defense,
        current_speed=role2.start_speed,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
    )
    GameUser.objects.bulk_create([
        gameuser1,
        gameuser2,
        gameuser3,
        gameuser4,
        gameuser5,
    ])

    # npcs + images
    npc1 = NPC(name="Narrator", image="logo.png")
    npc2 = NPC(name="Old Man", image="old-man.png")
    npc3 = NPC(name="Drunk Man 1", image="drunk-man-1.png")
    npc4 = NPC(name="Drunk Man 2", image="drunk-man-2.png")
    npc5 = NPC(name="Hilda", image="hilda.png")
    NPC.objects.bulk_create([
        npc1,
        npc2,
        npc3,
        npc4,
        npc5,
    ])

    # Enemies
    # TODO https://trello.com/c/WUxbo4qF/153-create-all-enemies-and-add-them-to-database - in this ticket we'll update drunk men stats
    enemy1 = Enemy(
        name="Drunk Man 1",
        image="drunk-man-1.png",
        type=type1,
        start_hp=100,
        start_mp=99,
        start_attack=98,
        start_defense=97,
        start_myst_attack=96,
        start_myst_defense=95,
        start_speed=94,
        ability_1=ability1,
    )
    enemy2 = Enemy(
        name="Drunk Man 2",
        image="drunk-man-2.png",
        type=type2,
        start_hp=100,
        start_mp=99,
        start_attack=98,
        start_defense=97,
        start_myst_attack=96,
        start_myst_defense=95,
        start_speed=94,
        ability_1=ability1,
    )
    Enemy.objects.bulk_create([
        enemy1,
        enemy2,
    ])

    # GameEnemy
    gameenemy1 = GameEnemy(
        game=game1,
        enemy=enemy1,
        act=1,
        battle=1,
        current_hp=enemy1.start_hp,
        current_mp=enemy1.start_mp,
        current_attack=enemy1.start_attack,
        current_defense=enemy1.start_defense,
        current_myst_attack=enemy1.start_myst_attack,
        current_myst_defense=enemy1.start_myst_defense,
        current_speed=enemy1.start_speed,
    )
    gameenemy2 = GameEnemy(
        game=game1,
        enemy=enemy2,
        act=1,
        battle=1,
        current_hp=enemy2.start_hp,
        current_mp=enemy2.start_mp,
        current_attack=enemy2.start_attack,
        current_defense=enemy2.start_defense,
        current_myst_attack=enemy2.start_myst_attack,
        current_myst_defense=enemy2.start_myst_defense,
        current_speed=enemy2.start_speed,
    )
    GameEnemy.objects.bulk_create([
        gameenemy1,
        gameenemy2,
    ])

    # dialogue Act 1 Scene 1
    node1 = Dialogue(from_node_id=0, node_type="narration", speaker="Narrator", text="Your group finds themselves teleported to an abandoned alleyway in what looks like a quaint old village. The narrow passage is dimly lit, and the silence is broken by the distant sounds of chatter and laughter. Suddenly, two drunk men spot your group and stagger towards you, their eyes gleaming with mischief.", act=1, scene=1)
    node2 = Dialogue(from_node_id=1, node_type="talk", speaker="Drunk Man 1", text="Blimey, would ya look at this lot! Fancied themselves lost tourists, do they?", act=1, scene=1)
    node3 = Dialogue(from_node_id=2, node_type="talk", speaker="Drunk Man 2", text="Aven't seen faces like these 'round 'ere before!", act=1, scene=1)
    node4 = Dialogue(from_node_id=3, node_type="talk", speaker="Group Leader", text="We don't mean any harm. We're just passing through, gentlemen.", act=1, scene=1)
    node5 = Dialogue(from_node_id=4, node_type="talk", speaker="Drunk Man 1", text="Passin' through, eh? Not so fast! We don't get visitors often, so we might as well 'ave some fun with ya!", act=1, scene=1)
    node6 = Dialogue(from_node_id=5, node_type="talk", speaker="Group Leader", text="We don't want any trouble. We'll be on our way.", act=1, scene=1)
    node7 = Dialogue(from_node_id=6, node_type="talk", speaker="Drunk Man 2", text="Not so fast! You're stayin' put!", act=1, scene=1)
    node8 = Dialogue(from_node_id=7, node_type="talk", speaker="Old Man", text="Ey, what's all this ruckus?", act=1, scene=1)
    node9 = Dialogue(from_node_id=8, node_type="talk", speaker="Drunk Man 1", text="Stay out of this, old timer! These strangers are gonna get what's comin' to 'em!", act=1, scene=1)
    node10 = Dialogue(from_node_id=9, node_type="talk", speaker="Old Man", text="Now, now, lads. That's no way to treat our guests. Let 'em pass and be on their way.", act=1, scene=1)
    node11 = Dialogue(from_node_id=10, node_type="talk", speaker="Drunk Man 2", text="Fine, but they better not show their faces 'round here again!", act=1, scene=1)
    node12 = Dialogue(from_node_id=11, node_type="talk", speaker="Old Man", text="I apologize for their behavior. They can get a bit rowdy when they've 'ad a few too many. Please, come inside my tavern. You'll be safe there.", act=1, scene=1)
    node13 = Dialogue(from_node_id=12, node_type="talk", speaker="Group Leader", text="Thank you for your help. We'll gladly take shelter in your tavern.", act=1, scene=1)
    node14 = Dialogue(from_node_id=13, node_type="narration", speaker="Narrator", text="As your group hurries into the tavern, the old man closes the door behind you, shutting out the noise and tension from the alleyway.", act=1, scene=1)
    node15 = Dialogue(from_node_id=14, node_type="talk", speaker="Old Man", text="Sit, sit! Let me tell ya a tale of our plight. Evil creatures, they are. Taking control over our town, the last stronghold of good in our world. We need help, you see, from individuals not easily swayed by these beasts. And, it dawns on me, I believe you and your group might be the ones we've been waitin' for.", act=1, scene=1)
    node16 = Dialogue(from_node_id=15, node_type="talk", speaker="Group Leader", text="Us? Why us?", act=1, scene=1)
    node17 = Dialogue(from_node_id=16, node_type="talk", speaker="Old Man", text="Not entirely sure, my dear, but it seems fate has brought you here. We've been seekin' aid for a long time now, and you seem like a capable bunch. A band of mercenaries you ain't, but together, you make a good team.", act=1, scene=1)
    node18 = Dialogue(from_node_id=17, node_type="talk", speaker="Group Leader", text="How did we even end up in this village?", act=1, scene=1)
    node19 = Dialogue(from_node_id=18, node_type="talk", speaker="Old Man", text="Have another round, and I'll tell ya what I think. As for the 'how'... well, we're in a magical and mysterious place, ain't we? My guess is that you were brought here for a reason. The only way to defeat these creatures is with outside help, and you seem like the help we need.", act=1, scene=1)
    node20 = Dialogue(from_node_id=19, node_type="talk", speaker="Group Leader", text="Why now? Why did we end up here at this specific time?", act=1, scene=1)
    node21 = Dialogue(from_node_id=20, node_type="talk", speaker="Old Man", text="Time's runnin' out, I'm afraid. These creatures are changin', and it's not for the better. Other towns nearby have already felt their wrath. We're on the brink of losin' ourselves. You might just be our last hope.", act=1, scene=1)
    node22 = Dialogue(from_node_id=21, node_type="talk", speaker="Group Leader", text="But we're not warriors or fighters. We're {software developers}!", act=1, scene=1)
    node23 = Dialogue(from_node_id=22, node_type="talk", speaker="Old Man", text="Software developers, eh? I don't know much about that, but I believe you have somethin' within you. You'll find what you need to face this challenge. First things first, get a room upstairs in the tavern inn. In the morning, head to the general store and gather some equipment for your journey. You'll need it before you set off.", act=1, scene=1)
    
    # player decision
    node24 = Dialogue(from_node_id=23, node_type="player response", speaker="Group Leader", text="Book a night at the inn and see what tomorrow brings", act=1, scene=1)
    node25 = Dialogue(from_node_id=23, node_type="player response", speaker="Group Leader", text="Attempt to leave the tavern and try to get home", act=1, scene=1)
    node26 = Dialogue(from_node_id=23, node_type="player response", speaker="Group Leader", text="Continue to talk to the old man", act=1, scene=1)

    # node 24 Tree: Book a night at the inn and see what tomorrow brings
    node27 = Dialogue(from_node_id=24, node_type="talk", speaker="Group Leader", text="We've had quite a day. Maybe we should get some rest, see what tomorrow brings.", act=1, scene=1)
    node28 = Dialogue(from_node_id=27, node_type="talk", speaker="Group Member 1", text="It's been a lot to take in. A good night's rest might clear our heads.", act=1, scene=1)
    node29 = Dialogue(from_node_id=28, node_type="talk", speaker="Group Member 2", text="But what if we're really stuck here? We can't just wait around forever.", act=1, scene=1)
    node30 = Dialogue(from_node_id=29, node_type="talk", speaker="Group Leader", text="We'll keep our eyes and ears open. If there's a chance to find our way back, we'll take it. For now, let's book a night at the inn and regroup in the morning.", act=1, scene=1)
    node31 = Dialogue(from_node_id=30, node_type="narration", speaker="Narrator", text="As the group gets settled into their room above the tavern inn, they realize they have a window with a view into the very same alleyway they found themselves in earlier that evening.", act=1, scene=1)
    node32 = Dialogue(from_node_id=31, node_type="talk", speaker="Group Member 1", text="Hold on, everyone. Come take a look at this!", act=1, scene=1)
    node33 = Dialogue(from_node_id=32, node_type="talk", speaker="Group Member 2", text="What is it?", act=1, scene=1)
    node34 = Dialogue(from_node_id=33, node_type="talk", speaker="Group Member 1", text="It's the exact spot where we found ourselves transported! There's a weird glimmer in the air. I think we should investigate.", act=1, scene=1)
    node35 = Dialogue(from_node_id=34, node_type="talk", speaker="Group Leader", text="You're right. It's worth checking out. Let's head over there and see if we can find any clues.", act=1, scene=1)

    # node 25 Tree: Attempt to leave the tavern and try to get home
    node36 = Dialogue(from_node_id=25, node_type="talk", speaker="Group Member 1", text="We can't just sit around here hoping for answers. We need to go back to where we entered this place and look for clues. Maybe we'll find a way back home.", act=1, scene=1)
    node37 = Dialogue(from_node_id=36, node_type="talk", speaker="Group Member 2", text="I agree. It's worth a shot. We should at least try to retrace our steps.", act=1, scene=1)
    node38 = Dialogue(from_node_id=37, node_type="talk", speaker="Group Leader", text="Alright, it's settled then. Let's head back to the alley and see if we can find any clues.", act=1, scene=1)

    # node 26 Tree: Continue to talk to the old man
    node39 = Dialogue(from_node_id=26, node_type="narration", speaker="Narrator", text="The group debates their options, torn between waiting for answers and seeking a way back home. They turn back to the old man and he is passed out under the table.", act=1, scene=1)
    node40 = Dialogue(from_node_id=39, node_type="talk", speaker="Group Member 1", text="I think he's had a bit too much to drink. Maybe we should leave him be for now.", act=1, scene=1)
    node41 = Dialogue(from_node_id=40, node_type="talk", speaker="Group Leader", text="Agreed. Let's try to figure this out on our own for now.", act=1, scene=1)

    # 3 options lead to same choice
    node42 = Dialogue(from_node_id=35, node_type="narration", speaker="Narrator", text="They open the door to the tavern to leave and sense an unusual change in the air. Something inside them feels different—strength, confidence, or something else they can't quite grasp.", act=1, scene=1)
    node43 = Dialogue(from_node_id=38, node_type="narration", speaker="Narrator", text="They open the door to the tavern to leave and sense an unusual change in the air. Something inside them feels different—strength, confidence, or something else they can't quite grasp.", act=1, scene=1)
    node44 = Dialogue(from_node_id=41, node_type="narration", speaker="Narrator", text="They open the door to the tavern to leave and sense an unusual change in the air. Something inside them feels different—strength, confidence, or something else they can't quite grasp.", act=1, scene=1)

    # continuation of story from node 42
    node45 = Dialogue(from_node_id=42, node_type="talk", speaker="Group Leader", text="Do you guys feel that too? It's like there's something... different.", act=1, scene=1)
    node46 = Dialogue(from_node_id=45, node_type="talk", speaker="Group Member 1", text="Yeah, it's strange. I can't quite put my finger on it.", act=1, scene=1)
    node47 = Dialogue(from_node_id=46, node_type="talk", speaker="Group Member 2", text="Well, whatever it is, let's stay alert. We don't know what's out there.", act=1, scene=1)
    node48 = Dialogue(from_node_id=47, node_type="talk", speaker="Drunk Man 1", text="Look who's back for another beating!", act=1, scene=1)
    node49 = Dialogue(from_node_id=48, node_type="talk", speaker="Drunk Man 2", text="We warned ya to stay away!", act=1, scene=1)
    node50 = Dialogue(from_node_id=49, node_type="talk", speaker="Group Leader", text="We've had enough of this. Let's just take these guys out.", act=1, scene=1)

    # continuation of story from node 43
    node51 = Dialogue(from_node_id=43, node_type="talk", speaker="Group Leader", text="Do you guys feel that too? It's like there's something... different.", act=1, scene=1)
    node52 = Dialogue(from_node_id=51, node_type="talk", speaker="Group Member 1", text="Yeah, it's strange. I can't quite put my finger on it.", act=1, scene=1)
    node53 = Dialogue(from_node_id=52, node_type="talk", speaker="Group Member 2", text="Well, whatever it is, let's stay alert. We don't know what's out there.", act=1, scene=1)
    node54 = Dialogue(from_node_id=53, node_type="talk", speaker="Drunk Man 1", text="Look who's back for another beating!", act=1, scene=1)
    node55 = Dialogue(from_node_id=54, node_type="talk", speaker="Drunk Man 2", text="We warned ya to stay away!", act=1, scene=1)
    node56 = Dialogue(from_node_id=55, node_type="talk", speaker="Group Leader", text="We've had enough of this. Let's just take these guys out.", act=1, scene=1)

    # continuation of story from node 44
    node57 = Dialogue(from_node_id=44, node_type="talk", speaker="Group Leader", text="Do you guys feel that too? It's like there's something... different.", act=1, scene=1)
    node58 = Dialogue(from_node_id=57, node_type="talk", speaker="Group Member 1", text="Yeah, it's strange. I can't quite put my finger on it.", act=1, scene=1)
    node59 = Dialogue(from_node_id=58, node_type="talk", speaker="Group Member 2", text="Well, whatever it is, let's stay alert. We don't know what's out there.", act=1, scene=1)
    node60 = Dialogue(from_node_id=59, node_type="talk", speaker="Drunk Man 1", text="Look who's back for another beating!", act=1, scene=1)
    node61 = Dialogue(from_node_id=60, node_type="talk", speaker="Drunk Man 2", text="We warned ya to stay away!", act=1, scene=1)
    node62 = Dialogue(from_node_id=61, node_type="talk", speaker="Group Leader", text="We've had enough of this. Let's just take these guys out.", act=1, scene=1)

    Dialogue.objects.bulk_create([
        node1,
        node2,
        node3,
        node4,
        node5,
        node6,
        node7,
        node8,
        node9,
        node10,
        node11,
        node12,
        node13,
        node14,
        node15,
        node16,
        node17,
        node18,
        node19,
        node20,
        node21,
        node22,
        node23,
        node24,
        node25,
        node26,
        node27,
        node28,
        node29,
        node30,
        node31,
        node32,
        node33,
        node34,
        node35,
        node36,
        node37,
        node38,
        node39,
        node40,
        node41,
        node42,
        node43,
        node44,
        node45,
        node46,
        node47,
        node48,
        node49,
        node50,
        node51,
        node52,
        node53,
        node54,
        node55,
        node56,
        node57,
        node58,
        node59,
        node60,
        node61,
        node62,
    ])

    return render(request, 'seed.html')

def live_update_prototype(request):
    games = Game.objects.all()
    return JsonResponse({"games":list(games.values())})

def live_update_prototype_view(request):
    context = {
        'games': Game.objects.all()
    }
    return render(request, 'liveupdateprototype.html', context)

def live_update_prototype_redirect_view(request):
    context = {
        'gameCount': Game.objects.all().count()
    }
    return render(request, 'liveupdateprototyperedirect.html', context)

class CreateOrJoinView(TemplateView):
    template_name = "tavern_app/home.html"

class GameView(ListView):
    model = Game
    template_name = 'tavern_app/games.html'
    queryset = Game.objects.annotate(num_players=Count('gameuser'))
    context_object_name = 'games'

class GameDetailView(FormMixin, DetailView):
    model = Game
    template_name = 'tavern_app/game_detail.html'
    form_class = JoinGameForm

    # TODO https://trello.com/c/tkGuaIp0/114-add-validation-to-all-forms-views
    # TODO if user is already in the game, redirect them to the lobby
    # TODO if user is not logged in, redirect them to login page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Must be logged in to join a game.', extra_tags="alert alert-danger")
            return self.form_invalid(form)
            
        game = self.get_object()
        password = form.cleaned_data.get('password')
        if password == game.password:
            existing_game_user = GameUser.objects.filter(user_id=self.request.user, game_id=game).exists()
            if existing_game_user:
                pass
            else:
                # Add the user to the GameUser table
                GameUser.objects.create(user=self.request.user, game=game)
            return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))
        else:
            messages.error(self.request, 'Incorrect password. Please try again.', extra_tags="alert alert-danger")
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def lobby(request, game_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to see a game.', extra_tags="alert alert-danger")
        return redirect('login')
    
    if GameUser.objects.filter(user_id=request.user, game_id=game_id).exists() == False:
        messages.error(request, 'Must be in the game to see it.', extra_tags="alert alert-danger")
        return redirect('tavern_app:games')
    
    game = Game.objects.get(id=game_id)
    gameusers = GameUser.objects.filter(game_id=game_id)
    is_leader = True if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user else False
    any_player_not_ready = gameusers.filter(is_ready=False).exists()
    num_players_in_lobby = gameusers.count()

    if game.game_started == True:
        gamescene = GameScene.objects.get(game=game)
        return redirect(reverse("tavern_app:" + gamescene.scene_type, kwargs={'game_id': game.id, 'act': gamescene.act, 'scene': gamescene.scene}))

    if request.method == 'POST':
        form = StartGameForm(request.POST)
        has_error = False

        if form.is_valid():
            if any_player_not_ready == True:
                messages.error(request, 'All players must be ready to start the game.', extra_tags="alert alert-danger")
                has_error = True

            if game.creator != request.user:
                messages.error(request, 'Game can only be started by party leader.', extra_tags="alert alert-danger")
                has_error = True

            if num_players_in_lobby != 4:
                messages.error(request, 'Game can only be started with 4 players.', extra_tags="alert alert-danger")
                has_error = True

            if has_error:
                return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game_id}))

            # Write first dialogue node for this game, populate game enemies, game_started True
            starting_game_dialogue = GameDialogue(game=game, dialogue=Dialogue.objects.get(pk=1))
            starting_game_dialogue.save()

            # TODO improve later: query all enemies and loop through adding them all into the game
            enemy1 = Enemy.objects.get(pk=1)
            enemy2 = Enemy.objects.get(pk=2)
            gameenemy1 = GameEnemy(
                game=game,
                enemy=enemy1,
                act=1,
                battle=1,
                current_hp=enemy1.start_hp,
                current_mp=enemy1.start_mp,
                current_attack=enemy1.start_attack,
                current_defense=enemy1.start_defense,
                current_myst_attack=enemy1.start_myst_attack,
                current_myst_defense=enemy1.start_myst_defense,
                current_speed=enemy1.start_speed,
            )
            gameenemy2 = GameEnemy(
                game=game,
                enemy=enemy2,
                act=1,
                battle=1,
                current_hp=enemy2.start_hp,
                current_mp=enemy2.start_mp,
                current_attack=enemy2.start_attack,
                current_defense=enemy2.start_defense,
                current_myst_attack=enemy2.start_myst_attack,
                current_myst_defense=enemy2.start_myst_defense,
                current_speed=enemy2.start_speed,
            )
            GameEnemy.objects.bulk_create([
                gameenemy1,
                gameenemy2,
            ])

            game.game_started = True
            game.save()

            gamescene = GameScene(game=game, act=1, scene_type="scene", scene=1)
            gamescene.save()

            return redirect(reverse("tavern_app:" + gamescene.scene_type, kwargs={'game_id': game.id, 'act': gamescene.act, 'scene': gamescene.scene}))

        else:
            messages.error(request, 'Something in the form was not valid.', extra_tags="alert alert-danger")
            return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))
            
    else:
        form = StartGameForm(initial={'game_id': game_id})

    context = {
        'game': game,
        'gameusers': gameusers,
        'is_leader': is_leader,
        'any_player_not_ready': any_player_not_ready,
        'num_players_in_lobby': num_players_in_lobby,
        'form': form,
    }
    
    return render(request, 'tavern_app/lobby.html', context)    

class CreateGameView(CreateView):
    model = Game
    template_name = 'tavern_app/create_game.html'
    form_class = CreateGameForm

    def form_valid(self, form):
        game = form.save(commit=False)
        game.creator = self.request.user
        game.save()

        # Add the user who created the game to the gameuser table
        GameUser.objects.create(user=self.request.user, game=game)

        return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))


class RoleAssignmentView(FormView):
    template_name = 'tavern_app/role_assignment.html'
    form_class = RoleAssignmentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['game_id'] = self.kwargs['game_id']
        kwargs['num_players'] = GameUser.objects.filter(game_id=self.kwargs['game_id']).count()
        return kwargs

    def form_valid(self, form):
        game = Game.objects.get(pk=self.kwargs['game_id'])
        num_players = form.initial['num_players']

        for i in range(1, num_players + 1):
            player_name = form.cleaned_data[f'player_{i}_name']
            player_role = form.cleaned_data[f'player_{i}_role']
            player_gender = form.cleaned_data[f'player_{i}_gender']

            player = GameUser.objects.get(game=game, user__username=player_name)

            player.role = player_role
            player.gender = player_gender

            player.current_hp = player.role.start_hp
            player.current_mp = player.role.start_mp
            player.current_attack = player.role.start_attack
            player.current_defense = player.role.start_defense
            player.current_myst_attack = player.role.start_myst_attack
            player.current_myst_defense = player.role.start_myst_defense
            player.current_speed = player.role.start_speed

            player.save()

        return super().form_valid(form)

    def get_success_url(self):
        game_id = self.kwargs['game_id']
        return reverse('tavern_app:lobby', kwargs={'game_id': game_id})

def scene(request, game_id, act, scene):
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to see a game.', extra_tags="alert alert-danger")
        return redirect('login')
    
    if GameUser.objects.filter(user_id=request.user, game_id=game_id).exists() == False:
        messages.error(request, 'Must be in the game to see it.', extra_tags="alert alert-danger")
        return redirect('tavern_app:games')
    
    # bool: is current user the party leader
    game = Game.objects.get(pk=game_id)
    is_leader = True if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user else False

    # form submission if game owner clicked next button or dialogue option
    if request.method == 'POST':
        form = GameDialogueForm(request.POST)

        if form.is_valid():
            # get the next dialogue from form values and write to db
            game = Game.objects.get(pk=game_id)
            dialogue = Dialogue.objects.get(pk=form.cleaned_data['dialogue'].id)

            # make sure submission is valid
            latest_game_dialogue_id = GameDialogue.objects.filter(game=game).latest('id').dialogue.id
            if dialogue.from_node_id != latest_game_dialogue_id:
                messages.error(request, 'Invalid dialogue choice. Must be connected to previous dialogue.', extra_tags="alert alert-danger")
                return redirect(reverse("tavern_app:scene", kwargs={'game_id': game_id, 'act': act, 'scene': scene}))
            
            if is_leader == False:
                messages.error(request, 'Only the party leader can progress dialogue.', extra_tags="alert alert-danger")
                return redirect(reverse("tavern_app:scene", kwargs={'game_id': game_id, 'act': act, 'scene': scene}))

            game_dialogue = GameDialogue(game=game, dialogue=dialogue)
            game_dialogue.save()

    # else render form
    else:
        form = GameDialogueForm()

    # character_list combines players and npcs into a single list that can later be used to add names and images to dialogues
    character_list = []
    game_users = GameUser.objects.filter(game=game)
    
    # in dialogue we save speakers as "Group Leader" or "Group Member 1"
    # at run time compare those against players in the game so we can display the player username
    for idx, game_user in enumerate(game_users):
        speaker = ""
        if idx == 0:
            speaker = "Group Leader"
        elif idx == 1:
            speaker = "Group Member 1"
        elif idx == 2:
            speaker = "Group Member 2"
        character_list.append({'name': game_user.user.username, 'image': game_user.image(), 'speaker': speaker})

    npcs = NPC.objects.all()
    for npc in npcs:
        character_list.append({'name': npc.name, 'image': npc.image, 'speaker': npc.name})
        
    # game_dialogue_progress_list is the current game's dialogue + names and images
    game_dialogue_progress_list = []
    game_dialogue_progress = GameDialogue.objects.filter(game=game_id)
    for game_dialogue in game_dialogue_progress:
        # only build the list for the current act and scene
        if game_dialogue.dialogue.act == act and game_dialogue.dialogue.scene == scene:
            name = ""
            image = ""
            for char in character_list:
                if char['speaker'] == game_dialogue.dialogue.speaker:
                    name = char['name']
                    image = char['image']
            
            game_dialogue_progress_list.append({
                'id': game_dialogue.dialogue.pk,
                'node_type': game_dialogue.dialogue.node_type,
                'name': name,
                'text': game_dialogue.dialogue.text,
                'image': image,
                })
        
    # next_dialogue_list queries the game dialogue progress for the next single dialogue or multiple player dialogue choices
    next_dialogue_list = []
    # make sure this act/scene has at least 1 node to prevent errors. filter by act and scene.
    if len(game_dialogue_progress_list) > 0:
        next_dialogue = Dialogue.objects.filter(from_node_id=game_dialogue_progress_list[-1]['id'], act=act, scene=scene)
        for dialogue in next_dialogue:
            name = ""
            image = ""
            for char in character_list:
                if char['speaker'] == dialogue.speaker:
                    name = char['name']
                    image = char['image']
            
            next_dialogue_list.append({
                'id': dialogue.pk,
                'from_node_id': dialogue.from_node_id,
                'node_type': dialogue.node_type,
                'name': name,
                'text': dialogue.text,
                'image': image,
                })
        
    # TODO https://trello.com/c/oL6acc6m/127-end-of-act-1-scene-1-final-button-goes-to-battle

    context = {
        'game_id': game_id,
        'game_dialogue_progress_list': game_dialogue_progress_list,
        'next_dialogue_list': next_dialogue_list,
        'form': form,
        'is_leader': is_leader,
    }

    return render(request, 'tavern_app/scene.html', context)

# TODO This entire view is Work in Progress purely for testing. Will be lots of upcoming cleanup.
def act1_battle1(request, game_id):

    if request.method == 'POST':
        form = CombatLogForm(request.POST)

        if form.is_valid():
            # TODO adjust to handle AOE abilities where mulitiple enemies are hit
            print("form submitted")
            player = GameUser.objects.get(game_id=game_id, user=request.user)
            enemy = GameEnemy.objects.get(game_id=game_id, enemy=Enemy(form.cleaned_data['enemy'].id))
            ability = Ability.objects.get(pk=form.cleaned_data['ability'].id)
            game = Game.objects.get(pk=game_id)
            print("player is:")
            print(player)
            print("enemy is:")
            print(enemy)
            print("ability is:")
            print(ability)
            print("ability min damage is " + str(ability.min_damage) + " and max damage is " + str(ability.max_damage))
           
            combat_log = CombatLog(
                game = game,
                player = player.user,
                enemy = enemy.enemy,
                player_or_enemy_took_action = "player",
                ability = ability,
                damage = ability.max_damage, # for testing do the max damage. will update later
                unit_previous_hp = enemy.current_hp,
                unit_resulting_hp = enemy.current_hp - ability.max_damage,
                ability_mp_cost = ability.mp_cost,
                unit_previous_mp = player.current_mp,
                unit_resulting_mp = player.current_mp - ability.mp_cost,
                ability_min_damage = ability.min_damage,
                ability_max_damage = ability.max_damage,
            )
            combat_log.save()

            enemy.current_hp = enemy.current_hp - ability.max_damage
            enemy.save()

            player.current_mp = player.current_mp - ability.mp_cost
            player.save()


    # else render form
    else:
        form = CombatLogForm()

    game = Game.objects.get(pk=game_id)
    is_leader = True if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user else False

    gameusers = GameUser.objects.filter(game_id=game_id)
    gameenemies = GameEnemy.objects.filter(game_id=game_id)

    player = GameUser.objects.get(game_id=game_id, user=request.user)

    combat_log_for_debug_display = CombatLog.objects.filter(game=game)

    context = {
        'game_id': game_id,
        'is_leader': is_leader,
        'gameusers': gameusers,
        'gameenemies': gameenemies,
        'form': form,
        'combat_log_for_debug_display': combat_log_for_debug_display,
        'player': player,
    }

    return render(request, 'tavern_app/act1/act1_battle1.html', context)
