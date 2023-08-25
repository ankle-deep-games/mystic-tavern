from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    game_started = models.BooleanField(default=False)
    game_over = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Game Name: ' + str(self.name) + ', Created by: ' + str(self.creator)


class Type(models.Model):
    name = models.CharField(max_length=255)
    strength = models.IntegerField(default=0)
    weakness = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Role(models.Model):
    name = models.CharField(max_length=255)
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
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class NPC(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Weapon(models.Model):
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
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    mp_cost = models.IntegerField(default=0)
    myst_attack_flag = models.BooleanField(default=False)
    threat = models.IntegerField(default=0)
    min_damage = models.IntegerField(default=0)
    max_damage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class GameUser(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=None, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, default=None, blank=True, null=True)
    is_ready = models.BooleanField(default=False)
    current_hp = models.IntegerField(default=0)
    current_mp = models.IntegerField(default=0)
    current_attack = models.IntegerField(default=0)
    current_defense = models.IntegerField(default=0)
    current_myst_attack = models.IntegerField(default=0)
    current_myst_defense = models.IntegerField(default=0)
    current_speed = models.IntegerField(default=0)
    ability_1 = models.ForeignKey(Ability, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='ability_1')
    ability_2 = models.ForeignKey(Ability, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='ability_2')
    ability_3 = models.ForeignKey(Ability, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='ability_3')
    weapon_1 = models.ForeignKey(Weapon, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='weapon_1')
    weapon_2 = models.ForeignKey(Weapon, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='weapon_2')
    weapon_3 = models.ForeignKey(Weapon, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='weapon_3')
    armor_1 = models.ForeignKey(Armor, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='armor_1')
    armor_2 = models.ForeignKey(Armor, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='armor_2')
    armor_3 = models.ForeignKey(Armor, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='armor_3')
    current_gold = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_is_ready_field(self):
        if self.role is not None and self.gender is not None:
            self.is_ready = True
        else:
            self.is_ready = False

    def update_stats_from_role(self):
        if self.role:
            self.current_hp = self.role.start_hp
            self.current_mp = self.role.start_mp
            self.current_attack = self.role.start_attack
            self.current_defense = self.role.start_defense
            self.current_myst_attack = self.role.start_myst_attack
            self.current_myst_defense = self.role.start_myst_defense
            self.current_speed = self.role.start_speed

    def save(self, *args, **kwargs):
        self.update_is_ready_field()
        self.update_stats_from_role()
        super().save(*args, **kwargs)

    def image(self):
        return f'{self.role}-{self.gender}.png'

    def __str__(self):
        game_name = self.game.name if self.game else 'Unknown Game'
        username = self.user.username if self.user else 'Unknown User'
        role_name = self.role.name if self.role else 'Unknown Role'

        return f'Game Name: {game_name}, Player: {username}, Role: {role_name}'


class Dialogue(models.Model):
    from_node_id = models.IntegerField(default=0)
    node_type = models.CharField(max_length=255)
    # talk     | player response | narration
    speaker = models.CharField(max_length=255)
    # npc name | Group Leader     | narator
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'from_node_id: ' + str(self.from_node_id) + ', node_type: ' + str(self.node_type) + ', speaker: ' + str(self.speaker) + ', text: ' + str(self.text)

# running log of decision tree nodes that have been selected for each game
class GameDialogue(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    dialogue = models.ForeignKey(Dialogue, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'game: ' + str(self.game) + ', dialogue: ' + str(self.dialogue)


class Enemy(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    hp = models.IntegerField(default=0)
    mp = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    myst_attack = models.IntegerField(default=0)
    myst_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    ability_1 = models.ForeignKey(Ability, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='enemy_ability_1')
    ability_2 = models.ForeignKey(Ability, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='enemy_ability_2')
    ability_3 = models.ForeignKey(Ability, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='enemy_ability_3')
    ability_4 = models.ForeignKey(Ability, on_delete=models.PROTECT, default=None, blank=True, null=True, related_name='enemy_ability_4')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
