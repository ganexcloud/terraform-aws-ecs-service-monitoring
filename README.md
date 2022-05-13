<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13.1 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 3.63 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 3.63 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_metric_alarm.cpu](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_cloudwatch_metric_alarm.memory](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_iam_account_alias.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_account_alias) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_alarm_name_prefix"></a> [alarm\_name\_prefix](#input\_alarm\_name\_prefix) | Alarm name prefix | `string` | `""` | no |
| <a name="input_cpu_alarm"></a> [cpu\_alarm](#input\_cpu\_alarm) | Enable Alarm to metric: cpu | `bool` | `true` | no |
| <a name="input_cpu_comparison_operator"></a> [cpu\_comparison\_operator](#input\_cpu\_comparison\_operator) | Comparison\_operator to alarm | `string` | `"GreaterThanThreshold"` | no |
| <a name="input_cpu_datapoint"></a> [cpu\_datapoint](#input\_cpu\_datapoint) | Datapoint check to alarm | `number` | `15` | no |
| <a name="input_cpu_period"></a> [cpu\_period](#input\_cpu\_period) | Period check to alarm (in seconds) | `number` | `60` | no |
| <a name="input_cpu_priority"></a> [cpu\_priority](#input\_cpu\_priority) | Priority of alarm | `string` | `"P3"` | no |
| <a name="input_cpu_threshold"></a> [cpu\_threshold](#input\_cpu\_threshold) | The maximum percentage of CPU utilization. | `string` | `90` | no |
| <a name="input_custom_event_rules"></a> [custom\_event\_rules](#input\_custom\_event\_rules) | A map of objects representing the custom EventBridge rule which will be created in addition to the default rules. | <pre>map(object({<br>    detail-type = any<br>    detail      = any<br>  }))</pre> | `{}` | no |
| <a name="input_ecs_cluster_name"></a> [ecs\_cluster\_name](#input\_ecs\_cluster\_name) | The instance ID of the RDS database instance that you want to monitor. | `string` | n/a | yes |
| <a name="input_ecs_deployment_state_event_rule_detail"></a> [ecs\_deployment\_state\_event\_rule\_detail](#input\_ecs\_deployment\_state\_event\_rule\_detail) | The content of the `detail` section in the EvenBridge Rule for `ECS Deployment State Change` events. Use it to filter the events which will be processed and sent to Slack. | `any` | <pre>{<br>  "eventType": [<br>    "ERROR"<br>  ]<br>}</pre> | no |
| <a name="input_ecs_service_action_event_rule_detail"></a> [ecs\_service\_action\_event\_rule\_detail](#input\_ecs\_service\_action\_event\_rule\_detail) | The content of the `detail` section in the EvenBridge Rule for `ECS Service Action` events. Use it to filter the events which will be processed and sent to Slack. | `any` | <pre>{<br>  "eventType": [<br>    "WARN",<br>    "ERROR"<br>  ]<br>}</pre> | no |
| <a name="input_ecs_service_name"></a> [ecs\_service\_name](#input\_ecs\_service\_name) | The instance ID of the RDS database instance that you want to monitor. | `string` | n/a | yes |
| <a name="input_ecs_task_state_event_rule_detail"></a> [ecs\_task\_state\_event\_rule\_detail](#input\_ecs\_task\_state\_event\_rule\_detail) | The content of the `detail` section in the EvenBridge Rule for `ECS Task State Change` events. Use it to filter the events which will be processed and sent to Slack. | `any` | <pre>{<br>  "lastStatus": [<br>    "STOPPED"<br>  ],<br>  "stoppedReason": [<br>    {<br>      "anything-but": {<br>        "prefix": "Scaling activity initiated by (deployment ecs-svc/"<br>      }<br>    }<br>  ]<br>}</pre> | no |
| <a name="input_enable_ecs_deployment_state_event_rule"></a> [enable\_ecs\_deployment\_state\_event\_rule](#input\_enable\_ecs\_deployment\_state\_event\_rule) | The boolean flag enabling the EvenBridge Rule for `ECS Deployment State Change` events. The `detail` section of this rule is configured with `ecs_deployment_state_event_rule_detail` variable. | `bool` | `true` | no |
| <a name="input_enable_ecs_service_action_event_rule"></a> [enable\_ecs\_service\_action\_event\_rule](#input\_enable\_ecs\_service\_action\_event\_rule) | The boolean flag enabling the EvenBridge Rule for `ECS Service Action` events. The `detail` section of this rule is configured with `ecs_service_action_event_rule_detail` variable. | `bool` | `true` | no |
| <a name="input_enable_ecs_task_state_event_rule"></a> [enable\_ecs\_task\_state\_event\_rule](#input\_enable\_ecs\_task\_state\_event\_rule) | The boolean flag enabling the EvenBridge Rule for `ECS Task State Change` events. The `detail` section of this rule is configured with `ecs_task_state_event_rule_detail` variable. | `bool` | `true` | no |
| <a name="input_memory_alarm"></a> [memory\_alarm](#input\_memory\_alarm) | Enable Alarm to metric: memory\_too\_high | `bool` | `true` | no |
| <a name="input_memory_comparison_operator"></a> [memory\_comparison\_operator](#input\_memory\_comparison\_operator) | Comparison\_operator to alarm | `string` | `"GreaterThanThreshold"` | no |
| <a name="input_memory_datapoint"></a> [memory\_datapoint](#input\_memory\_datapoint) | Datapoint check to alarm | `number` | `5` | no |
| <a name="input_memory_period"></a> [memory\_period](#input\_memory\_period) | Period check to alarm (in seconds) | `number` | `60` | no |
| <a name="input_memory_priority"></a> [memory\_priority](#input\_memory\_priority) | Priority of alarm | `string` | `"P3"` | no |
| <a name="input_memory_threshold"></a> [memory\_threshold](#input\_memory\_threshold) | The maximum percentage of memory utilization. | `number` | `90` | no |
| <a name="input_sns_topic_arn"></a> [sns\_topic\_arn](#input\_sns\_topic\_arn) | A list of ARNs (i.e. SNS Topic ARN) to notify on alerts | `list(string)` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | (Optional) A map of tags to assign to the all resources | `map(string)` | `{}` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->