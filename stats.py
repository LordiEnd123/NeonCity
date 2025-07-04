import config_stats

class PlayerStatsManager:
    def __init__(self):
        # Инициализация характеристик игрока из config_stats.py
        self.stamina = config_stats.player_stats["stamina"]
        self.max_stamina = config_stats.player_stats["max_stamina"]
        self.stamina_depletion_rate = config_stats.player_stats["stamina_depletion_rate"]
        self.stamina_regeneration_rate = config_stats.player_stats["stamina_regeneration_rate"]

    def get_stat(self, stat_name):
        """Возвращает значение статистики."""
        return getattr(self, stat_name, None)

    def set_stat(self, stat_name, value):
        """Устанавливает значение статистики."""
        if hasattr(self, stat_name):
            setattr(self, stat_name, value)

    def update_stamina(self, moving, accelerating, delta_time):
        """Обновление выносливости (уменьшение при ускорении, восстановление с течением времени)."""
        if moving:
            if accelerating and self.stamina > 0:
                # Увеличиваем расход выносливости, если ускоряемся
                self.stamina -= self.stamina_depletion_rate * 2 * delta_time  # Ускорение тратит больше выносливости
            elif self.stamina > 0:
                # Если не ускоряемся, но двигаемся, выносливость не тратится
                pass
            else:
                self.stamina = 0  # Не даем выносливости стать отрицательной
        else:
            # Восстановление выносливости, если персонаж не двигается
            if self.stamina < self.max_stamina:
                self.stamina += self.stamina_regeneration_rate * delta_time
                if self.stamina > self.max_stamina:
                    self.stamina = self.max_stamina  # Не даем выносливости выйти за пределы макс. значения