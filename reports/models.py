from django.db import models
from django.contrib.auth.models import User

class AccountantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    station_name = models.CharField(max_length=100, verbose_name="Название АЗС / Город")
    
    class Meta:
        verbose_name = "Профиль бухгалтера"
        verbose_name_plural = "Профили бухгалтеров"

    def __str__(self):
        return f"{self.user.username} — {self.station_name}"

class FuelReport(models.Model):
    accountant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Бухгалтер")
    date = models.DateField(verbose_name="Дата смены")
    
    # === ТОПЛИВО: ОСТАТКИ И ПРОДАЖИ ===
    ai92_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="АИ-92 остаток")
    ai92_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="АИ-92 продажа")
    
    ai95_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="АИ-95 остаток")
    ai95_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="АИ-95 продажа")
    
    dt_summer_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ДТ Лето остаток")
    dt_summer_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ДТ Лето продажа")
    
    # ДОБАВЛЕНЫ НОВЫЕ ВИДЫ ТОПЛИВА
    dt_euro_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ДТ Евро остаток")
    dt_euro_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ДТ Евро продажа")
    
    gas_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Газ остаток")
    gas_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Газ продажа")
    
    # === ДЕНЬГИ: РАСШИФРОВКА ПРОДАЖ ===
    cash_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Наличные")
    card_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Банк")
    invoice_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Ведомость")  # Переименовал для порядка
    
    # === КАССА (НОВЫЕ ПОЛЯ) ===
    not_handed_shifts = models.IntegerField(default=0, verbose_name="Не сдано смен")
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Остаток ден. средств")
    discount_rub = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Скидка покупателям")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отчет АЗС"
        verbose_name_plural = "Отчеты АЗС"
        # ВОТ ЭТО ГАРАНТИРУЕТ ЗАМЕНУ ДАННЫХ ПРИ ПОВТОРНОЙ ОТПРАВКЕ
        unique_together = ('accountant', 'date') 
        
    def __str__(self):
        return f"{self.accountant.username} — {self.date}"