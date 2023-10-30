## How scene works

Game leader loads the page from backend template html response.

When they post, they get a json response in return showing them the game update.

Other players load the same page as the party leader from the backend template html response. They get game updates by polling a separate route to get the latest state from the DB and immediately replacing the 3 dialogue nodes with the latest 3 in the db. This also checks to see if they should be rerouted to the next url and returns that in `new_url` in the json response.

This means they only get the html response on first page load, everything after that is javascript in the form of json responses.

## How is battle similiar and different?

### similar
Want to use polling to update the page based on polling data.

### different
There are now 4 players who can POST - not just the party leader. This means that the party leader also has to keep in sync with the others.

All 4 will have to poll from another route.

The reason we need another route is because the battle view needs to establish the base data if any player were to refresh their browser or get redirected to that battle page. They need fresh db data in both cases there.

There is also a lot more to keep track of than just latest 3 dialogue nodes.

There is:
- Each enemy health

- Each player HP
- Each player MP

- What move the enemy just cast. Who they targeted and how much damage they did. Both single target and AOE.

- What move the player just cast. Who they targeted and how much damage they did. Or how much they healed. Or what buff they cast. 

- We also want to display whose turn it is while waiting for others to progress.
    - Players waiting for them by name
    - Enemies if they go more than once happen immediately in the DB, but need to give the sense to players that they have happened individually with delays of progress.

- Need to display if move was not very effective or very effective.


## how to handle Single target vs AOE game progress text
- Enemy single targets: Drunk Man 1 hit John with Bar Punch for 5 damage. It was very effective.
- Enemy muliti targets. Drunk Man 1 hit John with Bar punch for 5 damage. It was very effective \n Drunk Man 1 hit George for 7 damage. It was not very effective.

Leaning towards AOEs need to loop and be individual because that way we can say if they were effective or not. And it helps by keeping each combat log entry different. If we don't do this, the dialogue could become too long and especially for mobile it wouldn't all fit nicely onto the screen in a specified game combat message center.

- Player single targets enemy: John hit Drunk Man 2 with Divine Light for 15 damage. It was not very effective.
- Player multi target damages: John hit Drunk Man 2 with Divine Light for 15 damage. It was not very effective. \n John hit Drunk Man 1 with Divine Light for 23 damage. It was very effective.

- Player single target heals player: John heals George for 15 with Divine Prayer.
- Player aoe heals: John heals George for 15 with Divine Prayer. \n John heals Paul for 17 with Divine Prayer.

- Player single target buffs: John buffs George with Divine Blessing, increasing attack and defense. (do some fancy stuff in the combat log where we log how they were buffed)
- Player aoe buffs: John buffs George with Divine Blessing, increasing attack and defense. \n John buffs Paul with Divine Blessing, increasing attack and defense.

How do we warn players they can't be double buffed?

## how to structure the json responses
Considerations:
- the previous state of enemy and player hp/mp.
- the next state of enemy and player hp/mp.
- what single target OR AOE was cast. Who attacked, who was targeted, how much damage/heal/buff. Resulting hp/mp of everyone.
- Need to be able to stack multiple responses because enemies could go twice in a row.

When someone refreshes the page, just get the current game state. But what happens if an enemy goes first? We need the initial state before the enemy attacked so we can display the change.

One page load, could have `starting state` and `resulting state`. If they are different in any way, go through the animation process. If they are the same, display whose turn it is to all other players, and for player whose turn it is present them their battle options.


```
{
    starting_state: {
        gameenemies: {
            id: {
                name: 'Drunk Man 1',
                hp: 85,
                max_hp: 100,
            },
            id: {
                name: 'Drunk Man 2',
                hp: 72,
                max_hp: 100,
            },
        },
        gameusers: {
            id: {
                name: 'John',
                hp: 100,
                max_hp: 120,
                with_gear_hp: 120,
                mp: 100,
                max_mp: 120,
                with_gear_mp: 120,
            },
            id: {
            },
            id: {
            },
            id: {
            },
        }
    },
    resulting_states: { // is this an array of all states that have passed?
        [
            combat_log_message: 'John hit Drunk Man 1 with Divine Light for 10 damage. It was not very effective.',
            gameenemies: {
                id: {
                    name: 'Drunk Man 1',
                    hp: 75,
                    max_hp: 100,
                },
                id: {
                    name: 'Drunk Man 2',
                    hp: 72,
                    max_hp: 100,
                },
            },
            gameusers: {
                id: {
                    name: 'John',
                    hp: 100,
                    max_hp: 120,
                    with_gear_hp: 120,
                    mp: 100,
                    max_mp: 120,
                    with_gear_mp: 120,
                },
                id: {
                },
                id: {
                },
                id: {
                },
            },
            next_turn: {
                name: 'John',
                gameuserid: id,
                gameenemyid: NULL,
            }
        ]
    }
}
```

