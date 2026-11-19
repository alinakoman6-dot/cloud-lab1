resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "lab2-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "1. Екземпляри: бажана і фактична кількість"
          region = var.aws_region
          view   = "timeSeries"
          stat   = "Maximum"
          period = 60
          yAxis  = { left = { min = 0 } }
          metrics = [
            ["ECS/ContainerInsights", "DesiredTaskCount", "ClusterName", aws_ecs_cluster.main.name, "ServiceName", aws_ecs_service.main.name, { label = "Бажана (Desired)" }],
            ["ECS/ContainerInsights", "RunningTaskCount", "ClusterName", aws_ecs_cluster.main.name, "ServiceName", aws_ecs_service.main.name, { label = "Фактична (Running)" }]
          ]
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "2. Завантаження процесора, %"
          region = var.aws_region
          view   = "timeSeries"
          stat   = "Average"
          period = 60
          yAxis  = { left = { min = 0, max = 100 } }
          annotations = {
            horizontal = [{ label = "Ціль масштабування 60%", value = 60 }]
          }
          metrics = [
            ["AWS/ECS", "CPUUtilization", "ClusterName", aws_ecs_cluster.main.name, "ServiceName", aws_ecs_service.main.name, { label = "CPU (середнє по екземплярах)" }]
          ]
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6
        properties = {
          title  = "3. Запити за хвилину"
          region = var.aws_region
          view   = "timeSeries"
          stat   = "Sum"
          period = 60
          yAxis  = { left = { min = 0 } }
          metrics = [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", aws_lb.main.arn_suffix, { label = "Запитів/хв" }]
          ]
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 6
        width  = 12
        height = 6
        properties = {
          title  = "4. Латентність p95, с"
          region = var.aws_region
          view   = "timeSeries"
          stat   = "p95"
          period = 60
          yAxis  = { left = { min = 0 } }
          annotations = {
            horizontal = [{ label = "Поріг 0.5 с", value = 0.5 }]
          }
          metrics = [
            ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", aws_lb.main.arn_suffix, { label = "p95" }]
          ]
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 12
        width  = 24
        height = 6
        properties = {
          title  = "5. Відповіді 5xx"
          region = var.aws_region
          view   = "timeSeries"
          stat   = "Sum"
          period = 60
          yAxis  = { left = { min = 0 } }
          metrics = [
            ["AWS/ApplicationELB", "HTTPCode_Target_5XX_Count", "LoadBalancer", aws_lb.main.arn_suffix, { label = "5xx від застосунку" }],
            ["AWS/ApplicationELB", "HTTPCode_ELB_5XX_Count", "LoadBalancer", aws_lb.main.arn_suffix, { label = "5xx від балансувальника" }]
          ]
        }
      }
    ]
  })
}

resource "aws_sns_topic" "alerts" {
  name = "lab2-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "lab2-cpu-high"
  alarm_description   = "CPU сервісу понад 70% протягом 2 хвилин"
  namespace           = "AWS/ECS"
  metric_name         = "CPUUtilization"
  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.main.name
  }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 2
  datapoints_to_alarm = 2
  threshold           = 70
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]  # лист при перевантаженні
  ok_actions    = [aws_sns_topic.alerts.arn]  # лист при поверненні до норми

  depends_on = [aws_ecs_service.main]
}