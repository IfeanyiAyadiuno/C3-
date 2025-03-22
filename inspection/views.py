from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Inspector, InspectionTicket, InspectionSchedule
from datetime import datetime, timedelta
import calendar

# Create your views here.
def index(request):
    """主页视图，重定向到检查票列表页面"""
    return redirect('inspection_tickets')

def inspection_tickets(request):
    """显示所有检查票的列表"""
    tickets = InspectionTicket.objects.all().order_by('-date_created')
    
    context = {
        'tickets': tickets,
    }
    return render(request, 'inspection/inspection_tickets.html', context)

def assign_inspector(request):
    """显示并处理检查员分配的页面"""
    inspectors = Inspector.objects.all()
    
    if request.method == 'POST':
        inspector_id = request.POST.get('inspector_id')
        ticket_id = request.POST.get('ticket_id')
        
        ticket = get_object_or_404(InspectionTicket, id=ticket_id)
        inspector = get_object_or_404(Inspector, id=inspector_id)
        
        ticket.inspector = inspector
        ticket.status = 'Assigned'
        ticket.save()
        
        return redirect('inspection_tickets')
    
    context = {
        'inspectors': inspectors,
    }
    return render(request, 'inspection/assign_inspector.html', context)

def schedule_inspection(request, ticket_id=None):
    """安排检查日程的页面"""
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(InspectionTicket, id=ticket_id)
    
    # 获取当前月份的日历
    today = timezone.now()
    year = today.year
    month = today.month
    
    # 如果请求中包含年月参数，则使用请求的年月
    if request.GET.get('year') and request.GET.get('month'):
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))
    
    # 获取当月第一天和最后一天
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1])
    
    # 获取整月的日期列表
    days = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        days.append({
            'day': day,
            'date': datetime(year, month, day),
            'is_today': day == today.day and month == today.month and year == today.year
        })
    
    # 处理POST请求（保存日程）
    if request.method == 'POST' and ticket:
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        inspection_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        inspection_time = datetime.strptime(time_str, '%H:%M').time()
        
        # 检查是否已有日程，如果有则更新，否则创建新的
        schedule, created = InspectionSchedule.objects.get_or_create(
            ticket=ticket,
            defaults={
                'inspection_date': inspection_date,
                'inspection_time': inspection_time,
            }
        )
        
        if not created:
            schedule.inspection_date = inspection_date
            schedule.inspection_time = inspection_time
            schedule.save()
        
        return redirect('inspection_tickets')
    
    context = {
        'ticket': ticket,
        'days': days,
        'month_name': calendar.month_name[month],
        'year': year,
        'prev_month': (month - 1) if month > 1 else 12,
        'prev_year': year if month > 1 else year - 1,
        'next_month': (month + 1) if month < 12 else 1,
        'next_year': year if month < 12 else year + 1,
    }
    return render(request, 'inspection/schedule_inspection.html', context)

def create_inspection_ticket(request):
    """创建新的检查票"""
    if request.method == 'POST':
        # 生成唯一的票号
        last_ticket = InspectionTicket.objects.order_by('-id').first()
        if last_ticket:
            ticket_num = f"T{int(last_ticket.ticket_number[1:]) + 1:05d}"
        else:
            ticket_num = "T00001"
        
        # 创建新票
        ticket = InspectionTicket(
            ticket_number=ticket_num,
            inspection_type=request.POST.get('inspection_type'),
            company=request.POST.get('company'),
            vehicle_make=request.POST.get('vehicle_make'),
            vin=request.POST.get('vin'),
            priority=request.POST.get('priority', 'Normal'),
            tag=request.POST.get('tag', 'No Tag Assigned'),
        )
        ticket.save()
        
        return redirect('inspection_tickets')
    
    return render(request, 'inspection/create_ticket.html')
