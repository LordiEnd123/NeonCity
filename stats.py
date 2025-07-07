from menu_all.upgrade_menu import load_player_stats


class PlayerStatsManager:
    def __init__(self):
        stats = load_player_stats()
        self.stamina = stats["stamina"]
        self.max_stamina = stats["max_stamina"]
        self.stamina_depletion_rate = stats["stamina_depletion_rate"]
        self.stamina_regeneration_rate = stats["stamina_regeneration_rate"]
        self.gun_ammo = stats["gun_ammo"]

    def get_stat(self, stat_name):
        return getattr(self, stat_name, None)

    def set_stat(self, stat_name, value):
        if hasattr(self, stat_name):
            setattr(self, stat_name, value)

    def update_stamina(self, moving, accelerating, delta_time):
        if moving:
            if accelerating and self.stamina > 0:
                self.stamina -= self.stamina_depletion_rate * 2 * delta_time
            elif self.stamina > 0:
                pass
            else:
                self.stamina = 0
        else:
            if self.stamina < self.max_stamina:
                self.stamina += self.stamina_regeneration_rate * delta_time
                if self.stamina > self.max_stamina:
                    self.stamina = self.max_stamina