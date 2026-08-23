import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from .models import AccountantProfile, FuelReport
from django.utils.safestring import mark_safe

# Функция безопасности: превращает любые "кривые" данные в 0
def safe_decimal(value):
    try:
        val = Decimal(str(value).replace(',', '.'))
        return val if val >= 0 else Decimal('0')
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0')

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('chief_dashboard')
    else:
        return redirect('accountant_dashboard')

@login_required
def accountant_dashboard(request):
    station_name = "АЗС не назначена"
    try:
        station_name = request.user.profile.station_name
    except AccountantProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        # ✅ ИСПРАВЛЕНИЕ: Берем дату из формы, а не из "сегодня"
        report_date = request.POST.get('report_date')
        
        # Если дата не пришла или пустая — используем сегодня как запасной вариант
        if not report_date:
            report_date = date.today().isoformat()
            
        FuelReport.objects.update_or_create(
            accountant=request.user,
            date=report_date,  # <-- Теперь здесь реальная выбранная дата
            defaults={
                'ai92_stock': safe_decimal(request.POST.get('ai92_stock')),
                'ai92_sold': safe_decimal(request.POST.get('ai92_sold')),
                'ai95_stock': safe_decimal(request.POST.get('ai95_stock')),
                'ai95_sold': safe_decimal(request.POST.get('ai95_sold')),
                'dt_summer_stock': safe_decimal(request.POST.get('dt_summer_stock')),
                'dt_summer_sold': safe_decimal(request.POST.get('dt_summer_sold')),
                'dt_euro_stock': safe_decimal(request.POST.get('dt_euro_stock')),
                'dt_euro_sold': safe_decimal(request.POST.get('dt_euro_sold')),
                'gas_stock': safe_decimal(request.POST.get('gas_stock')),
                'gas_sold': safe_decimal(request.POST.get('gas_sold')),
                'cash_sales': safe_decimal(request.POST.get('cash_sales')),
                'card_sales': safe_decimal(request.POST.get('card_sales')),
                'invoice_sales': safe_decimal(request.POST.get('invoice_sales')),
                'not_handed_shifts': safe_decimal(request.POST.get('not_handed_shifts')),
                'cash_balance': safe_decimal(request.POST.get('cash_balance')),
                'discount_rub': safe_decimal(request.POST.get('discount_rub')),
            }
        )
        messages.success(request, f'✅ Данные за {report_date} успешно сохранены!')
        return redirect('accountant_dashboard')

    context = {
        'station_name': station_name,
        'current_user': request.user.username,
        'today': date.today().isoformat()
    }
    return render(request, 'reports/accountant_dashboard.html', context)

@login_required
def chief_dashboard(request):
    selected_date = request.GET.get('date', date.today().isoformat())
    
    # 1. Получаем ВСЕ профили АЗС
    all_profiles = AccountantProfile.objects.select_related('user').order_by('id')
    
    # 2. Словарь отчетов за выбранную дату
    reports_dict = {}
    for report in FuelReport.objects.filter(date=selected_date).select_related('accountant__profile'):
        reports_dict[report.accountant_id] = report
    
    # 3. Собираем данные И СРАЗУ ПРЕВРАЩАЕМ ИХ В ПРОСТОЙ СЛОВАРЬ (JSON-friendly)
    final_data = []
    for profile in all_profiles:
        report = reports_dict.get(profile.user_id)
        
        item = {
            'station_name': profile.station_name,
            'has_data': bool(report),
            'total_remainder': 0,
            'total_sold': 0,
            'total_money': 0,
            'report': None
        }
        
        if report:
            def to_float(val):
                return float(val) if val is not None else 0.0
            
            item['report'] = {
                'ai92_stock': to_float(report.ai92_stock),
                'ai95_stock': to_float(report.ai95_stock),
                'dt_euro_stock': to_float(report.dt_euro_stock),
                'dt_summer_stock': to_float(report.dt_summer_stock),
                'gas_stock': to_float(report.gas_stock),
                
                'ai92_sold': to_float(report.ai92_sold),
                'ai95_sold': to_float(report.ai95_sold),
                'dt_euro_sold': to_float(report.dt_euro_sold),
                'dt_summer_sold': to_float(report.dt_summer_sold),
                'gas_sold': to_float(report.gas_sold),
                
                'cash_sales': to_float(report.cash_sales),
                'card_sales': to_float(report.card_sales),
                'invoice_sales': to_float(report.invoice_sales),
                
                'not_handed_shifts': int(report.not_handed_shifts) if report.not_handed_shifts else 0,
                'cash_balance': to_float(report.cash_balance),
                'discount_rub': to_float(report.discount_rub),
            }
            
            r = item['report']
            item['total_remainder'] = r['ai92_stock'] + r['ai95_stock'] + r['dt_euro_stock'] + r['dt_summer_stock'] + r['gas_stock']
            item['total_sold'] = r['ai92_sold'] + r['ai95_sold'] + r['dt_euro_sold'] + r['dt_summer_sold'] + r['gas_sold']
            item['total_money'] = r['cash_sales'] + r['card_sales'] + r['invoice_sales']
            
        final_data.append(item)
    
    # ✅ ПРАВИЛЬНО: один общий context, а не два отдельных!
    json_data = json.dumps(final_data, ensure_ascii=False, default=str)
    
    context = {
        'stations_data': final_data,              # Для HTML-таблиц
        'stations_data_json': mark_safe(json_data),  # Для JavaScript
        'selected_date': selected_date,
    }
    print("Дата:", selected_date)
    print("Отчетов:", FuelReport.objects.filter(date=selected_date).count())
    return render(request, 'reports/chief_dashboard.html', context)