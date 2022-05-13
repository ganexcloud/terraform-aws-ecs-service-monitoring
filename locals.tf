locals {
  alarm_name_prefix = title(var.alarm_name_prefix == "" ? data.aws_iam_account_alias.current.account_alias : var.alarm_name_prefix)
  event_rules = merge(
    var.enable_ecs_task_state_event_rule ? {
      ECSTaskStateChange = {
        detail-type = ["ECS Task State Change"]
        detail      = var.ecs_task_state_event_rule_detail
      }
    } : {},
    var.enable_ecs_deployment_state_event_rule ? {
      ECSDeploymentStateChange = {
        detail-type = ["ECS Deployment State Change"]
        detail      = var.ecs_deployment_state_event_rule_detail
      }
    } : {},
    var.enable_ecs_service_action_event_rule ? {
      ECSServiceAction = {
        detail-type = ["ECS Service Action"]
        detail      = var.ecs_service_action_event_rule_detail
      }
    } : {},
    var.custom_event_rules
  )
  event_rules_topic = flatten([
    for topic in var.sns_topic_arn : [
      for rule in keys(local.event_rules) : {
        rule  = rule
        topic = topic
      }
    ]
  ])
}