The players query for the battle_get_updates. They need to get recent updates since the latest request. But not repeat updates they've already executed on the front end.

Let's say this was a long array of every progress in the battle so far with each combat log mesage and every change that went along with it. For one I'm not storing all the resulting states every time. I'm storing a combat log of the text change with some data of gameuser/gameenemy and amount. And then I'm storing the existing state of every gameenemy and gameuser. So how would I keep track of all the changes over time?

Need to avoid doubling up on exectuing any game change. A game change on the frontend can happen only once when there is a change to make.

I either store the combat log message AND the resulting change in the JSON response, or I calculate the resulting changes on the FE. It seems like the better approach to calculate everything on the backend and make the front end as dumb as possible. Just a calculation to say hey at this stage when we're displaying the combat text of what happened - if anything is different, animate that change. Will reference what I did on the pokemon change to make that a gradual reduction or increase when something has changed.

Does the combat log need to be more robust? Should it store the JSON of complete changes?

Also need to account for combat log being tied to a specific act and battle number. That could be its own ticket. Otherwise how will I know which combat log to display?

So right now I can show a django message of what has happened. How much a enemy attacked for and how much a player attacked for. But those are showing the numbers only and the calculation of what is happening for everyone is handled by the backend because we're doing a fresh page reload to get the current state, which happens to line up with what has just happened. But that paradigm will change.

Another idea is each combat log stores the previous state and the resulting new state only. If I did that - I could step through each combat log one by one and display the text change and the change to hp/mp. I like this approach because it seems best to display AOE one line at a time for the sake of the front end not showing too much at once. So the combat log as only `previous_state` and `resulting_state`. The front end would need to keep track of how far long it has updated. The problem is what if multiple updates happen between polling? What could be done there is as part of the polling response I query and return all the combat log entries that have happened in this game/battle/battle_num. Its the full list in order. The FE goes through and sees where its at. If there is more then incrementally do more with all the timeouts needed. If there is no more, wait.

On post - the combat log queries for the previous state from the latest combat log entry. And then populates the resulting state. I think sqllite can store in json. Make the combat log write a human readable text string, as well as the previous/resulting state. Those could be in 1 field potentially. Or seperate, both could potentially work.

Change the initial page load to have previous and resulting state. Load the preivious state and then animate to the resulting state.

If loading the page for the first time and waiting for someone to go - just show whose turn it is.

If the next turn is the current gameuser - show them their battle options. For everyone else say its the other persons turn.

One thing to confirm with David that would be good is displaying the messages 1 by 1 for AOE. That will be important for how to implement.

And how to display buffs. If we indicate they did not get buffed any further and specifically which stats got buffed.

I like the idea of each combat log entry storing the previous and resulting state. That's way more manageable than each combat log storing the entire battle's progress. That's just unnessecary. Every time query the whole combat log.


```
{
    combat_log_id_1,
    combat_log_id_2,
    ... for every combat log in this battle
}
```

```
{
    combat_log_id_1,
    combat_log_id_2: {
        starting_state: {
            gameenemies: {
                id: {
                    name: 'Drunk Man 1',
                    hp: 85,
                    max_hp: 100,
                },
                id: {
                    name: 'Drunk Man 2',
                    hp: 72,
                    max_hp: 100,
                },
            },
            gameusers: {
                id: {
                    name: 'John',
                    hp: 100,
                    max_hp: 120,
                    with_gear_hp: 120,
                    mp: 100,
                    max_mp: 120,
                    with_gear_mp: 120,
                },
                id: {
                },
                id: {
                },
                id: {
                },
            }
        },
        resulting_state: {
            combat_log_message: 'John hit Drunk Man 1 with Divine Light for 10 damage. It was not very effective.',
            gameenemies: {
                id: {
                    name: 'Drunk Man 1',
                    hp: 75,
                    max_hp: 100,
                },
                id: {
                    name: 'Drunk Man 2',
                    hp: 72,
                    max_hp: 100,
                },
            },
            gameusers: {
                id: {
                    name: 'John',
                    hp: 100,
                    max_hp: 120,
                    with_gear_hp: 120,
                    mp: 90,
                    max_mp: 120,
                    with_gear_mp: 120,
                },
                id: {
                },
                id: {
                },
                id: {
                },
            },
        },
        // next_turn: {
        //    name: 'Paul',
        //    gameuserid: id,
        //    gameenemyid: NULL,
        // },
        errors: "error here if they did something wrong",
        next_url: "url here if they should be redirected at the end of animations".
    },
    combat_log_id_3: {
        ...
    },
    current_turn: {
        name: 'Paul',
        gameuserid: id,
        gameenemyid: NULL,
    }
}
```

