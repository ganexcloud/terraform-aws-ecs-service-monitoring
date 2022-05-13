# Variables

variable "sns_topic_arn" {
  description = "A list of ARNs (i.e. SNS Topic ARN) to notify on alerts"
  type        = list(string)
}

variable "alarm_name_prefix" {
  description = "Alarm name prefix"
  type        = string
  default     = ""
}

variable "ecs_cluster_name" {
  description = "The instance ID of the RDS database instance that you want to monitor."
  type        = string
}

variable "ecs_service_name" {
  description = "The instance ID of the RDS database instance that you want to monitor."
  type        = string
}

# CPU
variable "cpu_alarm" {
  description = "Enable Alarm to metric: cpu"
  type        = bool
  default     = true
}

variable "cpu_threshold" {
  description = "The maximum percentage of CPU utilization."
  type        = string
  default     = 90
}

variable "cpu_comparison_operator" {
  description = "Comparison_operator to alarm"
  type        = string
  default     = "GreaterThanThreshold"
}

variable "cpu_datapoint" {
  description = "Datapoint check to alarm"
  type        = number
  default     = 15
}

variable "cpu_period" {
  description = "Period check to alarm (in seconds)"
  type        = number
  default     = 60
}

variable "cpu_priority" {
  description = "Priority of alarm"
  type        = string
  default     = "P3"
}

# Memory
variable "memory_alarm" {
  description = "Enable Alarm to metric: memory_too_high"
  type        = bool
  default     = true
}

variable "memory_threshold" {
  description = "The maximum percentage of memory utilization."
  type        = number
  default     = 90
}

variable "memory_comparison_operator" {
  description = "Comparison_operator to alarm"
  type        = string
  default     = "GreaterThanThreshold"
}

variable "memory_datapoint" {
  description = "Datapoint check to alarm"
  type        = number
  default     = 5
}

variable "memory_period" {
  description = "Period check to alarm (in seconds)"
  type        = number
  default     = 60
}

variable "memory_priority" {
  description = "Priority of alarm"
  type        = string
  default     = "P3"
}

variable "tags" {
  description = "(Optional) A map of tags to assign to the all resources"
  type        = map(string)
  default     = {}
}

variable "enable_ecs_task_state_event_rule" {
  description = "The boolean flag enabling the EvenBridge Rule for `ECS Task State Change` events. The `detail` section of this rule is configured with `ecs_task_state_event_rule_detail` variable."
  type        = bool
  default     = true
}

variable "enable_ecs_deployment_state_event_rule" {
  description = "The boolean flag enabling the EvenBridge Rule for `ECS Deployment State Change` events. The `detail` section of this rule is configured with `ecs_deployment_state_event_rule_detail` variable."
  type        = bool
  default     = true
}

variable "enable_ecs_service_action_event_rule" {
  description = "The boolean flag enabling the EvenBridge Rule for `ECS Service Action` events. The `detail` section of this rule is configured with `ecs_service_action_event_rule_detail` variable."
  type        = bool
  default     = true
}

variable "ecs_task_state_event_rule_detail" {
  description = "The content of the `detail` section in the EvenBridge Rule for `ECS Task State Change` events. Use it to filter the events which will be processed and sent to Slack."
  type        = any
  default = {
    lastStatus    = ["STOPPED"]
    stoppedReason = [{ "anything-but" : { "prefix" : "Scaling activity initiated by (deployment ecs-svc/" } }] # skip task stopped events triggerd by deployments
  }
}

variable "ecs_deployment_state_event_rule_detail" {
  description = "The content of the `detail` section in the EvenBridge Rule for `ECS Deployment State Change` events. Use it to filter the events which will be processed and sent to Slack."
  type        = any
  default = {
    eventType = ["ERROR"]
  }
}

variable "ecs_service_action_event_rule_detail" {
  description = "The content of the `detail` section in the EvenBridge Rule for `ECS Service Action` events. Use it to filter the events which will be processed and sent to Slack."
  type        = any
  default = {
    eventType = ["WARN", "ERROR"]
  }
}

variable "custom_event_rules" {
  description = "A map of objects representing the custom EventBridge rule which will be created in addition to the default rules."
  type = map(object({
    detail-type = any
    detail      = any
  }))
  default = {}
}
