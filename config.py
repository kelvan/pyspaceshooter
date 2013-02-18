import powerup

size = (1024, 600)
music = True
sound = True
castSpeed = 100

levels = [{'spawns': 1000, 'spawnSpeed': 2000, 'powerUpSpeed': 12000},
          {'spawns': 2000, 'spawnSpeed': 1500, 'powerUpSpeed': 10000}]

powerups = [powerup.SpeedPowerUp,
            powerup.ReloadSpeedPowerUp,
            powerup.BulletSpeedPowerUp,
            powerup.PowerPowerUp,
            powerup.SlowDownPowerUp]