Front end stores what the latest combat log entry is for that battle. If there are any keys after/greater than that, it goes to the next one and does it. if there are not it waits until the response starts having a new one.

Handle edge case when user loads page and enemy has gone first.

On page refresh - show the most recent combat log starting and resulting so they can know what just happened.

An issue with next_turn: I currently don't know who it will be the next turn. I only know the next turn when loading. So I'm commenting out next_turn becuase the response shouldn't need that. it only needs to know whose turn it currently is. That part of the response can come separately. It can come at the end when building the whole response where I calculate unit_turn and is_request_user_turn. Does that get calculated Outside of all the combat log entries? And then the front end checks if it's run all the previous animations and then displays the current_turn if its waiting.

Now how do players know which abilities they can cast? I think that also needs to be included in the polling response. It would include all 4 players and all the abilities they can cast, including the name, description, MP required, single target or aoe. Maybe the polling response only includes the abilities for that current player, they don't need to know the others.

```
{
    combat_logs {
        combat_log_id_1,
        combat_log_id_2: {
            starting_state: {
                gameenemies: {
                    id: {
                        name: 'Drunk Man 1',
                        hp: 85,
                        max_hp: 100,
                    },
                    id: {
                        name: 'Drunk Man 2',
                        hp: 72,
                        max_hp: 100,
                    },
                },
                gameusers: {
                    id: {
                        name: 'John',
                        hp: 100,
                        max_hp: 120,
                        with_gear_hp: 120,
                        mp: 100,
                        max_mp: 120,
                        with_gear_mp: 120,
                    },
                    id: {
                    },
                    id: {
                    },
                    id: {
                    },
                }
            },
            resulting_state: {
                combat_log_message: 'John hit Drunk Man 1 with Divine Light for 10 damage. It was not very effective.',
                gameenemies: {
                    id: {
                        name: 'Drunk Man 1',
                        hp: 75,
                        max_hp: 100,
                    },
                    id: {
                        name: 'Drunk Man 2',
                        hp: 72,
                        max_hp: 100,
                    },
                },
                gameusers: {
                    id: {
                        name: 'John',
                        hp: 100,
                        max_hp: 120,
                        with_gear_hp: 120,
                        mp: 90,
                        max_mp: 120,
                        with_gear_mp: 120,
                    },
                    id: {
                    },
                    id: {
                    },
                    id: {
                    },
                },
            },
            // not sure best place for errors and next_url in the flow. maybe start without these and then find the best place for them.
            errors: "error here if they did something wrong",
            next_url: "url here if they should be redirected at the end of animations".
        },
        combat_log_id_3: {
            ...
        },
    }
    turn: {
        // only show this on FE when all animations have finished and its not the current request user turn
        is_request_user_turn: false,
        gameuser: gameuser,
        gameenemy: NULL,
    },
    request_player_abilities: {
        ability {
            name: 'divine light',
            mp: 10,
            description: 'dope divine light on single target',
            type: 'heal',
        },
        abilityid2,
        abilityid3,
        abilityid4,
    }
}
```

in the json explore returning models vs breaking models apart into the json response.

This seems like a good starting point. 

Next steps:
- Combat log add act/battle_num
- Verify sqllite can do json responses
- Combat log add previous state and resulting state. decide if 1 or two columns
- Create a new polling route that returns all combat logs for this act/battle.
- Start modifying it to fit the shape to also include turn, request_player_abilities, and play with where to put the error and redirect
- Piece by piece implement the javascript to show combat log text and simultaneiously reduce MP and HP accordingly.
- When current player turn show them their abilities and UI to select and go back and execute.
- When not their turn keep progressing the combat from the polled response and animate through them each time there is a combat log entry with a greater ID than the current progress.

Its going to be DB load to request combat log every few seconds in combat. but that's the way it has to be.