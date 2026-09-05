import sys
import gc
names = ['flgame.context', 'flgame.game_root', 'flgame.levels.layouts', 'flgame.levels.level', 'flgame.levels.tiles', 'flgame.objects.active_objects.active_object', 'flgame.objects.active_objects.ammo', 'flgame.objects.active_objects.exit', 'flgame.objects.active_objects.medikit', 'flgame.objects.dynamic_objects.dynamic_object', 'flgame.objects.dynamic_objects.entities.enemies.enemy', 'flgame.objects.dynamic_objects.entities.enemies.knight', 'flgame.objects.dynamic_objects.entities.enemies.skull', 'flgame.objects.dynamic_objects.entities.enemies.summoner', 'flgame.objects.dynamic_objects.entities.enemies.wizzard', 'flgame.objects.dynamic_objects.entities.entity', 'flgame.objects.dynamic_objects.entities.player', 'flgame.objects.dynamic_objects.projectiles.player_projectile', 'flgame.objects.dynamic_objects.projectiles.projectile', 'flgame.objects.dynamic_objects.projectiles.wizzard_projectile', 'flgame.objects.game_object', 'flgame.rendering.display', 'flgame.rendering.hud', 'flgame.rendering.renderer_3d', 'flgame.systems.object_manager', 'flgame.systems.physics_manager', 'flgame.weapons.weapon', 'flgame.weapons.weapon_manager', 'flgame.world']
ok_count = 0
fail_count = 0
for name in names:
    gc.collect()
    print('free before:', gc.mem_free())
    try:
        __import__(name)
        print('OK  ', name)
        ok_count += 1
    except Exception as e:
        print('FAIL', name)
        sys.print_exception(e)
        fail_count += 1
    gc.collect()
print('---')
print('ok:', ok_count, 'fail:', fail_count)
