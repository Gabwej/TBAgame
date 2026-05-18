# this file makes encounter creation more compact (easier to make in large scale)

def dialog_event(
    text,
    background=None,
    sprite=None,
    options=None
):

    return {
        "type": "dialog",
        "text": text,
        "background": background,
        "encounter_sprite": sprite,
        "options": options or []
    }


def battle_event(
    enemy,
    next_id,
    background=None,
    sprite=None
):

    return {
        "type": "battle",
        "enemy": enemy,
        "next": next_id,
        "background": background,
        "encounter_sprite": sprite
    }