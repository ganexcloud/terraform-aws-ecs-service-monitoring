resource "aws_cloudwatch_metric_alarm" "cpu" {
  count               = var.cpu_alarm ? 1 : 0
  alarm_name          = "[${title(local.alarm_name_prefix)}] ecs-service-${var.ecs_service_name}-cpu-high"
  comparison_operator = var.cpu_comparison_operator
  evaluation_periods  = var.cpu_datapoint
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = var.cpu_period
  statistic           = "Average"
  threshold           = min(max(var.cpu_threshold, 0), 100)
  alarm_description   = "Average ECS Service ${var.ecs_service_name} CPU utilization over last ${var.cpu_period} minutes too high. (${var.cpu_priority})"
  alarm_actions       = var.sns_topic_arn
  ok_actions          = var.sns_topic_arn
  tags                = var.tags

  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName = var.ecs_service_name
  }
}

resource "aws_cloudwatch_metric_alarm" "memory" {
  count               = var.memory_alarm ? 1 : 0
  alarm_name          = "[${title(local.alarm_name_prefix)}] ecs-service-${var.ecs_service_name}-memory-high"
  comparison_operator = var.memory_comparison_operator
  evaluation_periods  = var.memory_datapoint
  metric_name         = "MemoryUtilization"
  namespace           = "AWS/ECS"
  period              = var.memory_period
  statistic           = "Average"
  threshold           = min(max(var.memory_threshold, 0), 100)
  alarm_description   = "Average ECS Service ${var.ecs_service_name} memory utilization over last ${var.memory_period} minutes too high. (${var.memory_priority})"
  alarm_actions       = var.sns_topic_arn
  ok_actions          = var.sns_topic_arn
  tags                = var.tags

  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName = var.ecs_service_name
  }
}

resource "aws_cloudwatch_event_rule" "this" {
  for_each = local.event_rules
  name     = "${var.ecs_service_name}-${each.key}"
  event_pattern = jsonencode({
    source      = [try(each.value.source, "aws.ecs")]
    detail-type = each.value.detail-type
    detail      = each.value.detail
  })

  tags = var.tags
}

resource "aws_cloudwatch_event_target" "this" {
  for_each = { for sns_topic_arn in local.event_rules_topic : "${sns_topic_arn.topic}.${sns_topic_arn.rule}" => sns_topic_arn }
  arn      = each.value.topic
  rule     = aws_cloudwatch_event_rule.this[each.value.rule].name
}
