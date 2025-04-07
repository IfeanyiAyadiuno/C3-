from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Inspector, InspectionTicket, InspectionSchedule
from datetime import datetime, timedelta
import calendar
from django.db import transaction
from django.db import connection
import time

# Create your views here.
def index(request):
    """主页视图，重定向到检查票列表页面"""
    return redirect('inspection_tickets')

def inspection_tickets(request):
    """显示所有检查票的列表"""
    # 打印请求信息
    print("\n" + "="*50)
    print(f"加载inspection_tickets视图 - 时间: {datetime.now()}")
    print(f"请求方法: {request.method}, 请求参数: {request.GET}")
    
    # 清除任何可能的查询缓存
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")  # 简单查询强制刷新连接
    
    # 使用select_related预加载inspector数据，减少数据库查询
    tickets = InspectionTicket.objects.select_related('inspector').all().order_by('-date_created')
    
    # 用于调试：打印每个ticket的状态和检查员信息
    for ticket in tickets:
        inspector_name = ticket.inspector.name if ticket.inspector else "未分配"
        print(f"Ticket #{ticket.ticket_number} - 状态: {ticket.status}, 检查员: {inspector_name}")
    
    context = {
        'tickets': tickets,
    }
    
    # 强制刷新页面，添加no-cache头
    response = render(request, 'inspection/inspection_tickets.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def assign_inspector(request):
    """显示并处理检查员分配的页面"""
    inspectors = Inspector.objects.all()
    
    # 调试信息：打印请求方法和参数
    print(f"请求方法: {request.method}")
    if request.method == 'GET':
        print(f"GET参数: {request.GET}")
    elif request.method == 'POST':
        print(f"POST参数: {request.POST}")
    
    # 检查是否提供了ticket_id
    ticket_id = request.GET.get('ticket_id')
    if not ticket_id:
        print("错误: 未提供ticket_id")
        return redirect('inspection_tickets')
    
    # 获取对应的ticket
    try:
        ticket = InspectionTicket.objects.get(id=ticket_id)
        print(f"成功获取ticket: id={ticket.id}, ticket_number={ticket.ticket_number}, status={ticket.status}")
    except InspectionTicket.DoesNotExist:
        print(f"错误: 找不到ID为{ticket_id}的票据")
        return redirect('inspection_tickets')
    
    if request.method == 'POST':
        inspector_id = request.POST.get('inspector_id')
        post_ticket_id = request.POST.get('ticket_id')
        
        print(f"接收到POST请求: inspector_id={inspector_id}, ticket_id={post_ticket_id}")
        
        if not inspector_id or not post_ticket_id:
            # 添加错误处理
            print(f"错误：参数不完整：inspector_id={inspector_id}, ticket_id={post_ticket_id}")
            return redirect('inspection_tickets')
        
        try:
            # 尝试常规的ORM更新方法
            ticket = InspectionTicket.objects.get(id=post_ticket_id)
            inspector = Inspector.objects.get(id=inspector_id)
            
            print(f"更新前 - ticket.id: {ticket.id}, inspector_id: {ticket.inspector_id}, status: {ticket.status}")
            
            # 保存旧值用于比较
            old_inspector_id = ticket.inspector_id
            old_status = ticket.status
            
            # 使用ORM进行更新
            ticket.inspector = inspector
            ticket.status = 'Assigned'
            ticket.save()
            
            # 验证更新是否成功
            updated_ticket = InspectionTicket.objects.get(id=post_ticket_id)
            print(f"使用ORM更新后 - inspector_id: {updated_ticket.inspector_id}, status: {updated_ticket.status}")
            
            # 检查值是否已更新
            if updated_ticket.inspector_id == old_inspector_id and updated_ticket.status == old_status:
                print("警告: 使用ORM更新似乎没有生效，尝试直接SQL更新")
                
                # 如果ORM更新失败，使用直接SQL
                with connection.cursor() as cursor:
                    # 确保使用正确的表名前缀
                    cursor.execute(
                        "UPDATE inspection_inspectionticket SET inspector_id = %s, status = %s WHERE id = %s",
                        [inspector_id, 'Assigned', post_ticket_id]
                    )
                    print(f"执行SQL: UPDATE inspection_inspectionticket SET inspector_id = {inspector_id}, status = 'Assigned' WHERE id = {post_ticket_id}")
                
                # 再次验证更新
                final_ticket = InspectionTicket.objects.get(id=post_ticket_id)
                print(f"SQL更新后 - inspector_id: {final_ticket.inspector_id}, status: {final_ticket.status}")
            
            # 添加时间戳强制浏览器刷新
            timestamp = int(time.time())
            
            # 强制提交数据库更改
            from django.db import transaction
            transaction.commit()
            print("已提交事务")
            
            # 清空Django缓存
            from django.db.models import signals
            for model in [InspectionTicket, Inspector]:
                signals.post_save.send(sender=model, instance=None)
            
            print("重定向到tickets列表页面")
            return redirect(f'/inspection/tickets/?updated={timestamp}')
        except Exception as e:
            # 捕获并打印任何错误
            print(f"分配过程中出错：{str(e)}")
            import traceback
            traceback.print_exc()
            return redirect('inspection_tickets')
    
    context = {
        'inspectors': inspectors,
        'ticket': ticket
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

def create_inspector(request):
    """创建新的检查员"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        status = request.POST.get('status', 'Available')
        address = request.POST.get('address')
        
        if name and phone and address:
            inspector = Inspector(
                name=name,
                phone=phone,
                status=status,
                address=address
            )
            inspector.save()
            
            return redirect('inspection_tickets')
    
    return render(request, 'inspection/create_inspector.html')
