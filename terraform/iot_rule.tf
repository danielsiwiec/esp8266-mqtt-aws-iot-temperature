resource "aws_iot_topic_rule" "temp_analytics" {
  name        = "temp_analytics"
  description = "Send temperature readings to DynamoDB"
  enabled     = true
  sql         = "SELECT *, timestamp() as timestamp FROM 'tempReading/bedroom'"
  sql_version = "2016-03-23"

  dynamodb {
    table_name = aws_dynamodb_table.iot-temp.name
    hash_key_field = "timestamp"
    hash_key_value = "$${timestamp()}"
    role_arn = aws_iam_role.iot_rule_role.arn
  }
}

resource "aws_iam_role" "iot_rule_role" {
  name = "iot_rule_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "iot.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "put_message_role" {
  name = "put_message_role"
  role = aws_iam_role.iot_rule_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": "dynamodb:PutItem",
        "Resource": "${aws_dynamodb_table.iot-temp.arn}"
    }
}
EOF
}