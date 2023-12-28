from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    game_started = models.BooleanField(default=False)
    game_over = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Game Name: " + str(self.name) + ", Created by: " + str(self.creator) + ", Started: " + str(
            self.game_started) + ", Game Over : " + str(self.game_over)


class Type(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    strength = models.IntegerField(default=0)
    weakness = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Role(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    start_hp = models.IntegerField(default=0)
    start_mp = models.IntegerField(default=0)
    start_attack = models.IntegerField(default=0)
    start_defense = models.IntegerField(default=0)
    start_myst_attack = models.IntegerField(default=0)
    start_myst_defense = models.IntegerField(default=0)
    start_speed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Gender(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class NPC(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Weapon(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    attack_mod = models.IntegerField(default=0)
    myst_attack_mod = models.IntegerField(default=0)
    speed_mod = models.IntegerField(default=0)
    mp_mod = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Armor(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    defense_mod = models.IntegerField(default=0)
    myst_defense_mod = models.IntegerField(default=0)
    speed_mod = models.IntegerField(default=0)
    hp_mod = models.IntegerField(default=0)
    mp_mod = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Ability(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    mp_cost = models.IntegerField(default=0)
    is_myst_attack = models.BooleanField(default=False)
    is_heal = models.BooleanField(default=False)
    is_aoe = models.BooleanField(default=False)
    is_buff = models.BooleanField(default=False)
    buff_hp_percent = models.FloatField(default=0)  # between 0 and 1
    buff_mp_percent = models.FloatField(default=0)  # between 0 and 1
    buff_attack_percent = models.FloatField(default=0)  # between 0 and 1
    buff_defense_percent = models.FloatField(default=0)  # between 0 and 1
    buff_myst_attack_percent = models.FloatField(default=0)  # between 0 and 1
    buff_myst_defense_percent = models.FloatField(default=0)  # between 0 and 1
    buff_speed_percent = models.FloatField(default=0)  # between 0 and 1
    min_amount = models.IntegerField(default=0)
    max_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class GameUser(models.Model):
    objects = models.Manager()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, default=None, blank=True, null=True
    )
    gender = models.ForeignKey(
        Gender, on_delete=models.PROTECT, default=None, blank=True, null=True
    )
    is_ready = models.BooleanField(default=False)
    current_hp = models.IntegerField(default=0)
    current_max_hp = models.IntegerField(default=0)
    current_mp = models.IntegerField(default=0)
    current_max_mp = models.IntegerField(default=0)
    current_attack = models.IntegerField(default=0)
    current_defense = models.IntegerField(default=0)
    current_myst_attack = models.IntegerField(default=0)
    current_myst_defense = models.IntegerField(default=0)
    current_speed = models.IntegerField(default=0)
    with_gear_hp = models.IntegerField(default=0)
    with_gear_mp = models.IntegerField(default=0)
    with_gear_attack = models.IntegerField(default=0)
    with_gear_defense = models.IntegerField(default=0)
    with_gear_myst_attack = models.IntegerField(default=0)
    with_gear_myst_defense = models.IntegerField(default=0)
    with_gear_speed = models.IntegerField(default=0)
    current_battle_act = models.IntegerField(null=True, blank=True)
    current_battle_number = models.IntegerField(null=True, blank=True)
    current_battle_starting_hp = models.IntegerField(null=True, blank=True)
    current_battle_starting_mp = models.IntegerField(null=True, blank=True)
    ability_1 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="ability_1",
    )
    ability_2 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="ability_2",
    )
    ability_3 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="ability_3",
    )
    ability_4 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="ability_4",
    )
    weapon_1 = models.ForeignKey(
        Weapon,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="weapon_1",
    )
    armor_1 = models.ForeignKey(
        Armor,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="armor_1",
    )
    armor_2 = models.ForeignKey(
        Armor,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="armor_2",
    )
    armor_3 = models.ForeignKey(
        Armor,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="armor_3",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_is_ready_field(self):
        if self.role is not None and self.gender is not None:
            self.is_ready = True
        else:
            self.is_ready = False

    def save(self, *args, **kwargs):
        self.update_is_ready_field()
        super().save(*args, **kwargs)

    def name(self):
        return self.user.username

    def image(self):
        return f"{self.role}-{self.gender}.png"

    def hp_percentage(self):
        return round((self.current_hp / self.current_max_hp) * 100)

    def mp_percentage(self):
        return round((self.current_mp / self.current_max_mp) * 100)

    def __str__(self):
        game_name = self.game.name if self.game else "Unknown Game"
        gameuser = self.name() if self.user else "Unknown User"
        role_name = self.role.name if self.role else "Unknown Role"

        return f"Game Name: {game_name}, GameUser Name: {gameuser}, Role: {role_name}"


class Dialogue(models.Model):
    objects = models.Manager()
    from_node_id = models.IntegerField(default=0)
    node_type = models.CharField(max_length=255)
    # talk     | player response | narration
    speaker = models.CharField(max_length=255)
    # npc name | Group Leader     | narator
    text = models.TextField()
    act = models.IntegerField(default=0)
    scene = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
                "from_node_id: "
                + str(self.from_node_id)
                + ", node_type: "
                + str(self.node_type)
                + ", speaker: "
                + str(self.speaker)
                + ", text: "
                + str(self.text)
        )


# running log of decision tree nodes that have been selected for each game
class GameDialogue(models.Model):
    objects = models.Manager()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    dialogue = models.ForeignKey(Dialogue, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "game: " + str(self.game) + ", dialogue: " + str(self.dialogue)


class Enemy(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    start_hp = models.IntegerField(default=0)
    start_attack = models.IntegerField(default=0)
    start_defense = models.IntegerField(default=0)
    start_myst_attack = models.IntegerField(default=0)
    start_myst_defense = models.IntegerField(default=0)
    start_speed = models.IntegerField(default=0)
    ability_1 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="enemy_ability_1",
    )
    ability_2 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="enemy_ability_2",
    )
    ability_3 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="enemy_ability_3",
    )
    ability_4 = models.ForeignKey(
        Ability,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="enemy_ability_4",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class GameEnemy(models.Model):
    objects = models.Manager()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    enemy = models.ForeignKey(Enemy, on_delete=models.PROTECT)
    act = models.IntegerField(default=0)
    battle = models.IntegerField(default=0)
    current_hp = models.IntegerField(default=0)
    current_attack = models.IntegerField(default=0)
    current_defense = models.IntegerField(default=0)
    current_myst_attack = models.IntegerField(default=0)
    current_myst_defense = models.IntegerField(default=0)
    current_speed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def name(self):
        return self.enemy.name

    def image(self):
        return self.enemy.image

    def hp_percentage(self):
        return round((self.current_hp / self.enemy.start_hp) * 100)

    def __str__(self):
        return f"Game Name: {self.game.name}, Enemy Name: {self.name()}, Act: {self.act}, Battle: {self.battle}"


class CombatLog(models.Model):
    objects = models.Manager()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    act = models.IntegerField(default=0)
    battle = models.IntegerField(default=0)
    gameuser = models.ForeignKey(
        GameUser, on_delete=models.PROTECT, related_name="combat_log_gameuser"
    )
    gameenemy = models.ForeignKey(
        GameEnemy, on_delete=models.PROTECT, default=None, blank=True, null=True
    )
    player_or_enemy_took_action = models.CharField(max_length=255)  # 'player' or 'enemy'
    defensive_gameuser_target = models.ForeignKey(
        GameUser,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        related_name="combat_log_defensive_gameuser_target",
    )
    ability = models.ForeignKey(Ability, on_delete=models.PROTECT)
    amount = models.IntegerField(default=0)
    damage_or_heal_or_buff = models.CharField(max_length=255)  # 'damage' or 'heal' or 'buff'
    message = models.TextField()
    starting_gameusers_json = models.JSONField()
    starting_gameenemies_json = models.JSONField()
    resulting_gameusers_json = models.JSONField()
    resulting_gameenemies_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        gameuser = self.gameuser.name() if self.gameuser else "Null"
        gameenemy = self.gameenemy.name() if self.gameenemy else "Null"
        defensive_gameuser_target = (
            self.defensive_gameuser_target.name()
            if self.defensive_gameuser_target
            else "Null"
        )
        return f"who: {self.player_or_enemy_took_action}, act: {self.act}, battle: {self.battle}, gameuser: {gameuser}, gameenemy: {gameenemy}, defensive_gameuser_target: {defensive_gameuser_target}, ability: {self.ability.name}, amount: {self.amount}, damage_or_heal_or_buff: {self.damage_or_heal_or_buff}"


class GameLocation(models.Model):
    objects = models.Manager()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    act = models.IntegerField(default=0)
    location_type = models.CharField(max_length=255)  # "scene" or "battle"
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game Name: {self.game.name}, act: {self.act}, location_type: {self.location_type}, number: {self.number}"


class GameTurnOrder(models.Model):
    objects = models.Manager()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    gameuser = models.ForeignKey(
        GameUser, on_delete=models.PROTECT, default=None, blank=True, null=True
    )
    gameenemy = models.ForeignKey(
        GameEnemy, on_delete=models.PROTECT, default=None, blank=True, null=True
    )
    is_their_turn = models.BooleanField(default=False)
    accum_speed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        gameuser = self.gameuser.name() if self.gameuser else "Null"
        gameenemy = self.gameenemy.name() if self.gameenemy else "Null"
        return f"game: {self.game.name}, gameuser: {gameuser}, gameenemy: {gameenemy}, is_their_turn: {self.is_their_turn}, accum_speed: {self.accum_speed}"


class SceneImage(models.Model):
    objects = models.Manager()
    act = models.IntegerField(default=0)
    scene = models.IntegerField(default=0)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scene image url: {self.image}, Act: {self.act}, Scene: {self.scene}"
